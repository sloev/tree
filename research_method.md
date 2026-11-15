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
