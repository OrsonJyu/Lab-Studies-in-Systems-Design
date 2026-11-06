---
title: Assignment 3 final presentation — IP camera speaker script
aliases: [Final PPT 演讲稿, IP camera script, Part 01 演讲稿]
date: 2026-11-06
speaker: ZHU Kecheng
slides: Figma "Final PPT" section, slides 05–15 (Part 01 · IP Camera)
---

# Assignment 3 final presentation · Part 01 IP Camera · speaker script

- 幻灯片：[Figma · Final PPT](https://www.figma.com/design/sxi53cbglPTcFEPPy2EYiu/SD5531-Super-Gecko-Team?node-id=2045-87)，第 05–15 页（共 36 页）。
- 讲述顺序：IP Camera → Thermal Sensor → Thermal Data Communication → Placement → System & Next Steps。
- 本部分时长：约 6 分钟（约 940 个英文单词，按每分钟 150 词计；各页标注的秒数是目标值，合计约 5.7 分钟，语速稍快即可达到）。如需压缩到 3.5 分钟，见文末“短版”。
- 每页先列英文讲稿，再用一行中文写本页要点，方便记忆。方括号里是动作提示，不用念出来。
- 数字都和幻灯片上一致；讲稿里没有新增幻灯片上没有的结论。

---

## 05 · Camera Module (≈20 s)

> I'm Kecheng, and I'll start with the video part: the IP camera module. The question is simple: how does the camera decide *what* to record? I'll go through it in four steps — the hardware, how motion becomes a recording, how we make the detection precise, and how the system finds the gecko.

要点：自我介绍，本部分回答“摄像头怎么决定录什么”，分四步讲。

## 06 · Hardware Connection & Power (≈35 s)

> This is our real wiring. The camera gets video and 48-volt power over one network cable from the PoE injector. The injector, the ROCK 4C+ and the MacBook all meet at an 8-port gigabit switch. The ROCK 4C+ is our recorder. [Point to the right USB-C] It has no adapter of its own — the MacBook powers it over USB-C. That matters: the ROCK stopped suddenly twice, and this power path is our first suspect, although we have not confirmed it.

要点：PoE 一根网线同时供电和传视频；交换机连接所有设备；ROCK 由 Mac 的 USB-C 供电，两次意外停机可能与此有关（未确认）。

## 07 · Information Flow (≈35 s)

> The camera sends two streams. The full-resolution main stream, 2560 by 1440 at 20 frames per second, is only copied — never re-encoded — into a 60-second ring of 2-second segments in RAM. The small substream goes to a second FFmpeg process that shrinks it to 160 by 90 for analysis, and Python decides when an event starts and ends. Then we cut the clip out of the ring and move it to the Mac with a SHA-256 check. [Point to the latency test] We measured the delay by filming the Mac clock: the median from camera to ROCK is 0.23 seconds, and detection plus tracking uses about 13 % of the ROCK's CPU.

要点：两路码流——主码流只复制进 RAM 环形缓冲，子码流缩小后做分析；剪出片段、SHA-256 校验后传到 Mac；延迟中位数 0.23 s，CPU 约 13 %。

## 08 · Motion → Recording (≈40 s)

> Why a ring buffer? If we only start recording after we see motion, we lose the start: detection takes up to 0.65 seconds, connecting takes 0.4, and FFmpeg's first output takes about 2 seconds. That is exactly the moment a student wants to see. So FFmpeg never stops: it writes into RAM all the time. When an event closes, we join the segments from 4 seconds before the first motion to 5 seconds after the last one, without re-encoding. [Point to the clip] In this real clip the gecko is pulled at 5.1 seconds, and you can still see it before it moved. 97 clips were checked and moved to the Mac this way.

要点：先检测再开录会丢掉开头；所以一直往内存里录，事件结束时取“动作前 4 s 到最后动作后 5 s”；实拍片段保留了 5.1 s 的动作前画面，97 个片段已校验转存。

## 09 · Stage 1 · Any Change (≈25 s)

> Now: when does an event start? We made detection precise in three stages. Stage one is plain frame differencing in FFmpeg: any pixel whose brightness changes by more than 15, or whose colour changes enough, counts. It is fast, but it cannot tell *what* moved. At school it made 86 recordings in two and a half hours — people, hands, lights and auto-exposure.

要点：三阶段的第一阶段——任何像素变化都算；速度快但分不清是什么在动，学校 2.5 小时录了 86 段。

## 10 · Stage 2 · Detection Area (≈30 s)

> Stage two adds rules. We draw the enclosure area on the web page, and everything outside it is ignored. If thirty percent or more of the whole picture changes at once, that is a lighting or exposure change, not motion. And motion has to last half a second. Result: zero triggers from outside the area, and a 31.4 % whole-picture change was treated as a scene change and ignored. But one problem was left — [point to the third frame] a hand *inside* the area still records.

要点：第二阶段——只看画出的区域；整幅画面变化 ≥30 % 视为环境变化；动作需持续 0.5 s；区域外零误触发，但区域内的手仍会触发录像。

## 11 · Stage 3 · Lock on the Gecko (≈30 s)

> So in stage three, the trigger is the gecko itself. The area rules still run, but only for the log. A clip starts only when the tracked gecko really moves: its whole box must shift at least 2 pixels within a second, with opposite edges moving the same way — a shadow that only stretches one edge does not count. We also only follow a blob that overlaps the last box or looks like the gecko, and keeps a similar size.

要点：第三阶段——只有被锁定的守宫真的移动才开录：整个框在 1 秒内移动 ≥2 像素且两侧边同向；只跟随重叠或外观相似、大小相近的目标，影子拉长一侧不算。

## 12 · Stage 3 · On-site Tests (≈35 s)

> We tested this in the lab in three rounds, and each failure became a rule. Round one: three clips with only a hand — pixel flicker counted as movement, so we required real travel for half a second. Round two: two hand-only clips — the hand's shadow merged with the gecko and pulled the box, so we added the whole-box shift, the overlap check and the size band. Round three: zero. A hand stayed in the area for eight seconds, the old area rule fired on 87 frames, nothing was recorded, and all three real gecko clips were kept.

要点：实验室三轮测试，每次失败变成一条规则：3 段 → 2 段 → 0 段只有手的片段；第三轮手在区域内 8 秒，旧规则触发 87 帧，但没有录，3 段守宫片段都保留。

## 13 · Where Is the Gecko · Method (≈30 s)

> Stage three depends on knowing where the gecko is, so here is how the tracker finds it. It learns a background from still frames, marks pixels that differ from it, groups them into blobs, locks on the one that moves, and cleans up the "ghost" left behind. The key was colour. In brightness alone, our green lizard is almost the same grey as the desk — 157 against 156 to 186 — so the box covered only its tail. In the two colour channels it stands far apart. All this runs in pure Python at about 8 milliseconds per frame.

要点：跟踪方法——背景模型 → 前景 → 连通块 → 锁定跟随 → 清除残影；关键是颜色：亮度上蜥蜴和桌面几乎一样，颜色通道上差别明显；纯 Python，每帧约 8 ms。

## 14 · Where Is the Gecko · Results (≈25 s)

> On our recorded clips the box stays on the lizard while it moves and while it rests: the whole lizard was boxed in 5 of 6 sampled frames, and it stayed still for 55 seconds without a false "lost". The limit: if the lizard is pulled away fast, the box can stay on the empty spot for about two seconds.

要点：结果——6 帧抽样中 5 帧框住整只蜥蜴；静止 55 秒没有误判“丢失”；局限：被快速拿走时框会在原地停留约 2 秒。

## 15 · Results & Limits (≈35 s)

> To sum up the camera part: clips keep 4 to 6 seconds before the first motion, changes outside the area and lighting changes are ignored, and a hand in the area no longer records. What we have not tested yet: a real gecko — every test used a toy lizard — night recording with the camera's IR, and runs longer than a few hours. Next, we test in the real enclosure with the gecko, run a night test, and give the ROCK its own power supply for a 24-hour run. We also want to link clips to thermal events — which brings us to the thermal sensor. [Hand over to the next speaker]

要点：总结能做到的（动作前保留 4–6 s、忽略区域外和光线变化、手不再触发）和还没测的（真守宫、夜间红外、长时间运行）；下一步；用“和热成像事件联动”过渡到下一部分。

---

## 短版（约 3.5 分钟）

时间不够时：

1. 第 09 页（Stage 1）只说一句：“Stage one counted any changed pixel — 86 recordings in 2.5 hours at school, mostly people and lights.” 然后直接翻到第 10 页。
2. 第 11 页和第 12 页合起来讲，第 11 页只说“the trigger is the gecko itself”，规则细节留给第 12 页的三轮测试。
3. 第 13 页只讲颜色那一点（亮度相同、颜色不同），跳过五个步骤。
4. 第 14 页只念两个数字：5 / 6 和 55 s。

## 现场提示

- 第 08、10、12、14 页的画面是录像回放的截图：讲的时候指着时间轴、红框和绿框说明，不要说成实时画面。
- 有人问“为什么不用 ESP32-C3”：ESP32-C3 没有以太网，内存放不下一帧 2560×1440 的画面，也不能解码 H.264；所以目标控制器选 ROCK 4C+。
- 有人问“真守宫能用吗”：如实回答还没测，所有测试都用的是玩具蜥蜴，这是下一步的第一项。

---

## Final PPT 结构调整记录（2026-11-06）

在 Figma 中做的调整（核心内容未改；改动前的整份备份是旁边的 section “Final PPT — backup 6 Nov (before re-pacing)”）：

- 新增第 04 页 Agenda：五个部分及各自页码范围。
- 新增 4 张分节页，样式与 CAM 00 相同：第 16 页 Thermal Sensor、第 19 页 Thermal Data Communication、第 27 页 Placement、第 32 页 System & Next Steps。CAM 00（第 05 页）作为 Part 01 的分节页。
- 页码统一为“NN / 36”（原来混用 “/ 14”“/ 10”“/ 07”）。
- 第 05–36 页右上角加了进度条（01 IP CAMERA … 05 SYSTEM），当前部分为绿色。
- 物理集成页左上角标签由 “06 / PHYSICAL INTEGRATION · 0X” 统一为 “SD5531 / TEAM 02 / PHYSICAL INTEGRATION”。

## 删减建议（36 页偏多）

按 20 分钟左右的总时长估算，建议控制在 26–28 页。优先级从高到低：

| 建议 | 页 | 理由 |
| --- | --- | --- |
| 删 | 18 Thermal Circuit | 接线（VIN/GND/SDA/SCL）与第 17 页重复；原理图留在个人页面即可。 |
| 合并为 1 页 | 22 HTTP 200 · 23 Node-RED · 24 768 Values | 三页都是同一条链路的证据截图；保留一页“证据”拼图。 |
| 删或合并 | 21 What We Transmit | JSON 结构与第 24 页重叠；可并入证据页。 |
| 合并 | 09 Stage 1 + 10 Stage 2 | 第一阶段只需一句话和“86 段 / 2.5 h”这个数字。 |
| 合并 | 13 Method + 14 Results | 讲颜色和结果数字即可，代码截图可省。 |
| 合并 | 33 System Workflow + 03 System Architecture | 两页都是系统流程；保留一页即可。 |
| 合并 | 35 Revised Design & Scope + 36 Further Validation | 各部分末页已有 Next / 下一步，结尾一页总结即可。 |
| 可删 | 16 / 19 / 27 / 32 分节页 | 若删减后仍超时，可去掉分节页，只保留 Agenda 和进度条。 |

按以上建议可减少约 8–9 页。

## 需要组内确认的内容（未改动）

- 第 03、33、35 页仍写着视频只做到“60 秒测试片段 / microSD / short recording”，且第 33 页把“事件前缓冲”列为 “to validate”；摄像头部分（第 08、15 页）已经做到 RAM 环形缓冲和事件片段。建议更新这三页，避免前后矛盾。
- 第 10 页把 31.4 % 的整幅变化写成 “lights on/off”；实际原因在画面中看不出来，个人页面写的是 “cause not visible”。
- 第 17 页左下角有一句制作备注 “Use the checked module pin labels. Add the EasyEDA circuit screenshot to the study record.”，像是给自己的提示，建议删除。
