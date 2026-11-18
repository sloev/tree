#!/usr/bin/env python3
"""Create concise, content-specific Danish Nyhedsbulletin stories."""
from __future__ import annotations
import argparse, json, re, subprocess
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/"content"
ACTIVITY=CONTENT/"activity.md"

def parse_record(text):
    match=re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z",text,re.S)
    if not match:
        return {}, ""
    return (yaml.safe_load(match.group(1)) or {}), match.group(2).strip()

def read_meta(path):
    file=ROOT/path
    if not file.is_file():
        return {}
    return parse_record(file.read_text(encoding="utf-8"))[0]

def git_text(ref,path):
    if not ref or set(ref)=={"0"}:
        return ""
    result=subprocess.run(["git","show",f"{ref}:{path}"],cwd=ROOT,text=True,capture_output=True)
    return result.stdout if result.returncode==0 else ""

def changed_paths(before,after):
    if not before or set(before)=={"0"}:
        return []
    return subprocess.check_output(["git","diff","--name-only","--diff-filter=AMRT",before,after],cwd=ROOT,text=True).splitlines()

def add_entry(target,path,kind):
    meta=read_meta(path)
    ident=str(meta.get("id") or Path(path).stem)
    label=str(meta.get("name") or meta.get("title") or meta.get("label") or Path(path).stem.replace("-"," ").replace("_"," "))
    target[kind][ident]={"id":ident,"label":label,"path":path}

def enrichment_changes(path,before,kind,entries):
    field="people" if kind=="people" else "claims"
    newmeta,_=parse_record((ROOT/path).read_text(encoding="utf-8"))
    newmap=newmeta.get(field) or {}
    oldmeta,_=parse_record(git_text(before,path))
    oldmap=oldmeta.get(field) or {}
    changed=[str(k) for k in set(newmap)|set(oldmap) if newmap.get(k)!=oldmap.get(k)]
    folder="people" if kind=="people" else "claims"
    for ident in changed:
        record=f"content/{folder}/{ident}.md"
        if (ROOT/record).is_file():
            add_entry(entries,record,kind)

def prior_counts(before):
    counts={}
    for folder in ("people","claims","sources","places","media"):
        if not before or set(before)=={"0"}:
            counts[folder]=0
            continue
        output=subprocess.check_output(["git","ls-tree","-r","--name-only",before,"--",f"content/{folder}"],cwd=ROOT,text=True)
        counts[folder]=sum(1 for p in output.splitlines() if p.endswith(".md"))
    return counts

def prior_date(before):
    if not before or set(before)=={"0"}:
        return datetime.now(timezone.utc).date().isoformat()
    value=subprocess.check_output(["git","show","-s","--format=%cs",before],cwd=ROOT,text=True).strip()
    return value or datetime.now(timezone.utc).date().isoformat()

def short_list(items,limit=3):
    labels=[x["label"] for x in items]
    if not labels:
        return ""
    shown=", ".join(labels[:limit])
    if len(labels)>limit:
        shown+=f" (+{len(labels)-limit})"
    return shown

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

    entries={"people":{},"claims":{},"sources":{},"places":{},"media":{}}
    for path in research:
        if path=="content/person-enrichment.md":
            enrichment_changes(path,args.before,"people",entries)
        elif path=="content/research-enrichment.md":
            enrichment_changes(path,args.before,"claims",entries)
        elif path.startswith("content/people/") and path.endswith(".md"):
            add_entry(entries,path,"people")
        elif path.startswith("content/claims/") and path.endswith(".md"):
            add_entry(entries,path,"claims")
        elif path.startswith("content/sources/") and path.endswith(".md"):
            add_entry(entries,path,"sources")
        elif path.startswith("content/places/") and path.endswith(".md"):
            add_entry(entries,path,"places")
        elif path.startswith("content/media/") and path.endswith(".md"):
            add_entry(entries,path,"media")

    # If binary media changed, resolve its descriptive metadata where available.
    for path in media:
        for record in sorted((CONTENT/"media").glob("*.md")):
            meta,_=parse_record(record.read_text(encoding="utf-8"))
            if meta.get("file")==path:
                add_entry(entries,str(record.relative_to(ROOT)),"media")

    raw=ACTIVITY.read_text(encoding="utf-8")
    match=re.search(r"(?m)^bulletins:\s*(\[.*\])\s*$",raw)
    if not match:
        raise SystemExit("activity.md bulletins JSON array not found; refusing to overwrite")
    bulletins=json.loads(match.group(1))
    commit=args.after if args.after and set(args.after)!={"0"} else subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    if any(isinstance(x,dict) and x.get("commit")==commit for x in bulletins):
        print("Bulletin already exists for this commit.")
        return

    people=list(entries["people"].values())
    claims=list(entries["claims"].values())
    sources=list(entries["sources"].values())
    places=list(entries["places"].values())
    media_items=list(entries["media"].values())
    categories=[]
    if people: categories.append("Personer: "+short_list(people))
    if claims: categories.append("Forskningsspor: "+short_list(claims,2))
    if sources: categories.append("Kilder: "+short_list(sources,2))
    if places: categories.append("Steder: "+short_list(places,2))
    if media_items: categories.append("Billeder: "+short_list(media_items,2))

    if claims:
        title=claims[0]["label"]
    elif people:
        title="Personoplysninger: "+short_list(people,2)
    elif sources:
        title="Kildearbejde: "+short_list(sources,2)
    elif places:
        title="Steder i slægtshistorien: "+short_list(places,2)
    elif media_items:
        title="Historiske billeder: "+short_list(media_items,2)
    else:
        title="Redaktionel ændring i slægtshistorien"
    body=" · ".join(categories) if categories else "Der er tilføjet nyt historisk materiale."
    body+=". Kildegrundlag og åbne spørgsmål fremgår af de berørte poster."

    now=datetime.now(timezone.utc)
    item={
      "date":now.date().isoformat(),
      "date_label":now.strftime("%d.%m.%Y"),
      "created_at":now.isoformat(timespec="seconds").replace("+00:00","Z"),
      "title":title,"body":body,"paths":research+media,"commit":commit,
      "people":[x["id"] for x in people]
    }
    bulletins.insert(0,item)

    snapshot=prior_counts(args.before)
    snapshot["date"]=prior_date(args.before)
    stats_line="stats_snapshot: "+json.dumps(snapshot,ensure_ascii=False,separators=(",",":"))
    raw=re.sub(r"(?m)^stats_snapshot:.*\n","",raw)
    replacement=stats_line+"\nbulletins: "+json.dumps(bulletins,ensure_ascii=False,separators=(",",":"))
    raw,n=re.subn(r"(?m)^bulletins:\s*\[.*\]\s*$",lambda _m:replacement,raw,count=1)
    if n!=1:
        raise SystemExit("Could not update activity front matter safely")
    ACTIVITY.write_text(raw,encoding="utf-8")
    print(f"Added content-specific Nyhedsbulletin story for {commit}.")

if __name__=="__main__":
    main()
