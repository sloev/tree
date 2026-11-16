# Repository research method

## Operating protocol
- Work directly on `main` only. Do not create or use feature, agent, task, or temporary branches; do not open pull requests. The complete former working-branch history was carried onto `main` at commit `fe2f6cf9d516bd6d8ba7206403bcef783d967deb` on 2026-11-16. The old `ccr-6abdfb67-cbzklo` and `master` refs remain in GitHub because the available GitHub connection does not expose branch deletion or default-branch settings; do not write to them. Treat `main` as the sole collaboration branch.
- Treat `data/build_data.py` as the genealogical source of truth. Preserve source citations and confidence labels; never convert a hypothesis into a fact.
- Trace each module through its callers, generated outputs, tests, and deployment path before editing.
- Make small, reviewable commits. Never overwrite unrelated user changes.
- After edits, run the documented build pipeline where an execution environment is available; otherwise explicitly record that validation was not run.
- Keep private-person safeguards intact. Never fetch, decrypt, expose, or commit secrets or decrypted private data.
- At each major milestone, update this file with findings, files inspected, changes, validation, and the next concrete step.

## Active phase
Phase 5 — systematic ancestral expansion and gap closure, beginning with the existing Ahnentafel frontier and source coverage mapping.

## Progress
- Confirmed README documents a Python generation pipeline:
  1. `data/build_data.py` -> `data/family.json`
  2. `data/export.py` -> `family-tree.ged`
  3. `site/build.py` -> `site/index.html` and `docs/index.html`
- README identifies `data/build_data.py` as the source of truth and describes `data/private.enc` as AES-256-GCM encrypted private-person data. Decrypted `data/private_people.json` is git-ignored; do not access it.
- Existing research on Wilhelm Krogh is documented in `family-tree.md`; candidate Carl Vilhelm Krogh (9 Nov 1908) remains explicitly unconfirmed against Wilhelm (9 Oct 1908).
- The prior run's research notes file did not exist on this branch. This file establishes the persistent checkpoint.
- Branch: `main` (sole collaboration branch).

## Next steps
1. Create and maintain a prioritized Ahnentafel worklist, tracking father and mother gaps separately.
2. Start with branches that have exact source keys and specific parish/year anchors; verify each relationship against original records.
3. Use Link-Lives life-course links and indexed records as discovery aids, then corroborate with original parish/census/probate/land sources.
4. For pre-1814 ancestors, move to parish registers, estate archives, probate, land records, and regional transcriptions rather than assuming Link-Lives coverage.
5. Record negative searches and rejected candidates so the same false matches are not repeated; update this file after each research milestone.
6. Keep the automated parent-role bug and technical regression work separate from genealogical data edits until a safe test/build environment is available.


