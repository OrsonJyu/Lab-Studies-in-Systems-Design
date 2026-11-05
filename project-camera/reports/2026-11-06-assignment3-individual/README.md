---
id: report-2026-11-06-assignment3-individual
type: report
workstream: ws-preroll-recording
aliases: [Assignment 3, 个人技术可行性报告, individual feasibility study, Confluence 个人页面]
---

# Assignment 3 · 个人技术可行性研究 / Individual technical feasibility study — ZHU Kecheng

课程页面（Confluence，团队空间 SD5531_2026_S1_Team02 Home 下）：
[Video Recording Module: PoE IP Camera + ROCK 4C+ Event Recorder — ZHU Kecheng](https://www.designandmake.org/pages/viewpage.action?pageId=318019639)

本文件夹保存该页面使用的全部附件，以及生成页面正文的方式，便于核对。页面内容整理自本仓库的实验记录（`project-camera/experiments/2026-10-30-*`、`2026-11-05-*`）。

- 画面中只有手和玩具蜥蜴；含人脸的早期录像没有使用。
- 测试图片中标为 replay 的，是把录下的片段重新送入同一套检测/跟踪程序后逐帧画框得到的。
- 原理图用 EasyEDA 标准版 6.5.61 绘制（`04_EasyEDA_Schematic_Source.zip` 内有打开方法）。
- 小体积的报告视频（共约 9 MB）直接存入 Git（见 `.gitattributes` 中的 reports 规则），以便页面可直接引用。

The Confluence page above is the submission; this folder keeps every attachment it uses so the page can be checked or rebuilt.

| File | Content | SHA-256 |
| --- | --- | --- |
| [01_EasyEDA_Schematic_Editor_Screenshot.jpg](attachments/01_EasyEDA_Schematic_Editor_Screenshot.jpg) | EasyEDA editor screen capture of the schematic | `255d41693507f1d1…` |
| [02_EasyEDA_Schematic.png](attachments/02_EasyEDA_Schematic.png) | EasyEDA schematic, full-resolution export | `2de807e4443141e3…` |
| [03_Hardware_Wiring_and_Power.png](attachments/03_Hardware_Wiring_and_Power.png) | Hardware wiring and power picture (slide CAM 01) | `921ae750b16f4ba9…` |
| [04_EasyEDA_Schematic_Source.zip](attachments/04_EasyEDA_Schematic_Source.zip) | EasyEDA source files (zipped; open with File > Open > EasyEDA Source) | `033720c0dfaf7e5a…` |
| [05_Source_Code_recorder_and_demo.zip](attachments/05_Source_Code_recorder_and_demo.zip) | Source code snapshot (recorder, network check, demo) from commit dfc2147 | `21d269638eef0750…` |
| [06_Information_Flow.png](attachments/06_Information_Flow.png) | Information flow (slide CAM 02) | `5e60652992ae3461…` |
| [07_Code_ring_buffer_segmenter.png](attachments/07_Code_ring_buffer_segmenter.png) | Code: SegmentRun ring buffer | `f4be271cedea5f29…` |
| [08_Code_clip_assembly.png](attachments/08_Code_clip_assembly.png) | Code: assemble() pre-roll + concat | `2af54cf3bb343866…` |
| [09_Code_motion_filter.png](attachments/09_Code_motion_filter.png) | Code: motion_filter() | `f03a7669415769bf…` |
| [10_Code_area_rules.png](attachments/10_Code_area_rules.png) | Code: FrameAnalyzer.analyze() + MotionRules.frame() | `e60a7b6ec2e78e7f…` |
| [11_Code_gecko_trigger.png](attachments/11_Code_gecko_trigger.png) | Code: MotionDetector._read() gecko trigger | `2ae8b9f3d78eacbc…` |
| [12_Code_tracker_foreground.png](attachments/12_Code_tracker_foreground.png) | Code: Tracker._foreground() | `da5a098aa752137a…` |
| [13_Code_tracker_follow_shift.png](attachments/13_Code_tracker_follow_shift.png) | Code: Tracker._follow() + _shift() | `38190e1909ee1d60…` |
| [14_Test_first_recording_frame.jpg](attachments/14_Test_first_recording_frame.jpg) | Test: frame from the first 60 s recording (30 Oct) | `e3c33dd31e210b44…` |
| [15_Test_latency_clock.jpg](attachments/15_Test_latency_clock.jpg) | Test: latency clock frames + first frame at school | `1079e805787d29cd…` |
| [16_Test_stage1_any_change.jpg](attachments/16_Test_stage1_any_change.jpg) | Test: stage 1 change masks (replay) | `12bc6093711bc1db…` |
| [17_Test_stage2_detection_area.jpg](attachments/17_Test_stage2_detection_area.jpg) | Test: stage 2 detection area (replay) | `0f65a1c33e8480e6…` |
| [18_Test_stage3_gecko_trigger.jpg](attachments/18_Test_stage3_gecko_trigger.jpg) | Test: stage 3 gecko trigger vs area rule (replay) | `6813be70ec418227…` |
| [19_Test_gecko_tracking.jpg](attachments/19_Test_gecko_tracking.jpg) | Test: gecko tracking frames (replay) | `fc104794e468dd56…` |
| [20_Test_yuv_planes.jpg](attachments/20_Test_yuv_planes.jpg) | Test: Y/U/V planes, why colour | `a76b8320e49bf2af…` |
| [21_Video_ring_buffer_timeline.mp4](attachments/21_Video_ring_buffer_timeline.mp4) | Video: ring buffer timeline on a real clip | `730324d145145dca…` |
| [22_Video_hand_vs_gecko_replay.mp4](attachments/22_Video_hand_vs_gecko_replay.mp4) | Video: hand vs gecko trigger (replay) | `71fece5d9655af5a…` |
| [23_Video_gecko_box_replay.mp4](attachments/23_Video_gecko_box_replay.mp4) | Video: gecko box (replay) | `459ef350bee87263…` |
| [24_Video_raw_clip_gecko_pulled.mp4](attachments/24_Video_raw_clip_gecko_pulled.mp4) | Video: raw clip saved by the recorder (5 Nov 18:45:26) | `55143b97a5133a4b…` |
| 25_Photo_setup_top_view.jpg | Photo: setup at school, top view, numbered labels (5 Nov) | `6f5bdc309f00bb67…` |
| 26_Photo_setup_side_view.jpg | Photo: setup at school, side view (30 Oct) | `6547869b5136312d…` |
| 27_Photo_camera_closeup.jpg | Photo: camera close-up (30 Oct) | `7461b09ac8935405…` |
| 28_Video_hardware_walkthrough.mp4 | Video: hardware walk-through at home, first 46 s (30 Oct) | `21969587a51f7aae…` |
| 29_Video_latency_clock_test.mp4 | Video: filming the latency clock test (5 Nov) | `755887fb08796f0e…` |
| 30_Video_home_webview_hand_test.mp4 | Video: home web view hand test, 45 s middle part (5 Nov) | `c15c0a31c2aa0f2d…` |
| 31_Video_lab_live_tracking.mp4 | Video: live tracking at school, URL bar pixelated (5 Nov) | `63474fe3f674e419…` |

25–31 是真实装置的照片和视频，只放在 Confluence 页面上，不存入本仓库（上传时经过一个临时分支，上传后已删除）。照片和视频中没有人脸；30 剪掉了有地址栏的开头和结尾，31 的地址栏做了自动打码（未逐帧核查）。
Files 25–31 (photos and videos of the real setup) are attached to the Confluence page only and are not kept in this repository.

页面正文（Confluence storage format）由 [page/build_page.py](page/build_page.py) 生成为 [page/page_body.storage.xml](page/page_body.storage.xml)。
