# SD5531 · Lab Studies in Systems Design

豹纹守宫观察与记录系统，以及课程实验的可追溯档案。  
**PolyU · Project 2 / Video Recording Module · [English](README.en.md)**

版本：**v1.5.0** · 更新日期：**2026-11-05（香港）** · [变更记录](CHANGELOG.md) · [迁移范围](docs/SYNC_REPORT.md)

本项目为学校师生与照护者提供持续的影像和热阵列记录，支持回放、观察比较，以及后续经验证的行为信息整理。仓库同时保存课堂活动、开发过程、讨论和展示成果。**项目规划、代码可编译、实机观察与课程提交是不同状态。**

## 从这里开始

| 你想做什么 | 阅读入口 |
| --- | --- |
| **在另一台电脑上一键安装并运行守宫录像 demo** | [demo 一键安装与运行](project-camera/demo/README.md) |
| 家里/学校用同一配置，避免开机失联 | [共用有线指南](docs/guides/SHARED_WIRED_NETWORK_GUIDE.md) → [只读检查器](project-camera/src/network/README.md) |
| 接续下一阶段工作 | [当前上下文](docs/handoffs/2026-11-05-shared-wired-baseline.md) |
| 第一次来，了解项目与资料位置 | [文档导航](docs/INDEX.md) → [当前状态](docs/STATUS.md) |
| 理解完整目标和最新技术方向 | [项目范围](docs/SCOPE.md) → [系统架构](docs/ARCHITECTURE.md) |
| 看演示稿、架构图与跨组计划 | [摄像头项目成果](project-camera/README.md) |
| 找课堂活动代码与提交材料 | [课程实验目录](activities/README.md) |
| 看某件事做到哪了 | [工作流](docs/workstreams/README.md) |
| 核对测试与原始证据 | [证据索引](docs/EVIDENCE.md) |
| 分清家庭、学校和热点的测试条件 | [测试环境](project-camera/environments/README.md) |
| 复现 home 的接线、录像和实时预览 | [硬件与程序实验指导](docs/guides/HOME_HARDWARE_AND_EXPERIMENT_GUIDE.md) |
| 在学校配置有线网络、恢复 SSH 或练习 ROCK 自建热点 | [school 环境](project-camera/environments/school/README.md) → [配置与预览指南](docs/guides/SCHOOL_NETWORK_AND_PREVIEW_GUIDE.md) |
| 理解决定为什么变化 | [决定记录](docs/DECISIONS.md) → [历史时间线](docs/HISTORY.md) |
| 查看知识之间的关系 | [知识网](knowledge/NETWORK.md) · [机器可读图](knowledge/GRAPH.json) |
| 作为 agent 接手维护 | [AGENTS.md](AGENTS.md) → [PROJECT_STATE.json](PROJECT_STATE.json) → [记忆指南](docs/guides/GIT_MARKDOWN_MEMORY_GUIDE.md) |

## 当前基线

- **现场设备**：用户在 2026-10-23 明确采用 **Radxa ROCK 4C+＋本地 SATA 机械硬盘**。ROCK 5C、SSD 和云端方案仍作为历史探索保留。
- **已有实测**：home 系统卡短录/预览通过；school 同日后续完成一次板卡 60 秒短录和完整解码。原片与摘要的上传范围见各实验记录，SATA 未验收。
- **当前网络**：用户确认 home/school 统一独立交换机有线接法，Mac Wi-Fi 只负责外网。lab-wired 保留原 UUID/地址，自动连接；旧无线配置为手动备用。home 的装卡启动及统一后的正常重启均已恢复 SSH，重启后短解码通过。
- **事件录制**：[recorder 0.3](project-camera/src/recorder/README.md) 在 ROCK 上持续缓存最近画面，子码流检测到运动就保存含触发前画面的片段，静止 n 秒结束；局域网网页显示实时画面、状态和带运动时刻标记的时间轴。home 用手模拟时，手出现前保留 3.7–4.65 秒，检测延迟约 0.5 秒；拍摄到 ROCK 约 0.23 秒。p=4、n=5 仍是测试值。
- **近期重点**：在实际饲养箱机位和守宫上标定检测阈值；开机自启、断流恢复与长期运行；网页回看缓存与登录保护。
- **完整范围**：视频及热阵列采集、存储与访问、定位及个体识别探索、行为时间线与空间使用、跨组数据对齐。预录制只是其中一步。
- **已有成果**：展示 PDF / PPTX、合作计划、会议转录与 AI 纪要、Figma 文字及图片快照、8 题 Arduino 代码、编译记录与硬件证据。
- **环境边界**：配置共用、证据按地点分开；新 lab-wired 在学校现场仍待复测。通用 hotspot 和所有 Wi-Fi 组合未验收，检测到网段重叠应先协调地址规划。
- **证据边界**：预录与运动触发只在 home 用手短时间验证，尚无开机自启、长期稳定性、守宫检测或行为识别验收；课堂 ESP32C3 实验仍是独立证据。

## 目录

```text
docs/                 当前说明、决定、进度及历史讨论
  workstreams/        进行中 / 已完成的工作
  guides/             仓库记忆与维护指南
project-camera/       摄像头项目：展示、跨组计划、会议与设计快照
  src/                录制系统代码状态与约定
  experiments/        按日期和环境记录实测、媒体与校验
  environments/       home 与 school 已测条件；独立热点迁移边界
activities/           课堂实验：电路、焊接、2026-10-16 编程活动
knowledge/            带来源与关系类型的知识网
references/           课程资料与早期迁移参考（原样保存）
archive/              早期版本、采集原始帧及诊断程序
provenance/           来源、文件路径与 SHA-256 清单
scripts/              资料完整性和链接检查
```

原始视频及屏幕采集帧采用 Git LFS。完整下载需要先安装 Git LFS，再执行 `git lfs pull`；普通网页阅读文档不受影响。上传是否完成以[迁移报告](docs/SYNC_REPORT.md)为准。

课程附件、第三方代码和历史素材保留原有权利归属；本仓库不为这些材料新增开放许可。后续更新遵循[维护约定](CONTRIBUTING.md)与[版本规则](docs/VERSIONING.md)。
