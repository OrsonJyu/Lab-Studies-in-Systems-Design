#!/usr/bin/env python3
"""One-command setup and run of the SD5531 gecko recording demo (Python 3.9+, stdlib only).

Runs on the host computer (macOS or Linux) that is wired to the lab switch together
with the ROCK 4C+ and the IP camera. Everything on the ROCK is done over SSH.

  python3 project-camera/demo/demo.py setup    first time on a host: config, SSH trust,
                                               ROCK checks, camera files, deploy, self-test
  python3 project-camera/demo/demo.py start    clocks, deploy if changed, start, open the
                                               web page, keep moving clips to this host
  python3 project-camera/demo/demo.py stop     stop recording, move the last clips
  python3 project-camera/demo/demo.py status   what is running and how it is doing
  python3 project-camera/demo/demo.py sync     move finished clips once

Network values come from the private, git-ignored .local/wired-lab.json at the
repository root (same file as project-camera/src/network). Camera credentials live
only on the ROCK in ~/sd5531/private (mode 0600). This script never prints a stream
URI or a password, and never stores a password.
"""
import argparse, getpass, hashlib, io, ipaddress, json, os, re, shlex, shutil, socket
import subprocess, sys, tarfile, time, urllib.request, webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                       # repository root
CONFIG = ROOT / '.local' / 'wired-lab.json'
SRC = ROOT / 'project-camera' / 'src' / 'recorder'
CODE = ['recorder.py', 'tracker.py', 'webview.py', 'webview.html', 'cam_time.py',
        'start.sh', 'stop.sh', 'test_recorder.py', 'test_tracker.py', 'test_webview.py']
SELF_TEST = ['test_recorder.AnalyzerTests', 'test_recorder.RulesTests', 'test_recorder.TrackerTests',
             'test_tracker.TrackerTests', 'test_tracker.ColourTests']
REMOTE = '~/sd5531'
SOCKET = '/tmp/sd5531-lab-ssh.sock'          # shared with the older launchers on the first Mac
NAME = re.compile(r'^[0-9]{8}-[0-9]{6}-[0-9a-f]{6}\.(json|mp4)$')
DIRECT = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # lab LAN: never via a proxy


def say(msg=''):
    print(msg, flush=True)


def fail(msg):
    say('✗ ' + msg)
    sys.exit(1)


# ---------------------------------------------------------------- configuration

def load_config():
    if not CONFIG.exists():
        fail(f'没有私有网络配置 {CONFIG.relative_to(ROOT)}。先运行：python3 project-camera/demo/demo.py setup')
    c = json.loads(CONFIG.read_text())
    if c.get('example_only'):
        fail(f'{CONFIG.relative_to(ROOT)} 还是示例（example_only: true），请填写现场地址。')
    board = ipaddress.ip_interface(c['board']['ethernet_cidr'])
    host = ipaddress.ip_interface(c['mac']['ethernet_cidr'])
    camera = ipaddress.ip_address(c['camera']['ipv4'])
    if board.network != host.network or camera not in host.network:
        fail('配置里本机、ROCK、摄像头不在同一个有线网段。')
    return {'board_ip': str(board.ip), 'host_cidr': str(host), 'camera_ip': str(camera),
            'user': c['board']['ssh_user'], 'alias': c['board']['ssh_host_key_alias'],
            'rtsp_port': int(c['camera'].get('rtsp_port', 554)), 'onvif_port': int(c['camera'].get('onvif_port', 8899))}


def ask(prompt, default=None, check=None):
    while True:
        v = input(f'{prompt}' + (f' [{default}]' if default else '') + '：').strip() or (default or '')
        if v and (check is None or check(v)):
            return v
        say('  格式不对，请重新输入。')


def is_ip(v):
    try:
        ipaddress.ip_address(v)
        return True
    except ValueError:
        return False


def is_cidr(v):
    try:
        return '/' in v and bool(ipaddress.ip_interface(v))
    except ValueError:
        return False


