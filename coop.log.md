## 2026-11-16 — Frederik Christian III.727 death-record route

- Read current `research_method.md`, `leads/README.md`, `coop.log.md` and the Lorenz/Frederiksen dossier before research. Confirmed the project method: `main`, four active grandparent dossiers, evidence-status labels, no unsupported parentage edges.
- Followed the dossier's unresolved candidate match between Harbou's Frederik Christian III.727 (8 Jan 1775–21 May 1848) and the supplied “Christian Frederik Vilhelm” (1774–1848).
- Re-read Harbou's full entry and footnote 36. Harbou gives III.727's military career and death date, but no death locality in that entry; footnote 36 cites H. P. Selmer, `Nekrologiske Samlinger`, vol. II. Corrected the prior unsupported assumption that III.727 died at Bredsted: Harbou assigns Bredsted to his elder brother III.601, who died there in 1799.
- Identified relevant catalogue holdings at the Landeskirchliches Archiv Nordkirche / Archion: Bredstedt `Bestattungen 1831–1879` and index `Bredstedt_13`; Schleswig-Domgemeinde `Bestattungen 1823–1856` and burial-name index 1770–1874. Both cover 1848, but neither has yet been searched for III.727; catalogue entries are not proof of a burial. Archion images require access, and no original register image was inspected.
- Updated `leads/grandparent-lorenz-frederiksen.md` only; no canonical people, dates, relationships or edges changed. Commit: `9958e29140fc6d63b496a7022c1420500a0415f5` (https://github.com/sloev/tree/commit/9958e29140fc6d63b496a7022c1420500a0415f5).
- Validation: fetched the current source files and online source/catalogue pages; no local build, GEDCOM export, site build or browser test was run.
- Next action: inspect Selmer vol. II at Harbou's cited reference to establish locality/details, then inspect the appropriate 1848 burial index/register. If Selmer does not give a locality, test the Schleswig and Bredstedt indexes as bounded alternatives and corroborate identity by rank, family and residence. Keep the 1774–1848 supplied-person match speculative until independently corroborated.

## 2026-11-16 — Open research publication standard

The project owner clarified that research should remain visible on the public website while unresolved, so visitors can recognise details and contribute missing information. Agreed: the site is to function as an open research tree, not only a proven-facts tree. Unverified and competing claims should be visible with clear status and click-through explanations of provenance, evidence, limitations, missing records and concrete requests for help.

Updated:
- `research_method.md`: added the open-public-research standard, independent relationship-level statuses, public searchable research register requirements, contribution guidance, and a privacy/publication gate.
- `README.md`: added a public-facing explanation that credible unresolved leads should be published with explicit qualification and that visitors can contribute through Issues/PRs.

Important design requirements for the website implementation:
1. Visually distinguish established facts, claims needing evidence, hypotheses, family accounts, disputes and rejected leads. Do not rely on colour alone.
2. Clicking a person or relationship must explain the specific claim, source provenance, what it proves/does not prove, competing evidence, missing evidence and next check.
3. Represent relationships independently from person confidence; distinguish biological, legal/registered, step, adoptive, foster, guardian, household and marital ties. Never make a speculative biological link look settled.
4. Add a public research register with filters for person, place, family line, record type and status, plus actionable contribution requests and links to sources/history.
5. Publish reviewed public summaries from structured source data; do not expose unreviewed private dossier material or sensitive details about living people/informants.

This commit changes the publication policy and README only. The existing site already displays some person-level confidence and Lorenz's competing paternity claims in the person drawer, but it does not yet provide a complete structured public register of all four active dossiers, nor consistent click-through explanations for every uncertain relationship. Website implementation and audit remain outstanding. No canonical genealogy data changed. No local site build, GEDCOM export, browser test or deployment was run.

Commits: research method `dfbfb31136cf8406059d6a0e711357c192ee8ecc`; README `2340b5eb208addef9c0fb37a6065bc65094577d6`.

Next: design a structured, privacy-reviewed public research-claim dataset from the four active dossiers; wire it into a dedicated website research view and person/relationship drawers; then build and inspect the generated public output for privacy leaks and misleading edge styling.


## 16 November 2026 — first public research-register implementation

Implemented the first website-facing slice of the open-research policy:

- Added `data/research.json` as a separate structured, version-controlled register (eight initial claims across the four active grandparent dossiers).
- Added a `Forskningsspor` tab and public register view in `site/template.html`, with free-text search and status/branch filters.
- Each item visibly carries its uncertainty status and expands to show the claim, the evidence currently identified, what remains missing, the next research action, and a link to its active dossier.
- Added `site/build.py` injection for the structured research data.
- Added public contribution links to GitHub Issues and Pull Requests and a reminder not to publish sensitive information about living people.

The eight initial entries are a curated starting register, not a complete transcription of every note in all four dossiers. Some entries intentionally say that a source is identified but not yet inspected; do not upgrade them merely because they appear in the public register. Continue expanding the register from each active dossier, one claim at a time, with provenance and privacy review.

Validation performed: fetched the three changed files from `main`, parsed `data/research.json` as JSON, and checked that the tab, view, renderer, build placeholder and all four dossier links are present. A local Python site build, browser interaction test, deployment check and live-site inspection have **not** been run in this environment. Do not claim the public GitHub Pages site has changed until deployment is confirmed.


## 16 November 2026 — expand the public register and include source links

Expanded the structured public research register from 8 to **27 open claims**:
- Evald: 7 claims, including the 1764/1787 Rolsøgård probate, the separate 1820 Vibygård household, Rosmus identity conflict, Rousing parentage and Lovisa's missing mother.
- Liss: 6 claims, including Assing baptism, Kjersten's 1822 baptism, Hoven mill property context and Karen Jensen's date discrepancy.
- Gerda: 8 claims, including Kresten's possible mothers, Langø purchase/causeway, Iver Peder's 1910 contract, the 1787 probate and the reported family emigration.
- Lorenz: 6 claims, including the 1932 paternity file, Christian Adam's 1705 baptism, Frederik Christian III.727's 1848 death and the separate Kleist stem reconstructions.

Added curated source links to selected claims and a visible “Kilder og videre læsning” section in each expanded research card. Claims remain explicitly unresolved where the dossier says the original record has not been inspected; no canonical parent-child links or GEDCOM facts were changed.

Validation: JSON parses; 27 unique claim IDs; all entries point to one of the four active dossiers; all four branches and all three statuses are represented; the research tab/view/renderer, source-link UI and build injection are present. The automatic GitHub Actions rebuild for commit `a75e103` completed successfully and generated `docs/index.html`; the generated page was fetched from GitHub and checked for the tab, renderer, source section and newly added claim IDs. GitHub Pages deployment was still in progress at the time of this log entry.


## 16 November 2026 — person drawers linked to the public research register

Added claim-to-person references to 25 of the 27 public research entries (all referenced IDs checked against the 494 people in canonical `data/family.json`; no missing person IDs). Person drawers now show the relevant open research claims and a “Se belæg og hvad der mangler” control. Activating it closes the drawer, opens the research tab, expands that claim's evidence panel and scrolls it into view. Two broader branch-level claims remain available only in the register.

Validation: the main JavaScript function extracted from `site/template.html` passes JavaScript syntax compilation; the 27-record JSON parses; all claim IDs are unique; all dossier paths and person references resolve; the generated `docs/index.html` contains the tab, research renderer, source links, drawer claim controls and both later-added claim IDs. GitHub Actions rebuild completed successfully and the subsequent Pages build/deployment job completed successfully. The generated website output is committed by the workflow. This validates the build pipeline and Pages workflow; it is not a manual visual/browser usability review.

## 2026-11-16 — Grok agent: Dybbøl 1866 marriage null-result check

**Agent:** Grok (xAI)
**Task:** Follow previous handoff for the Dybbøl Ab 4 (Anne Christine Hansen / p53) 18 September 1866 marriage to Rasmus Jensen; perform bounded public-web and index search; record null result if no image or transcription appears.
**Branch policy:** main only; no branches or PRs.
**Files inspected:** research_method.md, leads/README.md, coop.log.md, leads/grandparent-lorenz-frederiksen.md (relevant sections on p52/p53).
**Files touched:** coop.log.md (this entry). No dossier or canonical data edited.

**Findings:**
- Bounded public-web searches (name + Dybbøl + 1866 + vielse/marriage variants, Arkivalieronline mentions) returned no index entry, transcription, or publicly accessible image of the 18 September 1866 Dybbøl marriage of Rasmus Jensen and Anne Christine Hansen.
- Earlier agent notes indicate the Arkivalieronline viewer can load the series index (Vielser 1723–1900) but systematic image paging for the specific entry has not yet been completed in this environment.
- Null result on publicly indexed sources. This does not prove the entry is absent; it remains a bounded negative search.

**Status:** No new evidence. No canonical people, dates, relationships or edges changed. Private/encrypted data not accessed.

**Unresolved / next concrete steps:**
1. Direct Arkivalieronline image retrieval and systematic paging of Dybbøl vielser series for 18 Sep 1866 (or nearest entries); transcribe if located.
2. If unavailable online, prepare precise archive enquiry to Rigsarkivet naming the persons, event, parish, date window and known references.
3. Alternative: rotate to another open lead in the Lorenz dossier (e.g., Selmer vol. II for Frederik Christian III.727 death locality, or 1932 paternity file).
4. Keep biological, legal and social parentage roles for Lorenz distinct.

**Handoff:** Small commits on main only. No private data exposed. Repositories remain strictly separated.
