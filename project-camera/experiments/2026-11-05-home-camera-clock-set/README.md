---
id: exp-home-camera-clock-set-20261105
type: experiment
environment: home
workstream: ws-preroll-recording
roadmap_stage: 1
aliases: [摄像头校时, OSD 时间, 画面时间, camera clock, ONVIF SetSystemDateAndTime]
related: [exp-home-board-clock-set-20261105, exp-home-stream-probe-20261105, ws-preroll-recording]
---

# 2026-11-05 · home 用 ROCK 时间设置摄像头时钟

日期：2026-11-05（香港）03:57–03:58。用户发现网页实时画面左上角的时间与板卡时间不一致，随后要求用 ROCK 的时间设置摄像头。这是**对摄像头设置的修改**，由用户在对话中明确同意。

## 原因

画面左上角的日期时间（OSD）由摄像头按自己的时钟叠加。摄像头时间方式为 NTP，但隔离的实验网连不到时间服务器，所以它的时钟一直不准：修改前比 ROCK 慢 2,427,179 秒（约 28 天 2 小时 13 分），与[只读探测](../2026-11-05-home-stream-probe/README.md)时的偏差一致，说明它一直在走，只是起点不对。ROCK 此前已[按 Mac 校准](../2026-11-05-home-board-clock-set/README.md)；录制程序的事件时间、文件名和网页时间轴都使用 ROCK 时间，不受影响。

## 方法

[cam_set_time.py](cam_set_time.py) 在 ROCK 上运行：先读取摄像头的时间、时区和时间方式并记录，等到 ROCK 时钟的下一个整秒，用 ONVIF `SetSystemDateAndTime` 把时间方式设为 `Manual`，写入当时的 UTC 时间；时区（`AWST-8WDT`，即 UTC+8）和夏令时（关闭）保持原值。2 秒后再读回核对。

## 结果

| 项目 | 修改前 | 修改后 |
| --- | --- | --- |
| 时间方式 | NTP（连不上服务器） | Manual |
| 摄像头 UTC 时间 | 2026-10-07 17:45:00 | 2026-11-04 19:58:01 |
| 与 ROCK 的差 | −2,427,178.8 秒 | −0.3 秒 |
| 时区 / 夏令时 | AWST-8WDT / 关闭 | 未变 |

设置请求返回 200、无错误。之后截取子码流画面左上角的时间条（[osd-after.jpg](osd-after.jpg)，只含时间字样一带）：显示 **2026-11-05 03:58:12**，截图后读到的 ROCK 香港时间为 03:58:13，与截图先后顺序一致。

## 限制

- ONVIF 只能精确到整秒，设置误差约在 1 秒内。
- 摄像头改为手动时间后不会再自动对时；它的时钟会不会慢慢走偏、断电（PoE 供电器拔掉）重启后能否保持，都没有测试。
- 如需恢复原设置：时间方式 NTP、时区 `AWST-8WDT`、夏令时关闭（见 [result.json](result.json)）。
- 画面上的时间仍只作为参考；事件时间以录制程序记录的 ROCK 时间为准。

## 证据与 SHA-256

| 文件 | SHA-256 |
| --- | --- |
| [result.json](result.json) | `1768f7d1cc88a54fdd130370ba319a76675d7cb4d7de90938b1d44ceef799239` |
| [cam_set_time.py](cam_set_time.py) | `9051289045a1db409f9b94d8a69c0f0c12fc89c276321b6e09d40deaecda4570` |
| [osd-after.jpg](osd-after.jpg) | `9e6e165ffd591c22d3b5b9445a217fd2e35eacb48b713241d8641dc01e98f6a2` |
