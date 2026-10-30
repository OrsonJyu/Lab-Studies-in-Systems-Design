---
id: env-school
type: environment
environment: school
status: limited_network_and_preview_verified
aliases: [school, 学校环境, 校园环境, 有线预览, ROCK 热点, IINA]
related: [D011, D013, exp-school-network-preview-20261030, ws-preroll-recording]
---

# school · 学校网络与预览环境

更新：2026-10-30（香港）。本页记录同一天在学校进行的接入方式切换；这些是 `school` 的网络变体，不新建一个已被普遍验证的 `hotspot` 环境。当前用户选择为 **Mac、ROCK 和摄像头数据端接同一交换机**，见 [D013](../../../docs/DECISIONS.md)。

配置操作见[学校网络与预览指南](../../../docs/guides/SCHOOL_NETWORK_AND_PREVIEW_GUIDE.md)，逐项证据和限制见[学校实验记录](../../experiments/2026-10-30-school-network-preview/README.md)。真实地址、SSID、网卡名、访问参数和本机启动入口留在本地；仓库仅提供[字段示例](config.example.json)。

## 当前设备与最终接线

沿用 home 的 ROCK 4C+、IP 摄像头、TL-SG1008D 普通交换机和独立 PoE 供电器。板卡终端报告 Debian 12 / aarch64、内核 6.1.115-8-rk2501。本次 Mac 为 macOS 27.2，使用 IINA；IINA 应用版本未单独登记。

```text
Mac ── USB 以太网转接头 ── 交换机
ROCK 4C+ 网口 ──────────── 交换机
PoE 供电器 LAN 数据口 ──── 交换机
PoE 供电器 POE 输出口 ──── 摄像头

Mac Wi-Fi ── 校园网（外网接入，与本地有线视频路径分开）
ROCK 的 USB-C 线：本次由 Mac 供电，供电稳定性未独立验收。
```

最终预览路径：**摄像头 → 交换机 → Mac / IINA**。该路径不以 ROCK 转发或手机热点可用为前提。ROCK 在这一拓扑中保留为拟录制端，但学校录像尚未测试。

## 分变体记录

| 变体 | 本次结果 | 边界 |
| --- | --- | --- |
| 校园 Wi-Fi 来源共享 | macOS 弹窗明确拒绝共享受 802.1X 保护的连接 | 只证明本次互联网共享方式不可用；未测出学校所有设备互通或客户端隔离规则 |
| Mac 与 ROCK 临时网线直连 | 本地 IPv6 SSH 和后续静态有线 SSH 曾成功 | 临时地址随后丢失；不能当成重启自动恢复通过 |
| 另一台电脑热点 | Mac 与 ROCK 的无线 SSH、ROCK 到相机端口连通；FFplay 探测和三秒解码曾通过 | 用户随后报告黑屏或画面不动，FFplay 可视预览不记为成功 |
| iPhone 热点 | 无线 SSH；经 ROCK/SSH 转发的 IINA 可见预览由用户确认 | 用户报告“网络太差”；未测吞吐、丢包或延迟，间歇 SSH 超时原因未定 |
| ROCK 自建 AP | NetworkManager 报告 AP 支持为 yes；配置复用后用户确认无线 SSH 成功 | 本地练习用途，没有验收外网、重启自动启动或持续视频性能 |
| 最终全有线 | Mac 直达相机的 80/554/8899 TCP 端口；H.264、2560 × 1440、报告 20 fps；三秒解码通过；用户确认 IINA 预览成功 | 末次检查中板卡固定 IPv4/SSH 仍未恢复；IPv6 只有 ICMP 回应，未通过 SSH；用户后续“成功”仅计作有线预览确认 |

本次 Mac 有线链路协商为 **100 Mbps 全双工**；交换机支持千兆不等于每段链路均以千兆运行，也没有进行端到端吞吐测试。

## 已保存配置与恢复条件

- 板卡 `school-camera`：NetworkManager 静态 IPv4，同摄像头网段，无有线默认路由；设置为**手动启用**。配置已创建和激活过，但末次需再次恢复管理连接后启用。
- 板卡 `rock-lab-ap`：AP 模式、独立于摄像头网段的 shared IPv4、WPA-PSK/RSN，手动启用；切换 AP 会改变内置无线接口的角色。
- Mac 网口：手动设置同摄像头网段的独立地址，网关和 DNS 留空；Wi-Fi 可另接校园网。真实值不进入仓库。
- IINA 本机入口：手机热点版经 SSH 转发；最终有线版直接读摄像头，采用 RTSP/TCP、软件解码和关闭声音。入口和带访问参数的 JSON 均留本地，未发布通用播放器程序。
- `IPQoS=none`、IPv4、超时和重试曾用于本机 SSH 兼容性测试；不同 QoS 标记测试均曾成功，**没有证明 QoS 或代理是唯一故障原因**。

## 尚未验证

学校环境未保存新录像，没有新的学校视频文件、持续录像、SATA、预录制、摄像头时间校准、长期流畅性、重启/断流恢复或性能对比验收。home 的一分钟录像仍仅属于 home。外接 USB 无线网卡未被采用为已验证方案，芯片和 macOS 兼容性没有确认。
