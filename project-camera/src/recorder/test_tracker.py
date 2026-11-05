"""Tests for tracker.py with synthetic frames (no ffmpeg needed)."""
import shutil, sys, tempfile, time, unittest
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
        fg = r.tr._foreground((scene([at(25)]),), set())
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
        # Moves again. While it still touches its own image in the rebuilt background only
        # the part outside that spot is visible, so it takes a little longer to read as moving.
        for x in range(26, 34):
            s = r.feed(scene([(x, 12, 6, 3, 130)], base=240))
        self.assertEqual(s['state'], 'moving')
        s = r.feed(scene([(33, 12, 6, 3, 130)], base=240), 30)   # ghost part absorbed
        self.assertEqual(s['state'], 'still')
        self.assertAlmostEqual(s['x'], (33 + 3) / W, delta=0.03)

    def test_hand_is_never_the_target(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 16):
            r.feed(scene([at(x)]))
        r.feed(scene([at(15)]), 10)
        for y in range(0, 10):                           # big hand sweeps across the top
            s = r.feed(scene([at(15), (0, y, 36, 16, 40)]))   # 48% of the area
        self.assertAlmostEqual(s['x'], (15 + 3) / W, delta=0.03)

    def test_flicker_without_travel_is_not_moving(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 20):
            r.feed(scene([at(x)]))
        r.feed(scene([at(19)]), 20)
        for i in range(20):                              # its pixels flicker (shadow, exposure)
            s = r.feed(scene([(19, 12, 6, 3, 90 if i % 2 else 60)]))
            self.assertEqual(s['state'], 'still')

    def test_shadow_merging_with_target_is_not_followed(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 20):
            r.feed(scene([at(x)]))
        r.feed(scene([at(19)]), 30)
        before = r.tr.state(r.t)['x']
        for k in range(15):                              # a darker area grows from the gecko upwards
            s = r.feed(scene([at(19), (15, max(0, 11 - k), 14, k + 1, 120)]))
            self.assertNotEqual(s['state'], 'moving')
        self.assertAlmostEqual(s['x'], before, delta=0.03)

    def test_vanished_target_is_not_moving(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 20):
            s = r.feed(scene([at(x)]))
        self.assertEqual(s['state'], 'moving')
        s = r.feed(scene([]), 4)                         # taken away
        self.assertNotEqual(s['state'], 'moving')

    def test_carried_far_is_found_by_appearance(self):
        r = self.start_with_gecko_in_background()
        for x in range(6, 12):
            r.feed(scene([at(x)]))
        r.feed(scene([at(11)]), 30)                      # rests 3 s: ghost part absorbed
        s = r.feed(scene([(30, 22, 6, 3, 90)]), 10)      # put down far away, then still
        self.assertAlmostEqual(s['x'], (30 + 3) / W, delta=0.03)
        self.assertAlmostEqual(s['y'], (22 + 1.5) / H, delta=0.05)


def planes(objects, base=(200, 110, 140)):
    """Y, U, V planes; each object is (x, y, w, h, (Y, U, V))."""
    out = []
    for c in range(3):
        f = bytearray([base[c]]) * (W * H)
        for x, y, w, h, val in objects:
            for yy in range(y, y + h):
                f[yy * W + x:yy * W + x + w] = bytes([val[c]]) * w
        out.append(bytes(f))
    return out


class ColourRun(Run):
    def feed(self, img, n=1, scene_change=False):
        out = None
        for i in range(n):
            ch = change(img[0], self.prev[0]) if self.prev else bytes(W * H)
            if self.prev:   # a colour-only object still shows in the change image via U/V
                ch = bytes(a or (abs(p - q) > 25) for a, p, q in zip(ch, img[1], self.prev[1]))
            out = self.tr.frame(self.t, img[0], ch, scene=scene_change and i == 0, u=img[1], v=img[2])
            self.prev, self.t = img, self.t + 0.1
        return out


# Green toy on a beige desk: grey almost equal (190 vs 200), colour far apart.
TOY = (190, 60, 80)


def toy(x, w=10):
    return (x, 12, w, 4, TOY)


