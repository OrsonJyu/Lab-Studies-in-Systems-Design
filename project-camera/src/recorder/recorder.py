#!/usr/bin/env python3
"""Rolling-buffer event recorder for the SD5531 camera (Python 3.9+, stdlib only).

FFmpeg copies the camera stream into short MPEG-TS segments in a RAM ring
directory. Motion observations open an event: manual triggers, or a second
FFmpeg process that decodes the low-resolution substream into per-frame change
images, filtered by detection area, scene-change, size and persistence rules
(MotionDetector). The
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
import argparse, csv, hashlib, json, os, queue, re, shutil, signal, subprocess, sys, threading, time, uuid
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tracker

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
    'motion': {
        'enabled': False,
        'source_config': '~/sd5531/private/camera_substream.json',
        'input_args': None,       # a list overrides source_config (tests)
        'fps': 10,
        'width': 160,
        'height': 90,
        'pixel_threshold': 25,    # grey-level change for a pixel to count as changed
        # Detection area: polygon of [x, y] frame fractions. The web page writes roi_file;
        # 'roi' in the config is the fallback; neither means the whole frame.
        'roi_file': '~/sd5531/roi.json',
        'roi': None,
        # A frame where at least this share of the whole picture changed is a scene
        # change (lights, auto exposure, IR switch), never motion.
        'global_fraction': 0.30,
        'scene_cooldown_s': 2.0,  # ignore frames this long after a scene change (exposure settles)
        # Changed regions (8-connected) inside the area: smaller than min_blob_px is noise;
        # larger than max_blob_fraction of the area (a hand, a person leaning in) rejects the frame.
        'size_filter': True,      # False: any change inside the area counts, whatever its size
        'min_blob_px': 4,
        'max_blob_fraction': 0.35,
        # Motion must last persist_s (gaps of up to max_gap_frames allowed) before it counts;
        # the event then starts at the first frame of that run.
        'persist_s': 0.5,
        'max_gap_frames': 1,
        # Areas ignored, as [x, y, w, h] fractions of the frame: camera date OSD
        # (top left) and camera name (bottom left).
        'mask': [[0, 0, 0.45, 0.09], [0, 0.9, 0.25, 0.1]],
        'stats_every_s': 10,
    },
}


def load_config(path):
    cfg = dict(DEFAULTS)
    user = json.loads(Path(path).read_text()) if path else {}
    cfg.update({k: v for k, v in user.items() if k != 'motion'})
    cfg['motion'] = {**DEFAULTS['motion'], **user.get('motion', {})}
    for key in ('source_config', 'roi_file'):
        cfg['motion'][key] = str(Path(cfg['motion'][key]).expanduser())
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
    sources: set = field(default_factory=set)


class EventTracker:
    """Motion intervals in, closed events out. Pure logic, no I/O."""

    def __init__(self, still_s, max_event_s, merge_gap_s=1.0):
        self.still_s = still_s
        self.max_event_s = max_event_s
        self.merge_gap_s = merge_gap_s   # join motion intervals closer than this in the record
        self.open = None

    def motion(self, t_start, t_end=None, source='manual'):
        """Record motion seen from t_start to t_end; return any event this closed."""
        t_end = t_start if t_end is None else max(t_start, t_end)
        closed = []
        if self.open and t_start - self.open.last_motion >= self.still_s:
            closed.append(self._close(self.open.last_motion + self.still_s, 'still'))
        if self.open is None:
            self.open = Event(new_event_id(t_start), t_start, t_end)
        self.open.last_motion = max(self.open.last_motion, t_end)
        self.open.sources.add(source)
        last = self.open.motions[-1] if self.open.motions else None
        if last and t_start - last[1] <= self.merge_gap_s:
            last[1] = round(max(last[1], t_end), 3)
        else:
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
        'event_id': event.event_id, 'camera_id': cfg['camera_id'],
        'source': ','.join(sorted(event.sources)),
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


# ---------------------------------------------------------------- motion
#
# FFmpeg decodes the substream, scales it down and outputs, per frame, a grey image
# where a pixel is 255 if it changed by more than pixel_threshold since the previous
# frame and 0 otherwise. Python then applies the rules:
#   1. only changes inside the detection area count (camera OSD always excluded);
#   2. a frame where a large share of the whole picture changed is a scene change;
#   3. changed regions are grouped; too small is noise, too large rejects the frame;
#   4. motion must persist for persist_s before it opens or extends an event.


def motion_filter(m):
    """FFmpeg filter chain producing, per output frame, the thresholded difference
    image (top half) stacked on the current grey frame (bottom half)."""
    return (f"fps={m['fps']},scale={m['width']}:{m['height']},format=gray,split[a][b];"
            f"[a]tblend=all_mode=difference,"
            f"lutyuv=y='if(gt(val,{m['pixel_threshold']}),255,0)'[d];[d][b]vstack")


def _popcount(x):
    return x.bit_count() if hasattr(x, 'bit_count') else bin(x).count('1')


def box_mask(boxes, w, h):
    """1 for pixels inside any [x, y, w, h] fraction box."""
    out = bytearray(w * h)
    for bx, by, bw, bh in boxes:
        x0, y0 = round(bx * w), round(by * h)
        x1, y1 = min(w, round((bx + bw) * w)), min(h, round((by + bh) * h))
        for y in range(max(0, y0), y1):
            out[y * w + max(0, x0):y * w + x1] = b'\x01' * (x1 - max(0, x0))
    return out


def polygon_mask(points, w, h):
    """1 for pixels whose centre lies inside the polygon (fractions of the frame)."""
    pts = [(x * w, y * h) for x, y in points]
    out = bytearray(w * h)
    n = len(pts)
    for py in range(h):
        cy = py + 0.5
        xs = []
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
            if (y1 <= cy < y2) or (y2 <= cy < y1):
                xs.append(x1 + (cy - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            lo, hi = max(0, int(a + 0.5)), min(w, int(b + 0.5))
            if hi > lo:
                out[py * w + lo:py * w + hi] = b'\x01' * (hi - lo)
    return out


def valid_roi(points):
    """A polygon of 3-12 [x, y] points inside the frame, or None."""
    if not isinstance(points, list) or not 3 <= len(points) <= 12:
        return None
    try:
        pts = [[float(x), float(y)] for x, y in points]
    except (TypeError, ValueError):
        return None
    if not all(0 <= v <= 1 for p in pts for v in p):
        return None
    area = sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts))) / 2
    return [[round(x, 4), round(y, 4)] for x, y in pts] if abs(area) > 1e-4 else None


class FrameAnalyzer:
    """Thresholded difference frame in, verdict out. Pure logic, no I/O."""

    def __init__(self, m, roi=None):
        self.m, self.w, self.h = m, m['width'], m['height']
        self.n = self.w * self.h
        self.osd = box_mask(m['mask'], self.w, self.h)
        self.set_roi(roi)

    def set_roi(self, roi):
        self.roi = roi
        inside = polygon_mask(roi, self.w, self.h) if roi else bytearray(b'\x01' * self.n)
        valid = bytes(0 if o else 1 for o in self.osd)
        area = bytes(a & v for a, v in zip(inside, valid))
        self.valid_int, self.valid_px = int.from_bytes(valid, 'big'), valid.count(1)
        self.area_int, self.area_px = int.from_bytes(area, 'big'), area.count(1)
        self.max_blob_px = self.m['max_blob_fraction'] * self.area_px
        self.area_mask = area

    def blobs(self, changed):
        """8-connected regions of the 0/1 bytes: list of (pixels, (x0, y0, x1, y1))."""
        w, todo, out = self.w, set(), []
        i = changed.find(1)
        while i >= 0:
            todo.add(i)
            i = changed.find(1, i + 1)
        while todo:
            stack = [todo.pop()]
            count, x0, y0, x1, y1 = 0, w, self.h, -1, -1
            while stack:
                p = stack.pop()
                count += 1
                y, x = divmod(p, w)
                x0, x1, y0, y1 = min(x0, x), max(x1, x), min(y0, y), max(y1, y)
                for dy in (-w, 0, w):
                    for dx in ((-1, 0, 1) if 0 < x < w - 1 else (0, 1) if x == 0 else (-1, 0)):
                        q = p + dy + dx
                        if q in todo:
                            todo.remove(q)
                            stack.append(q)
            out.append((count, (x0, y0, x1 + 1, y1 + 1)))
        return out

    def analyze(self, frame):
        bits = int.from_bytes(frame, 'big')   # bytes are 0x00 or 0xff
        global_share = _popcount(bits & self.valid_int) / max(1, self.valid_px)
        in_area = bits & self.area_int
        area_share = _popcount(in_area) / max(1, self.area_px)
        result = {'global_share': global_share, 'area_share': area_share, 'box': None,
                  'largest_px': 0, 'verdict': 'still'}
        if global_share >= self.m['global_fraction']:
            result['verdict'] = 'scene'
            return result
        if not in_area:
            return result
        found = self.blobs(in_area.to_bytes(self.n, 'big'))
        largest = max(found)
        result['largest_px'] = largest[0]
        if not self.m.get('size_filter', True):
            x0, y0, x1, y1 = largest[1]
            result.update(verdict='motion', box=[round(x0 / self.w, 4), round(y0 / self.h, 4),
                                                 round(x1 / self.w, 4), round(y1 / self.h, 4)])
        elif largest[0] > self.max_blob_px:
            result['verdict'] = 'large'
        elif largest[0] >= self.m['min_blob_px']:
            x0, y0, x1, y1 = largest[1]
            result.update(verdict='motion', box=[round(x0 / self.w, 4), round(y0 / self.h, 4),
                                                 round(x1 / self.w, 4), round(y1 / self.h, 4)])
        else:
            result['verdict'] = 'small'
        return result


class MotionRules:
    """Per-frame verdicts in, confirmed motion times and scene changes out. Pure logic."""

    def __init__(self, fps, persist_s, max_gap_frames, scene_cooldown_s):
        self.needed = max(1, round(persist_s * fps))
        self.max_gap, self.cooldown = max_gap_frames, scene_cooldown_s
        self.scene_until = float('-inf')
        self._reset()

    def _reset(self):
        self.run, self.gap, self.waiting = 0, 0, []

    def frame(self, t, verdict):
        """Return (motion times to report, True if a new scene change started)."""
        if verdict == 'scene':
            new = t >= self.scene_until
            self.scene_until = t + self.cooldown
            self._reset()
            return [], new
        if t < self.scene_until:
            return [], False
        if verdict == 'motion':
            self.run, self.gap = self.run + 1, 0
            self.waiting.append(t)
            if self.run >= self.needed:
                out, self.waiting = self.waiting, []
                return out, False
            return [], False
        if self.run:
            self.gap += 1
            if self.gap > self.max_gap:
                self._reset()
        return [], False

    def label(self, t, verdict):
        if verdict != 'scene' and t < self.scene_until:
            return 'settling'
        if verdict == 'motion' and self.run < self.needed:
            return 'pending'
        return verdict


def load_roi(m):
    """Detection area from the web page's file, else the config, else None (whole frame)."""
    try:
        return valid_roi(json.loads(Path(m['roi_file']).read_text()).get('points'))
    except (OSError, ValueError, AttributeError):
        return valid_roi(m['roi']) if m['roi'] else None