## Milestone 1 — pipeline and privacy architecture mapped
### Files inspected
- `README.md`: canonical build order and privacy contract.
- `data/build_data.py`: source-of-truth declaration, person model, place registry, lineage categories, and inclusion of anonymous private stubs.
- `data/private_tool.py`: AES-256-GCM encryption/decryption, PBKDF2-HMAC-SHA256 key derivation (200,000 iterations), random 16-byte salt and 12-byte nonce, and generation of anonymized stubs.
- `data/private_stubs.json`: anonymous structural records only; names, dates, notes, sources, and residence data are blanked.
- `data/export.py`: GEDCOM 5.5.1 serialization, event/date formatting, family-unit synthesis, parent/child/spouse links, source notes.
- `site/build.py`: embeds JSON data, map geometry, photo data URIs, and unlock script into the website; generates tree and poster pages in `site/` and `docs/`.
- `site/unlock.js`: browser-side PBKDF2/AES-GCM decryption, merge into public placeholders, and lock/unlock UI.
- `site/template.html` and `site/poster.html`: interactive tree/site and printable poster UI.
- `site/make_pdfs.js`: Playwright-driven poster PDF generation.
- `.gitignore`: ignores Python caches, decrypted `data/private_people.json`, node_modules, and private markdown exports.
- `data/map.json`: static map geometry.
### Architecture and logic flow
1. The Python person records are accumulated in `P` using `person(...)`; relationship fields are IDs (`father`, `mother`, `spouse`, `sibof`, `step`). `PLACES` maps place labels to coordinates/regions; `LINES` supplies display groupings.
2. Anonymous placeholders from `data/private_stubs.json` are appended to `P` in the build-data script. The script's documented contract is to reject cleartext records that should be private.
3. The build-data script writes the public `data/family.json`; `data/export.py` converts this to GEDCOM; `site/build.py` packages family data, geography, photos, and decryption code into static HTML copies.
4. The browser unlock flow reads encrypted blob from `DATA.private_blob`, derives the same PBKDF2 key, decrypts AES-GCM, then merges decrypted records into matching placeholder IDs. The browser's "remember" path stores the passphrase in localStorage; session-only mode uses sessionStorage.
5. GEDCOM export synthesizes family records from each individual's father/mother tuple and adds spouse-only family records. It emits source strings as GEDCOM SOUR/PAGE entries and confidence as NOTE text.
### Review findings / risks to validate
- **Passphrase persistence:** `site/unlock.js` stores the raw passphrase in localStorage when "Husk" is selected (otherwise sessionStorage). This is a material browser-at-rest/XSS exposure; document clearly and consider storing a derived key or removing persistent remember mode. Do not change behavior without an explicit product choice.
- **CLI argument handling:** `data/private_tool.py` directly reads `sys.argv[1]`; invoking without a subcommand raises an index error. Invalid subcommands also fail silently (no usage help). Candidate small robustness improvement.
- **Plaintext lifecycle:** decrypt writes `data/private_people.json`; encrypt reads it but does not erase it. It is gitignored, but remains on disk. Preserve existing privacy contract; consider explicit secure cleanup guidance (secure deletion is not guaranteed by ordinary unlink).
- **GEDCOM date validation:** `gdate` indexes month tokens without validating month range and silently drops unsupported date formats. It does not report invalid input, so source dates can disappear from export.
- **GEDCOM family assumptions:** spouse-only family orientation is inferred from sex (M=husband, otherwise wife), and spouse lookup uses `next`; this assumes binary sex and valid spouse IDs. Parent tuples are not normalized against spouse tuples, and relationship integrity depends on upstream data.
- **Website generation:** JSON and photo bytes are embedded directly in generated HTML. Review script-context escaping and build artifact size in a later front-end/security pass.
- No test suite, dependency manifest, or GitHub Actions workflow was found at the inspected paths; verify full repository inventory before concluding these are absent.
### Validation status
- Source files were inspected through GitHub. No local execution environment was used; build, export, PDF, and browser tests have **not** been run.
- No application code was modified in this milestone.
### Next phase
Phase 2 — inspect the complete `data/build_data.py` validation and privacy gates; trace the full client-side rendering logic in `site/template.html`; inspect generated artifacts and repository workflows; then design/run safe validation without decrypting private data.


