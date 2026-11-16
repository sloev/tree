# Repository research method

## Operating protocol
- Work on branch `ccr-6abdfb67-cbzklo`; do not silently switch branches or merge changes.
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
- Branch: `ccr-6abdfb67-cbzklo`.

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
- `site/unlock.js` lines 1–60: password storage, PBKDF2/AES-GCM decrypt, placeholder merge, unlock and lock lifecycle.
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
- `tools/`: Link Lives client, query/matching helpers, ancestor expansion, sibling discovery, and manual-add helper.
- `site/`: source template, site builder, unlock script, poster template, generated poster page, and PDF driver.
- `docs/`: GitHub Pages output, poster output, four PDF posters, and `.nojekyll`.
- `images/`: ten source images.
No test directory, dependency manifest, or GitHub Actions workflow appears anywhere in this complete tracked tree. This is a statement about tracked files on this branch, not about external CI configuration.
### Public snapshot integrity checks
Checks were performed on the public `data/family.json` snapshot only. The encrypted `private_blob` was excluded from content scans; private records were not enumerated or decrypted.
- 387 non-private people in the current snapshot.
- No duplicate public person IDs or duplicate public Ahnentafel numbers.
- No dangling `father`, `mother`, or `spouse` references among public people.
- 286 public people have at least one explicit father/mother link.
- 327 public birth values and 149 public death values are populated.
- Four non-ISO death strings were found: `efter 1922`, `1885–1892`, `efter 1811`, and `efter 1730`. All four are intentionally supported by `data/export.py:gdate()` as AFT or BET expressions; they are not malformed dates.
- No impossible calendar dates or invalid numeric months were found in ISO day/month values.
- No public string containing a literal closing `</script>` tag was found in the data fields embedded by `site/build.py`.
### Confirmed code-path defect sharpened
The compacting defect in `tools/expand.py` is confirmed by direct source tracing:
- Both the marriage-patch path and the ancestor-creation path store `_parents` as a list comprehension over `(father, mother)` with missing entries filtered out.
- The later expansion loop interprets list index 0 as father/Ahnentafel even slot and index 1 as mother/odd slot.
- Therefore, whenever the father is absent and the mother is present, the remaining mother record is deterministically misassigned to the father slot. This is not merely a theoretical indexing concern; the data model has no way to retain the omitted role once the list is compacted.
- Current `auto_ancestors.json` has eight entries with `_parents`: four empty, two one-element, and two two-element arrays. The two one-element entries require checking against their original Link Lives marriage records before concluding whether either is a shifted mother; the stored sidecar alone does not preserve that role information.
### Export and website generation observations
- `data/export.py:gdate()` supports exact dates, month precision, year precision, approximate years, after-dates, and year ranges. Numeric month/day validation is absent in code, although no invalid calendar dates were detected in the current public snapshot.
- `site/build.py` injects JSON strings directly into inline script content via `str.replace`. The current public data scan found no literal closing script tag, but the generator has no explicit script-context escaping. A future hardening change should serialize inline data safely (at minimum escape `<` as a Unicode escape in JSON payloads) and add a regression fixture containing `</script>` in a public text field.
- The tracked generated site and docs HTML differ slightly in size because docs output is wrapped as a standalone document; this is expected from the builder's separate wrapper logic. No build was run to verify byte-for-byte regeneration.
### Validation status
- Complete tracked-tree inventory and aggregate/public-data structural checks completed via GitHub source reads.
- No code or data files changed in this milestone; only this research checkpoint is updated.
- No local shell/runtime is available through the current repository connection, so Python build, GEDCOM export, browser tests, PDF generation, and regression tests remain unrun.
- No external Link Lives query was made; no encrypted or decrypted private data was accessed.
### Next steps
1. Inspect `tools/addman.py` and all remaining small utility code; finish call-graph and sidecar schema review.
2. Design an isolated, non-secret regression fixture for father-only, mother-only, and both-parent marriage cases; extract a pure role-preserving helper if the tests can be added without changing generated genealogy output.
3. Review `site/build.py` inline JSON serialization and implement script-context escaping with a minimal fixture.
4. Reconcile the four supported non-ISO dates and GEDCOM export behavior; add validation for impossible month/day values.
5. Update this checkpoint before any code edits and explicitly state that runtime validation is unavailable unless an execution route becomes available.


### Remaining utility review
- `tools/addman.py` was inspected. `add()` replaces an entry by Ahnentafel number and patch flag, then appends a normalized record; `sib()` replaces all sibling rows for a given `_for` person and expands the supplied rows with shared parent/source metadata.
- Minor API footgun: `sib()` calls `extra.pop("src", [])`, mutating each caller-supplied `extra` dictionary. This is surprising for a helper API and can affect a caller that reuses those dictionaries. A safer implementation would copy the dictionary or use `extra.get("src", [])`; low priority unless callers reuse row metadata.
- The script-context concern is supported by OWASP's current XSS prevention guidance: JSON.stringify output is not itself an HTML/script-context encoder, and a literal `</script>` can terminate an inline script before the JavaScript parser processes the quoted JSON. The current data scan was clean, but the generator should encode for the actual HTML script context or move JSON into a non-executable data block / external JSON resource. Reference: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html


## Milestone 5 — genealogical expansion strategy and Ahnentafel gap map
### Scope and safeguards
- Re-read this method file before continuing. Continued on branch `ccr-6abdfb67-cbzklo`.
- Shifted the immediate research objective from technical review to systematic ancestral expansion, per the user's stated goal of maximum depth and full coverage.
- Only the public portion of `data/family.json` was parsed. The `private_blob` field was not read or emitted; no private records were enumerated or decrypted.
- No source-data or application code was changed in this milestone.

### Current public Ahnentafel coverage
- The public snapshot contains 387 non-private people with Ahnentafel numbers.
- Ahnentafel slots 2–16 are fully occupied; generation 5 (32–63) has 31 of 32 slots, with slot 35 absent.
- Generation 6 (64–127) has 50 of 64 slots; 14 slots are absent: 64, 65, 68, 69, 70, 71, 81, 83, 84, 85, 92, 93, 122, 123.
- Generation 7 (128–255) currently has 15 people; generation 8 (256–511) has 9; generation 9 (512–1023) has 9; generation 10 (1024–2047) has 4; generations 11–13 have respectively 4, 2, and 2 people.
- Many people in generations 6–9 are already named but lack one or both parent links. This is an opportunity to recover parents from baptism, marriage, census, probate, and land records before searching blindly for additional names.
- Highest-priority named frontier candidates include:
  - Ahnentafel 32 Niels Jørgensen and 34 Niels Larsen (generation 5; both parents unknown).
  - 40 Jens Pedersen and 41 Kirsten Marie Nielsen (one parent each still unknown).
  - 42 Peder Jensen and 46 Jens Peder Larsen (both parents unknown).
  - 61 Karen Nielsen (both parents unknown).
  - 66 Hans Jensen (c.1752) and 67 Margaretha Pedersdatter (c.1797), parents unknown.
  - 72 Claus Gaardsted (c.1750) and 73 Kirsten Marie Jørgensdatter, parents unknown.
  - 74 Jens Hansen and 75 Mette Pedersdatter (one parent of 75 is already known as Peder Hallis; remaining parent unresolved).
  - Additional branches in the Langeland, Vester Starup, Fåborg, Hoven, Sønder Felding, Broager/Nybøl, Gedde/von Kleist, and Langø families.
- Existing reject markers in `data/auto_ancestors.json` are deliberate safeguards against wrong-parish/false matches. Do not reactivate them without new primary-source evidence.

### Source-coverage research
- Rigsarkivet states that Link-Lives exposes transcribed Danish parish records roughly 1814–1917 and census datasets for 1787, 1801, 1834, 1840, 1845, 1850, 1860, 1880, 1885 (Copenhagen only), and 1901; Link-Lives also provides proposed cross-record life-course links. Cite: https://link-lives.dk/data-og-kilder-i-link-lives/ and https://link-lives.dk/soegevejledning/
- Link-Lives search visibility is restricted for people born after 1904, and the source descriptions warn that the transcribed record is not a substitute for the original archival image. Cite: https://link-lives.dk/data-og-kilder-i-link-lives/
- Rigsarkivet's 2026 migration guidance says the Danish Demographic Database is moving to “Søg i Samlingerne”; datasets remain preserved but are being migrated, so availability and search behavior may change. Cite: https://www.rigsarkivet.dk/vejledning/fra-dansk-demografisk-database-til-soeg-i-samlingerne/
- A specialist regional index, Djurslandsdatabasen, independently lists Claus Gaardsted as born 1751 and deceased 1811 at Bogensholm, and lists Joachim/Jochum Gaardsted as born 1792 at Vosnæsgård. This is a promising regional lead for the Gaardsted line, not proof of Claus's parents or of every identity link. Cite: https://djursslaegt.djursdatabasen.dk/efternavne/EFTERNAVNG.htm
- Trap Danmark corroborates that Claus Gaardsted bought Bogensholm in 1796 and died in 1811. The 1803 royal memorandum confirms him as owner of Bogensholm. These establish context, not parentage. Cite: https://netstol.dk/slaegtsForskning/trap_danmark_4/Trap_Danmark_4_udgave_%281925%29_Bind_6_Randers_Amt_Mols_og_OEster-Lisbjaerg_Herreder.pdf and https://da.wikisource.org/wiki/Side:Kongelige_Rescripter,_Resolutioner_og_Collegialbreve_for_Danmark_og_Norge_udtogsvis_udgivne_i_chronologisk_Orden._VI._Deel._12._Bind_(1803%E2%80%931804).pdf/258

### Research discipline and next actions
1. Build a prioritized worklist from the current public Ahnentafel frontier. Track each open father/mother slot separately; distinguish “named but parents unknown” from “slot entirely empty.”
2. For each person, extract the existing source IDs and search the original birth/baptism, marriage, confirmation, death/burial, census, probate, and land records. Use Link-Lives life-course suggestions only as candidate navigation; verify relationships against original images.
3. For people born before the indexed parish-register coverage (especially pre-1814), identify the relevant parish, neighboring parishes, estate, and archive series. Do not assume Link-Lives has those baptisms.
4. Start with high-yield branches where there are already exact source keys or precise parish/year anchors: the Gaardsted/Vosnæsgård line; Jens Peder Larsen/Assing; Hans Jensen/Margaretha Pedersdatter/Syv; and the generation-5 Langeland branches.
5. Record every search, including negative searches, to avoid repeated work. Add a new person only when identity is supported; retain uncertainty and rejected alternatives in notes.
6. Continue the technical parent-role regression finding separately; do not let automated expansion write unreviewed relationships into the canonical tree.
7. The GitHub connector can inspect and update repository files but cannot execute the Python Link-Lives client or local build pipeline in this session. Web searches have been used for contextual leads only; no live Link-Lives API query was performed in this milestone.


