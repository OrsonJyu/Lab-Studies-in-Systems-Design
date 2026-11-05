#!/usr/bin/env python3
"""Local web page for the SD5531 recorder (Python 3.9+, stdlib only).

  /               live view, recorder status and a timeline with one marker per
                  recorded event; click a marker to play that clip
  /live.mjpg      live substream as MJPEG; one FFmpeg process shared by all
                  viewers, started on demand and stopped when nobody watches
  /api/status     recorder state.json plus board time
  /api/events     saved event records (newest first)
  /api/scenes     recent scene changes (lights, exposure) that were not counted as motion
  /api/roi        POST {"points": [[x, y], ...]} (frame fractions) sets the detection
                  area; {"points": null} clears it (whole frame). The recorder picks
                  the change up within about a second.
  /snapshot.jpg   one current frame, for drawing the detection area
  /clips/NAME     saved MP4 with HTTP Range support for seeking

Reads the same config as recorder.py. No authentication (anyone who can reach
the page can also change the detection area): bind it only to the isolated lab
network or to localhost.

  webview.py --config CONFIG
"""
import argparse, json, re, socketserver, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recorder

WEB_DEFAULTS = {
    'bind': '127.0.0.1',
    'port': 8080,
    'live_fps': 10,
    'live_width': 800,
    'live_quality': 5,      # MJPEG q:v, 2 (best) .. 31
    'idle_stop_s': 10,
    'input_args': None,     # a list overrides the substream source (tests)
}
EVENT_NAME = re.compile(r'^\d{8}-\d{6}-[0-9a-f]{6}\.mp4$')
PAGE = Path(__file__).resolve().parent / 'webview.html'


def load_config(path):
    cfg = recorder.load_config(path)
    user = json.loads(Path(path).read_text()).get('web', {}) if path else {}
    cfg['web'] = {**WEB_DEFAULTS, **user}
    return cfg


def parse_range(header, size):
    """Return (start, end) inclusive for a single 'bytes=' range, or None."""
    m = re.fullmatch(r'bytes=(\d*)-(\d*)', (header or '').strip())
    if not m or (m[1] == '' and m[2] == ''):
        return None
    if m[1] == '':
        start, end = max(0, size - int(m[2])), size - 1
    else:
        start = int(m[1])
        end = min(int(m[2]), size - 1) if m[2] else size - 1
    return (start, end) if start <= end < size else None


def load_events(output_dir, limit=500):
    records = []
    for js in sorted(Path(output_dir).glob('*.json'), reverse=True)[:limit]:
        try:
            rec = json.loads(js.read_text())
        except (OSError, ValueError):
            continue
        # The Mac's sync deletes the MP4 here once its own copy is verified; the record stays.
        rec['on_board'] = bool(rec.get('file')) and (Path(output_dir) / rec['file']).is_file()
        records.append(rec)
    return records


def load_scenes(output_dir, limit=500):
    path = Path(output_dir) / 'scene_changes.jsonl'
    try:
        lines = path.read_text().splitlines()[-limit:]
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def save_roi(path, points):
    """Validate and write the detection area atomically; returns the saved points."""
    roi = None if points is None else recorder.valid_roi(points)
    if points is not None and roi is None:
        raise ValueError('need 3-12 [x, y] points between 0 and 1 enclosing an area')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.part')
    tmp.write_text(json.dumps({'points': roi, 'saved_at': round(time.time(), 3)}))
    tmp.replace(path)
    return roi


