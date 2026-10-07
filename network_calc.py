"""Deterministic IPv4 and IPv6 network facts."""

import argparse
import ipaddress
import json


def describe_network(value: str) -> dict[str, object]:
    """Return stable, JSON-serializable facts for an IP network."""
    network = ipaddress.ip_network(value, strict=False)
    result: dict[str, object] = {
        "address_count": network.num_addresses,
        "first_address": str(network.network_address),
        "ip_version": network.version,
        "last_address": str(network[-1]),
        "netmask": str(network.netmask),
        "network": str(network),
        "network_address": str(network.network_address),
        "prefix_length": network.prefixlen,
    }
    if network.version == 4:
        result["broadcast_address"] = str(network.broadcast_address)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("network", help="IPv4 or IPv6 address with prefix length")
    args = parser.parse_args(argv)
    try:
        result = describe_network(args.network)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, sort_keys=True, separators=(", ", ": ")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
