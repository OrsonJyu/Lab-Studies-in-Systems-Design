import ipaddress
import subprocess
import unittest
from unittest.mock import patch

from check_network import inspect, interface_addresses, keys, overlaps, validate_config


def example():
    # Synthetic test-only network; these are not the deployed device addresses.
    return {'schema_version': 1, 'example_only': False,
            'mac': {'ethernet_interface': 'en99', 'ethernet_cidr': '10.243.19.20/24', 'wifi_interface': 'en98'},
            'board': {'ethernet_interface': 'testeth0', 'ethernet_cidr': '10.243.19.100/24',
                      'profile_id': 'lab-wired', 'profile_uuid': '11111111-2222-4333-8444-555555555555',
                      'ssh_user': 'testuser', 'ssh_host_key_alias': 'trusted-test-board'},
            'camera': {'ipv4': '10.243.19.10', 'rtsp_port': 554, 'onvif_port': 8899}}


class ConfigurationGuards(unittest.TestCase):
    def test_valid_private_plan(self):
        self.assertEqual(str(validate_config(example())[0].network), '10.243.19.0/24')

    def test_duplicate_endpoint_rejected(self):
        c = example(); c['camera']['ipv4'] = '10.243.19.100'
        with self.assertRaises(ValueError): validate_config(c)

    def test_prefix_mismatch_rejected(self):
        c = example(); c['board']['ethernet_cidr'] = '10.243.19.100/25'
        with self.assertRaises(ValueError): validate_config(c)

    def test_network_and_broadcast_rejected(self):
        for address in ('10.243.19.0', '10.243.19.255'):
            c = example(); c['camera']['ipv4'] = address
            with self.assertRaises(ValueError): validate_config(c)

    def test_public_network_rejected(self):
        c = example(); c['mac']['ethernet_cidr'] = '8.8.8.20/24'
        c['board']['ethernet_cidr'] = '8.8.8.100/24'; c['camera']['ipv4'] = '8.8.8.10'
        with self.assertRaises(ValueError): validate_config(c)

    def test_placeholder_and_legacy_profile_rejected(self):
        for field, value in [('profile_uuid', '<UUID>'), ('profile_id', 'school-camera')]:
            c = example(); c['board'][field] = value
            with self.assertRaises(ValueError): validate_config(c)
        c = example(); c['example_only'] = True
        with self.assertRaises(ValueError): validate_config(c)

    def test_invalid_command_fields_rejected(self):
        for section, field, value in [('mac', 'ethernet_interface', 'en99;reboot'),
                                      ('board', 'ssh_user', 'user@other-host'),
                                      ('board', 'ssh_host_key_alias', 'a b')]:
            c = example(); c[section][field] = value
            with self.assertRaises(ValueError): validate_config(c)

    def test_boolean_port_rejected(self):
        c = example(); c['camera']['rtsp_port'] = True
        with self.assertRaises(ValueError): validate_config(c)

    def test_uplink_overlap_detected_including_broader_prefix(self):
        net = validate_config(example())[0].network
        self.assertTrue(overlaps(net, [ipaddress.IPv4Interface('10.243.22.1/16')]))
        self.assertFalse(overlaps(net, [ipaddress.IPv4Interface('172.21.4.2/24')]))

    def test_macos_hex_mask_and_missing_address(self):
        text = 'en99: flags=UP\n inet 10.243.19.20 netmask 0xffffff00 broadcast 10.243.19.255\n status: active'
        self.assertEqual(interface_addresses(text), [ipaddress.IPv4Interface('10.243.19.20/24')])
        self.assertEqual(interface_addresses('status: active'), [])

    def test_host_key_comparison_ignores_host_label_and_comments(self):
        known = '# a comment\ntrusted-test-board ssh-ed25519 TESTKEY\n'
        scanned = 'test-endpoint ssh-ed25519 TESTKEY\n'
        self.assertTrue(keys(known) & keys(scanned))
        self.assertFalse(keys(known) & keys('test-endpoint ssh-ed25519 OTHERKEY\n'))

    def test_bad_local_preflight_never_probes_remote_endpoints(self):
        missing = subprocess.CompletedProcess([], 1, stdout='', stderr='')
        with patch('check_network.command', return_value=missing), patch('check_network.socket.create_connection') as connect:
            report = inspect(example(), 'home', remote=True)
            self.assertFalse(report['passed'])
            connect.assert_not_called()


if __name__ == '__main__':
    unittest.main()
