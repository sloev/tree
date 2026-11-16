#!/usr/bin/env python3
"""Generate recent-person markers and the newest bulletin from canonical tree.json changes."""
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = "data/tree.json"
OUTPUT = os.path.join(ROOT, "data", "recently-edited.json")

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()

def load_revision(rev):
    return json.loads(git("show", f"{rev}:{SOURCE}")) if rev else {"family": {"people": []}, "research": {"claims": []}}

def people(tree):
    return {p["id"]: p for p in tree.get("family", {}).get("people", [])}

def main():
    base, head = sys.argv[1:3]
    try:
        old_tree = load_revision(base) if base and base != "0" * 40 else {}
    except subprocess.CalledProcessError:
        old_tree = {}
    new_tree = load_revision(head)
    before, after = people(old_tree), people(new_tree)
    changed_ids = {pid for pid in set(before) | set(after) if before.get(pid) != after.get(pid)}
    changed_paths = git("diff", "--name-only", base, head).splitlines() if base and base != "0" * 40 else [SOURCE]
    relevant = [p for p in changed_paths if p == SOURCE or p == "coop.log.md"]
    try:
        state = json.load(open(OUTPUT, encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    markers = state.get("people", {}) if isinstance(state, dict) else {}
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=30)
    markers = {pid: stamp for pid, stamp in markers.items()
               if isinstance(stamp, str) and stamp >= cutoff.isoformat()[:10]}
    stamp = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    for pid in changed_ids:
        markers[pid] = stamp

    # Append-only history: migrate the former single bulletin once, then only append.
    bulletins = list(state.get("bulletins", [])) if isinstance(state, dict) else []
    legacy = state.get("latest_bulletin") if isinstance(state, dict) else None
    if isinstance(legacy, dict) and not any(
        isinstance(item, dict) and item.get("commit") == legacy.get("commit")
        for item in bulletins
    ):
        bulletins.append(legacy)

    appended = False
    if relevant:
        names = [after.get(pid, before.get(pid, {})).get("name", pid) for pid in sorted(changed_ids)]
        subject = git("log", "-1", "--format=%s", head)
        if names:
            title = "Stamtræ opdateret: " + ", ".join(names[:5]) + (f" (+{len(names)-5})" if len(names) > 5 else "")
            body = "Personoplysninger er ændret i den kanoniske datafil. Åbn personkortene for aktuelle datoer, noter og kilder."
        else:
            title = subject or "Forskningsregister opdateret"
            body = "Det offentlige forskningsregister eller andre kanoniske data er opdateret. Se forskningssiden for de aktuelle spor."
        bulletin = {"date": now.date().isoformat(), "date_label": now.strftime("%d.%m.%Y"),
                    "title": title, "body": body, "people": sorted(changed_ids),
                    "commit": head, "paths": relevant}
        if not any(isinstance(item, dict) and item.get("commit") == head for item in bulletins):
            bulletins.append(bulletin)
            appended = True
    latest = bulletins[-1] if bulletins else None
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({"people": markers, "bulletins": bulletins, "latest_bulletin": latest},
                  f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"Updated {len(changed_ids)} person marker(s); bulletin {'appended' if appended else 'retained'}.")

if __name__ == "__main__":
    main()
