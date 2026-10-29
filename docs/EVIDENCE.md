# 成果与证据索引 / Evidence index

核对日期：2026-10-30。2026-10-26 的导入只验证档案关系；本次新增 home 摄像头实测。课堂编译/实机结果继续按历史证据记录，没有在这次重新验收。

| 材料 | 位置 | 可以支持 / 限制 |
| --- | --- | --- |
| home 系统卡合成视频 | [实验](../project-camera/experiments/2026-10-30-home-system-card/README.md) | 基础保存与解码通过；不验证摄像头 |
| home 真实摄像头录像 | [实验与原片](../project-camera/experiments/2026-10-30-home-camera-recording/README.md) | 一次约 60 秒保存/解码、现场手部画面；OSD 与 DTS 问题保留，不证明预录制/长期稳定 |
| home Mac 实时预览 | [用户确认记录](../project-camera/experiments/2026-10-30-home-live-preview/README.md) | 用户确认 FFplay 动态画面；无延迟或跨环境性能结论 |
| home 实物参数 | [去访问参数观察与照片校验值](../project-camera/environments/home/hardware-observations.json) | 实物标签/型号观察；原始照片仍在本地，不独立证明协议标准认证 |
| 摄像头项目展示 | [PDF](../project-camera/references/SD5531_Gecko_Presentation_Group2.pdf)、[PPTX](../project-camera/references/SD5531_Gecko_Presentation_final.pptx) | 展示 scope 和探索方案；不证明部署、算法准确率或采购 |
| 跨组合作计划 | [合作计划 PDF](../project-camera/references/Gecko_各组合作计划.pdf) | 对接内容与机位讨论稿；责任需双方确认 |
| 会议资料 | [Tutorial 入口](../project-camera/references/Tutorial/README.md) | 机器转录与 AI 解读；原始音视频和质量报告尚未找到 |
| Figma | [设计档案](../project-camera/design/README.md) | 当前在线节点文字和26 份顶层架构图可视快照；仍包含旧方案，不等于最新硬件状态 |
| 编程任务 | [Tasks 1–8 总入口](../activities/2026-10-16-programming/README.md) | 八题源码、ZIP、英文测试步骤 |
| 编译结果 | [VALIDATION](../activities/2026-10-16-programming/VALIDATION.md)、[日志目录](../activities/2026-10-16-programming/03_Validation/) | 历史编译/链接通过；不等于电气或实际时序正确 |
| 实机记录 | [HARDWARE_PROGRESS](../activities/2026-10-16-programming/HARDWARE_PROGRESS.md) | 历史串口实机观察；拍屏与物理动作证据分开 |
| 早期模拟测试 | [运行环境](../archive/early-programming-2026-10-16/03_Validation/Build_Environment.md)、[测试代码](../archive/early-programming-2026-10-16/03_Validation/host_tests/) | 调度/串口/GPIO 适配模拟；不测试电路或二进制库 |
| 电路与焊接影像 | [BaseCircuits](../activities/BaseCircuits/)、[Soldering](../activities/Soldering/) | 原始课堂影像；未据此判定完成评分要求 |
| 原始采集帧 | [raw-screen-frames](../archive/raw-screen-frames/) | 拍屏视频生成的原始帧/采集信息；以 Git LFS 保存 PNG |

## 编程题目逐项

以下目录中的 `README.md` 提供题目与测试要求；`Evidence_To_Record` 是原文件夹名，即使已有录像也不重命名。

| 题目 | 源码/证据入口 | 当前可核对情况 |
| --- | --- | --- |
| 1 串口欢迎语 | [Task 1](../activities/2026-10-16-programming/01_Tasks_1-5/Task_01_Serial_Welcome/) | 已有串口 PNG；历史审查建议补首次 1500ms 输出，本次未找到新增截图 |
| 2 定时 FSM | [Task 2](../activities/2026-10-16-programming/01_Tasks_1-5/Task_02_Timed_Message_FSM/) | 历史记录称六条指定消息均有截图，源码及 ZIP 已更新 |
| 3 整数转换 +15 | [Task 3](../activities/2026-10-16-programming/01_Tasks_1-5/Task_03_Serial_Integer_Plus15/) | 五组输入/结果串口截图 |
| 4 重复输出 | [Task 4](../activities/2026-10-16-programming/01_Tasks_1-5/Task_04_Repeat_Hello_World/) | 拍屏 MP4 + 后来新增 `SerialMonitor2.mov`；完整覆盖需按要求复核 |
| 5 可改时长 FSM | [Task 5](../activities/2026-10-16-programming/01_Tasks_1-5/Task_05_Configurable_FSM/) | 拍屏 MP4 + 后来新增 `SerialMonitor2.mov` |
| 6 双 LED | [Task 6](../activities/2026-10-16-programming/02_Tasks_6-8/Task_06_Dual_LED_Blink/) | 三必做用例的串口视频，另有独立双 LED 测试 |
| 7 摩斯播放列表 | [Task 7](../activities/2026-10-16-programming/02_Tasks_6-8/Task_07_Morse_Sequence_Player/) | 两组串口 MP4，并找到后来补拍的两份 Real_Light.MOV；暂停歧义见 D007 |
| 8 短/长按 | [Task 8](../activities/2026-10-16-programming/02_Tasks_6-8/Task_08_Short_Long_Press/) | 串口 PNG/MP4，另找到 IMG_1320.MOV；抽样可见板卡/手/屏幕，完整结果待复核 |

已有原文件中的 `RECORDING_REQUIRED.txt` 是早期占位说明，不优先于后来出现的真实文件。课程提交回执尚未收集，不能从文件齐全推断已提交。

## 新实验记录

问题与假设、日期、设备/软件版本、条件、输入/操作、预期、实际观察、失败/缺失、证据路径、可确认的个人贡献、下一步。摄像头实验还应记录时间对齐、断流、磁盘状态与回放结果。摄像头实验按[实验记录模板](../project-camera/experiments/README.md)存放在 `project-camera/experiments/`；已有 home 实验；每项 front matter 和结果 JSON 标明环境，SHA-256 清单对应文件原字节。学校/热点需另建记录。