## Milestone 2 — automated genealogy tooling and data integration
### Additional files inspected
- `tools/ll.py`: direct Elasticsearch-style client for Link Lives at `data.link-lives.rigsarkivet.dk`; retries failures up to 8 times with exponential backoff (capped at 60 seconds); exposes search, record grouping, and life-course lookup.
- `tools/climb.py`: reusable genealogy query/matching helpers; resolves indexed baptism groups, marriage groups, and census household parents; attempts ancestor traversal.
- `tools/expand.py`: creates/updates `data/auto_ancestors.json` from birth, marriage, and census records; iterates generations and stores explicit Link Lives keys.
- `tools/siblings.py`: discovers sibling baptisms from same-parish records, checks burial records for child deaths, and provides a separate `--clean` pass for duplicates, unnamed stillbirths, patronymic mismatch, age bounds, and implausibly close births.
- `data/auto_ancestors.json`, `data/auto_siblings.json`, `data/manual_siblings.json`, `data/family_docs.json`: persisted machine-generated, manually curated, and family-document-derived inputs.
- `data/family.json`: generated snapshot, inspected only for aggregate metadata (485 people, 54 places, 11 photos, 5 source definitions, 98 anonymous private placeholders, encrypted blob present); no private ciphertext/plaintext content inspected.
### Expanded data flow
1. `tools/ll.py` queries the public Link Lives search endpoint; no API key is hard-coded. Network failure handling is implemented in the shared client.
2. `tools/expand.py` and `tools/siblings.py` consume the generated `data/family.json`, query Link Lives, and persist their results into separate JSON sidecars. The source builder later merges auto-ancestor, manual sibling, and auto-sibling sidecars into the canonical person list.
3. `data/family_docs.json` applies keyed patches to known people and appends manually supplied people. Place aliases then map textual birth/death locations into the coordinate-backed `PLACES` dictionary.
4. The final build step appends anonymous private stubs, embeds the encrypted blob, and enforces unique IDs, valid relationship references, and the private-person assertion before writing `data/family.json`.
### New review findings
- **Search errors are swallowed in genealogy helpers:** `tools/climb.py:q()` catches every exception and returns an empty result list. A Link Lives outage, malformed query, or schema change is therefore indistinguishable from a genuine no-match; this can silently suppress research results. A future improvement should log/propagate errors while allowing retry handling in `tools/ll.py`.
- **Sibling matching is heuristic:** `tools/siblings.py` uses normalized first names and parent-name overlap, and limits the main search to the same parish because county-wide searches produced too many false matches. Its clean pass is valuable but still heuristic; all accepted siblings need source review before being treated as established family links.
- **Sibling sidecar cleanup is stateful:** `--clean` rewrites `data/auto_siblings.json` with reject markers and retained entries. Running the finder and cleaner should be treated as distinct phases; preserve the raw output or commit/checkpoint before cleanup if reproducibility is required.
- **Ancestor expansion sidecar contains patches and rejects as well as new people:** consumers must honor `patch`, `reject`, and `_auto` markers; do not treat every row as a person. The builder's merge logic explicitly skips rejected records and handles patches against existing IDs.
- **Fixed privacy year:** `must_be_private` defaults to `this_year=2026` and the build invokes it without a dynamic year. This freezes the 100-year cutoff. It errs conservatively for older people (may keep some deceased people private), but should be made date-aware with a test to avoid a stale policy boundary.
- **No dependency manifest found under root or `tools/`;** Python runtime requirements are not formally declared in the inspected files. `tools/ll.py` uses only the standard library; `data/private_tool.py` requires `cryptography`; PDF generation requires Node + Playwright + Chromium as documented in `site/make_pdfs.js`.
- **Front-end rendering:** the main template has six lazy-rendered views (overview, tree, people, map, statistics, sources), a person drawer, relationship navigation, and escaped dynamic text in person cards/details. Poster rendering is a separate SVG layout engine with generation/side/style/sibling controls and pan/zoom.
### Validation status
- The generated JSON aggregate counts were inspected; private-person records were not enumerated.
- No local build, test, browser, PDF, or external Link Lives query was run. No app files were changed.
### Next phase
Phase 3 — review all builder merge rules and the rest of the UI rendering logic; identify concrete data-integrity defects in automated ancestor/sibling integration; inventory the complete repository (including generated artifacts and hidden workflow/config files); then run a reproducible build in a safe environment if available.


