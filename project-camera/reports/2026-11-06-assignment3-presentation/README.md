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
- **演讲稿（PDF）**：[英文](speaker-script/ip-camera-speaker-script-EN.pdf) · [中文](speaker-script/ip-camera-speaker-script-ZH.pdf)，内容一一对应，由 [build_pdf.py](speaker-script/build_pdf.py) 生成（需要 Chrome）。
- 逻辑：本部分只回答“摄像头怎么决定录什么”。一段有用的录像要满足两个要求——录到动作的开头（第 08 页）、只录守宫（第 09–12 页，跟踪方法见第 13–14 页）；先讲装置（第 06–07 页），最后讲结果（第 15 页）。
- 每页有一句“要点”（听众要记住的唯一一点）和一句连接下一部分的过渡句；约 940 个英文单词，5½–6 分钟。另附约 4 分钟的短版和可能被问到的问题。
- 数字都和幻灯片上一致；讲稿里没有新增幻灯片上没有的结论。早先的逐页讲稿和按制作过程讲的版本已被这份取代，可在 Git 历史中查到。

---

## Final PPT 结构调整记录（2026-11-06）

在 Figma 中做的调整（核心内容未改；改动前的整份备份是旁边的 section “Final PPT — backup 6 Nov (before re-pacing)”）：

- 新增第 04 页 Agenda：五个部分及各自页码范围。
- 新增 4 张分节页，样式与 CAM 00 相同：第 16 页 Thermal Sensor、第 19 页 Thermal Data Communication、第 27 页 Placement、第 32 页 System & Next Steps。CAM 00（第 05 页）作为 Part 01 的分节页。
- 页码统一为“NN / 36”（原来混用 “/ 14”“/ 10”“/ 07”）。
- 第 05–36 页右上角加了进度条（01 IP CAMERA … 05 SYSTEM），当前部分为绿色。
- 物理集成页左上角标签由 “06 / PHYSICAL INTEGRATION · 0X” 统一为 “SD5531 / TEAM 02 / PHYSICAL INTEGRATION”。
- IP Camera 部分改了 6 个标题：05 Camera Module → IP Camera Module；07 Information Flow → Two Streams, One Clip per Event（副标题相应改写）；08 Motion → Recording → Keep the Seconds Before Motion；13 / 14 Where Is the Gecko → Gecko Tracking；15 Results & Limits → Results, Limits & Next Steps。CAM 00 的目录项同步更新。
- 修复第 15 页 NEXT 栏文字重叠（“…then a 24 h run” 折行后压住下一条）。

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
