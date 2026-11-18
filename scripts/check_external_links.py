#!/usr/bin/env python3
"""Reachability audit for external Markdown links; report only, never rewrite source."""
from __future__ import annotations

import concurrent.futures
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
LINK = re.compile(r'!?(?:\[[^\]]*\])\((?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)')
UA = "Mozilla/5.0 (compatible; sloev-tree-link-audit/1.0)"


def check(url: str):
    # HEAD is cheap, but many archival services reject it. Retry with a one-byte GET.
    request_url = quote(url, safe=":/?&=%#[]@!$'()*+,;~-._")
    headers = {"User-Agent": UA, "Accept": "*/*"}
    try:
        req = urllib.request.Request(request_url, method="HEAD", headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return url, response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        if exc.code not in (403, 405, 501, 429):
            return url, exc.code, exc.reason
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            request_url, headers={**headers, "Range": "bytes=0-0"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return url, response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        return url, exc.code, exc.reason
    except Exception as exc:
        return url, "UNVERIFIED", str(exc)[:180]


def main():
    found = {}
    for path in sorted(CONTENT.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        for match in LINK.finditer(raw):
            target = (match.group(1) or match.group(2) or "").strip()
            if target.startswith(("https://", "http://")):
                found.setdefault(target, []).append(str(path.relative_to(ROOT)))

    print(
        "External Markdown links:",
        sum(map(len, found.values())),
        "occurrences;",
        len(found),
        "unique URLs",
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(check, sorted(found)))

    counts = {}
    for url, status, final in results:
        key = str(status)
        counts[key] = counts.get(key, 0) + 1
        if not isinstance(status, int) or not 200 <= status < 400:
            print(
                "EXTERNAL_STATUS",
                status,
                url,
                "=>",
                final,
                "files=",
                ",".join(sorted(set(found[url]))),
            )

    print("External URL status counts:", counts)
    print(
        "HTTP 2xx/3xx are reachable. 401/403/429 and UNVERIFIED may indicate "
        "login, bot protection or rate limiting, not a dead source."
    )


if __name__ == "__main__":
    main()
