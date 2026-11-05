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
- [home 运动检测手挥动](../../../project-camera/experiments/2026-11-05-home-motion-hand-test/README.md)：recorder 0.2 用子码流帧差检测，四个事件自动开启/结束；手出现前保留 3.7–4.65 秒，检测延迟 0.45–0.65 秒。
- [home 手动触发录制](../../../project-camera/experiments/2026-11-05-home-recorder-manual-trigger/README.md)：[recorder 0.1](../../../project-camera/src/recorder/README.md) 在内存盘做 2 秒分段滚动缓存；三个手动事件均保住触发前 5.0–5.6 秒，按静止 5 秒结束，3 秒内两次触发合并为一个事件。
- [home 延迟测量](../../../project-camera/experiments/2026-11-05-home-latency/README.md)：稳定接收时拍摄到 ROCK 约 0.19–0.29 秒；“触发后才启动录制”第一帧内容比触发晚约 0.36–0.41 秒，FFmpeg 约 2 秒后才输出，证实需要滚动缓存。
- [home 码流与接口探测](../../../project-camera/experiments/2026-11-05-home-stream-probe/README.md)：主/子码流关键帧间隔实测均为 2 秒；摄像头公告 ONVIF 运动事件主题（PullPoint），无录像/回放服务；板卡软件解码子码流约占 6 核的 3.6%。板卡与摄像头时钟分别慢约 5 天、28 天。

## 未完成与待定项

- [ ] 摄像头时间校准，包时间戳、重复 DTS 和事件/片段边界对齐验证。
- [x] home 共用有线自动启动及一次正常重启恢复；同一私有 JSON、按地点记录。
- [x] 新学校基线现场检查与录制服务首次运行（2026-11-05，[记录](../../../project-camera/experiments/2026-11-05-school-recorder-first-run/README.md)）。
- [ ] 板卡在学校中途失联一次的原因（供电/卡死/网线）；长期运行与异常断电恢复。
- [x] 循环分段、手动事件接收、片段保护、等待尾段、续接和过期清理：recorder 0.1 已在 home 用三个短事件实测。
- [x] 运动检测接入同一事件逻辑，并用手挥动做触发实验（recorder 0.2）。
- [ ] 在实际饲养箱机位和守宫上标定检测阈值与遮罩；光线变化、夜视切换下的误触发。
- [x] 局域网网页：实时画面、状态、时间轴标记与回放（recorder 0.3，已部署到 ROCK）。
- [ ] 网页往回拖看缓存画面、登录保护；开机自启。
- [ ] 断流、重启、磁盘满与长期连续运行的故障/恢复记录。
- [ ] SATA 硬盘连接、供电、挂载与正式写入验证。
- [ ] 摄像头商业品牌、运动事件的实际触发与延迟、供电兼容性。ONVIF 自报型号字符串、固件和事件主题已读取，尚未订阅或收到事件。
- [x] 2026-11-05 用户选择用 Mac 时间校准 ROCK；校准后偏差约 10 毫秒（[记录](../../../project-camera/experiments/2026-11-05-home-board-clock-set/README.md)）。
- [x] 2026-11-05 用户要求后，用 ROCK 时间经 ONVIF 设置摄像头（改为手动时间，修改后差 0.3 秒，画面时间核对一致）[记录](../../../project-camera/experiments/2026-11-05-home-camera-clock-set/README.md)。
- [ ] 板卡时间重启后保持情况、漂移速度（摄像头已确认断电后丢失手动时间，需每次重设）；实验网内长期时间源（例如 ROCK 提供 NTP）。
- [ ] 控制程序最终用 Python、Node-RED 或其他组合；数据库/消息协议仍为候选。
- [ ] 触发前保留 p 秒、静止结束阈值 n 秒、后录长度、缓存保留期限和事件元数据：未确认；5 秒仍仅为示例。
- [x] 10-30 较晚阶段恢复 school 板卡管理并完成一次系统卡录像；与较早 Mac 预览分别记录。
- [ ] 对 school 的网络/预览作持续性与重启恢复测试；其他热点/地点继续单独建记录。

## 下一次实验的操作意图

按用户 11-03 的讨论，手代 gecko 测运动触发、连续静止 n 秒结束，短暂停顿后再动保持同一事件；同时检查预录片段开头和端到端/检测延迟。网站实时画面为可选后续。5 秒静止和 3–5 秒预录只是建议，不是已确认参数；详见[接续上下文](../../handoffs/2026-11-05-shared-wired-baseline.md)。

## 完成标准

ROADMAP 阶段 1–4 各有可复核记录，覆盖连续运行、预录片段实际边界、事件时间对齐和故障恢复。当前短录像及预览只是基础进展，本工作流仍 active。
