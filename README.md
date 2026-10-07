# network-calc

`network-calc` is a dependency-free Python example that reports deterministic
facts about an IPv4 or IPv6 network.

## Why this repository exists

This repository is intentionally small.

I created it as the first public project under **Poulin Systems** to demonstrate
a way of working with AI that I have found increasingly useful: **learning and
building at the same time**.

The technical problem is deliberately modest. Given an IPv4 or IPv6 address and
prefix, the program reports deterministic facts about the resulting network.
That simplicity makes the project useful as a teaching surface. The networking
concepts can be examined, implemented, tested, challenged, and revised without
the surrounding complexity of a larger system.

The broader experiment is in the development process.

Rather than treating AI only as a code generator, I use it as part of an
iterative loop: explain a concept, test my understanding, implement it, inspect
the result, question assumptions, and improve the implementation. The goal is
not to remove the human from the work. It is to make the act of building
software part of the learning process itself.

This repository represents an early version of that idea. I have since
developed the approach further in other projects that are not yet public, but
this project captures the basic model in a small and inspectable form.

It also establishes several practices I intend to carry into later Poulin
Systems work:

- AI-assisted contributions should remain attributable and subject to human
  review;
- repository policy should be visible and testable rather than existing only as
  an informal convention;
- `main` should be protected and changes should arrive through reviewable pull
  requests;
- public work should have a deliberate boundary from private infrastructure and
  internal development history; and
- published code should contain only material intentionally prepared for a
  public audience.

For that reason, this repository was published with a new Git history rather
than exposing the history of the private systems used during development and
validation.

The implementation is dependency-free and includes a small deterministic
validator so that both the program and the expected public repository surface
can be checked locally.

This is not intended to become a large networking toolkit. It is a small
experiment in using AI to **teach, build, verify, and refine at the same time**—
and an early public example of a development model that I have continued to
expand elsewhere.

## Usage

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

`main` is protected by the repository policy in
[`policy/main-ruleset.json`](policy/main-ruleset.json). Changes use pull requests,
Louis owns review and integration through [CODEOWNERS](.github/CODEOWNERS), and
squash is the only allowed merge method. The ruleset requires a pull request but
does not require a second reviewer, so the sole human maintainer can integrate
an ordinary maintainer-authored change without an administrative bypass.

## License

No license has been selected. The source is publicly viewable if published, but
no permission to copy, modify, or redistribute it is granted until a license is
added by the owner.
