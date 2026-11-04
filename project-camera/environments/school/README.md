---
id: env-school
type: environment
environment: school
status: historical_wired_recording_verified_shared_baseline_retest_pending
aliases: [school, 学校环境, 共用有线, IINA]
related: [D011, D013, D014, ws-preroll-recording]
---

# school · 共用策略与历史验收

更新：2026-11-05。用户决定学校与家里继续使用同一[有线基线](../../../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md)：三个数据端接独立交换机，Mac Wi-Fi 仅负责外网；同一私有 JSON 与同一 lab-wired profile，不为学校另建地址/UUID。新基线已在 home 完成重启验收，在学校现场仍需再次运行检查器。

## 2026-10-30 历史过程

| 变体 | 当时结果与边界 |
| --- | --- |
| 校园 Wi-Fi 来源共享 | macOS 拒绝 802.1X 来源共享，不证明校园全局客户端隔离 |
| 临时有线管理 | IPv6 和静态 IPv4 SSH 曾成功，出现过地址丢失/未激活 |
| 电脑热点 | 有限无线 SSH/视频探测，用户后续报告黑屏或不动，不记可视成功 |
| iPhone 热点 | 用户确认 IINA 可见，但报告网络差；无延迟/吞吐定量结论 |
| ROCK AP | 用户确认无线 SSH；没有长期、外网或重启自启验收 |
| 较早全有线预览 | Mac 直读相机，三秒解码和用户可视确认通过；该阶段末次板卡管理仍未恢复 |
| 后来同日板卡录像 | 17:39 恢复有线管理，手动启用 school-camera，17:40 起完成系统卡 60 秒短录与完整解码；仍有时间戳问题，profile 当时仍手动 |

较早[网络/预览实验](../../experiments/2026-10-30-school-network-preview/README.md)保持原阶段结论；后续[板卡录像](../../experiments/2026-10-30-school-camera-recording/README.md)另起记录。仓库本次只补录该视频的结构化 JSON，原片仍本地保存。

旧学校静态/AP配置原本均手动。11-05 在 home 已修复并统一为 lab-wired 自动连接；旧无线 profile 保留且均手动，没有关闭全局射频。不要再把原 school-camera 的不自启当作当前要求，也不要从家中重启成功推定校园已复测。

ROCK 原学校使用 Mac USB-C 供电，负载供电稳定性未独立验收；普通交换机不供 PoE。长期性能、SATA、预录、时钟/事件对齐仍待验证。学校[旧探索指南](../../../docs/guides/SCHOOL_NETWORK_AND_PREVIEW_GUIDE.md)保留历史热点配置，日常使用共用指南。
