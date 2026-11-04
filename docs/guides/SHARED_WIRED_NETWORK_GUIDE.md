---
id: guide-shared-wired-network
type: guide
updated_on: 2026-11-05
aliases: [共用配置, 家庭学校统一网络, lab-wired, 开机失联, 网络恢复]
related: [D014, env-home, env-school, ws-preroll-recording]
---

# home / school 共用有线基线

按用户 2026-11-05 的决定，两地点采用同一有线实验网络；变化的是 Mac 的 Wi-Fi 外网。[D014](../DECISIONS.md)取代旧的地点专用地址/手动切换工作方式；环境标签仍保留，用来限定证据。

## 一套接线

```text
Mac USB 网卡 ──────── 普通交换机 ──────── ROCK 网口
                         │
                   PoE 供电器 LAN
                   PoE 供电器 POE ── 摄像头

Mac Wi-Fi ── 家中 / 学校 / 手机热点：只承担 Mac 外网
```

实验交换机只接上述三个数据端，不上联家庭路由器、校园墙口或其他 DHCP 网络。用户已确认本次如此接线。供电器 POE 输出只接匹配摄像头；交换机不供 PoE，ROCK 单独供电。USB-C 供电线不作为本次 SSH 网络。

## 唯一配置来源

共用的[JSON 字段](../../project-camera/src/network/config.example.json)填入忽略的 `.local/wired-lab.json`，由[只读检查器](../../project-camera/src/network/README.md)加载。真实参数留本地；本仓库不发布当前地址、SSID、UUID、主机密钥、密码、流 URI 或个人路径。

| 对象 | 固定规则 | 换地点时 |
| --- | --- | --- |
| Mac 有线 | 一个固定 IPv4/前缀，网关和 DNS 留空 | 保持 |
| ROCK 有线 | 同网段另一个固定 IPv4；`lab-wired` 自动连接、优先级 100、无有线默认路由 | 保持 |
| 摄像头 | 同网段第三个固定 IPv4 | 保持 |
| Mac Wi-Fi | 独立外网，可按地点连接不同 Wi-Fi | 只在 Mac 切换 |
| ROCK 无线 | 保存为手动维护/备用，默认不承担管理主通道 | 日常不切换 |

先核对三个地址不同、同网段、前缀一致且不是网络/广播地址。无需把摄像头改成 Wi-Fi 地址，也不依赖校园客户端互通。遇到 Mac Wi-Fi 与实验子网重叠，先停止该场地验收，协调一次完整地址规划；不能只改一台设备或假定所有网络永不冲突。

## 已有板卡迁移一次即可

先保留已验证的管理连接，核对已有连接的 UUID、接口、固定地址和主机身份。2026-11-05 的实机迁移保留了原 `school-camera` UUID 和地址，只改成通用名称并明确自动连接策略。不要反复创建同名 profile。

以下在 **ROCK 终端**执行，填入实际已核验的 UUID；不是 Mac 命令：

```sh
nmcli -f NAME,UUID,TYPE,DEVICE connection show
nmcli -g connection.interface-name,ipv4.addresses connection show uuid '<EXISTING_VERIFIED_UUID>'
sudo nmcli connection modify uuid '<EXISTING_VERIFIED_UUID>' \
  connection.id lab-wired connection.autoconnect yes \
  connection.autoconnect-priority 100 ipv4.never-default yes
```

这段不设置新 IP、不创建新 UUID。若实际地址与私有 JSON 不符，先核对现场；不要在唯一的远程管理通道上试探性替换地址。配置文件名可能保留历史名称，以 UUID 和 `connection.id` 识别实际连接。

对已有无线备用 profile，逐一按已核验 UUID设置手动启用，保留配置与凭据：

```sh
sudo nmcli connection modify uuid '<OPTIONAL_WIFI_PROFILE_UUID>' connection.autoconnect no
```

本次三份无线 profile 均为手动；没有删除它们，也没有用关闭全局网络或 Wi-Fi 射频来实现有线管理。ROCK 自建 AP 是维护选项，不是默认救援入口；未自动启用的 AP 不能被当成重启后必然可用的通道。

首次换硬件时先建立并验证管理入口，再按新设备生成固定地址配置；不能把旧 UUID、网口名或密钥直接复制过去。新 profile 的创建不由检查器自动执行。

## 每次移动与开机

1. 三个数据端接交换机；确认实验交换机没有外部上联。连接匹配电源后开机。
2. Mac 有线服务保持私有 JSON 中的固定地址；Wi-Fi 连接当前地点外网。
3. 使用同一个配置文件运行检查器，仅改变实验环境标签：

