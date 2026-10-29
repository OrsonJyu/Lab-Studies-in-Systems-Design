---
id: ws-preroll-recording
type: workstream
status: active
aliases: [预录制, 事件前录像, pre-roll, pre-event recording, 录制工作流, recording pipeline]
related: [D002, D003, D004, D005]
---

# 预录制工作流 / Pre-event recording

更新：2026-10-29。目标与阶段划分来自 [ROADMAP](../../ROADMAP.md) 阶段 1–4 和 [ARCHITECTURE](../../ARCHITECTURE.md)；这里只记录本工作流的现状和待定项。

## 目标

一条摄像头视频流经过接收、循环分段缓存和事件触发后，生成**包含触发前画面**的可播放片段，并留下对应事件记录。测试触发可以由人工发出，以便将录制链路与运动检测分开验证。

## 现状

- 硬件方向：ROCK 4C+ ＋本地 SATA 机械硬盘（[D002](../../DECISIONS.md)）。
- 已收集资料中**没有**摄像头录制的实现代码或实测记录；本工作流尚处于起步阶段。
- 代码放 [`project-camera/src/`](../../../project-camera/src/README.md)，每次测试放 [`project-camera/experiments/`](../../../project-camera/experiments/README.md)。

## 待定项（未确认前不当作需求）

- 摄像头确切型号、视频流和运动事件接口、PoE 规格。
- SATA 硬盘的连接与供电方式；ROCK 4C+ 的系统版本。
- 控制程序用 Python 还是 Node-RED（[D005](../../DECISIONS.md)）。
- 预录 `n` 秒、事件后时长、缓存保留期限、重叠事件合并方式。讨论里的"5 秒"只是示例。
- 事件元数据字段：草案见 ARCHITECTURE"时间与记录约定草案"。

## 完成标准

ROADMAP 阶段 1–4 各自有可复核的实验记录：读流与回放日志、连续运行、事件片段实际边界与事件时间对齐、断流/重启/磁盘满等故障情况。
