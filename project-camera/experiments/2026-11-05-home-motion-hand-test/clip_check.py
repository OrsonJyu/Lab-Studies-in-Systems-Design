import glob, json, os, re, subprocess
F = """fps=20,scale=160:90,format=gray,drawbox=x=iw*0:y=ih*0:w=iw*0.45:h=ih*0.09:color=black:t=fill,drawbox=x=iw*0:y=ih*0.9:w=iw*0.25:h=ih*0.1:color=black:t=fill,tblend=all_mode=difference,lutyuv=y='if(gt(val,25),255,0)',signalstats,metadata=print:key=lavfi.signalstats.YAVG"""
out = []
for js in sorted(glob.glob(os.path.expanduser('~/sd5531/events-motiontest/2*.json'))):
    r = json.load(open(js)); mp4 = js[:-5] + '.mp4'
    e = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'info', '-i', mp4, '-an', '-vf', F, '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    shares = [float(v) / 255 for v in re.findall(r'YAVG=([\d.]+)', e)]
    first = next((i for i in range(1, len(shares)) if shares[i] >= 0.005 and shares[i - 1] >= 0.005), None)
    first = first - 1 if first is not None else None
    d = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', mp4, '-f', 'null', '-'], capture_output=True, text=True)
    hand = None if first is None else first / 20
    clip0 = r['clip_window'][0]
    out.append({'event_id': r['event_id'], 'status': r['status'], 'source': r['source'], 'duration_s': r['duration_s'],
                'motions': r['motions'], 'first_motion': r['first_motion'], 'last_motion': r['last_motion'], 'event_end': r['event_end'],
                'clip_window': r['clip_window'], 'actual_pre_roll_s': r['actual_pre_roll_s'],
                'hand_first_seen_in_clip_s': hand,
                'hand_first_seen_receive_time': None if hand is None else round(clip0 + hand, 3),
                'detection_delay_s': None if hand is None else round(r['first_motion'] - (clip0 + hand), 3),
                'clip_before_hand_s': hand, 'clip_after_last_motion_s': round(r['clip_window'][1] - r['last_motion'], 3),
                'full_decode_exit': d.returncode})
print(json.dumps(out, indent=1))
