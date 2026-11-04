#!/usr/bin/env python3
"""Rolling-buffer event recorder for the SD5531 camera (Python 3.9+, stdlib only).

FFmpeg copies the camera stream into short MPEG-TS segments in a RAM ring
directory. Motion observations (manual triggers for now) open an event; the
event closes once no motion has been seen for `still_s` seconds. The clip
covers `pre_roll_s` before the first motion to the end of the still period,
is cut at segment (keyframe) boundaries, joined without re-encoding and saved
with a JSON record. Segments are deleted when they fall out of the ring and no
open or pending event needs them.

Times are ROCK wall-clock receive times (time.time()). Content time is earlier
by the capture-to-board latency, recorded as an estimate only.

  recorder.py run --config CONFIG
  recorder.py trigger --config CONFIG [--hold SECONDS]
"""
import argparse, csv, hashlib, json, os, shutil, signal, subprocess, sys, time, uuid
from dataclasses import dataclass, field
from pathlib import Path

DEFAULTS = {
    'camera_id': 'cam-01',
    'source_config': '~/sd5531/private/camera_source.json',
    'ring_dir': '/dev/shm/sd5531-ring',
    'output_dir': '~/sd5531/events',
    'segment_seconds': 2,
    'ring_seconds': 60,
    'pre_roll_s': 4.0,
    'still_s': 5.0,
    'max_event_s': 300.0,
    'min_free_mb': 500,
    'assemble_timeout_s': 30.0,
    'capture_latency_s': 0.23,
    'input_args': None,   # None: RTSP/TCP from source_config; a list overrides (tests)
    'codec_args': ['-c', 'copy'],
}


def load_config(path):
    cfg = dict(DEFAULTS)
    if path:
        cfg.update(json.loads(Path(path).read_text()))
    for key in ('source_config', 'ring_dir', 'output_dir'):
        cfg[key] = str(Path(cfg[key]).expanduser())
    if cfg['pre_roll_s'] < 0 or cfg['still_s'] <= 0 or cfg['segment_seconds'] <= 0:
        raise ValueError('pre_roll_s must be >= 0; still_s and segment_seconds must be > 0')
    return cfg


# ---------------------------------------------------------------- events

@dataclass
class Event:
    event_id: str
    start: float                 # first motion, wall clock
    last_motion: float
    motions: list = field(default_factory=list)
    end: float = None
    close_reason: str = None


class EventTracker:
    """Motion intervals in, closed events out. Pure logic, no I/O."""

    def __init__(self, still_s, max_event_s):
        self.still_s = still_s
        self.max_event_s = max_event_s
        self.open = None

    def motion(self, t_start, t_end=None):
        """Record motion seen from t_start to t_end; return any event this closed."""
        t_end = t_start if t_end is None else max(t_start, t_end)
        closed = []
        if self.open and t_start - self.open.last_motion >= self.still_s:
            closed.append(self._close(self.open.last_motion + self.still_s, 'still'))
        if self.open is None:
            self.open = Event(new_event_id(t_start), t_start, t_end)
        self.open.last_motion = max(self.open.last_motion, t_end)
        self.open.motions.append([round(t_start, 3), round(t_end, 3)])
        return closed

    def poll(self, now):
        if self.open is None:
            return []
        if now - self.open.last_motion >= self.still_s:
            return [self._close(self.open.last_motion + self.still_s, 'still')]
        if now - self.open.start >= self.max_event_s:
            return [self._close(self.open.start + self.max_event_s, 'max_event_s')]
        return []

    def _close(self, end, reason):
        event, self.open = self.open, None
        event.end, event.close_reason = end, reason
        return event


def new_event_id(t):
    return time.strftime('%Y%m%d-%H%M%S', time.localtime(t)) + '-' + uuid.uuid4().hex[:6]


# ---------------------------------------------------------------- segments

@dataclass
class Segment:
    path: str
    wall_start: float
    wall_end: float
    run: int


def select_segments(segments, a, b):
    """Segments overlapping [a, b), in time order."""
    return sorted((s for s in segments if s.wall_end > a and s.wall_start < b),
                  key=lambda s: s.wall_start)


def stamp_segments(directory, rows, prev_end, run):
    """Turn new segment-list rows into Segments timed by receive time.

    A segment file is last written when its final packet arrives, so its mtime
    is the receive time of its end, independent of how late the list is polled.
    The start is the previous segment's end, or end minus duration for the first.
    """
    out = []
    for name, start, end in rows:
        path = Path(directory) / name
        try:
            wall_end = path.stat().st_mtime
        except FileNotFoundError:
            continue
        wall_start = prev_end if prev_end is not None else wall_end - (float(end) - float(start))
        out.append(Segment(str(path), wall_start, wall_end, run))
        prev_end = wall_end
    return out


def gaps_between(segments, tolerance=0.5):
    return [[round(x.wall_end, 3), round(y.wall_start, 3)]
            for x, y in zip(segments, segments[1:]) if y.wall_start - x.wall_end > tolerance]


