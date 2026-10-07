"""Exports data/family.json to family-tree.ged (GEDCOM 5.5.1)."""
import json, os, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(root, "data", "family.json"), encoding="utf-8"))
P = D["people"]
MON = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()

def gdate(s):
    if not s: return None
    s = str(s)
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m: return f"{int(m[3])} {MON[int(m[2])-1]} {m[1]}"
    m = re.fullmatch(r"(\d{4})-(\d{2})", s)
    if m: return f"{MON[int(m[2])-1]} {m[1]}"
    if re.fullmatch(r"\d{4}", s): return s
    m = re.fullmatch(r"(?:c\.|ca\.) ?(\d{4})", s)
    if m: return f"ABT {m[1]}"
    m = re.fullmatch(r"(?:after|efter) (\d{4})", s)
    if m: return f"AFT {m[1]}"
    m = re.fullmatch(r"(\d{4})–(\d{4})", s)
    if m: return f"BET {m[1]} AND {m[2]}"
    return None

def gname(n):
    n = re.sub(r"\s*\(.*?\)", "", n).strip()
    parts = n.split(" ")
    return n if len(parts) == 1 else " ".join(parts[:-1]) + f" /{parts[-1]}/"

fams = {}
for p in P:
    if p["father"] or p["mother"]:
        fams.setdefault((p["father"], p["mother"]), []).append(p["id"])
for p in P:  # ægtepar uden fælles børn i data
    if p.get("spouse"):
        sp = next(q for q in P if q["id"] == p["spouse"])
        k = (p["id"], sp["id"]) if p["sex"] == "M" else (sp["id"], p["id"])
        fams.setdefault(k, [])
famid = {k: f"F{i+1}" for i, k in enumerate(fams)}
L = ["0 HEAD", "1 SOUR GaardstedJorgensenTree", "1 GEDC", "2 VERS 5.5.1", "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8"]
for p in P:
    L += [f"0 @{p['id']}@ INDI", f"1 NAME {gname(p['name'])}", f"1 SEX {p['sex'] if p['sex'] in 'MF' else 'U'}"]
    for tag, d, pl in (("BIRT", p["born"], p["bplace"]), ("DEAT", p["died"], p["dplace"])):
        if d or pl:
            L.append(f"1 {tag}")
            if gdate(d): L.append(f"2 DATE {gdate(d)}")
            if pl: L.append(f"2 PLAC {pl}, Danmark" if pl != "Malmö" else "2 PLAC Malmö, Sverige")
    for o in p["occ"]: L.append(f"1 OCCU {o}")
    for y, pl, what in p["res"]:
        L += ["1 RESI", f"2 DATE {y}", f"2 PLAC {pl}"] + ([f"2 NOTE {what}"] if what else [])
    if p["note"]: L.append(f"1 NOTE {p['note']}")
    if p["conf"] != "record": L.append(f"1 NOTE Sikkerhed: {dict(probable='sandsynlig', possible='mulig', told='oplyst af familien').get(p['conf'], p['conf'])}")
    for s in p["src"]: L += ["1 SOUR", f"2 PAGE {s}"]
    for k, kids in fams.items():
        if p["id"] in kids: L.append(f"1 FAMC @{famid[k]}@")
        if p["id"] in k: L.append(f"1 FAMS @{famid[k]}@")
for k, kids in fams.items():
    L.append(f"0 @{famid[k]}@ FAM")
    if k[0]: L.append(f"1 HUSB @{k[0]}@")
    if k[1]: L.append(f"1 WIFE @{k[1]}@")
    for c in kids: L.append(f"1 CHIL @{c}@")
L.append("0 TRLR")
open(os.path.join(root, "family-tree.ged"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(P), "personer,", len(fams), "familier")
