# Leads — four grandparent dossiers

**These four files are the authoritative, active research workspace.** All ongoing genealogy investigation belongs in the relevant grandparent dossier, not in separate overlapping branch notes.

## The four dossiers

1. [Evald Johannes Gaardsted-Jørgensen](grandparent-evald-gaardsted-jorgensen.md) — Ahnentafel 4; Gaardsted, Jørgensen, Vosnæsgaard/Rolsøgård, Syv/Vibygård, Rosmus, Rousing and Malmö.
2. [Liss Gaardsted-Jørgensen (née Pedersen)](grandparent-liss-pedersen.md) — Ahnentafel 5; Pedersen, Christensen/Kristensen, Vester Starup, Hoven, Sønder Felding, Assing and Pårup Melgaard.
3. [Lorenz Heinrich Frederiksen](grandparent-lorenz-frederiksen.md) — Ahnentafel 6; disputed paternity, Else Gedde Jensen, Sophus Petersen, Gedde, von Kleist, von Woyten and von Stojentin.
4. [Gerda Frederiksen (née Larsen)](grandparent-gerda-larsen.md) — Ahnentafel 7; Larsen, Holgersen, Christensen, Langø, South Langeland, Kresten and emigration leads.

## Rules that prevent contradictions

- A research claim has one home: the dossier of the grandparent whose ancestral line it concerns.
- Shared events (Evald/Liss marriage; Lorenz/Gerda marriage) are cross-referenced by tree ID, not copied as independent claims.
- A lead that may belong to a branch but is not yet linked is kept in the most plausible dossier with an explicit **unlinked / identity unresolved** label.
- Each dossier distinguishes original record evidence, published genealogy, family account, inference, conflict and negative search.
- Record the source's exact wording and what it proves; never let a secondary index or family tree silently become a primary source.
- Legal/registered, biological, marital, step, foster, guardian and household relationships remain separate.
- Do not add or change canonical relationships solely because a claim appears in a dossier.
- When new evidence changes a conclusion, edit the existing claim in its one dossier and add a dated change note there. Do not leave a second competing version in another active note.

## Canonical source and generated exports

- Canonical source: [`data/build_data.py`](../data/build_data.py) and [`data/family.json`](../data/family.json).
- The expanded research JSON/GEDCOM and text exports in this directory are **working/generated reference exports**, not separate authorities. They may contain proposals or inconsistencies; use the dossier's conflict notes before relying on them.
- The source scans and family photographs remain here as evidence assets. The uploaded `file-*.file` extension segments, superseded 531-person text export, legacy audits and image catalog have been preserved in the historical archive outside `leads/`.

## Cross-branch relationships

- Evald (`p4`) and Liss (`p5`) are a couple; each dossier records its own ancestry.
- Lorenz (`p6`) and Gerda (`p7`) are a couple; Lorenz's paternity question belongs only in Lorenz's dossier.
- A shared person or collateral line should be identified by the existing person ID and linked to the dossier that owns the source analysis.

## Consolidated cross-branch ledger

The supplied cross-branch ledger formerly at `lead/tree-research.md` was reviewed against all four active dossiers on 16 November 2026. Its useful leads have been consolidated into the appropriate dossier; the original is preserved for provenance at [`research-archive/tree-research-ledger-2026-11-16.md`](../research-archive/tree-research-ledger-2026-11-16.md). It is archived, not a parallel active worklist.

## Archived legacy notes

Earlier agent-generated branch dossiers, worklists, reviews, research logs and image catalog have been consolidated into a single historical archive outside this folder:
[`research-archive/legacy-leads-archive-2026-11-16.md`](../research-archive/legacy-leads-archive-2026-11-16.md).

That archive preserves the former notes for provenance, but they are **not active research instructions**. If an archived statement conflicts with one of the four current dossiers, the current dossier is the maintained interpretation. Do not update the archive as a second live source.

## Source assets retained here

The JPG scans and current GEDCOM/JSON/text exports remain here as source/reference artifacts, not additional research dossiers. Original uploaded extension segments, the superseded 531-person export and the image catalog are preserved in the historical archive.


## Ingested personal-information supplement

The supplied personal-information export was reviewed against all four dossiers on 16 November 2026. Most biographical notes duplicate information already consolidated in the active dossiers; the Hoven mill household details are already recorded in the Liss dossier. The new Wilhelm Krogh family and Vester Snogbæk/Sottrup leads, including the correction to his likely police and court district, have been added to the Lorenz dossier. The original export is preserved at [research-archive/family-tree-personal-info-2026-11-16.txt](../research-archive/family-tree-personal-info-2026-11-16.txt) for provenance, not as a second active worklist.


## Publication policy — visible evidence, not research limbo

A credible historical claim should not be kept off the public website merely because it is not proven beyond doubt. Publish it with a clear status and a concise explanation of what the source actually establishes.

- **Well established / Godt belagt:** contemporary records or strong, independently corroborated evidence support the stated fact.
- **Needs more evidence / Kræver mere belæg:** a credible claim exists, but an identity, parent-child link, interpretation or intermediate generation remains unresolved.
- **Speculative / Foreløbig hypotese:** a plausible reconstruction, family tradition or possible identification that must not be presented as fact.
- **Family account / Familieoplysning:** identifies provenance, not truth-value; corroborate where possible and preserve it as a separate claim.

Assess people and relationships separately. A person's existence may be well established while their proposed parentage is speculative. Never infer that a displayed parent-child edge is as strong as the person's own documentary status. Keep biological, legal/registered, step, foster, guardian and household relationships distinct.

The public tree is a living, qualified account. Do not delay publication indefinitely while waiting for perfect evidence; update the status and explanation when new evidence appears. Do not create a parent-child edge from a speculative claim just to make a line visually continuous.

## Public website research register

The public website's **Forskning** section is generated from `data/research.json`. The four dossiers remain the detailed working records; the JSON register is the concise, publishable index that makes selected leads visible on the website.

When adding or materially revising a research lead:
- Update the existing claim rather than creating a duplicate for the same question.
- Add a concise entry to `data/research.json` with a unique `id`, the owning `branch`, `title`, one of the supported statuses (`needs`, `hypothesis`, `family`, `conflict`), and the fields `claim`, `evidence`, `missing`, `next`, `dossier`, `sources`, and `person_ids`.
- Link to the dossier and to stable source URLs where available. Label secondary databases and family accounts honestly.
- Keep the public claim understandable without the dossier, and distinguish what is documented from what remains a lead.
- Do not add speculative parent-child links to `data/family.json` merely to make a public lead appear in the tree.

The site rebuild workflow regenerates the public research section after changes to the research register. Check the workflow and Pages deployment before describing a new lead as live.