def create_config():
    """Ask for the site values and write the private config (0600, in an 0700 dir)."""
    say('\n还没有私有网络配置。如果这台主机之外已有一份（项目原来那台电脑上的')
    say(f'{CONFIG.relative_to(ROOT)}），直接复制过来最省事，然后重新运行 setup。')
    say('否则现在按现场填写（地址见接线时设置的静态地址）：\n')
    host = ask('本机有线网卡的静态地址和前缀，例如 192.168.x.y/24', check=is_cidr)
    iface = ask('本机有线网卡名称（macOS 在“系统设置 › 网络”或 ifconfig 查看，Linux 用 ip addr）',
                check=lambda v: re.fullmatch(r'[A-Za-z0-9_.:-]+', v))
    board = ask('ROCK 的静态地址（不含前缀）', check=is_ip)
    user = ask('ROCK 登录用户名', 'radxa', check=lambda v: re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', v))
    camera = ask('摄像头地址', check=is_ip)
    prefix = ipaddress.ip_interface(host).network.prefixlen
    c = {'schema_version': 1, 'example_only': False,
         'mac': {'ethernet_interface': iface, 'ethernet_cidr': host, 'wifi_interface': 'unknown-wifi'},
         'board': {'ethernet_interface': 'eth0', 'ethernet_cidr': f'{board}/{prefix}', 'profile_id': 'lab-wired',
                   'profile_uuid': '00000000-0000-0000-0000-000000000000', 'ssh_user': user,
                   'ssh_host_key_alias': 'sd5531-rock'},
         'camera': {'ipv4': camera, 'rtsp_port': 554, 'onvif_port': 8899}}
    CONFIG.parent.mkdir(mode=0o700, exist_ok=True)
    CONFIG.write_text(json.dumps(c, indent=2) + '\n')
    os.chmod(CONFIG, 0o600)
    say(f'✓ 已写入 {CONFIG.relative_to(ROOT)}（仅本机，不进 Git）。')
    say('  注：网络检查器 check_network.py 还需要 wifi_interface 和 ROCK 连接 UUID，demo 不需要。')


# ---------------------------------------------------------------- SSH

def ssh_base(cfg, strict='yes'):
    return ['ssh', '-S', SOCKET, '-o', 'HostKeyAlias=' + cfg['alias'], '-o', 'StrictHostKeyChecking=' + strict,
            '-o', 'ConnectTimeout=8', f"{cfg['user']}@{cfg['board_ip']}"]


def ssh_alive(cfg):
    return subprocess.run(ssh_base(cfg)[:3] + ['-O', 'check', ssh_base(cfg)[-1]],
                          capture_output=True).returncode == 0


def ensure_ssh(cfg, first=False):
    """One password prompt opens a shared connection kept for 4 hours."""
    if ssh_alive(cfg):
        return
    if os.path.exists(SOCKET):
        os.remove(SOCKET)
    if first:
        say('\n首次连接这台 ROCK 时，SSH 会显示它的主机密钥指纹并问是否信任。')
        say('请先核对指纹：在 ROCK 本机（接显示器）运行 ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub，')
        say('或在原来那台已信任的电脑上运行 ssh-keygen -l -F ' + cfg['alias'] + '。一致才输入 yes。')
    say('连接 ROCK。出现 password 提示时，输入 ROCK 的登录密码。')
    cmd = ssh_base(cfg, 'ask' if first else 'yes')
    r = subprocess.run(cmd[:-1] + ['-f', '-N', '-M', '-o', 'ControlPersist=4h', cmd[-1]])
    if r.returncode or not ssh_alive(cfg):
        fail('无法登录 ROCK：检查网线、ROCK 电源和密码；首次使用请运行 setup。')


def rock(cfg, command, data=None, check=True, timeout=120):
    r = subprocess.run(ssh_base(cfg) + [command], input=data, capture_output=True, timeout=timeout)
    if check and r.returncode:
        fail(f'ROCK 上执行失败：{command[:60]}…\n{r.stderr.decode(errors="replace")[-400:]}')
    return r


def rock_text(cfg, command, **kw):
    return rock(cfg, command, **kw).stdout.decode(errors='replace')


# ---------------------------------------------------------------- checks

def port_open(ip, port, timeout=3):
    try:
        with socket.create_connection((ip, port), timeout):
            return True
    except OSError:
        return False


def check_network(cfg):
    ok = True
    for what, ip, port in [('ROCK SSH', cfg['board_ip'], 22), ('摄像头 RTSP', cfg['camera_ip'], cfg['rtsp_port']),
                           ('摄像头 ONVIF', cfg['camera_ip'], cfg['onvif_port'])]:
        up = port_open(ip, port)
        say(f"  {'✓' if up else '✗'} {what} 端口可达" if up else f'  ✗ {what} 连不上（{ip}:{port}）')
        ok &= up
    if not ok:
        say('  → 检查：本机有线网卡是否设成配置里的静态地址、网线和交换机灯、ROCK 是否通电。')
    return ok


def clock_offset(cfg, samples=5):
    """Host minus ROCK clock in seconds, from the lowest round-trip sample."""
    best = None
    for _ in range(samples):
        t0 = time.time()
        out = rock_text(cfg, 'date +%s.%N')
        t1 = time.time()
        if best is None or t1 - t0 < best[1]:
            best = ((t0 + t1) / 2 - float(out), t1 - t0)
    return best[0]


def set_board_clock(cfg, offset):
    say(f'ROCK 时间与本机相差 {offset:+.2f} 秒，需要校准（录像的时间戳都用 ROCK 时间）。')
    password = getpass.getpass('请输入 ROCK 登录密码以执行 sudo（输入时不显示）：')
    # The offset is applied on the ROCK after sudo accepts, so typing time does not matter.
    apply = ("import subprocess,time;"
             f"t=time.time()+{offset!r};"
             "subprocess.run(['date','-u','-s','@%.6f'%t],check=True,stdout=subprocess.DEVNULL)")
    r = rock(cfg, "sudo -S -p '' python3 -c " + shlex.quote(apply), data=(password + '\n').encode(), check=False)
    del password
    if r.returncode:
        fail('校准失败：密码不对或 sudo 被拒绝。ROCK 时间未改。')
    after = clock_offset(cfg)
    say(f'✓ ROCK 时间已校准（剩余偏差 {after * 1000:.0f} 毫秒）。')


def camera_clock(cfg, fix=True):
    """The camera forgets a manually set time on power loss; set it from the ROCK."""
    def offset(mode):
        out = rock_text(cfg, f"python3 {REMOTE}/recorder/cam_time.py {cfg['onvif_port']} {mode}", check=False).strip()
        try:
            return json.loads(out.splitlines()[-1])['camera_minus_board_s']
        except (ValueError, IndexError, KeyError):
            return None
    cam = offset('check')
    if cam is None:
        say('  ! 读不到摄像头时间（不影响录制，只影响画面左上角的时间）。')
    elif abs(cam) > 1 and fix:
        after = offset('set')
        say(f'  ✓ 摄像头画面时间已按 ROCK 校准（原差 {cam:+.1f} 秒，现差 {after:+.1f} 秒）。'
            if after is not None and abs(after) <= 1 else f'  ! 摄像头时间校准未成功（读回 {after}）。')
    else:
        say(f'  ✓ 摄像头画面时间正常（差 {cam:+.1f} 秒）。')


def rock_prereqs(cfg):
    out = rock_text(cfg, 'python3 -c "import sys;print(sys.version_info[:2] >= (3, 9))"; '
                         'command -v ffmpeg >/dev/null && echo ffmpeg; command -v ffprobe >/dev/null && echo ffprobe; '
                         f'df -Pm {REMOTE} 2>/dev/null | tail -1 || df -Pm ~ | tail -1', check=False)
    missing = []
    if 'True' not in out:
        missing.append('Python 3.9+')
    for tool in ('ffmpeg', 'ffprobe'):
        if tool not in out.split():
            missing.append(tool)
    if missing:
        fail('ROCK 缺少：' + '、'.join(missing) + '。需要临时联网后在 ROCK 上运行：sudo apt install -y ffmpeg python3')
    say('  ✓ ROCK 上有 Python 3.9+、ffmpeg、ffprobe')


# ---------------------------------------------------------------- deploy

def code_digest():
    return {f: hashlib.sha256((SRC / f).read_bytes()).hexdigest() for f in CODE}


def remote_digest(cfg):
    out = rock_text(cfg, f'cd {REMOTE}/recorder 2>/dev/null && sha256sum ' + ' '.join(CODE), check=False)
    return {line.split()[1]: line.split()[0] for line in out.splitlines() if len(line.split()) == 2}


def deploy(cfg):
    """Copy the recorder code to the ROCK (the ROCK has no rsync). Keeps config.json and the
    detection area; returns True if anything changed."""
    if remote_digest(cfg) == code_digest():
        say('  ✓ ROCK 上的程序与本仓库一致')
        return False
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w:gz') as tar:
        for f in CODE:
            tar.add(SRC / f, arcname=f)
    rock(cfg, f'mkdir -p {REMOTE}/recorder {REMOTE}/events && tar xzf - -C {REMOTE}/recorder', data=buf.getvalue())
    if remote_digest(cfg) != code_digest():
        fail('部署后 ROCK 上的文件校验不一致。')
    say('  ✓ 程序已部署到 ROCK（SHA-256 核对一致）')
    return True


def ensure_rock_config(cfg):
    """Write config.json on the ROCK if it has none, from the demo template."""
    if rock(cfg, f'test -f {REMOTE}/recorder/config.json', check=False).returncode == 0:
        say('  ✓ ROCK 上已有 config.json，保留不变')
        return
    c = json.loads((HERE / 'rock-config.json').read_text())
    c['web']['bind'] = cfg['board_ip']
    rock(cfg, f'cat > {REMOTE}/recorder/config.json', data=(json.dumps(c, indent=2) + '\n').encode())
    say('  ✓ 已在 ROCK 上写入 config.json（demo 默认参数）')


def stream_uri(cfg, user, password, stream):
    # This camera (GK7205V200 firmware) takes the credentials in the RTSP path.
    return (f"rtsp://{cfg['camera_ip']}:{cfg['rtsp_port']}/user={user}_password={password}"
            f"_channel=0_stream={stream}&onvif=0.sdp?real_stream")


def ensure_camera_files(cfg):
    """Stream URIs (with camera credentials) only ever exist on the ROCK, mode 0600."""
    have = rock(cfg, f'test -f {REMOTE}/private/camera_source.json && test -f {REMOTE}/private/camera_substream.json',
                check=False).returncode == 0
    if have:
        say('  ✓ ROCK 上已有摄像头私有配置，保留不变')
        return
    say('\nROCK 上还没有摄像头码流配置。请输入摄像头的 RTSP 登录信息（只写到 ROCK 上，权限 0600）。')
    user = input('摄像头用户名 [admin]：').strip() or 'admin'
    password = getpass.getpass('摄像头密码（输入时不显示；没有就直接回车）：')
    for name, stream, profile in (('camera_source.json', 0, 'main'), ('camera_substream.json', 1, 'sub')):
        body = json.dumps({'profile': profile, 'uri': stream_uri(cfg, user, password, stream)}).encode()
        rock(cfg, f'umask 077 && mkdir -p {REMOTE}/private && cat > {REMOTE}/private/{name}', data=body)
    del password
    say('  ✓ 摄像头私有配置已写到 ROCK')


def check_streams(cfg):
    """Decode a moment of both streams on the ROCK; reports size and codec only."""
    ok = True
    for name, label in (('camera_source.json', '主码流'), ('camera_substream.json', '子码流')):
        probe = ("import json,subprocess,sys;"
                 f"u=json.load(open(__import__('os').path.expanduser('{REMOTE}/private/{name}')))['uri'];"
                 "r=subprocess.run(['ffprobe','-v','error','-rtsp_transport','tcp','-timeout','8000000','-select_streams','v:0',"
                 "'-show_entries','stream=codec_name,width,height','-of','csv=p=0',u],capture_output=True,text=True,timeout=20);"
                 "print(r.stdout.strip() or 'FAIL')")
        out = rock_text(cfg, 'python3 -c ' + shlex.quote(probe), check=False).strip()
        good = out and out != 'FAIL'
        ok &= bool(good)
        say(f'  {"✓" if good else "✗"} {label}：{out if good else "读不到（检查摄像头密码、网线）"}')
    return ok


def self_test(cfg):
    r = rock(cfg, f'cd {REMOTE}/recorder && python3 -m unittest -q ' + ' '.join(SELF_TEST), check=False, timeout=300)
    tail = r.stderr.decode(errors='replace').strip().splitlines()[-1:] or ['']
    say(f'  {"✓" if r.returncode == 0 else "✗"} ROCK 上的自检：{tail[0]}')
    return r.returncode == 0


# ---------------------------------------------------------------- running

def api(cfg, path, timeout=4):
    with DIRECT.open(f"http://{cfg['board_ip']}:8080{path}", timeout=timeout) as r:
        return r.read()


def status_json(cfg):
    try:
        return json.loads(api(cfg, '/api/status'))
    except (OSError, ValueError):
        return None


def wait_running(cfg, seconds=20):
    end = time.time() + seconds
    while time.time() < end:
        s = status_json(cfg)
        r = s and s.get('recorder')
        if r and s['board_time'] - r['t'] < 5 and r['segmenter_alive'] and r['detector_alive']:
            return s
        time.sleep(1)
    return None


def live_frame(cfg):
    try:
        with DIRECT.open(f"http://{cfg['board_ip']}:8080/snapshot.jpg", timeout=10) as r:
            data = r.read()
        return data[:2] == b'\xff\xd8'
    except OSError:
        return False


def recordings_dir(args):
    d = Path(args.recordings or os.environ.get('SD5531_RECORDINGS') or ROOT.parent / 'recordings').expanduser()
    d.mkdir(parents=True, exist_ok=True)
    return d


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sync(cfg, local):
    """Move finished clips to this host: copy, check SHA-256 against the record, then delete
    the MP4 on the ROCK. The small JSON stays on the ROCK for the web timeline. Nothing on
    the host is ever deleted. Returns (new records, moved videos, failures)."""
    names = rock_text(cfg, f'cd {REMOTE}/events 2>/dev/null && ls -1 -- *.json *.mp4 2>/dev/null', check=False).split()
    names = [n for n in names if NAME.match(n)]
    on_board = {n for n in names if n.endswith('.mp4')}
    copied = moved = failed = 0
    for name in (n for n in names if n.endswith('.json')):
        local_json = local / name
        raw = local_json.read_bytes() if local_json.exists() else rock(cfg, f'cat {REMOTE}/events/{name}').stdout
        record = json.loads(raw)
        clip = record.get('file')
        if clip and not NAME.match(clip):
            continue
        if clip and clip in on_board:
            dest = local / clip
            if not (dest.exists() and sha256(dest) == record.get('sha256')):
                part = dest.with_suffix('.mp4.part')
                with open(part, 'wb') as out:
                    subprocess.run(ssh_base(cfg) + [f'cat {REMOTE}/events/{clip}'], stdout=out, check=True)
                if sha256(part) != record.get('sha256'):
                    part.unlink()
                    failed += 1
                    say(f'  ! {clip} 校验不符，ROCK 上的原片保留，下次重试')
                    continue
                part.replace(dest)
        if not local_json.exists():
            local_json.write_bytes(raw)
            copied += 1
        if clip and clip in on_board:
            rock(cfg, f'rm -f -- {REMOTE}/events/{clip}')
            moved += 1
    return copied, moved, failed


# ---------------------------------------------------------------- commands

def cmd_setup(args):
    say('== SD5531 demo 安装 ==\n')
    if sys.version_info < (3, 9):
        fail('本机 Python 需要 3.9 或更新。')
    if not shutil.which('ssh'):
        fail('本机没有 ssh 命令。')
    say('✓ 本机：Python %d.%d，ssh 可用' % sys.version_info[:2])
    if not CONFIG.exists():
        create_config()
    cfg = load_config()
    say('\n1. 网络')
    if not check_network(cfg):
        fail('网络不通，先按说明设置本机有线网卡。')
    say('\n2. 登录 ROCK')
    ensure_ssh(cfg, first=True)
    say('  ✓ 已登录（4 小时内不用再输密码）')
    say('\n3. ROCK 环境')
    rock_prereqs(cfg)
    say('\n4. 程序与配置')
    deploy(cfg)
    ensure_rock_config(cfg)
    ensure_camera_files(cfg)
    say('\n5. 检查')
    ok = check_streams(cfg)
    ok &= self_test(cfg)
    camera_clock(cfg, fix=False)
    off = clock_offset(cfg)
    say(f"  {'✓' if abs(off) <= 1 else '!'} ROCK 时间与本机相差 {off:+.2f} 秒" + ('' if abs(off) <= 1 else '（start 时会校准）'))
    say('\n' + ('✓ 安装完成。运行 start 开始录制。' if ok else '✗ 有检查没通过，见上面的 ✗ 项。'))
    sys.exit(0 if ok else 1)


def cmd_start(args):
    cfg = load_config()
    local = recordings_dir(args)
    if not check_network(cfg):
        fail('网络不通。')
    ensure_ssh(cfg)
    off = clock_offset(cfg)
    if abs(off) > 1:
        set_board_clock(cfg, off)
    else:
        say(f'✓ ROCK 时间正常（差 {off * 1000:.0f} 毫秒）')
    changed = deploy(cfg)
    ensure_rock_config(cfg)
    camera_clock(cfg)
    if changed:
        rock(cfg, f'sh {REMOTE}/recorder/stop.sh', check=False)
    say(rock_text(cfg, f'sh {REMOTE}/recorder/start.sh </dev/null').strip())
    s = wait_running(cfg)
    if not s:
        fail(f'录制程序没有正常运行。查看 ROCK 上的 /tmp/recorder.out 和 /tmp/webview.out。')
    r = s['recorder']
    say(f"✓ 录制程序运行中：缓存 {r['ring_seconds']} 秒，触发方式 {'守宫移动' if r.get('trigger') == 'gecko' else '画面变化'}，"
        f"检测区域 {'已设置' if r.get('roi') else '未设置（整幅画面）'}")
    say(f"  {'✓' if live_frame(cfg) else '✗'} 实时画面")
    url = f"http://{cfg['board_ip']}:8080/"
    say(f'网页：{url}')
    if not args.no_browser:
        webbrowser.open(url)
    say(f'录好的片段会移到：{local}')
    if args.once:
        report_sync(sync(cfg, local), local)
        return
    say('这个窗口开着就每 10 秒转存一次；按 Ctrl-C 只停止转存，ROCK 继续录制。停止录制请运行 stop。')
    try:
        while True:
            try:
                report_sync(sync(cfg, local), local)
            except (subprocess.SubprocessError, OSError, ValueError) as e:
                say(f'{time.strftime("%H:%M:%S")} 转存失败（{type(e).__name__}），10 秒后重试')
            time.sleep(10)
    except KeyboardInterrupt:
        say('\n已停止转存。ROCK 仍在录制，新片段暂存在 ROCK 上，下次 start 或 stop 时转存。')


def report_sync(result, local):
    copied, moved, failed = result
    if copied or moved or failed:
        total = sum(1 for p in local.glob('*.json'))
        say(f'{time.strftime("%H:%M:%S")} 新存入 {copied} 段，从 ROCK 移走 {moved} 个视频'
            + (f'，{failed} 个校验失败待重试' if failed else '') + f'（共 {total} 段）')


def cmd_stop(args):
    cfg = load_config()
    ensure_ssh(cfg)
    say(rock_text(cfg, f'sh {REMOTE}/recorder/stop.sh', check=False).strip() or '已停止')
    report_sync(sync(cfg, recordings_dir(args)), recordings_dir(args))
    say('✓ 录制已停止，片段已转存。')


def cmd_sync(args):
    cfg = load_config()
    ensure_ssh(cfg)
    local = recordings_dir(args)
    report_sync(sync(cfg, local), local)
    say(f'✓ 转存完成：{local}')


def cmd_status(args):
    cfg = load_config()
    check_network(cfg)
    s = status_json(cfg)
    if not s or not s.get('recorder'):
        say('✗ 网页或录制程序没有运行（运行 start）。')
        return
    r = s['recorder']
    fresh = s['board_time'] - r['t'] < 5
    tr = r.get('tracker') or {}
    say(f"{'✓' if fresh else '✗'} 录制程序{'运行中' if fresh else '没有更新状态'}；缓存 {r['ring_seconds']} 秒；"
        f"切片 {'正常' if r['segmenter_alive'] else '停止'}；检测 {'正常' if r['detector_alive'] else '停止'}")
    say(f"  触发方式：{'守宫移动' if r.get('trigger') == 'gecko' else '画面变化'}；检测区域：{'已设置' if r.get('roi') else '整幅画面'}")
    labels = {'learning': '正在生成背景', 'searching': '未锁定（等它第一次移动）', 'moving': '移动中',
              'still': '静止', 'lost': '丢失（最后出现位置已记录）'}
    say(f"  守宫：{labels.get(tr.get('state'), tr.get('state', '—'))}" + (f"，位置 ({tr['x']:.2f}, {tr['y']:.2f})" if 'x' in tr else ''))
    say(f"  正在录制：{'是' if r.get('open_event') else '否'}；待保存 {r.get('pending_events', 0)}")
    if ssh_alive(cfg):
        off = clock_offset(cfg)
        say(f"  {'✓' if abs(off) <= 1 else '!'} ROCK 时间与本机差 {off:+.2f} 秒")


def main(argv=None):
    p = argparse.ArgumentParser(description='SD5531 gecko recording demo')
    p.add_argument('command', choices=['setup', 'start', 'stop', 'status', 'sync'])
    p.add_argument('--recordings', help='where clips are moved (default: ../recordings next to the repository)')
    p.add_argument('--no-browser', action='store_true', help='start: do not open the web page')
    p.add_argument('--once', action='store_true', help='start: transfer once and exit instead of every 10 s')
    args = p.parse_args(argv)
    {'setup': cmd_setup, 'start': cmd_start, 'stop': cmd_stop, 'status': cmd_status, 'sync': cmd_sync}[args.command](args)


if __name__ == '__main__':
    main()
