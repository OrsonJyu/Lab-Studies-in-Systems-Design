"""Build the Confluence storage-format body for ZHU Kecheng's Assignment 3 page."""
import html, os

REPO = 'https://github.com/OrsonJyu/Lab-Studies-in-Systems-Design'
TREE = REPO + '/tree/main/project-camera'
FIGMA = 'https://www.figma.com/design/sxi53cbglPTcFEPPy2EYiu/SD5531-Super-Gecko-Team?node-id=2067-43'
COURSE_CAM = 'https://www.designandmake.org/display/DFL/Demonstration+Module+-+IP+Cam+with+POE'
E = html.escape


def p(t): return f'<p>{t}</p>'
def h(n, t): return f'<h{n}>{E(t)}</h{n}>'
def a(url, t): return f'<a href="{E(url)}">{E(t)}</a>'
def att(name, t=None): return (f'<ac:link><ri:attachment ri:filename="{E(name)}"/>'
                                f'<ac:plain-text-link-body><![CDATA[{t or name}]]></ac:plain-text-link-body></ac:link>')
def img(name, width=900, cap=None):
    s = f'<p><ac:image ac:width="{width}"><ri:attachment ri:filename="{E(name)}"/></ac:image></p>'
    return s + (f'<p><em>{cap}</em></p>' if cap else '')
def video(name, width=640, height=360, cap=None):
    s = (f'<p><ac:structured-macro ac:name="multimedia" ac:schema-version="1">'
         f'<ac:parameter ac:name="width">{width}</ac:parameter><ac:parameter ac:name="height">{height}</ac:parameter>'
         f'<ac:parameter ac:name="name"><ri:attachment ri:filename="{E(name)}"/></ac:parameter>'
         f'<ac:parameter ac:name="autostart">false</ac:parameter></ac:structured-macro></p>')
    return s + (f'<p><em>{cap} ({att(name, "download")})</em></p>' if cap else '')
def table(head, rows):
    th = ''.join(f'<th>{c}</th>' for c in head)
    body = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table><tbody><tr>{th}</tr>{body}</tbody></table>'
def macro(name, body, title=None):
    t = f'<ac:parameter ac:name="title">{E(title)}</ac:parameter>' if title else ''
    return f'<ac:structured-macro ac:name="{name}" ac:schema-version="1">{t}<ac:rich-text-body>{body}</ac:rich-text-body></ac:structured-macro>'
