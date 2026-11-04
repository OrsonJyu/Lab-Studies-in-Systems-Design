#!/usr/bin/env python3
"""On the ROCK: run recorder.py against the camera, fire three manual trigger
patterns, stop, and return event JSONs, the log and first/last frames as a tar."""
import io, json, shutil, subprocess, sys, tarfile, time
from pathlib import Path

HOME = Path.home() / 'sd5531'
REC = HOME / 'recorder' / 'recorder.py'
CFG = HOME / 'recorder' / 'config.json'
OUT = HOME / 'events-hwtest'
cfg = json.loads(CFG.read_text())
cfg['output_dir'] = str(OUT)
test_cfg = HOME / 'recorder' / 'config-hwtest.json'
test_cfg.write_text(json.dumps(cfg))
shutil.rmtree(OUT, ignore_errors=True)


def trigger(hold=0):
    t = time.time()
    subprocess.run(['python3', str(REC), 'trigger', '--config', str(test_cfg), '--hold', str(hold)],
                   check=True, capture_output=True)
    return round(t, 3)


def wait_events(n, limit):
    end = time.time() + limit
    while time.time() < end and len(list(OUT.glob('*.json'))) < n:
        time.sleep(0.5)


proc = subprocess.Popen(['python3', str(REC), 'run', '--config', str(test_cfg)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
plan = []
try:
    time.sleep(14)                                   # fill more than pre_roll in the ring
    plan.append({'case': 'single', 'triggers': [trigger()]})
    wait_events(1, 20); time.sleep(3)
    a = trigger(); time.sleep(3); b = trigger()
    plan.append({'case': 'two_within_still', 'triggers': [a, b]})
    wait_events(2, 25); time.sleep(3)
    plan.append({'case': 'hold_6s', 'triggers': [trigger(6)], 'hold': 6})
    wait_events(3, 30)
finally:
    proc.send_signal(2)
    err = proc.communicate(timeout=30)[1].decode()

frames = OUT / 'frames'
frames.mkdir()
for js in sorted(OUT.glob('*.json')):
    rec = json.loads(js.read_text())
    mp4 = OUT / rec.get('file', 'missing.mp4')
    if mp4.exists():
        for tag, args in [('first', []), ('last', ['-sseof', '-0.2'])]:
            subprocess.run(['ffmpeg', '-v', 'error', *args, '-i', str(mp4), '-frames:v', '1',
                            '-vf', 'scale=1280:-2', '-q:v', '3', '-y',
                            str(frames / f"{rec['event_id']}-{tag}.jpg")])
        d = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(mp4), '-f', 'null', '-'],
                           capture_output=True, text=True)
        rec['full_decode_exit'] = d.returncode
        js.write_text(json.dumps(rec, indent=1))
(OUT / 'plan.json').write_text(json.dumps({'plan': plan, 'recorder_exit': proc.returncode,
                                           'recorder_stderr_tail': err[-500:]}, indent=1))
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w:gz') as tar:
    for p in OUT.rglob('*'):
        if p.suffix != '.mp4':
            tar.add(p, arcname=str(p.relative_to(OUT)))
sys.stdout.buffer.write(buf.getvalue())
