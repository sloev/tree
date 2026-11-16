# Repository research method

This file defines the working method for genealogical research in `sloev/tree`. The repository-specific instructions in [AGENTS.md](AGENTS.md) and the four active grandparent dossiers in [leads/README.md](leads/README.md) take precedence if a procedural detail conflicts.

## 1. Scope and repository discipline

- Work only on the Gårdsted and Gedde family-history project.
- Work directly on `main`; do not create feature branches or pull requests unless the owner changes this instruction.
- Read `AGENTS.md`, `leads/README.md`, the latest `coop.log.md` entries and the relevant grandparent dossier before research or edits.
- The four grandparent dossiers are the sole active research workspaces. Put each claim in the dossier for the relevant grandparent line. Cross-reference shared events by person ID rather than copying the same claim into several active files.
- Never access, decrypt, quote or publish private records without explicit, scoped authorization. Never put passwords or decrypted files in Git.
- Keep generated files in step with their sources. The canonical genealogy source is `data/build_data.py`; `data/family.json`, `family-tree.ged`, summaries and website output are generated/reference products.

## 2. Evidence hierarchy and source handling

Prefer sources closest to the event, while recording the nature and limitations of every source:

1. Original civil, church, census, probate, court, military, land and other contemporary records.
2. Contemporary copies, certified extracts, official registers and archival finding aids.
3. Published scholarly or local-history works with traceable citations.
4. Compiled genealogies, indexes, online family trees and databases.
5. Family documents, oral history, photographs and correspondence.

This is not a mechanical ranking. A source may be authoritative for one fact and silent about another. For every item record:

- Creator/title, archive or collection, record type, date and locality.
- Volume, page, entry, image, folio, case or journal number where available.
- Exact wording or a faithful transcription for decisive statements.
- What the source directly establishes, what it merely reports, and what it cannot establish.
- Stable URL and access date for online material.

A catalogue entry proves that a record series is described or held; it does not prove the contents of an individual record. An index is a finding aid, not a substitute for the original entry. A search with no result is a bounded negative search, not proof that a person or record did not exist.

## 3. Separate identity, events and relationships

Do not merge people because they share a name, occupation, farm, parish or approximate date. Resolve identities using several independent attributes such as age, birthplace, spouse, parents, occupation, residence and witnesses. Keep similarly named people separate until the evidence supports a match.

Treat each relationship as its own sourced assertion. Distinguish:

- Biological parentage and descent, including children born outside marriage.
- Marriage, remarriage, partnership and other documented unions.
- Legal or recorded parenthood and acknowledged paternity.
- Adoptive parenthood.
- Step-parenthood.
- Foster, guardian, household and other social relationships.

Marriage does not prove biological parentage. A paternity declaration or court decision proves what was declared or legally decided to the extent shown by the record; it is not automatically independent genetic proof. A baptismal entry naming a father is evidence of what the register records, but conflicting evidence must remain visible. Do not infer illegitimacy from silence, stigma, a surname or a missing father field.

Use explicit calibrated states such as established by record, probable, family-claimed, possible, disputed, rejected and not yet checked. Keep evidence status separate from biological status. Preserve conflicting assertions with their own source, author/ informant, date and explanation; do not force a single answer when the evidence does not support one.

## 4. Research workflow

For each question:

1. **Frame the question.** State the exact identity or relationship to be tested, the competing hypotheses and the time/place range.
2. **Read the active dossier.** Check earlier searches, conflicts and handoffs so work is not repeated or contradictory.
3. **Find the record series.** Use official archive catalogues and finding aids. Confirm the correct parish, civil jurisdiction, archive creator, date range and administrative boundary.
4. **Inspect the record.** Prefer the original image or file. Transcribe names, dates, places, occupations, household roles, witnesses, marginal notes and references exactly enough for another researcher to repeat the check.
5. **Corroborate identity.** Follow the person through independent records before attaching parents, spouses, children or a similarly named individual.
6. **Assess each relationship.** Explain what each source proves and does not prove. Preserve disagreements and source limitations.
7. **Record the result.** Update the one relevant dossier, including the source citation, conclusion, confidence, rejected alternatives and next concrete action.
8. **Update canonical data only when justified.** Add or alter a person or relationship only when the evidence rule in the dossier is met. Keep uncertain claims in the dossier rather than presenting them as settled tree links.
9. **Regenerate and validate.** Run the documented data, GEDCOM and site build commands after source changes. Review generated diffs and check that privacy protections and unrelated branches remain intact.
10. **Hand off.** Append a concise dated entry to `coop.log.md` describing files read and changed, evidence found, tests/builds actually run, unresolved issues and the next actionable step.