## Milestone 6 — Gaardsted collateral-family evidence and estate archive lead
### New evidence found
- The public family snapshot identifies Ahnentafel 72 Claus Gaardsted (ca. 1750–1811), estate owner at Bogensholm, and Ahnentafel 73 Kirsten Marie Jørgensdatter (ca. 1752), his second wife. Neither has parent links. Existing source keys on Claus are `LL:0-414804`, `LL:1-475533`, and an Arkivalieronline citation to Skødstrup church book 1780–1809 p.75; Kirsten has `LL:0-414805` and `LL:1-475272`.
- A digitized abstract/index of Rolsøgård estate probate records (Mols Herred, 1778–1816) includes entry 11: Niels Jensen Degn of Vrinners, probate dated 14 May 1787, folio 39. The abstract says an inheritance in the estate of Niels's stepchildren from Christen Christensen Tohde (probate 1764) went to daughter Karen Christensdatter, and names “broder Claus Gaardsted forpagter på Vosnæsgård” as her guardian. This is a valuable collateral relationship: it appears to identify a Claus Gaardsted as Karen Christensdatter's brother, and confirms his occupation/location at Vosnæsgård in 1787. It does NOT yet prove that this Claus is identical to Ahnentafel 72, though the matching rare name and known Vosnæsgård association make that a strong candidate. It does not identify their parents.
- Source: Danske Slægtsforskere, “Alfabetisk navneliste og skifteuddrag til Rolsøgård gods (G302), Mols Herred 1778–1816 (1818),” especially lines/entry 11. Online PDF: https://slaegt.dk/media/jnnnvuml/alfabetisk-navneliste-og-skifteuddrag-til-rols%C3%B8g%C3%A5rd-gods-g302-mols-herred-1778-1816-1818.pdf
- The abstract explains that it lists deceased persons, heirs, guardians, and other stated family relationships; names/places have been standardized, and the transcript is not proof-text. Original probate folio 39 should be consulted.
- Trap 5 (Vistoft parish) independently says Claus Gaardsted bought Bogensholm in 1796 for 10,000 rigsdaler, died 1811, and his widow sold the estate at auction in 1811. This differs slightly from the older Trap 4 entry, which gives 1797; preserve the year discrepancy as 1796/97 until the deed is checked. Source: https://trap5.lex.dk/sogn/vistoft-sogn-mols-herred/
- The 1803 royal rescript explicitly calls Claus Gaardsted owner and resident of Bogensholm, corroborating identity and estate ownership: https://da.wikisource.org/wiki/Side:Kongelige_Rescripter,_Resolutioner_og_Collegialbreve_for_Danmark_og_Norge_udtogsvis_udgivne_i_chronologisk_Orden._VI._Deel._12._Bind_(1803%E2%80%931804).pdf/258
- The Bogensholm estate archive has a probate register and name register for 1800–1811, plus published extracts. This is the first-choice source for Claus's own probate, likely to list his widow and heirs; archive description: https://wiki.slaegt.dk/index.php/Bogensholm
- Djurslandsdatabasen lists Claus (1751–1811, Bogensholm) and later Gaardsted descendants including Joachim (1792, Vosnæsgård), Ernst Adolph (1785, Vosnæsgård), and Poul Christian (1789, Vosnæsgård). These may represent children/descendants of the Vosnæsgård household, but the surname index alone does not establish parent-child links. Source: https://djursslaegt.djursdatabasen.dk/efternavne/EFTERNAVNG.htm
### Interpretation and next research steps
1. Retrieve and read the original Rolsøgård probate folio 39 (1787) to establish the precise wording and whether Karen Christensdatter is explicitly Claus's sister; then identify Karen through her own marriage/death/baptism records. Her baptism may identify shared parents.
2. Retrieve the original Bogensholm probate of Claus Gaardsted (1811) and the register index. Extract every named heir, guardian, creditor, and family relationship. Determine whether his widow is Ahnentafel 73 and identify any children, including any link to the later Vosnæsgård Gaardsteds.
3. Search Skødstrup parish records around 1745–1760 for Claus and possible siblings; search adjacent parishes and estate records if no baptism appears. The surname may be locative and need not be hereditary in the modern sense.
4. Search the Vosnæsgård estate records, fæsteprotokoller, and probate/guardianship records for the 1787 tenant/factor appointment and prior family ties.
5. Do not add Karen, Claus's parents, or the later Gaardsted individuals to the tree until the original records or multiple corroborating sources establish the relationships.
### Coverage-number correction
The previous milestone's generation labels were offset by one, because the script used floor(log2(Ahnentafel number)) while calling that result “generation.” Corrected conventional ranges: 2–3 = generation 1 (2/2); 4–7 = generation 2 (4/4); 8–15 = generation 3 (8/8); 16–31 = generation 4 (16/16); 32–63 = generation 5 (31/32); 64–127 = generation 6 (50/64); 128–255 = generation 7 (15/128); 256–511 = generation 8 (9/256); 512–1023 = generation 9 (9/512); 1024–2047 = generation 10 (4/1024); 2048–4095 = generation 11 (4/2048); 4096–8191 = generation 12 (2/4096); 8192–16383 = generation 13 (2/8192). The counts themselves are unchanged; only the descriptive generation numbers are corrected.
### Validation
- Re-read `research_method.md` first and continued on the required branch.
- Inspected only public `data/family.json` records for Ahnentafel 72, 73, 150, 152, 153, and 304. No private records or encrypted data were read.
- Web research located the Rolsøgård probate abstract, Trap Vistoft entry, 1803 rescript, Djurslandsdatabasen name index, and Bogensholm archive description.
- No original archival image has yet been read; no family relationships or tree data were changed. No Link-Lives API query, local build, or tests were run.
### Next phase
Phase 5 continues: prioritize original probate records for the Gaardsted branch, beginning with Rolsøgård folio 39 (1787) and Bogensholm 1800–1811 register/probate. Then trace named heirs/siblings into Skødstrup/Vistoft parish registers.

## Milestone 7 — archival jurisdiction refined for the Gaardsted probate search
### New archival findings
- Re-read this method file first and continued on branch `ccr-6abdfb67-cbzklo`.
- Located the Rigsarkivet Arkivalieronline scans for Bogensholm Gods' 1800–1811 probate book and its register through the Danish Genealogical Society's DS-Wiki page. The viewer is linked from that page; the web text viewer itself returned an access error, so no original folio has yet been inspected. Direct entry points: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17175801 (book) and https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17175795 (register).
- Read Hanne Vinter Henriksen's published Bogensholm probate extracts (G298, 1800–1811). It explicitly describes the list as eight estate cases (Dorthe Pedersdatter 1800 through Peder Andersen Tuesen 1811), with deceased, heirs, guardians and family relationships. Claus Gaardsted is not among these eight. This is a negative result for this particular published extract, not proof that no probate was held for him. Source: https://www.milloup.dk/hvh/download/skifter/bogensholm_gods_skifter.htm
- Rigsarkivet's current guide explains the jurisdictional distinction: before 1793, non-tenant rural landowners' estates were handled by the county; 1793–1851, by the herredsfoged or birk. Since Claus was the owner of Bogensholm and died in 1811, the next target is therefore the relevant Mols Herredsfoged probate series/register, not just the Bogensholm Gods tenant-probate book. Confirm whether any special private/estate-owner arrangement applies. Source: https://www.rigsarkivet.dk/vejledning/skifter-og-testamenter/skiftearkivalier-kom-godt-i-gang/
- The DS-Wiki Bogensholm entry links both the 1800–1811 probate book and its name register. The Rolsøgård entry similarly links its 1778–1816 book and register. Sources: https://wiki.slaegt.dk/index.php/Bogensholm and https://wiki.slaegt.dk/index.php/Rols%C3%B8g%C3%A5rd
- Re-read the published Rolsøgård extract at entry 11: 14 May 1787, folio 39. It describes inheritance to a daughter Karen Christensdatter in connection with the estate of Christen Christensen Tohde? (probate 1764), then names “broder Claus Gaardsted forpagter på Vosnæsgård” as her guardian. This supports the existing provisional sibling record p74 in `data/build_data.py`, but the original folio remains necessary to verify the exact grammatical relationships and identity. The transcription itself warns it is not proof-text and is not proofread. Source: https://www.milloup.dk/hvh/download/skifter/rolsoegaard_gods_skifter.htm
- Rigsarkivet's guidance says probate records can identify heirs and family relationships, and that the correct jurisdiction depends on residence and legal status/occupation before 1851. Source: https://www.rigsarkivet.dk/vejledning/skifter-og-testamenter/skiftearkivalier-kom-godt-i-gang/
### Revised next actions
1. Search the Mols Herredsfoged skifteprotokol and name register covering 1811 for Claus Gaardsted, Bogensholm; inspect the original entry and all related probate documents.
2. Use the Bogensholm register/book as a collateral source for people who were tenants or employees, not as the presumed location of Claus's own landowner probate.
3. Inspect original Rolsøgård G302 folio 39 (14 May 1787) to verify Karen Christensdatter's precise relationship to Claus and the stepchild/inheritance context.
4. Trace Karen in parish registers and any later probate only after the original 1787 wording is settled.
5. Do not change the tree: no original probate images have yet been read, and no new parentage has been established.
### Validation
- Read only public source material and public repository files. No private or encrypted data was accessed.
- The Arkivalieronline page metadata and archive-series links were identified, but the image viewer was not readable through the current web text interface. No claim is made that the original folios were examined.
- No local code execution, Link-Lives API query, build, or tests were run. No genealogy source data was changed.


## Milestone 8 — exact Mols probate series located
### Stronger archival route identified
- Continued the Gaardsted probate search using Rigsarkivet's Daisy catalogue for the archive creator Djurs Sønder og Mols Herred (official name Djurs Sønder-Mols Herredsfoged, 1687–1919).
- The catalogue explicitly lists the combined **Skifteprotokol, Sønder Djurs og Mols Herred, 1794–1824**. This is the correct core protocol series for Claus's 1811 death under the post-1793 jurisdictional rules. The same catalogue lists **Skiftedesignationer og dødsanmeldelser, 1795–1851**, **Sager til skifteprotokol I, 1794–1887**, and **Korrespondance m.m. vedr. skifte og overformynderi, 1795–1871**. These are now prioritized in that order as the register/designation and supporting-document routes. Daisy archive-series catalogue: https://daisy.rigsarkivet.dk/arkivskabers_arkivserier?a=&b=&c=Djurs+S%C3%B8nde+herred&d=1&dir=&e=2022&ed=&ep=&epid=&es=&f=&faid=&g=&gsc=&h=&heid=&henid=&int=&m2rid=&meid=&ngid=522700&ngnid=2969153&side=&sort=
- The same catalogue also lists **Overformynderiprotokol, 1796–1868**, **Dokumenter vedrørende værgemål, 1806–1845**, and **Indberetninger om godsernes skifte og overformynderi, 1799–1850**. These could preserve the administration of minor heirs or guardians after Claus's death; they are secondary follow-up series if the main probate identifies underage children. The catalogue also contains **Arveafkald, 1787–1867**, potentially useful for heirs renouncing claims.
- The broad Daisy list separately identifies the 1795–1851 series “Skiftedesignationer og dødsanmeldelser” for Djurs Sønder-Mols Herredsfoged. It is not a name-index book by title, but is the best first scan to check around 1811 for the death/probate designation. Source: https://daisy.rigsarkivet.dk/arkivserie_liste?a=&b=d%C3%B8dsan&c=&d=1&dir=a&e=2016&ed=&ep=&epid=&es=&f=&faid=&g=&gsc=&h=&heid=&henid=&int=&m2rid=&meid=&ngid=&ngnid=&side=1&sort=1
- Arkivalieronline's published collection for guardianship lists Djurs Sønder-Mols Herredsfoged series including “Korrespondance m.m. vedr. skifte og overformynderi” 1795–1871 and “Overformynderiprotokol” 1796–1868. Source: https://arkivalieronline.rigsarkivet.dk/da/other/other-collection/69
### Revised action sequence
1. Locate and inspect the 1795–1851 Skiftedesignationer og dødsanmeldelser around 1811 for Claus Gaardsted/Bogensholm; extract the reference into the 1794–1824 joint Mols/Djurs probate protocol.
2. Inspect the original joint probate protocol entry and the corresponding case documents in Sager til skifteprotokol I (1794–1887).
3. If the probate reveals minor heirs or guardians, inspect the Overformynderiprotokol and guardianship documents/correspondence for the names of children, widow, and maternal/paternal relatives.
4. Independently inspect Rolsøgård G302 folio 39 (14 May 1787) to settle the exact Karen Christensdatter/Claus sibling wording.
5. Do not add any parents or children to the tree until original record wording supports the relationship.
### Validation
- Daisy catalogue descriptions and Rigsarkivet collection listings were read; no original image folios from these Mols probate series have yet been inspected.
- No private or encrypted data was accessed; no genealogical source data or application code was modified; no local build/tests were run.


## Milestone 9 — probate name register and jurisdiction correction
### New decisive catalogue detail
- Rechecked the full Daisy series list rather than relying on search snippets. It explicitly lists a **Navneregister til skifteprotokol, 1794–1917** for Djurs Sønder-Mols Herredsfoged. This is the first archive item to inspect for Claus Gaardsted's 1811 probate, ahead of manually scanning the chronological protocol. Daisy series list: https://daisy.rigsarkivet.dk/arkivskabers_arkivserier?a=&b=&c=Djurs+S%C3%B8nde+herred&d=1&dir=&e=2022&ed=&ep=&epid=&es=&f=&faid=&g=&gsc=&h=&heid=&henid=&int=&m2rid=&meid=&ngid=522700&ngnid=2969153&side=&sort= (lines 180–181).
- The same catalogue confirms the 1794–1824 **Skifteprotokol, Sønder Djurs og Mols Herred**, the 1794–1887 **Sager til skifteprotokol I**, the 1795–1851 **Skiftedesignationer og dødsanmeldelser**, and the 1795–1871 **Korrespondance m.m. vedr. skifte og overformynderi**.
- Rigsarkivet's current guide gives the exact legal rule: from 1793–1851, probate for rural non-tenants (godsejere, selvejere and other landboere uden fæstestatus) was handled by the herredsfoged or birk. It separately says estate owners handled the probate of their own tenants/employees. Therefore Claus's own probate as Bogensholm owner belongs in the herredsfoged/birk route if he was not himself a tenant; the Bogensholm estate probate register is not the presumed place for his own probate. The guide also notes private probate as a distinct route and directs researchers to county archives for executor/commission/private cases. Source: https://www.rigsarkivet.dk/vejledning/skifter-og-testamenter/skiftearkivalier-kom-godt-i-gang/ (sections on godsejere/selvejere, godsets fæstere/ansatte, and private skifter).
- This clarifies and sharpens Milestone 8: the 1794–1917 name register is the best first step, while the 1795–1851 designations/death notifications are a parallel cross-check. The register's existence is now confirmed from Daisy, but its original image sequence and exact Arkivalieronline viewer URL have not yet been resolved.
### Research order now
1. Open the 1794–1917 Navneregister til skifteprotokol in Arkivalieronline (via Søg i samlingerne/Daisy) and search the 1811 register section under Gaardsted/Claus; check spelling variants and the index's alphabetic structure.
2. Follow the referenced page into the 1794–1824 Skifteprotokol, Sønder Djurs og Mols Herred, and inspect the original probate.
3. Check Sager til skifteprotokol I (1794–1887) for supporting documents; use the 1795–1851 Skiftedesignationer og dødsanmeldelser as parallel corroboration.
4. If no entry is found, assess private probate/eksekutorbo possibilities in Randers Amt and estate-specific papers, rather than interpreting a negative index result as proof no probate exists.
5. If minor heirs appear, inspect Overformynderiprotokol (1796–1868), Dokumenter vedrørende værgemål (1806–1845), and Korrespondance m.m. vedr. skifte og overformynderi (1795–1871).
6. Continue to inspect Rolsøgård G302 original folio 39 (14 May 1787) for the exact wording of Claus's reported sister Karen Christensdatter.
### Validation and correction
- The earlier Milestone 8 phrase “the best first scan” for Skiftedesignationer is superseded: the newly verified 1794–1917 name register is the first-choice index.
- No original image from the name register, probate protocol, or Rolsøgård folio has yet been read. No relationships or source data were changed.
- Only public repository metadata and public archival guidance were accessed. No private/encrypted data was accessed. No local code, build, or tests were run.