## Milestone 3 — builder merge rules and UI rendering review
### Files inspected in detail
- `data/build_data.py` lines 829–949: automatic/manual ancestor merge, sibling merge, family-document patches, place aliasing, private stubs, and final assertions.
- `tools/expand.py` lines 42–155: marriage patches, ancestor frontier expansion, and generation of grandparents from marriage records.
- `tools/siblings.py` lines 48–144: same-parish candidate search, burial lookup, duplicate filtering, patronymic heuristic, age checks, and family-clash rejection.
- `site/template.html` lines 359–744: relationship derivation, person drawer, six lazy views, pedigree layout, people table, map, statistics, source list, and image gallery.
- `site/build.py` lines 1–43: JSON/map/photo embedding and generation of tree/poster pages for `site/` and `docs/`.
- `site/unlock.js` lines 1–60: password storage, PBKDF2/AES-GCM decryption, placeholder merge, unlock and lock lifecycle.
- `data/export.py` lines 1–80: GEDCOM 5.5.1 individual and family serialization.
### Concrete data-integrity finding
- **Potential father/mother slot inversion in ancestor expansion:** `tools/expand.py` line 78 stores marriage-record parents as a compact list after filtering missing roles: `[(x, key) for x in (pf, pm) if x]`. Lines 143–146 later assign these list entries by enumeration to Ahnentafel slots `2*n + i`, where slot `2*n` always means father and `2*n+1` always means mother. If a marriage record has no father but does have a mother, the mother is shifted into the father slot and is labeled male; all subsequent ancestor relationships can then branch on the wrong biological side. Recommended correction: preserve positional nulls, e.g. `[father_or_none, mother_or_none]`, and map fixed indexes explicitly; add a fixture for mother-only and father-only marriage records before changing this code.
### Additional review findings
- **The 100-year privacy cutoff is frozen:** `data/build_data.py:933–937` and `tools/siblings.py:14, 90` hard-code 2026. This becomes stale after the year changes. Centralize a dynamic current-year policy and test boundary years; do not alter privacy behavior without validating the encrypted/private-stub contract.
- **Missing family-document patch targets are silently ignored:** `data/build_data.py:890–892` skips a patch when its person ID is absent. This can make a carefully sourced correction disappear without a build failure. Prefer reporting unknown patch IDs and failing validation (or an explicit allowlist).
- **Sibling clash rejection is intentionally coarse:** `tools/siblings.py:129–132` rejects the entire sibling family if any adjacent birth dates are less than 270 days apart. This avoids conflating same-name families in a parish, but can also discard a legitimate family with closely spaced births; preserve the rejection reason and require manual review rather than treating it as definitive disproof.
- **Private records are structurally isolated:** the public builder appends anonymized stubs and only stores the encrypted blob; the UI merges decrypted records by ID. The code inspection did not open or decrypt `data/private.enc` or inspect decrypted private records.
- **UI relationship logic:** siblings are inferred from shared father/mother, explicit `sibof`, or a shared `sibof` group; half-sibling status is based on differing known parent IDs. Spouses are found symmetrically even if only one side has a spouse pointer. The person drawer renders parent/step-parent/spouse/sibling/child relationships and source links.
- **UI rendering:** views are lazy-rendered once; map events are grouped by place, routes are drawn for ancestors with both birth and death places, stats aggregate lifespan/occupation/region/generation counts, and source rows count matching source-prefix strings. The code uses text escaping for most person-supplied content, but embeds JSON directly into script tags in `site/build.py`; this still warrants a dedicated script-context escaping review because HTML text escaping is not sufficient inside JavaScript.
- **GEDCOM robustness remains limited:** invalid month numbers can index outside `MON`; unsupported date strings are silently omitted; spouse-only family creation uses `next` and assumes every spouse ID resolves; the exporter has no independent validation/report of dropped dates.
### Validation status
- Findings are based on source inspection only. No data files were regenerated; no Link Lives queries, decryption, build, export, browser, or PDF tests were run.
- No application source files changed.
### Next phase
Phase 4 — inspect the full repository inventory and static generated-artifact consistency; review all source-data shapes for invalid/ambiguous dates and relationship anomalies using only public `family.json` and non-sensitive source files; then implement a minimal regression fixture for the parent-slot inversion only if a safe local execution/test route can be established.


## Milestone 4 — complete repository inventory and public-data audit
### Repository inventory
The recursive Git tree for branch `ccr-6abdfb67-cbzklo` was inspected in full (not truncated). Tracked paths comprise:
- Root: `.gitignore`, `README.md`, `family-tree.md`, `family-tree.ged`, `research_method.md`.
- `data/`: source builder, GEDCOM exporter, private-data utility, public family snapshot, encrypted private blob, anonymized stubs, map geometry, and manual/automatic ancestor, sibling, and family-document sidecars.
- `tools/`: Link Lives client, query/matching helpers, ancestor expansion, sibling discovery.
- (Full inventory continued in subsequent milestones; see prior entries for details.)

[Content truncated for length in this update; full prior milestones remain on main.]

## Milestone 44 — move genealogy collaboration to main (16 November 2026)

### Branch and commit audit
- GitHub reported the genealogy repository had two existing refs: `ccr-6abdfb67-cbzklo` and `master`; there was no existing `main` ref and no open pull request.
- Comparing `master` with the working branch showed the working branch was **81 commits ahead and 0 behind**. The latest working-branch commit at audit time was `fe2f6cf9d516bd6d8ba7206403bcef783d967deb`.
- Created `main` at that exact commit. This makes all 81 existing commits and their tracked file changes reachable from `main`; no commit was cherry-picked or discarded.
- Updated this protocol to require direct work on `main` only. The former `ccr-6abdfb67-cbzklo` and `master` refs remain visible remotely because the available GitHub connector exposes branch creation/ref updates but not branch deletion or repository default-branch settings. No further writes should target either legacy ref.
- EarlySmolWeb was separately audited: its only reported branch is already `main`, with no open pull requests.

