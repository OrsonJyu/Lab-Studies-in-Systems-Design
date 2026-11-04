#!/bin/zsh
# Set the ROCK system clock from this Mac's clock over the wired lab network.
# Measures the offset first, applies it after the sudo password, then re-measures.
# Leaves an SSH control socket open for 4 hours so follow-up checks need no password.
set -eu

helper="${0:A:h}/shared_network.py"
target="$(python3 "$helper" ssh-target)"
alias_name="$(python3 "$helper" host-alias)"
socket="/private/tmp/sd5531-lab-ssh.sock"
result="${0:A:h}/clock-sync-$(date +%Y%m%d-%H%M%S).json"

if ! /usr/bin/ssh -S "$socket" -O check "$target" >/dev/null 2>&1; then
  [[ -S "$socket" ]] && /bin/rm "$socket"
  print "第 1 步：连接 ROCK。出现 password 提示时，输入板卡登录密码。"
  /usr/bin/ssh -f -N -M -S "$socket" -o ControlPersist=4h \
    -o "HostKeyAlias=$alias_name" -o StrictHostKeyChecking=yes "$target"
fi

python3 - "$socket" "$target" "$alias_name" "$result" <<'PY'
import getpass, json, shlex, subprocess, sys, time

socket, target, alias_name, result_path = sys.argv[1:]
base = ['/usr/bin/ssh', '-S', socket, '-o', 'HostKeyAlias=' + alias_name,
        '-o', 'StrictHostKeyChecking=yes', target]


def measure(samples=7):
    """Return (offset_s, rtt_s) of the lowest-RTT sample; offset = Mac - ROCK."""
    best = None
    for _ in range(samples):
        t0 = time.time()
        out = subprocess.run(base + ['date', '+%s.%N'], capture_output=True, text=True, check=True).stdout
        t1 = time.time()
        offset = (t0 + t1) / 2 - float(out.strip())
        if best is None or (t1 - t0) < best[1]:
            best = (offset, t1 - t0)
    return best


def utc(ts):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(ts))


before, rtt_before = measure()
board_before = time.time() - before
print(f'ROCK 当前时间（UTC）：{utc(board_before)}，比 Mac 慢 {before:.3f} 秒。')
print('第 2 步：校准 ROCK 时间。')
# Read the sudo password here (never echoed or stored) and pipe it to sudo -S;
# a pseudo-terminal through the shared SSH socket did not deliver keystrokes.
password = getpass.getpass('请输入板卡登录密码（输入时不显示，输完按回车）：')
# The delta is applied on the board after sudo succeeds, so typing time does not matter.
apply = ("import subprocess,time;"
         f"t=time.time()+{before!r};"
         "subprocess.run(['date','-u','-s','@%.6f'%t],check=True,stdout=subprocess.DEVNULL)")
done = subprocess.run(base + ["sudo -S -p '' python3 -c " + shlex.quote(apply)],
                      input=password + '\n', capture_output=True, text=True, timeout=30)
del password
if done.returncode:
    sys.exit('校准失败：密码不对或 sudo 被拒绝。ROCK 时间没有修改，可以重新运行。')
after, rtt_after = measure()
state = subprocess.run(base + ['timedatectl', 'show', '-p', 'NTPSynchronized', '-p', 'NTP'],
                       capture_output=True, text=True).stdout.split()
report = {
    'mac_utc_at_set': utc(time.time()),
    'offset_before_s': round(before, 3), 'rtt_before_s': round(rtt_before, 4),
    'offset_after_s': round(after, 4), 'rtt_after_s': round(rtt_after, 4),
    'board_time_state_after': state,
    'method': 'Mac wall clock via SSH midpoint of lowest-RTT sample; applied with date -u -s on the ROCK',
    'camera_clock_changed': False,
}
with open(result_path, 'w') as f:
    json.dump(report, f, indent=1)
print(f'完成。校准后剩余偏差 {after * 1000:.1f} 毫秒（往返 {rtt_after * 1000:.1f} 毫秒）。')
print('结果已保存：' + result_path)
PY
print "可以关闭这个窗口。摄像头时间没有修改。"
