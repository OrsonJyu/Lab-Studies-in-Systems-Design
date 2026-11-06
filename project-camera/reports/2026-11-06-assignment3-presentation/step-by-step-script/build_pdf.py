"""Build the step-by-step IP camera speaker script (English and Chinese) as HTML and PDF.

Usage:  python3 build_pdf.py
Needs Google Chrome (headless print). Outputs next to this file:
  ip-camera-step-by-step-script-EN.html / .pdf
  ip-camera-step-by-step-script-ZH.html / .pdf
Facts come from project-camera/experiments/2026-10-30-* and 2026-11-05-*.
"""
import html
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

EN = {
    "lang": "en",
    "file": "ip-camera-step-by-step-script-EN",
    "title": "IP Camera Module — How We Built It, Step by Step",
    "sub": "Speaker script · Final presentation Part 01 · slides 05–15",
    "meta": "ZHU Kecheng · SD5531 Team 02 · 6 November 2026",
    "note": [
        "About 6½ minutes at a normal pace (≈1,050 words). The story follows the order in which we actually worked: almost every design choice came from a test that went wrong.",
        "Text in [brackets] is a cue (a slide or a gesture); do not read it aloud.",
        "One change of order: we built the tracker (slides 13–14) just before the gecko trigger (slides 11–12). The script keeps the deck order and says so in one sentence.",
        "Every test used a green toy lizard, not a real gecko.",
    ],
    "tl_head": ["When", "Step", "What we learned"],
    "timeline": [
        ["30 Oct", "Wiring; first 60 s recordings at home and at school", "Camera, PoE and ROCK 4C+ work together; 1,200 frames decoded, copy checked with SHA-256"],
        ["5 Nov 02:51", "Latency test with a clock on the Mac screen", "0.23 s camera → ROCK; starting after a trigger loses ≥ 0.4 s"],
        ["03:07", "RAM ring buffer + manual trigger", "Pre-roll works; a timing bug was found and fixed"],
        ["03:24", "Frame-difference detection, hand at home", "4 events, each with 3.7–4.65 s before the hand"],
        ["12:23–14:56", "First long run at school", "86 recordings in 2.5 h, none of a gecko"],
        ["15:44", "Detection area + scene rule + 0.5 s persistence", "0 triggers from outside; a hand inside still records"],
        ["16:10", "Threshold 25 → 15", "The moving toy lizard is now caught"],
        ["16:22 / 16:47", "Tracker: brightness only, then colour", "Box on the tail only → box on the whole lizard"],
        ["17:47 / 18:04 / 18:45", "Gecko trigger, three rounds", "3 → 2 → 0 hand-only clips"],
    ],
    "slide": "Slide",
    "sections": [
        ("05", "IP Camera Module", "≈20 s",
         ["I'm Kecheng, and I built the video part. Instead of only listing what the system does, I'll tell you how we got there — in the order we did it, because almost every design choice came from a test that went wrong."]),
        ("06", "Step 1 · Get a picture", "≈35 s",
         ["Step one, on the 30th of October, was simply to get a picture. We connected the camera to a PoE injector, which sends 48 volts and video over one network cable, and joined the injector, the ROCK 4C+ and the MacBook on a gigabit switch. The ROCK recorded 60 seconds from the camera — 1,200 frames at 2560 by 1440. We decoded every frame and checked the copy on the Mac with SHA-256.",
          "One detail on this slide came back to us later. [Point to the right USB-C] The ROCK is powered by the Mac's USB-C port. It stopped suddenly twice at school, and this power path is our first suspect — not yet confirmed."]),
        ("07", "Step 2 · Measure before designing", "≈40 s",
         ["Step two, on the 5th of November, was to measure before designing. The camera sends two streams: a full-resolution main stream for recording, and a small substream that is cheap to analyse.",
          "To measure delay, we pointed the camera at a millisecond clock on the Mac screen. [Point to the clock photos] A frame reaches the ROCK 0.23 seconds after it is filmed. Then we tried the obvious design: start FFmpeg only when something moves. Six cold starts showed that the first frame is always about 0.4 seconds late, and FFmpeg needs about 2 seconds before it writes anything. So \"start after motion\" always loses the beginning — the very moment a student wants to see."]),
        ("08", "Step 3 · Record first, decide later", "≈40 s",
         ["That gave us step three: record first, decide later. FFmpeg never stops. It copies the main stream, without re-encoding, into 2-second segments in a 60-second ring in RAM. When an event ends, we join the segments from 4 seconds before the first motion to 5 seconds after the last one.",
          "We tested it with manual triggers against the clock, and the first run found a bug: segments were timed when we polled them, so the timing drifted and the ends of clips were cut. We switched to the files' write times, added a test, and the ends were right. [Point to the clip] In this real clip the lizard is pulled at 5.1 seconds, and you can still see it before it moved. So far 97 clips have been checked and moved to the Mac."]),
        ("09", "Step 4 · First detector, first surprise", "≈35 s",
         ["Step four was the first detector. A second FFmpeg process shrinks the substream to 160 by 90 and compares each frame with the one before. At home, with a hand, it worked: four events, each with 3.7 to 4.65 seconds before the hand appeared.",
          "Then we ran it at school for two and a half hours. It saved 86 recordings — and there was no gecko in any of them. People walking, hands, lights and auto-exposure all counted as motion."]),
        ("10", "Step 5 · Tell it where to look", "≈35 s",
         ["Step five was to tell it where to look. We draw the enclosure on the web page, and every change outside it is ignored. If 30 percent or more of the whole picture changes at once, we treat it as a scene change, not motion. And motion has to last half a second.",
          "The test: for about two minutes people moved in the background and nothing was recorded, and a 31.4 percent whole-picture change was ignored. [Point to the third frame] But a hand inside the box still recorded. We also found the opposite problem — the toy lizard was often missed — so we lowered the threshold from 25 to 15."]),
        ("11", "Step 6 · Trigger on the gecko itself", "≈35 s",
         ["That led to the main idea, step six: trigger on the gecko itself, not on any change. For this we needed a tracker — we built it just before this step, and I'll show how it works in two slides.",
          "Now the area rules only write to the log. A clip starts only when the locked gecko really moves: the whole box must shift at least 2 pixels within a second, with both edges moving the same way. A shadow that only stretches one edge does not count."]),
        ("12", "Step 6 · Three rounds in the lab", "≈40 s",
         ["We tested this in three rounds, and every failure became a rule. Round one, at 17:47: three clips with only a hand. The hand made the lizard's pixels flicker, so we required the centre to really move, for half a second.",
          "Round two, at 18:04: two hand-only clips. The hand's shadow joined the lizard and pulled the box, so we added the whole-box shift, an overlap check and a size limit. Round three, at 18:45: a hand stayed in the area for eight seconds, the old area rule fired on 87 frames, nothing was recorded — and all three real lizard clips were kept."]),
        ("13", "How the tracker finds the gecko", "≈30 s",
         ["Here is the tracker we relied on. It learns a background from still frames, marks the pixels that differ from it, groups them into blobs, and locks on the one that moves.",
          "In our first run the box covered only the tail. The reason was brightness: the green lizard is almost the same grey as the desk — 157 against 156 to 186. In the colour channels they are far apart, so we added colour. It runs in pure Python at about 8 milliseconds per frame, down from 63 before optimising."]),
        ("14", "Tracker results", "≈25 s",
         ["With colour, the box covers the whole lizard in 5 of 6 sampled frames, and the lizard stayed still for 55 seconds without a false \"lost\" — the first version had called it lost after about 100 seconds of rest. One limit: when the lizard is pulled away fast, the box can stay on the empty spot for about 2 seconds."]),
        ("15", "Where we are now", "≈35 s",
         ["So, step by step, we went from 86 recordings with no gecko to zero hand-only clips, and every clip keeps 4 to 6 seconds before the first motion.",
          "What we have not done yet: a real gecko — every test used a toy lizard — night recording with the camera's infrared, and runs longer than a few hours. Next, we test in the real enclosure, run a night test, give the ROCK its own power supply for a 24-hour run, and link clips to thermal events — which brings us to the thermal sensor. [Hand over to the next speaker]"]),
    ],
    "qa_title": "If someone asks",
    "qa": [
        ["Why not an ESP32-C3 for video?", "It has no Ethernet, its memory cannot hold one 2560×1440 frame, and it cannot decode H.264. So the recorder runs on the ROCK 4C+."],
        ["Does it work with a real gecko?", "Not tested yet. Every test used a toy lizard; the real enclosure is our first next step."],
        ["Are the images on slides 08, 10, 12 and 14 live?", "No. They are replays: recorded clips fed back through the same detector and tracker, with boxes drawn on each frame."],
    ],
    "foot": "Facts from project-camera/experiments (30 Oct and 5 Nov 2026). Numbers match the Figma “Final PPT” slides 05–15.",
}

