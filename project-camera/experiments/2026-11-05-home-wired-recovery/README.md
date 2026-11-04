---
id: exp-home-wired-recovery-20261105
type: experiment
environment: home
workstream: ws-preroll-recording
roadmap_stage: 1
---

# home · SD 网络恢复与共用有线重启验收

日期：2026-11-05（香港）。观察时间以 Mac/客户端为准；ROCK 和相机时间源尚未校准。用户选择的共用策略见[D014](../../../docs/DECISIONS.md)及[统一指南](../../../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md)。

## 问题和离线检查

ROCK 的旧家庭地址、学校固定地址与 IPv6 均不可达；此前 Mac 到摄像头成功。局部检查中 Mac 链路还曾在 100/10 Mbps 变化。直连协商到千兆和板卡绿灯不独立证明 Linux 已正常启动。

系统卡在 Mac 内置读卡器被标记 internal；只筛选 external 曾漏检，后续纠正。Linux 分区可用只读工具读取，并非由 Finder 无内容直接认定坏卡。卡套 LOCK 解释只读标志；没有认定它造成板卡上的历史失联。

已检查的持久目录含四份网络 profile，唯一有线 profile 的 autoconnect=false。全局 ifupdown managed=false 不等于关闭所有网络；未找到执行关闭全部网络或 Wi-Fi 射频的历史证据。原状态文件缺失也不能单独证明网络被关闭。

ext4 同时出现 clean 状态值、needs_recovery 和 orphan_present；只读检查跳过日志时有空闲计数差异。备份网络配置及约 173 MB 元数据后，标准工具配合撤销记录恢复日志、仅修改有线自启一行，并保持 root:root / 0600。完整只读校验通过，恢复标志清除。该备份不是完整整卡镜像；实际带权限的读写由用户在 Mac Terminal 启动助手准备的脚本，助手从本地报告核对。

## 共用策略和验收

1. 用户确认交换机只接 Mac、ROCK、摄像头数据端，Mac Wi-Fi 用于外网。
2. 装回卡上电后自动有线 SSH 成功，没有手动 connection up；主机密钥匹配原板卡。
3. 在保留 UUID 和地址的前提下改名 lab-wired，自动连接 yes、优先级 100、有线不设默认路由；三份旧无线配置保留且改为手动。未删除凭据或关闭全局射频。
4. 确认无正在运行的 FFmpeg 录制后，执行一次正常系统重启；重启后自动恢复 SSH。只读检查器的主机身份、路由、地址、端口与远端状态全部通过。
5. 重启后单独探测 H.264、2560×1440、报告 20 fps；三秒内存软件解码 60 帧，退出码 0，错误日志为空。未保存新录像或开启播放器。

[结构化结果](result.json)、[只读检查报告](health-check.json)、[视频检查](video-check.json)和 manifest 的哈希范围分别记录。网络/修复叙述为依据私有原始资料整理的摘要，不是完整原始工具日志。源私有报告哈希允许与本地原件核对；原 profile、密码、SSID、实际地址、磁盘编号、镜像、撤销文件和针对个人设备的写卡脚本未上传。

## 限制

确认了未自启的配置缺陷，同时也处理了日志恢复，没有单变量对照来宣布唯一根因。仅完成一次装卡启动及一次统一配置后的正常重启；不表示长期、异常断电恢复或全部 Wi-Fi 已验证。共用新基线在学校仍需现场复测；原学校后续短录另记。SATA、时钟、延迟和运动触发/预录均未验收。
