"""Vedligeholder manuelt indsamlede forslag i tree.json["ingestion"].

Brug: from addman import add, sib
Forslagene gemmes som intake-materiale og bliver ikke automatisk publiceret.
"""
import json
from pathlib import Path

TREE = Path(__file__).resolve().parents[1] / "data" / "tree.json"

def load():
    return json.loads(TREE.read_text(encoding="utf-8"))

def save(tree):
    TREE.write_text(json.dumps(tree, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

def add(ahnen, name=None, sex=None, patch=False, **kw):
    tree = load()
    bucket = tree.setdefault("ingestion", {}).setdefault("manual_ancestors", [])
    bucket[:] = [a for a in bucket if not (a["ahnen"] == ahnen and bool(a.get("patch")) == patch)]
    entry = {"ahnen": ahnen, "id": f"a{ahnen}", "patch": patch}
    if name: entry["name"] = name
    if sex: entry["sex"] = sex
    elif not patch: entry["sex"] = "M" if ahnen % 2 == 0 else "F"
    entry.update({k: v for k, v in kw.items() if v is not None})
    bucket.append(entry)
    bucket.sort(key=lambda a: a["ahnen"])
    save(tree)
    return entry

def sib(of, father, mother, rows, rel, line, src):
    """rows: [(navn, køn, født, ekstra-dict)]; src: fælles kilde."""
    tree = load()
    bucket = tree.setdefault("ingestion", {}).setdefault("manual_siblings", [])
    bucket[:] = [s for s in bucket if s.get("_for") != of]
    for i, (name, sex, born, extra) in enumerate(rows):
        extra = dict(extra)
        entry = {"_for": of, "id": f"ms_{of}_{i}", "name": name, "sex": sex, "born": born,
                 "father": father, "mother": mother, "rel": rel, "line": line,
                 "src": list(extra.pop("src", [])) + list(src)}
        entry.update(extra)
        bucket.append(entry)
    save(tree)