ZH = {
    "lang": "zh-Hans",
    "file": "ip-camera-step-by-step-script-ZH",
    "title": "IP 摄像头模块 —— 我们是怎样一步步做出来的",
    "sub": "演讲稿 · 期末展示第一部分 · 第 05–15 页",
    "meta": "ZHU Kecheng · SD5531 第 02 组 · 2026 年 11 月 6 日",
    "note": [
        "约 6½ 分钟，内容与英文稿一一对应。按我们实际做的顺序来讲：几乎每个设计决定都来自一次失败的测试。",
        "方括号 [ ] 里是提示（翻页或动作），不用念出来。",
        "顺序上有一处不同：跟踪程序（第 13–14 页）其实是在“守宫移动才录”（第 11–12 页）之前做的。讲稿保持幻灯片顺序，在第 11 页用一句话说明。",
        "所有测试用的都是绿色玩具蜥蜴，不是真守宫。",
    ],
    "tl_head": ["时间", "这一步做了什么", "学到了什么"],
    "timeline": [
        ["10 月 30 日", "接线；在家和学校各录第一段 60 秒", "摄像头、PoE 和 ROCK 4C+ 能一起工作；1,200 帧全部解码，拷贝用 SHA-256 核对"],
        ["11 月 5 日 02:51", "对着 Mac 屏幕上的时钟测延迟", "拍摄到 ROCK 0.23 秒；触发后才开录会丢 ≥ 0.4 秒"],
        ["03:07", "内存环形缓冲 + 手动触发", "预录有效；发现并修复了一个计时错误"],
        ["03:24", "帧差运动检测，在家用手测试", "4 个事件，手出现前都有 3.7–4.65 秒"],
        ["12:23–14:56", "在学校第一次长时间运行", "2.5 小时 86 段录像，没有一段是守宫"],
        ["15:44", "检测区域 + 整体变化规则 + 持续 0.5 秒", "区域外 0 次误触发；区域内的手仍会触发"],
        ["16:10", "阈值 25 → 15", "移动的玩具蜥蜴能录进去了"],
        ["16:22 / 16:47", "跟踪：先只用亮度，再加颜色", "只框住尾巴 → 框住整只蜥蜴"],
        ["17:47 / 18:04 / 18:45", "守宫移动才录，三轮测试", "只有手的片段 3 → 2 → 0"],
    ],
    "slide": "第",
    "slide_suffix": "页",
    "sections": [
        ("05", "IP 摄像头模块", "约 20 秒",
         ["我是 Kecheng，负责视频部分。我不只是列出系统能做什么，而是按我们实际做的顺序，讲讲我们是怎么一步步做到的——因为几乎每个设计决定，都来自一次出了问题的测试。"]),
        ("06", "第一步 · 先拿到画面", "约 35 秒",
         ["第一步是 10 月 30 日，目标很简单：先拿到画面。摄像头接到 PoE 供电器上，一根网线同时送 48 伏电和视频；供电器、ROCK 4C+ 和 MacBook 都接在一台千兆交换机上。ROCK 从摄像头录了 60 秒，2560×1440，共 1,200 帧。我们把每一帧都完整解码，传到 Mac 后再用 SHA-256 核对。",
          "这页有一个细节后来又碰到了。[指向右侧 USB-C] ROCK 是靠 Mac 的 USB-C 口供电的。它在学校两次突然停机，这条供电线路是我们的第一怀疑对象，但还没有证实。"]),
        ("07", "第二步 · 先测量，再设计", "约 40 秒",
         ["第二步是 11 月 5 日：先测量，再设计。摄像头同时发两路码流：一路全分辨率的主码流用来录像，一路小的子码流，分析起来很省资源。",
          "测延迟时，我们让摄像头对着 Mac 屏幕上的毫秒时钟。[指向时钟照片] 画面被拍到之后 0.23 秒到达 ROCK。然后我们试了最直接的设计：有动静时才启动 FFmpeg。冷启动六次的结果是：第一帧总是晚约 0.4 秒，而且 FFmpeg 要大约 2 秒才开始写文件。所以“有动作才开录”一定会丢掉开头——而开头恰恰是学生最想看的那一刻。"]),
        ("08", "第三步 · 先录下来，再决定留哪段", "约 40 秒",
         ["于是有了第三步：先录下来，再决定留哪段。FFmpeg 一直不停，把主码流原样复制、不重新编码，切成 2 秒一段，放进内存里 60 秒的环形缓冲。事件结束时，把“第一次动作前 4 秒”到“最后一次动作后 5 秒”的分段拼起来。",
          "我们对着时钟用手动触发来测，第一次就发现了一个错误：分段的时间是按“程序轮询看到它的时刻”算的，时间越来越偏，片段结尾被截短了。改成用文件的写入时间，加了一个测试，结尾就对了。[指向片段] 这段实拍里，蜥蜴在第 5.1 秒被拉动，片段里还能看到它被拉动之前的样子。目前已经有 97 个片段核对后转存到 Mac。"]),
        ("09", "第四步 · 第一个检测器，第一个意外", "约 35 秒",
         ["第四步是第一个检测器：第二个 FFmpeg 进程把子码流缩小到 160×90，每一帧和上一帧比较。在家用手测试是成功的：4 个事件，每个在手出现之前都留了 3.7 到 4.65 秒。",
          "然后我们在学校连续跑了两个半小时，存下了 86 段录像——没有一段里有守宫。有人走动、手、灯光、摄像头自动曝光，全都被当成了运动。"]),
        ("10", "第五步 · 告诉它该看哪里", "约 35 秒",
         ["第五步是告诉它该看哪里。我们在网页上画出饲养箱的范围，范围外的变化一律不算。如果整幅画面有 30% 以上同时变化，就当作环境变化，不算运动。另外，运动要持续半秒才算。",
          "测试结果：大约两分钟里，背景一直有人走动，一段都没录；一次 31.4% 的整幅画面变化也被忽略了。[指向第三张图] 但是手伸进盒子里，还是会录。我们还发现了相反的问题——玩具蜥蜴动了经常录不到——所以把阈值从 25 降到了 15。"]),
        ("11", "第六步 · 只在守宫本身移动时才录", "约 35 秒",
         ["这引出了最关键的第六步：不再是“有变化就录”，而是“守宫本身动了才录”。这需要一个跟踪程序——它是在这一步之前做好的，两页之后我再讲它怎么工作。",
          "现在区域规则只写进日志。只有被锁定的守宫真的移动，才开始录：整个框在一秒内至少平移 2 个像素，而且两侧边要朝同一个方向移动。影子只会让一侧边变长，所以不算。"]),
        ("12", "第六步 · 实验室三轮测试", "约 40 秒",
         ["我们分三轮测试，每一次失败都变成了一条新规则。第一轮，17:47：录到 3 段只有手的片段。手让蜥蜴身上的像素闪动，所以我们要求中心真正移动，并且持续半秒。",
          "第二轮，18:04：还有 2 段只有手的片段。手的影子和蜥蜴连成一块，把框拉走了，所以我们加了“整个框平移”、重叠检查和大小限制。第三轮，18:45：手在区域里停了 8 秒，旧的区域规则触发了 87 帧，但一段都没有录——而三段真正的蜥蜴片段全部保留了。"]),
        ("13", "跟踪程序怎样找到守宫", "约 30 秒",
         ["这是我们依赖的跟踪程序。它先用静止的画面学出背景，标出和背景不同的像素，把它们连成块，然后锁定那个在动的块。",
          "第一次实机运行时，框只框住了尾巴。原因在亮度：绿色蜥蜴和桌面几乎是同一个灰度——157 对 156 到 186。但在颜色通道上两者差得很远，所以我们加入了颜色。整个程序是纯 Python，每帧约 8 毫秒，优化前是 63 毫秒。"]),
        ("14", "跟踪结果", "约 25 秒",
         ["加入颜色后，抽查 6 帧里有 5 帧框住了整只蜥蜴；蜥蜴静止 55 秒，没有被误判为“丢失”——第一版在静止约 100 秒后就判丢失了。一个局限：蜥蜴被快速拿走时，框可能在原地停留大约 2 秒。"]),
        ("15", "现在做到哪一步", "约 35 秒",
         ["所以一步一步下来，我们从“86 段录像里没有一段是守宫”，做到了“0 段只有手的片段”，而且每段录像都保留了第一次动作前 4 到 6 秒。",
          "还没做的：真守宫——所有测试都用的是玩具蜥蜴；用摄像头红外模式的夜间录像；以及超过几个小时的长时间运行。下一步：在真实饲养箱里测试，做夜间测试，给 ROCK 配独立电源后跑 24 小时，并把视频片段和热成像事件关联起来——这就引出下一部分：热成像传感器。[交给下一位同学]"]),
    ],
    "qa_title": "可能被问到的问题",
    "qa": [
        ["为什么视频不用 ESP32-C3？", "它没有以太网，内存放不下一帧 2560×1440 的画面，也不能解码 H.264，所以录像放在 ROCK 4C+ 上。"],
        ["真守宫能用吗？", "还没测。所有测试都用玩具蜥蜴，进真实饲养箱测试是下一步的第一项。"],
        ["第 08、10、12、14 页的画面是实时的吗？", "不是。是回放：把录下的片段重新送进同一套检测和跟踪程序，逐帧画框。"],
    ],
    "foot": "事实依据：project-camera/experiments（2026 年 10 月 30 日与 11 月 5 日）。数字与 Figma “Final PPT” 第 05–15 页一致。",
}