## Milestone 10 — direct Arkivalieronline entry points recovered
### Rolsøgård originals
- The DS-Wiki Rolsøgård page exposes the original Rigsarkivet Arkivalieronline endpoints directly:
  - Probate protocol 1778–1816: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17177605
  - Name register 1778–1816: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17177607
  - DS-Wiki source: https://wiki.slaegt.dk/index.php/Rols%C3%B8g%C3%A5rd (links labelled AO 1778–1816 and Register 1778–1816).
- The web text browser cannot render the Arkivalieronline viewer (redirect returns HTTP 500), so no image pages have been read. These URLs are nonetheless exact, verified entry points for opening the source manually or in a compatible image viewer. The published transcription remains a finding aid only.
### Mols index accessibility
- Daisy confirms a Mols/Sønder Djurs name register to probate protocol for 1794–1917, but the Arkivalieronline collection “Skiftevæsen - Registre og hjælpemidler” does not list this register in its current online collection. Treat the register as an archival series described in Daisy, not yet confirmed as digitized. It may require retrieval through “Søg i samlingerne” or a reading-room request.
- The Daisy catalogue also confirms the main Mols/Sønder Djurs probate protocol 1794–1824 and the case papers 1794–1887.
### Next actions
1. Open the exact Rolsøgård protocol and register URLs above in a browser capable of Arkivalieronline image rendering; locate 14 May 1787 folio 39 in the protocol and read the full entry.
2. In Daisy/Søg i samlingerne, determine whether the Mols name register (1794–1917) is digitized or must be ordered to the reading room. If available, search Claus Gaardsted in the 1811 section; if not, request the register and the 1794–1824 protocol/case papers.
3. Continue the Mols probate search with the exact archive series and jurisdictional classification from Milestone 9.
4. No tree data or source records changed; no family relationships were newly established.
### Validation
- DS-Wiki page and its exact AO links were inspected; AO redirects were attempted but image rendering failed in the web text interface.
- Daisy series list and Arkivalieronline's digitized-register collection were compared. No original archival images have been inspected.
- Only public sources and public repository files were accessed. No private or encrypted data, local build, or tests were used.


## Milestone 11 — partial register digitization and jurisdiction-transfer lead
- Arkivalieronline has a live viewer for Djurs Sønder-Mols Herredsfoged, Navneregister til skifteprotokol, 1841–1855: https://arkivalieronline.rigsarkivet.dk/da/billedviser?bsid=122086. This confirms partial digitization of the 1794–1917 Daisy register series, but does not prove the earlier 1811 section is online.
- Daisy also lists Dokumenter vedrørende Roelsøgårds afgivelse af skiftejurisdiktion, 1803–1820, under Djurs Sønder-Mols Herredsfoged. This is a new priority: inspect the original papers to determine the date and scope of Rolsøgård's transfer/surrender of probate jurisdiction. The catalogue title alone does not establish its legal effect.
- Daisy continues to list the joint Sønder Djurs and Mols probate protocol 1794–1824, case papers 1794–1887, and designations/death notifications 1795–1851. These remain the likely route for Claus's 1811 probate if he fell under herredsfoged jurisdiction.
- Next: inspect the 1803–1820 jurisdiction-transfer papers; seek the earlier Mols name-register volume; then follow the appropriate register reference into the main probate protocol. Keep the 1787 Rolsøgård folio 39 separate until its original wording is read.
- Validation: re-read this file first; continued on ccr-6abdfb67-cbzklo. Read public catalogue metadata only; no original image text, private data, or encrypted data accessed. No tree/source data changed; no local build or tests run.


## Milestone 12 — restore balanced whole-tree research scope
- User explicitly clarified that the objective is Vivi's complete family tree, not a Gaardsted-only investigation. Gaardsted is one open lead among many and must not monopolize research time.
- Adopt a branch-balanced work queue: maintain a separate record for each open Ahnentafel father/mother slot; rank by (a) strongest source anchor, (b) realistic chance of extending ancestry, (c) generation depth and impact, and (d) diversity across unrelated branches. Do not spend consecutive research milestones exclusively on one surname/estate unless a primary-source discovery justifies a short focused sequence.
- Revisit the full public Ahnentafel frontier from Milestone 5/6: Niels Jørgensen (32), Niels Larsen (34), Jens Pedersen (40), Kirsten Marie Nielsen (41), Peder Jensen (42), Jens Peder Larsen (46), Karen Nielsen (61), Hans Jensen (66), Margaretha Pedersdatter (67), Claus Gaardsted (72), Kirsten Marie Jørgensdatter (73), Jens Hansen (74), Mette Pedersdatter (75), and the remaining gaps/branches in Langeland, Vester Starup, Fåborg, Hoven, Sønder Felding, Broager/Nybøl, Gedde/von Kleist, and Langø.
- New non-Gaardsted archival lead: Arkivalieronline's national church-register collection states that a new colour digitization of pre-1814 parish registers is underway and scheduled for completion in 2026. This may improve access for all pre-1814 branches; verify each parish's current availability rather than assuming completion. Source: https://arkivalieronline.rigsarkivet.dk/en/geo/geo-collection/5.
- Particularly promising branch-wide tools include the online register to Broager parish registers (1695–1895) and the Nybøl parish-register index (1642–1829), both listed in Arkivalieronline's registers/help aids collection. These are relevant to the existing Broager/Nybøl line and offer a concrete next step outside Gaardsted. Source: https://arkivalieronline.rigsarkivet.dk/da/other/other-collection/29.
- The Danish Genealogical Society's online probate-links collection lists multiple Langeland probate registers/series (including Langeland 1683–1850 name register, Langeland Herred 1802–1865 name register, and Langeland county/estate-related probate material). This is a strong route for the Langeland branch, but exact jurisdiction must be matched to each ancestor's parish and legal status. Source: https://slaegt.dk/kilder/hvor-finder-du/online-kilder-sub/linksamling-skifter/.
- Next run should leave Gaardsted temporarily and select one or more of the Broager/Nybøl and Langeland frontier slots; inspect their exact public source keys and parish/date anchors in `data/build_data.py`, `data/family_docs.json`, and public `data/family.json` only. Do not access private ciphertext or decrypted private data.
- Validation: re-read this method file first; continued on `ccr-6abdfb67-cbzklo`. Public web catalogues only. No original records read and no genealogy data changed.


## Milestone 13 — Broager/Nybøl collateral lead (non-Gaardsted branch)
### Exact parish-register indexes located
- Arkivalieronline lists a **Register til Broager kirkebog (1695–1895)**. Its index categories include births/deaths/marriages for women through 1874 and marriages for men through 1895. Exact index landing page: https://arkivalieronline.rigsarkivet.dk/da/other/index-creator/29/16417788/18484676; image viewer endpoint exposed by the category links: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=18484676.
- Arkivalieronline also lists a **Register til Nybøl kirkebog (1642–1829)** with deaths, births and marriages. Exact landing page: https://arkivalieronline.rigsarkivet.dk/da/other/index-creator/29/16417788/18484666; viewer endpoint: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=18484666.
- The text browser can read the index landing-page metadata but not the scanned image viewer. These are verified archival entry points, not evidence that any particular index entry has been read.
### Candidate collateral relationship to test
- Public tree person p53 is Anne Christine Hansen (Ahnentafel 53), wife of Rasmus Jensen (p52), married 18 Sep 1866 in Dybbøl. Her stated parents are Hans Hansen (p106) and Ellen Kock (p107), supported in the existing data by the marriage-index source `LL:13-4977282` and associated LL keys for the parents. Her own birth date/place are currently unknown.
- An independently published online genealogy page for **Jørgen Hansen**, born 26 Apr 1827 in Dybbøl, names parents Hans Hansen (born 1798) and Ellen Kock (born 1799), and cites Dybbøl parish register 1810–1853, p.95, no.10, image 50. It gives no documentary source for the parents' birth years and is a secondary online tree, so it is only a collateral lead. Source: https://www.stroemming.dk/genealogy/gedweb/Public/da/Details/Details-I6346.html.
- A separate local-history PDF also names a Marie Magdalene Hansen as daughter of the Dybbøl cottager Hans Hansen and Ellen Kock, but does not establish that she or Jørgen is a sibling of Ahnentafel 53. Source: https://slaegtsbibliotek.dk/2023/929725.pdf.
- Hypothesis to test, **not established**: p106/p107 might be the same Hans Hansen and Ellen Kock who were parents of Jørgen Hansen (1827) and possibly other Dybbøl children. Do not merge people or add sibling links without Anne Christine's baptism/marriage entry or another primary record confirming the same couple.
### Next research actions
1. Use the Broager index and Nybøl index to identify relevant birth/marriage entries for Hans Hansen and Ellen Kock and any children; verify the relevant parish is Dybbøl, Broager, or Nybøl rather than assuming the index coverage follows modern place labels.
2. Inspect the original Dybbøl 1827 baptism (p.95, no.10) to verify Jørgen's parents and residence, then search the same couple's children in Dybbøl/Broager/Nybøl registers.
3. Locate Anne Christine Hansen's own baptism, then compare the parents' names, residence, occupation and witnesses against the 1827 Jørgen record. Only then decide whether this is a sibling/collateral link.
4. After this bounded test, rotate to another independent frontier (e.g. Langeland p114/p115, p118/p119, or the Syv/Starup/Fåborg/Hoven lines) rather than allowing the Sønderjylland line to monopolize the queue.
### Validation
- Re-read this method file first; continued on branch `ccr-6abdfb67-cbzklo`.
- Inspected only public family.json people with Ahnentafel 32–127, plus public `data/build_data.py` and `data/family_docs.json`; no private or encrypted data was accessed. No genealogy records changed.
- Arkivalieronline index metadata and secondary collateral pages were searched. No original register image has been read; the possible Hans Hansen/Ellen Kock identity remains a hypothesis. No local build or tests were run.


## Milestone 14 — Langeland frontier and historical parish-name caution
- Began rotating to the Langeland line rather than continuing the Gaardsted or Broager work exclusively. Ahnentafel 32 Niels Jørgensen (ca. 1826) has an unresolved birth-place transcription in the existing note: “Hove/Høje sogn, Svendborg amt”; parents are unknown. Existing source keys: `LL:13-4281756`, `LL:6-420495`, `LL:7-586576`, `LL:8-31142`.
- Investigated whether this might mean Hov Sogn on northern Langeland. Trap 5 states Hov parish was only constituted as an independent parish in 1896, having previously been part of Snøde and Stoense parishes. Thus **Hov Sogn cannot be used uncritically as the parish name for a birth around 1826**. A Hov/Hovland district origin could still be described informally, but the baptism should be searched in the then-current Snøde or Stoense registers only if the original wording/geography supports that interpretation. Source: https://trap5.lex.dk/sogn/hov-sogn-langelands-noerre-herred/.
- Rigsarkivet's guide confirms the correct method: when a place is known but the parish is uncertain, use the historical-administrative DigDag map to identify the parish for the date; parish registers are then searched by event date and record type. Source: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/.
- Searches for “Hove/Høje sogn, Svendborg amt” and Niels Jørgensen ca. 1826 did not produce a reliable identification of the parish or parents. Do not silently normalize “Hove/Høje” to Hov.
- Additional branch queue remains: Langeland Ahnentafel 114–115 (Christian Hansen and Marie Madsdatter), 118–119 (Mads Stephensen Johansen and Maren Larsdatter), and 120–121 (Holger Eriksen and Anne Cathrine Hansdatter), as well as Syv/Starup/Fåborg/Hoven and other lines. Current web name searches did not yield a sufficiently reliable parentage result for these Langeland couples; parish and marriage records remain the next evidence route.
- Validation: public `family.json` only; no private/encrypted records accessed. Public historical parish guide and Rigsarkivet guide checked. No original church-book images inspected, no data edits, no build/tests.


