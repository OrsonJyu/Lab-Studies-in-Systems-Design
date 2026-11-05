"""Tests for recorder.py. Unit tests need nothing; the synthetic-stream tests
need ffmpeg/ffprobe with libx264 on PATH and take about 40 seconds."""
import json, os, shutil, subprocess, sys, tempfile, threading, time, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recorder
from recorder import (EventTracker, FrameAnalyzer, MotionRules, Segment, gaps_between, motion_filter,
                      polygon_mask, valid_roi,
                      select_segments, stamp_segments)


class TrackerTests(unittest.TestCase):
    def test_single_motion_closes_after_still_period(self):
        t = EventTracker(still_s=5, max_event_s=300)
        self.assertEqual(t.motion(100), [])
        self.assertEqual(t.poll(104.9), [])
        [e] = t.poll(105)
        self.assertEqual((e.start, e.end, e.close_reason), (100, 105, 'still'))
        self.assertIsNone(t.open)

    def test_motion_within_still_period_extends_same_event(self):
        t = EventTracker(5, 300)
        t.motion(100)
        t.motion(103)
        self.assertEqual(t.poll(107), [])
        [e] = t.poll(108)
        self.assertEqual((e.start, e.end, len(e.motions)), (100, 108, 2))

    def test_held_motion_keeps_event_open_until_hold_ends(self):
        t = EventTracker(5, 300)
        t.motion(100, 110)
        self.assertEqual(t.poll(114), [])
        [e] = t.poll(115)
        self.assertEqual(e.end, 115)

    def test_late_motion_after_missed_poll_starts_new_event(self):
        t = EventTracker(5, 300)
        t.motion(100)
        [closed] = t.motion(106)
        self.assertEqual((closed.start, closed.end), (100, 105))
        self.assertEqual(t.open.start, 106)

    def test_dense_motion_frames_merge_into_intervals(self):
        t = EventTracker(5, 300)
        for i in range(10):
            t.motion(100 + i * 0.1, source='motion')
        t.motion(103, source='motion')
        t.motion(103.5, source='manual')
        self.assertEqual(t.open.motions, [[100, 100.9], [103, 103.5]])
        self.assertEqual(t.open.sources, {'motion', 'manual'})

    def test_max_event_length(self):
        t = EventTracker(5, 20)
        t.motion(100, 200)
        [e] = t.poll(120)
        self.assertEqual((e.end, e.close_reason), (120, 'max_event_s'))


M = dict(recorder.DEFAULTS['motion'], width=40, height=20, mask=[])


def frame(*rects):
    """40x20 difference frame with 255 inside each (x0, y0, x1, y1) pixel rectangle."""
    f = bytearray(40 * 20)
    for x0, y0, x1, y1 in rects:
        for y in range(y0, y1):
            f[y * 40 + x0:y * 40 + x1] = b'\xff' * (x1 - x0)
    return bytes(f)


class AnalyzerTests(unittest.TestCase):
    def test_polygon_mask_covers_inside_only(self):
        m = polygon_mask([[0.25, 0], [0.75, 0], [0.75, 1], [0.25, 1]], 40, 20)
        self.assertEqual(m.count(1), 20 * 20)
        self.assertEqual((m[9], m[10], m[29], m[30]), (0, 1, 1, 0))

    def test_valid_roi(self):
        self.assertIsNone(valid_roi([[0, 0], [1, 0]]))
        self.assertIsNone(valid_roi([[0, 0], [1.2, 0], [1, 1]]))
        self.assertIsNone(valid_roi([[0, 0], [0.5, 0.5], [1, 1]]))       # no area
        self.assertEqual(valid_roi([[0, 0], [1, 0], ['1', 1]]), [[0, 0], [1, 0], [1, 1]])

    def test_small_object_inside_area_is_motion(self):
        r = FrameAnalyzer(M).analyze(frame((10, 5, 13, 8)))
        self.assertEqual(r['verdict'], 'motion')
        self.assertEqual(r['box'], [0.25, 0.25, 0.325, 0.4])

    def test_change_outside_area_is_ignored(self):
        a = FrameAnalyzer(M, roi=[[0, 0], [0.5, 0], [0.5, 1], [0, 1]])
        self.assertEqual(a.analyze(frame((30, 5, 34, 9)))['verdict'], 'still')
        self.assertEqual(a.analyze(frame((10, 5, 14, 9)))['verdict'], 'motion')

    def test_whole_picture_change_is_scene(self):
        self.assertEqual(FrameAnalyzer(M).analyze(frame((0, 0, 40, 10)))['verdict'], 'scene')

    def test_noise_and_oversized_regions(self):
        a = FrameAnalyzer(M)
        self.assertEqual(a.analyze(frame((3, 3, 4, 4), (20, 10, 21, 11)))['verdict'], 'small')
        # 160 px: 20% of the picture (not a scene) but 40% of the left-half area (> 35%).
        half = FrameAnalyzer(M, roi=[[0, 0], [0.5, 0], [0.5, 1], [0, 1]])
        self.assertEqual(half.analyze(frame((0, 0, 20, 8)))['verdict'], 'large')

    def test_size_filter_off_counts_any_change(self):
        a = FrameAnalyzer(dict(M, size_filter=False))
        self.assertEqual(a.analyze(frame((3, 3, 4, 4)))['verdict'], 'motion')        # 1 px
        self.assertEqual(a.analyze(frame((0, 0, 20, 10)))['verdict'], 'motion')      # 25%, not a scene
        self.assertEqual(a.analyze(frame((0, 0, 40, 10)))['verdict'], 'scene')       # scene rule stays

    def test_osd_mask_is_excluded(self):
        a = FrameAnalyzer(dict(M, mask=[[0, 0, 0.5, 0.5]]))
        self.assertEqual(a.analyze(frame((2, 2, 8, 8)))['verdict'], 'still')


