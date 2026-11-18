#!/usr/bin/env python3
"""Compile Markdown source records into GEDCOM and static HTML; never emits JSON."""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/"content"
def read_records(folder,schema):
    import yaml
    records=[]
    d=CONTENT/folder
    if not d.exists(): return records
    for path in sorted(d.glob("*.md")):
        raw=path.read_text(encoding="utf-8")
        match=re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z",raw,re.S)
        if not match: raise ValueError(f"{path}: missing YAML front matter")
        meta=yaml.safe_load(match.group(1)) or {}
        if not isinstance(meta,dict) or not meta.get("id") or not meta.get("schema"):
            raise ValueError(f"{path}: id and schema are required")
        if meta["schema"]==schema: records.append((meta,match.group(2).strip(),path))
    ids=[x[0]["id"] for x in records]
    if len(ids)!=len(set(ids)): raise ValueError(f"Duplicate IDs in content/{folder}")
    return records
def private(meta):
    born=str(meta.get("born") or "")
    if meta.get("public_consent") is True and not meta.get("private"): return False
    return meta.get("private") is True or meta.get("living") is True or bool(re.match(r"^(19(2[6-9]|[3-9]\d)|20\d\d)",born) and not meta.get("died"))
def ged_date(value):
    s=str(value or "")
    m=re.match(r"^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?$",s)
    if not m:
        approx=re.match(r"^(?:c[.]|ca[.]) *([0-9]{4})$",s,re.I)
        after=re.match(r"^(?:after|efter) *([0-9]{4})$",s,re.I)
        span=re.match(r"^([0-9]{4})[–-]([0-9]{4})$",s)
        if approx:return "ABT "+approx.group(1)
        if after:return "AFT "+after.group(1)
        if span:return "BET "+span.group(1)+" AND "+span.group(2)
        return s.upper()
    months=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    if not m.group(2):return m.group(1)
    if not m.group(3):return months[int(m.group(2))-1]+" "+m.group(1)
    return f"{int(m.group(3))} {months[int(m.group(2))-1]} {m.group(1)}"
