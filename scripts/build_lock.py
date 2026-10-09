#!/usr/bin/env python3
"""Serialize site build/clean commands on macOS and Linux."""
import fcntl
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: build_lock.py COMMAND [ARG ...]")
    # Keep this outside .cache: sri-clean removes that directory.
    # Never unlink the file: all callers must lock the same inode.
    with (ROOT / ".site-build.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        result = subprocess.run(sys.argv[1:], cwd=ROOT, pass_fds=(lock.fileno(),))
        raise SystemExit(result.returncode)
