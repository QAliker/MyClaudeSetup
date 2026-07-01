#!/usr/bin/env python3
"""PostToolUse(Edit|Write) formatter: format the file just edited.

Runs only when the right tool is installed (and, for prettier, only when the
project actually configures it). Never fails the edit — exit 0 no matter what.
"""
import json
import os
import shutil
import subprocess
import sys

PRETTIER_EXT = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json",
    ".css", ".scss", ".less", ".html", ".vue", ".md", ".mdx", ".yaml", ".yml",
}
PRETTIER_CONFIGS = (
    ".prettierrc", ".prettierrc.json", ".prettierrc.yaml", ".prettierrc.yml",
    ".prettierrc.js", ".prettierrc.cjs", "prettier.config.js", "prettier.config.cjs",
)


def has_prettier_config() -> bool:
    # ponytail: check cwd only. Add upward walk if a monorepo needs it.
    if any(os.path.exists(c) for c in PRETTIER_CONFIGS):
        return True
    try:
        with open("package.json") as f:
            return "prettier" in json.load(f)
    except Exception:
        return False


def formatter_for(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".go" and shutil.which("gofmt"):
        return ["gofmt", "-w", path]
    if ext == ".py":
        if shutil.which("ruff"):
            return ["ruff", "format", path]
        if shutil.which("black"):
            return ["black", "-q", path]
    if ext == ".rs" and shutil.which("rustfmt"):
        return ["rustfmt", path]
    if ext in PRETTIER_EXT and has_prettier_config() and shutil.which("npx"):
        return ["npx", "--no-install", "prettier", "--write", path]
    return None


def main() -> int:
    try:
        path = json.load(sys.stdin).get("tool_input", {}).get("file_path", "")
    except Exception:
        return 0
    if not path or not os.path.isfile(path):
        return 0
    cmd = formatter_for(path)
    if cmd:
        try:
            subprocess.run(cmd, capture_output=True, timeout=30)
        except Exception:
            pass  # formatting is best-effort; never block the edit
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        assert os.path.splitext("a.go")[1] == ".go"
        assert ".ts" in PRETTIER_EXT
        assert ".py" not in PRETTIER_EXT  # python has its own path
        print("ok")
        sys.exit(0)
    sys.exit(main())