def ul(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
def iteration(title, problem, change, result, extra=''):
    return h(3, title) + table(['', ''], [['<strong>Question / problem</strong>', problem],
                                          ['<strong>What I built or changed</strong>', change],
                                          ['<strong>Measured result</strong>', result]]) + extra


B = []
B.append(p('<strong>Contributor: ZHU Kecheng · Team 02 · SD5531 Assignment 3 (individual technical feasibility study)</strong>'))
B.append(p('<strong>Prototype:</strong> course PoE IP camera + 48 V PoE injector + isolated gigabit switch + Radxa ROCK 4C+ '
           'running my FFmpeg/Python event recorder, viewed and stored on a MacBook.'))
B.append(p(f'<strong>Source code (GitHub):</strong> {a(REPO, REPO)} · camera module: {a(TREE, "project-camera/")} · '
           f'<strong>Slides:</strong> {a(FIGMA, "camera-module section in our team Figma deck")}'))
B.append(macro('info', ul([
    '<strong>Sensor evaluated:</strong> PoE IP camera (GK7205V200, 2560×1440 H.264 at 20 fps + 800×448 substream, ONVIF), powered over the network cable.',
    '<strong>Target controller:</strong> Radxa ROCK 4C+ (RK3399, Debian 12) instead of ESP32-C3, because the camera delivers compressed video over Ethernet (reasons in section 4.1).',
    '<strong>Main result:</strong> the recorder keeps the 4–6 s <em>before</em> each movement, and in the final on-site test it recorded only when the tracked (toy) gecko moved: 3 of 3 clips correct, 0 clips of a hand moving in the enclosure.',
    '<strong>Not yet shown:</strong> a real gecko, night (IR) recording and multi-day running. These are listed in section 8.']), 'At a glance'))
B.append('<ac:structured-macro ac:name="toc" ac:schema-version="1"><ac:parameter ac:name="maxLevel">2</ac:parameter></ac:structured-macro>')

# requirement map
B.append(h(2, '0. Where each assignment requirement is answered'))
B.append(table(['Assignment 3 · item 3(b)', 'Section on this page'], [
    ['(i) What sensor/actuator did you evaluate?', '1. What I evaluated'],
    ['(ii) Online references on how to use it', '3. Online references and how I used them'],
    ['(iii) Why use it, and how it is used in our design solution', '2. Why this sensor, and how it fits Project 2'],
    ['(iv) Adapting to the target controller: EasyEDA schematic (screen capture + zipped file) and source code with build/run instructions',
     '4. Adapting the design to my target controller (4.2 schematic, 4.4 source code)'],
    ['(v) Photos and videos of the prototype, its physical structure and how it works', '5. Prototype, process and evidence'],
    ['(vi) Summary, reflection on suitability and improvements', '6. Results summary · 7. Reflection · 8. Further validation'],
    ['3(c) Who contributed', '9. Contribution statement']]))

# 1
B.append(h(2, '1. What I evaluated'))
B.append(p('I evaluated whether a PoE IP camera, driven by a small Linux board, can produce useful gecko video automatically: '
           'start recording when the gecko moves, keep the moment before it moved, ignore people and lighting changes, and '
           'hand each clip over with a verifiable record.'))
B.append(table(['Role', 'Part', 'What matters for this study'], [
    ['Sensor', 'PoE IP camera from the course demonstration module (GK7205V200 SoC, 2.8 mm lens, 940 nm IR LEDs)',
     'Main stream 2560×1440 H.264, 20 fps, keyframe every 2 s; substream 800×448; RTSP video; ONVIF for device control (clock). No microphone.'],
    ['Power for the sensor', '48 V PoE injector with its own mains cord', 'Puts 48 V on the same Cat5e cable that carries the video (no separate camera power cable).'],
    ['Network', '8-port gigabit switch with its own power adapter', 'Isolated wired network: camera, ROCK and Mac only; no internet on this network.'],
    ['Target controller', 'Radxa ROCK 4C+ (RK3399, 6 cores), Debian 12, Python 3.11, FFmpeg 5.1',
     'Receives both streams, keeps the RAM ring buffer, runs detection and tracking, serves the live web page.'],
    ['Host', 'MacBook + USB-C dock (Ethernet)', 'Web view, clip storage (recordings/), and USB-C power for the ROCK 4C+.']]))

# 2
B.append(h(2, '2. Why this sensor, and how it fits Project 2 (Video Recording Module)'))
B.append(p('Team 02 is assigned <strong>Project 2: Video Recording Module</strong> of the Final Project (an IoT system that helps '
           'primary and secondary students observe and care for a leopard gecko). Video is the only sensor in our system that '
           'gives evidence a student can replay: where the gecko went, when it was active, and what happened before. '
           'Leopard geckos are mostly active at dusk and night, so the camera’s 940 nm IR illumination matters for later work.'))
B.append(p('Following step 2 of the course’s Generic Workflow, I defined the data input, processing logic and output:'))
B.append(table(['Data input', 'Processing logic', 'Data output'], [
    ['Main stream (2560×1440) for the record; substream (800×448) for analysis; camera clock via ONVIF',
     'Keep the last 60 s in RAM. Find changes inside the area we drew; ignore whole-picture changes; locate and lock on the gecko; '
     'start an event when the locked gecko really moves for 0.5 s; end it after 5 s of stillness.',
     'One MP4 clip per event (from ~4 s before the first movement) + JSON record (times, segments, SHA-256), moved to the host; '
     'live web page with the gecko box, detection area and a clickable timeline.']]))
B.append(p('Scenarios this has to handle:'))
B.append(ul(['The gecko walks out of its hide → a clip that also shows the seconds <em>before</em> it moved.',
             'A student’s hand or a teacher reaching in, people walking past, lights switched on → <strong>no</strong> clip.',
             'Other teams (Hide, feeders, thermal) need clips with trustworthy times → the camera clock is set from the ROCK at every start, '
             'and every clip has a JSON record.']))

# 3
B.append(h(2, '3. Online references and how I used them'))
B.append(table(['Reference', 'What I took from it', 'What I had to change'], [
    [a(COURSE_CAM, 'Course page: Demonstration Module - IP Cam with POE'),
     'Camera and 48 V injector models, Cat5e cabling, PoE start-up checks (injector LED, link LED).',
     'The course setup views the camera from a Windows PC with the vendor “Video Play Tool” browser plugin. That plugin does not run on macOS '
     'or on the board, so I used the standard RTSP and ONVIF interfaces instead.'],
    [a('https://medium.com/@tom.humph/saving-rtsp-camera-streams-with-ffmpeg-baab7e80d767', 'Saving RTSP camera streams with FFmpeg (linked from the course page)'),
     'Recording an RTSP stream with FFmpeg using stream copy (no re-encoding).',
     'Recording continuously into short segments in RAM and cutting clips around events, instead of one long file.'],
    [a('https://ffmpeg.org/ffmpeg-formats.html#segment', 'FFmpeg segment muxer') + ' and ' + a('https://ffmpeg.org/ffmpeg-formats.html#concat-1', 'concat demuxer'),
     '2 s MPEG-TS segments with a live CSV list; joining segments without re-encoding.',
     'Segments are timed by their arrival on the ROCK, and a clip starts at a keyframe boundary ≥ 4 s before the first motion.'],
    [a('https://ffmpeg.org/ffmpeg-filters.html', 'FFmpeg filters: tblend, lut, extractplanes, vstack'),
     'Frame differencing and thresholding inside FFmpeg, so Python only counts pixels.',
     'One filter chain outputs 5 grey planes per frame (grey change, colour change, Y, U, V). I replaced lutyuv with lut on plain planes after '
     'finding lutyuv gives a constant 87 on full-range camera video (FFmpeg 8 on the Mac).'],
    [a('https://www.onvif.org/', 'ONVIF') + ' (Device Management: SetSystemDateAndTime)',
     'Reading and setting the camera clock without the vendor tool.', 'Small stdlib SOAP client (cam_time.py) with WS-Security digest; password typed by the user, never stored.'],
    [a('https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html', 'OpenCV tutorial: background subtraction'),
     'Idea of a background model and foreground mask for locating a moving object.',
     'Re-implemented in pure Python (no OpenCV/numpy on the board): median background, grey OR colour foreground, blob tracking.'],
    [a('https://docs.radxa.com/', 'Radxa documentation (ROCK 4 series)'), 'Board setup, Debian image, Ethernet.', 'Static wired address, SSH with a pinned host key.'],
    [a('https://flows.nodered.org/node/node-red-contrib-onvif', 'node-red-contrib-onvif (from the course page)'), 'Route to Node-RED integration.', 'Not done yet (section 8).']]))

# 4
B.append(h(2, '4. Adapting the design to my target controller'))
B.append(h(3, '4.1 Why a ROCK 4C+ and not an ESP32-C3'))
B.append(p('The assignment asks for evaluation on ESP32-C3 or the target controller. For this sensor the ESP32-C3 is not a workable target, '
           'so the target is the ROCK 4C+:'))
B.append(table(['Need', 'ESP32-C3', 'ROCK 4C+'], [
    ['Connect to a PoE IP camera', 'No Ethernet interface', 'Gigabit Ethernet'],
    ['Hold one 2560×1440 frame (≈5.5 MB as YUV 4:2:0)', '≈400 KB SRAM', 'Gigabytes of RAM; 60 s ring in /dev/shm'],
    ['Decode / copy H.264 video', 'No video decoder', 'FFmpeg 5.1; substream decode ≈3.6 % of the 6 cores'],
    ['Store and serve clips', 'No file system for video', 'Linux file system, Python web server']]))
B.append(p('An ESP32-C3 remains the right controller for the team’s simple sensors and actuators; the camera module connects to them later '
           'through Node-RED rather than through GPIO.'))
B.append(h(3, '4.2 Circuit: EasyEDA schematic and connections'))
B.append(p('The prototype has no breadboard: every connection is a cable between modules. I drew the as-built wiring and power in EasyEDA '
           '(Standard edition) with one symbol per module and one pin per connector. Screen capture from the EasyEDA editor:'))
B.append(img('01_EasyEDA_Schematic_Editor_Screenshot.jpg', 900, 'EasyEDA editor with the schematic open.'))
B.append(img('02_EasyEDA_Schematic.png', 900, 'Full-resolution export of the same sheet. Green = Ethernet/USB data, red = power.'))
B.append(p(f'<strong>EasyEDA file (zipped):</strong> {att("04_EasyEDA_Schematic_Source.zip")}. '
           'Open it in EasyEDA via File › Open › EasyEDA Source; a README inside the zip explains the files.'))
B.append(table(['#', 'From', 'To', 'Cable', 'Carries'], [
    ['1', 'MacBook left USB-C (upper)', 'MacBook charger', 'USB-C', 'Power for the Mac'],
    ['1', 'MacBook left USB-C (lower)', 'USB-C dock → its Ethernet port → switch', 'USB-C + Cat5e', 'Mac on the camera network'],
    ['2', 'MacBook right USB-C', 'ROCK 4C+ USB-C', 'USB-C', '<strong>5 V power for the ROCK</strong> (it has no adapter of its own)'],
    ['3', 'ROCK 4C+ Ethernet', 'Switch', 'Cat5e', 'RTSP video in, web page out'],
    ['4', 'Camera', 'PoE injector “POE” port', 'Cat5e', 'Video and 48 V power on one cable'],
    ['5', 'PoE injector “LAN” port', 'Switch', 'Cat5e', 'Camera video to the network'],
    ['6', 'PoE injector', 'Mains', 'Power cord', 'Injector power'],
    ['7', 'Switch', 'Mains', 'Power adapter', 'Switch power']]))
B.append(img('03_Hardware_Wiring_and_Power.png', 900, 'The same wiring as a picture (devices drawn with Figma AI; cables and ports drawn by me from the real setup).'))
B.append(h(3, '4.3 Software design on the ROCK 4C+'))
B.append(img('06_Information_Flow.png', 900, 'Two streams, two FFmpeg processes, one clip per event.'))
B.append(ul([
    '<strong>FFmpeg #1 (recorder):</strong> copies the main stream, without re-encoding, into 2 s MPEG-TS segments in a 60 s RAM ring (/dev/shm).',
    '<strong>FFmpeg #2 (detector):</strong> scales the substream to 160×90 at 10 fps and outputs, per frame, a grey-change mask (|ΔY| &gt; 15), '
    'a colour-change mask (|ΔU|+|ΔV| &gt; 24) and the Y, U, V planes.',
    '<strong>Python (standard library only):</strong> detection-area rules, gecko tracker, event logic, clip assembly, live web page (MJPEG + JSON API).',
    '<strong>Mac side:</strong> clips are copied, SHA-256-checked, and only then deleted on the ROCK; the camera clock is set over ONVIF at every start.']))
B.append(h(3, '4.4 Source code and how to build and run it'))
B.append(p(f'All code is in {a(REPO, "our GitHub repository")}; a snapshot of the files used here is attached as '
           f'{att("05_Source_Code_recorder_and_demo.zip")} (commit dfc2147 on branch code/demo-installer). Every attachment on this page, with its SHA-256, is also kept in ' + a(REPO + '/tree/main/project-camera/reports/2026-11-06-assignment3-individual', 'project-camera/reports/2026-11-06-assignment3-individual') + '. The code is Python 3 with the standard library only, '
           'so there is <strong>no compile step</strong>; FFmpeg does the video work.'))
B.append(table(['File', 'Purpose'], [
    ['project-camera/src/recorder/recorder.py', 'Ring-buffer recorder, FFmpeg filter chain, detection-area rules, event logic, clip assembly'],
    ['project-camera/src/recorder/tracker.py', 'Background model, colour foreground, blob tracking, “is the gecko really moving” rule'],
    ['project-camera/src/recorder/webview.py + webview.html', 'Live view, detection-area editor, gecko box and trail, event timeline'],
    ['project-camera/src/recorder/cam_time.py', 'Read/set the camera clock over ONVIF'],
    ['project-camera/demo/demo.py', 'One-command setup / start / status / stop / sync from any macOS or Linux host'],
    ['project-camera/src/recorder/test_*.py', '48 automated tests (all pass), including a full FFmpeg-pipeline test with a synthetic hand and gecko']]))
B.append(p('<strong>Requirements:</strong> ROCK 4C+ with Debian 12, Python ≥ 3.9 and FFmpeg; a macOS or Linux host with Python 3 and ssh; '
           'the camera, injector and switch wired as in 4.2, with static addresses on the isolated network.'))
B.append(ol(['<code>git clone ' + REPO + '.git</code> then <code>git checkout code/demo-installer</code> (the one-command installer is in ' + a(REPO + '/pull/12', 'pull request #12') + ' and not yet merged into main; the recorder itself is already on main)',
             '<code>python3 project-camera/demo/demo.py setup</code> — checks the network, logs in to the ROCK (password typed by the user), '
             'checks Python/FFmpeg, deploys the code with SHA-256 checks and runs the tests.',
             '<code>python3 project-camera/demo/demo.py start</code> — sets the clocks, starts recording and opens the web page; '
             'draw the detection area there.',
             '<code>python3 project-camera/demo/demo.py status</code> / <code>stop</code> — state, clip count; stop also moves the last clips to the host.',
             'Tests only: <code>python3 -m unittest discover -s project-camera/src/recorder</code>']))
B.append(p('Full step-by-step guide (Chinese, with an English section): ' + a(REPO + '/blob/code/demo-installer/project-camera/demo/README.md', 'project-camera/demo/README.md (branch code/demo-installer)') + '.'))

# 5
B.append(h(2, '5. Prototype, process and evidence'))
B.append(p('I built the module in small steps. Each step answered one question; when a test showed a problem, the next step fixed it. '
           'All tests were on the real camera and ROCK; a green toy lizard stood in for the gecko. Images marked “replay” were produced by '
           'feeding a recorded clip back through the same detector and tracker code, so that the boxes could be drawn on every frame.'))
B.append(h(3, '5.1 Physical setup'))
B.append(img('03_Hardware_Wiring_and_Power.png', 700))
B.append(p('<em>[PHOTOS OF THE REAL SETUP — to be added]</em>'))
B.append(iteration('5.2 Step 1 (30 Oct) — Can the ROCK receive and save the camera stream?',
    'First check of the whole chain: PoE camera → switch → ROCK, recording with FFmpeg over RTSP.',
    'FFmpeg on the ROCK records 60 s of the main stream with stream copy; the file is fully decoded and copied to the Mac with a SHA-256 check.',
    'Home: 1,201 frames in 60 s (20.4 fps, 2.1 Mbit/s, 0 dropped, 0 duplicated). School: 60.001 s, 1,200 frames, full decode with no errors, '
    'copy hash matched. FFmpeg warned about unset/non-monotonic timestamps from the camera, so clip timing must not rely on camera timestamps.',
    img('14_Test_first_recording_frame.jpg', 480, 'A frame from the first 60 s recording (IR lights on).')))
B.append(iteration('5.3 Step 2 (5 Nov, home) — How late is the video, and are the clocks right?',
    'If recording starts only after motion is seen, how much is lost? The camera’s on-screen clock was also wrong.',
    'Filmed a millisecond clock on the Mac screen and compared it with the ROCK’s receive time. Set the ROCK clock from the Mac, and the camera clock from the ROCK over ONVIF.',
    'Camera → ROCK delay 0.19–0.29 s (median 0.23 s). Starting FFmpeg after a trigger loses ≈0.4 s plus ≈2 s before the first output, so the start of a movement would be lost → '
    'a ring buffer is required. Camera clock was ≈28 days slow; after setting it, 0.3 s off. It resets on power loss, so it is now set automatically at every start.',
    img('15_Test_latency_clock.jpg', 900, 'Latency test: the camera films the Mac clock (left, middle); first frame received on the ROCK at school (right).')))
B.append(iteration('5.4 Step 3 — Never miss the start: RAM ring buffer',
    'Keep the seconds before a movement without recording everything to storage.',
    'FFmpeg #1 never stops and writes 2 s segments into a 60 s RAM ring. When an event closes, the segments from ≥4 s before the first motion to 5 s after the last motion are joined into one MP4.',
    'Manual triggers kept 5.0–5.6 s before the trigger; hand tests kept 3.7–4.65 s before the hand appeared, with 0.45–0.65 s detection delay. '
    'In the clip below the gecko was pulled at 5.1 s, and the pre-roll shows it still before that.',
    img('07_Code_ring_buffer_segmenter.png', 900) + img('08_Code_clip_assembly.png', 900) +
    video('21_Video_ring_buffer_timeline.mp4', 640, 360, 'A real clip with its timeline: cyan = pre-roll already in RAM, lime = gecko moving, grey = 5 s still, then close') +
    video('24_Video_raw_clip_gecko_pulled.mp4', 640, 360, 'The same clip as saved by the recorder (2560×1440, 21 s)')))
B.append(iteration('5.5 Step 4 — Stage 1: any changed pixel starts a recording',
    'Can simple frame differencing tell when something moved?',
    'motion_filter(): FFmpeg subtracts each 160×90 frame from the previous one and keeps pixels whose brightness changed by more than the threshold; a second mask does the same for colour.',
    'It reacts quickly, but in a real classroom it cannot tell <em>what</em> moved: 86 recordings in 2.5 h at school, mostly people, hands, lights and auto-exposure.',
    img('09_Code_motion_filter.png', 900) + img('16_Test_stage1_any_change.jpg', 900, 'Replay: camera frame and the change mask the rule sees, for a moving lizard (top) and for a hand only (bottom).')))
B.append(iteration('5.6 Step 5 — Stage 2: detection area and environment rules',
    'Ignore changes outside the enclosure and whole-picture changes.',
    'A polygon drawn on the web page becomes a bit mask (one AND per frame); ≥30 % of the whole picture changing counts as a lighting/scene change and is ignored for 2 s; '
    'motion must last 0.5 s. Threshold lowered from 25 to 15 so a moving lizard is caught.',
    'No triggers from activity outside the area in ≈2 min; one whole-picture change of 31.4 % (cause not visible) was classed as a scene change and ignored — only just above the 30 % limit; 201 still frames without a false trigger; ≈0.25 ms of analysis per frame. '
    'Problem left: a hand <em>inside</em> the area still records.',
    img('10_Code_area_rules.png', 900) + img('17_Test_stage2_detection_area.jpg', 900, 'Replay: blue = detection area, red = motion found inside it.')))
B.append(iteration('5.7 Step 6 — Where is the gecko? Background model and tracker',
    'To ignore hands, the system first has to know where the gecko is.',
    'Tracker: median background from still frames; foreground = grey difference &gt; 30 <em>or</em> colour difference &gt; 24; 8-connected blobs inside the area; lock on a blob that moves; '
    'follow it by overlap or appearance; absorb the “ghost” it leaves in the background.',
    'With brightness only, the box covered just the tail (lizard Y ≈ 157 vs desk 156–186). Adding colour (U 58 vs 102–115, V 81 vs 137–145): the box covered the whole lizard in 5 of 6 sampled frames, '
    'it stayed locked while still for 55 s, and reported “lost” correctly when the lizard was removed. Tracking costs ≈8 ms per frame (63 ms before optimising), ≈13 % CPU.',
    img('12_Code_tracker_foreground.png', 900) + img('20_Test_yuv_planes.jpg', 900, 'Why colour: in Y the lizard is nearly the desk’s grey; in U and V it stands out.') +
    img('19_Test_gecko_tracking.jpg', 900, 'Replay frames: the box while moving and resting.') +
    video('23_Video_gecko_box_replay.mp4', 640, 360, 'Replay: green box follows the gecko; the chip shows the tracker state')))
B.append(iteration('5.8 Step 7 — Stage 3: record only when the gecko itself moves',
    'With the gecko locked, a hand moving in the area still started recordings.',
    'Recording is triggered by the tracked gecko moving (area rules are only logged). “Moving” means the whole box shifts ≥2 px within 1 s with both opposite edges moving the same way; '
    'the blob followed must overlap the last box or look like the gecko and stay within 1/1.6–1.6× of its usual size; movement must last 0.5 s.',
    table(['On-site round', 'Hand-only clips', 'Cause → fix'], [
        ['1 (17:47)', '3', 'Pixel flicker from exposure/shadow counted as movement → require real travel + 0.5 s'],
        ['2 (18:04)', '2', 'Hand shadow merged with the gecko and pulled the box → whole-box edge shift, overlap/appearance check, size band'],
        ['3 (18:45)', '<strong>0</strong>', 'Hand in the area for 8 s: 87 frames fired the area rule, none recorded; 3 gecko clips kept']]),
    img('11_Code_gecko_trigger.png', 900) + img('13_Code_tracker_follow_shift.png', 900) +
    img('18_Test_stage3_gecko_trigger.jpg', 900, 'Replay: red = area rule fires, green = gecko box; only the gecko moving records.') +
    video('22_Video_hand_vs_gecko_replay.mp4', 640, 360, 'Replay: a hand waves while the gecko rests; the chips show what each trigger would do')))

# 6
B.append(h(2, '6. Results summary'))
B.append(table(['Question', 'Result', 'Evidence'], [
    ['Stream reception and saving', '60 s, 1,200–1,201 frames, fully decoded, hash-checked copy', '5.2'],
    ['Delay camera → ROCK', '0.19–0.29 s (median 0.23 s)', '5.3'],
    ['Seconds kept before a movement', '4–6 s (detection delay 0.45–0.65 s covered)', '5.4'],
    ['Changes outside the area / lighting', 'Ignored (0 triggers in ≈2 min; a 31.4 % whole-picture change ignored, small margin)', '5.6'],
    ['Locating the gecko', 'Whole lizard boxed in 5 of 6 sampled frames; 55 s still without a false “lost”', '5.7'],
    ['Hand moving in the area', '0 hand-only clips in the final on-site round', '5.8'],
    ['Load on the ROCK', '≈8 ms per frame for tracking, ≈13 % CPU', '5.7'],
    ['Clip handling', 'Moved to the Mac only after a SHA-256 match; 158 clips on the Mac on 5 Nov', '4.3']]))

# 7
B.append(h(2, '7. Reflection: is it suitable for our design solution?'))
B.append(p('<strong>Yes, for the daytime video recording function.</strong> The ring buffer solved the problem that mattered most for evidence (the start of a movement is never lost), '
           'and moving the trigger from “any change” to “the gecko moved” took false recordings from tens per hour to none in the final test. '
           'The board copes easily: the heavy per-pixel work stays inside FFmpeg and the Python analysis runs on 160×90 frames.'))
B.append(p('What I learned: each rule fixed one failure but exposed the next one (exposure flicker, then the hand’s shadow). Testing on site, replaying the recorded clips through the same code '
           'and writing each result down was what made the fixes possible.'))
B.append(p('<strong>Limitations:</strong>'))
B.append(ul(['All tests used a toy lizard in daylight; a real gecko is smaller, slower and often still for long periods, and the IR night mode is untested.',
             'Longest run so far is ≈2.5 h. The ROCK stopped suddenly twice on 5 Nov under light load. It is powered from the Mac’s USB-C port, which is the first suspect (not confirmed).',
             'The camera loses its clock when power is cut; this is handled by setting it at every start.',
             'When the gecko is pulled fast, the box can stay ≈2 s on the spot it left.',
             'Not yet connected to Node-RED or the other teams’ data; the module is not yet mounted on the enclosure.']))
B.append(p('<strong>Improvements:</strong> give the ROCK its own 5 V / 3 A supply and run for 24 h; test at night with IR and the real gecko; '
           'publish events (time, position, clip link) to Node-RED; agree camera position and field of view with the Enclosure and Hide teams.'))

# 8
B.append(h(2, '8. Further validation needed'))
B.append(table(['Test', 'Evidence to collect', 'Design decision it informs'], [
    ['Real gecko, day and night (IR)', 'Clips and tracker log over a full day/night cycle', 'Thresholds, IR settings, whether colour still helps at night'],
    ['Long run on independent power', '24 h log, restarts, missing segments', 'Power supply, watchdog / restart policy'],
    ['Mounting and field of view', 'Test shots from candidate positions on the enclosure', 'Camera position, cable route, detection area'],
    ['Node-RED integration', 'Events received in a Node-RED flow', 'Event format shared with other teams'],
    ['Storage over weeks', 'Disk use per day, clip retention', 'Retention policy, Mac vs SATA storage']]))

# 9
B.append(h(2, '9. Contribution statement'))
B.append(p('This page and the work on it are mine (ZHU Kecheng). I set up and wired the camera, PoE injector, switch and ROCK 4C+, ran every test at home and at school, '
           'decided each design change from the test results, drew the detection areas and judged each recorded clip. '
           'The code, test replays and documentation were developed with AI assistance (Claude Code) under my direction, and are versioned in our GitHub repository. '
           'The camera, injector and course demonstration-module information come from the course page linked in section 3. '
           'Teammates’ studies (e.g. the thermal array) are on their own pages.'))
B.append(h(2, 'Attachments'))
B.append('<ac:structured-macro ac:name="attachments" ac:schema-version="1"/>')

body = ''.join(B)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_body.storage.xml'), 'w').write(body)
print(len(body))
