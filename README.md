# network-calc

`network-calc` is a dependency-free Python example that reports deterministic
facts about an IPv4 or IPv6 network.

```console
$ python3 -m network_calc 192.0.2.130/26
{"address_count": 64, "broadcast_address": "192.0.2.191", "first_address": "192.0.2.128", "ip_version": 4, "last_address": "192.0.2.191", "netmask": "255.255.255.192", "network": "192.0.2.128/26", "network_address": "192.0.2.128", "prefix_length": 26}
```

The input is parsed with Python's standard-library `ipaddress` module using
non-strict network semantics. Output keys and JSON formatting are stable.

## Development

```console
python3 -m unittest discover -s tests -v
python3 tools/validate.py
```

`main` is designed to be protected by the repository policy in
[`policy/main-ruleset.json`](policy/main-ruleset.json). Changes use pull requests,
Louis owns review through [CODEOWNERS](.github/CODEOWNERS), and squash is the only
allowed merge method.

## License

No license has been selected. The source is publicly viewable if published, but
no permission to copy, modify, or redistribute it is granted until a license is
added by the owner.
