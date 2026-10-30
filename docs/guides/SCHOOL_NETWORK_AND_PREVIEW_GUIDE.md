---
id: guide-school-network-preview
type: guide
environment: school
updated_on: 2026-10-30
aliases: [校园环境复现, school 配置, 全有线, IINA, AP, 网络恢复]
related: [env-school, D013, exp-school-network-preview-20261030]
---

# 学校环境：接线、网络恢复与预览

本指南对应[学校环境档案](../../project-camera/environments/school/README.md)和[当日实验](../../project-camera/experiments/2026-10-30-school-network-preview/README.md)。最终通过的是 Mac 直接读取相机的有线预览；学校板卡录像、长期流畅性及重启自动恢复未验收。占位值必须填写，示例 JSON 不会自动配置网络。

## 1. 区分运行端和现场参数

- **Mac 终端**：提示符带 Mac 用户/主机名，执行 SSH、Mac 网口检查和 IINA。
- **ROCK 终端**：已 SSH 登录或在板卡本地控制台，执行 `ip`、`nmcli` 和板卡到相机检查。
- 在 ROCK 里再次 SSH 到自身，不证明 Mac 的有线管理已通。用 `echo "$SSH_CONNECTION"` 核对客户端与服务器地址。

按[字段示例](../../project-camera/environments/school/config.example.json)在忽略的 `.local/` 分别填写两端私有配置。本文使用的变量清单如下；密码和完整 RTSP URI 不放入这些环境变量文件。

| 变量 | 填写位置 / 含义 |
| --- | --- |
| `SD5531_MAC_ETH_IFACE` | Mac；当前 USB 以太网接口 |
| `SD5531_BOARD_USER` / `SD5531_BOARD_WIRED_HOST` | Mac；板卡实际账号和已验证的有线 SSH 地址 |
| `SD5531_CAMERA_HOST` | Mac 和 ROCK 各自填写；相机当前固定地址 |
| `SD5531_BOARD_ETH_IFACE` / `SD5531_BOARD_CAMERA_CIDR` | ROCK；有线接口和相机同网段未占用的板卡地址/前缀 |
| `SD5531_BOARD_WIFI_IFACE` | ROCK；当前无线接口 |
| `SD5531_AP_SSID` / `SD5531_AP_CIDR` | ROCK；自建热点名和独立 AP 地址/前缀，不与相机网段重叠 |

不要将 home/手机历史地址或旧 HostKeyAlias 当作通用值。SSH 主机密钥应与现场可信记录核对，不关闭密钥校验来消除告警。

## 2. 最终接线与 Mac 地址

需要四根数据网线：Mac 转接头到交换机、ROCK 到交换机、供电器 LAN 到交换机、供电器 POE 到相机。**POE 输出只连接匹配摄像头，LAN 数据口接交换机**。普通交换机不提供摄像头电源；ROCK 单独经 USB-C 供电。

