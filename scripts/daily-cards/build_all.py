#!/usr/bin/env python3
"""Build only the approved prototype gate (Day 02, 04, 05)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable


def run(*args: str) -> None:
    subprocess.run([PYTHON, *args], cwd=ROOT, check=True)


def main() -> None:
    run("scripts/daily-cards/validate.py")
    run("scripts/daily-cards/cache_routes.py", "4", "5")
    run("scripts/daily-cards/cache_tiles.py", "2", "4", "5")
    run("scripts/daily-cards/render.py", "2", "4", "5")
    run("scripts/daily-cards/validate.py", "--write-report")


if __name__ == "__main__":
    main()

