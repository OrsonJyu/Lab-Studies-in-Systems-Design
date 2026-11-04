#!/usr/bin/env python3
"""Read-only macOS preflight for the shared wired camera network (Python 3.9+)."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import uuid

PRIVATE = tuple(ipaddress.ip_network(n) for n in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'))


def validate_config(c):
    if c.get('schema_version') != 1 or c.get('example_only', False):
        raise ValueError('Fill a private configuration; the example cannot run')
    mac = ipaddress.IPv4Interface(c['mac']['ethernet_cidr'])
    board = ipaddress.IPv4Interface(c['board']['ethernet_cidr'])
    camera = ipaddress.IPv4Address(c['camera']['ipv4'])
    net = mac.network
    if board.network != net or camera not in net:
        raise ValueError('All three roles must use one wired subnet and prefix')
    if net.prefixlen > 29 or not any(net.subnet_of(p) for p in PRIVATE):
        raise ValueError('Use a suitable RFC1918 wired subnet with at least three usable addresses')
    if len({mac.ip, board.ip, camera}) != 3 or any(a in (net.network_address, net.broadcast_address) for a in (mac.ip, board.ip, camera)):
        raise ValueError('Role addresses must be distinct usable host addresses')
    for section, key in [('mac', 'ethernet_interface'), ('mac', 'wifi_interface'),
                         ('board', 'ethernet_interface'), ('board', 'ssh_host_key_alias')]:
        if not re.fullmatch(r'[A-Za-z0-9_.:-]+', c[section][key]):
            raise ValueError('Invalid interface or trusted-host name')
    if c['mac']['ethernet_interface'] == c['mac']['wifi_interface']:
        raise ValueError('Wired and Wi-Fi interfaces must be distinct')
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*', c['board']['ssh_user']):
        raise ValueError('Invalid SSH user')
    uuid.UUID(c['board']['profile_uuid'])
    if c['board']['profile_id'] != 'lab-wired':
        raise ValueError('Shared runtime profile must be lab-wired; migrate by its existing UUID')
    for key in ('rtsp_port', 'onvif_port'):
        p = c['camera'][key]
        if type(p) is not int or not 1 <= p <= 65535:
            raise ValueError('Invalid camera port')
    return mac, board, camera


def interface_addresses(text):
    result = []
    for host, mask in re.findall(r'\binet (\S+) netmask (\S+)', text):
        dotted = str(ipaddress.IPv4Address(int(mask, 16))) if mask.startswith('0x') else mask
        result.append(ipaddress.IPv4Interface(host + '/' + dotted))
    return result


def overlaps(network, addresses):
    return any(network.overlaps(a.network) for a in addresses)


def command(args, timeout=8, **kwargs):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout, **kwargs)
    except (OSError, subprocess.TimeoutExpired):
        return None


def keys(text):
    return {tuple(f[1:3]) for line in text.splitlines() if not line.startswith('#')
            and len(f := line.split()) >= 3}


def remote_script(c):
    expected = {'interface': c['board']['ethernet_interface'],
                'uuid': c['board']['profile_uuid'], 'id': c['board']['profile_id'],
                'cidr': c['board']['ethernet_cidr'], 'camera': c['camera']['ipv4']}
    return "expected = " + repr(expected) + '''
import json, subprocess
def get(field):
    return subprocess.check_output(['nmcli','-g',field,'connection','show','uuid',expected['uuid']],text=True).strip()
active = subprocess.check_output(['nmcli','-t','-f','UUID,DEVICE','connection','show','--active'],text=True).splitlines()
route = json.loads(subprocess.check_output(['ip','-j','route','get',expected['camera']],text=True))[0]
wireless = []
for row in subprocess.check_output(['nmcli','-t','-f','UUID,TYPE','connection','show'],text=True).splitlines():
    key, kind = row.split(':',1)
    if kind in ('wifi','802-11-wireless'):
        wireless.append(subprocess.check_output(['nmcli','-g','connection.autoconnect','connection','show','uuid',key],text=True).strip() == 'no')
print(json.dumps({
    'profile_id_matches': get('connection.id') == expected['id'],
    'active_uuid_matches': expected['uuid']+':'+expected['interface'] in active,
    'autoconnect_enabled': get('connection.autoconnect') == 'yes',
    'priority_matches': get('connection.autoconnect-priority') == '100',
    'address_matches': get('ipv4.addresses') == expected['cidr'],
    'wired_never_default': get('ipv4.never-default') == 'yes',
    'camera_route_wired': route.get('dev') == expected['interface'],
    'optional_wifi_manual': all(wireless),
    'recording_not_started_by_check': True
}))
'''


def make_report(checks, environment):
    return {'schema_version': 1, 'environment': environment,
            'observed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'tool': 'shared-wired-preflight/1', 'read_only': True,
            'checks': checks, 'passed': all(x['status'] == 'ok' for x in checks),
            'limits': 'No recording, decoding, reboot, endurance, camera clock or site-isolation validation is performed by this tool.'}


def inspect(c, environment, remote=False, interactive=False, control_path=None):
    mac, board, camera = validate_config(c)
    checks = []

    def add(name, ok, detail, severity='fail'):
        checks.append({'check': name, 'status': 'ok' if ok else severity, 'detail': detail})

    wired = command(['ifconfig', c['mac']['ethernet_interface']])
    text = wired.stdout if wired and wired.returncode == 0 else ''
    add('mac_wired_link', 'status: active' in text, 'Configured wired interface must have carrier')
    add('mac_wired_address', mac in interface_addresses(text), 'Configured static address and prefix must be present')
    wifi = command(['ifconfig', c['mac']['wifi_interface']])
    uplink = interface_addresses(wifi.stdout) if wifi and wifi.returncode == 0 else []
    add('uplink_subnet_distinct', not overlaps(mac.network, uplink), 'Overlapping Wi-Fi/VPN networks require review; do not automatically renumber devices')
    for name, host in [('board', str(board.ip)), ('camera', str(camera))]:
        route = command(['route', '-n', 'get', host])
        m = re.search(r'\binterface:\s+(\S+)', route.stdout) if route else None
        add(name+'_route_wired', bool(m and m[1] == c['mac']['ethernet_interface']), 'Endpoint route must use the configured wired interface')

    if any(x['status'] == 'fail' for x in checks):
        add('endpoint_checks', False, 'Skipped until local address, subnet and route checks pass', 'warn')
        return make_report(checks, environment)

    endpoints = [('board_ssh', str(board.ip), 22),
                 ('camera_rtsp', str(camera), c['camera']['rtsp_port']),
                 ('camera_onvif_tcp', str(camera), c['camera']['onvif_port'])]

    def probe(item):
        name, host, port = item
        try:
            with socket.create_connection((host, port), timeout=3):
                return name, True
        except OSError:
            return name, False

    with ThreadPoolExecutor(max_workers=3) as pool:
        for name, ok in pool.map(probe, endpoints):
            add(name, ok, 'TCP only; camera protocol and decoding are separate checks')

    alias = c['board']['ssh_host_key_alias']
    known = command(['ssh-keygen', '-F', alias])
    scanned = command(['ssh-keyscan', '-T', '3', '-t', 'ed25519', str(board.ip)])
    trusted = bool(known and scanned and keys(known.stdout) & keys(scanned.stdout))
    add('board_host_key', trusted, 'Must match the existing trusted key; never disables verification or edits known_hosts')
    if remote and trusted and not any(x['status'] == 'fail' for x in checks):
        args = ['ssh', '-T', '-o', 'StrictHostKeyChecking=yes', '-o', 'HostKeyAlias='+alias,
                '-o', 'ConnectTimeout=5', '-o', 'IPQoS=none',
                '-o', 'BatchMode='+('no' if interactive else 'yes')]
        if control_path:
            args += ['-S', control_path]
        args += [c['board']['ssh_user']+'@'+str(board.ip), 'python3', '-']
        result = command(args, timeout=90 if interactive else 20, input=remote_script(c))
        if result and result.returncode == 0:
            try:
                values = json.loads(result.stdout)
                if not isinstance(values, dict) or not values or any(type(v) is not bool for v in values.values()):
                    raise ValueError('Unexpected report')
                for name, value in values.items():
                    add('board_'+name, value, 'Read-only board state check')
            except (ValueError, TypeError):
                add('board_remote_state', False, 'Remote response was not a valid health report')
        else:
            add('board_remote_state', False, 'Authentication/session unavailable; use --interactive in Terminal or an existing SSH control path', 'warn')
    else:
        add('board_remote_state', False, 'Remote activation/autoconnect state was not checked', 'warn')
    return make_report(checks, environment)


def save_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False) as f:
        json.dump(report, f, indent=2)
        f.write('\n')
        staged = Path(f.name)
    staged.chmod(0o600)
    staged.replace(path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', required=True, type=Path)
    p.add_argument('--environment', required=True, choices=('home', 'school', 'hotspot'))
    p.add_argument('--remote', action='store_true')
    p.add_argument('--interactive', action='store_true', help='Allow SSH password prompt in the caller Terminal; never stores credentials')
    p.add_argument('--ssh-control-path', help='Optional caller-owned existing SSH master socket')
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    try:
        report = inspect(json.loads(args.config.read_text()), args.environment,
                         args.remote, args.interactive, args.ssh_control_path)
        if args.report:
            save_report(args.report, report)
        print(json.dumps(report, indent=2))
        return 0 if report['passed'] else (1 if any(c['status'] == 'fail' for c in report['checks']) else 2)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        p.exit(1, 'Configuration/check failed: '+type(exc).__name__+'. Check the private config and required macOS tools.\n')


if __name__ == '__main__':
    raise SystemExit(main())
