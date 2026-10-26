# In-Class Activity 6 · Tasks 1–8

当前归档入口，整理日期 2026-10-26。原始 [README_START_HERE](README_START_HERE.md)、[使用说明](使用说明.md)、[HARDWARE_PROGRESS](HARDWARE_PROGRESS.md) 保持历史内容不变。

| 文件夹 | 内容 |
| --- | --- |
| [00_Course_Materials](00_Course_Materials/) | 六份课件 PDF、七个原始示例 ZIP 与 IO_Control 包 |
| [01_Tasks_1-5](01_Tasks_1-5/) | Tasks 1–5：源码、源码 ZIP、说明与证据 |
| [02_Tasks_6-8](02_Tasks_6-8/) | Tasks 6–8：源码、源码 ZIP、说明与证据 |
| [03_Validation](03_Validation/) | 历史编译记录；见 [VALIDATION](VALIDATION.md) |
| [05_Real_Hardware_Evidence](05_Real_Hardware_Evidence/) | 原拍屏录像与采集方式说明的工作区备份 |
| [原始屏幕帧](../../archive/raw-screen-frames/) | 原先 04_Actual_Screen_Frames，单独归档以免干扰题目导航 |

## 使用与验证

按每题 README 打开与 sketch 文件夹同名的 `.ino`，保留配套 `SerialInput.h`。历史环境记录为 Arduino IDE 2.3.10 / ESP32 core 3.3.12 / AirM2M CORE ESP32C3 / IO_Control。部分编译日志目标写为通用 ESP32C3，早期实现使用 AirM2M FQBN；原记录均保留，不能假定两套实现环境完全一致。串口为 115200 baud。

文件归档没有修改源码，没有在此次导入中重新运行硬件测试。原编译/实机报告见上方原文，最新证据索引见 [EVIDENCE](../../docs/EVIDENCE.md)。

## 新发现的补拍材料

Documents 版本另有 Tasks 4/5 的 `SerialMonitor2.mov`、Task 7 两组 `Real_Light.MOV`，以及 Task 8 的 `IMG_1320.MOV`。因此旧说明中“尚缺 Task 8 手机录像”已经不是文件存在状态的完整描述。该录像抽样可见手、板卡和屏幕；短/长按及可读输出的完整覆盖仍待整段核对。

Task 7 采用 2000ms 暂停，保留课件 200ms/2000ms 的矛盾记录。Task 1 首次 1500ms 截图仍待查找/补充。课程平台是否已提交未知；旧截止日期仅作为历史要求保存，不推定延期或提交结果。
