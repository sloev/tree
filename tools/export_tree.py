#!/usr/bin/env python3
"""Export the family tree as people plus a provenance-preserving relationship ledger.

Run from the repository root:
    python3 tools/export_tree.py
    python3 tools/export_tree.py --out-dir /tmp/tree-export

The exporter reads the generated data/family.json, applies family_docs.json patches
idempotently (the normal build already applies them), and reconciles GEDCOM family
records as a second representation. It never guesses biological parentage from
keywords, names, surnames, or the existence of a marriage.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def merge_patches(people, docs):
    """Mirror build_data.py patch semantics without duplicating already-built patches."""
    by_id = {p["id"]: p for p in people}
    for person_id, patch in (docs.get("patch") or {}).items():
        person = by_id.get(person_id)
        if person is None:
            continue
        for key, value in patch.items():
            if key == "note":
                old = person.get("note") or ""
                if value and value not in old:
                    person["note"] = (old + " " + value).strip()
            elif key in ("src", "occ"):
                old = person.setdefault(key, [])
                for item in value:
                    if item not in old:
                        old.append(item)
            elif key in ("bplace", "dplace") and value not in (None, ""):
                person[key] = value
            else:
                person[key] = value
    for raw in docs.get("people") or []:
        person = dict(raw)
        if not any(p["id"] == person.get("id") for p in people):
            people.append(person)
    return people


def parse_gedcom(path: Path):
    """Return INDI and FAM records, retaining raw tags needed for reconciliation."""
    individuals, families = {}, {}
    current_type = current_id = None
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        bits = raw.split(" ", 2)
        if len(bits) < 2:
            continue
        try:
            level = int(bits[0])
        except ValueError:
            continue
        xref = bits[1]
        tag = bits[2] if len(bits) > 2 else ""
        if level == 0:
            current_type = tag
            current_id = xref if xref.startswith("@") else None
            target = individuals if current_type == "INDI" else families if current_type == "FAM" else None
            if target is not None and current_id:
                target[current_id.strip("@")] = {"xref": current_id, "tags": []}
        elif current_type in ("INDI", "FAM") and current_id:
            target = individuals if current_type == "INDI" else families
            target[current_id.strip("@")]["tags"].append((level, xref, tag))
    return individuals, families


def gedcom_fields(record):
    out = defaultdict(list)
    for level, tag, value in record["tags"]:
        if level == 1:
            out[tag].append(value)
    return out


def build_export(family, docs, gedcom_path):
    people = merge_patches([dict(p) for p in family.get("people", [])], docs)
    ids = [p["id"] for p in people]
    if len(ids) != len(set(ids)):
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        raise ValueError(f"Duplicate person IDs: {dupes}")
    by_id = {p["id"]: p for p in people}
    edges = []

    def add(edge):
        # Keep separate source assertions, but suppress exact duplicate rows.
        if edge not in edges:
            edges.append(edge)

    # Structured source data. These are recorded links, not automatic proof of blood.
    for p in people:
        for field, role in (("father", "father"), ("mother", "mother")):
            target = p.get(field)
            if target:
                if target not in by_id:
                    raise ValueError(f"{p['id']} has missing {field} reference {target}")
                add({
                    "from": p["id"], "to": target, "relationship": "parent_child",
                    "role_from_child": role, "assertion_source": "family.json",
                    "biological_status": "not_assessed",
                    "evidence_status": "recorded_in_tree",
                    "sources": list(p.get("src") or []),
                    "context": p.get("note") or ""
                })
        target = p.get("step")
        if target:
            if target not in by_id:
                raise ValueError(f"{p['id']} has missing step reference {target}")
            add({
                "from": p["id"], "to": target, "relationship": "step_parent",
                "role_from_child": "step_parent", "assertion_source": "family.json",
                "biological_status": "not_implied",
                "evidence_status": "recorded_in_tree",
                "sources": list(p.get("src") or []),
                "context": p.get("note") or ""
            })
        sibling = p.get("sibof")
        if sibling:
            if sibling not in by_id:
                raise ValueError(f"{p['id']} has missing sibof reference {sibling}")
            add({
                "from": p["id"], "to": sibling, "relationship": "sibling_group_reference",
                "assertion_source": "family.json", "biological_status": "not_assessed",
                "evidence_status": "recorded_in_tree",
                "sources": list(p.get("src") or []),
                "context": "sibof is a grouping/reference field; it does not establish full or half-sibling status by itself."
            })
        target = p.get("spouse")
        if target:
            if target not in by_id:
                raise ValueError(f"{p['id']} has missing spouse reference {target}")
            add({
                "from": p["id"], "to": target, "relationship": "spouse_or_union",
                "assertion_source": "family.json", "biological_status": "not_implied",
                "evidence_status": "recorded_in_tree",
                "sources": list(p.get("src") or []),
                "context": "The source schema calls this spouse; dates and legal status are not inferred."
            })

    # GEDCOM is a separate assertion layer. PEDI is preserved verbatim and never
    # silently converted into biological parentage.
    ged_people, ged_families = parse_gedcom(gedcom_path)
    gedcom_person_ids = set(ged_people)
    for family_xref, record in ged_families.items():
        fields = gedcom_fields(record)
        husbands = fields.get("HUSB", [])
        wives = fields.get("WIFE", [])
        children = fields.get("CHIL", [])
        partners = husbands + wives
        for child_xref in children:
            child_id = child_xref.strip("@")
            if child_id not in gedcom_person_ids:
                continue
            # PEDI is nested under the child's FAMC structure in GEDCOM.
            child_tags = ged_people[child_id]["tags"]
            pedigree = []
            active_famc = None
            for level, tag, value in child_tags:
                if level == 1:
                    active_famc = value if tag == "FAMC" else None
                elif level == 2 and tag == "PEDI" and active_famc == record["xref"]:
                    pedigree.append(value)
            for parent_xref in partners:
                parent_id = parent_xref.strip("@")
                if parent_id not in gedcom_person_ids:
                    continue
                # Only assert GEDCOM family membership; FAM role and PEDI stay visible.
                add({
                    "from": child_id, "to": parent_id, "relationship": "gedcom_family_parent_link",
                    "role_from_child": "family_partner",
                    "assertion_source": "family-tree.ged",
                    "family_record": family_xref,
                    "gedcom_parent_role": "HUSB" if parent_xref in husbands else "WIFE",
                    "pedigree_tags": pedigree,
                    "biological_status": "unspecified",
                    "evidence_status": "gedcom_recorded"
                })
        for idx, a in enumerate(partners):
            for b in partners[idx + 1:]:
                add({
                    "from": a.strip("@"), "to": b.strip("@"),
                    "relationship": "gedcom_family_union",
                    "assertion_source": "family-tree.ged",
                    "family_record": family_xref,
                    "biological_status": "not_implied",
                    "evidence_status": "gedcom_recorded"
                })

    # Preserve all source material and notes on person records.
    out_people = []
    for p in people:
        out_people.append({
            "id": p.get("id"), "name": p.get("name"), "sex": p.get("sex"),
            "born": p.get("born"), "bplace": p.get("bplace"),
            "died": p.get("died"), "dplace": p.get("dplace"),
            "living": p.get("living", False), "private": p.get("private", False),
            "father": p.get("father"), "mother": p.get("mother"),
            "step": p.get("step"), "spouse": p.get("spouse"),
            "note": p.get("note"), "sources": p.get("src") or [],
            "occupations": p.get("occ") or [], "residences": p.get("res") or [],
            "confidence_person_record": p.get("conf"),
            "gedcom_present": p.get("id") in gedcom_person_ids
        })
    return {
        "metadata": {
            "purpose": "Research export; not an assertion that every recorded relationship is biological.",
            "people_count": len(out_people),
            "relationship_assertions_count": len(edges),
            "relationship_semantics": (
                "Each edge preserves its source representation. Biological status is not inferred "
                "from marriage, surname, GEDCOM family membership, legal paternity, or keywords."
            )
        },
        "people": out_people,
        "relationships": edges,
        "gedcom_only_individual_ids": sorted(gedcom_person_ids - set(by_id)),
        "tree_only_person_ids": sorted(set(by_id) - gedcom_person_ids)
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "lead" / "tree-export")
    parser.add_argument("--family", type=Path, default=ROOT / "data" / "family.json")
    parser.add_argument("--docs", type=Path, default=ROOT / "data" / "family_docs.json")
    parser.add_argument("--gedcom", type=Path, default=ROOT / "family-tree.ged")
    args = parser.parse_args()
    family, docs = load_json(args.family), load_json(args.docs)
    result = build_export(family, docs, args.gedcom)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "people.json").write_text(
        json.dumps({"metadata": result["metadata"], "people": result["people"]},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "relationships.json").write_text(
        json.dumps({"metadata": result["metadata"], "relationships": result["relationships"],
                    "gedcom_only_individual_ids": result["gedcom_only_individual_ids"],
                    "tree_only_person_ids": result["tree_only_person_ids"]},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(result['people'])} people and "
          f"{len(result['relationships'])} relationship assertions to {args.out_dir}")


if __name__ == "__main__":
    main()
