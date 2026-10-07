#!/usr/bin/env python3
"""Validate the public candidate without network access or dependencies."""

import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    ".github/CODEOWNERS",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "SECURITY.md",
    "network_calc.py",
    "policy/main-ruleset.json",
    "policy/repository-settings.json",
    "tests/test_network_calc.py",
    "tools/validate.py",
}


def main() -> int:
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts
        and "__pycache__" not in path.relative_to(ROOT).parts
    }
    if actual != EXPECTED:
        raise SystemExit("public file allowlist mismatch")

    for relative in sorted(EXPECTED):
        raw = (ROOT / relative).read_bytes()
        indicators = (b"BEGIN " + b"PRIVATE KEY", b"github" + b"_pat_")
        if any(indicator in raw for indicator in indicators):
            raise SystemExit("credential indicator detected")
        if relative.endswith(".py"):
            ast.parse(raw, filename=relative)
        if relative.endswith(".json"):
            json.loads(raw)

    subprocess.run(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )
    inventory = {
        relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        for relative in sorted(EXPECTED)
    }
    print(json.dumps({"files": inventory, "status": "PASS"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
