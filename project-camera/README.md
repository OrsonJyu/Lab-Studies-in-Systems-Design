# 摄像头项目 / Camera project

> 2026-11-05 当前入口：[共用有线指南](../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md) · [只读检查器](src/network/README.md) · [接续上下文](../docs/handoffs/2026-11-05-shared-wired-baseline.md)。home 重启通过，学校后续短录已补录，新学校基线现场仍待复测。


当前硬件与状态先看 [STATUS](../docs/STATUS.md)；范围与角色看 [SCOPE](../docs/SCOPE.md) 和 [ARCHITECTURE](../docs/ARCHITECTURE.md)。这里保存实际成果与来源。

| 成果 | 阅读 / 使用 |
| --- | --- |
| 27 页项目展示稿 | [PDF](references/SD5531_Gecko_Presentation_Group2.pdf) |
| 可编辑演示文件 | [PPTX](references/SD5531_Gecko_Presentation_final.pptx) |
| 1 页跨组合作计划 | [PDF](references/Gecko_各组合作计划.pdf) |
| 会议转录与 AI 解读 | [Tutorial](references/Tutorial/README.md) |
| 架构图与 Figma 档案 | [Design](design/README.md) |
| 决定与范围变化 | [DECISIONS](../docs/DECISIONS.md) |
| 录制系统代码状态与约定 | [src](src/README.md) |
| home / school 实测记录与模板 | [experiments](experiments/README.md) |
| 测试环境与迁移边界 | [home / school / hotspot](environments/README.md) |
| 当前工作流 | [ws-preroll-recording](../docs/workstreams/active/ws-preroll-recording.md) |

这些文件可能处于不同历史阶段。展示和 Figma 中的 ROCK 5C / SSD / Cloud Server 不覆盖 2026-10-23 用户明确的 ROCK 4C+ + SATA HDD 基线。文件名中的 final 不独立证明已提交或全组确认。

2026-10-30 的 `home` 测试先使用系统 microSD：真实短录像和用户确认的实时预览已通过；SATA、预录制、长期稳定性及其他环境仍需各自验证。

school 同日较晚阶段已恢复板卡管理并完成[60 秒短录](experiments/2026-10-30-school-camera-recording/README.md)，与较早网络/预览阶段分开。11-05 共用策略已在 home 重启验收，新学校现场待复测；日常配置见[统一指南](../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md)。
