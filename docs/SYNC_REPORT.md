# 资料迁移与完整性 / Synchronization report

盘点日期：**2026-10-26（香港）**。目标：`OrsonJyu/Lab-Studies-in-Systems-Design`，保持私有。

## 来源与组织

| 来源组 | 归档位置 | 处理方式 |
| --- | --- | --- |
| 项目镜像 `sources` | `references/project-migration/` | 复制；原文件未修改 |
| 工作区当前编程产出 | `activities/2026-10-16-programming/`、`archive/raw-screen-frames/` | 保存代码、证据及原始帧 |
| 工作区早期编程产出 | `archive/early-programming-2026-10-16/` | 明确为独立早期实现，不与最终源码混用 |
| iCloud 课程文件夹 | `references/course/`、`project-camera/references/`、`activities/` | 保存课程、展示、会议、电路与焊接素材 |
| Documents 编程工作目录 | `activities/2026-10-16-programming/`、`archive/board-diagnostics/` | 相同文件共用路径；新增物理录像纳入 |
| 可读取的相关 chats | `docs/history/` | 保存用户文字与助手最终答复，带日期/原始 turn ID |
| Figma | `project-camera/design/` | 文字/节点索引、26 份顶层可视 PNG、原在线入口 |

逐文件映射与 SHA-256 见 [source-manifest.json](../provenance/source-manifest.json)。它记录 **1,701 条来源文件记录、1,624 个不同归档路径**（不含本次新写的维护文档及新增 Figma 快照）。同内容复制到同一目的路径时去重；不丢弃不同版本。有冲突时保存到 `archive/mirror-differences/`。忽略系统 `.DS_Store`。

来源文件累计约 **2.21 GB（十进制，含来源间重复）**。大体积原视频与原始帧采用 Git LFS，保留原始字节，不用转码替代原件。

## 当前传输状态

**目前可取得的资料已完成上传与校验。** 原始资料导入提交 `464fa5f25633b9a1bfbe5fb8f023a3bcb7163b71` 已发布到 main，接续原有历史。

Git LFS 的 **1,414 个文件路径对应 1,029 个独立对象，约 1.98 GB**；全部 1,029 个对象已逐批确认在远端可读取，[核对记录](../provenance/remote-lfs-check-2026-10-26.json)中缺失数为 0。原件保持原始字节，完整性检查见 [IMPORT_VALIDATION](IMPORT_VALIDATION.md)。

正式资料基线：[v1.0.0](https://github.com/OrsonJyu/Lab-Studies-in-Systems-Design/releases/tag/v1.0.0)。此前的 v0.1.0 文档基线保留为版本标签；不可取得的历史原件仍按下表登记，未伪称已经补齐。

## 尚未取得的历史材料

| 缺项 | 影响 / 下一步 |
| --- | --- |
| 白板照片 `IMG_1633.HEIC` | 原讨论中的 Downloads 路径已无文件；保留文字讨论，需用户补原图 |
| 两段教师会议原始录像/音轨 | 已有转录；无法独立回听关键语句，不能把 ASR 升级成教师确认 |
| Tutorial 的 `QUALITY_REVIEW.md`、`working/` 字幕/文本/概率 JSON | 原始引用仍保留；需要原处理文件夹才能恢复完整转录复核链 |
| 旧 `00_CONFLUENCE_SYNC` JSON 快照 | 会议纪要引用了这些本地快照，但当前课程目录没有；不能冒充本次在线核实 |
| Figma 原生 `.fig` 完整导出 | 当前有在线入口、文字及完整顶层可视快照；不等同于可离线恢复整个设计的原生文件 |
| 课程平台提交回执 | 当前没有，提交状态待用户确认 |
| 未暴露到当前可访问 chats 的内容/附件 | 目前已归档相关可访问返回页；其他历史内容不能保证可取全 |

## 原始链接与文档冲突

原始文件保持内容不变，可能仍含失效本地路径和旧状态。新导航维护相对链接；历史链接不是遗漏上传的自动证据。Tutorial 原文把 `MEETING_MINUTES_CN.md` 指向不存在的旧名，本次新增同名导航页连接实际 `MEETING_MINUTES_CN(1).md`。其余缺失引用明确登记，不制作虚假的原始文件。

已发现原 Task 8 文档所称“缺手机录像”与后来新增文件不一致；当前说明使用“文件已找到，完整覆盖待核”。具体见 [STATUS](STATUS.md) 与 [EVIDENCE](EVIDENCE.md)。
