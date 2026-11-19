---
phase: 事件录制原型（Project 2 / Video Recording Module）
updated: 2026-11-19
next: 整理文件库资料；school 现场复测共用有线基线；手部触发录制实验
---

# 项目现状

本文件是规范要求的简短入口，直接改写。详细现状只维护在 [docs/STATUS.md](docs/STATUS.md) 和 [PROJECT_STATE.json](PROJECT_STATE.json)，这里不复制。

## 阶段

ROCK 4C+ 上的 recorder 0.3 已能在隔离有线实验网中按运动保存事件片段并提供局域网页面；预录制参数、SATA、长期运行和跨组接口仍未验收。

## 最近改动

- 2026-11-19：接入 [project-standards](https://github.com/OrsonJyu/project-standards) 1.3.0（模块 hardware、software），文件库连接到 `library/`。

## 当前决定

见 [docs/DECISIONS.md](docs/DECISIONS.md)，当前硬件基线为 D002 / D012 / D014 / D015。

## 验证

`python3 scripts/check_standard.py` 通过；导入原件 `project-camera/references/Tutorial/` 的旧链接已列入 `exclude`。

## 限制

- 文件库里的资料尚未按 5.1 节归位，分类方案等待用户确认，见 [docs/LIBRARY.md](docs/LIBRARY.md)。
- 硬件结论的边界见 [docs/STATUS.md](docs/STATUS.md)。

## 下一步

- 用户确认分类方案后整理文件库、运行 `library.py clean`。
- 见 [docs/STATUS.md](docs/STATUS.md) 的"下一项实验"和 [docs/ROADMAP.md](docs/ROADMAP.md)。
