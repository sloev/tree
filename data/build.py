"""Build all derived genealogy data from the single canonical source, data/tree.json.

Edit tree.json only. family.json, research.json and map.json are compatibility projections
for existing scripts and are regenerated here; they are never authoritative.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "data", "tree.json")

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def write_json(path, value):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=1)
        f.write("\n")

def must_be_private(person, this_year=2026):
    if person.get("public_consent") is True or person.get("private"):
        return False
    year = re.search(r"\d{4}", str(person.get("born") or ""))
    return bool(person.get("living") or (
        not person.get("died") and year and int(year.group()) >= this_year - 100
    ))

def validate(tree):
    assert tree.get("schema_version") == 1, "Ukendt tree.json schema_version"
    family = tree["family"]
    research = tree["research"]
    assert isinstance(family.get("people"), list), "family.people skal være en liste"
    ids = [p["id"] for p in family["people"]]
    assert len(ids) == len(set(ids)), "Dublet person-id i family.people"
    id_set = set(ids)
    for p in family["people"]:
        for field in ("father", "mother", "sibof", "step", "spouse"):
            target = p.get(field)
            assert target is None or target in id_set, (p["id"], field, target)
        assert not must_be_private(p), f"Mulig privat person står i klartekst: {p['id']}"
    claim_ids = [c["id"] for c in research.get("claims", [])]
    assert len(claim_ids) == len(set(claim_ids)), "Dublet forskningsspor-id"
    for claim in research.get("claims", []):
        required = ("id", "branch", "title", "status", "claim", "evidence", "missing", "next", "sources", "person_ids")
        for field in required:
            assert field in claim, f"{claim.get('id', 'Ukendt spor')} mangler feltet {field}"
        assert claim["status"] in {"needs", "hypothesis", "family", "conflict"}, (claim["id"], claim["status"])
        assert isinstance(claim["sources"], list), f"{claim['id']}.sources skal være en liste"
        for source in claim["sources"]:
            assert isinstance(source, dict) and source.get("label") and source.get("url"), f"Ugyldig kilde i {claim['id']}"
        assert isinstance(claim["person_ids"], list), f"{claim['id']}.person_ids skal være en liste"
        for pid in claim.get("person_ids", []):
            assert pid in id_set, f"{claim['id']} henviser til ukendt person {pid}"
        dossier = claim.get("dossier")
        if dossier:
            assert os.path.isfile(os.path.join(ROOT, dossier)), f"Mangler dossier: {dossier}"
    assert isinstance(tree.get("map"), dict), "tree.map mangler"
    ingestion = tree.get("ingestion", {})
    for key in ("auto_ancestors", "auto_siblings", "manual_ancestors", "manual_siblings"):
        assert isinstance(ingestion.get(key, []), list), f"tree.ingestion.{key} skal være en liste"
    assert isinstance(ingestion.get("family_docs", {}), dict), "tree.ingestion.family_docs skal være et objekt"

if __name__ == "__main__":
    tree = load_json(SOURCE)
    validate(tree)
    write_json(os.path.join(ROOT, "data", "family.json"), tree["family"])
    write_json(os.path.join(ROOT, "data", "research.json"), tree["research"])
    write_json(os.path.join(ROOT, "data", "map.json"), tree["map"])
    print(f"Validated {len(tree['family']['people'])} people and {len(tree['research']['claims'])} research claims from data/tree.json")
