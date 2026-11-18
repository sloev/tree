#!/usr/bin/env python3
"""Build the single interactive site and compatibility permalinks from Markdown."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from interactive_site import build as build_interactive_front_page


def main():
    ged = ROOT / "family-tree.ged"
    if not ged.is_file():
        raise SystemExit("family-tree.ged missing; run scripts/compile_content.py first")
    shutil.copy2(ged, ROOT / "docs" / "family-tree.ged")
    build_interactive_front_page()
    print("Published the unified interactive site and canonical record routes")


if __name__ == "__main__":
    main()
