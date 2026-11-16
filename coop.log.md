# Cooperation log — sloev/tree

Append-only coordination log for the Gårdsted / Gedde family-history project. Agents read the latest entries before starting and append a dated handoff on completion. Work only on main. Never expose private data. Treat data/build_data.py as source of truth.

---

## 2026-11-16 — Grok agent: inspection and null result

**Agent:** Grok (xAI)
**Task:** Read research_method.md, AGENTS.md, leads/README.md, and lead/tree-research.md; confirm branch policy; record status of open genealogical leads without accessing private data.
**Branch policy:** main only; no branches or PRs.
**Files inspected:** README.md, AGENTS.md, research_method.md (stub), leads/README.md, lead/tree-research.md, data/ (structure only).
**Files touched:** coop.log.md (this new file).

**Findings:**
- research_method.md is a 224-byte placeholder referencing a missing /tmp file; it does not contain the expected research method, milestones, or handoffs. Active instructions are in AGENTS.md and leads/README.md (four grandparent dossiers are the authoritative research workspace).
- Canonical data remains data/build_data.py / data/family.json. Private records stay encrypted in data/private.enc. No private data decrypted or inspected.
- Open public leads (from ledger and prior handoffs) include Dybbøl 18 September 1866 marriage image for Rasmus Jensen / Anne Christine Hansen (p52/p53), and Zedler inspection for earlier von Woyten. No new primary evidence located in this pass.
- Null result: no new genealogical facts, relationships, or sources added. No changes to build_data.py or family.json.

**Status:** Research method file requires restoration. Four grandparent dossiers remain the active workspace. No expansion this run.

**Unresolved / next concrete steps:**
1. Restore a complete research_method.md from repository history or local agent records if available.
2. Continue systematic retrieval of the Dybbøl Ab 4 1866 marriage image via Arkivalieronline for transcription.
3. Inspect Zedler vol. 59 “Woyden, Woyten” for exact statements on earlier von Woyten figures.
4. Do not modify canonical data without primary evidence meeting the evidence rule in lead/tree-research.md.

**Handoff:** Small commits on main only. Never expose private data. Repositories remain strictly separated from earlysmolweb.

---

## 2026-11-16 — Grok agent: null-result confirmation

**Agent:** Grok (xAI)
**Task:** Confirm research_method.md status and open public leads; record null result without accessing private data or modifying canonical sources.
**Branch policy:** main only; no branches or PRs.
**Files inspected:** README.md, AGENTS.md, research_method.md (still stub), leads/README.md, coop.log.md.
**Files touched:** coop.log.md (this entry).

**Findings:**
- research_method.md remains a placeholder stub with no usable research method, milestones, or evidence rules beyond what is in AGENTS.md and the four grandparent dossiers.
- Canonical data remains data/build_data.py / data/family.json. Private records stay encrypted in data/private.enc. No private data decrypted, inspected, or exposed.
- Open public leads (Dybbøl 18 September 1866 marriage image; Zedler von Woyten inspection) unchanged. No new primary evidence located.
- Null result: no new genealogical facts, relationships, or sources added. No changes to build_data.py or family.json.

**Status:** Research method file still requires restoration. Four grandparent dossiers remain the active workspace. No expansion this run.

**Unresolved / next concrete steps:**
1. Restore a complete research_method.md from repository history or local agent records if available.
2. Continue systematic retrieval of the Dybbøl Ab 4 1866 marriage image via Arkivalieronline for transcription.
3. Inspect Zedler vol. 59 “Woyden, Woyten” for exact statements on earlier von Woyten figures.
4. Do not modify canonical data without primary evidence meeting the evidence rules in the dossiers and AGENTS.md.

**Handoff:** Small commits on main only. Never expose private data. Repositories remain strictly separated from earlysmolweb.

---

## 2026-11-16 — ChatGPT: reconcile current main and disputed Lorenz parentage

**Branch:** `main` (confirmed; no feature branch created).  
**Instructions read:** `AGENTS.md`, `README.md`, `leads/README.md`, latest `coop.log.md`, and the four active grandparent dossiers.  
**New supplement:** reviewed the archived `research-archive/family-tree-personal-info-2026-11-16.txt` reference and confirmed that its Wilhelm Krogh family/locality leads have already been consolidated into the Lorenz dossier. No private records were decrypted.

### Changes made

- Restored `research_method.md` as a usable, repository-specific research method. The former file was a 224-byte placeholder referring to an unavailable `/tmp` file; no missing milestone history was invented.
- Corrected Lorenz (`p6`) in canonical `data/build_data.py`: `father` is now unset while the biological parentage remains unresolved. The official register's designation of Wilhelm Krogh and the family's claim naming Sophus Petersen are retained as separate disputed relationship assertions. Peter Frederiksen remains a separate step-parent/social-father link.
- Synchronized `data/family.json`, `family-tree.ged` and `family-tree.md` so Sophus is no longer encoded as a settled biological father. The GEDCOM retains the maternal link and Lorenz's separate spouse/stepfather context; the text summary labels Sophus as the family's disputed candidate and Wilhelm as the register-recorded candidate.
- Updated `tools/export_tree.py` so evidence status and biological status are separate fields. Updated tests to assert that disputed candidates are not exported as settled parent-child edges.
- Updated the person-card presentation to distinguish a recorded/family-claimed assertion from disputed biological status.
- Added the official Rigsarkivet Dybbøl marriage-index route and the printed inventory description for Ab 4 to the Lorenz dossier. These confirm the catalogue path only; the 18 September 1866 entry has not yet been read.

### Validation and limits

- Parsed the current `data/family.json` successfully and checked that Lorenz has no settled father ID, while both candidate claims and their source descriptions remain present.
- Checked that the generated GEDCOM no longer contains a husband link from Sophus to Lorenz in the relevant family record.
- Confirmed the tree template contains the male/female symbols and the revised claim-status display.
- **Not run:** Python unit tests or the full data/GEDCOM/site build. This session had GitHub repository access but no network-capable local clone/runtime; generated files were synchronised for the Lorenz change by targeted edits. Do not treat this as a full build or deployment verification.
- No living-person records were decrypted, renamed or exposed.

### Next steps

1. Run `python3 -m unittest discover -s tools -p 'test_*.py'` and the documented build commands in a local checkout; inspect generated diffs.
2. Obtain/read the original 1932 county/court file if the family wants to resolve Lorenz's biological paternity; online catalogue discovery is currently exhausted.
3. Continue the Dybbøl 18 September 1866 marriage inspection via the official index and Ab 4 images; do not promote Hans Hansen/Ellen Kock until the entry is transcribed.
4. Follow the priority lists in the Evald, Liss and Gerda dossiers for their next primary-record checks.

**Privacy:** living-person protections and encrypted private records left intact.  
**Handoff:** main only; keep each new research claim in its one active grandparent dossier.

