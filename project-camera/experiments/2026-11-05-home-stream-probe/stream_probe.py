#!/usr/bin/env python3
"""Read-only stream probe on the ROCK: keyframe cadence and decode CPU cost.

Reads the stream URIs saved by onvif_probe.py, prints only redacted numbers,
writes no media. The private URI file is removed at the end.
"""
import json, os, resource, statistics, subprocess, time

PRIV = os.path.expanduser('~/sd5531/private/probe-stream-uris.json')
uris = json.load(open(PRIV))
out = {'read_only': True, 'media_saved': False}


def packets(uri, seconds):
    cmd = ['ffprobe', '-v', 'error', '-rtsp_transport', 'tcp', '-timeout', '10000000',
           '-read_intervals', f'%+{seconds}', '-select_streams', 'v:0',
           '-show_entries', 'packet=pts_time,dts_time,flags,size', '-of', 'json', uri]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=seconds + 30)
    wall = time.time() - t0
    pk = json.loads(r.stdout or '{}').get('packets', [])
    pts = [float(p['pts_time']) for p in pk if p.get('pts_time') not in (None, 'N/A')]
    keys = [float(p['pts_time']) for p in pk if 'K' in p.get('flags', '') and p.get('pts_time') not in (None, 'N/A')]
    gaps = [b - a for a, b in zip(keys, keys[1:])]
    deltas = [b - a for a, b in zip(pts, pts[1:])]
    return {'exit': r.returncode, 'stderr_lines': len(r.stderr.splitlines()),
            'wall_s': round(wall, 2), 'packets': len(pk),
            'stream_span_s': round(pts[-1] - pts[0], 3) if len(pts) > 1 else None,
            'keyframes': len(keys),
            'keyframe_interval_s': {'min': round(min(gaps), 3), 'median': round(statistics.median(gaps), 3),
                                    'max': round(max(gaps), 3)} if gaps else None,
            'frame_delta_s': {'median': round(statistics.median(deltas), 4), 'max': round(max(deltas), 4)} if deltas else None,
            'nonmonotonic_pts': sum(1 for d in deltas if d <= 0),
            'mean_packet_bytes': round(statistics.mean(int(p['size']) for p in pk)) if pk else None}


def decode_cost(uri, seconds):
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error', '-rtsp_transport', 'tcp',
           '-timeout', '10000000', '-i', uri, '-t', str(seconds), '-an', '-f', 'null', '-']
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=seconds + 30)
    wall = time.time() - t0
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (after.ru_utime - before.ru_utime) + (after.ru_stime - before.ru_stime)
    return {'exit': r.returncode, 'stderr_lines': len(r.stderr.splitlines()), 'decode_s': seconds,
            'wall_s': round(wall, 2), 'cpu_s': round(cpu, 2),
            'avg_cores_busy': round(cpu / wall, 2), 'share_of_6_cores_pct': round(100 * cpu / wall / 6, 1),
            'max_rss_mb': round(after.ru_maxrss / 1024, 1)}


try:
    out['keyframes_main'] = packets(uris['000'], 12)
    out['keyframes_sub'] = packets(uris['001'], 12)
    out['decode_sub_30s'] = decode_cost(uris['001'], 30)
    out['decode_main_15s'] = decode_cost(uris['000'], 15)
    out['loadavg_after'] = os.getloadavg()
finally:
    os.remove(PRIV)
    out['private_uri_file_removed'] = not os.path.exists(PRIV)
print(json.dumps(out, indent=1))
