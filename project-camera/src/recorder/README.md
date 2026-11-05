# 滚动缓存事件录制 / Rolling-buffer recorder

版本：`recorder/0.3`（帧差运动检测 + 手动触发 + 局域网网页）。运行在 ROCK 4C+：Debian 12、Python 3.11（只用标准库）、FFmpeg 5.1。工作流见 [ws-preroll-recording](../../../docs/workstreams/active/ws-preroll-recording.md)。

## 做什么

1. FFmpeg 不重新编码，把摄像头主码流切成约 2 秒一段的 MPEG-TS，写进内存盘 `/dev/shm`，不磨损系统卡。
2. 收到“有运动”的信号就开启事件；**连续 `still_s` 秒没有新的运动信号就结束**；结束前又有运动则续接同一事件。
3. 事件结束后，取“第一次运动前 `pre_roll_s` 秒”到“结束”之间的分段，直接拼成 MP4，连同一份 JSON 记录存到 `output_dir`。
4. 超出 `ring_seconds` 且没有事件需要的分段自动删除。

运动信号有两个来源，进入同一套事件逻辑：

- **运动检测**（`motion.enabled: true`）：第二个 FFmpeg 进程读取子码流，每秒取 10 帧缩小为 160×90 灰度，与上一帧比较，灰度变化超过 `pixel_threshold` 的像素记为"变了"，每帧输出给 Python 判断。规则依次是：
  1. **检测区域**：只看网页上画出的区域（多边形，一般点饲养箱的 4 个角）；没画就看整幅画面。`mask` 中的区域（摄像头日期和名称）始终不算。
  2. **环境变化**：整幅画面有 `global_fraction`（30%）以上的像素同时变化，视为开关灯、自动曝光或红外切换，不算运动，只在时间轴上记一条"环境变化"；之后 `scene_cooldown_s` 秒内等画面稳定，也不算。
  3. **大小**：区域内的变化按相连的像素分块；最大一块小于 `min_blob_px` 是噪点，大于区域面积的 `max_blob_fraction` 视为手或人探进来，都不算。
  4. **持续**：符合条件的帧要持续 `persist_s` 秒（允许中间断 `max_gap_frames` 帧）才算运动；事件开始时间取这段的第一帧，触发前保留不受影响。

  每 `stats_every_s` 秒在日志中记录各种判断的帧数，便于调参数。
- **在网页上设置检测区域**：点"设置检测区域"，画面换成一张静止截图，依次点出饲养箱的角（3–12 个点），点"保存"。区域写入 `motion.roi_file`，录制程序约 1 秒内改用新区域，不用重启。之后实时画面上一直叠着半透明的区域框，摄像头被碰歪时能看出来；检测到运动时，运动的那一块用红框标出。也可以在配置的 `motion.roi` 里直接写点的坐标（按画面比例），作为后备。
- **手动信号**（`trigger` 命令），用于测试或人工标记。

帧差法只看画面变化，不识别物体：物体停住后事件照常按 `still_s` 结束，再动时开新事件（定位并锁定静止的守宫是下一步）。大小和持续参数是按替代场景（玩具）设的初始值，未在守宫场景验证，见[手挥动实验](../../experiments/2026-11-05-home-motion-hand-test/README.md)。

为什么要缓存而不是检测到再开始录：见 [延迟实验](../../experiments/2026-11-05-home-latency/README.md)，触发后才连接摄像头，第一帧比触发晚约 0.4 秒，FFmpeg 约 2 秒后才开始输出。

## 网页

[webview.py](webview.py) 在局域网提供一个页面（Python 标准库，无外部前端依赖）：

- **实时画面**：子码流转为 MJPEG，约每秒 10 帧；有人观看时才启动转码，无人观看 10 秒后停止。浏览器标签页切到后台时自动断开。
- **当前状态**：是否正在录制、本次开始时刻、最近一次运动、画面变化量（与阈值对比）、缓存长度；板卡时间与浏览器所在电脑相差超过 2 秒时提示先校时。
- **时间轴**：每个已保存的片段是一个标记，上方标出检测到运动的时刻（时:分:秒）；浅色部分为触发前保留的画面，红色闪烁的是正在录制的事件。可切换 10 分钟 / 1 小时 / 6 小时 / 24 小时。点击标记播放该片段并显示详细时间。
- **片段列表**：按时间倒序，点击行同样可以播放；支持拖动进度条（HTTP Range）和下载。

录制程序每 0.5 秒把状态写入 `ring_dir/state.json`，网页读取它；两个程序互相独立，网页停掉不影响录制。

```sh
python3 webview.py --config ~/sd5531/recorder/config.json
```

**没有登录或加密。** `web.bind` 默认只监听 `127.0.0.1`；在实验网使用时设为 ROCK 有线地址，只在隔离的实验交换机上可访问，不要绑定到连外网或校园网的接口。实时画面会占用摄像头的第三路 RTSP 连接。

| 键 | 默认 | 含义 |
| --- | --- | --- |
| `web.bind` | `127.0.0.1` | 监听地址 |
| `web.port` | 8080 | 端口 |
| `web.live_fps` / `web.live_width` | 10 / 800 | 实时画面帧率与宽度 |
| `web.idle_stop_s` | 10 | 无人观看多少秒后停止转码 |

## 日常启动和停止

ROCK 上 `~/sd5531/recorder/` 放着 [start.sh](start.sh) 和 [stop.sh](stop.sh)：

