# 测试环境与共用配置

环境命名保留 [D011](../../docs/DECISIONS.md)；2026-11-05 用户按 [D014](../../docs/DECISIONS.md)统一 home/school 有线接法和配置。环境标签记录地点，不再决定另一套地址或板卡 profile。

Mac、ROCK、摄像头数据端接同一独立交换机，Mac Wi-Fi 只负责外网。共用 profile 为 lab-wired，自动连接、优先级 100；日常不依赖 ROCK 无线、DHCP 或发现服务。

| 环境 | 当前证据与限制 | 入口 |
| --- | --- | --- |
| home | 历史短录/预览；11-05 SD 恢复、共用配置和正常重启后自动 SSH/短解码通过 | [home](home/README.md) |
| school | 10-30 网络/AP/有线预览及后来板卡短录通过；新 lab-wired 基线待现场复测 | [school](school/README.md) |
| hotspot | 通用独立环境仍预留；可作为 Mac 外网，实际组合需单独验证 | [统一指南](../../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md) |

唯一可执行配置字段见[共用模板](../src/network/config.example.json)；复制到忽略的 `.local/wired-lab.json`，真实值只保留这一份。home/school 下的 JSON 只是同一规范的索引，不应各复制一套参数。密码与流 URI 另存私有配置，完整网络备份不上传。

每天按[统一指南](../../docs/guides/SHARED_WIRED_NETWORK_GUIDE.md)运行[只读检查器](../src/network/README.md)，只改 --environment 标签。检查失败先定位地址、路由、重叠、主机身份和自动连接，程序不会自动修改地址或替换连接。Wi-Fi/VPN 与实验子网发生重叠时需协调地址规划，不能保证任意网络天然不冲突。

每次实验的 front matter / JSON 保留实际环境，记录接收端、存储、时间源、版本和适用范围。学校旧热点变体不是通用 hotspot 的证明；home 新配置验收也不是学校现场复测。机器可读索引见 [registry.json](registry.json)。
