"""Tests for tracker.py with synthetic frames (no ffmpeg needed)."""
import shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracker import Tracker

W, H = 40, 30
AREA = bytes([1]) * (W * H)


def scene(objects, base=200):
    """Grey frame: background `base`, each (x, y, w, h, value) drawn on top."""
    f = bytearray([base]) * (W * H)
    for x, y, w, h, v in objects:
        for yy in range(y, y + h):
            f[yy * W + x:yy * W + x + w] = bytes([v]) * w
    return bytes(f)


def change(a, b):
    return bytes(1 if abs(p - q) > 25 else 0 for p, q in zip(a, b))


class Run:
    """Feed frames at 10 fps; keeps the previous frame for the change image."""

    def __init__(self, **cfg):
        self.tr = Tracker(cfg, W, H, AREA)
        self.t, self.prev = 0.0, None

    def feed(self, frame, n=1, scene_change=False):
        out = None
        for i in range(n):
            ch = change(frame, self.prev) if self.prev else bytes(W * H)
            out = self.tr.frame(self.t, frame, ch, scene=scene_change and i == 0)
            self.prev, self.t = frame, self.t + 0.1
        return out


GECKO = (5, 12, 6, 3, 90)


def at(x):
    return (x, 12, 6, 3, 90)


class TrackerTests(unittest.TestCase):
    def start_with_gecko_in_background(self):
        r = Run()
        self.assertEqual(r.feed(scene([GECKO]))['state'], 'learning')
        self.assertEqual(r.feed(scene([GECKO]), 40)['state'], 'searching')   # gecko is in the background
        return r

    def test_first_move_locks_target_and_absorbs_ghost(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 26):                       # walks right, 1 px per frame
            s = r.feed(scene([at(x)]))
        self.assertEqual(s['state'], 'moving')
        self.assertAlmostEqual(s['x'], (25 + 3) / W, delta=0.03)
        s = r.feed(scene([at(25)]), 30)              # rests 3 s
        self.assertEqual(s['state'], 'still')
        self.assertAlmostEqual(s['x'], (25 + 3) / W, delta=0.03)
        # The spot it left (substrate, unlike the start-up background) was absorbed.
        fg = r.tr._foreground(scene([at(25)]), bytes(W * H))
        self.assertEqual(len(fg), 1)
        self.assertGreater(fg[0].cx, 20)

    def test_long_rest_keeps_lock_and_confirms(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 26):
            r.feed(scene([at(x)]))
        s = r.feed(scene([at(25)]), 600)             # one minute still
        self.assertEqual(s['state'], 'still')
        self.assertGreater(s['last_confirmed'], r.t - 6)
        self.assertGreater(r.t - s['still_since'], 55)

    def test_scene_change_rebuilds_background_and_keeps_target(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 26):
            r.feed(scene([at(x)]))
        r.feed(scene([at(25)]), 20)
        lit = scene([(25, 12, 6, 3, 130)], base=240)     # lights on: everything brighter
        s = r.feed(lit, 1, scene_change=True)
        self.assertTrue(s['learning'])
        s = r.feed(lit, 60)
        self.assertFalse(s['learning'])
        self.assertIn(s['state'], ('still', 'lost'))     # brighter gecko may not match
        self.assertAlmostEqual(s['x'], (25 + 3) / W, delta=0.03)
        for x in range(26, 32):                          # moves again: picked up again
            s = r.feed(scene([(x, 12, 6, 3, 130)], base=240))
        self.assertEqual(s['state'], 'moving')
        s = r.feed(scene([(31, 12, 6, 3, 130)], base=240), 30)   # ghost part absorbed
        self.assertEqual(s['state'], 'still')
        self.assertAlmostEqual(s['x'], (31 + 3) / W, delta=0.03)

    def test_hand_is_never_the_target(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 16):
            r.feed(scene([at(x)]))
        r.feed(scene([at(15)]), 10)
        for y in range(0, 10):                           # big hand sweeps across the top
            s = r.feed(scene([at(15), (0, y, 36, 16, 40)]))   # 48% of the area
        self.assertAlmostEqual(s['x'], (15 + 3) / W, delta=0.03)

    def test_carried_far_is_found_by_appearance(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 12):
            r.feed(scene([at(x)]))
        r.feed(scene([at(11)]), 30)                      # rests 3 s: ghost part absorbed
        s = r.feed(scene([(30, 22, 6, 3, 90)]), 10)      # put down far away, then still
        self.assertAlmostEqual(s['x'], (30 + 3) / W, delta=0.03)
        self.assertAlmostEqual(s['y'], (22 + 1.5) / H, delta=0.05)


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg not installed')
class DetectorPipelineTest(unittest.TestCase):
    """Real FFmpeg pipeline: a dark square sits still for 4 s, slides right for 2 s,
    then rests. The tracker should lock on and report it resting at the new spot."""

    def test_square_is_tracked_through_the_detector(self):
        import recorder
        graph = ("color=c=0xc8c8c8:s=320x180:r=10[bg];color=c=0x404040:s=24x12:r=10[fg];"
                 "[bg][fg]overlay=x='if(lt(t,4),60,if(lt(t,6),60+60*(t-4),180))':y=90")
        tmp = Path(tempfile.mkdtemp())
        cfg = recorder.load_config(None)
        cfg['output_dir'] = str(tmp)
        cfg['motion'].update(enabled=True, mask=[], roi_file=str(tmp / 'roi.json'),
                             input_args=['-re', '-f', 'lavfi', '-i', graph, '-t', '10'])
        det = recorder.MotionDetector(cfg, lambda *a, **k: None)
        det.proc.wait(20)
        det.thread.join(5)
        det.proc.stdout.close()
        st = det.track_state
        shutil.rmtree(tmp)
        self.assertEqual(st['state'], 'still', st)
        self.assertAlmostEqual(st['x'], (180 + 12) / 320, delta=0.03)
        self.assertAlmostEqual(st['y'], (90 + 6) / 180, delta=0.04)


if __name__ == '__main__':
    unittest.main()
