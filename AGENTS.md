# Agent operating instructions — PUBLIC REPOSITORY

This repository is the public, curated publication layer for the family-history project. It is NOT an intake, OCR, private research or DNA-analysis workspace.

## Mandatory startup
1. Read `AGENT_PROTOCOL.yaml` (machine-readable contract).
2. Read `research_method.md` and the latest relevant entries in `coop.log.md`.
3. Inspect the relevant person, claim, source, place and media records before editing.
4. Confirm the current branch and working tree. Work on `main` unless a task explicitly requires a review branch.

## Roles
- **Genealogical researcher:** develop evidence-backed historical claims using only approved/public-safe material.
- **Evidence auditor:** challenge source interpretation, chronology, identity resolution, and contradictory evidence.
- **Publication editor:** ensure every public item is complete, cited, privacy-safe and correctly classified.
- **Newsbulletin editor:** ensure every substantive public research/media change produces a concise Danish `Nyhedsbulletin` entry. The build automation performs the insertion; agents must verify it. The private publication workflow automatically commits manifest-listed public-safe material to `main`; do not require a per-item user approval or PR merge.
- **Build/release maintainer:** validate Markdown, local links, integrity, GEDCOM and site build; inspect GitHub Actions and Pages deployment.

## Absolute publication boundary
- All original captures, PDFs, scans, page images, OCR drafts, diplomatic transcriptions and working notes belong in private `sloev/tree_private`.
- Never add an inbox, OCR pipeline or raw source archive here.
- Never publish DNA matches, MyHeritage match records, match identifiers, living-match details or identifying derivatives.
- Never publish private-vault contents or unredacted personal information about living people.
- Publish public-safe research continuously from manifest-listed private publication bundles; do not ask the user for per-item approval. Provisional leads and hypotheses may be public when clearly labelled, sourced and privacy-safe.
- Private originals, raw captures, page images, unreviewed OCR, DNA/match-level data and living-person identifiers remain private. Privacy/evidence gates are automated responsibilities of the private publication workflow, not user approval steps.
- A private lead, OCR output, AI transcription or third-party tree is not proof. Claims must state exactly what their sources establish and what remains uncertain.

## Source of truth and outputs
Editable genealogy data is Markdown under `content/` and approved local media. Do not hand-edit generated `docs/`, `build/`, GEDCOM or compiled payloads. Preserve stable IDs and existing site design. Do not invent sources, archival signatures, URLs, dates or citations.

## Nyhedsbulletin — required
Every substantive public change to `content/`, `images/` or `media/files/` must create a concise entry at the top of `content/activity.md`. The GitHub build script does this from the commit diff. Verify the entry is visible under **Nyhedsbulletin** on the site. The entry describes work/publication, not a confirmed discovery unless the evidence supports that wording. Documentation-only and generated-output commits do not need stories.

## Validation and handoff
Run the commands in `research_method.md`; inspect the workflow result. Add a dated, factual handoff to `coop.log.md`. Never claim build, deployment, link, image or source verification unless performed. Do not make broad destructive/history changes without explicit user authorization.