本次由 Mac 给 ROCK 供电，但负载下供电稳定性未验收。官方列出 ROCK 4C+ Type-C 5V/3A 供电，供电与网络分开检查：[Radxa 说明](https://docs.radxa.com/en/rock4/rock4c%2B/getting-started/overview)。

有线网络保持独立，Mac Wi-Fi 可另接校园网。本次 macOS 拒绝共享 802.1X 来源连接；最终本地有线预览不需要互联网共享。

Mac“系统设置 → 网络 → 对应 USB 以太网接口 → 详细信息 → TCP/IP”：手动 IPv4，使用摄像头同网段的未占用 Mac 地址和正确掩码，路由器和 DNS 留空。不要与板卡或相机地址重复。在 Mac 私有终端变量填写后检查：

```sh
ifconfig "$SD5531_MAC_ETH_IFACE"
```

应为 `active` 且有正确地址。灯亮不证明目标已取得地址。本次为 100 Mbps 全双工，不由交换机规格推定每段均为千兆。

## 3. ROCK 配置与管理恢复

先通过仍可用的有线/无线 SSH 或本地显示器键盘登录，在 ROCK 记录：

```sh
echo "$SSH_CONNECTION"
ip -br addr
ip route
nmcli -f NAME,UUID,TYPE,DEVICE connection show
```

没有可用登录路径时，不能直接在 Mac 执行板卡 `nmcli`。先接回此前可用的 AP/热点，或使用本地控制台。IPv6 只有在本次发现、核对密钥并测试 SSH 后才能用；末次只有 ICMP 回应，不能计作 SSH 恢复。

本次已有 `school-camera`，核对实际配置后直接启用：

```sh
sudo nmcli connection up school-camera
ip -br addr show "$SD5531_BOARD_ETH_IFACE"
ip route get "$SD5531_CAMERA_HOST"
```

该连接本次为**手动启用**。重启/重新插线后重新检查，不重复创建同名配置。如果 profile 不存在，才首次创建；原有家庭 DHCP 配置保留。

```sh
sudo nmcli connection add type ethernet \
  con-name school-camera ifname "$SD5531_BOARD_ETH_IFACE" \
  connection.autoconnect no \
  ipv4.method manual ipv4.addresses "$SD5531_BOARD_CAMERA_CIDR" \
  ipv4.never-default yes ipv6.method link-local
sudo nmcli connection up school-camera
```

NetworkManager 管理静态地址；`ip addr add` 仅临时增加，可能在重新激活时被清理。本次出现过临时地址丢失。`never-default` 用于保留其他接口默认路由：[参数说明](https://networkmanager.dev/docs/api/1.42/nm-settings-nmcli.html)。

在 **Mac 新终端**登录，并在板卡核对 SSH 客户端来自 Mac 的有线地址：

```sh
ssh -o IPQoS=none "${SD5531_BOARD_USER}@${SD5531_BOARD_WIRED_HOST}"
```

`IPQoS=none` 是本次兼容性尝试，不是已证明的故障修复。末次板卡管理恢复仍待独立完成。

## 4. Mac 直接检查摄像头与 IINA

Mac 填写并导出当前私有相机地址后运行：

```sh
python3 - <<'PY'
import os
import socket
for port in (80, 554, 8899):
    try:
        with socket.create_connection((os.environ['SD5531_CAMERA_HOST'], port), timeout=3):
            print(f'{port}: connected')
    except OSError as exc:
        print(f'{port}: {type(exc).__name__}')
PY
```

8899 是这台相机本次的 ONVIF TCP 端口，不是统一标准端口；TCP 成功不等于 ONVIF 协议功能验收。

本次本地有线 IINA 入口从私有 JSON 读取相机原 RTSP URI，先用 ffprobe 检查视频，再由 IINA CLI 打开。实际入口未随仓库上传；其中密码、流地址和个人路径不进入共享文档、终端历史或 PR。

```text
IINA CLI 本次播放参数：
--no-stdin --separate-windows
--mpv-rtsp-transport=tcp --mpv-hwdec=no --mpv-audio=no
输入：从本机私有配置读取的相机 URI
```

IINA CLI 可传入 mpv 参数；RTSP/TCP 与软件解码含义见[mpv 手册](https://mpv.io/manual/stable/)。参数只作用于此次播放。本次码流为 H.264、2560 × 1440、报告 20 fps；预览不保存录像，关闭对应窗口即可停止观看。

检验顺序：端口 → 视频探测 → 短解码 → 实际画面。进程存在或“已启动”不能替代用户画面确认。用户最后确认有线 IINA 成功，长期流畅性仍待测。

## 5. 可选：ROCK 自建 AP 练习无线 SSH

这是学校已尝试成功的独立变体，不是最终有线预览的必需步骤。先保留真正的 Mac → ROCK 有线 SSH，检查 AP 支持和已有连接：

```sh
echo "$SSH_CONNECTION"
nmcli -f WIFI-PROPERTIES.AP device show "$SD5531_BOARD_WIFI_IFACE"
nmcli -f NAME,TYPE,DEVICE connection show
```

AP 为 yes 时继续。本次已有 `rock-lab-ap`，读取后复用，不重复创建。以下**首次创建**步骤只用于该 profile 不存在的情况：

```sh
sudo nmcli connection add type wifi \
  ifname "$SD5531_BOARD_WIFI_IFACE" con-name rock-lab-ap \
  ssid "$SD5531_AP_SSID" wifi.mode ap wifi.band bg \
  wifi-sec.key-mgmt wpa-psk wifi-sec.proto rsn \
  ipv4.method shared ipv4.addresses "$SD5531_AP_CIDR" \
  ipv4.never-default yes ipv6.method disabled connection.autoconnect no
sudo nmcli --ask --wait 30 connection up rock-lab-ap
```

启用已有 profile 只执行最后一行，按提示在终端输入热点密码。秘密参数交互见[NetworkManager 手册](https://manpages.debian.org/bookworm/network-manager/nmcli.1.en.html)。Mac 加入热点后新开终端 SSH 到板卡 AP 地址，核对客户端来自 AP 网段，再决定移动管理网线。

本次内置无线接口在手机热点客户端与 AP 模式之间切换，不假定两者可同时工作。AP 没有验收互联网，Mac 加入后可能暂时无法访问网络聊天；测试后可切回外网发结果。

```sh
sudo nmcli connection down rock-lab-ap
```

停止 AP 前保留其他实际可用的管理路径。

## 6. 故障定位与迁移验收

| 观察 | 下一步 |
| --- | --- |
| 网口 inactive / 无载波 | 检查电源、网线、端口与板卡启动 |
| 灯亮但没有 IPv4 | 检查 NetworkManager profile；普通交换机不会自动提供 DHCP |
| 相机邻居可达、ping 来源却为 Wi-Fi | 检查有线地址是否丢失，启用正确的静态 profile |
| 旧热点地址 SSH 超时 | 核对两端当前网络和 DHCP 地址，不沿用旧值 |
| 启动器退出，播放器仍运行 | 分别检查进程、解码和画面，不能只看终端状态 |
| Mac 有线预览成功但 ROCK 不可达 | 分别验收视频与板卡管理，恢复管理后再测试录像 |

恢复后核对实际接口/地址、默认路由、SSH 来源、相机端口、画面、板卡存储和时间源。持久录制、SATA、时钟校准、预录制和长期故障恢复仍是独立任务。
