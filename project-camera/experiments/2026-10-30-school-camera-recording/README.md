---
id: exp-school-camera-recording-20261030
type: experiment
environment: school
workstream: ws-preroll-recording
roadmap_stage: 1
---

# school · 后续板卡 60 秒录像

实验日期：2026-10-30，香港 17:40。登记日期：2026-11-05。这是同日较早[学校网络与预览记录](../2026-10-30-school-network-preview/README.md)之后的另一次实验；保留前一记录的当时限制，不把较早阶段的“尚无学校录像”继续当作当前事实。

本聊天后来通过有线 IPv6 恢复 SSH，手动激活原 school-camera；同一交换机连接 Mac、ROCK 和摄像头数据端。ROCK 将 RTSP/TCP 原码流存入系统 microSD，无音频。

- 文件 60.001 秒，H.264 / avc1，2560×1440，1200 帧，37,637,189 字节。
- 采集退出码 0；板卡完整软件解码退出码 0，12 张预览。拷贝到 Mac 后 SHA-256 相同。
- 原片 SHA-256：`1428f1431419b4da59b007ef171c6308c7aa5766fb38c40ea7811f0fe4e7bb6d`。
- 仍有未设置时间戳和非单调 DTS 警告；OSD 日期不正确。未证明事件时间对齐、预录、SATA或长期性能。
- 当时 profile 仍为手动；网络持久恢复在[后续 home 实验](../2026-11-05-home-wired-recovery/README.md)另记。

本目录上传的是原 JSON 采集、解码及复制校验结果。原片、预览、原始私有日志和机器脚本保留在本地，未上传此视频，不声称能从 GitHub 下载或重放它。源文件与摘要的范围分别说明，不能用 manifest 哈希替代独立重复实验。

这次之前另有一次 Mac 录制尝试：请求 60 秒，实际 58 秒后 RTSP 超时，虽然文件可解码，未通过预期时长；不将它混作本次 ROCK 验收。用户现场接线并选择仅做 60 秒验收，助手执行录制和文件检查；没有新课程提交或他人贡献确认。
