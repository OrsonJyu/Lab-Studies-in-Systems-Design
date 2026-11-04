---
id: env-home
type: environment
environment: home
status: shared_wired_reboot_verified
aliases: [home, 家庭环境, 共用有线]
related: [D002, D011, D012, D014, ws-preroll-recording]
---

# home · 当前共用有线环境

更新：2026-11-05。按[统一指南](../../../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md)使用同一个 lab-wired 基线：Mac USB 网卡、ROCK、摄像头数据端接独立交换机；Mac Wi-Fi 用于外网，交换机没有路由器/墙口上联。真实地址/接口/UUID取共用私有 JSON，不在本页复制。

板卡保留原 UUID 和固定地址，已将 school-camera 改名 lab-wired，自动连接 yes、优先级 100、有线无默认路由；三份旧无线 profile 保存为手动备用。完成卡恢复后的开机和配置统一后的正常重启，均未手动 connection up 即恢复 SSH；主机密钥、路由、端口与只读检查器通过。重启后三秒视频解码为 60 帧，无错误，新录像未启动。[实测与限制](../../experiments/2026-11-05-home-wired-recovery/README.md)。

## 沿用设备与已有媒体

ROCK 4C+、Debian 12 / aarch64、系统 microSD / ext4；普通 TL-SG1008D 配独立 PoE 供电器。摄像头实物标称 4MP、2.8mm、PoE 48V/4W、ONVIF，实际流 H.264、2560×1440、报告 20 fps。SATA仍为项目方向但未验收。详见[原实物观察](hardware-observations.json)，不据旧图确认芯片/确切型号/固件或 PoE 标准认证。

10-30 的[系统卡合成测试](../../experiments/2026-10-30-home-system-card/README.md)、[真实短录](../../experiments/2026-10-30-home-camera-recording/README.md)和[用户确认预览](../../experiments/2026-10-30-home-live-preview/README.md)保持原证据。其 DHCP 管理和临时辅助地址是旧实验条件，不再作为日常配置。

当前不把学校 Wi-Fi、热点、代理或 QoS 当作唯一根因；摄像头/板卡时钟、DTS、预录、SATA、长时间与异常断电恢复仍待验收。本机预览入口读取共用 JSON，但本次未重新作播放器可视确认。旧[home 实验教程](../../../docs/guides/HOME_HARDWARE_AND_EXPERIMENT_GUIDE.md)仅保留历史接线/取流/短录步骤的参考用途。
