# Review of expanded family tree file — 16 November 2026

## File inspected

- `leads/family-tree-expanded.txt`
- Repository version: 103,941 bytes in GitHub metadata; fetched text 98,416 characters / 1,302 lines.
- SHA: `2daeaca32eea2e0466abdb68a81bf79263464cf8`
- The file is preserved unchanged. This review is separate; no canonical family data or GEDCOM was changed.

## Overall assessment

This is a substantial research compilation, not merely a prose summary. It contains a large expanded transcription of branches and a separate November 2026 research summary. It is valuable as a working source register and clue map. It should **not** be imported wholesale or described as 39 independently verified new ancestors: the file mixes archival references, modern family-history compilations, online genealogy databases, family knowledge and hypotheses. Its own legend distinguishes some of these categories, but the summary headings sometimes overstate certainty.

The current `data/family.json` has 489 person records and 489 unique IDs (98 living/private records). The expanded file correctly says its starting tree has 489 people; its claimed 528 total is a projection for the expanded text, not the current canonical dataset.

## Critical correction: von Kleist Tychow branch is still mis-nested in this file

The file's tree section around lines 444–463 and its summary around lines 1170–1208 both give:

`Reimer II.2 → Bartez II.6 → Andreas (Drews) II.11 → Carsten II.21 → Bernd II.39 → Christian II.60`

That parentage is not what the numbered biographies in the cited 2025 Tychow-Dubberow volume state. The same volume distinguishes the two brothers and their branches:

- The 2025 Tychow-Dubberow volume says Hans of Tychow I.24 had sons Reimer II.2 and Bartes II.3.
- However, L. Quandt's transcription of the 13 April 1477 collective fief letter in *Allgemeine Geschichte* names “Pribbeslaw zu Muttrin mit seinen Söhnen, die Brüder Reymer und Bartes zu [Groß-]Tichow”. The same discussion says the earlier Tychow/Dubberow branch ancestor is not known from the older family records. The father of Reimer and Bartes is therefore disputed between the 1477 charter transcription and the later Tychow genealogy; do not state Hans I.24 as proven.
- Reimer II.2's sons include Bartez II.6.
- Bartes II.3's sons include Andreas (Drews) II.11.
- Andreas II.11 is the father of Carsten II.21; Carsten is father of Bernd II.39; Bernd is father of Christian II.60.

Therefore Bartez II.6 is a collateral relative of Andreas II.11, not his father. The expanded file's indentation and its “verified chain” paragraph both need correction before this text is reused. From Bartes onward, the branch is **Bartes II.3 → Andreas II.11 → Carsten II.21 → Bernd II.39 → Christian II.60**. Reimer II.2 → Bartez II.6 is a separate sibling branch. The parent of Reimer and Bartes remains disputed: the Tychow-Dubberow genealogy says Hans I.24, while the 1477 charter transcription in *Allgemeine Geschichte* says Pribbeslaw of Muttrin. The English PDF is a machine translation; consult the German originals and underlying charter before publication.

The file also says “five generations” were added from Reimer to Christian, but the line actually mixes the collateral Reimer/Bartez branch with the Andreas/Carsten branch. Do not repeat that generation count without recalculating it from the corrected branch.

## Other high-priority source-quality issues

### Rosenkrantz and Krag

The file labels these lines “verified,” but much of the cited support is WikiTree, Geni, Wikipedia, Finn Holbek and family-tree compilations. Those are useful discovery tools, not primary sources. The biographical dictionary may support particular public-figure facts, but it does not automatically prove every parent-child link in the chain. Treat these as promising secondary/tertiary leads until each link is backed by contemporary records or a reputable scholarly genealogy with transparent citations.

### Gedde

- The file correctly labels some Samuel Christoph / Hans Christopher Gedde relationships as uncertain, but other entries appear in the expanded tree with record symbols despite citations to modern biographies or Geni.
- The Ove Samuel Gedde birth-date conflict (1778 in Harbou vs 1788 in Anker) remains unresolved. Do not create a second Ove or overwrite the existing record on this file alone.
- Keep the 1895 family group photograph and other family-held material as separate image/source leads; the text's existence does not itself supply the actual image or permission to publish it.

### Other branches

The expanded file includes many useful indexed record references (LL/AO/DFS/ARK identifiers), but a citation identifier alone is not an extracted record. For each new relationship, retain the actual image/transcription, parish/archive, year, event and exact wording. The notes on the Gaardsted, Vibygård, Lorenz/Wilhelm Krogh, Dybbøl, Langeland and other open lines should remain leads until the cited entries have been inspected and identity matches tested.

## Data and editorial checks

- The expanded file is a separate `.txt` compilation; it does not itself update `data/family.json` or the GEDCOM.
- It reports 39 new verified entries and 528 total entries, but the actual canonical `data/family.json` remains 489 people. The claimed 39 additions need an itemized ID-to-source audit before any import.
- The file's own “verified” label is not an independent evidence grade. Reclassify each new person/relationship by the actual source type and what the source explicitly states.
- Keep biological, legal, step/social, adoptive and household relationships distinct.
- Preserve the existing raw file unchanged and record corrections in a separate review.

## Recommended next steps

1. Correct the two Tychow diagrams/summary paragraphs so Reimer/Bartez and Bartes/Andreas are shown as collateral branches.
2. Build an itemized register of the claimed 39 additions: proposed ID, name, relationship, source/page/record, exact supporting statement, evidence class, confidence and unresolved conflicts.
3. Audit Rosenkrantz and Krag links first against the cited biographical works and contemporary records; demote unsupported WikiTree/Geni-only links to leads.
4. Resolve Ove Samuel Gedde's 1778/1788 conflict independently.
5. Inspect the strongest LL/AO/DFS record references for the other branches and log negative searches with exact scope.
6. Only then prepare a small, sourced patch for `data/family.json` and GEDCOM. No structural import has been made in this review.


## Subsequent source qualification — 1477 father attribution

The statement above that Hans I.24 is the father of Reimer II.2 and Bartes II.3 is not settled. A later comparison found that *Allgemeine Geschichte* transcribes the 1477 collective fief letter as naming Pribbeslaw of Muttrin with sons Reimer and Bartes. The 2025 Tychow-Dubberow volume instead assigns the brothers to Hans I.24. This conflict is recorded in the new itemized audit at leads/von-kleist-source-audit-2026-11-16.md. Until the charter and the later genealogical reconstruction are reconciled, show the parent as disputed. The corrected chain from Bartes II.3 through Andreas II.11, Carsten II.21, Bernd II.39 and Christian II.60 remains source-stated; Bartez II.6 remains on Reimer's separate branch.
