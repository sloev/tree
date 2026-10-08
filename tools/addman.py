"""Tilføjer et håndfundet led til data/manual_ancestors.json.
Brug fra Python: from addman import add; add(ahnen, navn, køn, born=..., bplace_text=..., src=[...], note=..., patch=False)"""
import json, os
PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "manual_ancestors.json")
def add(ahnen, name=None, sex=None, patch=False, **kw):
    L = json.load(open(PATH, encoding="utf-8")) if os.path.exists(PATH) else []
    L = [a for a in L if not (a["ahnen"] == ahnen and bool(a.get("patch")) == patch)]
    e = {"ahnen": ahnen, "id": f"a{ahnen}", "patch": patch}
    if name: e["name"] = name
    if sex: e["sex"] = sex
    elif not patch: e["sex"] = "M" if ahnen % 2 == 0 else "F"
    e.update({k: v for k, v in kw.items() if v is not None})
    L.append(e); L.sort(key=lambda a: a["ahnen"])
    json.dump(L, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return e

SIB = os.path.join(os.path.dirname(PATH), "manual_siblings.json")
def sib(of, father, mother, rows, rel, line, src):
    """rows: [(navn, køn, født, ekstra-dict)]; src: fælles kilde (fx folketælling)."""
    L = json.load(open(SIB, encoding="utf-8")) if os.path.exists(SIB) else []
    L = [s for s in L if s.get("_for") != of]
    for i, (name, sex, born, extra) in enumerate(rows):
        e = {"_for": of, "id": f"ms_{of}_{i}", "name": name, "sex": sex, "born": born, "father": father, "mother": mother,
             "rel": rel, "line": line, "src": list(extra.pop("src", [])) + list(src)}
        e.update(extra); L.append(e)
    json.dump(L, open(SIB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