## Milestone 15 — Assing baptism source recovered for a separate frontier ancestor
- Shifted from the Langeland and Broager leads to Ahnentafel 46, Jens Peder Larsen (born about 1812, Assing), father of a later generation in the Skarrild line. Existing public-tree sources anchor him in Assing through the 1845/1850 censuses and a daughter's 1852 baptism, but his parents remain unknown.
- DS-Wiki's Assing parish page confirms historical parish-book coverage **1723–1815** and identifies the parish as Assing, Hammerum Herred, Ringkøbing Amt. Source: https://wiki.slaegt.dk/index.php/Assing_Sogn.
- Arkivalieronline's ENB collection separately lists **Enesteministerialbog for Assing Sogn (1723–1815)**. The exact AO index landing page is https://arkivalieronline.rigsarkivet.dk/da/other/index-creator/202/11592820/24284385 and the viewer endpoint is https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=24284385. The text interface exposes only a category link labelled F 1723–1745, so this ENB endpoint alone does not prove that the 1812 baptism pages are accessible there; Daisy/ordinary scanned parish-register holdings should be checked for the complete 1723–1815 volume.
- Rigsarkivet's general guide confirms that pre-1814 parish books are searched in the Enesteministerialbog and are chronological rather than using the later standardized forms; it also confirms that the records are scanned on Arkivalieronline. Source: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/.
- Rigsarkivet's digitized collection catalogue marks the Assing volume as an ENB item. This is a notable archival-quality signal, but no original page has been read and no parent names have been discovered. Source: https://arkivalieronline.rigsarkivet.dk/da/other/other-collection/202.
### Next steps for this line
1. Locate the complete Assing 1723–1815 book or its 1812 segment in the ordinary Arkivalieronline parish-register catalogue (the ENB viewer's F 1723–1745 link is not enough).
2. Search the 1810–1814 baptism chronology for Jens Peder/Jens Peter/Jens Larsen, allowing that the recorded baptism year may differ from the approximate birth year and that the later patronymic/surname form may vary.
3. Verify candidate against the 1845 and 1850 census household, spouse Kjersten Frederiksdatter, and known children's baptisms in Skarrild; only use a baptism with matching identity/context to attach parents.
4. If no baptism is found in Assing, check the original source behind the census birthplace transcription and neighboring parishes before rejecting Assing.
### Whole-tree rotation maintained
- This milestone is intentionally independent of Gaardsted, Broager/Nybøl, and Langeland. Other still-open lines remain p32/p34, p40/p41, p42/p43, p61, p66/p67, p74/p75, p114/p115, p118/p119, and p120/p121, plus the wider named branch groups recorded in Milestone 12.
### Validation
- Re-read `research_method.md` first; continued on branch `ccr-6abdfb67-cbzklo`.
- Inspected only public `family.json` for p46's public facts/source keys and public archive/parish guidance. No private/encrypted data accessed. No original baptism image read, no genealogical data changed, no build/tests run.


## Milestone 16 — Vibygård probate and employment trail for Hans Jensen (Ahnentafel 66)
- Rotated to the Syv branch (p66 Hans Jensen, ca.1752–1837; p67 Margaretha Pedersdatter, ca.1797–1871), rather than continuing the Assing, Broager, Langeland, or Gaardsted branches.
- Reconfirmed the public tree anchors: Hans Jensen married Margaretha in Syv in 1822, was described in the 1834 census as a retired gardener at Wiibygaard and on aftægt, and died in Syv in 1837 aged 85. The existing approximate birth year ca.1752 is derived from the reported age at death, not a baptism.
- Located the estate archive of Vibygård, which is directly relevant because the estate lay in Syv parish and had a long-running local archive. DS-Wiki's Vibygård page lists:
  - Skifteprotokol 1743–1850 and its register, with AO viewer endpoints https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=21026101 and https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17021266.
  - Fæsteprotokol 1719–1827 and its register, linked from the same page.
  - Source: https://wiki.slaegt.dk/index.php/Vibyg%C3%A5rd.
- A publicly available secondary extraction of the Vibygård probate protocol (Aurelia Clemons, Book 1 1743–1818; Book 2 1819–1850) gives two important leads:
  1. In a probate dated 25 February 1799 for Niels Jensen, a witness is named Hans Jensen, gartner i Wiibyegrd. This independently anchors a Hans Jensen with the exact occupation and estate location at Vibygård in 1799, when a man born around 1752 would have been about 47. It is a strong candidate match, not yet a proven identity.
  2. In a probate dated 31 December 1820 for Maren Poulsdatter in Viby, the extraction identifies her husband as Hans Jensen, gartner, and lists adult children Poul Hansen (cottager in Assingløse), Jens Hansen (also a gardener), Peder Hansen (cottager in Viby), and Ane Hansdatter (married to Willum Hansen in Valsø). This may be the same Hans Jensen who married Margaretha Pedersdatter in 1822, potentially as a widower; alternatively it may be a different gardener of the same name. The 1822 marriage record must be checked for marital status, age, occupation, and residence before identifying the men.
  - Extraction: https://aurelia-clemons.dk/vibygdx.htm (1799 entry around lines 988–995; 1820 entry around lines 1519–1525).
- The probate transcription is a finding aid, not the original record. Arkivalieronline's scanned viewer endpoints were recovered from DS-Wiki, but the image viewer returned an inaccessible/500 response through the text browser. No original probate image has been read.
- The estate also has a Fæsteprotokol 1719–1827 and a name register, but Hans was a salaried gardener rather than necessarily a tenant farmer. These may still reveal his appointment/residence or related household, while the probate protocol is the more promising immediate source.
### Next research actions
1. Inspect the original 1820 Vibygård probate for Maren Poulsdatter and verify the exact wording, marital status, and heirs; then compare with the original 1822 Syv marriage entry for Hans Jensen and Margaretha Pedersdatter.
2. If the 1822 groom is recorded as a widower and his age/occupation/residence align, treat the 1799 witness and 1820 probate as a coherent candidate chain, but do not merge until primary entries agree.
3. Search the Syv enesteministerialbog for a Hans Jensen baptism around 1750–1755; if not found, expand to neighboring parishes and use the 1799 estate employment clue to assess migration.
4. Search the Vibygård register/protocol for earlier employment, household, or probate entries that could identify Hans's parents or siblings. Distinguish the gardener from other local Hans Jensens.
5. Continue the whole-tree rotation after this bounded test; do not let the Syv/Vibygård line monopolize the next milestones.
### Validation
- Re-read this method file first; continued on branch ccr-6abdfb67-cbzklo.
- Inspected public data/family.json entries for Ahnentafel 66–67 and the public data/auto_ancestors.json frontier only. No private/encrypted data was accessed.
- Checked public archive metadata and a secondary extraction of the Vibygård probate protocol. No original register image read, no parentage established, no genealogy source data changed, no local build/tests run.


## Milestone 17 — Recheck Vibygård probate transcription and correct archive endpoints
- Reopened the actual Aurelia Clemons probate extraction rather than relying on the prior summary. It explicitly labels the material as Book 1 (1743–1818) and Book 2 (1819–1850), both on film 41401.
- Confirmed the 25 February 1799 entry for Niels Jensen at page 452 (with later references pages 464): witness is transcribed as “Hans Jensen gartner i Wiibyegrd”. This is a concrete occupation/location match to the later Syv ancestor p66, but remains a candidate identity only.
- Confirmed the 31 December 1820 probate for Maren Poulsdatter in Viby, pages 21–22 and later references 32–34: the transcription calls her husband “Hans Jensen gartner” and lists children Poul Hansen (cottager in Assingløse), Jens Hansen (gardener), Peder Hansen (cottager in Viby), and Ane Hansdatter (married to Willum Hansen in Valsø). This supports a plausible prior marriage/widower scenario before p66's Syv marriage in 1822, but does not prove identity. The 1822 marriage entry remains the key comparison.
- **Correction to Milestone 16's AO endpoint mapping:** DS-Wiki's table at https://wiki.slaegt.dk/index.php/Vibyg%C3%A5rd identifies the Skifteprotokol 1743–1850 AO endpoint as `epid=17021260` (link 8), and its register as `epid=17021266` (link 10). The Fæsteprotokol 1719–1827 is link 12; its register is link 14 (`epid=21026101`). Milestone 16 incorrectly labelled `epid=21026101` as the probate protocol. The direct AO redirects currently fail in the text browser with HTTP 500, so no original image has been read.
- Rigsarkivet's probate guide confirms that before 1851 an individual's occupation/status determined the jurisdiction; estate servants and employees are one distinct category of probate. This makes the estate archive relevant, but does not by itself establish that every gardener's probate must be in the estate protocol. Source: https://www.rigsarkivet.dk/vejledning/skifter-og-testamenter/skiftearkivalier-kom-godt-i-gang/.
- The extraction is a secondary transcription/finding aid, not the original probate protocol. It records the 1799 and 1820 entries but gives no parents for Hans Jensen. No relationship or family structure added.
### Next steps
1. Check the original Syv marriage entry from 1822 for p66 Hans Jensen and Margaretha Pedersdatter: especially widower status, age, occupation, and residence. If recorded as widower/gartner from Viby, it would materially strengthen the candidate chain from 1820 and 1799.
2. Search the Syv enesteministerialbog for Hans's baptism around 1750–1755 and check the completeness of births for that interval; do not infer parents from probate witnesses alone.
3. Then rotate to an unrelated open branch (priority: Langeland Ahnentafel 114–115 or Broager/Nybøl collateral p53) rather than continuing to mine Vibygård indefinitely.
### Validation
- Re-read this method file first; continued on branch `ccr-6abdfb67-cbzklo`.
- Inspected only public family.json and public archival catalogues/transcriptions; no private/encrypted data accessed. No original image read, no genealogy source data changed, no local build/tests run.


## Milestone 18 — bounded Syv marriage check and Langeland branch rotation
- Re-read the full research method before continuing on `ccr-6abdfb67-cbzklo`. Reconfirmed p66 Hans Jensen's exact public source key in `data/family.json`: `LL:13-4442506` is the Syv 1822 marriage; p67's corresponding key is `LL:13-4442507`. The public person note says Hans was about 70, married Margaretha (about 45 years younger), and was later described as a former gardener at Wiibygaard. No extra details of the marriage entry are transcribed in the public tree.
- Searched the exact Link-Lives source key and the names/date/parish for an independently indexed transcription or image of the 1822 marriage. The web index did not surface the record itself. Therefore the critical fields (widower/bachelor status, age, occupation, residence, witnesses) remain unverified; do not use the 1799 or 1820 probate leads to infer that the two Hans Jensen references are the same man.
- Rechecked Rigsarkivet's current parish-register guidance: for 1814–1960 use the main or duplicate parish register and search by parish, event date and name; the register is chronological by event type. The national Arkivalieronline collection still describes the new pre-1814 colour scanning as due to complete in 2026; this is a collection-level statement, not confirmation that Syv's specific volume has been updated. Sources: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/ and https://arkivalieronline.rigsarkivet.dk/en/geo/geo-collection/5.
- Rotated the public-name search to Langeland Ahnentafel 114–121: Christian Hansen/Marie Madsdatter (Magleby 1829), Mads Stephensen Johansen/Maren Larsdatter (Magleby 1832 family event), and Holger Eriksen/Anne Cathrine Hansdatter (Tved 1838). Exact-name/date searches did not return a reliable matching family transcription. Search noise included unrelated people with common patronymics; no candidates accepted and no parent links added.
- A useful archival catalogue lead for Langeland remains the Magleby Pastorat archive registration (1738–1882) in Arkivalieronline's archive-created finding aids, but the catalogue entry alone is not a parish-register or probate image. Further work should open that exact entry and map it to the correct church-book and probate series, then inspect the original 1829/1838 marriage records and adjacent baptisms. The source catalogue is https://arkivalieronline.rigsarkivet.dk/da/other/other-collection/200.
### Validation
- Re-read `research_method.md`; inspected public `data/family.json` only for p66/p67 source keys. No private or encrypted data accessed. No original parish/probate image read; no genealogy source data changed; no local build or tests run.
### Next steps
1. Resolve the Magleby Pastorat archive catalogue entry into exact Langeland parish register and probate references, then work the 1829 marriage of p114/p115.
2. Preserve the p66 Hans Jensen probate/marriage identity as unresolved until the original 1822 Syv entry is read.
3. Continue rotating across unrelated open branches; avoid treating common-name search hits as evidence.


## Milestone 19 — Magleby Langeland register series identified; catalogue lead narrowed
- Re-read the full research method first and continued on `ccr-6abdfb67-cbzklo`. Reopened the public `data/family.json` entries for p114–p121. p114 Christian Hansen (ca.1806) and p115 Marie Madsdatter (ca.1807) are recorded as married 13 November 1829 in Magleby (Langeland), with paired Link-Lives marriage keys `LL:13-5235043/44` and event keys `LL:12-16287086/87`. Their parent fields remain empty. p118–p119 are anchored by a daughter's 1832 baptism in Magleby; p120–p121 by their 1838 marriage in Tved.
- Identified a much more precise church-book series for the 1829 Magleby event: the Langeland Magleby register is catalogued by independent transcribers as **KMB 1828–1839 FKVDJTA** (Kontraministerialbog, births/confirmations/marriages/deaths/burials), with a sample marriage entry in that exact volume recorded as 1833, no.11, new image 9. This confirms the correct series and shows that marriages for 1829 should be in this volume. Source example: https://www.stroemming.dk/genealogy/gedweb/Public/da/Details/Details-I5581.html. DS-Wiki independently confirms Magleby parish is in Langelands Sønder Herred, Svendborg Amt and has church books 1813–1990: https://wiki.slaegt.dk/index.php/Magleby_Sogn_%28Langelands_S%C3%B8nder_Herred%29.
- An additional independent source list gives a generic locator “Kirkebog Magleby 1829, opslag 211” (https://www.boejesen.dk/mit%20stamtrae/kilder.htm), but it does not name Christian Hansen or Marie Madsdatter beside that locator. Treat image 211 as a possible image pointer only, not as a confirmed reference to their marriage. The exact Link-Lives event key is still the strongest direct index anchor.
- Important correction to the previous milestone's archive-catalogue assumption: Arkivalieronline's “Magleby Pastorat (1738–1882)” entry appears in the broad archive-created finding-aids index, but the accessible index text does not establish which Magleby Pastorat it describes or connect it to the Langeland marriage book. Do not cite it as the archival identity of this parish. The specific Langeland parish-register series above is a stronger and independent identification.
- Searches for the exact couple names, date, and Link-Lives key did not surface a reliable transcription of the 1829 marriage or parents. No original image was readable in this pass. No parentage or sibling relationship has been added.
### Next steps
1. Retrieve the AO/Daisy viewer endpoint for Magleby Langeland KMB 1828–1839 FKVDJTA, then inspect the 1829 marriage section around 13 November. Record both spouses' age/status, residence, occupation, fathers, witnesses and banns/permission details exactly as written.
2. Use the couple's residences and occupations from the marriage to search Magleby 1820/1825/1830 census and baptism entries, then look for each spouse's baptism around 1806–1807. Do not assume both were born in Magleby.
3. Continue branch rotation after this bounded source-recovery attempt; p118–p119 and p120–p121 remain separate Langeland family units, and other unrelated branches remain in the whole-tree queue.
### Validation
- Re-read `research_method.md`; inspected only public `data/family.json` entries for p114–p121 and public archive/catalogue/transcription metadata. No private or encrypted data accessed. No original marriage image read; no genealogy source data changed; no local build or tests run.


## Milestone 20 — Daisy catalogue confirms the correct Magleby archive creator
- Re-read the full method file and continued on branch `ccr-6abdfb67-cbzklo`. Followed the Daisy catalogue beyond the generic Magleby Pastorat lead. Daisy's own archive-series search explicitly lists **Magleby Sogn (Svendborg Amt)** as an archive creator and records an **Enesteministerialbog 1682–1814** for that creator. This is the Magleby in Svendborg Amt (the Langeland parish), not Magleby on Møn or Store Magleby on Amager. Daisy also lists a **Jævnførelsesregister, kontraministerialbog 1814–1871** for Magleby Sogn (Svendborg Amt). Sources: https://daisy.rigsarkivet.dk/arkivserie_liste?a=&b=Enesteministerialbog&d=1700&e=1700 (search result explicitly includes Magleby Sogn (Svendborg Amt), 1682–1814); and the broader Daisy archive-series listing https://daisy.rigsarkivet.dk/arkivserie_liste?a=&b=Kontraministerialbog&d=1&e=2024 (lists the parish's 1814–1871 cross-reference register).
- Daisy's digitized geographical finding aid explicitly places **Langelands søndre Magleby** in Svendborg Amt and distinguishes it from the northern Langeland parishes. Its region listing number 213 is labelled “Svendborg amt Langelands søndre Magleby”. Source: https://daisy.rigsarkivet.dk/ep?id=335346. This independently resolves the parish geography and removes the ambiguity left by the generic “Magleby Pastorat” catalogue item.
- The catalogue results do not yet expose a direct scanned-image endpoint for the **1828–1839 KMB FKVDJTA** volume. The independent Stroemming transcription still cites that exact volume for a 1833 Magleby marriage (anno 1833, no.11, new image 9), confirming the volume's identity but not the 1829 entry. Rigsarkivet's guidance says 1814–1960 entries should be sought in the main or duplicate register, organized by event type; for 1829 the V (viede) section is the target. Sources: https://www.stroemming.dk/genealogy/gedweb/Public/da/Details/Details-I5581.html and https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/.
- Search of the exact p114/p115 couple names, marriage date, and Link-Lives event keys did not find an indexed independent transcription. No original marriage image was read. The 1829 marriage and parentage remain unverified beyond the public tree's Link-Lives citations.
### Next steps
1. In Daisy/Arkivalieronline, use archive creator exactly **Magleby Sogn (Svendborg Amt)** and locate the 1814–1839 Kontraministerialbog (or Hovedministerialbog) series, then its Viede 1828–1839 segment. If the scan is not linked, record the Daisy series ID and image reference from the contents overview.
2. Inspect 13 November 1829 and the surrounding banns/marriage entries; capture the original wording and identify both spouses' residences, status, fathers, occupations and witnesses.
3. After the marriage check, rotate to another independent branch (e.g. p40–43 or p74–75) rather than extending only the Langeland line.
### Validation
- Re-read `research_method.md`; consulted public Daisy catalogue and public church-register guidance; inspected only public family tree data from the preceding milestone. No private/encrypted data accessed. No original church-book image read, no genealogy source data changed, no local build/tests run.


## Milestone 21 — vertical-first tree and site-wide UX pass; new Ribe branch evidence
### Product/UI changes
- Changed the primary navigation order so **Stamtræ** is the first destination. With no explicit URL hash, the page now opens directly on the tree rather than restoring an older overview preference from local storage. Explicit view hashes still work.
- Reworked the pedigree coordinates so the default layout is **top-to-bottom**: the proband starts at the top and ancestor generations descend below; paternal branches are laid out to the left of maternal branches. Added a visible direction switch so users can still choose the previous left-to-right landscape layout.
- Added a labelled, keyboard-focusable tree scroll region; improved focus indication for person nodes; adjusted node sizing and whitespace for easier reading.
- Applied a consistent site-wide visual refinement in site/template.html: more responsive page width and spacing, clearer sticky navigation, stronger active/hover states, more consistent card and panel surfaces, more generous table/filter controls, and refined mobile spacing.
- Kept the existing data model, person drawer, privacy unlock flow, and family facts unchanged. No genealogy records or parent links were edited.
- The coordinate code was re-read after the edit and an obsolete duplicate connector loop was removed. The generated site/index.html and docs/index.html are build outputs and have **not** been regenerated; site/build.py must be run in a local build environment before these source-template changes are reflected in generated pages/deployment.

### Genealogy — Vester Starup / Fåborg branch (Ahnentafel 40–43)
- Reopened public data/family.json entries for p40–p43 and the next generation:
  - p40 Jens Pedersen, ca.1831, married in Vester Starup in 1860; his father slot is a80, Peder Jensen, named in the marriage source. Mother is not linked.
  - p41 Kirsten Marie Nielsen, ca.1831, married p40 in 1860; her father slot is a82, Niels Jepsen. Mother is not linked.
  - p42 Peder Jensen, ca.1820, married p43 Karen Johnsen in Fåborg in 1852; both parents are unknown.
  - p43 Karen Johnsen was born 20 June 1830 in Fåborg and is already linked to John Eskesen and Ana Knudsdatter (a86/a87).
- Found a detailed secondary family history by Hans Grue, *Efterslægten til Christen Clausen fra Puggaard i Jernved sogn* (genEbooks, 2020), which appears to identify p40/p41:
  - It gives Jens Pedersen as born **2 September 1831 in Faaborg** and died **18 May 1905 in Vester Starup**.
  - It gives his wife Kirsten Marie Nielsen as born **24 October 1831 in Vester Starup** and died **26 September 1895 there**.
  - Its 1845 census transcription places a 14-year-old Jens Pedersen in the household of Peder Jensen and Zennet Marie Sørensdatter in Agerbæk, Faaborg parish. Its 1880 census transcription places Jens Pedersen and Kirsten Marie Nielsen together in Vester Starup, with children and Kirsten's brother in the household.
  - The book identifies Jens's father Peder Jensen as born **5 September 1802 in Vejrup**, married to Sinnet Marie Sørensdatter on 7 November 1830 in Faaborg. This is a strong candidate for p40's existing father stub a80 and suggests a possible mother for p40, but the book is a secondary compilation and no original register image has been read. Source: https://slaegtsbibliotek.dk/2024/946520.pdf (notably the entry for no. 184 and child no. 403 around printed pages 71–72, plus the repeated no. 403 entry and 1880 census around printed pages 131–132).
- Separately, the Danske Slægtsforskere GEDCOM-project has a **Peder Jensen** born 4 April 1820 in Vorbasse, son of Jens Christian Hansen and Else Sørensdatter, baptized 9 July 1820, married to Karen Johnsen on 7 October 1852 in Fåborg, and father of Jensine (1861) and John (1863). Its Karen Johnsen page gives her birth as 20 June 1830 in Agerbæk and names John Eskesen and Anne Knudsdatter as her parents. These details align closely with p42/p43's approximate birth, marriage, spouse, and p43's existing birth/parent anchors. This is a promising independent identity lead, **not primary-source proof**; the site explicitly says its data was submitted by a genealogist. Sources: https://gedcom.slaegt.dk/?fil=60&person=9317 and https://gedcom.slaegt.dk/?fil=60&person=9318.
- Keep the two families distinct: p40's father candidate Peder Jensen was born in 1802 in Vejrup and married Sinnet Marie Sørensdatter in 1830; p42's candidate Peder Jensen was born in 1820 in Vorbasse and married Karen Johnsen in 1852. They are different generations and different Ahnentafel branches, despite the shared name and Fåborg parish anchor.
- Do not add the suggested mother to p40 or parents to p42 yet. The original sources to inspect are the Fåborg (Skast Herred, Ribe Amt) birth entry for Jens Pedersen in 1831, the Vester Starup marriage entry in 1860, the Vejrup/Fåborg records for Peder Jensen and Sinnet Marie Sørensdatter, and the Fåborg marriage and Vorbasse baptism entries for p42. Avoid confusing this Fåborg parish in Ribe Amt with Faaborg town/parish in Svendborg Amt.
- Rigsarkivet's guide confirms that 1814–1960 main/duplicate parish registers are arranged chronologically by event category (births, confirmations, marriages, arrivals, departures, deaths); this gives the correct search structure for the 1831 baptism and 1852/1860 marriages. Source: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/.

### Validation and next steps
- Re-read research_method.md before work; stayed on branch ccr-6abdfb67-cbzklo.
- Inspected only public data/family.json, site/template.html, and public archival/genealogy sources. No private/encrypted data accessed. No original parish image read; no parentage changed.
- No local build, browser test, or automated test was run. The generated HTML copies remain stale until the documented build is executed.
1. Validate the vertical SVG coordinates and connectors in a browser at desktop and mobile widths; check that the whole-tree canvas remains navigable with keyboard and touch.
2. Inspect the original Fåborg 1831 baptism and Vester Starup 1860 marriage for p40/p41; compare the parents/residences with the secondary book before linking Sinnet Marie Sørensdatter.
3. Inspect the Vorbasse 1820 baptism and Fåborg 1852 marriage for p42/p43; only add Peder Jensen's parents if both primary records support the identity.
4. Continue whole-tree rotation after this bounded Ribe-branch check; do not return to Langeland or Gaardsted by default.


## Milestone 22 — drawer accessibility, Danish document language, and Ribe branch triangulation
### UX and accessibility refinements
- Added `aria-modal="true"` to the person drawer and a keyboard focus trap: Tab/Shift+Tab stays within the open dialog, Escape closes it, and closing returns focus to the invoking control.
- Opening the drawer now locks background page scrolling; the drawer body itself remains independently scrollable, with touch overscroll containment.
- Added shared visible keyboard focus styling, touch-friendly interaction behavior, and a `prefers-reduced-motion` override so transitions/animations are minimized for users who request reduced motion.
- Widened the drawer to a 480px maximum while retaining a full-width mobile drawer.
- Corrected `site/build.py` so the generated GitHub Pages document declares Danish (`lang="da"`) rather than English. This is an accessibility and screen-reader language improvement for the Danish-language family site.
- Source files changed: `site/template.html` and `site/build.py`. Generated `site/index.html` and `docs/index.html` are not regenerated yet; the local build commands in README remain required. No build or browser test was run.

### Genealogy — Ribe / Vorbasse / Egtved branch (p42, p84–p85, candidate p168–p171)
- Re-read the public family tree and confirmed that p42 Peder Jensen (born ca.1820; spouse p43 Karen Johnsen) has no linked parents. The public tree has p43's parents already linked as a86 John Eskesen and a87 Ana Knudsdatter.
- The Danske Slægtsforskere GEDCOM-project gives a Peder Jensen born **4 April 1820 in Vorbasse**, baptized **9 July 1820** after home baptism on 6 April, son of **Jens Christian Hansen** and **Else Sørensdatter**; it also connects him to Karen Johnsen, their 1852 marriage in Fåborg, and children Jensine (1861) and John (1863). The site states that these details were submitted by a genealogist, so this remains secondary/submitted evidence, not an original register transcript. Source: https://gedcom.slaegt.dk/?fil=60&person=9317.
- Independently located Svend Aage Nielsen's 2021 *Anetavle for fabrikant Poul Rahbek Hansen* (Danskernes Historie Online, https://slaegtsbibliotek.dk/927489.pdf). Its compact Ahnentafel lists Jens Christian Hansen (1783–1852, Egtved) and Else Sørensdatter (16 Apr 1797–18 Jul 1841, Egtved) as the couple corresponding to p42's reported parents. Its expanded pedigree identifies Jens Christian as child of **Hans Christian Hansen** (ca.1751–1830) and **Ane Pedersdatter** (1755–1798), and Else as child of **Søren Storm** (ca.1759–1820) and **Anna Kirstine Bentsdatter** (1759–1838). The book further says Hans Christian was son of Hans Christoffersen; Søren Storm married Anna Kirstine in 1783 in Vester Nebel; Anna Kirstine was daughter of Bent Mikkelsen. The book supplies detailed birth, baptism, death, and burial claims, but it is a compiled pedigree, not the original parish records. Source lines: compact table on PDF printed pages 6–7; expanded entries around printed page 32 (PDF lines 2263–2315 in the extracted text).
- The independent 2020 Hans Grue family history *Efterslægten til Christen Clausen fra Puggaard i Jernved sogn* does **not** identify this same Peder Jensen: it describes a different Peder Jensen born 5 Sep 1802 in Vejrup, husband of Sinnet Marie Sørensdatter, and their son Jens Pedersen born 2 Sep 1831 in Faaborg. Keep this 1802 Peder (p40's father candidate) separate from p42's 1820 Peder. Source: https://slaegtsbibliotek.dk/2024/946520.pdf, printed page 72.
- Located the precise AO viewer collection for Vorbasse Sogn's Kontraministerialbog **1813 FKVDJTA–1821 FKVDJTA**: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17128288. This covers the reported 1820 baptism. AO's churchbook guide confirms F=born, K=confirmed, V=married, D=dead and the 1814–1892 duplicate-register scans; the viewer itself exposes the collection but its scan image could not be read in this text session. Sources: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17128288 and https://arkivalieronline.rigsarkivet.dk/da/geo/geo-collection/5.
- The 2020 family history also gives more exact evidence for p40: Jens Pedersen born **2 Sep 1831 in Faaborg**, died 18 May 1905 in Vester Starup; 1845 census household at Agerbæk includes Peder Jensen (43), Zennet Marie Sørensdatter (37), and Jens (14), plus siblings; 1880 Vester Starup census lists Jens with wife Kirsten Marie Nielsen, their children, and her brother Kristen Nielsen. It says Peder Jensen (1802–1882) married Sinnet Marie on 7 Nov 1830 in Faaborg. This is a strong identity match for p40 and p40's existing father stub a80, but no original record has yet been read. The source is a detailed secondary compilation: https://slaegtsbibliotek.dk/2024/946520.pdf, printed pages 72 and 132.
- Do **not** create p42's parents or grandparents yet. p84–p85 and p168–p171 are well-defined candidates from two secondary compilations, but the promised original Vorbasse 1820 baptism and Egtved records have not been inspected. The original Fåborg 1852 marriage also remains unread. Likewise, p40's mother candidate Sinnet Marie Sørensdatter remains unlinked pending primary verification.

### Validation and next steps
- Re-read `research_method.md` before continuing; remained on `ccr-6abdfb67-cbzklo`. Public `data/family.json` only; no private/encrypted data accessed and no genealogy records changed.
- Inspected the changed source-template logic, generated-page build logic, and drawer interactions. Static source checks only; no browser execution, local build, or automated tests.
1. Open the Vorbasse 1813–1821 Kontraministerialbog and inspect the 1820 F entry for Peder Jensen; transcribe the original parents, residence, and witnesses. Then inspect Egtved baptism/marriage/death entries for Jens Christian Hansen and Else Sørensdatter.
2. Locate Fåborg's 1831 baptism for Jens Pedersen and Vester Starup's 1860 marriage for p40/p41; compare all names, ages, residences, fathers, and witnesses against the 2020 secondary book.
3. Inspect the Fåborg 1852 marriage and subsequent children for p42/p43 before creating p84–p85 links.
4. Run `python3 site/build.py` in a local environment and verify the vertical tree, direction toggle, mobile scrolling, dialog focus trap, reduced-motion behavior, and Danish page language.
5. Resume whole-tree branch rotation after the bounded Ribe checks; do not allow this line to monopolize further milestones.



## Milestone 23 — Syv / Vibygård probate lead for Ahnentafel 66
- Re-read the complete research method and public tree before continuing on branch `ccr-6abdfb67-cbzklo`. Rotated from the Ribe/Vorbasse work to the separate Syv branch (Ahnentafel 66–67); no private or encrypted data was accessed.
- Reopened the public entries for a66 Hans Jensen and a67 Margaretha Pedersdatter. The tree records their marriage in Syv in 1822, a daughter baptized in 1825, and Hans's death in Syv in 1837 at a reported age of 85. Its note says he was formerly a gardener at Vibygård and was on aftægt in 1834. This makes a birth around 1752 plausible but still derived from the death-age report.
- Reopened Aurelia Clemons's published extraction of Vibygård Gods probate protocol (a secondary transcription/extract, not the original register). It identifies a probate on **31 December 1820** for **Maren Poulsdatter in Viby**; her husband is named **Hans Jensen, gardener**. Four adult children are listed: Poul Hansen (cottager in Assingløse), Jens Hansen (gardener), Peder Hansen (cottager in Viby), and Ane Hansdatter (married to Willum Hansen, farmer in Valsø). The entry is in Book 2 (1819–1850), pp. 21–22, with further references on pp. 32–34. Source: https://aurelia-clemons.dk/vibygdx.htm (lines 1519–1525 in the opened extraction).
- This is a substantial candidate link to a66: the same estate context and the same distinctive occupation (gardener) align with the tree's report that Hans Jensen had been Vibygård's gardener before marrying Margaretha in 1822. If the probate husband is a66, Maren Poulsdatter would be his prior wife and the four named adults his children. The chronology is plausible, but **the identification is not proved**: the probate extract does not give Hans's age, patronymic, or a direct reference to the 1822 Syv marriage. Do not add Maren or the four children to the tree yet.
- The DS-Wiki Vibygård entry independently confirms that the estate had both a probate protocol (1743–1850) and a fæsteprotokol (1719–1827), with digitized viewer links. The AO probate protocol viewer is https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17021260 and register viewer https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17021266; the fæste-protocol viewer is https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=21026101. The text-only web interface could not read the original scan images. DS-Wiki: https://wiki.slaegt.dk/index.php/Vibyg%C3%A5rd.
- Rigsarkivet's guide confirms that a post-1814 marriage should be sought in the parish's Hovedministerialbog or Kontraministerialbog, under the chronological Viede section; the church-book collection guide explains the event abbreviations. Sources: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/ and https://arkivalieronline.rigsarkivet.dk/da/geo/geo-collection/5.
- No original probate or Syv marriage image was read, and no family relationships were changed. Public tree inspection only; no local build or tests were run.
### Next steps
1. Compare the original 1820 Vibygård probate entry (pp. 21–22 and cross-references pp. 32–34) with the Syv 1822 marriage entry for Hans Jensen and Margrethe/Margaretha Pedersdatter. Look for explicit widower status, age, residence, and occupation; seek the original 1837 burial entry for Hans's age and residence.
2. If the identity is corroborated, trace the four adult children and Maren Poulsdatter through Syv/Viby/Assingløse registers and censuses before adding any family links.
3. Rotate to another open branch (for example a74–a75, Rosmus/Attrup, or the separate Langeland family units) rather than letting Syv become the sole focus.
4. Keep the original scan unread status explicit; secondary extraction is a lead, not a primary-source transcription.


## Milestone 24 — Elgezira.dk Magleby/Langeland source collection reviewed
- Re-read the full method file and checked the current public tree entries for the Langeland branch (p114–p121). Stayed on `ccr-6abdfb67-cbzklo`; no private or encrypted data accessed.
- Reviewed https://elgezira.dk/historie.html and followed its linked documents:
  - Magleby parish-register transcriptions: 1682–1706, 1707–1726, and 1727–1744.
  - A reconstructed family compilation for Magleby 1682–1706.
  - Ahlefeldt estate probate extracts for 1755–1850 (books 1–5; book 6's 1827–1850 probate papers are explicitly not available in the document).
  - An index/extract of Bagenkop probates 1689–1850, plus land-register links from 1665, 1675, 1688 and 1701.
- The site’s family-compilation foreword is important for source criticism: the author says it was assembled over 6–7 years using the parish-register transcription and local knowledge of Nordenbro; people are grouped into families across 1682–1706, and children are followed where possible. The author explicitly warns that there will be uncertainties and errors, and that some identities/places cannot be fully read or verified. Ages at death/probate and inferred birth years are sometimes calculated retrospectively. Treat this as a valuable finding aid and secondary reconstruction, not as primary evidence. Source: https://elgezira.dk/historie/bog/Familier_sat_sammen_i_Magleby_sogn_1682_1706.pdf (foreword, PDF p.1).
- The Ahlefeldt estate probate compilation is credited to Aurelia Clemons (dated 10 March 2004 and April 2009) and identifies its source series as Ahlefeldt gods, Svendborg probate protocols, books 1–5, 1755–1850, with Family History Library film references. It gives useful estate and kinship detail, but it too is an index/abstract, not a scan transcription of each original probate. Source: https://elgezira.dk/historie/bog/Grevskabet%20Langeland%20Gods,%20Svendborg%20Book%201,2,3,4,5%20&%206%20-%201755-1850.pdf (opening page).
- Specific lead in the probate abstracts: a **Christian Hansen, farmer in Nordenbro**, appears in a probate dated **5 March 1787**, with second wife Mette Jensdatter and children Sidsel (6), Ane Christine (4), Maren (1½), and a posthumous son Christian Christiansen; the first wife Sidsel Christensdatter had died in 1779, and their children included Hans Christiansen (11) and Karen Christiansdatter (9). The abstract refers back to the first wife's 1779 probate. This may be useful background for identifying earlier Christian/Hansen families in Nordenbro, but there is no demonstrated connection to p114 Christian Hansen (born ca.1806, married 1829); the names and parish alone are insufficient to attach the family. Source: same Ahlefeldt probate abstract, entry around PDF p.38 (lines 1700–1710 in extracted text).
- The Magleby church-book transcriptions contain many people called Maren Larsdatter. For example, the 1707–1726 transcription records a Maren Larsdatter who married John/Johan Henrichsen in 1712; the 1727–1744 book records a Maren Larsdatter associated with Nordenbro/Nordenbrogaard and several later events. The family reconstruction also distinguishes multiple unrelated Larsdatter families (including Maren born ca.1691 and another Maren born ca.1703). These are **not** p119 Maren Larsdatter (born ca.1807): the dates are a century too early, and the repeated name is not evidence of identity. This reinforces the need to use the 1832 baptism source and later records for p119 before tracing her parents.
- Exact-name checks for p118 Mads Stephensen Johansen and p120 Holger Eriksen did not find matches in the three 1682–1744 parish-book transcriptions or the Ahlefeldt probate abstract. This is expected for men born around 1800–1815, since the church-book transcriptions stop in 1744; absence from these older documents is not evidence against their identity. The Ahlefeldt probate abstract does contain numerous local Nordenbro entries and may help with collateral family context, but no p118/p120 link is established.
- The source page also links a Bagenkop-only probate index, but p114–p121 are tied to Magleby/Nordenbro rather than Bagenkop; that index was not treated as evidence for them. The main Ahlefeldt probate compilation is the more geographically relevant lead.
- No tree relationships or source data were changed. No original parish-book or probate images were read; all reviewed material from this site is transcribed/compiled secondary material. No local build or tests were run.
### Next steps
1. Use the Ahlefeldt probate references (book/page/film) to locate original probate images for relevant Nordenbro families, especially the 1787 Christian Hansen case, then test any proposed descendant link through parish baptisms/marriages.
2. For p114 Christian Hansen and p115 Marie Madsdatter, prioritize the original 13 November 1829 Magleby marriage entry and baptism records circa 1806–1807; do not use 18th-century same-name people as parents without an explicit chain.
3. For p118/p119, trace the daughter’s 1832 baptism and identify the exact residence and parent names; then follow Maren Larsdatter's own baptism/marriage/death in the 1800s register rather than selecting one of the earlier same-name women.
4. Continue the full-tree branch rotation after this Langeland source reconnaissance; p40–43, p66–67, and p74–75 remain independent work items.


## Milestone 25 — Rosmus/Attrup: conflicting 1811 marriage identity (Ahnentafel 74–75)
- Re-read the full research method and public data/family.json; stayed on branch ccr-6abdfb67-cbzklo. Inspected only public people and public archival/genealogy sources; no private/encrypted data accessed.
- The current tree records a74 Jens Hansen as an unmarried man from Attrup who married 6 July 1811 in Rosmus to a75 Mette Pedersdatter, daughter of farmer Peder Hallis/Hallisen in Attrup. The tree says their children were Ane Sophie (1812), Christen (1818), and Mette (1820); it cites the Rosmus register's 1811 marriage image and 1812 baptism image (internal image labels 28238649 and 28238652). These are the tree's existing claims, not independently verified in this milestone.
- Found a substantial independent genealogy extract, Nanna Vester's GEDCOM extract (Tom Brøndsted), which gives Jens Hansen Broge, born 10 June 1781 in Attrup and baptized in Rosmus, as a son of Hans Pedersen Broge and Mette Jensdatter Smed. It states that this Jens married Mette Sørensdatter Helles on 6 July 1811 in Rosmus — the same date and parish as a74's recorded marriage, but with a different bride's name. Source: https://tom.brondsted.dk/genextracts/?chpt=21&colbranch=&ged=2&sid=I29 (search extraction around child no. 43). This creates a significant identity conflict: the groom's name, date, and parish fit a74 very closely, but the bride does not match a75. The extract is a compiled GEDCOM, not the original register; it does not prove that the two references are to the same couple or establish which bride is correct.
- The Rosmus/Hyllested transcription of the earlier church book (1684–1788) independently documents the Broge family name and Attrup locality, but it ends before the 1811 marriage and cannot resolve the bride. Source: https://www.wadschier.dk/afskrifter/rosmus_hylle1684_1788_w.pdf.
- A Rugaard Gods probate index/extract (1754–1787) includes an 1783 probate for Søren Sørensen Helles in Rosmus. It names a deceased daughter Mette Sørensdatter Helles in Balle, who had been married to Rasmus Jensen Hjulmand and left a son Jens Rasmussen. This is an earlier, distinct Mette and is not evidence for the proposed 1788-born bride; it is useful mainly as a warning not to merge same-name Helles women. The extract also produced no exact Peder Hallis or Halles match. Source: https://slaegt.dk/media/h3neknbf/alfabetisk-navneliste-og-skifteuddrag-for-rugaard-gods-g296-71-1754-1787.pdf (entry 179, probate dated 27 September 1783).
- Rigsarkivet's current guide confirms that the original 1811 event belongs in the pre-1814 Enesteministerialbog and should be found under the chronological marriage entries; after 1814, main and duplicate books are used. The guide also notes the historical administrative parish must be established correctly. Sources: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/ and https://arkivalieronline.rigsarkivet.dk/da/geo/geo-collection/5.
- Research conclusion: this is the strongest new lead in the Rosmus branch, but the original 1811 marriage and the 1812/1818/1820 baptisms have not been read in this session. Do not change a74's spouse, add parents to a74, or remove a75/a150. Preserve both candidate bride identities as unresolved until the original entries are inspected. The 1812 baptism is especially important: it should identify the mother and can test whether the marriage was to Mette Pedersdatter Hallis or Mette Sørensdatter Helles.
- No tree relationships or source data were changed. No original register or probate image was read, and no local build or tests were run.
### Next steps
1. Inspect the original Rosmus 6 July 1811 marriage entry and transcribe both spouses, residences, status, witnesses/guarantors, and any father's names; compare with both candidate identities.
2. Inspect the 1812 baptism of Ane Sophie and the 1818/1820 baptisms; determine whether the same couple and maternal name recur.
3. If the groom is Jens Hansen Broge (born 1781), verify his baptism and parents in the Rosmus book before attaching them to a74.
4. Trace Mette Pedersdatter Hallis independently through the original 1812 baptism and her own birth/confirmation/marriage/death records; do not treat the Peder Hallis reading as settled until checked against the scan.
5. Rotate to a separate branch after this bounded conflict-resolution pass; retain whole-tree coverage rather than focusing exclusively on Rosmus.


### Milestone 25 follow-up — resolve the Rosmus conflict and rotate to Assing
- Rechecked the actual public tree entries for a74/a75 and their child p37, rather than relying only on the research summary. The tree's p37 note says the 16 February 1812 birth/baptism entry was read directly from Rosmus kirkebog image 28238652 and explicitly names the parents as farmer Jens Hansen and Mette Pedersdatter; p37 was home-baptized 17 February. The 1818 and 1820 children are separate Link-Lives baptism references (LL:12-3672434 and LL:12-3673083), but their source strings do not themselves identify the mother's full name. This is direct-source evidence for Mette Pedersdatter as mother of the 1812 child, stronger than the compiled GEDCOM's assertion that Jens Hansen Broge married Mette Sørensdatter Helles on the same date. It still does not prove whether there were two Jens Hansen marriages/couples or whether the GEDCOM entry is wrong; do not merge the two identities.
- Newly located Rigsarkivet volunteer inventory (March 2026) lists Rosmus Sogn's Enesteministerialbog 1789–1816 as containing **FVD** (births, marriages? no: the official abbreviations are F=born, V=married, D=dead; the inventory's FVD list therefore does include V) from 1789–1816. Important correction: the initial reading of FVD as omitting V would be wrong; V is the marriage abbreviation. This series therefore is the correct original book for checking the 1811 marriage. Source: https://www.rigsarkivet.dk/wp-content/uploads/2022/02/Nyt-fra-de-frivillige-marts-2026.pdf, p.4; abbreviation key: https://arkivalieronline.rigsarkivet.dk/da/geo/geo-collection/5. (Note: FVD = fødte, viede, døde.)
- The Rigsarkivet guide confirms pre-1814 events should be found in the Enesteministerialbog and are written chronologically; it is not a preformatted event table. Source: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/.
- Rotated research to the separate Assing branch, p46 Jens Peder Larsen. A public compiled family database gives a precise candidate profile: Jens Peder Larsen, born 29 February 1812 in Pårup Melgaard, Assing, baptized same date, married Kjersten Frederichsdatter on 8 October 1843 in Sønder Felding, died 25 May 1870 in Sønder Omme/Kirkeby and buried 2 June 1870. This matches p46's approximate 1812 Assing birth, spouse, and branch context. Source: https://www.horsboel.dk/familie/grind/dat16.htm (lines 415–429). The database does not name his parents in this entry and is secondary evidence, so it adds no parentage. The 1870 Sønder Omme census transcription independently places Jens Peder Larsen (age 51, born Assing) with Kirsten Frederiksen and children in Kirkeby, consistent with the same family. Source: https://www.horsboel.dk/fkt/FKT_Sdr_Omme_1870.pdf (p.26).
- Rigsarkivet's Assing finding aid confirms the relevant pre-1814 Enesteministerialbog spans 1723–1815, which includes the reported 1812 birth; DS-Wiki lists later Assing church books 1816–1956. Sources: https://arkivalieronline.rigsarkivet.dk/da/other/other-collection/202 and https://wiki.slaegt.dk/index.php/Assing_Sogn. The original 1812 baptism image has not been read in this session; no parents should be added to p46 based on the secondary compilation alone.
- No genealogy data or relationships changed. Public tree only; no private/encrypted data accessed. No original scan was read, and no build/tests were run.
### Updated next steps
1. Inspect the Rosmus Enesteministerialbog 1789–1816 at the 6 July 1811 marriage entry and compare the bride's full name with p37's 1812 baptism; use the original record to decide whether the GEDCOM's Mette Sørensdatter Helles is an error or a separate couple.
2. For p46, inspect the Assing 1812 baptism (29 February) and transcribe parents, residence, and witnesses; then compare the Sønder Felding 1843 marriage and Sønder Omme 1870 burial against the Horsboel secondary profile.
3. Continue rotating to other open branches after these bounded source checks; no speculative parent links.


## Milestone 26 — homepage redesign, latest research and vertical tree
- Re-read the complete research method before editing; stayed on `ccr-6abdfb67-cbzklo`. No private or encrypted data was accessed.
- Updated `site/template.html` so the default landing view is the former overview, renamed in the navigation to **Forside**. The overview now includes a dedicated **Seneste fund** section and the interactive family tree directly on the same page. The navigation's **Stamtræ** item now jumps to that homepage section rather than switching to a separate view.
- Added four research cards, each with links to the relevant external source material and an explicit evidence status:
  - **Assing / Jens Peder Larsen:** secondary family compilation gives the 29 February 1812 Assing baptism, 1843 marriage and 1870 death; the independent 1870 census transcription supports the household identity. His parents remain unverified, so no parent link was added.
  - **Rosmus / 1811 marriage:** the tree's existing 1812 baptism note identifies Mette Pedersdatter, while a compiled GEDCOM gives a conflicting bride, Mette Sørensdatter Helles. The original marriage entry is still needed.
  - **Syv / Hans Jensen:** the 1820 Vibygård probate extract is a plausible but unproved match for the tree's Hans Jensen; no spouse or children were added.
  - **Magleby / Christian Hansen:** the 1787 Nordenbro probate is useful local context but is not connected to the Christian Hansen who married in 1829.
- Moved the existing interactive ancestor-tree controls and SVG into the homepage. The tree now has a single, fixed top-to-bottom generation layout; removed the horizontal direction toggle and its rendering branch. Father/mother ordering and person-card interactions remain unchanged.
- Added responsive research-card styling and retained the existing accessible focus, scrolling and reduced-motion rules. A static structural check passed: all five remaining view IDs exist, the homepage renders the tree, the tree is nested within the overview, no duplicate HTML IDs were found, and no stale horizontal-layout identifiers or old tree-view references remain.
- **Validation limitation:** no browser, JavaScript runtime, local build, or visual regression test was available. `site/build.py` was not run; generated `site/index.html` and `docs/index.html` have therefore not been regenerated in this commit. The live Pages output will require the normal public-data build pipeline before deployment. No genealogical source data or relationships were changed.
### Next steps
1. Run `python3 site/build.py` in the repository's normal safe build environment, then inspect the generated homepage at desktop and mobile widths.
2. Check the vertical tree's scroll/zoom behavior with the full ancestor set and confirm that the homepage anchor and person drawer's “Vis i stamtræ” action land correctly.
3. If the generated pages pass review, commit the build artifacts through the normal publishing workflow; do not copy or expose decrypted private data.
4. Continue whole-tree genealogy research separately; the four homepage cards are leads and evidence summaries, not new parentage claims.

- **Milestone 26 follow-up:** a post-edit reference scan found one remaining person-drawer visibility check pointing at the removed `v-stamtrae` view. Updated it to check the homepage overview before scrolling to the tree. Re-ran the structural checks: all remaining view containers exist, the drawer-to-tree check targets the homepage, the tree is vertical-only, no duplicate IDs exist, and there are no stale `v-stamtrae` references. Latest template content SHA: `a85c8d7acd07f4aa11fa2e6c1b16c63e602e29dd`. Browser/build validation is still outstanding.


## Milestone 27 — von Kleist-sporet mod middelalderen
- Re-læste hele denne metodefil og fortsatte på `ccr-6abdfb67-cbzklo`. Arbejdede kun med offentlige slægtsoplysninger og åbne historiske kilder; ingen private eller krypterede data blev tilgået.
- Genbesøgte den allerede dokumenterede Gedde/von Kleist-forbindelse og kontrollerede H. W. Harbous artikel *Slægten von Kleist i Danmark* (Personalhistorisk Tidsskrift, 1897). Harbou fører Ove Samuel Geddes hustru Frederikke Louise Dorthea von Kleist (født 5. januar 1786) til hendes far Christian Frederik (født 1743), dennes far Christian Adam (født 1705), og videre til Cartz Ulrik von Kleist, søn af Pribislaff von Kleist på Muttrin og Esther von Kameke. Kilden er en genealogisk sammenstilling fra 1897, men giver en konkret, navngiven forbindelse mellem Vivis Gedde-linje og Muttrin-grenen i Pommern. Kilde: https://www.v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf (især linjerne/afsnittet om Cartz Ulrik og hans børn).
- Kontrollerede von Kleist-familiens dokumentoversigt og dokumentbog:
  - **1248:** Conradus og Bertoldus Clest optræder i et dokument.
  - **1289:** Klest (Klest de Densin) optræder i et dokument fra Stolp.
  - **1477:** lensbrev fra hertug Bogislaw X nævner Muttrin-, Damen-, Tychow-, Dubberow-, Vilnow- og Raddatz-linjerne; teksten gengiver familiens erklæring om fælles stamfader og tre sønner.
  Kilder: https://www.v-kleist.com/FG/urkunden/urkunden.htm og https://www.v-kleist.com/FG/Gesamt.pdf.
- Vigtig kildekritik: 1248/1289-dokumenterne og 1477-lensbrevet dokumenterer middelalderlige medlemmer og slægtens egen påstand om fælles ophav, men de beviser ikke i sig selv en ubrudt direkte kæde fra Vivis konkrete Muttrin-forfader Pribislaff (død 1698) til Conradus Clest eller Klest de Densin. Familiehistorien omtaler selv huller i den tidlige dokumentation; forbindelser mellem enkelte tidlige generationer må behandles som hypotetiske, indtil de er dokumenteret i de relevante lensbreve og biografier. Ingen middelalderlige personer er derfor føjet til stamtræet som direkte aner.
- Opdaterede `site/template.html` med et femte kort under **Seneste fund** på forsiden, der beskriver von Kleist-sporet og dets begrænsninger med links til Harbou, dokumentbogen og Muttrin-registeret. Den vertikale anetavle og øvrige forsideelementer er bevaret.
- Opdaterede `family-tree.md` med en særskilt note om middelaldersporet og den nødvendige forskel mellem dokumenteret slægtsgren og endnu ikke bevist middelalderlig direkte afstamning.
- Validering: kontrollerede indsættelsesmarkører og filopdateringer via GitHub-API; ingen lokal HTML-build, browser- eller JavaScript-test er kørt. `site/build.py` er ikke kørt, så genererede `site/index.html` og `docs/index.html` afspejler endnu ikke det nye forsidekort. Ingen relationer i genealogidata blev ændret.
### Næste skridt
1. Gennemgå Muttrin-familiehistorien fra 2025 for den præcise far-til-søn-kæde fra Pribislaff (III.281, død 1698) tilbage gennem de dokumenterede 1400-talsled; sammenhold hvert led med de nævnte urkunden.
2. Læs selve 1477-lensbrevet i dokumentbogen og identificér, hvilke Muttrin-personer der faktisk indgår i den direkte gren, frem for at stole på senere navnelighed.
3. Fortsæt samtidig på andre uafhængige grene i Vivis træ. Middelaldermålet må ikke få os til at overse bonde-, præste- og håndværkerlinjer, som kan føres til 1500–1600-tallet via skifter, jordebøger, tingbøger og fæsteprotokoller.


### Milestone 27 follow-up — the Muttrin history reaches 1364
- Inspected the full searchable text of the revised 2025 *Geschichte des Geschlechts v. Kleist — Muttrin-Damensche Linie, der Muttriner Ast* (2nd revised edition). Its contents explicitly include a **Borntin-Dänischer Seitenzweig**, the branch relevant to the Danish officers. The volume says the Muttrin-Damensche line descends from the second of three family stem-brothers, **Prissebur** (Urk. 125), and describes the early sequence from **Klest de Densin** through Prissebur and his descendants.
- Particularly important source criticism in the volume itself: it states that its early genealogical arrangement is based on individual contemporary documents **and** family records from much later, and that the placement of the earliest persons is a **probable reconstruction**. It reports Prissebur in document 83 (1364) as co-owner of land at Glineke, named as Klest of Muttrin; the names of his sons come from a family genealogy dated 1576, corroborated by a referenced older letter. It then cites documents from 1389, 1402, 1407, 1435 and 1439 for successive members and relationships. Source: https://www.v-kleist.com/FG/Muttrin/Muttrin.pdf, printed pages 5–7 / extracted lines 293–333.
- The same volume identifies the Muttrin branch's 1477 ancestor Bisprow as son of Henning and says the 13 April 1477 feudal letter names him with three sons. The Danish Harbou article (1897) separately places the Danish-connected Cartz Ulrik as son of Pribislaff von Kleist of Muttrin/Borntin and lists Christian Adam among Cartz Ulrik's children; the volume's contents include a Borntin-Danish branch. Together these make a coherent, high-value research path from the Danish Kleist line into the medieval Muttrin-Damensche family history, but the precise step-by-step identification of Pribislaff III.281 within the 2025 branch genealogy still needs to be extracted and checked before adding medieval ancestors to Vivis tree.
- Updated the homepage card and `family-tree.md` to include the 1364 Prissebur evidence, the Borntin-Danish branch, and the family-history authors' own warning that the earliest pedigree is reconstructed. No medieval ancestor was added to `data/build_data.py` or the public tree.
- No local build or browser test was run. The new homepage card is in `site/template.html`; generated `site/index.html` and `docs/index.html` remain stale until the normal safe build.


- **Source-scope clarification:** the 2025 PDF is titled for the Muttrin branch; its contents list the Borntin-Danish side branch as part of the wider Muttrin-Damensche history, but the exact Borntin-Danish section itself has not yet been read. Homepage and narrative wording now say that the contents list this branch, not that the current PDF's extracted pages independently prove its full genealogy. Next, locate and inspect that branch's own pages/biographies before claiming the precise connection from Pribislaff III.281 to Prissebur.


## Milestone 28 — Borntin-Dänischer Seitenzweig: Pribislaff III.281
- Re-read the complete `research_method.md` before continuing; stayed on `ccr-6abdfb67-cbzklo`. Only public genealogical and historical sources were inspected. No private/encrypted material was accessed.
- Rechecked Harbou's 1897 *Slægten von Kleist i Danmark*. It explicitly identifies Danish officer **Cartz Ulrik (III.369)** as son of **Pribislaff (III.281)** of Muttrin, Borntin, Döbel and Drenow and Esther von Kameke. Harbou records Cartz Ulrik's Brandenburg service in Brabant (1692–1694), entry into Danish service 9 August 1701, subsequent promotions, and death at Rendsburg in 1722. Source: https://www.v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf, PDF lines 174–179 / article page around 104.
- The current von Kleist name index identifies Pribislaff III.281 as a Muttrin member, died 1698, spouse A. E. von Kamecke, biography reference FG III,3 p.277. This corroborates the identity and corrects the older Lengnick chart's death reference of 1686. Source: https://v-kleist.com/FG/NamenabfrageL.html (search result extraction for row III.281).
- Located a specific candidate father: the 1840 Lengnick family table (reproduced in the digitized volume *Familien V. Kleist*) gives the sequence **Prebislaw of Borntin (documented/mentioned 1621) → Hans Jürgen, Landrat → Prebislaw of Muttrin, Borntin and Drenow → Cartz Ulrik**. It then links Christian Adam and Christian Frederik to the Danish Gedde family. This is a secondary pedigree and its earlier medieval sequence is not proof by itself. Source: https://slaegtsbibliotek.dk/900782.pdf, extracted lines 4005–4018.
- Additional independent secondary pointers: Schlossarchiv's Rittergüter-Lexikon lists the Muttrin and Döbel owners in a sequence **Pribislaff (d.1640) → Hans Jürgen (d. before 1665) → Pribislaff (d.1698)**. Geneanet user trees also propose Hans Jürgen III.186 as father of Pribislaff III.281 and Pribislaff III.114 (d.1640) as his father. These are finding aids/user genealogies, not primary proof. Sources: https://schlossarchiv.de/?gut=9439&such= and https://schlossarchiv.de/?gut=9409&such= and https://gw.geneanet.org/cvpolier?lang=en&n=von+kleist&p=hans+jurgen.
- Dirk Peters' 2017 *Ahnentafel Peters* register excerpt says Adam Heinrich von Kleist was Pribislaff's eldest son and received Borntin in 1688 during his father's lifetime; it cites a division agreement dated 12 July 1698 for Muttrin/Döbel holdings. Useful for targeting the underlying feudal/probate records, but secondary compilation only. Source: https://dirkpeters.info/wp-content/uploads/2018/10/ahnentafel_peters_bd_4.pdf (search result around register entry 5110).
- The 2025 Muttrin-Damensche family history remains the key medieval source. It explicitly warns that its early pedigree is a probable arrangement based on contemporary documents plus much later family records; it identifies Prissebur at Muttrin in 1364, then names sons from a 1576 family genealogy and documents successive members in 1389, 1402, 1407, 1435 and 1439. It does **not** by itself yet prove the specific chain from Pribislaff III.281 to Prissebur. Source: https://www.v-kleist.com/FG/Muttrin/Muttrin.pdf, printed pages 5–7 / extracted lines 293–333.
- Assessment: Cartz Ulrik → Pribislaff III.281 is strongly supported by Harbou and the current family register. Hans Jürgen as father of III.281 is a concrete secondary-source lead; Pribislaff (d.1640) as Hans Jürgen's father is another candidate link. Neither relationship was verified in an original feudal letter, estate account, probate, or other contemporary record in this session. The 1840 Lengnick pedigree offers a search route toward the 13th-century names but must not be treated as proof of uninterrupted descent.
- Updated `family-tree.md` with the candidate chain, clear source hierarchy, and caveat; updated the von Kleist homepage research card to mention the Hans Jürgen lead as unconfirmed. No person relationships or dates were changed in `data/build_data.py` or public genealogy data.
- Validation: GitHub file updates and insertion markers only. No local build, browser test, or original archival image/record inspection was available. Generated `site/index.html` and `docs/index.html` remain stale until the normal safe build.
### Next steps
1. Locate the original 1698 inheritance division and the 1688 Borntin feudal grant; inspect their wording, witnesses, heirs and father-son designations for Pribislaff III.281, Adam Heinrich, and any siblings.
2. Locate the contemporary feudal/estate records that identify Hans Jürgen's father and distinguish Pribislaff III.114 (d.1640) from other same-name Kleists.
3. Inspect the actual Borntin-Danish section (the 2025 volume contents place it at p.420 in that edition) and trace its source notes, not just its contents heading.
4. After this bounded source pass, rotate to another open branch of Vivis tree; keep the whole-tree scope.


### Milestone 28 follow-up — exact Muttrin inheritance chain and archive targets
- Located and inspected the family-history compilation *Materialzusammenstellung zu den früheren Gütern der Familie v. Kleist*. Its Muttrin section states that the estate passed from Hans v. Kleist at Borntin to his son Pribislaw III.281; the footnote identifies Hans as III.186 and gives his inheritance chain: **III.186 inherited from III.114, III.114 from III.54, and III.54 from III.22**. This is a much more specific chain than the previously isolated Hans-Jürgen lead. It is still a later family-history synthesis, not an original deed transcription. Source: https://www.v-kleist.com/FG_allg/G_Zusammenstellung.pdf, pp.118–119, footnotes 353–354.
- The same source exposes a date discrepancy that must be resolved: it dates the Muttrin inheritance/partition after Pribislaff's death to **12 June 1698**, while its Drenow section dates the transfer of Drenow to his second son Cartz Ulrik to **12 July 1698**. Dirk Peters' 2017 compilation gives 12 July for a partition agreement. Do not merge these into one event; locate the underlying original agreements and determine whether there were two separate transactions or a secondary transcription/date error.
- Identified primary-source repositories and finding aids from the family association's Landesarchiv Greifswald inventory:
  - **Rep. 40 Nr. 35 gg, fols. 2–13**: 99 feudal-letter extracts compiled by Lehnsarchivar Thilo. The archive note says the original extracts were sold to Peter Christian von Kleist in 1766 and that it is currently unclear whether the Greifswald text is the original.
  - **Rep. 41 Nr. 28 Plathe**: von der Osten's Adelsspiegel manuscripts, including an older family genealogy with later marginal additions.
  - **Rep. 40 Nr. 35 gg** also contains pastor Steinbrück's genealogical work c.1780 and the son's 1820–1830 work/materials.
  - Elzow's Adelsspiegel is held in Stettin under **65/16/0/60/498**, genealogical material from folio 180 onward. The family archive guide quotes Elzow's own warning that his material was incomplete and may contain errors.
  Source: https://www.v-kleist.com/bestand_greifswald.htm, especially lines 7–37.
- This is an actionable archival plan, not proof that the 13th-century chain is continuous. Updated `family-tree.md` with the III.22 → III.54 → III.114 → III.186 → III.281 chain, the June/July 1698 date conflict, and the exact archive references. No genealogical data or relationships changed.
- Validation remains GitHub file update only; no original archival document has been inspected and no build/browser test run.


- Further archival inventory detail: the Greifswald family-archive list includes a file titled **“Klage der Erben des Hans-Jürgen v. gegen die Prälaten Mannen und Städte des Stiftes Cammin wegen Schuldenforderungen”**, dated **1633–1692**, signature **Rep. 7 Nr. 5894**. This may be relevant to Hans Jürgen III.186 or another same-name person; identity must be checked before use. It is now an additional targeted archive request alongside Rep.40 Nr.35 gg and Rep.41 Nr.28 Plathe. Source: https://www.v-kleist.com/bestand_greifswald.htm.


## Milestone 29 — Assing 1812 baptism: archive coverage rechecked
- Resumed the whole-tree research queue after rereading this complete method file and the public family-tree notes. Chose Ahnentafel 46, Jens Peder Larsen (c.1812, Assing), because the existing secondary profile gives a precise baptism date (29 February 1812) while his parents remain unverified.
- Rechecked Rigsarkivet's Daisy catalogue. It lists two distinct Enesteministerialbog records associated with Assing for 1723–1815: one for **Assing Sogn** and one for **Sønder Felding Sogn**. This is useful because the later family profile's 1843 Sønder Felding marriage must not be conflated with the 1812 Assing baptism volume. Catalogue: https://daisy.rigsarkivet.dk/arkivskaber_og_arkivserie_liste?a=sogn&b=enestemin&d=1&e=2022 (rows for Assing at lines 77–78); ENB overview: https://arkivalieronline.rigsarkivet.dk/da/other/other-collection/202.
- Rigsarkivet's current guide confirms that pre-1814 entries are in the Enesteministerialbog, recorded chronologically rather than in the later standard forms, and that the scans are made available through Arkivalieronline. Source: https://www.rigsarkivet.dk/vejledning/kirkeboeger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/.
- Attempted to open the previously identified Arkivalieronline viewer endpoint for the Assing ENB (epid 24284385), but the web retrieval interface could not access it. No page image or baptism entry was inspected in this run. The catalogue confirms a relevant archival series, not the specific baptism, identity, or parentage.
- **Conclusion:** no parent names or new relationships are established; no genealogy data, family-tree.md, or homepage content was changed. The 1812 baptism remains an outstanding primary-source check. Next step: open the Assing ENB directly in a normal browser/Arkivalieronline viewer, navigate chronologically to 29 February 1812 (also check the adjacent date because the old calendar/recording may differ), transcribe the full entry and witnesses, then test the identity against the 1843 Sønder Felding marriage and the 1870 Sønder Omme census.
- Validation: source catalogue and guide inspected through indexed web text; original scan inaccessible in this session. No build or tests run.
