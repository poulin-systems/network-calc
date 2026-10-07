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
        command = [sys.executable, "-m", "network_calc", "198.51.100.7/32"]
        first = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
        second = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual("198.51.100.7/32", json.loads(first.stdout)["network"])


if __name__ == "__main__":
    unittest.main()
