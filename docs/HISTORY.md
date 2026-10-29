# 历史时间线 / Project history

本页是便于定位的整理，原始陈述见下方讨论档案。历史日期与 2026-10-26 仓库导入日期分开。

| 时期 | 内容 | 后续关系 |
| --- | --- | --- |
| 2026-09-15 | 确立 SD5531 项目；首选 PoE IP Camera → ROCK 5C → SSD，备选 ESP32-P4/UVC/SD；热阵列与跨组范围 | 作为原始 scope；硬件后由 D002 修订 |
| 2026-09-17 整理 | 两段会议 ASR、AI 纪要与中文讲解 | 实际会议日期/说话人/关键语句仍有不确定性 |
| 2026-09 规划与展示 | 架构图、云端路线、个体识别/定位、跨组输入输出及展示文件 | 原图保留；模型、设备数量不当作验证结论 |
| 2026-10-16 起 | In-Class Activity 6：八题代码、编译、主机模拟、逐步采集实机证据 | 两套实现均保存，早期版单独标记 |
| 2026-10-23 | 用户明确 ROCK 4C+ + SATA HDD；讨论信息流、循环缓存及事件前录像 | 当前技术基线与近期验证目标 |
| 2026-10-26 | 建立仓库档案、导航、版本与知识网；发现补拍物理录像 | 文件导入不代表重新完成硬件验收 |
| 2026-10-29 | 采用 Git + Markdown 记忆指南；新增工作流、源码与实验目录，明确分支规则（D009） | 仓库维护方式调整，不涉及项目实现进度 |
| 2026-10-30 | ROCK 4C+ 启动与 SSH、系统卡合成视频、真实摄像头约 60 秒录像与完整解码、Mac 实时预览；用户命名本次环境为 home（D011），本阶段先用系统卡（D012） | 首个有限摄像头实测基线；时间校准、DTS、预录制、SATA、长期与跨环境验证仍待完成；见[home](../project-camera/environments/home/README.md)与[实验索引](../project-camera/experiments/README.md) |

## 可检索讨论档案

- [主讨论 Main: Videoing](history/main-videoing.md) · [JSON](history/main-videoing.json)
- [Plan-pre：架构与展示讨论](history/planning-presentation.md) · [JSON](history/planning-presentation.json)
- [完成课堂活动：后续核对](history/programming-review.md) · [JSON](history/programming-review.json)
- [编程执行记录中的用户消息与最终答复](history/programming-execution.md) · [JSON](history/programming-execution.json)
- [早期编程请求](history/programming-initial.md) · [JSON](history/programming-initial.json)
- [2026-09-15 原始迁移历史](../references/project-migration/历史对话.md)

这些文件保留可访问的用户文字与助手最终答复；不包含系统指令、内部推理或完整工具日志。缺失附件、不再可用的本地路径和平台截断内容不会被推测补齐。旧请求只作史料，不应重放执行。
