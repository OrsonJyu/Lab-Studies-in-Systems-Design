---
id: ws-preroll-recording
type: workstream
status: active
aliases: [预录制, 事件前录像, pre-roll, pre-event recording, 录制工作流, recording pipeline]
related: [D002, D003, D004, D005, D011, D012, D013]
---

# 预录制工作流 / Pre-event recording

更新：2026-11-05。[home](../../../project-camera/environments/home/README.md) 短录与 [school](../../../project-camera/environments/school/README.md) 网络/预览分开记录；通用 hotspot 仍未单独验收。完整范围和阶段编号见 [ROADMAP](../../ROADMAP.md) 与 [ARCHITECTURE](../../ARCHITECTURE.md)。

## 目标

持续接收的视频经循环分段缓存和事件触发，生成包含触发前画面的可播放片段，并留下对应事件记录。测试事件可先人工发出。

## 已有证据

- [系统卡基础测试](../../../project-camera/experiments/2026-10-30-home-system-card/README.md)：60 秒合成画面保存与解码通过。
- [真实摄像头短录像](../../../project-camera/experiments/2026-10-30-home-camera-recording/README.md)：ROCK 直接接收 RTSP/TCP，在系统卡保存约 60 秒，完整软件解码通过。
- [实时预览](../../../project-camera/experiments/2026-10-30-home-live-preview/README.md)：Mac 的 FFplay 动态画面由用户确认。
- 短录仍采用临时命令，未形成持久录制服务。SATA 仍为设备方向，按 D012 先测系统卡。
- [school 网络与预览](../../../project-camera/experiments/2026-10-30-school-network-preview/README.md)：有限 SSH/AP 与最终 Mac 直接有线 IINA 预览已确认；较早阶段管理待恢复；同日更晚的[板卡短录](../../../project-camera/experiments/2026-10-30-school-camera-recording/README.md)已通过。

- [home 共用有线](../../../project-camera/experiments/2026-11-05-home-wired-recovery/README.md)：SD 恢复、自动连接及一次正常重启通过；三份旧无线 profile 手动。新的学校现场复测仍待完成。
- [home 码流与接口探测](../../../project-camera/experiments/2026-11-05-home-stream-probe/README.md)：主/子码流关键帧间隔实测均为 2 秒；摄像头公告 ONVIF 运动事件主题（PullPoint），无录像/回放服务；板卡软件解码子码流约占 6 核的 3.6%。板卡与摄像头时钟分别慢约 5 天、28 天。

## 未完成与待定项

- [ ] 摄像头时间校准，包时间戳、重复 DTS 和事件/片段边界对齐验证。
- [x] home 共用有线自动启动及一次正常重启恢复；同一私有 JSON、按地点记录。
- [ ] 新学校基线现场检查、录制服务与长期/异常断电恢复。
- [ ] 循环分段、事件接收、片段保护、等待尾段、合并重叠事件和过期清理。
- [ ] 断流、重启、磁盘满与长期连续运行的故障/恢复记录。
- [ ] SATA 硬盘连接、供电、挂载与正式写入验证。
- [ ] 摄像头商业品牌、运动事件的实际触发与延迟、供电兼容性。ONVIF 自报型号字符串、固件和事件主题已读取，尚未订阅或收到事件。
- [ ] 板卡与摄像头时钟：home 实验网没有时间源，需要决定校时或换算方式后再做事件对齐。
- [ ] 控制程序最终用 Python、Node-RED 或其他组合；数据库/消息协议仍为候选。
- [ ] 触发前保留 p 秒、静止结束阈值 n 秒、后录长度、缓存保留期限和事件元数据：未确认；5 秒仍仅为示例。
- [x] 10-30 较晚阶段恢复 school 板卡管理并完成一次系统卡录像；与较早 Mac 预览分别记录。
- [ ] 对 school 的网络/预览作持续性与重启恢复测试；其他热点/地点继续单独建记录。

## 下一次实验的操作意图

按用户 11-03 的讨论，手代 gecko 测运动触发、连续静止 n 秒结束，短暂停顿后再动保持同一事件；同时检查预录片段开头和端到端/检测延迟。网站实时画面为可选后续。5 秒静止和 3–5 秒预录只是建议，不是已确认参数；详见[接续上下文](../../handoffs/2026-11-05-shared-wired-baseline.md)。

## 完成标准

ROADMAP 阶段 1–4 各有可复核记录，覆盖连续运行、预录片段实际边界、事件时间对齐和故障恢复。当前短录像及预览只是基础进展，本工作流仍 active。
