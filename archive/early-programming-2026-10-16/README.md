# SD5531 In-Class Activity 6 - 16 October 2026

本文件夹包含本课全部 6 份 PDF、7 个原始示例，以及 Tasks 1-8 的独立 Arduino sketch。每题的代码文件夹与 .ino 同名，InputHelpers.h 已随需要它的题目一同保存。

## 文件分类

- 00_Reference/PDFs：本课 6 份原始 PDF。
- 00_Reference/Example_ZIPs：页面提供的 7 个原始示例压缩包。
- Task_01 至 Task_08：每题的独立代码、英文说明、Evidence 验证资料。
- 01_Submission_ZIPs：每题一个可上传的源码 ZIP。
- 02_Submission_Notes.md：按 Task 1-8 整理的英文说明，可用于准备提交页面。
- 03_Validation：运行环境和额外验证资料。

## 作业范围与期限

课程第 7 课对应 In-Class Activity 6，要求完成 Tasks 1-5 和 6-8，每个 sub-team 一份提交。Tasks 1-5 截止 2026-10-23，Tasks 6-8 截止 2026-10-30（课程页面原文为 end of date）。此处仅准备本地文件，没有向课程平台提交。

## 使用方法

1. 打开题目子文件夹内的 .ino。
2. 使用已安装的 IO_Control 库，板型选 AirM2M CORE ESP32C3，USB CDC On Boot 为 Disabled，串口 115200 baud。
3. 编译并上传到开发板，再依照每题 README 中的测试步骤检查。
4. 将对应源码 ZIP 和实际运行截图/视频上传到对应 Task 标题下。

## 已知课件矛盾

Task 7 对 -1 的暂停时间在 lecture 6 p.40 写 2000ms，在 p.41 写 200ms。本答案采用 p.40 的完整例子（2000ms），并将时间集中在 PAUSE_MS 常量中。

## 验证与提交证据状态

正在验证，最终状态见后续更新。不得将模拟、预期输出或编译记录当作实板截图/视频。