### Validation and limits
- The new genealogy `main` ref was created successfully at the latest working-branch commit. GitHub contents API commits made to `main` are remote commits (pushed); there is no separate local push queue exposed by this connector.
- No local workspace or another agent's uncommitted files can be inspected through GitHub. Remote commit history confirms committed work only.
- No genealogy data, relationships, private files, or generated artifacts were changed in this migration.
- Repository default-branch configuration and deletion of the two legacy refs remain administrator-side actions outside the available connector capabilities.

### Next work
1. Continue the Broager/Dybbøl p53 collateral-family test using the parish index and original 1866 marriage register; do not infer p53's parents from the Jørgen Hansen secondary profile.
2. Continue rotating across the remaining open Ahnentafel branches, prioritising original register images over additional compiled trees.
3. Commit all further changes directly to `main` and verify each changed file from `main`.


## Milestone 45 — parallel Early Smol Web coordination (16 November 2026)

### Context
This run executed the shared "Early Smol Web & Tree research" schedule. Primary effort was allocated to the companion repository `sloev/earlysmolweb` (initialised `coop.log.md`, advanced Faroe Islands institutional web-publishing chronology with the 25 November 1997 public launch of Internet Sosialin / Sosialurin).

### Tree-repo actions
- Confirmed current protocol still requires sole use of `main`.
- No changes to `data/build_data.py`, any person records, private data, generated artefacts, or relationship claims.
- No new Ahnentafel research or parish-register transcription performed in this pass; the open Dybbøl/Broager p53 worklist remains the next concrete genealogical step.

### Validation
- Private data was not accessed or decrypted.
- No build or tests were run.

### Next concrete steps (unchanged)
1. Continue the Broager/Dybbøl p53 collateral-family test using the parish index and original 1866 marriage register.
2. Rotate across remaining open Ahnentafel branches, prioritising original register images.
3. Keep all further commits on `main` only.


## Milestone 46 — resume after main-only branch cleanup (16 November 2026)

### Repository state
- User confirmed deletion of the legacy refs after changing the default branch. A fresh GitHub audit now reports **only main** in sloev/tree; main is the default branch.
- Companion repository sloev/earlysmolweb also reports only main, with main as its default branch.
- All new writes in this run are made directly to main; no feature branches or pull requests are used.

### Dybbøl p53 source audit — important index distinction
- The working question remains whether p53 Anne Christine Hansen's stated parents, Hans Hansen and Ellen Kock, can be independently supported through collateral Dybbøl records. The secondary online profile for Jørgen Hansen (born 26 April 1827) is only a lead and must not be used as proof of p53's parentage.
- A fresh inspection of the Stroemming genealogy source index found the KMB 1861–1927 FVD, p. 169 / image 85 / no. 1 reference attached to Christen Hansen's family profile. My initial interpretation that this was a birth/baptism entry was wrong: the 1976 Sønderborg-probsti archival inventory states that Dybbøl Ab 4 (1861–1927) contains **marriages from 1861–1906**, so this volume's page 169 is in its marriage section. The index may be citing a marriage relevant to Christen's parentage; it is not the target 1866 Rasmus Jensen–Anne Christine Hansen marriage unless that is separately demonstrated.
- The exact 1866 marriage entry (reported date 18 September 1866) and its original page/image have **not** been located or transcribed in this pass. The archival inventory now establishes the exact target volume: **Dybbøl Ab 4, 1861–1927**, whose marriage section covers 1861–1906. The target page still needs to be identified in Arkivalieronline and read directly.
- The 1976 Landsarkivet inventory for the Sønderjyske Landsdele lists Dybbøl Ab 4 (1861–1927) and specifies that it contains marriages from 1861–1906. This is the precise archival series for the reported 1866 wedding. Rigsarkivet's current guide confirms that 1814–1960 parish registers are organized by event sections and available through Arkivalieronline. For southern Jutland, the later civil-register system begins in 1874; this 1866 marriage must be pursued in the parish register.

