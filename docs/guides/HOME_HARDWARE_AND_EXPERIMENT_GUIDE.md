---
id: guide-home-hardware-reproduction
type: guide
environment: home
document_version: 1.2.1
updated_on: 2026-10-30
aliases: [home 实验复现, 硬件接线, 摄像头实验指导, agent 交接, RTSP, ONVIF]
related: [env-home, D011, D012, ws-preroll-recording]
---

# home 硬件连接与程序实验复现指南

**对象：接手本项目的同学与 agent。** 本文依据 2026-10-30 的 `home` 实验和仓库 v1.2.0 基线编写。目标是复现“ROCK 接收真实视频 → 系统卡保存 → 文件检查 → Mac 实时查看”，不把学校、热点或预录制描述为已经通过。

本文从 **microSD 已刷好系统**开始。新设备需先按 [Radxa 官方安装说明](https://docs.radxa.com/en/rock4/rock4c%2B/getting-started/install-os)准备 ROCK 4C+ 对应镜像；本次使用 Debian 12 bookworm KDE。不要为复现实验重复刷写已正常工作的系统卡或录像硬盘。

需要取得仓库时，在有访问权限的 Mac 上先克隆并进入仓库。下面固定到本指南的 v1.2.1 文档版本，并跳过自动下载历史 LFS 媒体；本指南本身不依赖那些媒体才能运行。标签检出用于复现，要提交新实验时先按维护规则创建工作分支。

```sh
GIT_LFS_SKIP_SMUDGE=1 git clone --branch v1.2.1 --single-branch https://github.com/OrsonJyu/Lab-Studies-in-Systems-Design.git
cd Lab-Studies-in-Systems-Design
```

若需要查看本次已归档的对照录像，按仓库首页安装 Git LFS 后，可仅下载对应实验目录，而不必先取回整个历史媒体档案：

```sh
git lfs pull --include='project-camera/experiments/2026-10-30-home-*/**' --exclude=''
```

## 1. 先理解本次实验

摄像头是一台 **IP 网络设备**。它通过交换机向 ROCK 提供视频；ROCK 运行 FFmpeg 并保存文件。Mac 用于 SSH 操作和实时预览，不承担本次录像的现场存储。

| 要复现的结果 | 本次证据 | 不能据此认定 |
| --- | --- | --- |
| 系统卡基础保存与解码 | 60 秒合成片段，640 × 360，900 帧 | 摄像头已接通或系统卡耐久通过 |
| 真实摄像头短录像 | H.264，2560 × 1440，约 20 fps，60.001 秒、1201 帧，完整解码通过 | 预录制、全天稳定或事件时间准确 |
| Mac 实时预览 | FFplay 窗口中动态画面由用户确认 | 延迟为零、IINA 必然可用或已自动录制 |

参考：[home 环境](../../project-camera/environments/home/README.md)、[系统卡实验](../../project-camera/experiments/2026-10-30-home-system-card/README.md)、[真实录像](../../project-camera/experiments/2026-10-30-home-camera-recording/README.md)、[预览实验](../../project-camera/experiments/2026-10-30-home-live-preview/README.md)。

**阅读与执行顺序：** 接线 → 找到 ROCK → 检查存储/软件 → 配置摄像头网段 → ONVIF 取流 → 录像 → 解码/回放 → 实时预览。前一步没有通过，就在该层排查，不直接跳到“摄像头坏了”或“代理导致”。

## 2. 硬件与版本

| 部件 | 本次使用 / 作用 |
| --- | --- |
| ROCK 4C+ | Debian 12 bookworm，aarch64；内核 6.1.115-8-rk2501 |
| 系统 microSD | 本次实际录像介质，ext4；开始时根文件系统约剩余 104 GiB |
| ROCK 电源 | 独立 USB-C 电源；按板卡要求供电，官方准备说明列出 5V / 3A |
| 网络摄像头 | 实物标签：标称 4MP、2.8mm、PoE 48V / 4W、ONVIF |
| PoE 供电器 | 标签型号 4805，输出 48V / 0.5A；有 POE 与 LAN 两个网口 |
| TP-LINK TL-SG1008D | 普通 8 口千兆交换机；只连接数据，不给相机提供 PoE 电源 |
| 家用路由器 | 为本次管理网络提供接入，Mac 经 Wi-Fi 管理 ROCK |
| Mac | 本次 FFplay 8.0.1 用于预览；还需 SSH 与 Python 3.9+；无需外接 ROCK 显示器 |
| 板卡软件 | FFmpeg / ffprobe 5.1.9-0+deb12u1，Python 3 标准库 |

本指南只针对已实测的这些角色和设备。旧展示里的 ROCK 5C、SSD、XM530AI + SC2235 或 5MP 文字不能替代本次实物标签和测得的视频参数。完整摄像头型号/固件及 PoE 标准协商兼容性没有独立验收。

## 3. 硬件怎样接

```text
摄像头网口
    │ 网线 A：数据 + 摄像头供电
PoE 供电器【POE／有电压】口
PoE 供电器【LAN／数据】口
    │ 网线 B：数据
TL-SG1008D 普通交换机
    ├── 网线 C ── ROCK 4C+ 网口
    └── 网线 D ── 路由器 LAN 口
                         └── Wi-Fi ── Mac

另外接电：PoE 供电器、交换机、路由器、ROCK 各用其匹配电源。
录像路径：摄像头 → 交换机 → ROCK / FFmpeg → 系统 microSD。
预览路径：摄像头 → ROCK → SSH 转发 → Mac 本机端口 → FFplay。
```

| 线 | 起点 | 终点 | 核对重点 |
| --- | --- | --- | --- |
| A | 摄像头 | 供电器 POE 口 | POE 端有输出电压，仅接匹配相机 |
| B | 供电器 LAN 口 | 交换机任意数据口 | 不是把 POE 输出口插入普通交换机 |
| C | ROCK 网口 | 交换机另一个数据口 | ROCK 继续独立供电 |
| D | 路由器 LAN 口 | 交换机另一个数据口 | 使用 LAN，不是 WAN |

交换机共占 3 个口，四根网线分别连接上述设备。端口够用不表示地址自动互通。首次移动接线时，先接好“交换机到路由器”，再移动 ROCK 的管理网线，便于继续 SSH。

**不要把供电器的 POE 输出口接 Mac、ROCK 普通网口或普通交换机。** 本次已有供电器，无需仅因交换机不带 PoE 就更换交换机。供电器标称电压匹配不等于任何其他摄像头都能使用。

## 4. 先填现场参数，不照抄其他环境的地址

以下 `<...>` 都是待填字段，执行前替换。实际地址和账号由现场网络、设备标签或负责人提供，不写进共享文档。密码不放进这些变量。

| 参数 | 从哪里取得 |
| --- | --- |
| `SD5531_BOARD_HOST` | 当前路由器 DHCP 列表、已知板卡主机名或已有管理记录 |
| `SD5531_BOARD_USER` | 板卡实际登录账号；登录密码由负责人私下提供 |
| `SD5531_CAMERA_HOST` | 相机标签固定 IP；若已修改，按实际配置核对 |
| `SD5531_BOARD_IFACE` | ROCK 的 `ip -br -4 addr` 输出；本次为有线接口，不能假定叫 eth0 |
| `SD5531_BOARD_CAMERA_CIDR` | 摄像头网段内未使用的板卡地址/前缀；本次板卡辅助地址用了 /24，不能与相机或其他设备重复 |
| `SD5531_ONVIF_PORT` | 本次标签给出的服务端口为 8899；不是所有设备的统一值 |
| `SD5531_LOCAL_PORT` | Mac 上未被占用的本机端口；本次使用 18554 |

### 在 Mac：保存本机参数

在仓库根目录执行，随后用编辑器把占位值填好。`.local/` 已被 Git 忽略。没有克隆仓库时，也可在自己的私有工作目录建这个文件，但不要上传实际参数。

```sh
mkdir -p .local
cat > .local/home.mac.env <<'EOF'
export SD5531_ENV='home'
export SD5531_BOARD_HOST='<当前板卡管理地址>'
export SD5531_BOARD_USER='<板卡登录账号>'
export SD5531_CAMERA_HOST='<相机当前固定地址>'
export SD5531_LOCAL_PORT='18554'
export SD5531_REMOTE_SOURCE='sd5531/private/home-camera-source.json'
EOF
chmod 600 .local/home.mac.env
```

填好后，在 **Mac 终端**执行：

```sh
source .local/home.mac.env
command -v ssh
python3 --version
ssh "${SD5531_BOARD_USER}@${SD5531_BOARD_HOST}"
```

首次 SSH 需要确认目标主机；密码输入时不显示字符。成功后提示符通常带板卡主机名。**从此刻起是在 ROCK 执行命令**，不是 Mac。每开一个新终端，环境变量不会自动共享；后文会注明哪些参数要重新加载。

如果只知道路由器地址而不知道管理密码，不要恢复路由器出厂设置。本实验需要找到板卡地址，不以重置宽带或路由器为前提。`arp -a` 可以提供设备线索，但其缓存不是完整设备清单；`.local` 主机名也依赖现场发现条件。

## 5. 在 ROCK：确认系统、存储和工具

```sh
cat /etc/os-release
uname -m
uname -r
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS,MODEL
df -h /
command -v ffmpeg
command -v ffprobe
python3 --version
```

预期：本次系统为 Debian 12 / bookworm、aarch64；输出目录所在文件系统是系统卡。不要仅凭“能看到一块磁盘”就把它记成 SATA 已验证。

缺少软件时，仍在 **ROCK** 执行：

```sh
sudo apt-get update
sudo apt-get install -y ffmpeg python3
ffmpeg -version
ffprobe -version
```

记录实际安装版本。后续安全更新可能使版本号变化，不能冒充仍是原实验版本。本文不要求执行全系统升级。

## 6. 在 ROCK：让它与摄像头地址互通

本次管理网络和摄像头固定地址不在同一个直接可达网段。采用的办法是：**保留板卡原管理地址和默认路由，给有线接口临时增加一个摄像头网段地址**。

先读取：

```sh
ip -br -4 addr
ip route
```

在当前 ROCK 终端填写：

```sh
export SD5531_ENV='home'
export SD5531_CAMERA_HOST='<相机当前固定地址>'
export SD5531_BOARD_IFACE='<当前有线接口名>'
export SD5531_BOARD_CAMERA_CIDR='<未使用的同网段板卡地址/前缀>'
export SD5531_ONVIF_PORT='8899'
export SD5531_PRIVATE_SOURCE="$HOME/sd5531/private/home-camera-source.json"
```

确认辅助地址未被其他设备使用、掩码正确，再执行下段。它不会替换 DHCP 主地址或添加默认网关；若相同地址已经存在，会保留现状。

**Python 代码块的运行方式：** 在 ROCK 终端输入 `python3 - <<'PY'`，粘贴整段 Python，再单独一行输入 `PY`。后文独立 Python 块采用同样方式；第 10 节明确改在 Mac 执行。也可以由 agent 将代码保存为本地 `.py` 后运行。不要把 Python 逐行当 shell 命令执行。

```python
import ipaddress
import json
import os
import subprocess

iface = os.environ['SD5531_BOARD_IFACE']
candidate = ipaddress.IPv4Interface(os.environ['SD5531_BOARD_CAMERA_CIDR'])
camera = ipaddress.IPv4Address(os.environ['SD5531_CAMERA_HOST'])
if (camera not in candidate.network or candidate.ip == camera or
        candidate.ip in (candidate.network.network_address, candidate.network.broadcast_address)):
    raise SystemExit('请填写与相机同网段、但不同于相机的未使用地址')
links = json.loads(subprocess.check_output(
    ['ip', '-j', '-4', 'addr', 'show', 'dev', iface], text=True))
matching = [a for link in links for a in link.get('addr_info', [])
            if a.get('local') == str(candidate.ip)]
if matching and not any(a.get('prefixlen') == candidate.network.prefixlen for a in matching):
    raise SystemExit('该地址已使用不同前缀，先核对配置，不自动覆盖')
already = bool(matching)
if not already:
    subprocess.run(['sudo', 'ip', 'addr', 'add', str(candidate),
                    'dev', iface], check=True)
print('辅助地址已存在' if already else '已添加本次临时辅助地址')
subprocess.run(['ip', 'route', 'get', str(camera)], check=True)
```

`ip route get` 应显示从目标有线接口直接到达相机，而不是经管理网络的网关绕行。然后检查端口：

```python
import os
import socket

host = os.environ['SD5531_CAMERA_HOST']
for port in (80, int(os.environ['SD5531_ONVIF_PORT']), 554):
    try:
        with socket.create_connection((host, port), timeout=3):
            print(port, 'TCP 可连接')
    except OSError as exc:
        print(port, '未连通：', type(exc).__name__)
```

本次这三项在 ROCK 上均成功。ARP 回应只证明地址解析层有设备回应，不等于取流成功；ping 不通也不能单独证明设备没有上电。8899 是本机标签标注的服务入口，浏览器访问根路径没有网页，不足以判断 ONVIF 不工作。

## 7. 在 ROCK：通过 ONVIF 取得真正的 RTSP URI

不能凭相机 IP 拼一个猜测的 `/stream` 地址，也不要把含访问参数的 URI 粘贴到聊天、Git 或共享日志。

下面代码使用本次成功的只读调用顺序：`GetCapabilities → GetProfiles → GetStreamUri`。它会查询媒体服务、选择最高分辨率的 H.264/H.265 配置，并把完整 URI 写到环境对应的私有 JSON。**不会修改摄像头设置**；重复执行会原子更新该环境的私有流配置。

本机相机在当次状态下允许这些读取。若返回鉴权错误，向负责人取得授权账户并使用对应 ONVIF 客户端处理；本段没有实现其他固件的 WS-Security 鉴权，不尝试猜密码或重置设备。

本指南为新复现单独使用 `home-camera-source.json`，不依赖负责人已有的双击启动文件。若经负责人确认复用已有私有流文件，ROCK 的 `SD5531_PRIVATE_SOURCE` 与 Mac 的 `SD5531_REMOTE_SOURCE` 必须指向同一份文件。

```python
import json
import os
from pathlib import Path
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

host = os.environ['SD5531_CAMERA_HOST']
port = int(os.environ['SD5531_ONVIF_PORT'])
private = Path(os.environ['SD5531_PRIVATE_SOURCE']).expanduser()
ns = {'tt': 'http://www.onvif.org/ver10/schema',
      'trt': 'http://www.onvif.org/ver10/media/wsdl'}
dev = 'http://www.onvif.org/ver10/device/wsdl'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

def request(url, action, body):
    envelope = ('<?xml version="1.0"?><s:Envelope '
        'xmlns:s="http://www.w3.org/2003/05/soap-envelope" '
        f'xmlns:tds="{dev}" xmlns:trt="{ns["trt"]}" '
        f'xmlns:tt="{ns["tt"]}"><s:Body>{body}</s:Body></s:Envelope>')
    req = urllib.request.Request(url, data=envelope.encode(), headers={
        'Content-Type': 'application/soap+xml; charset=utf-8; action="'+action+'"'})
    with opener.open(req, timeout=8) as response:
        root = ET.fromstring(response.read(100000))
    if any(e.tag.endswith('}Fault') for e in root.iter()):
        raise RuntimeError('ONVIF SOAP Fault')
    return root

try:
    capabilities = request(f'http://{host}:{port}/onvif/device_service',
        dev+'/GetCapabilities', '<tds:GetCapabilities>'
        '<tds:Category>All</tds:Category></tds:GetCapabilities>')
    media_node = next(e for e in capabilities.iter() if e.tag.endswith('}Media'))
    media_url = next(e.text for e in media_node.iter() if e.tag.endswith('}XAddr'))
    if urllib.parse.urlsplit(media_url).hostname != host:
        raise RuntimeError('媒体服务地址与已确认相机地址不同，请先人工核对')
    root = request(media_url, ns['trt']+'/GetProfiles', '<trt:GetProfiles/>')
    profiles = []
    for item in root.findall('.//trt:Profiles', ns):
        def value(path):
            return item.findtext(path, default='', namespaces=ns)
        profile = {'token': item.get('token'), 'name': value('tt:Name'),
            'encoding': value('.//tt:VideoEncoderConfiguration/tt:Encoding'),
            'width': int(value('.//tt:VideoEncoderConfiguration/tt:Resolution/tt:Width') or 0),
            'height': int(value('.//tt:VideoEncoderConfiguration/tt:Resolution/tt:Height') or 0),
            'configured_fps': value('.//tt:VideoEncoderConfiguration/tt:RateControl/tt:FrameRateLimit')}
        if profile['encoding'] in ('H264', 'H265') and profile['token']:
            profiles.append(profile)
    if not profiles:
        raise RuntimeError('没有适用的视频配置')
    selected = max(profiles, key=lambda p: p['width']*p['height'])
    body = ('<trt:GetStreamUri><trt:StreamSetup><tt:Stream>RTP-Unicast</tt:Stream>'
        '<tt:Transport><tt:Protocol>RTSP</tt:Protocol></tt:Transport>'
        '</trt:StreamSetup><trt:ProfileToken>'+escape(selected['token'])+
        '</trt:ProfileToken></trt:GetStreamUri>')
    root = request(media_url, ns['trt']+'/GetStreamUri', body)
    uri = root.findtext('.//tt:Uri', namespaces=ns)
    parsed = urllib.parse.urlsplit(uri or '')
    if parsed.scheme not in ('rtsp', 'rtsps') or parsed.hostname != host:
        raise RuntimeError('返回的视频 URI 不符合本次已确认的相机目标')
    private.parent.mkdir(parents=True, exist_ok=True)
    private.parent.chmod(0o700)
    with tempfile.NamedTemporaryFile('w', dir=private.parent, delete=False) as f:
        json.dump({'environment': os.environ['SD5531_ENV'],
                   'uri': uri, 'profile': selected}, f)
        staged = Path(f.name)
    staged.chmod(0o600)
    staged.replace(private)
    print('私有流配置已写入；未打印 URI。')
    print(json.dumps({k: v for k, v in selected.items() if k != 'token'},
                     ensure_ascii=False))
except urllib.error.HTTPError as exc:
    raise SystemExit('ONVIF HTTP '+str(exc.code)+
                     '：检查服务路径或授权；不要公开原始响应。')
except Exception as exc:
    raise SystemExit('ONVIF 获取未完成：'+type(exc).__name__+
                     '。检查服务地址和授权状态；不要公开原始响应。')
```

预期：本次主配置为 H.264、2560 × 1440、配置帧率 20。实际新文件的编码、帧率和时长仍须在第 9 节重新检查；不要把配置声明当作实际性能。

## 8. 在 ROCK：录一段 60 秒真实视频

先为**这次新运行**创建目录，不覆盖仓库中已经归档的原实验：

```sh
export SD5531_RUN_DIR="$HOME/sd5531/experiments/$(TZ=Asia/Hong_Kong date +%Y-%m-%d-%H%M%S)-home-reproduction"
mkdir -p "$SD5531_RUN_DIR"
chmod 700 "$SD5531_RUN_DIR"
df -h "$SD5531_RUN_DIR"
findmnt -T "$SD5531_RUN_DIR" -o SOURCE,FSTYPE,TARGET
```

确认路径确实落在系统卡。执行下面代码后，**等它打印 `RECORDING_STARTED` 再挥手**。这个消息是在首批真实视频帧到达后发出，不是进程刚启动时发出。

```python
import datetime
import json
import os
from pathlib import Path
import subprocess
import threading
import time

source = json.loads(Path(os.environ['SD5531_PRIVATE_SOURCE']).read_text())
out = Path(os.environ['SD5531_RUN_DIR'])
clip = out/'camera-main-60s.mp4'
if clip.exists():
    raise SystemExit('目标录像已存在，请换新运行目录；不覆盖原片')
args = ['ffmpeg', '-hide_banner', '-nostdin', '-n', '-rtsp_transport', 'tcp',
        '-timeout', '10000000', '-i', source['uri'], '-t', '60',
        '-map', '0:v:0', '-an', '-c:v', 'copy', '-movflags', '+faststart',
        '-progress', 'pipe:1', '-nostats', str(clip)]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
first_frame = None
progress = {}
t0 = time.monotonic()
fd = os.open(out/'recording.private.log', os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as log:
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=log,
                               text=True, bufsize=1)
    watchdog = threading.Timer(100, process.terminate)
    watchdog.start()
    try:
        for line in process.stdout:
            key, sep, val = line.strip().partition('=')
            if sep:
                progress[key] = val
            if key == 'frame' and val.isdigit() and int(val) > 0 and first_frame is None:
                first_frame = datetime.datetime.now(datetime.timezone.utc).isoformat()
                print('RECORDING_STARTED：已收到真实视频，现在可以挥手。', flush=True)
        code = process.wait()
    finally:
        watchdog.cancel()
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=10)
result = {'environment': os.environ['SD5531_ENV'], 'started_utc': started,
          'first_frame_received_utc': first_frame, 'capture_exit': code,
          'wall_seconds': round(time.monotonic()-t0, 2),
          'requested_duration_seconds': 60, 'audio_recorded': False,
          'last_progress': progress, 'bytes': clip.stat().st_size if clip.exists() else 0}
(out/'capture-result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
print('输出目录：', out)
if code != 0:
    raise SystemExit('采集未正常完成；保留原片和私有日志，不标记为通过')
```

对着镜头挥手或展示可核对的动作，保持镜头稳定一段时间。60 秒结束后程序自动退出；本次 `-c:v copy` 是保存相机编码，不重新编码，`-an` 不保存音频。此方法不包含运动检测、事件触发或预录制。

`recording.private.log` 可能带相机访问 URI，必须留本地。需要分享时制作去访问参数的副本，并保留原始文件校验值；不要把未经检查的原日志直接 `git add`。

## 9. 在 ROCK 检查文件，再到 Mac 回放

以下完整读取文件并软件解码，同时约每 5 秒输出一张预览。不要只看文件存在或大小大于零就认定成功。

```python
import hashlib
import json
import os
from pathlib import Path
import subprocess

out = Path(os.environ['SD5531_RUN_DIR'])
clip = out/'camera-main-60s.mp4'
probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
    'stream=codec_name,codec_tag_string,width,height,avg_frame_rate,r_frame_rate,nb_frames,start_time,duration:format=duration,size',
    '-of', 'json', str(clip)], capture_output=True, text=True)
if probe.returncode:
    raise SystemExit('媒体检查未通过，请检查本地文件')
media = json.loads(probe.stdout)
previews = out/'previews'
previews.mkdir(exist_ok=True)
with (out/'decode.log').open('w') as log:
    decoded = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-n',
        '-v', 'error', '-xerror', '-threads', '4', '-i', str(clip),
        '-vf', 'fps=1/5,scale=640:-2', '-an', str(previews/'preview-%02d.jpg')],
        stdout=log, stderr=log, timeout=180)
digest = hashlib.sha256()
with clip.open('rb') as f:
    for block in iter(lambda: f.read(1024*1024), b''):
        digest.update(block)
result = {'environment': os.environ['SD5531_ENV'], 'media': media,
          'full_decode_exit': decoded.returncode, 'sha256': digest.hexdigest(),
          'preview_count': len(list(previews.glob('preview-*.jpg')))}
(out/'validation-result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
if decoded.returncode:
    raise SystemExit('完整解码未通过，不标记实验成功')
```

预览目录已经有图片时，`-n` 会拒绝覆盖；重新验证可换一个新的预览目录，保留原来的检查记录。

### 在 Mac：复制与回放

打开另一个 **Mac 终端**，回到含 `.local/home.mac.env` 的工作目录，加载 Mac 参数。`SD5531_REMOTE_RUN` 填第 8 节实际输出的板卡目录。

```sh
source .local/home.mac.env
export SD5531_REMOTE_RUN='<本轮 ROCK 输出目录>'
export SD5531_LOCAL_RUN=".local/home-reproduction/$(basename "$SD5531_REMOTE_RUN")"
mkdir -p "$SD5531_LOCAL_RUN"
scp "${SD5531_BOARD_USER}@${SD5531_BOARD_HOST}:${SD5531_REMOTE_RUN}/camera-main-60s.mp4" "$SD5531_LOCAL_RUN/"
shasum -a 256 "$SD5531_LOCAL_RUN/camera-main-60s.mp4"
```

Mac 的 SHA-256 应等于**这次新文件** `validation-result.json` 的 SHA-256。新拍的视频不会与旧实验原片有相同哈希，帧数、体积也不要求逐字节一致。

本地目录随本轮远端目录命名。目标文件已存在时先核对其来源，不覆盖另一轮运行的文件。

用本机播放器打开新 MP4，确认能看到这轮现场动作，检查开头、动作期间和结尾。若系统播放器不能解码，可先用已安装的 FFplay 或支持该编码的播放器核对；不能把播放器不支持直接当作文件损坏。

## 10. 在 Mac 实时看画面

### 10.1 检查播放器

```sh
command -v ffplay
ffplay -version
```

本次 Mac 已安装 FFplay 8.0.1。没有时，可按本机受信任的软件安装流程安装 FFmpeg（例如 [Homebrew 官方配方](https://formulae.brew.sh/formula/ffmpeg)），再确认 `ffplay` 实际存在并记录版本。不要假定所有 FFmpeg 安装都包含播放器。

### 10.2 Mac 终端 A：保持 SSH 转发

在含 `.local/home.mac.env` 的工作目录执行：

```sh
source .local/home.mac.env
lsof -nP -iTCP:"$SD5531_LOCAL_PORT" -sTCP:LISTEN
```

若端口被不明进程占用，换一个空闲端口并同步修改本机参数；不要随意结束别人的进程。本次仍运行中的已知 SSH 预览通道可以复用，不要重复绑定同一端口。

需要新通道时：

```sh
ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 \
  -L "127.0.0.1:${SD5531_LOCAL_PORT}:${SD5531_CAMERA_HOST}:554" \
  "${SD5531_BOARD_USER}@${SD5531_BOARD_HOST}"
```

这个终端保持运行。它让 Mac 本机端口经 ROCK 到相机，不要求 Mac 直接进入相机固定地址网段；`127.0.0.1` 只供本机访问。没有新增路由器端口映射或公网视频服务。

### 10.3 Mac 终端 B：读取私有配置并打开 FFplay

另开一个 **Mac 终端**，进入同一个工作目录，执行 `source .local/home.mac.env`，再运行以下 Python 代码。它通过 SSH 读取第 7 节生成的私有 JSON，在内存中替换 RTSP 目标为本机端口，不把 URI 打印到终端。

```python
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import urllib.parse

target = os.environ['SD5531_BOARD_USER']+'@'+os.environ['SD5531_BOARD_HOST']
remote_file = os.environ['SD5531_REMOTE_SOURCE']
player = shutil.which('ffplay')
if not player:
    raise SystemExit('本机没有找到 ffplay')
response = subprocess.run(['ssh', target, 'cat', shlex.quote(remote_file)],
    capture_output=True, text=True, timeout=120)
if response.returncode:
    raise SystemExit('未能读取板卡私有配置；检查 SSH 及相对用户目录的文件位置')
source = json.loads(response.stdout)
parsed = urllib.parse.urlsplit(source['uri'])
userinfo = parsed.netloc.rsplit('@', 1)[0]+'@' if '@' in parsed.netloc else ''
uri = urllib.parse.urlunsplit((parsed.scheme,
    userinfo+'127.0.0.1:'+os.environ['SD5531_LOCAL_PORT'],
    parsed.path, parsed.query, parsed.fragment))
log_path = Path(tempfile.gettempdir())/('sd5531-'+os.environ['SD5531_ENV']+'-preview.private.log')
fd = os.open(log_path, os.O_WRONLY|os.O_CREAT|os.O_TRUNC, 0o600)
os.fchmod(fd, 0o600)
with os.fdopen(fd, 'w') as log:
    process = subprocess.Popen([player, '-hide_banner', '-loglevel', 'warning',
        '-nostats', '-rtsp_transport', 'tcp', '-an', '-window_title',
        'SD5531 Live Camera', '-x', '960', '-y', '540', uri],
        stdin=subprocess.DEVNULL, stdout=log, stderr=log)
    print('请查看 SD5531 Live Camera 窗口。预览不保存录像。', flush=True)
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait(timeout=10)
```

SSH 读取配置时可能再次询问板卡密码，正常输入即可。**看到窗口后再挥手**，确认画面持续更新。仅有程序进程、端口连接或“启动成功”文字，不能当作画面已经显示。

关闭预览窗口可停止观看；终端 A 按 `Ctrl+C` 可关闭本次前台 SSH 通道。两者不等于关闭 ROCK，也不应误停其他录制任务。实时预览默认静音、不保存视频，实际延迟没有在本次量测。

当前负责人的本地工作目录还保留了双击启动/关闭入口，但这些绑定本机参数的文件不作为其他电脑必需依赖。新同学按本节手工步骤即可建立同一类预览。

## 11. 可选：复现系统卡合成画面测试

用于在不依赖摄像头的情况下区分“工具/文件系统问题”和“相机/网络问题”。仍在 ROCK，使用新的实验目录；不要把合成画面计为摄像头实测。

```sh
export SD5531_RUN_DIR="$HOME/sd5531/experiments/$(TZ=Asia/Hong_Kong date +%Y-%m-%d-%H%M%S)-home-synthetic"
mkdir -p "$SD5531_RUN_DIR"
ffmpeg -hide_banner -nostdin -n -re -f lavfi -i testsrc2=size=640x360:rate=15 \
  -t 60 -an -c:v libx264 -threads 2 -preset ultrafast -crf 23 \
  -pix_fmt yuv420p -movflags +faststart "$SD5531_RUN_DIR/synthetic-60s.mp4"
sync
ffprobe -v error -count_frames \
  -show_entries stream=codec_name,width,height,avg_frame_rate,nb_read_frames:format=duration,size \
  -of json "$SD5531_RUN_DIR/synthetic-60s.mp4"
ffmpeg -hide_banner -nostdin -v error -xerror \
  -i "$SD5531_RUN_DIR/synthetic-60s.mp4" -f null -
```

本次参考结果：60 秒、900 帧、640 × 360、15 fps、完整解码退出码 0。它不是系统卡写入速度或寿命测试。

## 12. 怎么判定复现通过

| 检查点 | 通过条件 | 常见误判 |
| --- | --- | --- |
| 管理连接 | Mac 能 SSH 操作正确的 ROCK | 只看到路由器或某个 IP |
| 地址与取流 | ROCK 有直接到相机的路径，ONVIF 返回配置和有效 URI，实际收到视频 | 交换机亮灯、ARP 成功就算录像通过 |
| 文件 | 采集正常结束，文件时长约 60 秒、编码/分辨率可读，完整软件解码通过 | 文件存在、文件很大就算可用 |
| 现场动作 | 新录像中可核对本轮动作，开头与结尾可回放 | 只检查一张静态截图 |
| 复制 | 新文件两端 SHA-256 一致 | 要求新录像等于旧原片的 SHA-256 |
| 实时预览 | 人或可用的界面证据确认动态画面更新 | 进程存在、TCP 已连接就声称用户看到了 |

**同样的实验结果指能力与验收条件可复现，不指现场画面、字节数、帧数或哈希必须完全相同。** 本次一分钟结果只能支持本次短测试；FFmpeg 的丢帧计数也不能独立证明传输全程零丢失。

## 13. 排查顺序与已知问题

| 现象 | 先查什么 |
| --- | --- |
| SSH 失败 | 板卡供电/启动、当前管理地址、Mac 与 ROCK 的互通、交换机到路由器 LAN 的连接 |
| 有线灯亮但相机不响应 | PoE 供电器方向和电源、相机固定地址、ROCK 辅助地址/掩码；灯亮可能只是交换机链路 |
| ARP 有回应但 TCP 超时 | 实际路由、源网段、相机服务；换取流端后成功不能直接认定代理是唯一原因 |
| ONVIF 报错 | 标签端口、服务 URL、固件支持和授权；不要把 8899 当作必然有网页的地址 |
| RTSP 接通但无图像 | URI 是否由该相机返回、TCP 传输、实际解码与播放器日志 |
| IINA 没画面 | 本次没有以 IINA 计为成功；按已确认的 FFplay 路径复核，先检查动态画面 |
| 重启后失败 | 临时辅助地址与 SSH 通道会丢失；按当前接口和地址重建，不覆盖 DHCP 管理地址 |
| 复制后不能播放 | 先查文件哈希与完整解码，再区分编码兼容性和文件问题 |

本次特别保留两项限制：

- 相机 OSD 日期显示 2026-10-07，与实验记录日期不符。主机记录时间、相机叠加时间与媒体时间轴分开保存，不能把 OSD 当作真实事件时间。
- 真实录像日志出现未设置包时间戳提示和两处 DTS 修正警告。文件可解码，不证明精确事件对齐通过。校时、时间戳处理或参数变更应另建实验，不能覆盖旧原片后声称旧测试没有这些问题。

## 14. 移动到学校或热点时

这次环境名是 `home`。新环境另建参数与实验记录，不能只换一个 Wi-Fi 名称后继续沿用家庭地址。

分别验证两条网络：**摄像头 ↔ ROCK 的本地视频链路**、**Mac ↔ ROCK 的管理链路**。互联网是否可用是另一个问题。

- 学校网络可能隔离客户端，SSH、多播发现和 RTSP 互通条件需现场确认；关闭代理不会解除学校网络自身的隔离。
- 手机热点不自动接入有线摄像头，也不保证客户端对等互通；有线网络与热点之间的设备和路由方式尚未实测。
- 可以考虑独立本地网络承担设备互连，外网按现场允许方式另接；本指南没有选定或验证学校/热点拓扑。
- 每次迁移重新填写当前地址、掩码、接口、私有配置路径、存储介质与时间源，先做短录像和回放，再考虑长期运行。

详见[测试环境目录](../../project-camera/environments/README.md)。

## 15. 清理、记录和 agent 交接

如果还要使用预览或录像，保留本次需要的临时地址。若结束测试、确需清理，在 ROCK 只删除**本轮新加的辅助地址**：

```sh
sudo ip addr del "$SD5531_BOARD_CAMERA_CIDR" dev "$SD5531_BOARD_IFACE"
```

不要删除原 DHCP 管理地址、刷新整个接口地址或为了清理重启网络服务。停止预览只关闭自己的播放器/转发进程，不结束其他人的工作。

新实验用新目录，至少记录：

```markdown
日期/时区：
environment：home（或本轮真实环境）
硬件、系统、工具版本：
接线与私有配置的本地位置：
实际存储介质：
执行步骤与参数变更：
采集开始/首帧接收时间（UTC）及动作说明：
时长、帧数、编码、分辨率、完整解码退出码：
两端文件 SHA-256：
现场画面/用户确认：
警告、失败、限制与未测试项目：
操作者及可确认贡献：
```

给 agent 的交接要求：

1. 先读仓库 `AGENTS.md`、当前状态、home 档案和已有实验，不把旧聊天中的操作当作本轮自动授权。
2. 优先读取现有本地私有配置和实物标签；缺少参数时问确实缺失的部分，不重新索要已归档的全部型号。
3. 每个命令先确认执行端和环境 ID；不把 Mac 的代理、校园隔离、相机供电与地址配置混为一个问题。
4. 通知“开始挥手”必须等实际收到视频帧；通知“已显示”必须有动态画面证据或用户确认。
5. 不把语法检查、端口检查或合成画面写成真实摄像头验收；不把短录写成预录制/长期/SATA 验收。
6. 不公开私有流 URI、密码或原始访问日志。共享证据先去访问参数、个人路径，并登记转换及哈希；MP4 依仓库规则走 Git LFS。
7. 原始基线不覆盖；新结果按日期和环境新增，结论变化按仓库分支规则走 PR。

本指南中的命令和 Python 包装是将本次实际操作整理成可复现形式，不是生产录制服务或已验证的跨环境自动化。阅读后仍需完成参数填写和本轮各检查点，不能仅凭本文存在就认定新的实验通过。

## 16. 原始依据与工具说明

- [home 实物与网络条件](../../project-camera/environments/home/README.md)
- [真实录像结果、日志和原片](../../project-camera/experiments/2026-10-30-home-camera-recording/README.md)
- [系统卡基础实验](../../project-camera/experiments/2026-10-30-home-system-card/README.md)
- [Mac 预览用户确认](../../project-camera/experiments/2026-10-30-home-live-preview/README.md)
- [Radxa ROCK 4C+ 官方准备说明](https://docs.radxa.com/en/rock4/rock4c%2B/getting-started/before-start)
- [ONVIF 官方操作目录](https://www.onvif.org/onvif/ver20/util/operationIndex.html)
- [FFmpeg / ffprobe 官方文档](https://ffmpeg.org/ffprobe.html)
- [FFplay 官方文档](https://ffmpeg.org/ffplay.html)

版本范围：硬件结果以 v1.2.0 归档为依据。文档代码块的语法与参数流程需随修改检查；新的硬件运行结果应另留证据，不倒填到 2026-10-30 原实验中。

## 17. 本指南的检查范围

本次编写已核对归档结果、实际媒体命令与现有本地预览入口；Python 块做了语法检查，shell 块做了 Bash/Zsh 语法检查，并检查维护链接和访问参数泄漏。

没有把这些文档检查冒充新一轮硬件复现。编写时原 SSH 会话已经断开，本轮未再次执行完整的一分钟实物录制、网络迁移或鉴权变体测试；原 home 实测依据仍是第 16 节列出的记录。复现者应按第 12 节为自己的新运行逐项验收。
