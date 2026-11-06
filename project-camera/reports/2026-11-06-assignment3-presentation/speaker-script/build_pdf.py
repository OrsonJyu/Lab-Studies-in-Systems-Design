"""Build the IP camera presentation speaker script (English and Chinese) as HTML and PDF.

Usage:  python3 build_pdf.py
Needs Google Chrome (headless print). Outputs next to this file:
  ip-camera-speaker-script-EN.html / .pdf
  ip-camera-speaker-script-ZH.html / .pdf
Facts come from project-camera/experiments/2026-10-30-* and 2026-11-05-*;
numbers match the Figma "Final PPT" slides 05-15.
"""
import html
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

EN = {
    "lang": "en",
    "file": "ip-camera-speaker-script-EN",
    "title": "IP Camera Module — Speaker Script",
    "sub": "Final presentation · Part 01 · slides 05–15 · about 5½–6 minutes",
    "meta": "ZHU Kecheng · SD5531 Team 02 · 6 November 2026",
    "logic_title": "The logic in one sentence",
    "logic": "Everything in this part answers one question — how does the camera decide what to record? A useful clip must meet two requirements: (1) it includes the start of the movement, and (2) it is about the gecko, not people or lights. The setup comes first, then one section for each requirement, then results.",
    "map_head": ["Slides", "Section", "Key message"],
    "map": [
        ["05", "The question", "How does the camera decide what to record?"],
        ["06–07", "Setup", "PoE camera → ROCK 4C+ recorder; main stream recorded, substream analysed"],
        ["08", "Requirement 1 · the start", "Never stop recording: keep 4 s before and 5 s after the motion"],
        ["09–12", "Requirement 2 · only the gecko", "Three stages: any change → detection area → the gecko itself"],
        ["13–14", "How we find the gecko", "Colour, not brightness, separates the lizard from the desk"],
        ["15", "Results & next", "Both requirements met in the lab; a real gecko is next"],
    ],
    "nums_title": "Three numbers to remember",
    "nums": [["4–6 s", "kept before the first motion"], ["86 → 0", "unwanted clips: stage 1 at school → hand-only clips in round 3"], ["0.23 s", "delay from camera to ROCK"]],
    "how": "How to read this script: the green line under each title is the one point the audience must remember from that slide. Text in [brackets] is a cue, not to be read aloud. Arrows (→) mark the sentence that links to the next section.",
    "key": "Key point",
    "slide": "Slide",
    "sections": [
        ("05", "IP Camera Module", "≈20 s",
         "One question: how does the camera decide what to record?",
         ["I'm Kecheng, and I'll present the IP camera module. Everything in this part answers one question: how does the camera decide what to record?",
          "A useful clip has to meet two requirements. First, it must include the start of the movement. Second, it must be about the gecko — not about people or lights. I'll show the setup, then how we meet each requirement, and finish with results and limits."]),
        ("06", "Hardware Connection & Power", "≈30 s",
         "One cable powers the camera; the ROCK 4C+ is the recorder.",
         ["This is our real setup. The camera gets 48-volt power and sends video over one network cable from the PoE injector. The injector, the ROCK 4C+ and the MacBook meet at a gigabit switch. The ROCK is the recorder; the Mac keeps the finished clips.",
          "One weak point: [point to the right USB-C] the ROCK has no adapter of its own — the Mac's USB-C port powers it. The ROCK stopped suddenly twice, and we suspect this power path, but it is not confirmed."]),
        ("07", "Two Streams, One Clip per Event", "≈35 s",
         "The main stream is recorded; the small substream is analysed.",
         ["The camera sends two streams, and we give them different jobs. The full 2560-by-1440 main stream is only copied, never re-encoded, so recording costs almost nothing. The small substream is shrunk to 160 by 90 and analysed to decide when an event starts and ends. Then the clip is cut, checked with SHA-256 and moved to the Mac.",
          "[Point to the latency test] We measured the delay by filming a clock on the Mac screen: 0.23 seconds from camera to ROCK. Detection and tracking use about 13 percent of the ROCK's CPU, so there is plenty of headroom.",
          "→ With this setup, the first requirement: the start of the movement."]),
        ("08", "Keep the Seconds Before Motion", "≈40 s",
         "Requirement 1: never stop recording — keep 4 s before and 5 s after the motion.",
         ["If we start recording only after motion is detected, the start is always lost: detection takes up to 0.65 seconds, connecting takes 0.4, and FFmpeg needs about 2 seconds before it writes anything.",
          "So our recorder never stops. It writes 2-second segments into a 60-second ring in RAM. When an event ends, we join the segments from 4 seconds before the first motion to 5 seconds after the last one, without re-encoding. [Point to the clip] In this real clip the lizard is pulled at 5.1 seconds, and you can still see it before it moved. 97 clips have been saved and checked this way.",
          "→ That solves the start. The second requirement is harder: record only the gecko."]),
        ("09", "Stage 1 · Any Change", "≈25 s",
         "Counting every changed pixel records far too much: 86 clips in 2.5 h.",
         ["We reached it in three stages. Stage one counts every pixel that changes between frames. It is fast, but it cannot tell what moved. At school it made 86 recordings in two and a half hours, with no gecko in the scene — people, hands, lights and auto-exposure all counted as motion."]),
        ("10", "Stage 2 · Detection Area", "≈30 s",
         "Watch only the enclosure, and ignore whole-picture changes.",
         ["Stage two tells it where to look. We draw the enclosure on the web page, and changes outside it are ignored. If 30 percent or more of the picture changes at once, it is a lighting or exposure change, not motion. And motion must last half a second.",
          "Result: zero triggers from outside the area, and a 31.4 percent whole-picture change was ignored. But one problem is left: [point to the third frame] a hand inside the area still records."]),
        ("11", "Stage 3 · Lock on the Gecko", "≈30 s",
         "The trigger is the gecko itself, not any change.",
         ["So in stage three, the trigger is the gecko itself. A clip starts only when the tracked gecko really moves: its whole box must shift at least 2 pixels within a second, with both edges moving the same way. A shadow only stretches one edge, so it does not count.",
          "The old area rule still runs, but only writes to the log, so we can compare the two rules on the same video."]),
        ("12", "Stage 3 · On-site Tests", "≈35 s",
         "Three lab rounds; hand-only clips went 3 → 2 → 0.",
         ["We tested stage three in the lab in three rounds, and each failure became a rule. Round one: three clips with only a hand — pixel flicker looked like movement, so we required real travel for half a second. Round two: two — the hand's shadow joined the gecko and pulled the box, so we added the whole-box shift, an overlap check and a size limit.",
          "Round three: zero. A hand stayed in the area for 8 seconds, the old rule fired on 87 frames, nothing was recorded, and all three gecko clips were kept.",
          "→ All of this depends on knowing where the gecko is. Here is how we find it."]),
        ("13", "Gecko Tracking · Method", "≈30 s",
         "Colour, not brightness, separates the lizard from the desk.",
         ["The tracker learns a background from still frames, finds the pixels that differ from it, groups them into blobs, and locks on the one that moves.",
          "The key was colour. In brightness, our green lizard is almost the same grey as the desk — 157 against 156 to 186 — so at first the box covered only its tail. In the colour channels they are far apart. The tracker runs in pure Python at about 8 milliseconds per frame."]),
        ("14", "Gecko Tracking · Results", "≈20 s",
         "The box stays on the lizard while it moves and while it rests.",
         ["With colour, the box covers the whole lizard in 5 of 6 sampled frames, and it stayed on the lizard through 55 seconds of rest without a false \"lost\". The limit: if the lizard is pulled away fast, the box can stay on the empty spot for about 2 seconds."]),
        ("15", "Results, Limits & Next Steps", "≈35 s",
         "Both requirements are met in the lab; a real gecko is the next test.",
         ["To sum up: both requirements are met in the lab. Clips keep 4 to 6 seconds before the first motion, and changes outside the area, lighting changes and a hand in the area no longer start a recording.",
          "What we have not tested yet: a real gecko — every test used a toy lizard — night recording with the camera's infrared, and runs longer than a few hours. Next, we test in the real enclosure, run a night test, give the ROCK its own power supply for a 24-hour run, and link clips to thermal events.",
          "→ Which brings us to the thermal sensor. [Hand over to the next speaker]"]),
    ],
    "short_title": "If time is short (about 4 minutes)",
    "short": [
        "Slide 07: say only the two jobs of the two streams and 0.23 s; skip the CPU figure.",
        "Slides 09 and 10: one sentence each — “86 recordings in 2.5 h” and “outside the area is ignored, but a hand inside still records”.",
        "Slide 12: say only “3 → 2 → 0 hand-only clips”.",
        "Slide 13: say only the colour point; skip the five steps.",
    ],
    "qa_title": "If someone asks",
    "qa": [
        ["Why not an ESP32-C3 for video?", "It has no Ethernet, its memory cannot hold one 2560×1440 frame, and it cannot decode H.264. So the recorder runs on the ROCK 4C+."],
        ["Does it work with a real gecko?", "Not tested yet. Every test used a toy lizard; the real enclosure is our first next step."],
        ["Are the images on slides 08, 10, 12 and 14 live?", "No. They are replays: recorded clips fed back through the same detector and tracker, with boxes drawn on each frame."],
        ["What caused the 31.4 % change?", "It is not visible in the recording; the rule treated it as a scene change and ignored it."],
    ],
    "foot": "Facts from project-camera/experiments (30 Oct and 5 Nov 2026). Numbers match the Figma “Final PPT” slides 05–15.",
}

