# 工作流 / Workstreams

回答"这件事做到哪了"。每个工作流一份文件，文件名即 `id`（`ws-*`）。做法见[仓库记忆指南](../guides/GIT_MARKDOWN_MEMORY_GUIDE.md)。

| 状态 | id | 内容 |
| --- | --- | --- |
| active | [ws-preroll-recording](active/ws-preroll-recording.md) | 摄像头接收、循环缓存、事件触发与预录片段 |
| active | [ws-archive-gaps](active/ws-archive-gaps.md) | 档案缺项与课堂证据复核 |
| completed | [ws-archive-baseline](completed/ws-archive-baseline.md) | v1.0.0 资料档案基线 |

## 规则

- 只为**正在做或已完成**的事建文件，不预先列出 ROADMAP 中尚未启动的阶段。
- 文件头：`id`、`type: workstream`、`status`、`aliases`、`related`（决定编号或其他 `ws-*`）。
- 本工作流专属的要求、临时约定和待定参数写在这里，**不升级为全局规则**；被团队确认后再写进 DECISIONS。
- 当前文件只写现状；进度变化直接改写，过程留给 Git 历史与实验记录。
- 完成后用 `git mv` 移到 `completed/`，更新本表和指向它的链接。
