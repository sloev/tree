#!/usr/bin/env python3
"""Validate local Markdown links and media file references.

External URLs are reported as provenance/link-policy debt; they are not fetched.
Use --strict-external only after all source URLs have local copies or are explicitly
moved into non-clickable original_url metadata.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
LINK = re.compile(r"!?(?:\[[^\]]*\])\((?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.S)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict-external", action="store_true")
    args = ap.parse_args()
    broken = []
    external = []
    checked = 0
    for md in sorted(CONTENT.rglob("*.md")):
        raw = md.read_text(encoding="utf-8")
        for match in LINK.finditer(raw):
            target = (match.group(1) or match.group(2) or "").strip()
            if not target or target.startswith("#"):
                continue
            parts = urlsplit(target)
            if parts.scheme or target.startswith("//"):
                if parts.scheme in {"http", "https"}:
                    external.append((md.relative_to(ROOT), target))
                continue
            path_text = unquote(parts.path)
            if not path_text:
                continue
            target_path = (md.parent / path_text).resolve()
            if ROOT.resolve() not in target_path.parents and target_path != ROOT.resolve():
                broken.append((md.relative_to(ROOT), target, "path escapes repository"))
            elif not target_path.exists():
                broken.append((md.relative_to(ROOT), target, "target does not exist"))
            else:
                checked += 1
        front = FRONT.match(raw)
        if front:
            # Media metadata's file field is a repository-root-relative local asset.
            try:
                import yaml
                meta = yaml.safe_load(front.group(1)) or {}
            except Exception:
                meta = {}
            file_ref = meta.get("file") if isinstance(meta, dict) else None
            if file_ref:
                target_path = (ROOT / str(file_ref)).resolve()
                if ROOT.resolve() not in target_path.parents or not target_path.is_file():
                    broken.append((md.relative_to(ROOT), str(file_ref), "media file missing or outside repository"))
                else:
                    checked += 1
    for path, target, why in broken:
        print(f"ERROR {path}: {target} ({why})")
    for path, target in external:
        print(f"EXTERNAL {path}: {target}")
    print(f"Checked {checked} local targets; {len(broken)} broken; {len(external)} external hyperlinks remain.")
    if broken or (args.strict_external and external):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
