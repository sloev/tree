#!/usr/bin/env python3
"""Check every local href/src in generated GitHub Pages HTML."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            value = attrs.get(key)
            if value:
                self.targets.append((tag, key, value))

def main():
    errors = []
    checked = 0
    pages = sorted(DOCS.rglob("*.html"))
    for page in pages:
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for tag, attr, raw in parser.targets:
            value = raw.strip()
            if not value or value.startswith("#"):
                continue
            parts = urlsplit(value)
            if parts.scheme or value.startswith("//"):
                continue
            target = (page.parent / unquote(parts.path)).resolve() if parts.path else page.resolve()
            if DOCS.resolve() not in target.parents and target != DOCS.resolve():
                errors.append((page.relative_to(ROOT), value, "path escapes docs"))
                continue
            if not target.exists():
                errors.append((page.relative_to(ROOT), value, "target does not exist"))
                continue
            checked += 1
            if parts.fragment and target.is_file() and target.suffix.lower() in {".html", ".htm"}:
                text = target.read_text(encoding="utf-8")
                fragment = unquote(parts.fragment)
                if f'id="{fragment}"' not in text and f"name=\"{fragment}\"" not in text:
                    errors.append((page.relative_to(ROOT), value, "fragment does not exist"))
    for page, target, reason in errors:
        print(f"ERROR {page}: {target} ({reason})")
    print(f"Checked {checked} local HTML links across {len(pages)} pages; {len(errors)} broken.")
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
