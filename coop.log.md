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



---

## 2026-11-16 — ChatGPT: audit von Kleist medieval and early-modern leads

**Branch:** `main`.  
**Scope:** all Kleist-related material located in the four active dossiers, the archived legacy-leads archive, the archived cross-branch ledger, the personal-information supplement, and the relevant current tree records. The active owner remains `leads/grandparent-lorenz-frederiksen.md`.

### Work completed

- Consolidated the Kleist evidence leads into a new source-by-source audit in the Lorenz dossier, separating the medieval 1289/1364 material, the 1407/1435 Muttrin sequence, the 1477 three-line charter, the Damen/Bratta branch, the Borntin line to Pribislaff III.281 (p3472), the separate Tychow-Dubberow line, and collateral Woyten/Stojentin hypotheses.
- Rechecked the family association's 2025 Muttrin and Damen volumes, 2025 Tychow-Dubberow translation, Quandt's general-history chapter and charter interpretation, Harbou's 1897 Danish genealogy, and the online charter/person indexes.
- Recorded the material conflict over “Prissebur, Clest fratres” in Urk. 75; Quandt's brother interpretation is argued and challenged, not an uncontested literal statement.
- Corrected the working date note: Urk. 83 is indexed as 1364 for Prissebur of Muttrin; Urk. 84 is 1368 for Dubbeslaff Cleest.
- Confirmed Harbou explicitly identifies Cartz Ulrik III.369 as son of Pribislaff III.281 and Esther von Kameke, and that the family-association register identifies Pribislaff III.281 as dying in 1698. The parents of Pribislaff III.281 remain unresolved in canonical data.
- Preserved the Reimer/Bartes father conflict between the 2025 Tychow-Dubberow genealogy and Quandt's reading of the 1477 charter.
- Kept the von Woyten and von Stojentin proposed medieval ancestry separate from the direct male Kleist line.

### Repository changes

- Updated only `leads/grandparent-lorenz-frederiksen.md` with the full audit, source grading, open contradictions and a prioritized source retrieval plan.
- No canonical people or parent relationships changed; no edits to `data/build_data.py`, `data/family.json`, GEDCOM or generated site.
- No private/encrypted records were opened or decrypted.

### Validation and limits

- Read current main repository tree and relevant files through GitHub.
- Web source checks included the family association's official document indexes and the digitized family-history PDFs.
- The original medieval charter images themselves were not inspected in this pass. The available transcriptions and family-history interpretations are not substitutes for those originals.
- No local Python tests, full build, or deployment verification were run.

### Next steps

1. Retrieve and transcribe Urk. 75, 83, 100, 104, 125 and 192 from the document book/original archive.
2. Inspect the 2025 Muttrin German biography around III.281 / p.277 and resolve the III.186 → III.281 crosswalk.
3. Inspect the 1576 genealogy and older Glineke letter cited for Prissebur's sons.
4. Compare the German Tychow-Dubberow volume and original 1477 charter to resolve Reimer/Bartes.
5. Only after those checks consider whether any disputed parent links should enter canonical data.

**Handoff:** all findings and next actions live in the Lorenz dossier; archive material remains provenance-only. Main branch only.


### Audit follow-up — expanded tree exports checked

A second pass searched the complete expanded JSON, GEDCOM and text exports plus the archived personal-information supplement, rather than relying only on the narrative archive. This located and evaluated the research-only IDs exp020–exp042 and the associated collateral spouses/parents.

Important clarification incorporated into the dossier:
- The 2025 Muttrin genealogy explicitly states that Pribislaff III.281 (p3472) was the son of Hans Jürgen III.186 and an unnamed daughter of Achatz III.110. The expanded record exp033 has the narrative child assertion, but p3472's own structured `father` and `mother` fields remain null. This is a data-model/encoding gap, not absence of a published parentage claim.
- The same 2025 genealogy identifies p3473 as Anna Esther von Kameke of Kratzig, daughter of Jacob von Kameke of Körlin and Catharina von Koller; the expanded export has exp036/exp037 but canonical p3473 has no parent links.
- The expanded note also records the reported beheading-after-duel tradition for Pribislaff and lists his other children. These have been retained as sourced tradition/collateral leads, not asserted as established fact.
- The full proposed path exp020–exp042 has been written into the Lorenz dossier with source-by-source grades and the limits of each generation.

No canonical data or GEDCOM edges were changed. No local tests/build were run.


### Medieval source-critical follow-up — Urk. 75, Nycolaus Klest (1325), Urk. 83