CSS = """
@page { size: A4; margin: 16mm 17mm 16mm 17mm; }
* { box-sizing: border-box; }
body { font-family: %(font)s; color: #16202a; font-size: 10.5pt; line-height: 1.5; margin: 0; }
h1 { font-size: 20pt; line-height: 1.2; margin: 0 0 4pt; letter-spacing: -0.01em; }
.sub { font-size: 11pt; color: #2b6f78; font-weight: 600; margin: 0 0 2pt; }
.meta { font-size: 9.5pt; color: #5b6770; margin: 0 0 12pt; }
.note { background: #f1f6f6; border-left: 3pt solid #3aa7b0; padding: 7pt 10pt; margin: 0 0 12pt; }
.note p { margin: 2pt 0; font-size: 9.5pt; }
h2 { font-size: 11.5pt; margin: 14pt 0 6pt; color: #16202a; }
table { border-collapse: collapse; width: 100%%; font-size: 9pt; }
th { text-align: left; background: #16202a; color: #fff; padding: 4pt 6pt; font-weight: 600; }
td { padding: 4pt 6pt; border-bottom: 0.6pt solid #d5dde0; vertical-align: top; }
td:first-child { white-space: nowrap; color: #2b6f78; font-weight: 600; }
.sec { break-inside: avoid; margin: 0 0 11pt; padding-top: 2pt; }
.sec-head { display: flex; align-items: baseline; gap: 8pt; border-bottom: 0.8pt solid #c9d3d6; padding-bottom: 3pt; margin-bottom: 5pt; }
.pill { background: #c7f36b; color: #16202a; font-weight: 700; font-size: 8.5pt; padding: 1pt 6pt; border-radius: 8pt; white-space: nowrap; }
.sec-title { font-weight: 700; font-size: 12pt; flex: 1; }
.time { color: #5b6770; font-size: 9pt; white-space: nowrap; }
.say p { margin: 0 0 5pt; font-size: %(say)s; line-height: %(lh)s; }
.cue { color: #2b6f78; font-style: %(cue_style)s; font-weight: 600; }
.qa td:first-child { white-space: normal; width: 38%%; color: #16202a; }
.foot { margin-top: 12pt; font-size: 8.5pt; color: #6b767e; border-top: 0.6pt solid #d5dde0; padding-top: 5pt; }
"""


