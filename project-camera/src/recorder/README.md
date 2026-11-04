# 滚动缓存事件录制 / Rolling-buffer recorder

版本：`recorder/0.1`（手动触发）。运行在 ROCK 4C+：Debian 12、Python 3.11（只用标准库）、FFmpeg 5.1。工作流见 [ws-preroll-recording](../../../docs/workstreams/active/ws-preroll-recording.md)。

## 做什么

1. FFmpeg 不重新编码，把摄像头主码流切成约 2 秒一段的 MPEG-TS，写进内存盘 `/dev/shm`，不磨损系统卡。
2. 收到“有运动”的信号就开启事件；**连续 `still_s` 秒没有新的运动信号就结束**；结束前又有运动则续接同一事件。
3. 事件结束后，取“第一次运动前 `pre_roll_s` 秒”到“结束”之间的分段，直接拼成 MP4，连同一份 JSON 记录存到 `output_dir`。
4. 超出 `ring_seconds` 且没有事件需要的分段自动删除。

目前运动信号只能手动发出（`trigger` 命令）。运动检测会作为另一个信号来源接进同一套事件逻辑，尚未实现。

为什么要缓存而不是检测到再开始录：见 [延迟实验](../../experiments/2026-11-05-home-latency/README.md)，触发后才连接摄像头，第一帧比触发晚约 0.4 秒，FFmpeg 约 2 秒后才开始输出。

## 运行

```sh
cp config.example.json ~/sd5531/recorder/config.json   # 按需修改
python3 recorder.py run --config ~/sd5531/recorder/config.json
```

另一个终端发出手动运动信号：

```sh
python3 recorder.py trigger --config ~/sd5531/recorder/config.json            # 一次
python3 recorder.py trigger --config ~/sd5531/recorder/config.json --hold 8   # 运动持续 8 秒
```

`Ctrl-C` 停止；未结束的事件会以 `partial` 状态保存。流地址从板卡私有的 `source_config` 读取，不写进配置或日志。

## 参数

| 键 | 默认 | 含义 |
| --- | --- | --- |
| `pre_roll_s` | 4 | 第一次运动前至少保留多少秒；实际按分段边界往前取，通常多 0–2 秒 |
| `still_s` | 5 | 静止多少秒算事件结束（需求里的 n） |
| `segment_seconds` | 2 | 分段长度；摄像头关键帧间隔为 2 秒，实际只能在关键帧处切 |
| `ring_seconds` | 60 | 没有事件时保留最近多少秒 |
| `max_event_s` | 300 | 单个事件最长秒数，到时强制结束 |
| `min_free_mb` | 500 | 输出目录剩余空间低于此值就不写视频，只写失败记录 |
| `capture_latency_s` | 0.23 | 拍摄到 ROCK 的实测延迟，只写进记录作为估计 |

`pre_roll_s=4`、`still_s=5` 是测试值，不是已确认的项目参数。

## 输出

每个事件一个 `<event_id>.mp4` 和 `<event_id>.json`。JSON 记录运动时刻、请求窗口、实际片段起止、实际预录秒数、使用的分段、是否有断流、文件大小、SHA-256、时长和状态（`ok` / `partial` / `failed`）。运行日志为 `recorder.log.jsonl`。

所有时间都是 **ROCK 收到画面的系统时间**（Unix 秒），画面实际拍摄时间约早 `capture_latency_s`。ROCK 时钟需先[按 Mac 校准](../../experiments/2026-11-05-home-board-clock-set/README.md)，否则文件名和记录时间都会错。

## 测试

```sh
python3 -m unittest -v test_recorder
```

8 个逻辑测试不需要其他软件；1 个合成画面测试需要带 libx264 的 FFmpeg，用测试图案模拟摄像头，约 15 秒，检查预录长度、片段时长和完整解码。2026-11-05 已在 home 真实摄像头上用手动信号实测三种情形，见[实测记录](../../experiments/2026-11-05-home-recorder-manual-trigger/README.md)。

## 已知限制

- 分段的结束时间取分段文件的写入时间（最后一个包到达的时刻），开始时间取前一段的结束。早期版本按轮询时刻推算，拼接时会累积误差、截短片段结尾，已修复并加了回归测试，见[实测记录](../../experiments/2026-11-05-home-recorder-manual-trigger/README.md)。
- 断流后 FFmpeg 3 秒后重启，新旧分段分开存放；跨断流的事件会在 JSON `gaps` 中标出，拼接结果可能有跳变。
- 拼接在主循环里同步执行，长事件拼接期间新信号会稍晚处理（信号自带时间，不影响事件边界）。
- 没有做开机自启、SATA 输出、网页查看或运动检测。
