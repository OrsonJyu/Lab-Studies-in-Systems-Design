---
id: guide-demo-one-command
type: guide
workstream: ws-preroll-recording
roadmap_stage: 1
aliases: [一键安装, 一键运行, demo 安装, 守宫录像演示, demo.py, setup.command, start.command, run the demo, install the demo]
related: [ws-preroll-recording, exp-school-gecko-trigger-20261105, exp-school-gecko-tracker-colour-20261105]
---

# 守宫录像 demo：在任意主机上一键安装和运行

这份说明让你在**另一台电脑**上，接上**同一套硬件**（ROCK 4C+、IP 摄像头、隔离交换机），用一条命令完成安装和检查，再用一条命令开始录制。做完后的功能和 2026-11-05 学校现场验收的一致：

- 摄像头画面先进入 ROCK 上 60 秒的滚动缓存；
- **锁定的守宫移动时才录**（手在区域里动、人走动、开关灯都不录），每段保留触发前约 4 秒，守宫静止 5 秒后结束；
- 网页上看实时画面、画检测区域、看守宫的绿框和轨迹、在时间轴上点开每一段录像；
- 录好的片段核对 SHA-256 后**移到这台主机**的 `recordings/` 文件夹，ROCK 上不留视频。

> English summary for agents and visitors is at the [end of this page](#for-agents-and-english-readers).

## 1. 准备

**主机**：macOS 或 Linux，有一个有线网口（USB 转网口也可以），装有 Python 3.9+ 和 `ssh`（macOS 自带；若提示安装命令行工具，按提示装即可）。不需要装 FFmpeg。Windows 暂不支持。

**硬件**（与原项目相同）：

| 设备 | 说明 |
| --- | --- |
| ROCK 4C+ | Debian 12，已装 Python 3 和 FFmpeg；用 5V 3A 以上的 USB-C 电源（2026-11-05 学校出现过两次轻负载下突然断电，疑似供电不足） |
| IP 摄像头 | GK7205V200 方案，ONVIF；主码流 2560×1440、子码流 800×448；由 PoE 供电器供电 |
| 交换机 | 隔离的有线交换机，三者都接在上面；不接校园网 |

**网络**：三台设备用同一个网段的**静态地址**，地址写在仓库根目录的私有文件 `.local/wired-lab.json` 里（不进 Git）。主机的 Wi-Fi 只用来上外网，不用关。

1. **最省事**：把项目原来那台电脑上的 `.local/wired-lab.json` 复制到这台主机的仓库根目录同一位置。它里面就是现场使用的地址。
2. 没有那份文件时，`setup` 会逐项问你（本机有线地址和前缀、网卡名、ROCK 地址、ROCK 用户名、摄像头地址），并以 0600 权限写入。
3. 把主机的**有线网卡**设成配置里的静态地址：
   - macOS：系统设置 › 网络 › 有线网卡 › 详细信息 › TCP/IP › 配置 IPv4 选"手动"，填地址和子网掩码，**路由器留空**（这样不会抢走 Wi-Fi 的外网）。
   - Linux（NetworkManager）：`nmcli con add type ethernet ifname <网卡> con-name sd5531-lab ipv4.method manual ipv4.addresses <地址/前缀> ipv4.never-default yes ipv6.method disabled`

## 2. 第一次：安装和检查（约 15 秒）

```bash
git clone https://github.com/OrsonJyu/Lab-Studies-in-Systems-Design.git
```

```bash
cd Lab-Studies-in-Systems-Design && python3 project-camera/demo/demo.py setup
```

macOS 也可以在访达里双击 `project-camera/demo/setup.command`。

`setup` 依次做这些事，每一项都打 ✓ 或 ✗：

| 步骤 | 做什么 | 需要你操作 |
| --- | --- | --- |
| 网络 | 检查 ROCK 的 SSH、摄像头的 RTSP 和 ONVIF 端口能否连上 | — |
| 登录 ROCK | 建立一个保持 4 小时的 SSH 连接，之后的命令都走它 | 输入 ROCK 登录密码。**第一次**会显示 ROCK 的主机密钥指纹：在 ROCK 本机运行 `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`，或在原来那台已信任的电脑上运行 `ssh-keygen -l -F <配置里的 ssh_host_key_alias>`，核对一致才输入 `yes` |
| ROCK 环境 | 检查 Python 3.9+、ffmpeg、ffprobe | 缺 ffmpeg 时需临时让 ROCK 联网：`sudo apt install -y ffmpeg` |
| 部署程序 | 把 `project-camera/src/recorder/` 的程序复制到 ROCK 的 `~/sd5531/recorder/`，逐个文件核对 SHA-256 | — |
| ROCK 配置 | ROCK 上没有 `config.json` 时写入 [rock-config.json](rock-config.json)（守宫触发、阈值 15、关闭大小规则）；已有就保留 | — |
| 摄像头码流 | ROCK 上没有 `~/sd5531/private/camera_*.json` 时，问摄像头的 RTSP 用户名和密码，只写到 ROCK 上（0600） | 输入摄像头用户名和密码（输入时不显示）；已有就跳过 |
| 检查 | 在 ROCK 上解码主、子码流各一下；运行自检（跟踪和检测规则的单元测试）；读 ROCK 和摄像头的时间 | — |

全部 ✓ 后显示"安装完成"。`setup` 可以重复运行，不会覆盖已有的配置、检测区域或摄像头密码。

## 3. 每次使用

| 做什么 | 命令（macOS 也可双击同名 `.command`） |
| --- | --- |
| 开始录制 | `python3 project-camera/demo/demo.py start` |
| 查看状态 | `python3 project-camera/demo/demo.py status` |
| 停止录制 | `python3 project-camera/demo/demo.py stop` |
| 只转存一次片段 | `python3 project-camera/demo/demo.py sync` |

`start` 依次：检查网络 → 登录（4 小时内不用再输）→ ROCK 时间与本机差超过 1 秒就校准（要再输一次 ROCK 密码用于 sudo）→ 程序与仓库不一致就重新部署并重启 → 摄像头画面时间差超过 1 秒就按 ROCK 时间设置（摄像头断电后会忘记时间）→ 启动录制和网页 → 确认缓存、检测、实时画面都正常 → 打开网页 → **窗口开着就每 10 秒把新片段移到本机**。

- 片段默认存到仓库旁边的 `recordings/`（即 `<仓库>/../recordings`）；用 `--recordings 目录` 或环境变量 `SD5531_RECORDINGS` 改。片段里可能拍到人，不要提交到 Git。
- 关掉 `start` 的窗口（或 Ctrl-C）只停止转存，ROCK 继续录制，新片段暂存在 ROCK 上，下次 `start` 或 `stop` 时再移过来。
- 本机上的片段从不删除；ROCK 上的视频只在本机副本 SHA-256 核对一致后才删除，记录（JSON）留在 ROCK 上给网页时间轴用。

## 4. 演示步骤

网页地址在 `start` 的输出里（`http://<ROCK 地址>:8080/`），用本机浏览器打开。

1. **画检测区域**（每摆一次摄像头做一次）：点"设置检测区域"，在静止截图上依次点出饲养箱（或代替它的区域）的角，点"保存"。之后实时画面上一直叠着蓝色半透明框。
2. **放好守宫**（或玩具代替），保持画面静止约 3 秒，右侧"守宫"显示"未锁定：等它第一次移动"。
3. 按下表演示：

| 操作 | 应该看到 |
| --- | --- |
| 拉动守宫后停下 | 绿框锁定它、跟着走；出现"录制中"；停下 5 秒后结束，时间轴上多一段 |
| 让它静止 1 分钟以上 | "静止于 (x, y)，已 N 秒，最后确认 N 秒前"，不变成"丢失" |
| 手在区域里晃（不碰守宫） | 绿框留在守宫上，**不录** |
| 人在区域外走动 | 不录 |
| 开关灯 | 不录；时间轴上出现灰色竖线（环境变化），守宫保持锁定 |
| 再拉动守宫 | 又开始录制 |
| 把守宫拿走 | 约 15 秒后显示"丢失：最后出现于 …" |

4. 点时间轴上的标记或下方表格可以播放片段；已移到本机的片段会注明"已存到 Mac 的 recordings 文件夹"。

## 5. 参数

ROCK 上的参数在 `~/sd5531/recorder/config.json`，改完运行 `stop` 再 `start` 生效。各项含义见[录制程序说明](../src/recorder/README.md)。演示用的值：

| 参数 | 值 | 作用 |
| --- | --- | --- |
| `motion.trigger` | `gecko` | 守宫移动才录；改成 `change` 就是"检测区域里画面有变化就录" |
| `motion.pixel_threshold` | 15 | 越小越灵敏 |
| `motion.size_filter` | `false` | 不按变化块大小过滤（移动玩具时更容易录到） |
| `pre_roll_s` / `still_s` | 4 / 5 | 触发前保留秒数 / 静止多少秒结束 |

这些是替代场景（玩具蜥蜴）下调出的初始值，没有在真实守宫和饲养箱里验证。

## 6. 出问题时

| 现象 | 处理 |
| --- | --- |
| `ROCK SSH 连不上`，摄像头能连 | ROCK 可能断电或死机：看指示灯，重新插电，约 1 分钟后重试；频繁出现请换电源适配器或插座 |
| 三个端口都连不上 | 本机有线网卡没有设成配置里的静态地址，或网线/USB 网卡松了（macOS 上 USB 网卡掉线后要重新插） |
| `无法登录 ROCK` | 密码错，或 ROCK 的主机密钥和已信任的不一致（换过系统卡）。后者先核对指纹，确认后再处理 `~/.ssh/known_hosts` |
| `ROCK 缺少 ffmpeg` | ROCK 临时联网：`sudo apt install -y ffmpeg` |
| 主/子码流读不到 | 摄像头密码不对：删掉 ROCK 上 `~/sd5531/private/camera_*.json` 后重新运行 `setup` |
| 网页打不开 | 用 `status` 看；浏览器若走代理，把 ROCK 地址加入直连 |
| 画面左上角时间不对 | 不影响录像（录像用 ROCK 时间）；`start` 会自动校准 |
| 手晃时仍被录下 | 先确认检测区域只框住了饲养箱；仍有问题可临时把 `motion.trigger` 改为 `change` 对比 |
| 守宫一直"未锁定" | 它要先动一次才会被锁定；启动时画面要静止约 3 秒才能生成背景 |

## 7. 已验证的范围

- 2026-11-05 在学校现场：拉动玩具蜥蜴被录下，手在区域里晃 8 秒不录（[记录](../experiments/2026-11-05-school-gecko-trigger/README.md)）；绿框框住整只蜥蜴（[记录](../experiments/2026-11-05-school-gecko-tracker-colour/README.md)）。
- 同日在原来那台 Mac 上用真实硬件测试本工具：`setup`（13 秒，全部 ✓）、`start`、`stop` → `start`、`status`、`sync`；在 ROCK 的临时目录里测了从零部署、写默认配置、写摄像头配置（权限 0600，不打印密码）。
- **尚未验证**：在另一台主机上从零运行（主机密钥首次信任、交互填写网络配置只在模拟输入下测过）；Linux 主机；真实守宫和饲养箱；长时间运行；开关灯一项只在早期版本中观察到一次。

---

## For agents and English readers

One command installs and checks, one runs. Host: macOS/Linux with Python 3.9+ and `ssh`, wired to the same isolated switch as the ROCK 4C+ and the camera, static address on the wired port.

```bash
python3 project-camera/demo/demo.py setup    # first time: network, SSH trust, ROCK deps, deploy, camera files, self-test
python3 project-camera/demo/demo.py start    # clocks, deploy if changed, start, open web page, move clips every 10 s
python3 project-camera/demo/demo.py status   # health
python3 project-camera/demo/demo.py stop     # stop and move the last clips
```

- Network values: git-ignored `.local/wired-lab.json` (schema in `project-camera/src/network/config.example.json`); copy it from the original host or let `setup` ask. Real addresses never go into the repository.
- Camera stream URIs contain the camera credentials (in the RTSP path). They exist only on the ROCK in `~/sd5531/private/camera_*.json` (0600). `demo.py` never prints them; do not print, log or commit them.
- Code deployed to the ROCK is `project-camera/src/recorder/*`, verified by SHA-256; `config.json`, the detection area (`~/sd5531/roi.json`) and camera files on the ROCK are kept if present. The detection area belongs to the user: do not redraw or overwrite it.
- Passwords (ROCK login, sudo for the clock, camera) are typed by the user at prompts; the script does not store them. An agent should not type them.
- Recording is triggered by the tracked gecko moving (`motion.trigger: gecko`); see `project-camera/src/recorder/README.md` for every parameter and `project-camera/experiments/2026-11-05-school-*` for the evidence and limits.