ZH = {
    "lang": "zh-Hans",
    "file": "ip-camera-speaker-script-ZH",
    "title": "IP 摄像头模块 —— 演讲稿",
    "sub": "期末展示 · 第一部分 · 第 05–15 页 · 约 5½–6 分钟",
    "meta": "ZHU Kecheng · SD5531 第 02 组 · 2026 年 11 月 6 日",
    "logic_title": "一句话讲清逻辑",
    "logic": "这一部分只回答一个问题——摄像头怎么决定录什么？一段有用的录像要满足两个要求：(1) 录到动作的开头；(2) 录的是守宫，而不是人或灯光。先讲装置，再分别讲怎么满足这两个要求，最后讲结果。",
    "map_head": ["页", "部分", "要点"],
    "map": [
        ["05", "提出问题", "摄像头怎么决定录什么？"],
        ["06–07", "装置", "PoE 摄像头 → ROCK 4C+ 录像；主码流录像，子码流分析"],
        ["08", "要求一 · 录到开头", "一直在录：保留动作前 4 秒、动作后 5 秒"],
        ["09–12", "要求二 · 只录守宫", "三个阶段：任何变化 → 检测区域 → 守宫本身"],
        ["13–14", "怎样找到守宫", "区分蜥蜴和桌面靠的是颜色，不是亮度"],
        ["15", "结果与下一步", "两个要求在实验室都达到了；下一步测真守宫"],
    ],
    "nums_title": "要记住的三个数字",
    "nums": [["4–6 秒", "第一次动作前保留的画面"], ["86 → 0", "不该录的片段：第一阶段在学校 86 段 → 第三轮只有手的片段 0 段"], ["0.23 秒", "摄像头到 ROCK 的延迟"]],
    "how": "怎么用这份讲稿：每页标题下的绿色一行，是这一页要让听众记住的唯一要点。方括号 [ ] 里是提示，不用念出来。箭头（→）标出连接下一部分的过渡句。",
    "key": "要点",
    "slide": "第",
    "slide_suffix": "页",
    "sections": [
        ("05", "IP 摄像头模块", "约 20 秒",
         "一个问题：摄像头怎么决定录什么？",
         ["我是 Kecheng，我来介绍 IP 摄像头模块。这一部分只回答一个问题：摄像头怎么决定录什么？",
          "一段有用的录像要满足两个要求。第一，要录到动作的开头。第二，录的必须是守宫，而不是人或灯光。我先介绍装置，然后讲怎么满足这两个要求，最后讲结果和局限。"]),
        ("06", "硬件连接与供电", "约 30 秒",
         "一根网线给摄像头供电；ROCK 4C+ 负责录像。",
         ["这是我们真实的接线。摄像头通过一根网线从 PoE 供电器取得 48 伏电，同时传视频。供电器、ROCK 4C+ 和 MacBook 都接在一台千兆交换机上。ROCK 负责录像，Mac 保存录好的片段。",
          "有一个薄弱点：[指向右侧 USB-C] ROCK 没有自己的电源适配器，是靠 Mac 的 USB-C 口供电的。ROCK 两次突然停机，我们怀疑和这条供电线路有关，但还没有证实。"]),
        ("07", "两路码流，一个事件一段录像", "约 35 秒",
         "主码流用来录像，小的子码流用来分析。",
         ["摄像头发两路码流，我们让它们各做一件事。2560×1440 的主码流只复制、不重新编码，所以录像几乎不占资源。小的子码流缩小到 160×90 做分析，判断事件什么时候开始、什么时候结束。然后剪出片段，用 SHA-256 核对后转存到 Mac。",
          "[指向延迟测试] 我们让摄像头拍 Mac 屏幕上的时钟来测延迟：摄像头到 ROCK 是 0.23 秒。检测加跟踪只用了 ROCK 大约 13% 的 CPU，余量很充足。",
          "→ 有了这套装置，先看第一个要求：录到动作的开头。"]),
        ("08", "保留动作之前的几秒", "约 40 秒",
         "要求一：一直在录——保留动作前 4 秒、动作后 5 秒。",
         ["如果检测到动作才开始录，开头一定会丢：检测最多要 0.65 秒，连接要 0.4 秒，FFmpeg 还要大约 2 秒才开始写文件。",
          "所以我们的录像程序从不停止。它把画面切成 2 秒一段，写进内存里 60 秒的环形缓冲。事件结束时，把“第一次动作前 4 秒”到“最后一次动作后 5 秒”的分段拼起来，不重新编码。[指向片段] 这段实拍里，蜥蜴在第 5.1 秒被拉动，片段里还能看到它被拉动之前的样子。已经有 97 个片段这样保存并核对过。",
          "→ 开头的问题解决了。第二个要求更难：只录守宫。"]),
        ("09", "第一阶段 · 任何变化都算", "约 25 秒",
         "每个变化的像素都算，录得太多：2.5 小时 86 段。",
         ["我们分三个阶段做到。第一阶段：两帧之间有变化的像素都算。速度快，但分不清是什么在动。在学校，两个半小时录了 86 段，画面里根本没有守宫——人、手、灯光和自动曝光都被当成了运动。"]),
        ("10", "第二阶段 · 检测区域", "约 30 秒",
         "只看饲养箱范围，忽略整幅画面的变化。",
         ["第二阶段告诉它该看哪里。我们在网页上画出饲养箱的范围，范围外的变化一律不算。如果整幅画面 30% 以上同时变化，就是光线或曝光变化，不算运动。另外，运动要持续半秒才算。",
          "结果：区域外零次误触发，一次 31.4% 的整幅画面变化也被忽略了。但还剩一个问题：[指向第三张图] 手伸进区域里，仍然会录。"]),
        ("11", "第三阶段 · 锁定守宫", "约 30 秒",
         "触发条件是守宫本身，而不是任何变化。",
         ["所以第三阶段，触发条件变成守宫本身。只有被跟踪的守宫真的移动，才开始录：整个框在一秒内至少平移 2 个像素，而且两侧边要朝同一个方向移动。影子只会让一侧边变长，所以不算。",
          "旧的区域规则还在运行，但只写进日志，这样可以在同一段视频上比较两种规则。"]),
        ("12", "第三阶段 · 实验室测试", "约 35 秒",
         "实验室三轮测试：只有手的片段 3 → 2 → 0。",
         ["我们在实验室分三轮测试第三阶段，每一次失败都变成了一条规则。第一轮：录到 3 段只有手的片段——像素闪动被当成了移动，所以我们要求真正的位移，并持续半秒。第二轮：2 段——手的影子和守宫连成一块，把框拉走了，所以我们加了“整个框平移”、重叠检查和大小限制。",
          "第三轮：0 段。手在区域里停了 8 秒，旧规则触发了 87 帧，但一段都没录，三段守宫片段全部保留。",
          "→ 这一切的前提是知道守宫在哪里。下面讲我们怎么找到它。"]),
        ("13", "守宫跟踪 · 方法", "约 30 秒",
         "区分蜥蜴和桌面靠的是颜色，不是亮度。",
         ["跟踪程序先用静止的画面学出背景，找出和背景不同的像素，把它们连成块，然后锁定那个在动的块。",
          "关键是颜色。在亮度上，绿色蜥蜴和桌面几乎是同一个灰度——157 对 156 到 186——所以一开始框只框住了尾巴。在颜色通道上，两者差得很远。跟踪程序是纯 Python，每帧约 8 毫秒。"]),
        ("14", "守宫跟踪 · 结果", "约 20 秒",
         "蜥蜴移动和静止时，框都能跟住它。",
         ["加入颜色后，抽查 6 帧里有 5 帧框住了整只蜥蜴；蜥蜴静止 55 秒，框一直在它身上，没有误判为“丢失”。局限：蜥蜴被快速拿走时，框可能在原地停留大约 2 秒。"]),
        ("15", "结果、局限与下一步", "约 35 秒",
         "两个要求在实验室都达到了；下一步是测真守宫。",
         ["总结一下：两个要求在实验室都达到了。片段保留第一次动作前 4 到 6 秒；区域外的变化、光线变化和区域里的手，都不会再触发录像。",
          "还没测的：真守宫——所有测试都用的是玩具蜥蜴；用摄像头红外模式的夜间录像；以及超过几个小时的长时间运行。下一步：在真实饲养箱里测试，做夜间测试，给 ROCK 配独立电源后跑 24 小时，并把片段和热成像事件关联起来。",
          "→ 这就引出下一部分：热成像传感器。[交给下一位同学]"]),
    ],
    "short_title": "时间不够时（约 4 分钟）",
    "short": [
        "第 07 页：只讲两路码流各做什么和 0.23 秒，跳过 CPU 数字。",
        "第 09、10 页：各一句——“2.5 小时 86 段”和“区域外不算，但区域里的手仍会录”。",
        "第 12 页：只讲“只有手的片段 3 → 2 → 0”。",
        "第 13 页：只讲颜色这一点，跳过五个步骤。",
    ],
    "qa_title": "可能被问到的问题",
    "qa": [
        ["为什么视频不用 ESP32-C3？", "它没有以太网，内存放不下一帧 2560×1440 的画面，也不能解码 H.264，所以录像放在 ROCK 4C+ 上。"],
        ["真守宫能用吗？", "还没测。所有测试都用玩具蜥蜴，进真实饲养箱测试是下一步的第一项。"],
        ["第 08、10、12、14 页的画面是实时的吗？", "不是。是回放：把录下的片段重新送进同一套检测和跟踪程序，逐帧画框。"],
        ["31.4% 的变化是什么引起的？", "录像里看不出原因；规则把它当作环境变化忽略了。"],
    ],
    "foot": "事实依据：project-camera/experiments（2026 年 10 月 30 日与 11 月 5 日）。数字与 Figma “Final PPT” 第 05–15 页一致。",
}

