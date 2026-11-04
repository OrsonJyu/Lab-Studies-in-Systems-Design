---
id: exp-home-board-clock-set-20261105
type: experiment
environment: home
workstream: ws-preroll-recording
roadmap_stage: 1
aliases: [板卡校时, 时钟校准, ROCK 时间, clock sync, board clock]
related: [exp-home-stream-probe-20261105, ws-preroll-recording]
---

# 2026-11-05 · home 用 Mac 时间校准 ROCK 系统时钟

日期：2026-11-05（香港），Mac UTC 2026-11-04 18:45。前一项[只读探测](../2026-11-05-home-stream-probe/README.md)发现板卡比 Mac 慢约 5 天。用户选择在录制实验前用 Mac 时间校准 ROCK；**摄像头时间不改**。

## 方法

- 用户在 Mac 终端运行 [clock-sync.command](clock-sync.command)，自己输入板卡登录密码；助手没有接触密码。脚本在本机工具目录中运行，通过私有配置取得 SSH 目标，仓库副本仅作方法记录，不能直接在仓库目录运行。
- 测偏差：经 SSH 连续读 7 次板卡时间，取往返最短的一次，以往返中点计算 Mac − ROCK。
- 校准：在板卡上以 `sudo` 执行 `date -u -s`，目标时间为“板卡当前时间 + 测得偏差”，所以输入密码的时间长短不影响结果。
- 复测：校准后脚本再测一次；助手另用 9 次采样独立复测。
- Mac 时钟视为基准（已联网校时，未另行核对外部时间源）。

前两次运行失败，ROCK 时间都没有改：第一次脚本标准输入是 heredoc，sudo 收不到密码；第二次经共享 SSH 通道请求终端，键盘输入没有转发，助手结束了卡住的进程。第三次改为在 Mac 本地读取密码、经管道交给 `sudo -S` 后成功。板卡 sudo 日志与上述过程一致。

## 结果

| 项目 | 结果 |
| --- | --- |
| 校准前偏差（Mac − ROCK） | 455,720.007 秒（约 5 天 6 小时 35 分），往返 33.5 毫秒 |
| 校准时刻（Mac UTC） | 2026-11-04 18:45:36 |
| 校准后偏差（脚本） | 10.2 毫秒，往返 29.1 毫秒 |
| 独立复测（18:45:50） | 8.4 毫秒，往返 33.2 毫秒 |
| 板卡时间状态 | `NTP=yes`，`NTPSynchronized=no`；实验网仍没有可达的时间服务器 |
| 摄像头 | 未修改，仍按探测时约慢 28 天 |

**ROCK 系统时钟已与 Mac 对齐到约 ±15 毫秒内**（测量不确定度约为半个往返时间）。

## 限制

- 只校准了一次，没有测板卡时钟此后的漂移速度。
- 板卡有 `/dev/rtc0`，没有安装 fake-hwclock；重启或断电后时间能否保持未验证。录制实验前应先复测偏差，必要时重新校准。
- 摄像头 OSD 和摄像头内部时间仍不准；需要摄像头时间时按探测得到的偏差换算，或另行决定是否修改摄像头设置。
- 校准的是系统时间，不是视频包时间戳；包时间戳、DTS 与事件边界对齐仍需在录制实验中检查。

## 证据与 SHA-256

| 文件 | SHA-256 |
| --- | --- |
| [clock-sync-result.json](clock-sync-result.json) | `9f05cdb4a3976b36fc9144d9277c7b9b7ed8f97e3d051f9482c7c5d36f1af8a1` |
| [clock-sync.command](clock-sync.command) | `3721c0aba382e544ae769d14d27e906c4dbf73820372d8d2026b5f4181c4610e` |