class ColourTests(unittest.TestCase):
    def test_colour_only_object_is_tracked_whole(self):
        r = ColourRun()
        r.feed(planes([toy(5)]), 40)
        for x in range(6, 22):
            s = r.feed(planes([toy(x)]))
        s = r.feed(planes([toy(21)]), 30)
        self.assertEqual(s['state'], 'still')
        x0, y0, x1, y1 = s['box']
        self.assertAlmostEqual(x0, 21 / W, delta=0.03)
        self.assertAlmostEqual(x1, 31 / W, delta=0.03)       # the whole 10 px body, not a piece

    def test_grey_alone_misses_it(self):
        r = Run()
        r.feed(planes([toy(5)])[0], 40)
        for x in range(6, 22):
            s = r.feed(planes([toy(x)])[0])
        self.assertEqual(s['state'], 'searching')

    def test_slow_exposure_drift_while_resting_is_not_lost(self):
        r = ColourRun()
        r.feed(planes([toy(5)]), 40)
        for x in range(6, 22):
            r.feed(planes([toy(x)]))
        r.feed(planes([toy(21)]), 30)
        for k in range(1, 900):                                 # 90 s, grey creeps up 15 levels
            g = k * 15 // 900
            s = r.feed(planes([(21, 12, 10, 4, (190 + g, 60, 80))], base=(200 + g, 110, 140)))
        self.assertEqual(s['state'], 'still')
        self.assertGreater(s['last_confirmed'], r.t - 6)

    def test_lost_needs_repeated_misses(self):
        r = ColourRun()
        r.feed(planes([toy(5)]), 40)
        for x in range(6, 22):
            r.feed(planes([toy(x)]))
        r.feed(planes([toy(21)]), 30)
        empty = planes([])
        r.tr.reset_background()                                 # as after a scene change
        s = r.feed(empty, 40)                                   # background rebuilt without the toy
        s = r.feed(empty, 50)                                   # 5 s: one failed check
        self.assertNotEqual(s['state'], 'lost')
        s = r.feed(empty, 120)                                  # 12 s more: three failed checks
        self.assertEqual(s['state'], 'lost')


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg not installed')
class DetectorPipelineTest(unittest.TestCase):
    """Real FFmpeg pipeline: a dark square sits still for 4 s, slides right for 2 s,
    then rests. The tracker should lock on and report it resting at the new spot."""

    def track(self, bg, fg):
        import recorder
        graph = (f"color=c={bg}:s=320x180:r=10[bg];color=c={fg}:s=24x12:r=10[fg];"
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
        shutil.rmtree(tmp)
        return det.track_state

    def check(self, st):
        self.assertEqual(st['state'], 'still', st)
        self.assertAlmostEqual(st['x'], (180 + 12) / 320, delta=0.03)
        self.assertAlmostEqual(st['y'], (90 + 6) / 180, delta=0.04)
        x0, _, x1, _ = st['box']
        self.assertGreater(x1 - x0, 18 / 320)                 # most of the 24 px width

    def test_dark_square_is_tracked_through_the_detector(self):
        self.check(self.track('0xc8c8c8', '0x404040'))

    def test_green_on_beige_is_tracked_by_colour(self):
        # Grey levels about 183 vs 165: below fg_threshold, so only colour separates them.
        self.check(self.track('0xc8b496', '0x6ed24a'))

    def test_hand_elsewhere_does_not_trigger_recording(self):
        import recorder
        graph = ("color=c=0xc8c8c8:s=320x180:r=10[bg];color=c=0x404040:s=24x12:r=10[fg];"
                 "color=c=0x806040:s=40x40:r=10[hand];"
                 "[bg][fg]overlay=x='if(lt(t,4),60,if(lt(t,6),60+60*(t-4),180))':y=90[a];"
                 "[a][hand]overlay=x='20+40*(t-7.5)':y=20:enable='between(t,7.5,9.5)'")
        tmp = Path(tempfile.mkdtemp())
        cfg = recorder.load_config(None)
        cfg['output_dir'] = str(tmp)
        cfg['motion'].update(enabled=True, mask=[], roi_file=str(tmp / 'roi.json'),
                             input_args=['-re', '-f', 'lavfi', '-i', graph, '-t', '11'])
        t0 = time.time()
        det = recorder.MotionDetector(cfg, lambda *a, **k: None)
        det.proc.wait(25)
        det.thread.join(5)
        det.proc.stdout.close()
        shutil.rmtree(tmp)
        events = [t - t0 for t in det.drain()]
        shadow = [t - t0 for t in det.drain_shadow()]
        self.assertEqual(det.source, 'gecko')
        self.assertTrue(events, 'the moving square should trigger')
        self.assertTrue(all(3.5 < t < 7.5 for t in events), events)          # only while it moves
        self.assertTrue(any(7.5 < t < 10 for t in shadow), shadow)          # the hand: logged only


if __name__ == '__main__':
    unittest.main()
