#!/usr/bin/env python3
"""Generate recent-person markers and the newest automatic bulletin entry."""
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = "data/build_data.py"
OUTPUT = os.path.join(ROOT, "data", "recently-edited.json")
PERSON_START = re.compile(r'^person\("([^"]+)",\s*"([^"]+)"')

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()

def person_records(text):
    lines = text.splitlines()
    result, i = {}, 0
    while i < len(lines):
        match = PERSON_START.match(lines[i])
        if not match:
            i += 1
            continue
        start, pid, name = i, match.group(1), match.group(2)
        i += 1
        while i < len(lines) and not PERSON_START.match(lines[i]):
            i += 1
        result[pid] = (name, "\n".join(lines[start:i]).strip())
    return result

def main():
    base, head = sys.argv[1:3]
    try:
        old = git("show", f"{base}:{SOURCE}") if base and base != "0" * 40 else ""
    except subprocess.CalledProcessError:
        old = ""
    new = git("show", f"{head}:{SOURCE}")
    before, after = person_records(old), person_records(new)
    changed_ids = sorted(pid for pid in set(before) | set(after)
                         if before.get(pid) != after.get(pid))
    changed_paths = git("diff", "--name-only", base, head).splitlines() if base and base != "0" * 40 else [SOURCE]
    try:
        state = json.load(open(OUTPUT, encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    # Migrate the earlier simple {person_id: timestamp} representation.
    people = state.get("people", {}) if isinstance(state, dict) else {}
    if state and not any(k in state for k in ("people", "latest_bulletin")):
        people = state
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=30)
    people = {pid: stamp for pid, stamp in people.items()
              if isinstance(stamp, str) and stamp >= cutoff.isoformat()[:10]}
    stamp = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    for pid in changed_ids:
        people[pid] = stamp

    # Keep the last bulletin unless this commit changed a research/data input.
    bulletin = state.get("latest_bulletin") if isinstance(state, dict) else None
    relevant = [p for p in changed_paths if p.startswith(("data/build_data.py", "leads/", "research-archive/"))
                or p in ("coop.log.md", "README.md")]
    if relevant:
        names = [after.get(pid, before.get(pid, (pid, "")))[0] for pid in changed_ids]
        subject = git("log", "-1", "--format=%s", head)
        if names:
            title = "Stamtræ opdateret: " + ", ".join(names[:5]) + (f" (+{len(names)-5})" if len(names) > 5 else "")
            body = "Personoplysninger er ændret i kildedataene. Åbn personkortene for at se de aktuelle datoer, noter og kilder."
        else:
            title = subject or "Nyt forskningsnotat"
            body = "Forskningsmateriale eller kildegrundlag er opdateret. Se ændringsloggen og de relevante forskningsnoter for detaljer."
        bulletin = {"date": now.date().isoformat(), "date_label": now.strftime("%-d. %B %Y"),
                    "title": title, "body": body, "people": changed_ids,
                    "commit": head, "paths": relevant}
    json.dump({"people": people, "latest_bulletin": bulletin}, open(OUTPUT, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, sort_keys=True)
    with open(OUTPUT, "a", encoding="utf-8") as f:
        f.write("\n")
    print(f"Updated {len(changed_ids)} person marker(s); bulletin {'refreshed' if relevant else 'retained'}.")

if __name__ == "__main__":
    main()