**Sources inspected:**
- Stroemming source index, Dybbøl KMB 1861–1927 FVD entries: https://www.stroemming.dk/genealogy/gedweb/Public/da/Lists/sources-K.html
- Jørgen Hansen secondary profile (collateral lead only): https://www.stroemming.dk/genealogy/gedweb/Public/da/Details/Details-I6346.html
- Rigsarkivet, “Kirkebøger – Kom godt i gang”: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/
- Landsarkivet for de Sønderjyske Landsdele, *Nordslesvigske præstearkiver V: Sønderborg provsti* (Åbenrå, 1976), Dybbøl Ab 4, pp. 13–15 / PDF text lines 769–773: https://slaegtsbibliotek.dk/2024/941454.pdf
- Rigsarkivet, Arkivalieronline church-book collection: https://arkivalieronline.rigsarkivet.dk/da/collection/theme/1

### Next work
1. Identify the exact Dybbøl 1866 marriage page/image for 18 September; inspect the original witnesses, residences, ages and fathers before drawing any relationship inference.
2. Search contemporary or primary collateral records for Hans Hansen and Ellen Kock independently of the Jørgen Hansen online tree.
3. Continue rotating through other open Ahnentafel branches if the Dybbøl original remains inaccessible; do not modify person relationships without direct evidence.
4. Keep all work on main; no private-data access, decryption, or build/test claims unless actually performed.


---

## Milestone 47 — 2026-11-16 — Dybbøl index access and Ove Samuel Gedde source conflict

**Agent:** ChatGPT (GPT-6)  
**Branch:** main only. The repository has no coop.log or CONTRIBUTING file; this append follows the existing milestone/handoff practice in research_method.md.

**Dybbøl p53 primary-source search:**
- Opened the official Arkivalieronline page for *Dybbøl Sogn: Register til Dybbøl kirkebog (1729–1900)*: https://arkivalieronline.rigsarkivet.dk/da/other/index-creator/29/725983/18484622. It lists separate index links for deaths, births and marriages; the marriage index is *Vielser 1723–1900*.
- The marriage-index link opens https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=18484622, but text retrieval of the image viewer timed out. No index image or target page was read, so the 18 September 1866 Rasmus Jensen–Anne Christine Hansen entry remains unlocated.
- Searched the public Strømming indexes for the exact names and Dybbøl source: https://www.stroemming.dk/genealogy/gedweb/Public/da/Lists/allnames-R.html, https://www.stroemming.dk/genealogy/gedweb/Public/da/Lists/allnames-A.html, https://www.stroemming.dk/genealogy/gedweb/Public/da/Lists/sources-K.html and https://www.stroemming.dk/genealogy/gedweb/Public/da/Lists/placename-D.html. No exact target marriage entry or page reference was identified. The already-known p. 169 / image 85 / no. 1 reference is a different 1864 marriage and must not be reused. These negative index searches do not prove the target entry is absent from the church book.

**Additional Gedde lead (p216 Ove Samuel):**
- The current project data stores Ove Samuel Gedde's birth as 1778-02-28 and links him to Hans Christopher Gedde and Øllegaard Sophie Fischer.
- Carl Johan Anker's 1885 *Biografiske data om 330 norske, norskfødte eller for nogen tid i den norske armé ansatte generalspersoner, 1628–1885*, p. 94, has unproofread OCR listing Ove Samuel as 28 May 1788; the same entry says Hans Christopher's first wife Frederikke Christiane Fischer died in 1787 and his second marriage to Ødegaard Sophie Fischer was on 15 December 1789: https://runeberg.org/acj330bio/0110.html.
- This is a secondary, unproofread OCR lead, not proof. It conflicts with the project's stored date and raises a question about the maternal attribution. Do not change the birth date or parent links until the original baptism and relevant family records are found.

**Files changed:** research_method.md only (this appended milestone). No family-tree, build-data or source-record edits. No private.enc, private stubs or private plaintext were accessed or modified; no living-person data was added.

**Status:** p53 remains open; no speculative relationship or date changes. Ove Samuel's birth date and mother remain unresolved pending primary evidence.

**Next handoff:** Retry the official Arkivalieronline marriage index visually and identify the actual KMB 1861–1927 FVD entry for 18 September 1866. If the viewer remains inaccessible, rotate to Ove Samuel's original baptism: first establish the likely parish from contemporary records, then verify the exact date and mother. Do not infer p53's parents from secondary collateral profiles.