class LiveFeed:
    """One FFmpeg MJPEG process; viewers wait on a condition for each new frame."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.cond = threading.Condition()
        self.frame, self.seq = None, 0
        self.viewers, self.last_viewer = 0, 0.0
        self.proc = None

    def args(self):
        w = self.cfg['web']
        if w['input_args'] is not None:
            src = list(w['input_args'])
        else:
            uri = json.loads(Path(self.cfg['motion']['source_config']).read_text())['uri']
            src = ['-rtsp_transport', 'tcp', '-timeout', '10000000', '-i', uri]
        return ['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error'] + src + \
               ['-an', '-vf', f"fps={w['live_fps']},scale={w['live_width']}:-2",
                '-q:v', str(w['live_quality']), '-f', 'mjpeg', '-flush_packets', '1', 'pipe:1']

    def join(self):
        with self.cond:
            self.viewers += 1
            if self.proc is None or self.proc.poll() is not None:
                self.proc = subprocess.Popen(self.args(), stdin=subprocess.DEVNULL,
                                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                threading.Thread(target=self._read, args=(self.proc,), daemon=True).start()

    def leave(self):
        with self.cond:
            self.viewers -= 1
            self.last_viewer = time.time()

    def _read(self, proc):
        buf = b''
        while True:
            chunk = proc.stdout.read1(65536)   # read() would wait for a full 64 KiB
            if not chunk:
                break
            buf += chunk
            while True:
                start = buf.find(b'\xff\xd8')
                end = buf.find(b'\xff\xd9', start + 2) if start >= 0 else -1
                if end < 0:
                    break
                with self.cond:
                    self.frame, self.seq = buf[start:end + 2], self.seq + 1
                    self.cond.notify_all()
                buf = buf[end + 2:]
        with self.cond:
            self.cond.notify_all()

    def next_frame(self, after, timeout=5):
        with self.cond:
            self.cond.wait_for(lambda: self.seq != after, timeout)
            return self.frame, self.seq

    def reap_idle(self):
        """Stop FFmpeg when nobody has watched for idle_stop_s seconds."""
        while True:
            time.sleep(1)
            with self.cond:
                idle = self.viewers == 0 and time.time() - self.last_viewer > self.cfg['web']['idle_stop_s']
                if idle and self.proc and self.proc.poll() is None:
                    self.proc.terminate()
                    self.proc = None


def make_handler(cfg, feed):
    out_dir = Path(cfg['output_dir'])
    state_path = Path(cfg['ring_dir']) / 'state.json'

    class Handler(BaseHTTPRequestHandler):
        server_version = 'sd5531-webview/0.1'

        def log_message(self, *_):
            pass

        def send_json(self, obj):
            body = json.dumps(obj).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split('?', 1)[0]
            if path == '/':
                body = PAGE.read_bytes()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif path == '/api/status':
                try:
                    state = json.loads(state_path.read_text())
                except (OSError, ValueError):
                    state = None
                self.send_json({'board_time': time.time(), 'recorder': state})
            elif path == '/api/events':
                self.send_json(load_events(out_dir))
            elif path == '/api/scenes':
                self.send_json(load_scenes(out_dir))
            elif path == '/live.mjpg':
                self.live()
            elif path == '/snapshot.jpg':
                self.snapshot()
            elif path.startswith('/clips/') and EVENT_NAME.match(path[7:]):
                self.clip(out_dir / path[7:])
            else:
                self.send_error(404)

        def do_POST(self):
            if self.path.split('?', 1)[0] != '/api/roi':
                self.send_error(404)
                return
            try:
                length = int(self.headers.get('Content-Length') or 0)
                if length > 4096:
                    raise ValueError('request too large')
                body = json.loads(self.rfile.read(length) or b'{}')
                roi = save_roi(cfg['motion']['roi_file'], body.get('points'))
            except (ValueError, AttributeError) as e:
                self.send_response(400)
                msg = json.dumps({'error': str(e)}).encode()
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
                return
            self.send_json({'points': roi})

        def snapshot(self):
            feed.join()
            try:
                frame, _ = feed.next_frame(feed.seq)   # wait for a fresh frame
            finally:
                feed.leave()
            if frame is None:
                self.send_error(503, 'no frame from the camera')
                return
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(frame)))
            self.end_headers()
            self.wfile.write(frame)

        def live(self):
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            feed.join()
            seq = 0
            try:
                while True:
                    frame, seq = feed.next_frame(seq)
                    if frame is None:
                        continue
                    self.wfile.write(b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: '
                                     + str(len(frame)).encode() + b'\r\n\r\n' + frame + b'\r\n')
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                feed.leave()

        def clip(self, mp4):
            if not mp4.is_file():
                self.send_error(404)
                return
            size = mp4.stat().st_size
            rng = parse_range(self.headers.get('Range'), size)
            start, end = rng or (0, size - 1)
            self.send_response(206 if rng else 200)
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Length', str(end - start + 1))
            if rng:
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.end_headers()
            with open(mp4, 'rb') as f:
                f.seek(start)
                left = end - start + 1
                try:
                    while left > 0:
                        chunk = f.read(min(left, 1 << 20))
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        left -= len(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    pass

    return Handler


class Server(ThreadingHTTPServer):
    def server_bind(self):
        # HTTPServer.server_bind looks up the host's FQDN, which blocks on the
        # isolated lab network (no DNS). The name is only used in logs.
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]


def serve(cfg):
    feed = LiveFeed(cfg)
    threading.Thread(target=feed.reap_idle, daemon=True).start()
    server = Server((cfg['web']['bind'], cfg['web']['port']), make_handler(cfg, feed))
    server.daemon_threads = True
    return server, feed


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--config')
    args = p.parse_args(argv)
    cfg = load_config(args.config)
    server, _ = serve(cfg)
    print(f"serving on http://{cfg['web']['bind']}:{cfg['web']['port']}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
