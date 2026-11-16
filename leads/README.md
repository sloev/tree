# Genealogical leads

This directory consolidates the readable uploads, the prior research file, and the original ZIP export.

## Contents

- [Complete ancestry register](ancestry-register.md) — all readable material transcribed from tree2.txt, including profiles, relationships, notes, citations, image names, archival identifiers, caveats and statistics.
- [Consolidated branch dossiers](branch-dossiers.md) — both dossier files, combined and reformatted.
- [Investigation worklist](investigation-worklist.md) — actionable leads and conflicts extracted from the source material.
- [Research notes](research-notes.md) — first source checks, corrections, archival search routes and findings.
- [Earlier tree research](tree-research.md) — prior von Woyten, von Stojentin, von Kleist and Gedde research, plus the all-connections evidence policy.
- [Archive review leads](archive-review-leads.md) — review of the unpacked export and its image-based leads.
- [Independent research and GEDCOM audit](independent-research-2026-11.md) — independent source checks, the four JSON-only people missing from GEDCOM, and next archival steps.
- [Original ZIP export](family-tree-export.zip) — retained byte-for-byte as supplied. Its contents have been unpacked and reviewed; the original archive remains the untouched source package.

## Source and evidence policy

The uploaded files are derivative research compilations. Treat their assertions as leads, not primary evidence. Verify parentage and identity against original parish registers, census schedules, probate, court/paternity files, military records, and contemporary archival documents. Preserve negative searches and conflicting evidence. Do not merge hypotheses into data/build_data.py without primary-source support.

## Privacy

The ZIP includes an encrypted private_blob field described as containing details for living/private people. It was not decrypted or inspected. The extracted working copy excludes that encrypted payload; living people remain redacted. Do not attempt to decrypt data/private.enc or infer private identities from family-link structure.
