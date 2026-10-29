---
id: exp-home-live-preview-20261030
type: experiment
environment: home
workstream: ws-preroll-recording
roadmap_stage: 1
---

# home · Mac 实时预览

日期：2026-10-30（香港）。目标：用户能在 Mac 看到摄像头持续更新的画面。环境、供电和网络见 [home](../../environments/home/README.md)。

## 方法与结果

- ROCK 从摄像头获取 RTSP 视频；Mac 经 SSH 将摄像头 RTSP 端口转发到仅监听 `127.0.0.1` 的本机端口。
- 先检查转发后的 RTSP 服务，ffprobe 成功读取 2560 × 1440 的 H.264 视频流。
- 最初 IINA 与通道建立连接，但用户没有看到画面，不能据此标为预览成功。
- 改用 Mac 已安装的 FFplay 8.0.1，RTSP/TCP，关闭音频，显示 960 × 540 的独立窗口。用户明确回复：**“看到了，画面在更新”**。
- 本地启动入口的“已运行”检测随后执行通过，没有重复启动第二个 FFplay 窗口。

结论：**本次 `home` 条件下，用户确认实时预览通过**。这不是自动录制，未测量端到端延迟，也没有证据说明其他网络环境可用。

## 复现形式

以下是变量占位形式；现场需填当前环境参数。建立 SSH 转发时仍使用原有板卡登录授权，不新增公网服务：

```sh
ssh -N -o ExitOnForwardFailure=yes \
  -L "127.0.0.1:${LOCAL_PORT}:${CAMERA_HOST}:554" "${BOARD_USER}@${BOARD_HOST}"
ffplay -hide_banner -nostats -rtsp_transport tcp -an \
  -window_title 'SD5531 Live Camera' -x 960 -y 540 "$PRIVATE_FORWARDED_RTSP_URI"
```

`$PRIVATE_FORWARDED_RTSP_URI` 是 ONVIF 返回的原流 URI 在本机转发地址上的对应 URI，仍可能包含访问参数，不写入文档或命令历史。现有本地双击启动文件绑定 `home` 的私有配置，未作为通用跨环境程序发布。

原始[短录像及抽帧证据](../2026-10-30-home-camera-recording/README.md)支持视频输入能力；本项预览结论另由进程/连接检查和用户确认支持，未录制或上传桌面画面。

## 限制与持续性

ROCK 的摄像头网段辅助地址与 Mac 本地转发均为本次会话配置，尚未持久化。更换网络或重启后需要重新发现地址、检查互通并建立连接。学校网络隔离和热点接入仍待独立实测。

贡献记录：助手建立、检查连接并提供本地入口，用户观察播放器并确认动态画面。未据此分配其他组员贡献或认定课程验收完成。

本项的结构化[结果](result.json)记录用户确认及限制；[来源与校验](manifest.json)记录对应文件。