class RulesTests(unittest.TestCase):
    def run_rules(self, verdicts):
        r = MotionRules(fps=10, persist_s=0.3, max_gap_frames=1, scene_cooldown_s=1.0)
        out, scenes = [], []
        for i, v in enumerate(verdicts):
            times, scene = r.frame(i / 10, v)
            out += times
            if scene:
                scenes.append(i / 10)
        return out, scenes

    def test_motion_must_persist_and_starts_at_first_frame(self):
        out, _ = self.run_rules(['motion', 'motion', 'still', 'still', 'motion', 'motion', 'motion', 'motion'])
        self.assertEqual(out, [0.4, 0.5, 0.6, 0.7])      # the first two frames were too short

    def test_single_dropout_is_tolerated(self):
        out, _ = self.run_rules(['motion', 'small', 'motion', 'motion'])
        self.assertEqual(out, [0.0, 0.2, 0.3])

    def test_scene_change_suppresses_motion_during_cooldown(self):
        out, scenes = self.run_rules(['scene', 'motion', 'motion', 'motion', 'scene'] + ['motion'] * 14)
        self.assertEqual(scenes, [0.0])                  # the second one is inside the cooldown
        self.assertEqual(out, [1.4, 1.5, 1.6, 1.7, 1.8])  # cooldown runs to 0.4 + 1.0 s


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg not installed')
class MotionFilterTests(unittest.TestCase):
    def verdicts(self, graph, roi=None):
        m = dict(recorder.DEFAULTS['motion'], mask=[])
        r = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error', '-f', 'lavfi',
                            '-i', graph, '-t', '2', '-vf', motion_filter(m), '-f', 'rawvideo',
                            '-pix_fmt', 'gray', '-'], capture_output=True, check=True)
        a, n = FrameAnalyzer(m, roi), m['width'] * m['height']
        # Each output frame: grey change, colour change, Y, U, V.
        return [a.analyze(r.stdout[i:i + n])['verdict'] for i in range(0, len(r.stdout) - 5 * n + 1, 5 * n)]

    moving_square = ("color=c=gray:s=320x180:r=20[bg];color=c=white:s=16x16:r=20[fg];"
                     "[bg][fg]overlay=x='40+40*t':y=80")

    def test_moving_square_is_motion(self):
        self.assertIn('motion', self.verdicts(self.moving_square))

    def test_area_elsewhere_ignores_it(self):
        right = [[0.6, 0], [1, 0], [1, 1], [0.6, 1]]
        self.assertNotIn('motion', self.verdicts(self.moving_square, right))

    def test_brightness_jump_is_scene(self):
        graph = ("color=c=0x505050:s=320x180:r=20:d=1[a];color=c=0xb0b0b0:s=320x180:r=20:d=1[b];"
                 "[a][b]concat")
        self.assertIn('scene', self.verdicts(graph))
