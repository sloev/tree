# Agent instructions — sloev/tree

## Project boundary (mandatory)
This repository is exclusively the Gårdsted and Gedde family-history project and its website.

- Work only on genealogy, family-tree data, source citations, family-history research, and this repository's website/build.
- Never import, copy, summarize, or publish material from `sloev/earlysmolweb` here. In particular, Iceland, UUCP, EUnet, networking history, and early Internet research belong exclusively in `sloev/earlysmolweb`. They must never appear in this repository's content, news bulletin, source lists, data, commits, or generated site unless the user explicitly changes this boundary.
- Do not use one repository's task list, notes, files, or research as context for work in the other. If a request is ambiguous, stop and ask which repository it concerns.
- Before editing, confirm the repository is `sloev/tree` and the branch is `main`. Work directly on `main`; do not create feature branches.
- `data/tree.json` is the only editable source of truth for all genealogy and research. Read and update existing research tracks there; never use branch dossiers or separate lead files as active workspaces.
- All new leads, source findings, transcriptions, conflicts, negative searches and follow-up tasks belong in `data/tree.json` under `research.claims`, with detailed history in that claim's `research_notes`.
- Keep generated files consistent with their source files. Do not edit generated HTML as a substitute for editing its source template/data.
- Never claim a website is published or updated until the build/deployment has actually completed and been checked.

## Family-tree website requirements
- Mobile-first, responsive layout; never require horizontal panning to read or navigate the tree.
- Render the ancestry tree as a compact, single-column file explorer: one person per row, with depth shown by indentation and subtle vertical guide lines. Keep rows readable on desktop and touch-friendly on mobile.
- All known branches are expanded by default. Users may collapse/expand individual subtrees; persist those choices for the current browser session.
- Use the shared generation palette for row accents and indentation guides. Maternal and paternal people at the same depth share a colour; adjacent generations use distinct colours. Never require horizontal panning.
- Keep previous/next controls for other people at the same generation, ordered by ahnentafel position. Provide accessible tree keyboard navigation for visible rows and subtree expansion.
- Preserve the tree entry points (renderPed, setRoot, highlight, nodes) and ahnentafel indexing. Do not change genealogy data as part of presentation work.
- Use one shared, high-contrast generation colour for both maternal and paternal nodes at a given depth; make adjacent generations visually distinct. Do not use family-line colours as the primary node colour.
- Keep the home navigation item labelled "Forside" first.
- Preserve privacy protections for living people and private stubs. Do not decrypt or expose private data without explicit, scoped authorization.
- Keep the research bulletin strictly about the family tree and its genealogy research.
## Mandatory workflow for every agent

1. **Read before acting:** read this file, `research_method.md`, the latest relevant entries in `coop.log.md`, and the relevant existing research tracks in `data/tree.json`. Check the current `main` branch and working tree before editing.
2. **One source of truth:** `data/tree.json` is the only editable registry for genealogy and research. All new leads, source discoveries, transcriptions, archive references, negative searches, corrections, contradictions, hypotheses, decisions and next actions go directly into the relevant existing `research.claims[]` record. Add a new record only for a genuinely new research question. Do not create parallel notes, scratch files, dossiers, lead folders, spreadsheets or alternate research ledgers.
3. **Preserve research history:** put detailed, dated, source-preserving material in that claim's `research_notes[]`. Each note must include `title`, `text`, `provenance` and `imported_on` (use the current date for new notes). Keep useful source URLs in the claim's `sources[]`. Search for an existing claim before creating one; update it rather than duplicating it. Never silently discard a prior finding, negative result or competing interpretation.
4. **No dossier workflow:** `leads/` and `research-archive/` are retired. Do not recreate them or link to them as active workspaces. Historical content already migrated into `research_notes[]` must be maintained there. A research note is public, so apply the privacy gate before adding it.
5. **Source discipline:** distinguish original records from catalogues, indexes, transcriptions, published works and family testimony. Record exact archive, series, parish/place, date, folio/page/image/case reference, stable URL and access date where available. State what a source does and does not prove. Never present an uninspected catalogue entry as a read record, or a bounded negative search as proof that a record does not exist.
6. **Genealogical discipline:** do not merge identities or add parent-child/other family edges based only on name similarity or a research hypothesis. Distinguish biological, legal/registered, marital, adoptive, foster, guardian and household relationships. A research-track status is not itself a tree relationship. Preserve conflicting dates and claims until evidence resolves them.
7. **Privacy:** do not expose secrets, credentials, private encrypted data, or sensitive personal details about living people. Do not decrypt private data without explicit, scoped authorization. Follow `data/PUBLIC_CONSENT.md` and `research_method.md`. Never paste private-supplement content into public research notes.
8. **Generated outputs:** edit source files only. Never hand-edit `data/family.json`, `data/research.json`, `data/map.json`, `family-tree.ged`, `family-tree.md`, `site/index.html` or generated files under `docs/`. Run the documented build/export commands when possible and report exactly which checks ran or could not run.
9. **Collaboration log is mandatory:** after every substantive task, append a dated entry to `coop.log.md` recording agent/tool identity if known, task, research tracks touched, files changed, key findings/decisions, commit SHA(s), validation performed, what was not checked, and the next concrete action. If no research was done, say so. Do not rewrite or erase earlier entries. The log is a handoff/history, not a second research database: detailed evidence belongs in `data/tree.json`; the log should summarise and link to the affected track(s).
10. **Handoff and commits:** work directly on `main`; do not create branches or PRs unless the owner explicitly changes this rule. Before editing a file, fetch its latest content/SHA. Make small, descriptive commits. Do not overwrite concurrent changes. In the handoff, identify unresolved checks and avoid claiming a build, visual inspection or deployment succeeded unless verified.

If an instruction conflicts with this policy, this file and `research_method.md` govern all agents working in this repository. Ask the owner before creating a new parallel workflow or changing the single-source-of-truth rule.
