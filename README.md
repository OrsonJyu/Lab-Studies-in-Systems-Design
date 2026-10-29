# SD5531 · Lab Studies in Systems Design

豹纹守宫观察与记录系统，以及课程实验的可追溯档案。  
**PolyU · Project 2 / Video Recording Module · [English](README.en.md)**

版本候选：**v1.2.0**（PR 审阅后合并、再打标签） · 更新日期：**2026-10-30（香港）** · [变更记录](CHANGELOG.md) · [迁移范围](docs/SYNC_REPORT.md)

本项目为学校师生与照护者提供持续的影像和热阵列记录，支持回放、观察比较，以及后续经验证的行为信息整理。仓库同时保存课堂活动、开发过程、讨论和展示成果。**项目规划、代码可编译、实机观察与课程提交是不同状态。**

## 从这里开始

| 你想做什么 | 阅读入口 |
| --- | --- |
| 第一次来，了解项目与资料位置 | [文档导航](docs/INDEX.md) → [当前状态](docs/STATUS.md) |
| 理解完整目标和最新技术方向 | [项目范围](docs/SCOPE.md) → [系统架构](docs/ARCHITECTURE.md) |
| 看演示稿、架构图与跨组计划 | [摄像头项目成果](project-camera/README.md) |
| 找课堂活动代码与提交材料 | [课程实验目录](activities/README.md) |
| 看某件事做到哪了 | [工作流](docs/workstreams/README.md) |
| 核对测试与原始证据 | [证据索引](docs/EVIDENCE.md) |
| 分清家庭、学校和热点的测试条件 | [测试环境](project-camera/environments/README.md) |
| 理解决定为什么变化 | [决定记录](docs/DECISIONS.md) → [历史时间线](docs/HISTORY.md) |
| 查看知识之间的关系 | [知识网](knowledge/NETWORK.md) · [机器可读图](knowledge/GRAPH.json) |
| 作为 agent 接手维护 | [AGENTS.md](AGENTS.md) → [PROJECT_STATE.json](PROJECT_STATE.json) → [记忆指南](docs/guides/GIT_MARKDOWN_MEMORY_GUIDE.md) |

## 当前基线

- **现场设备**：用户在 2026-10-23 明确采用 **Radxa ROCK 4C+＋本地 SATA 机械硬盘**。ROCK 5C、SSD 和云端方案仍作为历史探索保留。
- **本次实测**：`home` 环境中，ROCK 已启动 Debian 12 并能 SSH 管理；先用系统 microSD 保存合成片段和约 60 秒真实摄像头录像，完整解码通过；Mac 实时预览由用户确认。SATA 没有参与这次验证。
- **近期重点**：处理摄像头时间、视频时间戳与临时网络配置，再实现循环分段、事件触发和预录制；这些部分仍未验收。
- **完整范围**：视频及热阵列采集、存储与访问、定位及个体识别探索、行为时间线与空间使用、跨组数据对齐。预录制只是其中一步。
- **已有成果**：展示 PDF / PPTX、合作计划、会议转录与 AI 纪要、Figma 文字及图片快照、8 题 Arduino 代码、编译记录与硬件证据。
- **环境边界**：本次明确命名为 `home`；`school` / `hotspot` 仅预留、未测试。地址、设备互通、热点/校园网络隔离和结果各自记录，不把家庭网络当通用配置。
- **证据边界**：已有有限摄像头实测，尚无完整持久录制服务、预录制、长期稳定性或行为识别验收；课堂 ESP32C3 实验仍是独立证据。

## 目录

```text
docs/                 当前说明、决定、进度及历史讨论
  workstreams/        进行中 / 已完成的工作
  guides/             仓库记忆与维护指南
project-camera/       摄像头项目：展示、跨组计划、会议与设计快照
  src/                录制系统代码状态与约定
  experiments/        按日期和环境记录实测、媒体与校验
  environments/       home 已测条件；学校/热点迁移边界
activities/           课堂实验：电路、焊接、2026-10-16 编程活动
knowledge/            带来源与关系类型的知识网
references/           课程资料与早期迁移参考（原样保存）
archive/              早期版本、采集原始帧及诊断程序
provenance/           来源、文件路径与 SHA-256 清单
scripts/              资料完整性和链接检查
```

原始视频及屏幕采集帧采用 Git LFS。完整下载需要先安装 Git LFS，再执行 `git lfs pull`；普通网页阅读文档不受影响。上传是否完成以[迁移报告](docs/SYNC_REPORT.md)为准。

课程附件、第三方代码和历史素材保留原有权利归属；本仓库不为这些材料新增开放许可。后续更新遵循[维护约定](CONTRIBUTING.md)与[版本规则](docs/VERSIONING.md)。
