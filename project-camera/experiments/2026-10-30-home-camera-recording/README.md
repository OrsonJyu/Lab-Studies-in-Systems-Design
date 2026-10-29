---
id: exp-home-camera-recording-20261030
type: experiment
environment: home
workstream: ws-preroll-recording
roadmap_stage: 1
---

# home · 首次真实摄像头短录像

日期：2026-10-30（香港）。目标：由 ROCK 直接接收实物摄像头视频，在系统卡保存约 60 秒，再读回与完整解码。环境与接线见 [home](../../environments/home/README.md)。

## 输入与方法

1. 用户完成摄像头、48V PoE 供电器、普通千兆交换机、ROCK 和路由器的连接。
2. ROCK 保留管理网络，增加摄像头网段的临时有线地址。设备响应网页、ONVIF、RTSP 服务；ONVIF 返回主码流 H.264、2560 × 1440、20 fps 的配置。
3. 从 ONVIF 获取实际 RTSP URI，留在板卡私有配置。以 RTSP/TCP 读取主码流，直接封装为 MP4，不重新编码、不录音频。
4. 首批视频帧到达后，在聊天中通知用户开始挥手。用户负责镜头前动作，助手执行录制、检查及归档。
5. 用 ffprobe 检查容器，用 FFmpeg 完整解码并约每 5 秒抽帧；复制至 Mac 后核对 SHA-256。

本次运行的是临时命令/脚本，未形成可重启恢复的录制服务；没有可引用的录制系统源码提交。以下保留实际媒体操作的去凭据命令形式：

```sh
ffmpeg -hide_banner -nostdin -n -rtsp_transport tcp -timeout 10000000 \
  -i "$PRIVATE_RTSP_URI" -t 60 -map 0:v:0 -an -c:v copy \
  -movflags +faststart -progress pipe:1 -nostats "$OUT/camera-main-60s.mp4"
ffprobe -v error \
  -show_entries stream=codec_name,codec_tag_string,width,height,avg_frame_rate,r_frame_rate,nb_frames,start_time,duration:format=duration,size \
  -of json "$OUT/camera-main-60s.mp4"
ffmpeg -hide_banner -nostdin -n -v error -xerror -threads 4 \
  -i "$OUT/camera-main-60s.mp4" -vf 'fps=1/5,scale=640:-2' -an "$OUT/preview-%02d.jpg"
```

`$PRIVATE_RTSP_URI` 与 `$OUT` 是复现占位符。原始访问参数不进入 Git；现有日志中的访问 URI 与个人绝对路径已隐藏。

## 实际结果

| 项目 | 结果 |
| --- | --- |
| 采集命令开始 | 2026-10-30 01:53:09.886（香港）；原始 UTC 见结果 JSON |
| 实际文件编码 | H.264 / avc1 |
| 实际分辨率与标称帧率 | 2560 × 1440，20 fps |
| 容器时长与帧数 | 60.001 秒，1201 帧 |
| 文件大小 | 16,051,971 字节 |
| 采集退出码 | 0 |
| 完整解码与抽帧 | 退出码 0，解码日志为空，生成 12 个预览帧 |
| 图像观察 | 末段约 52.5 秒、57.5 秒可见手进入画面，镜头方向变化可见 |
| Mac 副本 | 与板卡文件 SHA-256 一致 |

**本次单路短录像的保存与完整解码通过。** 这项实测取代“没有摄像头录制实测证据”的当前状态描述，但不等于完整系统部署。

## 时间与限制

- 画面叠加日期显示 2026-10-07，与本次记录日期不一致；未自动修改摄像头时间，不拿 OSD 时间当事件真实时间。
- 录制日志有一条包时间戳未设置提示，以及两处重复 DTS 被 FFmpeg 微调的警告。文件可解码，不证明精确时间对齐通过；预录制前需进一步检查时间戳与实际片段边界。
- FFmpeg 的 `dup_frames` / `drop_frames` 输出不构成传输全程无丢失的独立证明。
- 本次只验证 `home`、系统卡、约一分钟的单路采集；未验证分段循环、事件触发、预录制、长期稳定性、重启/断流恢复、磁盘满、SATA 或学校/热点。
- 先前 Mac 连接失败与后来 ROCK 成功的条件不止一个变化，不能据此认定代理是唯一原因。

## 证据

- [原始录像](camera-main-60s.mp4)（Git LFS，未转码）
- [抽帧总览](contact-sheet.jpg) · [抽帧目录](previews/)
- [采集结果](capture-result.json) · [媒体与解码结果](validation-result.json)
- [录制日志](recording.log) · [解码日志](decode.log)
- [文件与来源校验](manifest.json)

下一项[实时预览](../2026-10-30-home-live-preview/README.md)另留用户确认，不与录像测试合并推定。