```sh
~/sd5531/recorder/start.sh   # 启动录制和网页；已经在运行就不重复启动
~/sd5531/recorder/stop.sh    # 停止二者；正在录的事件会以 partial 保存
```

用户的 Mac 上另有两个双击脚本（在 `Video_SD5531/live-preview/`，读取本机私有网络配置，不在仓库里）：

- **开始录制.command**：连接 ROCK（需要时输入密码）→ 检查板卡时间，相差超过 1 秒就先运行校时 → 检查摄像头时间（画面左上角），相差超过 1 秒就用 [cam_time.py](cam_time.py) `set` 按 ROCK 时间设置并读回核对 → 运行 `start.sh` → 打开网页 → 窗口开着期间每 10 秒把新片段**移到** Mac 的 `Video_SD5531/recordings/`。关闭窗口后 ROCK 继续录制，新片段暂存在 ROCK 上，等下次打开窗口或停止录制时再移走。
- **停止录制.command**：运行 `stop.sh`，再移走最后的片段。

摄像头没有断电保持时间的能力（[学校记录](../../experiments/2026-11-05-school-recorder-first-run/README.md)），所以每次开始录制都检查。

转存通过 SSH 进行（ROCK 上没有 rsync）：每段视频先复制到 Mac，按其 JSON 记录里的 SHA-256 核对一致后，才删除 ROCK 上的 MP4；核对不符时 ROCK 上的原片保留，下次重试。几 KB 的 JSON 记录留在 ROCK 上，网页时间轴仍显示该事件，并注明视频已存到 Mac（`/api/events` 的 `on_board` 为 `false`）。Mac 上的文件不会被删除。视频在 ROCK 上最多停留到下一次转存（窗口开着时约 10 秒）。
`recordings/` 在 Git 仓库之外：片段里可能有房间和人物，不提交到 GitHub。

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
| `motion.enabled` | false | 是否启用运动检测 |
| `motion.source_config` | `~/sd5531/private/camera_substream.json` | 子码流地址（板卡私有文件，不进仓库） |
| `motion.pixel_threshold` | 25 | 灰度变化超过多少算一个像素“变了” |
| `motion.roi_file` | `~/sd5531/roi.json` | 网页保存的检测区域 |
| `motion.roi` | 无 | 后备检测区域：`[[x, y], …]`，按画面比例；`roi_file` 存在时以它为准 |
| `motion.global_fraction` | 0.30 | 整幅画面变化超过这个比例算环境变化 |
| `motion.scene_cooldown_s` | 2.0 | 环境变化后多少秒内不判断运动 |
| `motion.min_blob_px` | 4 | 最大变化块小于多少像素（160×90 画面上）算噪点 |
| `motion.max_blob_fraction` | 0.35 | 最大变化块超过检测区域的多少比例算"太大" |
| `motion.persist_s` | 0.5 | 运动要持续多少秒才算 |
| `motion.max_gap_frames` | 1 | 持续期间允许中断的帧数 |
| `motion.mask` | 日期、名称区域 | 不参与检测的矩形，`[x, y, w, h]`，按画面比例 |

`pre_roll_s=4`、`still_s=5` 是测试值，不是已确认的项目参数。

## 输出

每个事件一个 `<event_id>.mp4` 和 `<event_id>.json`。JSON 记录运动时刻、请求窗口、实际片段起止、实际预录秒数、使用的分段、是否有断流、文件大小、SHA-256、时长和状态（`ok` / `partial` / `failed`）。运行日志为 `recorder.log.jsonl`。

所有时间都是 **ROCK 收到画面的系统时间**（Unix 秒），画面实际拍摄时间约早 `capture_latency_s`。ROCK 时钟需先[按 Mac 校准](../../experiments/2026-11-05-home-board-clock-set/README.md)，否则文件名和记录时间都会错。

## 测试

```sh
python3 -m unittest -v test_recorder test_webview
```

`test_recorder`：10 个逻辑测试不需要其他软件；4 个需要 FFmpeg（合成画面需 libx264）：检测滤镜能测出变化、遮罩区域被忽略、手动触发全流程、运动检测自动开关事件的全流程，共约 30 秒。`test_webview`：Range 解析、文件名白名单，以及启动服务后检查页面、接口、片段分段读取和实时 MJPEG 帧率，约 5 秒。2026-11-05 已在 home 真实摄像头上实测：[手动信号三种情形](../../experiments/2026-11-05-home-recorder-manual-trigger/README.md)、[运动检测手挥动四个事件](../../experiments/2026-11-05-home-motion-hand-test/README.md)。

## 已知限制

- 分段的结束时间取分段文件的写入时间（最后一个包到达的时刻），开始时间取前一段的结束。早期版本按轮询时刻推算，拼接时会累积误差、截短片段结尾，已修复并加了回归测试，见[实测记录](../../experiments/2026-11-05-home-recorder-manual-trigger/README.md)。
- 断流后 FFmpeg 3 秒后重启，新旧分段分开存放；跨断流的事件会在 JSON `gaps` 中标出，拼接结果可能有跳变。
- 拼接在主循环里同步执行，长事件拼接期间新信号会稍晚处理（信号自带时间，不影响事件边界）。
- 运动检测阈值只针对手挥动标定；光线变化、夜视切换未测。
- 网页不能往回拖看缓存中尚未成为事件的画面，只能看已保存的片段。
- 没有做开机自启或 SATA 输出；ROCK 重启后需重新运行 `start.sh`（或双击“开始录制”）。
