---
id: exp-home-system-card-20261030
type: experiment
environment: home
workstream: ws-preroll-recording
roadmap_stage: 1
---

# home · 系统卡基础视频保存

日期：2026-10-30（香港）。目标：确认 ROCK 可以在系统 microSD 上保存、读回并完整解码短视频。输入为合成画面，摄像头尚未参与这项测试。

## 条件与方法

设备、存储与环境见 [home](../../environments/home/README.md)。板卡 FFmpeg 5.1.9，以实时速率读取 `testsrc2`，输出 640 × 360、15 fps 的 H.264/MP4、无音频，60 秒。写入后同步文件系统，以 ffprobe 完整计帧，并用 FFmpeg 完整软件解码。随后复制到 Mac 核对 SHA-256。

下列命令中的 `$OUT` 是本次实验输出目录占位符，不是共享的永久部署路径：

```sh
ffmpeg -hide_banner -nostdin -n -re -f lavfi -i testsrc2=size=640x360:rate=15 \
  -t 60 -an -c:v libx264 -threads 2 -preset ultrafast -crf 23 \
  -pix_fmt yuv420p -movflags +faststart "$OUT/synthetic-60s.mp4"
sync
ffprobe -v error -count_frames \
  -show_entries stream=codec_name,width,height,avg_frame_rate,nb_read_frames:format=duration,size \
  -of json "$OUT/synthetic-60s.mp4"
ffmpeg -hide_banner -nostdin -v error -xerror -i "$OUT/synthetic-60s.mp4" -f null -
```

## 实际观察

| 项目 | 结果 |
| --- | --- |
| 视频 | 60.000 秒，900 帧，640 × 360，15 fps |
| 文件 | 8,915,986 字节 |
| 生成与同步耗时 | 60.76 秒 |
| 完整软件解码 | 退出码 0，解码日志为空 |
| 本地复制 | 两端 SHA-256 一致 |

结论：**本次条件下的基础保存、读取和软件解码通过**。不是速度上限、容量、耐久、真实取流、SATA 或预录制测试。

贡献记录：助手执行生成、检查和归档；未据此推定其他组员的个人贡献。来源和文件校验见 [manifest.json](manifest.json)。

- [原始测试视频](synthetic-60s.mp4)（Git LFS）
- [结构化结果及命令](result.json)（个人路径已替换为占位符）
- [生成日志](encode.log)
- [解码日志](decode.log)

后续真实摄像头测试单独记录于[下一项实验](../2026-10-30-home-camera-recording/README.md)。