def gedcom(people, unions=None):
    rows=[x[0] for x in people]; refs={str(p["id"]):f"@I{i}@" for i,p in enumerate(rows,1)}
    fams=[]; pair_index={}
    def family(pair):
        key=tuple(sorted(pair))
        if key not in pair_index:
            pair_index[key]=len(fams)+1; fams.append({"pair":pair,"children":[],"union":None})
        return fams[pair_index[key]-1]
    for p in rows:
        father=str(p.get("father") or ""); mother=str(p.get("mother") or "")
        if father or mother:
            family((father,mother))["children"].append(str(p["id"]))
        spouse=str(p.get("spouse") or "")
        if spouse and spouse in refs and not private(p) and not private(next((x[0] for x in people if str(x[0]["id"])==spouse),{})):
            other=next((x[0] for x in people if str(x[0]["id"])==spouse),{})
            if p.get("sex")=="M": pair=(str(p["id"]),spouse)
            elif p.get("sex")=="F": pair=(spouse,str(p["id"]))
            elif other.get("sex")=="F": pair=(spouse,str(p["id"]))
            else: pair=(str(p["id"]),spouse)
            family(pair)
    by_id={str(p["id"]):p for p in rows}
    for union in unions or []:
        partners=[str(x) for x in union.get("partners",[]) or []]
        if len(partners)!=2 or any(x not in by_id for x in partners): continue
        if union.get("public") is not True or any(private(by_id[x]) for x in partners): continue
        first,second=(by_id[partners[0]],by_id[partners[1]])
        if first.get("sex")=="M": pair=(partners[0],partners[1])
        elif second.get("sex")=="M": pair=(partners[1],partners[0])
        elif first.get("sex")=="F": pair=(partners[1],partners[0])
        else: pair=(partners[0],partners[1])
        family(pair)["union"]=union
    partner_fams={}; child_fams={}
    for i,f in enumerate(fams,1):
        for partner in f["pair"]:
            if partner: partner_fams.setdefault(partner,[]).append(i)
        for child in f["children"]: child_fams.setdefault(child,[]).append(i)
    lines=["0 HEAD","1 SOUR sloev/tree Markdown compiler","1 GEDC","2 VERS 5.5.1","1 CHAR UTF-8"]
    for p in rows:
        pid=str(p["id"]); lines += [f"0 {refs[pid]} INDI"]
        name="Privat person" if private(p) else str(p.get("name") or pid)
        parts=name.replace("/"," ").split()
        if len(parts)>1: lines.append("1 NAME "+" ".join(parts[:-1])+" /"+parts[-1]+"/")
        else: lines.append("1 NAME "+name)
        if not private(p) and p.get("sex") in ("M","F"): lines.append("1 SEX "+p["sex"])
        if not private(p) and p.get("born"):
            lines += ["1 BIRT","2 DATE "+ged_date(p["born"])]
            if p.get("bplace") and not private(p): lines.append("2 PLAC "+str(p["bplace"]))
        if not private(p) and p.get("died"):
            lines += ["1 DEAT","2 DATE "+ged_date(p["died"])]
            if p.get("dplace") and not private(p): lines.append("2 PLAC "+str(p["dplace"]))
        if not private(p):
            for occ in p.get("occ",[]) or []: lines.append("1 OCCU "+str(occ).replace("\n"," "))
            for line in (p.get("note") or "").splitlines():
                if line.strip(): lines.append("1 NOTE "+line.strip().replace("\n"," "))
        for family_id in partner_fams.get(pid,[]): lines.append(f"1 FAMS @F{family_id}@")
        for family_id in child_fams.get(pid,[]): lines.append(f"1 FAMC @F{family_id}@")
    for f in fams:
        n=pair_index[tuple(sorted(f["pair"]))]; father,mother=f["pair"]; lines.append(f"0 @F{n}@ FAM")
        if father in refs: lines.append("1 HUSB "+refs[father])
        if mother in refs: lines.append("1 WIFE "+refs[mother])
        union=f.get("union") or {}
        if union.get("status")=="divorced": lines.append("1 DIV")
        if union.get("note"): lines.append("1 NOTE "+str(union["note"]).replace("\n"," "))
        for child in f["children"]:
            if child in refs: lines.append("1 CHIL "+refs[child])
    lines.append("0 TRLR")
    return "\n".join(lines)+"\n"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    ap.add_argument("--site",action="store_true")
    args=ap.parse_args()
    people=read_records("people","person/v1")
    claims=read_records("claims","claim/v1")
    for folder,schema in [("sources","source/v1"),("media","media/v1"),("places","place/v1")]:
        read_records(folder,schema)
    unions=read_records("unions","union/v1")
    if len(people)<100: raise SystemExit(f"Only {len(people)} people found; refusing build")
    ids={str(p[0]["id"]) for p in people}
    duplicate=len(ids)!=len(people)
    if duplicate: raise SystemExit("Duplicate person IDs")
    missing=[]
    for meta,_,path in people:
        for key in ("father","mother","spouse"):
            ref=meta.get(key)
            if ref and str(ref) not in ids: missing.append(f"{path}: {key} references missing {ref}")
    for msg in missing[:30]: print("WARN:",msg,file=sys.stderr)
    print(f"Validated Markdown: {len(people)} people, {len(claims)} research claims")
    if args.check:return
    text=gedcom(people,[m for m,_,_ in unions])
    (ROOT/"family-tree.ged").write_text(text,encoding="utf-8")
    build=ROOT/"build"; build.mkdir(exist_ok=True)
    (build/"family-tree.ged").write_text(text,encoding="utf-8")
    if args.site: subprocess.check_call([sys.executable,str(ROOT/"site"/"build.py")],cwd=ROOT)
    print("Wrote family-tree.ged")
if __name__=="__main__": main()
