#!/usr/bin/env python3
"""Run the portable skill package validator from the repository root."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "aident-brand-visual-production" / "scripts" / "validate_package.py"


def main() -> int:
    if not SCRIPT.is_file():
        print(f"missing skill validator: {SCRIPT}", file=sys.stderr)
        return 1
    return subprocess.call([sys.executable, str(SCRIPT)])


if __name__ == "__main__":
    sys.exit(main())
