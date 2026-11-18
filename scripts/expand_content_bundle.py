#!/usr/bin/env python3
"""Expand content_bundle.b64.part* into content/**/*.md

Usage:
  python3 scripts/expand_content_bundle.py
"""
from __future__ import annotations

import base64
import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    parts = sorted(ROOT.glob("content_bundle.b64.part*"))
    single = ROOT / "content_bundle.b64"
    if parts:
        b64 = "".join(p.read_text(encoding="ascii") for p in parts)
    elif single.exists():
        b64 = single.read_text(encoding="ascii")
    else:
        print("No content_bundle.b64 or parts found", file=sys.stderr)
        sys.exit(1)
    data = json.loads(gzip.decompress(base64.b64decode(b64)))
    n = 0
    for rel, text in data.items():
        path = ROOT / "content" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        n += 1
    print(f"Expanded {n} markdown files under content/")

if __name__ == "__main__":
    main()
