---
id: ws-preroll-recording
type: workstream
status: active
aliases: [预录制, 事件前录像, pre-roll, pre-event recording, 录制工作流, recording pipeline]
related: [D002, D003, D004, D005, D011, D012, D013]
---

# 预录制工作流 / Pre-event recording

更新：2026-10-30。[home](../../../project-camera/environments/home/README.md) 短录与 [school](../../../project-camera/environments/school/README.md) 网络/预览分开记录；通用 hotspot 仍未单独验收。完整范围和阶段编号见 [ROADMAP](../../ROADMAP.md) 与 [ARCHITECTURE](../../ARCHITECTURE.md)。

## 目标

持续接收的视频经循环分段缓存和事件触发，生成包含触发前画面的可播放片段，并留下对应事件记录。测试事件可先人工发出。

## 已有证据

- [系统卡基础测试](../../../project-camera/experiments/2026-10-30-home-system-card/README.md)：60 秒合成画面保存与解码通过。
- [真实摄像头短录像](../../../project-camera/experiments/2026-10-30-home-camera-recording/README.md)：ROCK 直接接收 RTSP/TCP，在系统卡保存约 60 秒，完整软件解码通过。
- [实时预览](../../../project-camera/experiments/2026-10-30-home-live-preview/README.md)：Mac 的 FFplay 动态画面由用户确认。
- 本次采用临时命令和网络辅助地址，未形成完整持久录制服务。SATA 仍为设备方向，但本阶段按 D012 先测系统卡。
- [school 网络与预览](../../../project-camera/experiments/2026-10-30-school-network-preview/README.md)：有限 SSH/AP 与最终 Mac 直接有线 IINA 预览已确认；末次板卡管理待恢复，学校未录制新视频。静态/AP 配置已保存但为手动启用。

## 未完成与待定项

- [ ] 摄像头时间校准，包时间戳、重复 DTS 和事件/片段边界对齐验证。
- [ ] 网络与服务重启后的恢复；每个环境使用自己的地址、接口和配置。
- [ ] 循环分段、事件接收、片段保护、等待尾段、合并重叠事件和过期清理。
- [ ] 断流、重启、磁盘满与长期连续运行的故障/恢复记录。
- [ ] SATA 硬盘连接、供电、挂载与正式写入验证。
- [ ] 摄像头确切商业型号/固件、运动事件接口及供电兼容性。
- [ ] 控制程序最终用 Python、Node-RED 或其他组合；数据库/消息协议仍为候选。
- [ ] 预录 n 秒、后录长度、缓存保留期限和事件元数据：未确认；5 秒仍仅为示例。
- [ ] 恢复 school 最终有线板卡管理，验证板卡到相机和一次学校录像；已有 Mac 预览不替代该验收。
- [ ] 对 school 的网络/预览作持续性与重启恢复测试；其他热点/地点继续单独建记录。

## 完成标准

ROADMAP 阶段 1–4 各有可复核记录，覆盖连续运行、预录片段实际边界、事件时间对齐和故障恢复。当前短录像及预览只是基础进展，本工作流仍 active。
