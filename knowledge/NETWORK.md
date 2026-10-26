# 知识网 / Knowledge network

版本 1.0 · 整理日期 2026-10-26。对应[机器可读图 GRAPH.json](GRAPH.json)。本图由既有材料整理，用于找到概念、决定、成果与验证之间的关系；不把关系线视为因果证明或已实现的数据链。

```mermaid
flowchart TD
    G[学校观察与学习目标] --> S[完整项目范围]
    S --> V[视频采集与保存]
    S --> T[热阵列观察]
    S --> B[行为与空间信息]
    S --> X[跨组数据对齐]
    H[ROCK 4C+ + SATA HDD: user confirmed] --> V
    Z[Historical Figma diagrams] --> O
    O[ROCK 5C / SSD / cloud: historical] -. superseded baseline .-> H
    V --> P[近期预录制工作流]
    P --> F[FFmpeg: media operations]
    P --> C[Controller: proposed event/retention logic]
    P --> M[时间与事件元数据草案]
    X --> M
    B --> R[人工复核与可见性记录]
    T --> R
    A[Arduino课堂活动] --> E[编译/串口/物理证据]
    D[展示与历史讨论] --> S
```

## 如何读取

| 关系 | 含义 |
| --- | --- |
| `defines_scope` / `includes` | 文档描述范围或范围包含某能力，不表示完成 |
| `user_confirms` / `supersedes` | 用户明确事实与旧基线之间的修订 |
| `proposed_role` / `depends_on` | 建议的角色或验证依赖，不表示已部署 |
| `documents` / `evidence_for` | 材料记录某项内容或支持指定范围的观察 |
| `requires_validation` | 明确待验证或待协商的部分 |

图中的每条 JSON 关系都列出状态、来源路径和理由。新的关联应有独立价值；不把所有概念相互连接，也不把旧提案提升为已确认实现。

关键来源：[SCOPE](../docs/SCOPE.md)、[ARCHITECTURE](../docs/ARCHITECTURE.md)、[DECISIONS](../docs/DECISIONS.md)、[EVIDENCE](../docs/EVIDENCE.md)、[历史讨论](../docs/HISTORY.md)。
