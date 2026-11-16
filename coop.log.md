## 2026-11-16 — Frederik Christian III.727 death-record route

- Read current `research_method.md`, `leads/README.md`, `coop.log.md` and the Lorenz/Frederiksen dossier before research. Confirmed the project method: `main`, four active grandparent dossiers, evidence-status labels, no unsupported parentage edges.
- Followed the dossier's unresolved candidate match between Harbou's Frederik Christian III.727 (8 Jan 1775–21 May 1848) and the supplied “Christian Frederik Vilhelm” (1774–1848).
- Re-read Harbou's full entry and footnote 36. Harbou gives III.727's military career and death date, but no death locality in that entry; footnote 36 cites H. P. Selmer, `Nekrologiske Samlinger`, vol. II. Corrected the prior unsupported assumption that III.727 died at Bredsted: Harbou assigns Bredsted to his elder brother III.601, who died there in 1799.
- Identified relevant catalogue holdings at the Landeskirchliches Archiv Nordkirche / Archion: Bredstedt `Bestattungen 1831–1879` and index `Bredstedt_13`; Schleswig-Domgemeinde `Bestattungen 1823–1856` and burial-name index 1770–1874. Both cover 1848, but neither has yet been searched for III.727; catalogue entries are not proof of a burial. Archion images require access, and no original register image was inspected.
- Updated `leads/grandparent-lorenz-frederiksen.md` only; no canonical people, dates, relationships or edges changed. Commit: `9958e29140fc6d63b496a7022c1420500a0415f5` (https://github.com/sloev/tree/commit/9958e29140fc6d63b496a7022c1420500a0415f5).
- Validation: fetched the current source files and online source/catalogue pages; no local build, GEDCOM export, site build or browser test was run.
- Next action: inspect Selmer vol. II at Harbou's cited reference to establish locality/details, then inspect the appropriate 1848 burial index/register. If Selmer does not give a locality, test the Schleswig and Bredstedt indexes as bounded alternatives and corroborate identity by rank, family and residence. Keep the 1774–1848 supplied-person match speculative until independently corroborated.

## 2026-11-16 — Open research publication standard

The project owner clarified that research should remain visible on the public website while unresolved, so visitors can recognise details and contribute missing information. Agreed: the site is to function as an open research tree, not only a proven-facts tree. Unverified and competing claims should be visible with clear status and click-through explanations of provenance, evidence, limitations, missing records and concrete requests for help.

Updated:
- `research_method.md`: added the open-public-research standard, independent relationship-level statuses, public searchable research register requirements, contribution guidance, and a privacy/publication gate.
- `README.md`: added a public-facing explanation that credible unresolved leads should be published with explicit qualification and that visitors can contribute through Issues/PRs.

Important design requirements for the website implementation:
1. Visually distinguish established facts, claims needing evidence, hypotheses, family accounts, disputes and rejected leads. Do not rely on colour alone.
2. Clicking a person or relationship must explain the specific claim, source provenance, what it proves/does not prove, competing evidence, missing evidence and next check.
3. Represent relationships independently from person confidence; distinguish biological, legal/registered, step, adoptive, foster, guardian, household and marital ties. Never make a speculative biological link look settled.
4. Add a public research register with filters for person, place, family line, record type and status, plus actionable contribution requests and links to sources/history.
5. Publish reviewed public summaries from structured source data; do not expose unreviewed private dossier material or sensitive details about living people/informants.

This commit changes the publication policy and README only. The existing site already displays some person-level confidence and Lorenz's competing paternity claims in the person drawer, but it does not yet provide a complete structured public register of all four active dossiers, nor consistent click-through explanations for every uncertain relationship. Website implementation and audit remain outstanding. No canonical genealogy data changed. No local site build, GEDCOM export, browser test or deployment was run.

Commits: research method `dfbfb31136cf8406059d6a0e711357c192ee8ecc`; README `2340b5eb208addef9c0fb37a6065bc65094577d6`.

Next: design a structured, privacy-reviewed public research-claim dataset from the four active dossiers; wire it into a dedicated website research view and person/relationship drawers; then build and inspect the generated public output for privacy leaks and misleading edge styling.


## 16 November 2026 — first public research-register implementation

Implemented the first website-facing slice of the open-research policy:

- Added `data/research.json` as a separate structured, version-controlled register (eight initial claims across the four active grandparent dossiers).
- Added a `Forskningsspor` tab and public register view in `site/template.html`, with free-text search and status/branch filters.
- Each item visibly carries its uncertainty status and expands to show the claim, the evidence currently identified, what remains missing, the next research action, and a link to its active dossier.
- Added `site/build.py` injection for the structured research data.
- Added public contribution links to GitHub Issues and Pull Requests and a reminder not to publish sensitive information about living people.

The eight initial entries are a curated starting register, not a complete transcription of every note in all four dossiers. Some entries intentionally say that a source is identified but not yet inspected; do not upgrade them merely because they appear in the public register. Continue expanding the register from each active dossier, one claim at a time, with provenance and privacy review.

Validation performed: fetched the three changed files from `main`, parsed `data/research.json` as JSON, and checked that the tab, view, renderer, build placeholder and all four dossier links are present. A local Python site build, browser interaction test, deployment check and live-site inspection have **not** been run in this environment. Do not claim the public GitHub Pages site has changed until deployment is confirmed.


## 16 November 2026 — expand the public register and include source links

Expanded the structured public research register from 8 to **27 open claims**:
- Evald: 7 claims, including the 1764/1787 Rolsøgård probate, the separate 1820 Vibygård household, Rosmus identity conflict, Rousing parentage and Lovisa's missing mother.
- Liss: 6 claims, including Assing baptism, Kjersten's 1822 baptism, Hoven mill property context and Karen Jensen's date discrepancy.
- Gerda: 8 claims, including Kresten's possible mothers, Langø purchase/causeway, Iver Peder's 1910 contract, the 1787 probate and the reported family emigration.
- Lorenz: 6 claims, including the 1932 paternity file, Christian Adam's 1705 baptism, Frederik Christian III.727's 1848 death and the separate Kleist stem reconstructions.

Added curated source links to selected claims and a visible “Kilder og videre læsning” section in each expanded research card. Claims remain explicitly unresolved where the dossier says the original record has not been inspected; no canonical parent-child links or GEDCOM facts were changed.

Validation: JSON parses; 27 unique claim IDs; all entries point to one of the four active dossiers; all four branches and all three statuses are represented; the research tab/view/renderer, source-link UI and build injection are present. The automatic GitHub Actions rebuild for commit `a75e103` completed successfully and generated `docs/index.html`; the generated page was fetched from GitHub and checked for the tab, renderer, source section and newly added claim IDs. GitHub Pages deployment was still in progress at the time of this log entry.


## 16 November 2026 — person drawers linked to the public research register

Added claim-to-person references to 25 of the 27 public research entries (all referenced IDs checked against the 494 people in canonical `data/family.json`; no missing person IDs). Person drawers now show the relevant open research claims and a “Se belæg og hvad der mangler” control. Activating it closes the drawer, opens the research tab, expands that claim's evidence panel and scrolls it into view. Two broader branch-level claims remain available only in the register.

Validation: the main JavaScript function extracted from `site/template.html` passes JavaScript syntax compilation; the 27-record JSON parses; all claim IDs are unique; all dossier paths and person references resolve; the generated `docs/index.html` contains the tab, research renderer, source links, drawer claim controls and both later-added claim IDs. GitHub Actions rebuild completed successfully and the subsequent Pages build/deployment job completed successfully. The generated website output is committed by the workflow. This validates the build pipeline and Pages workflow; it is not a manual visual/browser usability review.

## 2026-11-16 — Grok agent: Dybbøl 1866 marriage null-result check

**Agent:** Grok (xAI)
**Task:** Follow previous handoff for the Dybbøl Ab 4 (Anne Christine Hansen / p53) 18 September 1866 marriage to Rasmus Jensen; perform bounded public-web and index search; record null result if no image or transcription appears.
**Branch policy:** main only; no branches or PRs.
**Files inspected:** research_method.md, leads/README.md, coop.log.md, leads/grandparent-lorenz-frederiksen.md (relevant sections on p52/p53).
**Files touched:** coop.log.md (this entry). No dossier or canonical data edited.

**Findings:**
- Bounded public-web searches (name + Dybbøl + 1866 + vielse/marriage variants, Arkivalieronline mentions) returned no index entry, transcription, or publicly accessible image of the 18 September 1866 Dybbøl marriage of Rasmus Jensen and Anne Christine Hansen.
- Earlier agent notes indicate the Arkivalieronline viewer can load the series index (Vielser 1723–1900) but systematic image paging for the specific entry has not yet been completed in this environment.
- Null result on publicly indexed sources. This does not prove the entry is absent; it remains a bounded negative search.

**Status:** No new evidence. No canonical people, dates, relationships or edges changed. Private/encrypted data not accessed.

**Unresolved / next concrete steps:**
1. Direct Arkivalieronline image retrieval and systematic paging of Dybbøl vielser series for 18 Sep 1866 (or nearest entries); transcribe if located.
2. If unavailable online, prepare precise archive enquiry to Rigsarkivet naming the persons, event, parish, date window and known references.
3. Alternative: rotate to another open lead in the Lorenz dossier (e.g., Selmer vol. II for Frederik Christian III.727 death locality, or 1932 paternity file).
4. Keep biological, legal and social parentage roles for Lorenz distinct.

**Handoff:** Small commits on main only. No private data exposed. Repositories remain strictly separated.

## 2026-11-16 — unified agent operating method and collaboration log

**Request:** repository owner asked that the agent method be updated for every agent working in this repository and that this collaboration log be maintained.

**Policy now made explicit in `AGENTS.md`:**
- Every agent must read `AGENTS.md`, `research_method.md`, relevant recent handoffs in this log, and the existing tracks in `data/tree.json` before work.
- `data/tree.json` → `research.claims[]` is the sole editable research registry. New evidence, leads, transcriptions, negative searches, conflicts, decisions and next steps are recorded in the relevant existing track; only genuinely new questions get a new track.
- Detailed research history is stored as dated, provenance-bearing `research_notes[]` on the track, not in sidecar files. Required note fields: `title`, `text`, `provenance`, `imported_on`.
- `leads/` and `research-archive/` are retired and must not be recreated as active workspaces. Generated JSON, GEDCOM, Markdown and HTML outputs must not be edited by hand.
- Source criticism, relationship/identity caution, public-data privacy, main-only collaboration, SHA-safe edits, build verification and truthful deployment reporting are mandatory.
- Every substantive agent task must append a dated summary here with affected tracks/files, commits, checks actually performed, outstanding checks and next action. This log is a handoff summary, not a parallel research ledger.

**Related repository state:** the single-source research method is documented in `research_method.md`; the public register and imported note rendering are in `data/tree.json` and the site template. The historical lead/archive directories and the obsolete `data/build_data.py` were removed in the cleanup sequence. Retired dossier pointers were removed from research records and migrated note provenance was normalized to human-readable archive descriptions.

**Validation / limitations:** repository file listings and research JSON were inspected through GitHub. The current canonical research register contains 54 tracks; detailed imported notes are stored on those tracks. A local Python build, GEDCOM export, browser/visual review and final Pages deployment check have not been performed as part of this log update. Do not infer those checks from a queued or unrelated Actions run.

**Next:** use this method for all future agents and keep this log current. Reconcile any remaining stale README references or generated-site links to retired dossiers, then run `python3 data/build.py`, `python3 data/export.py`, `python3 site/build.py` in a local checkout and verify the latest Actions/Pages run.

## 2026-11-16 — research loop: Evald probate cross-check and Liss local archive lead

**Task:** Continue finding new leads, ingest them into existing research tracks, and work the tracks iteratively.

**Tracks updated:**
- `evald-tohde-probate`: added a three-record comparison from Isgård-Kvelstrup G299 (Rasmus Christensen, 19 Feb 1772 fol. 58; Karen Christensdatter, 2 Jun 1774 fol. 90) and Rolsøgård G302 (Niels Jensen Degn, 14 May 1787 fol. 39). The comparison supports a testable hypothesis that the widow Karen Christensdatter in 1772/1774 is the Karen who inherited from Christen Christensen Tohde? and whose brother/guardian was Claus Gaardsted. No family edge was added; all three are published abstracts, not originals. Added the source URLs and a dated research note.
- `liss-marriage`: added Arkiv.dk A410, the Jens and Eli Kjær person archive at Sønder Felding Lokalhistoriske Arkiv. The catalogue includes local/genealogical notes for 1786–1844 and transcribed churchbook material for 1826–1860, a promising route for the 1843 marriage conflict. Added Horsbøl's secondary identification/date as corroboration only, not primary proof.

**Important source correction:** Rolsøgård G302's probate book is 1778–1816, so it cannot be the original 1764 probate cited in the 1787 abstract. The 1970 private-estate archive overview also lists Vosnæsgård G311 with holdings 1736–1743 and 1839–1850, not a 1764 probate book. The original 1764 jurisdiction/record remains unidentified. The Daisy justitsprotokol result is a distinct court series described as containing judgments; it was not treated as the probate file.

**Sources reviewed:** Isgård-Kvelstrup G299 PDF; Rolsøgård G302 PDF; Landsarkivet's 1970 inventory of private estate records; Rigsarkivet probate guidance; Arkiv.dk A410; Horsbøl genealogy page.

**Files changed:** `data/tree.json` only for the research ingestion; this entry updates the collaboration log. No people, dates or family edges were changed.

**Validation:** Fetched current file SHA before edit; JSON parsed before update. No local Python build, GEDCOM export, visual review or Pages deployment verification performed in this research loop.

**Next actions:** (1) identify which authority/estate held the 1764 Dejret probate of Christen Christensen Tohde?; (2) inspect original G299 records 1772 fol. 58 and 1774 fol. 90 if scans can be resolved; (3) request item-level detail from Sønder Felding Lokalhistoriske Arkiv for A410 nr. 15 and 22 before assuming they contain Liss's marriage.

## 2026-11-16 — research loop: Kolding baptism search aid

**Track updated:** `lorenz-danish-kleist-1775`.

**New lead:** Rigsarkivet's Arkivalieronline catalog exposes a Kolding Sankt Nikolaj name-register (1635–1891), with a scanned register unit. Added its official link and a note to the existing track. The title says “kirkebøger, viede og døde”; it is not yet established that it indexes baptisms in 1775. The AO web view exposed only the image-viewer shell in this environment, so no name lookup or negative result is claimed.

**Research implication:** the primary next step remains comparison of Kolding Sankt Nikolaj C 469-3 and C 469-7 for January 1775, checking both books and recording parents, residence, witnesses and exact event dates against Selmer (3 January) and Harbou (8 January).

**Sources:** Rigsarkivet Arkivalieronline Kolding Sankt Nikolaj name-register; Selmer's 1848–49 necrology; Harbou's Danish von Kleist history.

**Files changed:** `data/tree.json` and this `coop.log.md` entry. No person or family edge changed.

**Validation:** current SHA fetched before update; canonical JSON parsed before write. No local build/export, visual inspection or deployment check performed.

**Next:** inspect the register images and original C 469-3/C 469-7 pages; if inaccessible, use the Kolding Stadsarkiv transcription portal or request exact scans from Kolding Stadsarkiv.

## 2026-11-16 — research loop: bounded negative search in G299

**Track updated:** `evald-tohde-probate`.

**Finding:** searched the full text of the published Isgård-Kvelstrup G299 index/extract (1762–1812) for the exact form “Christen Christensen Tohde”. The PDF search did not return a separate entry for him. The index does contain Rasmus Christensen at Dejret (19 Feb 1772, no. 32, fol. 58) and Karen Christensdatter (2 Jun 1774, no. 50, fol. 90), which remain useful identity anchors. This is a bounded negative result in a standardized secondary extract only; it does not establish that the 1764 probate is absent.

**Refined next route:** do not continue looking for a 1764 original in Rolsøgård G302 (1778–1816) or assume it is in G299. Use the named family cluster and Dejret location to identify another estate/jurisdiction or surviving loose probate documents. Keep the father identity and sibling edges unaltered until an original source is found.

**Files changed:** `data/tree.json` and `coop.log.md`. Commit for the new track note: `ee4c597aed3893ce5e607f25cdc8d7b533ec0545`. No people, dates or family edges changed.

**Validation:** current file SHA fetched before update; canonical JSON parsed before write. No local build/export or Pages check performed.


## 2026-11-17 — research loop: Bogensholm G298, 1803 ownership record and Rousing disambiguation

**Tracks updated:**
- `evald-claus-probate-1811`: identified the original Bogensholm Gods G298 probate series (1800–1811), its register, Arkivalieronline unit and Hanne Vinter Henriksen's digital extract. The eight-case published extract has no separate Claus Gaardsted entry; this is a bounded negative result in the extract only, not proof that no original probate exists. Next: inspect the original register/protocol and 1811 auction records.
- `evald-bogensholm`: added the 6 August 1803 printed royal chancery memorandum that explicitly calls Claus Gaardsted owner and resident at Bogensholm. Added Trap 4 (1925), which gives 1797, alongside Trap 5's 1796 date. Ownership in 1803 is supported; acquisition year remains unresolved pending the original deed/pantebog.
- `evald-rousing-parentage`: added Skærsø G304 no. 206 (7 October 1813, fols. 331/336), a published extract for a Rasmus Jensen Rousing smith and wife Kirsten Thygesdatter at Visbeholm, with two daughters and named guardians. This is a new same-name disambiguation lead, not evidence that the man is p76 (Fuglslev, ca. 1780–1858); the original folios must establish the precise probate subject.

**Sources reviewed:** DS-Wiki Bogensholm archive page; Hanne Vinter Henriksen's Bogensholm G298 extract; Arkivalieronline link for G298; Trap 4 and Trap 5; *Kongelige Rescripter* 6 August 1803; Skærsø G304 published probate extract.

**Files changed:** `data/tree.json` and this `coop.log.md` entry. No people, dates or family edges were changed. No new research tracks or sidecar files were created.

**Validation:** fetched current source files and SHA values; parsed canonical `data/tree.json` as JSON before editing. No local Python build/export, visual review, original archive-image inspection or Pages deployment check was performed. The Arkivalieronline G298 series was identified, but its original images were not read.

**Next actions:** (1) inspect Bogensholm G298 register and original 1811 protocol; (2) locate the 1811 auction record for Bogensholm; (3) inspect Skærsø G304 no. 206, fols. 331/336; (4) continue the existing priority order for the 1764 Dejret probate, Liss's 1843 marriage and Kolding's January 1775 baptism.


## 2026-11-17 — research loop: narrow the 1764 Dejret probate to Isgård G299

**Track updated:** `evald-tohde-probate`.

**New archival route:** a cross-check of the Nørrejyske estate-place register and the Isgård estate inventory shows that Dejret in Tved parish was within Isgård Gods (G299), which has an original probate protocol and register for 1762–1812. The later G302 abstract describes Christen Christensen Tohde? as bailiff/foged in Dejret. Rigsarkivet's guidance says estate owners normally handled probate for their tenants and employees. This makes Isgård G299 the first original protocol to inspect for the 1764 case, although Tohde's employment by Isgård is not yet independently established.

**Negative-result qualification:** the previously checked published G299 extract has no separate named entry for Christen Christensen Tohde. That is not a search of the original G299 protocol/register and does not exclude an unindexed or differently named case.

**Sources reviewed:** DS-Wiki Isgård archive page; Nørrejyske estate-place register; Isgård G299 leasehold register for Dejret; Rigsarkivet probate guidance; earlier G299 published extract.

**Files changed:** `data/tree.json` and this `coop.log.md` entry. No new track or sidecar file; no family-tree people or relationships changed.

**Validation:** fetched current file contents and SHA values; parsed canonical JSON before editing. No original G299 images were inspected; no local build/export or Pages deployment check was performed.

**Next:** inspect Isgård G299's original register and protocol around 1764; if no case appears, identify the bailiff's employer and follow the correct jurisdiction under the pre-1793 rules.


## 2026-11-17 — research loop: correct Bogensholm chronology and deepen Skærsø Rousing lead

**Tracks updated:**
- `evald-bogensholm`: corrected a prior research-note error. Trap 4 (1925), pp. 666 ff., says Rosenkrantz sold Bogensholm to Claus Gaardsted in **1796**, not 1797; Trap 5 also says 1796. The previously reported 1796/1797 disagreement was caused by our transcription error and is withdrawn. The original deed remains uninspected.
- `evald-claus-probate-1811`: added Djurslandsdatabasen's secondary entry for Claus Gaardsted, born 1751 and died 1811 at Bogensholm. This agrees with the tree's approximate birth and the known death year, but provides no parents or spouse in the index. No precise birth date was added.
- `evald-rousing-parentage`: inspected the published Skærsø G304 extract, no. 206, 7 October 1813, fols. 331 and 336. It names Rasmus Jensen Rousing, smith at Visbeholm, wife Kirsten Thygesdatter, daughters Marie Cathrine (19) and Anne Elisabeth, and maternal uncle Peder Thygesen / paternal uncle Hans Jensen as guardians. This is a specific family group and makes identification with p76 (Fuglslev, ca. 1780) unlikely; original folios must confirm the deceased and relationships. No tree edges changed.

**Sources reviewed:** Trap 4 PDF, lines 1882–1897; Skærsø G304 published extract, lines 937–938; DS-Wiki Skærsø archive inventory; Djurslandsdatabasen Gaardsted index.

**Files changed:** `data/tree.json` and `coop.log.md`. No separate lead files and no family relationships created.

**Validation:** fetched current files and SHAs; parsed JSON before edit. Original G304 folios, Bogensholm deed and original Claus baptism not inspected. No local build/export or deployment check performed.

**Next:** inspect Skærsø G304 original fols. 331/336; locate original Bogensholm deed/realregister entry in Djurs Sønder-Mols Herred records; continue original-source checks on the remaining open claims.


## 2026-11-17 — research loop: Skærsø G304 no. 52 and Fuglslev Rasmus Jensen

**Track updated:** `evald-rousing-parentage`.

A second entry in the published Skærsø G304 abstract has been identified: no. 52, Esben Thygesen of Gravlev Mølle, 7 June 1762, fol. 135. The abstract names Esben's deceased sister Karen Thygesdatter and lists Rasmus Jensen in Fuglslev, Thyge Jensen in Fuglslev and Anne Jensdatter married to Rasmus Rasmussen in Gravlev among her children. This is a promising candidate family for p304 (Rasmus Jensen, ca. 1718, Fuglslev), potentially identifying his mother as Karen Thygesdatter and Esben as maternal uncle. It is not a proven match: the original folio and independent identity details are required.

The same G304 source also has no. 206 (1813), the Visbeholm smith Rasmus Jensen Rousing, wife Kirsten Thygesdatter and daughters. This remains a separate likely same-name individual, not merged with p76 or p304.

**Sources:** Skærsø G304 published extract, no. 52, fol. 135 and no. 206, fols. 331/336; DS-Wiki Skærsø archive inventory.

**Files changed:** `data/tree.json` and `coop.log.md`. No family edges or person facts changed.

**Validation:** current SHA fetched; JSON parsed before write. Original G304 folios not inspected; no local build/export or deployment check performed.

**Next:** inspect original G304 fol. 135; then search Skærsø leasehold register 1781–1820 and Fuglslev parish records for Rasmus Jensen's identity and children.


## 2026-11-17 — research loop: Rousing family identified across 1735 and 1762 probate extracts

**Track updated:** `evald-rousing-parentage`.

A major new corroborating source was found in Erik Brejl's *Skanderborg Rytterdistrikt* probate extracts: no. 1678, Maren Thygesdatter in Bryrup, 4 April 1735, fol. 96. It identifies her mother as Maren Pedersdatter, widow of Thyge Jespersen of Gravlev Mølle, and lists siblings including Karen Thygesdatter married to Jens Rasmussen in Fuglslev and Esben Thygesen in Gravlev Mølle. Read together with Skærsø G304 no. 52 (7 June 1762, fol. 135), which names Esben's deceased sister Karen and her children Rasmus Jensen and two others in/near Fuglslev, this materially strengthens the hypothesis that p304 (Rasmus Jensen, ca. 1718, Fuglslev) was a son of Karen Thygesdatter and Jens Rasmussen. Both are published extracts/transcriptions; neither original probate image has yet been independently inspected. No parentage edges were added.

A further route was found in the Skærsø leasehold register 1781–1820: entry no. 9, page 5, dated 31 October 1784, says Rasmus Jensen Smed of Fuglslev relinquished a holding due to old age with life support for himself and his wife. This could fit p304's approximate birth c.1718, but requires the original lease and corroborating records. Entry no. 43 (24 March 1800) separately names Rasmus Jensen Degn from Øster Alling as tenant of Gravlev Mølle after Thyge Mathiasen; do not conflate him with the Fuglslev Rasmus. The Gravlev Mølle transcription also contains a 1787 census entry for a 25-year-old Rasmus Jensen servant at the mill, a possible namesake kept separate pending original census review.

**Sources reviewed:** Erik Brejl, Skanderborg Rytterdistrikt probate extract no. 1678 (1735); Skærsø G304 transcript, no. 52, fol. 135; Skærsø leasehold register 1781–1820, entries 9 and 43; Gravlev Mølle transcription; Norddjursarkiver local history of Fuglslev.

**Files changed:** `data/tree.json` and `coop.log.md`. Added a dated, source-preserving note and stable source links to the existing track. No new track, sidecar file, person fact or family edge created.

**Validation:** parsed canonical JSON before update; confirmed current branch is `main`; fetched current blob SHA before each write. No original probate/lease images, original census image, local build/export or Pages deployment were checked.

**Next:** inspect original G304 fol. 135; inspect the original 1784 lease entry and identify the farm/household; then test the 1735/1762 family cluster against parish baptisms, marriage and the 1801 household. Keep p304 parentage and p152's parentage unchanged until those checks are complete.


## 2026-11-17 — research loop: Rasmus Jensen Smed matched across 1744, 1787 and lease records

**Track updated:** `evald-rousing-parentage`.

Further corroboration was found for the candidate Rasmus Jensen in Fuglslev. Karin Jørgensen's Tirstrup register (1704–1799) lists Rasmus Jensen Smed, unmarried, of Fuglslev, betrothed 8 March 1744 and married 8 July 1744 to Anne Cathrine Sørensdatter of Tirstrup. The register's author warns that it is unproofread and must be checked against the original churchbook. Aksel Rousing's *Fuglslev – en by og dens historie* (2006) transcribes the 1787 census for Møllegården: Rasmus Jensen Smed, 66, farmer; wife Ane Cathrine Sørensdatter, 65; daughter Mette Rasmusdatter, 36; granddaughter Ane Poulsdatter, 7. This is a strong name/place/occupation/spouse/age match to the candidate Rasmus named in G304 no. 52 and to p304 (born ca. 1718). A local churchbook index also reports the death in 1758 of Rasmus Jensen Smed's daughter Anne Cathrine, about six months old, and the 1744 marriage register supplies a matching wife. The original churchbook and census images remain uninspected.

**Chronology/property issue retained:** Skærsø lease register no. 9 is dated 31 October 1784 and says Rasmus Jensen Smed in Fuglslev relinquished a holding due to old age with aftægt for himself and wife. Aksel Rousing's later farm history lists Rasmus Jensen Smed as tenant of Møllegården in 1788 and his son-in-law Poul Hansen as successor in 1799. These may concern different properties or a multi-stage transition; do not silently reconcile them without the original lease deeds. The 1787 census age (66) is consistent with birth c.1720/21, close to p304's approximate c.1718.

**Sources reviewed:** Tirstrup churchbook name register (1744 marriage); Aksel Rousing, *Fuglslev – en by og dens historie* (1787 census transcription and farm chronology); Tirstrup-Fuglslev death index (1758 child); Skærsø lease register (1784 entry); earlier 1735 and 1762 probate extracts.

**Files changed:** `data/tree.json` and `coop.log.md`; added a dated evidence note and source links to the existing Rousing track. No new claim or sidecar file; no person facts or parentage edges changed.

**Validation:** canonical JSON parsed before update; current blob SHA fetched before writes. No original kirkebog, census, probate or lease images were read; no local build/export or deployment check performed.

**Next:** inspect the original 1744 marriage entry and the 1787 census image; search baptism/death entries for the children of Rasmus and Anne Cathrine; inspect the underlying 1784 and 1788/1799 lease documents to establish whether they refer to the same holding; then assess whether p304's parentage can be upgraded.


## 2026-11-17 — research loop: possible identification of Christen Gårdsted in Dejret

**Track updated:** `evald-tohde-probate`.

Hanne Vinter Henriksen's Isgård G299 lease-register transcription (1719–1823) has a highly relevant entry: Tved, Dejret; Christen Christensen Gårdsted; 1750; page 123; note: former bailiff at Rolsgård, taking the house vacated by Søren Pedersen Danmand. This is a strong candidate for the man called “Christen Christensen Tohde?” in Rolsøgård G302 no. 11 (14 May 1787, fol. 39): the name, Dejret location, and bailiff/Rolsgård connection align. The uncertain “Tohde?” may be a misreading or alternative nickname; it is not yet safe to equate the men.

The original archival route is now precisely identified via DS-Wiki Isgård: AO scan for G299 probate protocol 1762–1812 (epid 17176611), register (17176629), lease protocol 1719–1829 (21027118), and lease register (21027120). The web viewer cannot read the scanned images, so these are concrete manual inspection targets. The G299 public index extract did not list a separate 1764 probate under this name; that remains only a negative result in a secondary extract. The 1750 lease entry makes it particularly important to check the original G299 probate register/protocol around 1764 and lease page 123.

**Interpretive guardrail:** G302 describes Karen Christensdatter and Claus Gaardsted as “stedbørn” of the deceased Christen Christensen, not established biological children. No parentage or sibling edges were changed. The new entry may clarify the man's identity and jurisdiction, not the biological parentage of Claus/Karen by itself.

**Sources reviewed:** Isgård G299 lease register (1750, p.123); Rolsøgård G302 published extract (1787, fol.39); DS-Wiki Isgård; 1970 Landsarkiv inventory of private estate probate/lease records; Rigsarkivet AO catalogue links.

**Files changed:** `data/tree.json` and `coop.log.md`; appended a dated note to the existing track and added original AO links. No sidecar file, no new person, no family edge.

**Validation:** canonical JSON parsed before write; fetched current SHA before write. AO pages resolve to official scan viewer URLs, but original images were not read; no local build or deployment status checked in this cycle.

**Next:** inspect original G299 register/protocol around 1764 and original lease page 123; compare the handwritten name with “Tohde?” in original G302 fol.39. Confirm whether the 1764 deceased was a G299 tenant/employee and preserve the distinction between stepchildren and biological parentage.
