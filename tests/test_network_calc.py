"""Tests for the public network calculator."""

import json
import subprocess
import sys
import unittest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from network_calc import describe_network


class NetworkCalcTests(unittest.TestCase):
    @staticmethod
    def run_cli(*arguments: str) -> str:
        command = [sys.executable, "-m", "network_calc", *arguments]
        return subprocess.run(
            command, cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout

    def test_ipv4_host_input_is_normalized(self):
        self.assertEqual(
            {
                "address_count": 64,
                "broadcast_address": "192.0.2.191",
                "first_address": "192.0.2.128",
                "ip_version": 4,
                "last_address": "192.0.2.191",
                "netmask": "255.255.255.192",
                "network": "192.0.2.128/26",
                "network_address": "192.0.2.128",
                "prefix_length": 26,
            },
            describe_network("192.0.2.130/26"),
        )

    def test_ipv6_host_input_is_normalized(self):
        result = describe_network("2001:db8::9/126")
        self.assertEqual("2001:db8::8/126", result["network"])
        self.assertEqual("2001:db8::b", result["last_address"])
        self.assertEqual(6, result["ip_version"])
        self.assertNotIn("broadcast_address", result)

    def test_invalid_input_is_rejected(self):
        with self.assertRaises(ValueError):
            describe_network("not-a-network")

    def test_cli_output_is_deterministic_json(self):
        first = self.run_cli("198.51.100.7/32")
        second = self.run_cli("198.51.100.7/32")
        self.assertEqual(first, second)
        self.assertEqual("198.51.100.7/32", json.loads(first)["network"])

    def test_default_cli_output_remains_compact_and_compatible(self):
        self.assertEqual(
            '{"address_count": 1, "broadcast_address": "198.51.100.7", '
            '"first_address": "198.51.100.7", "ip_version": 4, '
            '"last_address": "198.51.100.7", "netmask": "255.255.255.255", '
            '"network": "198.51.100.7/32", '
            '"network_address": "198.51.100.7", "prefix_length": 32}\n',
            self.run_cli("198.51.100.7/32"),
        )

    def test_pretty_output_is_deterministic_and_semantically_equivalent(self):
        compact = self.run_cli("2001:db8::9/126")
        first = self.run_cli("--pretty", "2001:db8::9/126")
        second = self.run_cli("--pretty", "2001:db8::9/126")
        self.assertEqual(first, second)
        self.assertEqual(json.loads(compact), json.loads(first))
        self.assertEqual("2001:db8::8/126", json.loads(first)["network"])
        self.assertTrue(first.startswith('{\n  "address_count"'))


if __name__ == "__main__":
    unittest.main()
