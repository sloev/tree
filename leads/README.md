# Leads — research intake

**This folder is an intake and evidence workspace, not a second database.** Keep source scans, transcripts, research notes and candidate leads here while they are being assessed. Do not treat a dossier or file in this folder as canonical family data or as a direct website input.

The canonical, public-facing data lives in [\`data/tree.json\`](../data/tree.json). When a lead is sufficiently described for publication, ingest it there as:
- a person or relationship only when the evidence and confidence level justify it;
- a research claim when the question, evidence, uncertainty and next archival action should be visible on the website;
- source metadata or a note attached to the relevant person when it adds durable, traceable information.

The website build reads only \`data/tree.json\` plus its presentation templates and assets. Changes in this folder do not publish themselves and do not trigger a site rebuild. This separation prevents unfinished notes, duplicated claims and conflicting versions from silently becoming public data.


## Historiske dossierer

De fire filer nedenfor er bevaret som baggrund og kildeproveniens. De er ikke længere de aktive steder for åbne spørgsmål eller næste handlinger. Se forskningssporene i `data/tree.json` for den aktuelle, komplette registrering.

1. [Evald Johannes Gaardsted-Jørgensen](grandparent-evald-gaardsted-jorgensen.md)
2. [Liss Gaardsted-Jørgensen (født Pedersen)](grandparent-liss-pedersen.md)
3. [Lorenz Heinrich Frederiksen](grandparent-lorenz-frederiksen.md)
4. [Gerda Frederiksen (født Larsen)](grandparent-gerda-larsen.md)

## Regler for én sandhedskilde

- Hvert selvstændigt forskningsspørgsmål har ét forskningsspor i `data/tree.json`.
- Nye fund og opfølgninger føjes til det eksisterende spor, hvis spørgsmålet allerede findes; ellers oprettes et nyt spor.
- Registrér kildens ordlyd, kildeart, hvad den faktisk beviser, hvad den ikke beviser, kildekonflikter og negative søgninger direkte i sporet.
- Delte begivenheder krydsrefereres med eksisterende person-ID'er; undgå dublerede spor for samme spørgsmål.
- Juridiske/registrerede, biologiske, ægteskabelige, sted-, pleje-, værge- og husstandsrelationer holdes adskilt.
- En forskningspåstand opretter ikke automatisk en forældre-/barn-relation i stamtræet.
- Dossierer opdateres ikke parallelt. De bevares som historiske kilder og tidligere analyser.

## Canonical data and derived exports

- Canonical source: [`data/tree.json`](../data/tree.json).
- `data/family.json`, `data/research.json`, `data/map.json` and GEDCOM are generated projections. Do not edit them by hand.
- The legacy Python builder and intermediate input files are archived/retained for provenance only; they are not part of the active build.
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

## Forskningsspor — eneste aktive registrering

Forskningsfanen genereres fra `data/tree.json` (via `data/research.json`, som er en afledt fil). Det er her hele forskningsforløbet skal være forståeligt uden at åbne et separat dossier.

Når et spor oprettes eller opdateres, redigér `data/tree.json` og medtag så vidt muligt:
- unik `id`, `branch`, `title` og status (`needs`, `hypothesis`, `family` eller `conflict`);
- konkret påstand/spørgsmål, foreliggende belæg og kildeart;
- præcist hvad der mangler, og næste konkrete kontrol;
- stabile kildehenvisninger med forklarende etiketter;
- relevante `person_ids` og eventuelle relationer til andre spor.

Tilføj ny dokumentation til det eksisterende spor i stedet for at oprette en parallel note. Hold teksten tilstrækkelig fyldestgørende til, at offentligheden kan følge både fund og usikkerhed direkte på hjemmesiden. Opfind ikke forældre-/barn-relationer i stamtræet for at få et hypotetisk spor til at passe visuelt.

The site rebuild workflow regenerates the public research section after changes to the research register. Check the workflow and Pages deployment before describing a new lead as live.



## Forslag og arbejdsmateriale

Manuelle og automatiske ane-/søskendeforslag samt familiedokumenternes supplerende rettelser opbevares i `data/tree.json` under `ingestion`. Det er fortsat indbakke-/arbejdsmateriale, ikke publicerede slægtsdata. Brug værktøjerne i `tools/`; de skriver til denne del af den kanoniske fil. Kun en bevidst, kildeunderbygget godkendelse flytter oplysninger til `family` eller `research`.
