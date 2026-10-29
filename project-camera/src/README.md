# 摄像头项目源码 / Source

本目录存放摄像头录制系统的代码与配置（接收、分段、事件控制、保留与清理、元数据）。当前工作流见 [ws-preroll-recording](../../docs/workstreams/active/ws-preroll-recording.md)。

**状态：目前为空。** 已收集资料中没有摄像头录制的实现代码。

## 约定

- 按组件分子目录，例如 `capture/`（FFmpeg 命令或脚本）、`controller/`（事件与保留逻辑）、`config/`。目录在需要时再建。
- 每个组件的 README 写明：用途、运行环境与版本（ROCK 4C+ 系统、FFmpeg、Python/Node-RED）、运行方法、已知限制。
- 只提交示例配置（如 `config.example.yaml`）。**摄像头密码、RTSP 带凭据的地址、token 不进仓库**；`.env` 已被忽略。
- 代码能运行不等于实测通过：实测结果写进 [experiments](../experiments/README.md)，并注明所用提交。
- 代码改动走工作分支和 PR，见 [CONTRIBUTING](../../CONTRIBUTING.md)。