def para(text):
    t = html.escape(text, quote=False)
    return re.sub(r"\[([^\]]+)\]", r'<span class="cue">[\1]</span>', t)


def build(d):
    zh = d["lang"].startswith("zh")
    font = ('"PingFang SC", "Hiragino Sans GB", "Heiti SC", sans-serif' if zh
            else '"Helvetica Neue", Helvetica, Arial, sans-serif')
    css = CSS % {"font": font, "say": "11.5pt" if zh else "11pt",
                 "lh": "1.7" if zh else "1.55", "cue_style": "normal" if zh else "italic"}
    out = [f'<!doctype html><html lang="{d["lang"]}"><head><meta charset="utf-8">',
           f'<title>{html.escape(d["title"])}</title><style>{css}</style></head><body>',
           f'<h1>{html.escape(d["title"])}</h1><p class="sub">{html.escape(d["sub"])}</p>',
           f'<p class="meta">{html.escape(d["meta"])}</p><div class="note">']
    out += [f"<p>{para(n)}</p>" for n in d["note"]]
    out.append("</div>")
    out.append(f'<h2>{"时间线" if zh else "Timeline"}</h2><table><tr>')
    out += [f"<th>{html.escape(h)}</th>" for h in d["tl_head"]]
    out.append("</tr>")
    for row in d["timeline"]:
        out.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in row) + "</tr>")
    brk = "" if zh else ' style="break-before: page; margin-top: 0"'
    out.append(f'</table><h2{brk}>{"讲稿" if zh else "Script"}</h2>')
    for num, title, secs, paras in d["sections"]:
        label = f'{d["slide"]} {num} {d.get("slide_suffix", "")}'.strip()
        out.append(f'<div class="sec"><div class="sec-head"><span class="pill">{label}</span>'
                   f'<span class="sec-title">{html.escape(title)}</span><span class="time">{secs}</span></div>'
                   '<div class="say">' + "".join(f"<p>{para(p)}</p>" for p in paras) + "</div></div>")
    out.append(f'<div class="sec"><h2>{html.escape(d["qa_title"])}</h2><table class="qa">')
    for q, a in d["qa"]:
        out.append(f"<tr><td>{html.escape(q)}</td><td>{html.escape(a)}</td></tr>")
    out.append(f'</table></div><p class="foot">{html.escape(d["foot"])}</p></body></html>')
    page = HERE / f'{d["file"]}.html'
    page.write_text("".join(out), encoding="utf-8")
    pdf = HERE / f'{d["file"]}.pdf'
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", page.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return pdf


if __name__ == "__main__":
    for d in (EN, ZH):
        words = sum(len(p.split()) for s in d["sections"] for p in s[3])
        print(build(d), "words" if d is EN else "", words if d is EN else "")