CSS = """
@page { size: A4; margin: 15mm 17mm 15mm 17mm; }
* { box-sizing: border-box; }
body { font-family: %(font)s; color: #16202a; font-size: 10.5pt; line-height: 1.5; margin: 0; }
h1 { font-size: 21pt; line-height: 1.2; margin: 0 0 4pt; letter-spacing: -0.01em; }
.sub { font-size: 11pt; color: #2b6f78; font-weight: 600; margin: 0 0 2pt; }
.meta { font-size: 9.5pt; color: #5b6770; margin: 0 0 12pt; }
h2 { font-size: 11.5pt; margin: 14pt 0 6pt; }
.logic { background: #16202a; color: #f5f8f7; padding: 10pt 12pt; border-radius: 4pt; font-size: 11pt; line-height: 1.55; margin: 0 0 4pt; }
.logic b { color: #c7f36b; }
table { border-collapse: collapse; width: 100%%; font-size: 9.5pt; }
th { text-align: left; background: #e8eff0; padding: 4pt 6pt; font-weight: 700; }
td { padding: 4pt 6pt; border-bottom: 0.6pt solid #d5dde0; vertical-align: top; }
.map td:first-child { white-space: nowrap; color: #2b6f78; font-weight: 700; width: 11%%; }
.map td:nth-child(2) { font-weight: 600; width: 30%%; }
.nums { display: flex; gap: 8pt; margin: 0; }
.num { flex: 1; border: 0.8pt solid #c9d3d6; border-radius: 4pt; padding: 7pt 9pt; }
.num b { display: block; font-size: 17pt; color: #2b6f78; line-height: 1.15; }
.num span { font-size: 9pt; color: #44505a; }
.how { font-size: 9.5pt; color: #44505a; margin: 12pt 0 0; }
.sec { break-inside: avoid; margin: 0 0 12pt; }
.sec-head { display: flex; align-items: baseline; gap: 8pt; border-bottom: 0.8pt solid #c9d3d6; padding-bottom: 3pt; }
.pill { background: #16202a; color: #fff; font-weight: 700; font-size: 8.5pt; padding: 1pt 6pt; border-radius: 8pt; white-space: nowrap; }
.sec-title { font-weight: 700; font-size: 12.5pt; flex: 1; }
.time { color: #5b6770; font-size: 9pt; white-space: nowrap; }
.key { background: #eefbd3; border-left: 3pt solid #8fc23a; padding: 4pt 8pt; margin: 5pt 0 6pt; font-weight: 700; font-size: 10.5pt; }
.key small { color: #5a7d1f; font-weight: 700; font-size: 8pt; text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6pt; }
.say p { margin: 0 0 5pt; font-size: %(say)s; line-height: %(lh)s; }
.say p.bridge { color: #2b6f78; font-weight: 600; }
.cue { color: #2b6f78; font-style: %(cue_style)s; font-weight: 600; }
ul { margin: 0; padding-left: 14pt; }
li { margin: 0 0 3pt; font-size: 10pt; }
.qa td:first-child { width: 36%%; font-weight: 600; }
.foot { margin-top: 12pt; font-size: 8.5pt; color: #6b767e; border-top: 0.6pt solid #d5dde0; padding-top: 5pt; }
.break { break-before: page; margin-top: 0; }
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
    e = lambda s: html.escape(s, quote=False)
    o = [f'<!doctype html><html lang="{d["lang"]}"><head><meta charset="utf-8">',
         f'<title>{e(d["title"])}</title><style>{css}</style></head><body>',
         f'<h1>{e(d["title"])}</h1><p class="sub">{e(d["sub"])}</p><p class="meta">{e(d["meta"])}</p>',
         f'<h2 style="margin-top:0">{e(d["logic_title"])}</h2><div class="logic">{e(d["logic"])}</div>',
         '<h2>' + ("结构" if zh else "Structure") + '</h2><table class="map"><tr>']
    o += [f"<th>{e(h)}</th>" for h in d["map_head"]]
    o.append("</tr>")
    for row in d["map"]:
        o.append("<tr>" + "".join(f"<td>{e(c)}</td>" for c in row) + "</tr>")
    o.append(f'</table><h2>{e(d["nums_title"])}</h2><div class="nums">')
    o += [f'<div class="num"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in d["nums"]]
    o.append(f'</div><p class="how">{para(d["how"])}</p>')
    o.append('<h2 class="break">' + ("讲稿" if zh else "Script") + "</h2>")
    for num, title, secs, key, paras in d["sections"]:
        label = f'{d["slide"]} {num} {d.get("slide_suffix", "")}'.strip()
        body = "".join(
            f'<p class="bridge">{para(p)}</p>' if p.startswith("→") else f"<p>{para(p)}</p>" for p in paras)
        o.append(f'<div class="sec"><div class="sec-head"><span class="pill">{label}</span>'
                 f'<span class="sec-title">{e(title)}</span><span class="time">{secs}</span></div>'
                 f'<div class="key"><small>{e(d["key"])}</small>{e(key)}</div><div class="say">{body}</div></div>')
    o.append(f'<div class="sec"><h2>{e(d["short_title"])}</h2><ul>')
    o += [f"<li>{e(s)}</li>" for s in d["short"]]
    o.append(f'</ul></div><div class="sec"><h2>{e(d["qa_title"])}</h2><table class="qa">')
    o += [f"<tr><td>{e(q)}</td><td>{e(a)}</td></tr>" for q, a in d["qa"]]
    o.append(f'</table></div><p class="foot">{e(d["foot"])}</p></body></html>')
    page = HERE / f'{d["file"]}.html'
    page.write_text("".join(o), encoding="utf-8")
    pdf = HERE / f'{d["file"]}.pdf'
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", page.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return pdf


if __name__ == "__main__":
    words = sum(len(p.split()) for s in EN["sections"] for p in s[4])
    print("EN spoken words:", words, f"≈ {words / 150:.1f} min at 150 wpm")
    for d in (EN, ZH):
        print(build(d))