```sh
python3 project-camera/src/network/check_network.py \
  --config .local/wired-lab.json --environment home \
  --remote --interactive --report .local/home-network-check.json
```

4. 全部通过后才进行录像实验。报告只证明其中列出的检查，不证明实际画面或持续录制。学校采用同样配置，但需在学校现场再运行并另存 `school` 报告。

需要单独登录时，在 Mac 填入私有配置中的值：

```sh
ssh -o StrictHostKeyChecking=yes -o HostKeyAlias='<TRUSTED_HOST_NAME>' \
  '<LOGIN_USER>@<BOARD_WIRED_IPV4>'
```

旧 `HostKeyAlias` 仅用于沿用可信公钥记录，不是连接目标。目标始终是固定有线地址。密钥不匹配时先核验设备，不关闭校验或自动删除记录。

## 避免再次失联

- `lab-wired` 必须保存 `autoconnect=yes`；手动 `connection up` 成功不等于开机恢复已通过。
- 更改连接名称时保留 UUID；修改后检查实际活动 UUID、固定地址和自动连接。不要通过新增多份冲突的有线配置来“修复”。
- 对一次正常系统重启做实测：在 ROCK 正常执行 `sudo systemctl reboot`，等待重新可达，再运行同一检查器。网络检查器不会替你重启或改变连接。
- 关机在 ROCK 执行 `sudo systemctl poweroff`，完成关机后再断电。失联时优先查物理链路、地址/ARP、设备启动和网络状态；网口灯或千兆协商不能证明 Linux 已正常运行。
- `ifupdown` 段的 `managed=false` 仅影响其接口定义；不是“关闭所有网络”。`ipv6.method disabled` 在旧 AP 配置中也不是关闭 Wi-Fi 的命令。
- 有线局域网不依赖互联网。ROCK 需要软件更新/联网校时时，可在保留有线管理的条件下临时启用已核验的无线维护连接；完成后恢复手动策略，不替换主有线配置。
- 流畅性、OSD/板卡时钟和包时间戳单独验收；本次网络恢复不等于这些问题已解决。

## 旧配置的去向

| 历史项 | 当前处理 |
| --- | --- |
| 原 home DHCP 管理地址 | 不作为日常入口；旧快捷入口改读共用配置 |
| `ip addr add` 摄像头网段辅助地址 | 历史临时测试，不再用于日常持久管理 |
| `school-camera` + 不自动连接 | 同一 UUID 迁移为 `lab-wired`，自动连接开启 |
| 电脑/iPhone Wi-Fi 与 `rock-lab-ap` | 保留私有配置，手动备用，不承诺开机自启 |
| home/school 各自示例 | 指向同一规范；地点只标注实验结果 |

原[home 教程](HOME_HARDWARE_AND_EXPERIMENT_GUIDE.md)的录像、ONVIF、解码步骤仍可参考；其中旧 DHCP/临时辅助地址章节仅解释当时实验。原[school 教程](SCHOOL_NETWORK_AND_PREVIEW_GUIDE.md)保存热点探索与历史恢复步骤，日常网络以本指南为准。

## 本次 SD 恢复的边界

2026-11-05 发现唯一持久有线 profile 为手动启用，同时 ext4 有待恢复日志。Mac 内置读卡器将卡标为 `internal`，仅查 external 会漏检；Linux 分区未在 Finder 显示也不是坏卡证据。

离线过程先核对介质身份并备份网络文件和文件系统元数据，再使用标准工具与撤销记录恢复日志、修改一行并校验权限/内容/文件系统。备份不是完整逐字节整卡镜像。针对个人设备的原始 profile、密钥、截图、元数据镜像、撤销文件及有写卡能力的本机脚本不上传。

不要把含 `needs_recovery` 的分区直接当成完全干净的文件系统，也不要复制通用原始磁盘写入命令；离线恢复需要针对已核验且未挂载的介质。已确认的网络自启缺陷和日志恢复都参与了此次修复，没有做单变量排除实验。

规范依据：[NetworkManager profile](https://networkmanager.dev/docs/api/1.42/nm-settings-nmcli.html)、[NetworkManager 全局配置](https://networkmanager.dev/docs/api/1.42/NetworkManager.conf.html)、[e2fsck](https://manpages.debian.org/bookworm/e2fsprogs/e2fsck.8.en.html)。实测见[恢复与统一验收](../../project-camera/experiments/2026-11-05-home-wired-recovery/README.md)。
