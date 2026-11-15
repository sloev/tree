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
Phase 0 — establish repository state and map the architecture.

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
