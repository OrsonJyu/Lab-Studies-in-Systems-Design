"""Tests for webview.py. Range parsing needs nothing; the server test needs ffmpeg."""
import json, shutil, subprocess, sys, tempfile, threading, time, unittest, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import webview
from webview import EVENT_NAME, parse_range


class RangeTests(unittest.TestCase):
    def test_ranges(self):
        self.assertEqual(parse_range('bytes=0-99', 1000), (0, 99))
        self.assertEqual(parse_range('bytes=900-', 1000), (900, 999))
        self.assertEqual(parse_range('bytes=-100', 1000), (900, 999))
        self.assertEqual(parse_range('bytes=0-5000', 1000), (0, 999))
        self.assertIsNone(parse_range('bytes=1000-', 1000))
        self.assertIsNone(parse_range('bytes=5-1', 1000))
        self.assertIsNone(parse_range('items=0-1', 1000))
        self.assertIsNone(parse_range(None, 1000))

    def test_only_event_files_are_served(self):
        self.assertTrue(EVENT_NAME.match('20261105-033359-ccd8fb.mp4'))
        for bad in ['../config.json', '20261105-033359-ccd8fb.json', 'a/20261105-033359-ccd8fb.mp4', '%2e%2e%2fx.mp4']:
            self.assertFalse(EVENT_NAME.match(bad), bad)


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg not installed')

class LoadEventsTest(unittest.TestCase):
    def test_marks_clips_moved_off_the_board(self):
        with tempfile.TemporaryDirectory() as d:
            for name, keep in (('20261105-010000-aaaaaa', True), ('20261105-020000-bbbbbb', False)):
                Path(d, name + '.json').write_text(json.dumps({'event_id': name, 'file': name + '.mp4'}))
                if keep:
                    Path(d, name + '.mp4').write_bytes(b'x')
            Path(d, '20261105-030000-cccccc.json').write_text(json.dumps({'event_id': 'c', 'file': None}))
            got = {r['event_id']: r['on_board'] for r in webview.load_events(d)}
        self.assertEqual(got, {'20261105-010000-aaaaaa': True, '20261105-020000-bbbbbb': False, 'c': False})

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        events = self.tmp / 'events'
        events.mkdir()
        (self.tmp / 'ring').mkdir()
        self.clip = events / '20261105-033359-ccd8fb.mp4'
        self.clip.write_bytes(bytes(range(256)) * 40)
        (events / '20261105-033359-ccd8fb.json').write_text(json.dumps(
            {'event_id': '20261105-033359-ccd8fb', 'file': self.clip.name, 'status': 'ok'}))
        (self.tmp / 'ring' / 'state.json').write_text(json.dumps({'t': time.time(), 'open_event': None}))
        cfg_path = self.tmp / 'config.json'
        cfg_path.write_text(json.dumps({
            'ring_dir': str(self.tmp / 'ring'), 'output_dir': str(events),
            'web': {'port': 0, 'idle_stop_s': 1,
                    'input_args': ['-re', '-f', 'lavfi', '-i', 'testsrc2=s=320x180:r=20']}}))
        self.server, self.feed = webview.serve(webview.load_config(cfg_path))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f'http://127.0.0.1:{self.server.server_address[1]}'

    def tearDown(self):
        self.server.shutdown()
        if self.feed.proc:
            self.feed.proc.terminate()
        shutil.rmtree(self.tmp)

    def get(self, path, headers=None):
        return urllib.request.urlopen(urllib.request.Request(self.base + path, headers=headers or {}), timeout=5)

    def test_pages_and_api(self):
        self.assertIn('时间轴', self.get('/').read().decode())
        status = json.load(self.get('/api/status'))
        self.assertIn('board_time', status)
        self.assertIsNone(status['recorder']['open_event'])
        [event] = json.load(self.get('/api/events'))
        self.assertEqual(event['event_id'], '20261105-033359-ccd8fb')

    def test_clip_range(self):
        r = self.get('/clips/' + self.clip.name, {'Range': 'bytes=10-19'})
        self.assertEqual(r.status, 206)
        self.assertEqual(r.headers['Content-Range'], f'bytes 10-19/{self.clip.stat().st_size}')
        self.assertEqual(r.read(), self.clip.read_bytes()[10:20])

    def test_live_mjpeg_streams_frames(self):
        r = self.get('/live.mjpg')
        self.assertTrue(r.headers['Content-Type'].startswith('multipart/x-mixed-replace'))
        frames, t0 = 0, time.time()
        while time.time() - t0 < 3:
            frames += r.read1(65536).count(b'Content-Type: image/jpeg')
        r.close()
        self.assertGreaterEqual(frames, 10)   # about 10 fps


if __name__ == '__main__':
    unittest.main()
