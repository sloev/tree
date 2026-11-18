#!/usr/bin/env python3
"""Build the static records and the original interactive front page from Markdown."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from static_site import build as build_static_pages
from interactive_site import build as build_interactive_front_page


def main():
    # The static person/research/source pages remain available as secondary pages.
    build_static_pages()
    ged = ROOT / "family-tree.ged"
    if not ged.is_file():
        raise SystemExit("family-tree.ged missing; run scripts/compile_content.py first")
    shutil.copy2(ged, ROOT / "docs" / "family-tree.ged")
    build_interactive_front_page()
    print("Published the original interactive front page and Markdown-generated data")


if __name__ == "__main__":
    main()