## 5. Archive and online research

Search using spelling and language variants, historic place names, parish boundaries and administrative changes. Record which variants, catalogues, date ranges and collections were searched. For Danish and Schleswig-Holstein research, distinguish parish, herred, amt, judicial district, police district and later archive creator; their boundaries and names may change over time.

When a record is unavailable online, do not repeatedly issue broad searches after the catalogue and indexed sources have been exhausted. Write a precise archive enquiry naming the person(s), event, locality, date window, record series and known reference numbers. State which documents are still needed and what each would resolve.

## 6. Canonical data and website changes

- Keep genealogical facts in `data/build_data.py`; regenerate `data/family.json` with `python3 data/build_data.py`.
- Regenerate GEDCOM with `python3 data/export.py`.
- Regenerate the site with `python3 site/build.py`.
- Do not hand-edit generated output as a substitute for editing its source.
- Relationship evidence belongs to a relationship, not to a person's overall confidence field. Where the data model cannot represent competing parentage, do not leave one disputed candidate in a field rendered as settled parentage.
- Preserve multiple unions and distinct parent roles where the source data supports them; never infer a biological link from spouse or household membership.
- Follow `AGENTS.md` for responsive design, accessibility, generation colours, navigation and privacy.

## 7. Completion standard

A research task is complete when another researcher can repeat the source search, understand the conclusion and its limits, distinguish facts from hypotheses, and see exactly what remains unresolved. A null result is useful when its search scope is documented. Do not claim that a build, test, deployment, archive inspection or source verification occurred unless it was actually performed.

## 8. Current handoff

The active branch dossiers and the latest entries in `coop.log.md` are the live status. In particular, the Lorenz paternity question remains unresolved: the Egernsund register records Wilhelm Krogh as biological father following a declaration and court decision; the family account identifies Sophus Petersen; Peter Frederiksen was the social/stepfather. The original 1932 case file has not yet been inspected. Keep these three roles distinct and do not mark biological paternity as settled.


## 8. Publication threshold: publish with an explicit status

Do not hold a credible historical claim back from the public family tree merely because it is not proven beyond doubt. Publish it with a plain-language confidence label and a short explanation of what the source does and does not establish. The aim is a living, qualified family history, not an indefinitely unfinished research project.

Use these public labels:

- **Well established / Godt belagt:** contemporary records or strong, genuinely independent corroboration support the stated fact.
- **Needs more evidence / Kræver mere belæg:** the claim is credible, but an identity, parent-child link, reading or intermediate generation remains unresolved.
- **Speculative / Foreløbig hypotese:** a plausible reconstruction, family tradition or possible identification; never render it as a proven parent-child edge.
- **Family account / Familieoplysning:** a provenance label, not a confidence rating. Preserve the account as a claim and seek corroboration without erasing it.

Assess the existence/identity of a person separately from every relationship attributed to that person. A well-documented individual may have speculative parentage. A source may establish a person's title, landholding or presence as a witness without proving descent. Distinguish biological, legal/registered, marital, step, foster, guardian and household ties. If the website's current data model cannot label a particular relationship independently, explain that limitation in the person's note and do not imply that person-level confidence automatically validates the edge.

Publication is not permission to flatten contradictions: show competing readings and identify which source is contemporary, derivative, or family tradition. Change the canonical parent edge only when the evidence supports that relationship at the chosen level; otherwise publish the person and claim without connecting the line.
