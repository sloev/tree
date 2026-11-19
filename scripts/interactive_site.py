#!/usr/bin/env python3
"""Self-healing loader: fetch known-good interactive_site from git history, then exec.

Workaround for tool upload size limits. Points at TEMPLATE=site/template.html
(the Leaflet maps template). After first successful run you can replace this
file with the restored body if desired.
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

GOOD_URL = (
    "https://raw.githubusercontent.com/sloev/tree/"
    "70471102aab6b06c988b893ec7337f8638846b30/scripts/interactive_site.py"
)

_here = Path(__file__).resolve()
_cache = _here.with_name("_interactive_site_restored.py")


def _load() -> str:
    if _cache.is_file() and _cache.stat().st_size > 10000:
        return _cache.read_text(encoding="utf-8")
    with urllib.request.urlopen(GOOD_URL, timeout=60) as resp:
        text = resp.read().decode("utf-8")
    if "def build(" not in text or "TEMPLATE" not in text:
        raise SystemExit("Restored interactive_site.py looks invalid")
    # Ensure Leaflet template path (file was renamed to template.html)
    text = text.replace(
        'TEMPLATE = ROOT / "site" / "template-leaflet-maps.html"',
        'TEMPLATE = ROOT / "site" / "template.html"',
    )
    if 'TEMPLATE = ROOT / "site" / "template.html"' not in text:
        raise SystemExit("Restored interactive_site.py missing TEMPLATE path")
    _cache.write_text(text, encoding="utf-8")
    return text


_code = _load()
exec(compile(_code, str(_cache if _cache.is_file() else _here), "exec"), globals())
