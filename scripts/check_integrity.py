#!/usr/bin/env python3
"""Cross-reference and provenance audit for the Markdown source of truth."""
from __future__ import annotations
import argparse, hashlib, re
from pathlib import Path
from urllib.parse import unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
SCHEMAS = {"people":"person/v1","claims":"claim/v1","sources":"source/v1","media":"media/v1","places":"place/v1","unions":"union/v1"}
FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.S)

def read_records(folder, schema):
    result=[]; errors=[]
    for path in sorted((CONTENT/folder).glob("*.md")):
        raw=path.read_text(encoding="utf-8")
        m=FRONT.match(raw)
        if not m:
            errors.append(f"{path.relative_to(ROOT)}: missing front matter"); continue
        try: meta=yaml.safe_load(m.group(1)) or {}
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}"); continue
        if not isinstance(meta,dict) or meta.get("schema") != schema or not meta.get("id"):
            errors.append(f"{path.relative_to(ROOT)}: expected {schema} and id"); continue
        result.append((meta,m.group(2),path))
    ids=[str(x[0]["id"]) for x in result]
    if len(ids)!=len(set(ids)): errors.append(f"content/{folder}: duplicate IDs")
    return result,errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--strict",action="store_true")
    args=ap.parse_args()
    records={}; errors=[]; warnings=[]
    for folder,schema in SCHEMAS.items():
        records[folder],bad=read_records(folder,schema); errors.extend(bad)
    people={str(m["id"]):m for m,_,_ in records["people"]}
    claims={str(m["id"]):m for m,_,_ in records["claims"]}
    sources={str(m["id"]):m for m,_,_ in records["sources"]}
    media={str(m["id"]):m for m,_,_ in records["media"]}
    places={str(m["id"]):m for m,_,_ in records["places"]}
    unions={str(m["id"]):m for m,_,_ in records["unions"]}
    place_names={str(m.get("name") or m["id"]) for m in places.values()}
    def refs(owner, key, valid, label):
        value=owner.get(key) or []
        if not isinstance(value,list): value=[value]
        for item in value:
            if str(item) not in valid: warnings.append(f"{label}: unresolved {key}={item}")
    for pid,p in people.items():
        for key in ("father","mother","spouse"):
            ref=p.get(key)
            if ref and str(ref) not in people: errors.append(f"person {pid}: {key} references missing person {ref}")
        born=re.search(r"(?<!\d)(1[0-9]{3}|20[0-9]{2})",str(p.get("born") or ""))
        died=re.search(r"(?<!\d)(1[0-9]{3}|20[0-9]{2})",str(p.get("died") or ""))
        if born and died and int(died.group(1)) < int(born.group(1)):
            errors.append(f"person {pid}: death year precedes birth year ({born.group(1)} > {died.group(1)})")
        for key in ("bplace","dplace"):
            place=p.get(key)
            if place and str(place) not in place_names:
                warnings.append(f"person {pid}: {key} has no exact place-register match: {place}")
    for cid,c in claims.items():
        refs(c,"person_ids",people,f"claim {cid}")
        refs(c,"sources",sources,f"claim {cid}")
        for key in ("place_ids","media_ids"):
            refs(c,key,places if key=="place_ids" else media,f"claim {cid}")
    for mid,m in media.items():
        refs(m,"person_ids",people,f"media {mid}")
        refs(m,"claim_ids",claims,f"media {mid}")
        refs(m,"source_ids",sources,f"media {mid}")
        refs(m,"place_ids",places,f"media {mid}")
        file_ref=m.get("file")
        if file_ref:
            target=(ROOT/str(file_ref)).resolve()
            if ROOT.resolve() not in target.parents or not target.is_file():
                errors.append(f"media {mid}: missing/unsafe file {file_ref}")
        else: warnings.append(f"media {mid}: no file path")
    for sid,s in sources.items():
        local=s.get("local_copy")
        if local:
            target=(ROOT/str(local)).resolve()
            if ROOT.resolve() not in target.parents or not target.is_file():
                errors.append(f"source {sid}: missing/unsafe local_copy {local}")
            elif s.get("sha256"):
                actual=hashlib.sha256(target.read_bytes()).hexdigest()
                if actual.lower()!=str(s["sha256"]).lower():
                    errors.append(f"source {sid}: SHA-256 mismatch for {local}")
        elif s.get("original_url"):
            warnings.append(f"source {sid}: original URL has no local copy; document access restriction")
    for uid,u in unions.items():
        refs(u,"partners",people,f"union {uid}")
    # Verify local Markdown links and count external links separately.
    link=re.compile(r"!?(?:\[[^\]]*\])\((?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
    local=external=0
    for path in sorted(CONTENT.rglob("*.md")):
        raw=path.read_text(encoding="utf-8")
        for match in link.finditer(raw):
            target=(match.group(1) or match.group(2) or "").strip()
            if not target or target.startswith("#"): continue
            parts=urlsplit(target)
            if parts.scheme or target.startswith("//"):
                if parts.scheme in {"http","https"}: external+=1
                continue
            dest=(path.parent/unquote(parts.path)).resolve()
            if ROOT.resolve() not in dest.parents or not dest.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken local link {target}")
            else: local+=1
    print(f"INTEGRITY records: people={len(people)} claims={len(claims)} sources={len(sources)} media={len(media)} places={len(places)} unions={len(unions)}")
    print(f"INTEGRITY links: local={local} external={external}")
    print(f"INTEGRITY issues: errors={len(errors)} warnings={len(warnings)}")
    for item in errors[:150]: print("ERROR",item)
    for item in warnings[:150]: print("WARN",item)
    if len(errors)>150 or len(warnings)>150: print("Further issues omitted from log.")
    if args.strict and errors: raise SystemExit(1)

if __name__=="__main__": main()
