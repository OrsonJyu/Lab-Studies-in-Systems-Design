---
id: guide-node-red-mongodb-integration
type: guide
updated_on: 2026-11-21
status: proposal
aliases: [Node-RED dashboard, MongoDB, 实时画面接入, 录像入库, 数据库接入方案]
related: [D015, ws-preroll-recording]
---

# 摄像头数据接入 Node-RED dashboard 与 MongoDB（方案）

> **状态：建议方案，未实现、未测试，也不是已确认的决定。** 依据是 recorder 0.3（[`recorder.py`](../../project-camera/src/recorder/recorder.py)、[`webview.py`](../../project-camera/src/recorder/webview.py)）现有的接口。Node-RED 和 MongoDB 装在哪台机器上、dashboard 给谁看，都还没有确定（见文末）。

基本原则：**视频本身不放进 MongoDB，数据库只存描述视频的数据**，比如事件时间、守宫位置、文件在哪、SHA-256。视频照样以 MP4 文件存在硬盘上，Node-RED 通过 HTTP 去取。

```text
摄像头 ──RTSP──> ROCK 4C+ (recorder.py + webview.py :8080)
                   ├─ /live.mjpg    实时画面 ──────────────> Node-RED dashboard (img 标签)
                   ├─ /api/status   当前状态（约 0.5 秒更新）──> Node-RED ──> dashboard 文字、指标
                   ├─ /api/events   事件记录（JSON）─────────> Node-RED ──> MongoDB.events
                   └─ /clips/xxx.mp4 片段，可拖动 ───────────> dashboard 的 video 标签
Mac recordings/*.mp4 + *.json ──(文件监视/HTTP)──> Node-RED ──> MongoDB（更新文件位置）
```

## 1. 实时画面显示在 Node-RED dashboard 上

现有接口已经够用，recorder 不需要改。

- **画面**：在 dashboard 里放一个 `ui_template` 节点，写一个 img 标签指向 `http://<ROCK地址>:8080/live.mjpg`。浏览器原生支持这种 MJPEG 流，大约每秒 10 帧。Node-RED 本身不能直接播放 RTSP，所以不要让它直接连摄像头。
- **状态**：用 `inject` 节点每 1 秒触发一次，经 `http request` 读 `/api/status`，再接到文字或指标控件。可以显示的有：是否在录（`open_event`）、画面变化量（`detector.area_share`）、守宫状态和坐标（`tracker.state/x/y`）。
- **回放**：用 `/api/events` 生成列表，点一条就在 video 标签里播放 `/clips/<event_id>.mp4`。这个地址支持 Range，可以拖动进度条。
- 旧版 `node-red-dashboard` 和新版 FlowFuse Dashboard 2.0 都有 template 节点，两种都能用。

几点限制：

- 打开 dashboard 的浏览器必须能访问 ROCK。现在 ROCK 只在隔离交换机上，而且 `webview.py` 没有登录，不要为了这个把它接到校园网。
- dashboard 如果走 HTTPS，浏览器会拦掉 http 的画面（mixed content）。
- 每多一个观看来源，就多占摄像头一路 RTSP。所有观看者共用一个转码进程，这点没问题。

## 2. 实时数据能接到 MongoDB 吗？

能，存的是数据，不是视频流。建议分三个 collection：

| collection | 来源 | 频率 |
| --- | --- | --- |
| `events` | `/api/events`，每个事件一条，带运动时刻、片段起止、实际预录秒数、状态、SHA-256 | 每个事件一次 |
| `tracks`（建成 time-series） | 守宫的 `t / state / x / y` | 1 Hz |
| `status_changes` | 开始录、停止录、断流、环境变化这类状态变化 | 只在变化时写 |

**最省事的接法**：Node-RED 每 5–10 秒读一次 `/api/events`，按 `event_id` 做 upsert（重复读不会产生重复记录）。MongoDB 节点用 `node-red-contrib-mongodb4`。recorder 保持只用 Python 标准库，不用加 pymongo。以后要实时推送，再考虑让 recorder 发 MQTT，由 Node-RED 订阅后写库。

有两件事要先知道：

- **MongoDB 最好不要装在 ROCK 4C+ 上。** RK3399 是 ARMv8.0，而官方 MongoDB 5.0 及以后的 ARM 版本要求 ARMv8.2-A，在这块板上会直接 "Illegal instruction" 起不来。板上只能跑已经停止维护的 4.4，内存和 microSD 也不宽裕。建议 Node-RED 和 MongoDB 放在 Mac 或另一台服务器上。
- **守宫的 1 Hz 轨迹目前没有对外接口。** `recorder.py` 只把它写进板上的轨迹文件（`self.track_file`），`/api/status` 只给当前这一刻的位置。要完整存进 `tracks`，需要给 `webview.py` 加一个小接口，比如 `/api/track?since=`，或者改发 MQTT。这属于代码改动，按仓库规则要走分支加 PR。

## 3. 硬盘上的录像怎么让 Node-RED 和 MongoDB 读到

Node-RED 和 MongoDB 不去解析 MP4 的内容，它们读的是**每个 MP4 旁边的同名 `.json` 记录**，里面已经有时间、时长、SHA-256、状态。

1. **补录已有文件**：一次性扫描 `recordings/*.json`，用 `mongoimport` 或者一个 Node-RED flow 都行，全部 upsert 进 `events`。
2. **之后自动跟上**：Node-RED 的 `watch` 节点监视 `recordings/` 目录，出现新的 json 就读进来写库，同时写上 `video.location`（`rock` 或 `mac`）、`video.path` 和播放 URL。
3. **播放**：在 Node-RED 的 `settings.js` 里把 `httpStatic` 指向 `recordings/`，dashboard 就能用 `http://<Node-RED>:1880/xxx.mp4` 播放。还在 ROCK 上的片段继续用 `/clips/`。
4. **位置变化**：按 [D015](../DECISIONS.md)，视频核对哈希后会从 ROCK 移到 Mac，`/api/events` 里 `on_board` 会变成 `false`。Node-RED 看到这个变化时，就更新那条记录的 `video.location`，同一个 `event_id` 始终只有一条记录。

不建议用 GridFS 把 MP4 存进 MongoDB。数据库会迅速变大，备份和查询都会变慢，而且 webview 已经能提供拖动播放。

## 待确定

1. Node-RED 和 MongoDB 装在哪台机器上？是 Mac，还是别的小组或服务器的？这决定了上面的地址怎么填，以及隔离网络要不要开口子。
2. dashboard 只在实验网内看，还是要给别的组远程访问？如果要远程访问，就得先加登录或者加一层反向代理。

建议的第一步：Node-RED 先装在 Mac 上，做一个能导入的 flow.json，包括实时画面、状态、事件同步到 MongoDB、已有录像补录；这一步不需要改 recorder。之后再在分支上加轨迹接口。