class SegmentTests(unittest.TestCase):
    segs = [Segment(f's{i}', 100 + 2 * i, 102 + 2 * i, 1) for i in range(10)]

    def test_select_covers_window_at_segment_boundaries(self):
        chosen = select_segments(self.segs, 103.5, 109)
        self.assertEqual([s.path for s in chosen], ['s1', 's2', 's3', 's4'])

    def test_stamps_come_from_file_mtimes_not_poll_time(self):
        # Regression: on the ROCK, polling late (while a clip was being joined)
        # stamped segments late and the error accumulated, cutting clip tails.
        d = Path(tempfile.mkdtemp())
        for i, mtime in enumerate([1000.0, 1002.05, 1003.98]):
            p = d / f'seg-{i}.ts'
            p.write_bytes(b'x')
            os.utime(p, (mtime, mtime))
        rows = [['seg-0.ts', '0', '2'], ['seg-1.ts', '2', '4'], ['seg-2.ts', '4', '6']]
        time.sleep(0.2)   # "poll" well after the files were written
        segs = stamp_segments(d, rows, None, 1)
        self.assertEqual([(round(s.wall_start, 3), round(s.wall_end, 3)) for s in segs],
                         [(998.0, 1000.0), (1000.0, 1002.05), (1002.05, 1003.98)])
        more = stamp_segments(d, [['missing.ts', '6', '8']], segs[-1].wall_end, 1)
        self.assertEqual(more, [])
        shutil.rmtree(d)

    def test_gap_detection(self):
        segs = [Segment('a', 0, 2, 1), Segment('b', 2, 4, 1), Segment('c', 7, 9, 2)]
        self.assertEqual(gaps_between(segs), [[4, 7]])


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'ffmpeg not installed')
class SyntheticStreamTest(unittest.TestCase):
    """Real-time test pattern -> segments -> one manual trigger -> clip with pre-roll."""

    def test_trigger_produces_clip_with_pre_roll(self):
        tmp = Path(tempfile.mkdtemp())
        cfg_path = tmp / 'config.json'
        cfg_path.write_text(json.dumps({
            'ring_dir': str(tmp / 'ring'), 'output_dir': str(tmp / 'events'),
            'pre_roll_s': 4, 'still_s': 3, 'ring_seconds': 30, 'min_free_mb': 1,
            'input_args': ['-re', '-f', 'lavfi', '-i', 'testsrc2=size=320x240:rate=20'],
            'codec_args': ['-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
                           '-g', '40', '-keyint_min', '40', '-sc_threshold', '0'],
        }))
        cfg = recorder.load_config(cfg_path)
        rec = recorder.Recorder(cfg)
        worker = threading.Thread(target=rec.loop)
        worker.start()
        try:
            time.sleep(10)                     # fill the ring
            recorder.write_trigger(cfg, 0)
            trigger = time.time()
            deadline = trigger + 20
            while time.time() < deadline and not list((tmp / 'events').glob('*.json')):
                time.sleep(0.5)
        finally:
            rec.stopping = True
            worker.join(15)
        [record_path] = (tmp / 'events').glob('*.json')
        record = json.loads(record_path.read_text())
        self.assertEqual(record['status'], 'ok', record)
        self.assertGreaterEqual(record['actual_pre_roll_s'], 4 - 0.3)
        self.assertLessEqual(record['actual_pre_roll_s'], 4 + 2 + 0.5)
        # pre-roll (4..6 s) + still period (3 s) + up to one segment of tail
        self.assertGreater(record['duration_s'], 6.5)
        self.assertLess(record['duration_s'], 12)
        mp4 = tmp / 'events' / record['file']
        decode = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(mp4), '-f', 'null', '-'],
                                capture_output=True, text=True)
        self.assertEqual(decode.returncode, 0, decode.stderr)
        shutil.rmtree(tmp)


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'ffmpeg not installed')
class SyntheticMotionTest(unittest.TestCase):
    """Moving pattern visible from 10 s to 12 s -> detector opens one event by itself."""

    def test_detected_motion_produces_one_clip(self):
        tmp = Path(tempfile.mkdtemp())
        graph = ("color=c=gray:s=320x240:r=20[bg];testsrc2=s=100x100:r=20[fg];"
                 "[bg][fg]overlay=110:70:enable='between(t,10,12)'")
        cfg_path = tmp / 'config.json'
        cfg_path.write_text(json.dumps({
            'ring_dir': str(tmp / 'ring'), 'output_dir': str(tmp / 'events'),
            'pre_roll_s': 4, 'still_s': 3, 'ring_seconds': 30, 'min_free_mb': 1,
            'input_args': ['-re', '-f', 'lavfi', '-i', graph],
            'codec_args': ['-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
                           '-g', '40', '-keyint_min', '40', '-sc_threshold', '0'],
            'motion': {'enabled': True, 'trigger': 'change', 'input_args': ['-re', '-f', 'lavfi', '-i', graph]},
        }))
        cfg = recorder.load_config(cfg_path)
        rec = recorder.Recorder(cfg)
        started = time.time()
        worker = threading.Thread(target=rec.loop)
        worker.start()
        try:
            deadline = started + 30
            while time.time() < deadline and not list((tmp / 'events').glob('*.json')):
                time.sleep(0.5)
        finally:
            rec.stopping = True
            worker.join(15)
        records = [json.loads(p.read_text()) for p in (tmp / 'events').glob('*.json')]
        self.assertEqual(len(records), 1, records)
        r = records[0]
        self.assertEqual((r['status'], r['source']), ('ok', 'motion'), r)
        first = r['first_motion'] - started
        self.assertTrue(9.5 < first < 11.5, first)          # pattern appears at 10 s
        self.assertTrue(11.5 < r['last_motion'] - started < 13, r['last_motion'] - started)
        self.assertGreaterEqual(r['actual_pre_roll_s'], 4 - 0.3)
        shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main()
