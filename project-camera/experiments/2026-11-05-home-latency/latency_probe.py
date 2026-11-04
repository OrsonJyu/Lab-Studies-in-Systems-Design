#!/usr/bin/env python3
"""Latency probe run on the ROCK while the camera watches a millisecond clock.

FFmpeg copies the main stream (no decode) to two outputs: a framecrc line per
packet, flushed immediately and stamped by this script with the ROCK wall clock
on arrival, and an MKV kept only long enough to extract frames as JPEG.

A: continuous 20 s; one JPEG per 20 packets for reading the clock.
B: cold starts, as a "start recording on trigger" design would; launch time,
   first packet and first keyframe arrival, first decodable frame as JPEG.
Results stream back as a tar on stdout. The stream URI is never printed and no
video file is kept on the board.
"""
import io, json, os, random, shutil, subprocess, sys, tarfile, time

URI = json.load(open(os.path.expanduser('~/sd5531/private/camera_source.json')))['uri']
WORK = '/tmp/sd5531-latency'
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK)


def capture(seconds, mkv):
    """Return (launch_time, [arrival times per video packet], ffmpeg exit)."""
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error', '-rtsp_transport', 'tcp',
           '-timeout', '10000000', '-i', URI, '-t', str(seconds),
           '-map', '0:v:0', '-c', 'copy', '-f', 'framecrc', '-flush_packets', '1', 'pipe:1',
           '-map', '0:v:0', '-c', 'copy', '-t', str(seconds), '-y', mkv]
    launch = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
    stamps, pending = [], b''
    while True:
        chunk = p.stdout.read(4096)
        if not chunk:
            break
        now = time.time()
        pending += chunk
        *lines, pending = pending.split(b'\n')
        stamps += [now for line in lines if line and not line.startswith(b'#')]
    return launch, stamps, p.wait()


def keyflags(mkv):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                          '-show_entries', 'packet=flags', '-of', 'csv=p=0', mkv],
                         capture_output=True, text=True).stdout.split()
    return ['K' in f for f in out]


def jpeg(mkv, index, out):
    subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error', '-i', mkv,
                    '-vf', f"select='eq(n\\,{index})',scale=1280:-2", '-frames:v', '1',
                    '-q:v', '3', '-y', out], check=False)


summary = {'board_clock': 'set from Mac on 2026-11-05, about 10 ms residual',
           'stamp': 'ROCK time.time() when the framecrc line of each copied packet reached this script'}

mkv = f'{WORK}/a.mkv'
launch, stamps, code = capture(20, mkv)
keys = keyflags(mkv)
gaps = [b - a for a, b in zip(stamps, stamps[1:])]
summary['A'] = {
    'exit': code, 'packets': len(stamps), 'mkv_packets': len(keys), 'keyframes': sum(keys),
    'arrival_gap_s': {'min': round(min(gaps), 4), 'max': round(max(gaps), 4),
                      'mean': round(sum(gaps) / len(gaps), 4)} if gaps else None,
    'gaps_over_100ms': sum(1 for g in gaps if g > 0.1),
    'saved': []}
# Decoded frame index equals packet index only after the first keyframe.
first_key = keys.index(True) if True in keys else 0
for n in range(first_key, min(len(stamps), len(keys)), 20):
    name = f'a_{n:03d}.jpg'
    jpeg(mkv, n - first_key, f'{WORK}/{name}')
    summary['A']['saved'].append({'file': name, 'packet': n, 'arrival_unix': round(stamps[n], 3),
                                  'key': keys[n]})
os.remove(mkv)

trials = []
for i in range(6):
    time.sleep(2 + random.random() * 2)
    mkv = f'{WORK}/b.mkv'
    launch, stamps, code = capture(4, mkv)
    keys = keyflags(mkv)
    k = keys.index(True) if True in keys else None
    name = f'b_{i + 1}.jpg'
    jpeg(mkv, 0, f'{WORK}/{name}')
    trials.append({'trial': i + 1, 'exit': code, 'launch_unix': round(launch, 3),
                   'first_packet_s': round(stamps[0] - launch, 3) if stamps else None,
                   'first_packet_is_key': keys[0] if keys else None,
                   'first_keyframe_s': round(stamps[k] - launch, 3) if k is not None and k < len(stamps) else None,
                   'packets_before_first_key': k, 'first_decodable_jpeg': name})
    os.remove(mkv)
summary['B'] = trials

with open(f'{WORK}/summary.json', 'w') as f:
    json.dump(summary, f, indent=1)
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w:gz') as tar:
    tar.add(WORK, arcname='latency')
shutil.rmtree(WORK)
sys.stdout.buffer.write(buf.getvalue())
