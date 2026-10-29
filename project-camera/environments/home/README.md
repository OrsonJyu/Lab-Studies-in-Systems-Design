---
id: env-home
type: environment
environment: home
status: limited_hardware_baseline_verified
aliases: [home, 家庭环境, 家中测试, 移动办公]
related: [D002, D011, ws-preroll-recording]
---

# home · 家庭测试环境

用户于 2026-10-30 命名。本页描述这次实测条件；不作为学校或热点的通用网络配置。

从接线到取流、录像、解码和预览的操作步骤，见 [home 硬件与程序实验复现指南](../../../docs/guides/HOME_HARDWARE_AND_EXPERIMENT_GUIDE.md)。指南中的现场参数需重新填写，不是已有自动部署服务。

## 实物与运行环境

| 部分 | 本次观察 / 限制 |
| --- | --- |
| 现场计算 | ROCK 4C+；Debian GNU/Linux 12 bookworm，aarch64；内核 6.1.115-8-rk2501 |
| 录制工具 | 板卡 FFmpeg / ffprobe 5.1.9-0+deb12u1；Python 标准库调用 ONVIF |
| 本次存储 | 系统 microSD 卡，ext4；开始测试时根文件系统约剩余 104 GiB |
| SATA HDD | 仍是项目设备方向（D002）；本次没有参与录像验证，不能据此标记已接通 |
| 摄像头标签 | 标称 4MP、2.8mm、PoE 48V / 4W，ONVIF；标签本身未给出完整品牌/型号/固件 |
| 实际保存的视频 | H.264 / avc1，2560 × 1440，约 20 fps；详见原文件检查结果 |
| 数据交换机 | TP-LINK TL-SG1008D，普通 8 口千兆交换机；它不承担 PoE 供电 |
| 摄像头供电 | 独立 PoE 供电器，标签型号 4805、输出 48V / 0.5A；IEEE 协商兼容性未独立验收 |
| 管理与预览 | Mac 经路由器网络 SSH 到 ROCK；FFplay 8.0.1 通过仅监听 Mac 本机的 SSH 转发看 RTSP/TCP 视频，用户确认画面更新 |

旧展示/Figma 中 `XM530AI + SC2235`、5MP、ROCK 5C、SSD/云端等文字保留为历史材料。不能用芯片组合或旧商品截图覆盖本次实物标签与实际视频参数，也没有据此确认新摄像头的芯片型号。

实物照片的来源 ID、校验值及去访问参数观察见 [hardware-observations.json](hardware-observations.json)。原始照片保留在本地，未将带默认访问信息的标签图或房间全景上传。

## 本次成功接线与数据路径

```text
摄像头 ← PoE 供电器的 POE 输出口
                 LAN 数据口
                     │
              TL-SG1008D 交换机
                ├── ROCK 4C+（独立电源）
                └── 路由器 LAN ── Wi-Fi ── Mac

录像：摄像头 → 交换机 → ROCK / FFmpeg → 系统 microSD 卡
预览：摄像头 → ROCK → SSH 本机转发 → Mac / FFplay
```

供电器的 POE 口按标签为有电压输出，仅连接匹配的摄像头；LAN 口接普通数据网络。交换机端口数量足够不等于设备地址、掩码和路由已经互通。

## 地址与持续性

摄像头保留原固定地址；ROCK 原管理地址由当前家庭网络分配。本次给 ROCK 有线接口增加了摄像头网段的**临时辅助 IPv4 地址**，保留原管理地址与默认路由。这不是完整持久网络部署：板卡重启、更换路由器或网卡后需重新核对与配置。

真实地址、远程私有文件位置和本机播放器路径保存在本地配置，不写入仓库。字段示例见 [config.example.json](config.example.json)；示例不会自动配置网络，也不是可直接运行的配置。

## 已验证与未验证

- [系统卡基础保存/解码](../../experiments/2026-10-30-home-system-card/README.md)：60 秒合成画面，不是摄像头录像。
- [真实摄像头短录像](../../experiments/2026-10-30-home-camera-recording/README.md)：约 60 秒保存与完整解码通过，末段可见手进入画面。
- [实时预览](../../experiments/2026-10-30-home-live-preview/README.md)：用户确认 Mac 独立播放器中的画面持续更新；没有测量端到端延迟。
- 摄像头 OSD 日期不正确；录制出现未设置时间戳和两处 DTS 修正警告。精确时间对齐、预录制、长期稳定性、自动恢复、SATA、跨组接口均未通过本次测试。
- Mac 直连阶段曾有 ARP 回应但 TCP 服务超时；切换到 ROCK 取流后成功。代理开关、接线及网络路径没有形成单变量实验，**不能认定 Shadowrocket 是唯一原因**。

移动办公的记录方法及学校/热点待测边界见[环境目录](../README.md)。