class SegmentRun:
    """One FFmpeg process writing segments and a live CSV list into its own directory."""

    def __init__(self, cfg, number, log):
        self.cfg, self.number, self.log = cfg, number, log
        self.dir = Path(cfg['ring_dir']) / f'run-{number:04d}'
        self.dir.mkdir(parents=True, exist_ok=True)
        self.list_path = self.dir / 'list.csv'
        self.seen = 0
        self.last_end = None
        cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error'] + input_args(cfg) + \
              ['-map', '0:v:0'] + cfg['codec_args'] + \
              ['-f', 'segment', '-segment_time', str(cfg['segment_seconds']),
               '-segment_format', 'mpegts', '-segment_list', str(self.list_path),
               '-segment_list_type', 'csv', '-segment_list_flags', '+live',
               str(self.dir / 'seg-%06d.ts')]
        self.stderr = open(self.dir / 'ffmpeg.log', 'w')
        self.proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                     stderr=self.stderr)
        log('segmenter_started', run=number)

    def poll(self):
        """Return segments completed since the last poll, stamped with receive time."""
        if not self.list_path.exists():
            return []
        rows = list(csv.reader(self.list_path.read_text().splitlines()))
        new = stamp_segments(self.dir, rows[self.seen:], self.last_end, self.number)
        self.seen = len(rows)
        if new:
            self.last_end = new[-1].wall_end
        return new

    def alive(self):
        return self.proc.poll() is None

    def stop(self):
        if self.alive():
            self.proc.send_signal(signal.SIGINT)
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.stderr.close()


def input_args(cfg):
    if cfg['input_args'] is not None:
        return list(cfg['input_args'])
    uri = json.loads(Path(cfg['source_config']).read_text())['uri']
    return ['-rtsp_transport', 'tcp', '-timeout', '10000000', '-i', uri]


# ---------------------------------------------------------------- assembly

