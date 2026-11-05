"""Replay a recorded clip through the detector + tracker and record the box per frame."""
import json, sys, tempfile, time
sys.path.insert(0, sys.argv[1])
import recorder
clip, out = sys.argv[2], sys.argv[3]
tmp = tempfile.mkdtemp()
cfg = recorder.load_config(None)
cfg['output_dir'] = tmp
roi = [[0.1194, 0.1092], [0.0937, 0.904], [0.9526, 0.9186], [0.895, 0.1637]]
cfg['motion'].update(enabled=True, pixel_threshold=15, size_filter=False, roi=roi, roi_file=tmp + '/none.json',
                     input_args=['-re', '-i', clip])
rows = []
orig = recorder.MotionDetector._track
def spy(self, now, *a, **k):
    r = orig(self, now, *a, **k)
    st = self.track_state
    rows.append({'t': round(now - t0, 2), 'state': st['state'], 'box': st.get('box')})
    return r
recorder.MotionDetector._track = spy
t0 = time.time()
det = recorder.MotionDetector(cfg, lambda *a, **k: None)
det.proc.wait(120); det.thread.join(5)
json.dump(rows, open(out, 'w'))
print(len(rows), rows[-1])