- Compared the 1862 Kleist Urkundenbuch transcription of Urk. 75 with the 1888 Pommersches Urkundenbuch transcription. The former prints `Prissebur, Clest fratres` and says the original has a comma between the two names; the latter prints `Prissebur, Clest, fratres`. Both editions note the source as the original Bukow charter in the Stettin State Archive, damaged by moisture, with seal detached. The grammatical reading is disputed.
- Read Eberhard Sauer's 1937 dissertation extracts (published 1939), which explicitly argues that “Prissebur, [the] Clest brothers” is possible and that Kratz/Quandt's brother reading is not proven. Sauer emphasizes the gap between the 1289 witnesses, Nycolaus Klest in 1325 and Prissebur of Muttrin in 1364; he does not establish a link among them.
- Located the 1325 charter itself in Pommersches Urkundenbuch VI, Urk. 3888. It names Nycolaus Klest as a witness to a Dargun boundary settlement; the edition says it is based on the original in the Hauptarchiv Schwerin, Dargun collection. The record does not state his residence or parentage. Sauer's possible Kolberg citizenship is an interpretation only.
- Reconfirmed Urk. 83 (22 June 1364) in the Kleist Urkundenbuch. Its source note identifies a 1589 transsumpt and several sixteenth-century copies, not the original 1364 parchment. Also found a typo in the current family-association “Wichtige Urkunden” summary which calls Urk. 83 1368; the document itself and other indexes give 1364, while Urk. 84 is the 1368 Dubbeslaff record.
- Updated the Lorenz dossier with the source-critical comparison and revised assessment: Urk. 75 → Urk. 83 is not proven; the 1325 Nycolaus is an independent name-bearing witness, not a bridge. No canonical parent links changed.
- Sources read: https://v-kleist.com/FG/urkunden/Urkundenbuch_3.pdf ; https://kpbc.umk.pl/Content/23561/PDF/Pomorze_062_05.pdf ; https://kpbc.umk.pl/Content/23455/PDF/Pomorze_062_12.pdf ; https://v-kleist.com/FG/Adel_Ostpommern.htm ; https://v-kleist.com/FG/Muttrin/Muttrin.pdf
- No local tests/build/deployment run. No private records opened.


### 1477 charter and Quandt's three-period framework

- Read Quandt's methodological section in the General History (pp. 45–46). He explicitly calls the genealogy from 1477 onward a secure family tree (with some documentary differences and inserted persons needing investigation); from 1316 to 1477 he says only some genealogical connections are established; before 1316 the origin and affiliations of the three name-bearing men remain to be investigated. This is now stated as the source hierarchy in the dossier.
- Transcribed the key 1477 Urk. 125 passage from the Kleist Urkundenbuch. The edition is based on a sixteenth-century authenticated copy, with further transsumpts in 1546, 1568 and 1621, not the original 1477 parchment.
- The 1477 copy explicitly lists “Pribbeslaff to Muttrin with his sons, the brothers Reymer and Bartes to Tichow” and records the Kleists' testimony that three branches descended from an unnamed “Oldervader” and his three sons. This is a valuable legal/family statement, but does not identify the Oldervater with Klest de Densin.
- Quandt documents the Reimer/Bartes contradiction: 1477 places them as sons of Pribbeslaff of Muttrin; the 1618 genealogy places the Tychow line under Hans, repeated in 1621 and the 1706 compilation. The 1575/1601 fief letters describe Muttrin descendants from Prissebur but the underlying “Nachrichtung” is lost.
- Updated dossier with source text, provenance, and evidence grades. No canonical family data changed.

### 2026-11-16 — Privacy correction: Jørgen and Vivi

- Corrected the person mapping: Jørgen is p2; Vivi is p3. The divorced historical union is between those two people, not the separate later family union represented by x_kirill.
- Removed p2.spouse from the public/current-partner fields and added a separate union_statuses record for p2 + p3 with status divorced. The GEDCOM retains the historical family unit, its child, and a divorce marker.
- Kept Jørgen's public name and personal details anonymised. His parent links (p4 and p5) remain in the public tree; ancestry has not been suppressed.
- Published Vivi's name (p3) under her explicit consent. Her parents and other family links remain intact. Her separate family connection to x_kirill and their children was restored and not marked divorced.
- Updated the private-data merge so unlocking does not reintroduce Jørgen as Vivi's current partner.
- The public Pages HTML now contains Vivi's consented name, Jørgen's anonymised stub, the corrected divorced union status, and the updated unlock logic.
- Confirmed the tree template already renders the gender symbols ♀/♂ with the requested pink/blue styling.
- No private encrypted records were decrypted. No tests or full build were run locally; generated GEDCOM and public Pages content were inspected after the repository updates.
