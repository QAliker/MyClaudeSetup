#!/usr/bin/env python3
"""PreToolUse(Bash) guard: the human commits, not the agent.

Blocks `git commit` / `git push` (incl. via wrappers like `rtk git commit`).
Everything else — status, diff, add, log — passes. Exit 2 = deny + tell Claude why.
"""
import json
import re
import sys

# ponytail: matches `git ... commit|push` with optional flags between.
# Ceiling: also trips on contrived cases like `git log --grep=commit`.
# Tighten only if that bites.
BLOCK = re.compile(r"(^|[\s;&|(])git(\s+-\S+)*\s+(commit|push)\b")


def blocked(cmd: str) -> bool:
    return bool(BLOCK.search(cmd))


def main() -> int:
    try:
        cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except Exception:
        return 0  # can't parse → don't get in the way
    if blocked(cmd):
        print(
            "Blocked by QT-kit commit-guard: you commit and push, not the agent. "
            "Stage nothing, leave the commit to the human. "
            "If you truly need this, the human runs it themselves.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert blocked("git commit -m x")
        assert blocked("rtk git commit -am x")
        assert blocked("git push origin main")
        assert blocked("git push")
        assert not blocked("git status")
        assert not blocked("git add -A")
        assert not blocked("git diff --staged")
        assert not blocked("grep commit file.txt")
        print("ok")
        sys.exit(0)
    sys.exit(main())
