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
Phase 4 — complete public-data integrity audit and regression-test design; implementation is deferred until a safe execution/test route is available.

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
1. Inventory root, `data/`, `site/`, `docs/`, tests, workflows, and dependency/config files.
2. Trace data model and validation/privacy logic in `data/build_data.py`, `data/private_tool.py`, `data/export.py`, and `site/build.py`.
3. Inspect generated artifacts and deployment workflows for consistency.
4. Identify tests and run safe, non-secret-dependent checks where possible.
5. Resume genealogical source research only after the technical architecture is mapped; preserve uncertainty around all candidate identities.


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
