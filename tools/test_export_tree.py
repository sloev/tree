import tempfile
import unittest
from pathlib import Path

from export_tree import build_export


class ExportRelationshipTests(unittest.TestCase):
    def test_keeps_competing_parentage_claims_and_stepfather_distinct(self):
        people = [
            {"id": "child", "name": "Child", "sex": "M", "father": "family_father",
             "mother": "mother", "step": "stepfather", "spouse": None,
             "relationship_claims": [
                 {"person": "family_father", "relationship": "claimed_biological_parent",
                  "status": "family_claim", "biological_status": "disputed", "asserted_by": "family account",
                  "sources": ["family note"], "note": "Family account."},
                 {"person": "recorded_father", "relationship": "recorded_biological_parentage",
                  "status": "recorded", "biological_status": "disputed",
                  "asserted_by": "civil register", "sources": ["register"],
                  "note": "Declaration recorded; biological status unresolved."}
             ]},
            {"id": "family_father", "name": "Family father"},
            {"id": "recorded_father", "name": "Recorded father"},
            {"id": "mother", "name": "Mother"},
            {"id": "stepfather", "name": "Stepfather"}
        ]
        ged = """0 HEAD
0 @child@ INDI
1 FAMC @F1@
2 PEDI adopted
0 @family_father@ INDI
0 @recorded_father@ INDI
0 @mother@ INDI
0 @stepfather@ INDI
0 @F1@ FAM
1 HUSB @recorded_father@
1 WIFE @mother@
1 CHIL @child@
0 TRLR
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.ged"
            path.write_text(ged, encoding="utf-8")
            result = build_export({"people": people}, {}, path)

        edges = result["relationships"]
        family_claim = next(e for e in edges if e.get("relationship") == "claimed_biological_parent")
        recorded_claim = next(e for e in edges if e.get("relationship") == "paternity_declaration")
        step = next(e for e in edges if e.get("relationship") == "step_parent")
        gedcom_parent = next(e for e in edges if e.get("relationship") == "gedcom_family_parent_link"
                             and e.get("to") == "recorded_father")
        self.assertEqual(family_claim["biological_status"], "disputed")
        self.assertEqual(recorded_claim["evidence_status"], "recorded")
        self.assertEqual(recorded_claim["biological_status"], "disputed")
        self.assertFalse(any(e.get("relationship") == "parent_child" and e.get("to") in {"family_father", "recorded_father"} for e in edges))
        self.assertEqual(step["biological_status"], "not_implied")
        self.assertEqual(gedcom_parent["biological_status"], "unspecified")
        self.assertEqual(gedcom_parent["pedigree_tags"], ["adopted"])

    def test_family_document_patch_merge_is_idempotent(self):
        from export_tree import merge_patches
        people = [{"id": "p1", "name": "Person", "note": "Existing note",
                   "src": ["source A"], "occ": ["farmer"]}]
        docs = {"patch": {"p1": {"note": "Additional note",
                                  "src": ["source A", "source B"],
                                  "occ": ["farmer", "teacher"]}}}
        merge_patches(people, docs)
        merge_patches(people, docs)
        self.assertEqual(people[0]["note"], "Existing note Additional note")
        self.assertEqual(people[0]["src"], ["source A", "source B"])
        self.assertEqual(people[0]["occ"], ["farmer", "teacher"])


if __name__ == "__main__":
    unittest.main()
