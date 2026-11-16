#!/usr/bin/env python3
"""Track person records changed in data/build_data.py for a short visual highlight."""
import datetime as dt
import difflib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = "data/build_data.py"
OUTPUT = os.path.join(ROOT, "data", "recently-edited.json")
PERSON_START = re.compile(r'^person\("([^"]+)"')

def git_text(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)

def blocks(text):
    lines = text.splitlines(keepends=True)
    found = {}
    i = 0
    while i < len(lines):
        match = PERSON_START.match(lines[i])
        if not match:
            i += 1
            continue
        start = i
        i += 1
        # Each person() record ends at the next top-level person() call or comment.
        while i < len(lines) and not PERSON_START.match(lines[i]):
            i += 1
        found[match.group(1)] = "".join(lines[start:i]).strip()
    return found

def main():
    base, head = sys.argv[1:3]
    old = git_text("show", f"{base}:{SOURCE}") if base and base != "0" * 40 else ""
    new = git_text("show", f"{head}:{SOURCE}")
    before, after = blocks(old), blocks(new)
    changed = {pid for pid in set(before) | set(after) if before.get(pid) != after.get(pid)}

    try:
        recent = json.load(open(OUTPUT, encoding="utf-8"))
    except (OSError, ValueError):
        recent = {}
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=30)
    cleaned = {}
    for pid, stamp in recent.items():
        try:
            when = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            if when >= cutoff:
                cleaned[pid] = stamp
        except (TypeError, ValueError):
            continue
    stamp = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    for pid in changed:
        cleaned[pid] = stamp
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"Marked {len(changed)} changed person record(s); {len(cleaned)} active highlight(s).")

if __name__ == "__main__":
    main()