def assemble(cfg, event, segments, partial, log):
    """Join the segments for one event into an MP4 plus a JSON record."""
    out_dir = Path(cfg['output_dir'])
    out_dir.mkdir(parents=True, exist_ok=True)
    a, b = event.start - cfg['pre_roll_s'], event.end
    chosen = select_segments(segments, a, b)
    record = {
        'event_id': event.event_id, 'camera_id': cfg['camera_id'], 'source': 'manual',
        'clock': 'ROCK wall-clock receive time, Unix seconds',
        'motions': event.motions,
        'first_motion': round(event.start, 3), 'last_motion': round(event.last_motion, 3),
        'event_end': round(event.end, 3), 'close_reason': event.close_reason,
        'pre_roll_s': cfg['pre_roll_s'], 'still_s': cfg['still_s'],
        'requested_window': [round(a, 3), round(b, 3)],
        'capture_latency_s_estimate': cfg['capture_latency_s'],
        'segments': [Path(s.path).name for s in chosen],
        'runs': sorted({s.run for s in chosen}),
        'gaps': gaps_between(chosen),
        'partial': partial,
    }
    if chosen:
        record['clip_window'] = [round(chosen[0].wall_start, 3), round(chosen[-1].wall_end, 3)]
        record['actual_pre_roll_s'] = round(event.start - chosen[0].wall_start, 3)
    base = out_dir / event.event_id
    free_mb = shutil.disk_usage(out_dir).free / 2**20
    if not chosen:
        record.update(status='failed', failure='no segments cover the event window')
    elif free_mb < cfg['min_free_mb']:
        record.update(status='failed', failure=f'free space {free_mb:.0f} MiB below min_free_mb')
    else:
        listing = base.with_suffix('.concat.txt')
        listing.write_text(''.join(f"file '{s.path}'\n" for s in chosen))
        tmp = base.with_suffix('.part.mp4')
        r = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error', '-y',
                            '-f', 'concat', '-safe', '0', '-i', str(listing),
                            '-c', 'copy', '-movflags', '+faststart', '-f', 'mp4', str(tmp)],
                           capture_output=True, text=True)
        listing.unlink()
        if r.returncode:
            tmp.unlink(missing_ok=True)
            record.update(status='failed', failure='ffmpeg concat: ' + r.stderr.strip()[-300:])
        else:
            mp4 = base.with_suffix('.mp4')
            tmp.rename(mp4)
            record.update(status='partial' if partial else 'ok', file=mp4.name,
                          bytes=mp4.stat().st_size, sha256=sha256(mp4),
                          duration_s=probe_duration(mp4))
    tmp_json = base.with_suffix('.json.part')
    tmp_json.write_text(json.dumps(record, indent=1))
    tmp_json.rename(base.with_suffix('.json'))
    log('event_saved', event_id=event.event_id, status=record['status'],
        duration_s=record.get('duration_s'), actual_pre_roll_s=record.get('actual_pre_roll_s'))
    return record


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def probe_duration(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', str(path)], capture_output=True, text=True)
    try:
        return round(float(r.stdout.strip()), 3)
    except ValueError:
        return None


# ---------------------------------------------------------------- service

class Recorder:
    def __init__(self, cfg):
        self.cfg = cfg
        self.ring = Path(cfg['ring_dir'])
        self.requests = self.ring / 'requests'
        shutil.rmtree(self.ring, ignore_errors=True)   # stale segments have no usable times
        self.requests.mkdir(parents=True)
        Path(cfg['output_dir']).mkdir(parents=True, exist_ok=True)
        self.log_file = open(Path(cfg['output_dir']) / 'recorder.log.jsonl', 'a')
        self.tracker = EventTracker(cfg['still_s'], cfg['max_event_s'])
        self.segments, self.pending = [], []
        self.run_number, self.run = 0, None
        self.restart_at = 0.0
        self.stopping = False

    def log(self, kind, **fields):
        self.log_file.write(json.dumps({'t': round(time.time(), 3), 'kind': kind, **fields}) + '\n')
        self.log_file.flush()

    def ensure_segmenter(self, now):
        if self.run and self.run.alive():
            return
        if self.run:
            self.log('segmenter_exited', run=self.run.number, code=self.run.proc.returncode)
            self.run.stop()
            self.run = None
            self.restart_at = now + 3
        if now >= self.restart_at:
            self.run_number += 1
            self.run = SegmentRun(self.cfg, self.run_number, self.log)

    def read_requests(self):
        for path in sorted(self.requests.glob('*.json')):
            try:
                req = json.loads(path.read_text())
                t = float(req['t'])
                for event in self.tracker.motion(t, t + float(req.get('hold', 0))):
                    self.pending.append(event)
                self.log('motion', source='manual', t=round(t, 3), hold=req.get('hold', 0))
            except (ValueError, KeyError, OSError) as e:
                self.log('bad_request', file=path.name, error=str(e))
            path.unlink(missing_ok=True)

    def assemble_ready(self, now):
        latest = max((s.wall_end for s in self.segments), default=0)
        for event in list(self.pending):
            timed_out = now - event.end > self.cfg['assemble_timeout_s']
            if latest >= event.end or timed_out:
                assemble(self.cfg, event, self.segments, partial=latest < event.end, log=self.log)
                self.pending.remove(event)

    def cleanup(self, now):
        keep_after = now - self.cfg['ring_seconds']
        needed = [e.start - self.cfg['pre_roll_s'] for e in self.pending]
        if self.tracker.open:
            needed.append(self.tracker.open.start - self.cfg['pre_roll_s'])
        if needed:
            keep_after = min(keep_after, min(needed))
        kept = []
        for s in self.segments:
            if s.wall_end < keep_after:
                Path(s.path).unlink(missing_ok=True)
            else:
                kept.append(s)
        self.segments = kept

    def loop(self):
        self.log('recorder_started', pre_roll_s=self.cfg['pre_roll_s'], still_s=self.cfg['still_s'],
                 segment_seconds=self.cfg['segment_seconds'], ring_seconds=self.cfg['ring_seconds'])
        while not self.stopping:
            now = time.time()
            self.ensure_segmenter(now)
            if self.run:
                fresh = self.run.poll()
                if fresh and self.segments and fresh[0].wall_start - self.segments[-1].wall_end > 0.5:
                    self.log('stream_gap', start=round(self.segments[-1].wall_end, 3),
                             end=round(fresh[0].wall_start, 3))
                self.segments += fresh
            self.read_requests()
            self.pending += self.tracker.poll(now)
            self.assemble_ready(now)
            self.cleanup(now)
            time.sleep(0.1)
        self.shutdown()

    def shutdown(self):
        now = time.time()
        if self.tracker.open:
            self.pending.append(self.tracker._close(now, 'shutdown'))
        if self.run:
            self.run.stop()
            self.segments += self.run.poll()
        for event in list(self.pending):
            assemble(self.cfg, event, self.segments, partial=True, log=self.log)
        self.log('recorder_stopped')
        self.log_file.close()


def write_trigger(cfg, hold):
    req_dir = Path(cfg['ring_dir']) / 'requests'
    if not req_dir.is_dir():
        sys.exit('recorder is not running (no requests directory)')
    t = time.time()
    tmp = req_dir / f'.{t:.6f}.tmp'
    tmp.write_text(json.dumps({'t': t, 'hold': hold}))
    tmp.rename(req_dir / f'{t:.6f}.json')
    stamp = time.strftime('%H:%M:%S', time.localtime(t)) + f'{t % 1:.3f}'[1:]
    print(f'motion at {stamp}' + (f', held {hold:g} s' if hold else ''))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest='cmd', required=True)
    run = sub.add_parser('run', help='run the segmenter and event recorder')
    run.add_argument('--config')
    trig = sub.add_parser('trigger', help='report manual motion to a running recorder')
    trig.add_argument('--config')
    trig.add_argument('--hold', type=float, default=0, help='motion continues for this many seconds')
    args = p.parse_args(argv)
    cfg = load_config(args.config)
    if args.cmd == 'trigger':
        write_trigger(cfg, args.hold)
        return
    rec = Recorder(cfg)

    def stop(*_):
        rec.stopping = True
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    rec.loop()


if __name__ == '__main__':
    main()
