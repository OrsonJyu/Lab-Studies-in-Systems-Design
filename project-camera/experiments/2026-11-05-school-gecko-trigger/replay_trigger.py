import json, sys, tempfile, time
sys.path.insert(0, sys.argv[1])
import recorder
tmp = tempfile.mkdtemp()
cfg = recorder.load_config(None); cfg['output_dir'] = tmp
roi = [[0.1194, 0.1092], [0.0937, 0.904], [0.9526, 0.9186], [0.895, 0.1637]]
cfg['motion'].update(enabled=True, pixel_threshold=15, size_filter=False, roi=roi, roi_file=tmp + '/none.json',
                     trigger='gecko', input_args=['-re', '-i', sys.argv[2]])
states = []
orig = recorder.MotionDetector._track
def spy(self, now, *a, **k):
    r = orig(self, now, *a, **k); states.append((round(now - t0, 1), self.track_state['state'])); return r
recorder.MotionDetector._track = spy
t0 = time.time()
det = recorder.MotionDetector(cfg, lambda *a, **k: None)
det.proc.wait(120); det.thread.join(5)
ev = [round(t - t0, 1) for t in det.drain()]; sh = [round(t - t0, 1) for t in det.drain_shadow()]
def spans(ts):
    out = []
    for t in ts:
        if out and t - out[-1][1] <= 1.0: out[-1][1] = t
        else: out.append([t, t])
    return out
print('gecko trigger spans (s):', spans(ev))
print('change-rule spans (s):  ', spans(sh))
chg = [s for i, s in enumerate(states) if i == 0 or s[1] != states[i - 1][1]]
print('track changes:', chg[:30])
