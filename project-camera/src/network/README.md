# 共用有线网络检查器

版本：`shared-wired-preflight/1`。Python 3.9+，macOS 客户端；ROCK 为使用 NetworkManager 的 Debian。它读取私有 JSON 检查网络，不部署网络、不改地址、不启用/关闭连接、不修改 known_hosts、不启动录像。

home / school 共用同一份私有配置；`--environment` 只标记观测地点。接线和首次迁移见[统一指南](../../../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md)。

在仓库根目录复制并填写[示例](config.example.json)：

```sh
mkdir -p .local
chmod 700 .local
cp project-camera/src/network/config.example.json .local/wired-lab.json
chmod 600 .local/wired-lab.json
```

填写后将 `example_only` 改为 `false`。使用现场已核验的地址、网卡、已有连接 UUID 与可信主机密钥别名；占位符不能运行。JSON 不保存密码或流 URI，不提交 `.local/`。

```sh
python3 project-camera/src/network/check_network.py \
  --config .local/wired-lab.json --environment home \
  --remote --interactive --report .local/home-network-check.json
```

到学校只把 `--environment home` 改为 `--environment school`，配置文件保持同一份。SSH 如需密码，在调用者终端交互输入；无人值守调用可使用已认证的 `--ssh-control-path` 或正常 SSH 密钥。该工具不创建会话通道，不读取摄像头私有流配置。没有认证时远端状态记为 `warn`，不能把 TCP 成功当成自动连接验收。

检查内容：静态地址/掩码、有效载波、Mac Wi-Fi 网段重叠、目标实际有线路由、SSH/RTSP/ONVIF TCP 端口、原可信主机密钥，以及远端活动 UUID、自动连接、优先级、地址、路由和无线备用配置的手动策略。实际 SSH 继续使用严格主机密钥检查；远端探测为只读 `nmcli` / `ip`。

报告不含实际地址、SSID、UUID、密钥或 URI；本地输出文件权限为 0600。退出码 `0` 为全部检查通过，`1` 为配置或连通性失败，`2` 为仅有未完成项。它不验证视频解码、录像、延迟、真实重启、长期稳定或镜头时钟；这些另建实验。

默认会检测有线地址与 Mac Wi-Fi 地址范围的重叠，并检查两个目标路由。VPN 的所有策略不由本程序穷举；路由/连通异常应保留现场结果，不能直接归因于某个代理。

```sh
python3 -m unittest discover -s project-camera/src/network -p 'test_*.py' -v
```

测试覆盖重复/不可用地址、掩码不一致、非 RFC1918 地址、旧 profile 名、占位符、命令字段、可信密钥比较和 Wi-Fi 网段重叠。硬件结果见[home 恢复与统一验收](../../experiments/2026-11-05-home-wired-recovery/README.md)。
