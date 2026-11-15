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