class MotionDetector:
    """Second FFmpeg process on the substream. A reader thread stamps each frame with
    ROCK receive time, so a busy main loop does not delay the stamp."""

    def __init__(self, cfg, log):
        m = cfg['motion']
        self.m, self.log = m, log
        self.events, self.scenes = queue.Queue(), queue.Queue()
        self.analyzer = FrameAnalyzer(m, load_roi(m))
        self.rules = MotionRules(m['fps'], m['persist_s'], m['max_gap_frames'], m['scene_cooldown_s'])
        self.last, self.last_frame = None, None
        tcfg = m.get('tracker') or {}
        self.tracker = tracker.Tracker(tcfg, m['width'], m['height'], self.analyzer.area_mask) \
            if tcfg.get('enabled', True) else None
        self.track_state, self.track_trail = None, []
        self.track_file = Path(cfg['output_dir']) / 'track.jsonl'
        self.roi_mtime = self._roi_mtime()
        if m['input_args'] is not None:
            args = list(m['input_args'])
        else:
            uri = json.loads(Path(m['source_config']).read_text())['uri']
            args = ['-rtsp_transport', 'tcp', '-timeout', '10000000', '-i', uri]
        cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error'] + args + \
              ['-an', '-vf', motion_filter(m), '-f', 'rawvideo', '-pix_fmt', 'gray', 'pipe:1']
        self.proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL)
        self.thread = threading.Thread(target=self._read, daemon=True)
        self.thread.start()
        log('detector_started', fps=m['fps'], size=[m['width'], m['height']],
            pixel_threshold=m['pixel_threshold'], roi=self.analyzer.roi,
            global_fraction=m['global_fraction'], min_blob_px=m['min_blob_px'],
            max_blob_fraction=m['max_blob_fraction'], size_filter=m['size_filter'],
            persist_s=m['persist_s'], mask=m['mask'])

    def _roi_mtime(self):
        try:
            return os.stat(self.m['roi_file']).st_mtime
        except OSError:
            return None

    def _check_roi(self):
        mtime = self._roi_mtime()
        if mtime != self.roi_mtime:
            self.roi_mtime = mtime
            self.analyzer.set_roi(load_roi(self.m))
            if self.tracker:
                self.tracker.set_area(self.analyzer.area_mask)   # start over in the new area
            self.log('roi_changed', roi=self.analyzer.roi, area_px=self.analyzer.area_px)

    def _read(self):
        size = self.analyzer.n
        counts, since, roi_checked, logged = {}, time.time(), 0.0, 0.0
        while True:
            pair = self.proc.stdout.read(2 * size)
            if len(pair) < 2 * size:
                return
            frame, gray = pair[:size], pair[size:]
            now = time.time()
            if now - roi_checked >= 1:
                self._check_roi()
                roi_checked = now
            r = self.analyzer.analyze(frame)
            times, scene = self.rules.frame(now, r['verdict'])
            if self.tracker:
                logged = self._track(now, gray, frame, r['verdict'] == 'scene', logged)
            r['label'] = self.rules.label(now, r['verdict'])
            self.last, self.last_frame = r, now
            counts[r['label']] = counts.get(r['label'], 0) + 1
            for t in times:
                self.events.put(t)
            if scene:
                self.scenes.put((now, round(r['global_share'], 3)))
            if now - since >= self.m['stats_every_s']:
                self.log('motion_stats', frames=sum(counts.values()), verdicts=counts)
                counts, since = {}, now

    def _track(self, now, gray, change, scene, logged):
        """Feed the tracker; log state changes and one position a second."""
        st = self.tracker.frame(now, gray, change, scene=scene)
        prev = self.track_state['state'] if self.track_state else None
        self.track_state, self.track_trail = st, self.tracker.trail(now)
        if st['state'] != prev:
            self.log('track_state', state=st['state'], prev=prev, x=st.get('x'), y=st.get('y'))
        if now - logged >= 1 and 'x' in st:
            with open(self.track_file, 'a') as f:
                f.write(json.dumps({'t': round(now, 3), 'state': st['state'], 'x': st['x'], 'y': st['y']}) + '\n')
            return now
        return logged

    def drain(self):
        return self._drain(self.events)

    def drain_scenes(self):
        return self._drain(self.scenes)

    @staticmethod
    def _drain(q):
        out = []
        while True:
            try:
                out.append(q.get_nowait())
            except queue.Empty:
                return out

    def alive(self):
        return self.proc.poll() is None

    def stop(self):
        if self.alive():
            self.proc.send_signal(signal.SIGINT)
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


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
        self.detector, self.detector_restart_at = None, 0.0
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

    def ensure_detector(self, now):
        if not self.cfg['motion']['enabled'] or (self.detector and self.detector.alive()):
            return
        if self.detector:
            self.log('detector_exited', code=self.detector.proc.returncode)
            self.detector = None
            self.detector_restart_at = now + 3
        if now >= self.detector_restart_at:
            self.detector = MotionDetector(self.cfg, self.log)

    def read_motion(self):
        if not self.detector:
            return
        times = self.detector.drain()
        for t in times:
            self.pending += self.tracker.motion(t, source='motion')
        if times:
            self.log('motion', source='motion', first=round(times[0], 3), last=round(times[-1], 3),
                     frames=len(times))
        for t, share in self.detector.drain_scenes():
            # Not motion: noted for the web timeline only.
            self.log('scene_change', at=round(t, 3), global_share=share)
            with open(Path(self.cfg['output_dir']) / 'scene_changes.jsonl', 'a') as f:
                f.write(json.dumps({'t': round(t, 3), 'global_share': share}) + '\n')

    def read_requests(self):
        for path in sorted(self.requests.glob('*.json')):
            try:
                req = json.loads(path.read_text())
                t = float(req['t'])
                for event in self.tracker.motion(t, t + float(req.get('hold', 0)), source='manual'):
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

    def write_state(self, now):
        """Status for the web page, rewritten atomically about twice a second."""
        if now - getattr(self, '_state_at', 0) < 0.5:
            return
        self._state_at = now
        e = self.tracker.open
        d = self.detector
        state = {
            't': round(now, 3),
            'pre_roll_s': self.cfg['pre_roll_s'], 'still_s': self.cfg['still_s'],
            'segmenter_alive': bool(self.run and self.run.alive()),
            'detector_enabled': self.cfg['motion']['enabled'],
            'detector_alive': bool(d and d.alive()),
            'detector': None if not d or d.last is None else {
                'at': round(d.last_frame, 3), 'label': d.last['label'],
                'global_share': round(d.last['global_share'], 4),
                'area_share': round(d.last['area_share'], 4), 'box': d.last['box'],
                'largest_px': d.last['largest_px']},
            'roi': d.analyzer.roi if d else load_roi(self.cfg['motion']),
            'tracker': None if not d or not d.track_state else {**d.track_state, 'trail': d.track_trail},
            'global_fraction': self.cfg['motion']['global_fraction'],
            'ring_seconds': round(sum(s.wall_end - s.wall_start for s in self.segments), 1),
            'open_event': None if e is None else {
                'event_id': e.event_id, 'first_motion': round(e.start, 3),
                'last_motion': round(e.last_motion, 3), 'sources': sorted(e.sources)},
            'pending_events': len(self.pending),
        }
        tmp = self.ring / 'state.json.part'
        tmp.write_text(json.dumps(state))
        tmp.rename(self.ring / 'state.json')

    def loop(self):
        self.log('recorder_started', pre_roll_s=self.cfg['pre_roll_s'], still_s=self.cfg['still_s'],
                 segment_seconds=self.cfg['segment_seconds'], ring_seconds=self.cfg['ring_seconds'])
        while not self.stopping:
            now = time.time()
            self.ensure_segmenter(now)
            self.ensure_detector(now)
            if self.run:
                fresh = self.run.poll()
                if fresh and self.segments and fresh[0].wall_start - self.segments[-1].wall_end > 0.5:
                    self.log('stream_gap', start=round(self.segments[-1].wall_end, 3),
                             end=round(fresh[0].wall_start, 3))
                self.segments += fresh
            self.read_requests()
            self.read_motion()
            self.pending += self.tracker.poll(now)
            self.assemble_ready(now)
            self.cleanup(now)
            self.write_state(now)
            time.sleep(0.1)
        self.shutdown()

    def shutdown(self):
        now = time.time()
        if self.tracker.open:
            self.pending.append(self.tracker._close(now, 'shutdown'))
        if self.detector:
            self.detector.stop()
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
