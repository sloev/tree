#!/usr/bin/env python3
"""Create one concise Danish Nyhedsbulletin story per public research/media commit."""
from __future__ import annotations
import argparse, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
ACTIVITY=ROOT/"content"/"activity.md"

def changed_paths(before: str, after: str) -> list[str]:
    if not before or set(before)=={"0"}:
        return []
    return subprocess.check_output(
        ["git","diff","--name-only","--diff-filter=AMRT",before,after],
        cwd=ROOT,text=True
    ).splitlines()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--before",default="")
    ap.add_argument("--after",default="HEAD")
    args=ap.parse_args()
    paths=changed_paths(args.before,args.after)
    paths=[p for p in paths if p!="content/activity.md"]
    research=[p for p in paths if p.startswith("content/")]
    media=[p for p in paths if p.startswith(("images/","media/files/"))]
    if not research and not media:
        print("No substantive public research/media changes; bulletin unchanged.")
        return
    raw=ACTIVITY.read_text(encoding="utf-8")
    match=re.search(r"(?m)^bulletins:\s*(\[.*\])\s*$",raw)
    if not match:
        raise SystemExit("activity.md bulletins JSON array not found; refusing to overwrite")
    bulletins=json.loads(match.group(1))
    commit=args.after if args.after and set(args.after)!={"0"} else subprocess.check_output(
        ["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    if any(isinstance(x,dict) and x.get("commit")==commit for x in bulletins):
        print("Bulletin already exists for this commit.")
        return
    counts={
      "personer":sum(p.startswith("content/people/") for p in research),
      "forskningsspor":sum(p.startswith("content/claims/") for p in research),
      "kilder":sum(p.startswith("content/sources/") for p in research),
      "steder":sum(p.startswith("content/places/") for p in research),
      "øvrige redaktionelle poster":sum(not p.startswith(("content/people/","content/claims/","content/sources/","content/places/")) for p in research),
      "mediefiler":len(media)
    }
    parts=[f"{n} {label}" for label,n in counts.items() if n]
    names=[]
    for p in research:
        stem=Path(p).stem.replace("-"," ").replace("_"," ")
        if stem and stem not in names and len(names)<4:
            names.append(stem)
    title="Forskningsarbejde opdateret"
    if counts["forskningsspor"] and counts["kilder"]:
        title="Nye forskningsspor og kilder"
    elif counts["personer"]:
        title="Personoplysninger opdateret"
    elif counts["kilder"]:
        title="Nye kilder registreret"
    elif media:
        title="Historisk billedmateriale tilføjet"
    body="Der er offentliggjort "+", ".join(parts)+"."
    if names:
        body+=" Berørte poster: "+", ".join(names)+"."
    body+=" Se kilder og forskningsspor for dokumentation og åbne spørgsmål. En opdatering er ikke i sig selv et bekræftet genealogisk fund."
    now=datetime.now(timezone.utc)
    item={
      "date":now.date().isoformat(),
      "date_label":now.strftime("%d.%m.%Y"),
      "created_at":now.isoformat(timespec="seconds").replace("+00:00","Z"),
      "title":title,"body":body,"paths":research + media,"commit":commit,"people":[]
    }
    bulletins.insert(0,item)
    replacement="bulletins: "+json.dumps(bulletins,ensure_ascii=False,separators=(",",":"))
    ACTIVITY.write_text(raw[:match.start()]+replacement+raw[match.end():],encoding="utf-8")
    print(f"Added Nyhedsbulletin story for {commit}.")
if __name__=="__main__": main()
