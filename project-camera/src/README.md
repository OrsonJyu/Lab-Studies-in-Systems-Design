# 摄像头项目源码 / Source

本目录存放摄像头录制系统的代码与配置（接收、分段、事件控制、保留与清理、元数据）。当前工作流见 [ws-preroll-recording](../../docs/workstreams/active/ws-preroll-recording.md)。

**状态：[滚动缓存事件录制](recorder/README.md)（0.2，帧差运动检测 + 手动触发）已实现并在 home 实测；开机自启和长期运行尚未实现，运动阈值未在守宫场景验证。** 以下为此前状态： home/school 的短录来自临时 FFmpeg/Python 命令。11-05 新增[只读网络检查器](network/README.md)，加载一份私有 JSON，已在 home 验证；它不是录制程序。

当前统一网络为自动连接的 lab-wired，home 正常重启通过；学校现场复测仍待完成。实验见[目录](../experiments/README.md)，操作见[统一指南](../../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md)，接续参数见[上下文](../../docs/handoffs/2026-11-05-shared-wired-baseline.md)。实际地址/接口/UUID、凭据和流配置保存在忽略的私有文件；网络示例由检查器加载，旧每地点 JSON 仅为规范索引。

## 约定

- 按组件分子目录，例如 `capture/`（FFmpeg 命令或脚本）、`controller/`（事件与保留逻辑）、`config/`。目录在需要时再建。
- 每个组件的 README 写明：用途、运行环境与版本（ROCK 4C+ 系统、FFmpeg、Python/Node-RED）、运行方法、已知限制。
- 只提交示例配置（如 `config.example.yaml`）。**摄像头密码、RTSP 带凭据的地址、token 不进仓库**；`.env` 已被忽略。
- 代码能运行不等于实测通过：实测结果写进 [experiments](../experiments/README.md)，并注明所用提交。
- 代码改动走工作分支和 PR，见 [CONTRIBUTING](../../CONTRIBUTING.md)。
