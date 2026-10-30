# 摄像头项目源码 / Source

本目录存放摄像头录制系统的代码与配置（接收、分段、事件控制、保留与清理、元数据）。当前工作流见 [ws-preroll-recording](../../docs/workstreams/active/ws-preroll-recording.md)。

**状态：通用录制服务尚未实现。** 2026-10-30 在 `home` 通过 FFmpeg 命令和临时 Python 操作完成短录像，并在 Mac 用 FFplay 预览；同日后续 `school` 有限网络/AP 与 IINA 预览另行记录，最终有线视频直达 Mac，未完成学校录像。可复核的命令与结果见[实验目录](../experiments/README.md)。这证明有限链路可运行，不等于已有分段、事件控制、清理或重启恢复服务。

当前双击预览入口与带访问参数的流配置保存在用户本地，不把其中的机器路径、地址或密码硬编码进仓库。环境字段示例见[测试环境](../environments/README.md)，目前没有程序加载该示例或自动切换环境。

## 约定

- 按组件分子目录，例如 `capture/`（FFmpeg 命令或脚本）、`controller/`（事件与保留逻辑）、`config/`。目录在需要时再建。
- 每个组件的 README 写明：用途、运行环境与版本（ROCK 4C+ 系统、FFmpeg、Python/Node-RED）、运行方法、已知限制。
- 只提交示例配置（如 `config.example.yaml`）。**摄像头密码、RTSP 带凭据的地址、token 不进仓库**；`.env` 已被忽略。
- 代码能运行不等于实测通过：实测结果写进 [experiments](../experiments/README.md)，并注明所用提交。
- 代码改动走工作分支和 PR，见 [CONTRIBUTING](../../CONTRIBUTING.md)。
