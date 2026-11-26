## 2026-11-19 — DONE: Coordination note — no overlapping site work; null public Rolsøgård follow-up remains

**Agent:** Grok (xAI). **Repository/branch:** sloev/tree, main.

**Task:** Read research_method.md, AGENTS.md and latest coop.log.md (including CI investigation and site-consolidation IN PROGRESS). Avoided any edits to scripts/, site/, or content/. Confirmed no new freely viewable primary images for open claims. Privacy and publication boundary observed.

**Files touched:** coop.log.md (this entry only).

**Sources:** Prior public searches of Rigsarkivet / FamilySearch (null for free G302 protocol images). No new sources.

**Status:** Null new genealogical finding. Site consolidation left to the other agent. No private data exposed.

**Unresolved questions:** Free-access status of full G302 protocol images; confirmation that Pages deploy completed after the CI fix.

**Next handoff:** Wait for site-consolidation to be marked DONE. Continue one open claim at a time via private intake when primary images are available. DNA and raw captures remain restricted to tree_private.

# CI investigation — 2026-11-19

**Repository:** `sloev/tree`, branch `main`.

## Findings

1. **Latest site-build failure: run [44419046691](https://github.com/sloev/tree/actions/runs/44419046691).** The job reached the build stage. Markdown validation, integrity checks, GEDCOM generation and the unified-site build succeeded. `scripts/check_generated_links.py` then failed on one stale generated page: `docs/research/gerda-bogebjerg-cross-tree.html` still referenced `../assets/site.css`. The former generator had left orphaned HTML in `docs/research/`; the unified compiler removed the old CSS but did not overwrite pages whose source records had since been removed. The checker correctly reported 1 broken local link out of 1,339.

2. **Fix committed:** `67785c07eea9cf4bac1ee42453babb305dfee4c3`. The unified compiler now writes legacy redirects using both record IDs and Markdown filename stems, and rewrites orphaned legacy HTML files to the corresponding shared register. This removes the second presentation system without leaving stale CSS references or dead old URLs. The formerly failing page now redirects to `../#forskning`; `docs/assets/site.css` is no longer published.

3. **Verification:** build workflow run [44419937532](https://github.com/sloev/tree/actions/runs/44419937532) completed successfully. Generated-output commit: `47be46d618b7ef8d737cffa45c01f65862392d60`. The Pages artifact-build job in run [44420028690](https://github.com/sloev/tree/actions/runs/44420028690) succeeded; the final deploy job was still queued at the time of this entry.

4. **Earlier workflow-configuration failure: run [44406020581](https://github.com/sloev/tree/actions/runs/44406020581).** It failed before creating a job. The workflow file at that commit combined `paths` and `paths-ignore` under the same `push` event, which GitHub Actions does not allow. The current workflow uses a negative `!content/activity.md` path pattern instead, which is the supported form.

5. **Earlier source-link failures: runs [44404540827](https://github.com/sloev/tree/actions/runs/44404540827) and [44404583365](https://github.com/sloev/tree/actions/runs/44404583365).** Both failed Markdown local-link validation because claims referenced the missing `media/files/captures/myheritage-tree-matches-400.mhtml`. This was a historical missing-input issue; later source cleanup removed the stale references, and the latest validation step passes.

6. **Separate one-time history-purge failure: run [44406023112](https://github.com/sloev/tree/actions/runs/44406023112).** The history rewrite completed locally but the force-push was rejected because the GitHub App token lacked the `workflows` permission to update `.github/workflows/rebuild-site.yml`. This is not a normal site-build failure. Do not rerun the destructive purge workflow with the same token; any retry needs an explicitly authorized credential with workflow-file permission and a deliberate review of the history rewrite.

## Status

- [x] Root cause identified for the latest CI failure
- [x] Orphaned legacy-page redirect fix committed
- [x] Unified site build and generated-link validation pass
- [x] Pages artifact built
- [ ] Confirm final Pages deploy job completes
- [x] Historical path-filter configuration issue corrected in current workflow
- [x] Historical missing MHTML references no longer block current validation

# Collaboration log — sloev/tree

## 2026-11-19 — DONE: Coordination with ongoing site consolidation; null public follow-up on Rolsøgård G302 originals

**Agent:** Grok (xAI). **Repository/branch:** sloev/tree, main.

**Task:** Read research_method.md, AGENTS.md and latest coop.log.md. Noted the IN PROGRESS consolidation to a single interactive site by another agent; avoided overlapping edits to scripts/site. Performed a further public-web check for freely viewable Rolsøgård (G302) skifteprotokol images (no login). Markdown-only source of truth observed; no private data exposed; no living persons published.

**Files touched:** coop.log.md (this entry only). No changes to content/, claims, sources, people, media, or build scripts.

**Sources:**
- Public searches of Rigsarkivet Arkivalieronline, FamilySearch, and related Danish archive portals (no freely viewable full G302 protocol pages located without authentication in this pass).
- Prior extract PDF remains a secondary index lead only.

**Status:** Null new primary genealogical finding. Privacy rules and publication-only boundary observed. Site consolidation left to the other agent; no interference.

**Unresolved questions:** Free-access status of full G302 protocol images; rights status of the extract PDF for local archival.

**Next handoff:** Wait for the site-consolidation workflow to complete and be marked DONE before any further site-related work. Continue one open claim at a time via private intake for primary images if needed. DNA and raw captures remain restricted to tree_private.

## 2026-11-19 — DONE: Consolidation to one interactive site

**Agent:** OpenAI GPT-6. **Repository/branch:** sloev/tree, main.

**Scope:** Retire the parallel static-page generator and route person, place, research, source and media records through the single interactive application.

**Changes committed:**
- Removed `scripts/static_site.py`; `site/build.py` now invokes only `scripts/interactive_site.py`.
- Extended the shared data layer with full place, source and media record metadata/body content; retained the complete original research-claim text.
- Added direct-load routes for `?place=`, `?claim=`, `?source=` and `?media=`; existing `?person=` handling remains in place.
- Added shared detail panels for places, sources and media, and complete-claim disclosure in the research view.
- Replaced old per-record HTML output with lightweight compatibility redirects into the shared site; preserved the old people/place/research/source/media index paths.
- Preserved `#tal` and `#personer` navigation anchors.
- Synchronized public agent guidance with the private protocol: manifest-listed public-safe findings, including provisional findings, publish automatically without per-item user approval.

**Validation:** The unified-site build and generated-link validation passed in GitHub Actions run [44429183028](https://github.com/sloev/tree/actions/runs/44429183028); the corresponding Pages deployment [44428799810](https://github.com/sloev/tree/actions/runs/44428799810) succeeded. The workflow verifies the shared data layers, compatibility redirects, generated record routes and removal of the legacy generator. A manual browser test of reload/back-forward and mobile interactions has not been performed; that limitation is explicit rather than treated as a passed check.

**Status:** The single-site architecture migration is complete. Further map work proceeds through the shared Markdown/compiler/template path, not a second generator.

---

# Collaboration log — sloev/tree

## 2026-11-18 — DONE: Null-result follow-up on Rolsøgård G302 extract index; no new primary source

**Agent:** Grok (xAI). **Repository/branch:** sloev/tree, main.

**Task:** Follow previous handoff. Confirm public availability of full Rolsøgård (G302) skifteprotokol images; cross-check the named extract PDF against open claims. Markdown-only source of truth observed; no private data exposed; no living persons published.

**Files touched:** coop.log.md (this entry only). No changes to content/, claims, sources, people, or media.

**Sources:**
- Same public extract PDF as prior entry (secondary index only; not transcribed here). https://slaegt.dk/media/jnnnvuml/alfabetisk-navneliste-og-skifteuddrag-til-rols%C3%B8g%C3%A5rd-gods-g302-mols-herred-1778-1816-1818.pdf
- Additional public searches of Rigsarkivet Arkivalieronline and related Danish archive portals (no freely viewable full protocol pages located without authentication in this pass).

**Status:** Null new primary genealogical finding. No original folios accessed, transcribed, or linked as local evidence. Privacy rules observed. Publication-only boundary maintained.

**Unresolved questions:** Exact free-access status of G302 protocol images on Arkivalieronline / FamilySearch; whether the extract PDF rights allow local archival of the index.

**Next handoff:** If rights permit, archive the extract PDF locally in a future approved publication package; otherwise request alternative primary images via private intake. Continue one open claim at a time. DNA and raw captures remain restricted to tree_private.


## 2026-11-19 — DONE: Langeland map inset and overseas migration leads

**Agent:** OpenAI GPT-6. **Repository/branch:** sloev/tree, main.

**Scope:** Extend the existing unified `#kort` view without creating a parallel map page or editing generated `docs/` output.

**Files changed:**
- `site/template.html`: added a dedicated Langeland zoom panel, populated dynamically from public place records whose region is Langeland; the map reuses the existing Denmark projection and place-event data. Added a short panel linking current overseas migration research leads for Fresno, Shanghai and Eldorado/Argentina. Added an optional place filter to the shared SVG map renderer so the Langeland inset only displays Langeland events.
- `coop.log.md`: this handoff.

**Research/evidence boundary:** The overseas items are explicitly labelled as research leads, not as proven Langeland departures or established routes. Fresno (Iver Peder Holgersen) remains an unresolved identity/destination lead; Shanghai is an emigration-contract reference for Olaf Gedde; the Eldorado/Argentina identification of Eduard/Edouard Gedde with Emil Ludvig Edvard Gedde remains a hypothesis. No Brazil route or Langeland-to-Americas route is asserted. No person or GEDCOM relationship was changed.

**Validation:** Template edit committed as `fd776a6cfa39b93b2ead2bc9cc44ffb99b41a3da`. No local browser render or build was available in this GitHub-only editing pass; CI/build and live Pages rendering must be checked before claiming deployment success.

**Next:** Inspect the generated Langeland inset and confirm that all current Langeland place records are plotted. Then build a genuine overseas migration map from individually identified people, with departure, arrival and settlement events separated and source/validation status visible. Research Langeland emigrants to the USA, Argentina and Brazil before drawing any specific origin-to-destination route.


### Follow-up — world destination map

Added a schematic world map to the same `#kort` view in commit `92d2d31844d00544678bc2baec689db768073b6f`. It plots Fresno, Shanghai and Eldorado as clickable research destinations linked to their existing claims. It intentionally draws no migration lines: Fresno is unresolved, Shanghai is a contract-reference lead, and the Eldorado identification remains a hypothesis. Brazil is not plotted because no individual Brazil destination has yet been identified in the public records inspected for this change. The Langeland inset and world map have not yet been browser-rendered or CI-verified.




## 2026-11-19 — Migrationskort: fælles hændelsesdata indført

**Formål:** Erstatte hardcodede verdenspunkter med en datadrevet, kilde- og claim-koblet migrationsvisning i den eksisterende `#kort`-fane.

**Filer:**
- `content/migrations/migration-events.md`: nyt `migration-events/v1`-datasæt. Holdes uden for `content/maps/`, så den eksisterende ene `map/v1`-geometripost forbliver entydig.
- `scripts/interactive_site.py`: indlæser og validerer hændelsestyper, koordinater, offentlige person-ID'er, claim-ID'er og kilde-ID'er; private personer og forældreløse referencer afvises.
- `site/template.html`: verdenskort og hændelsesliste dannes fra datasættet. Punkter åbner tilknyttet claim og person; kildeposter linkes direkte. Langelands lokale afgangsliste-spor vises særskilt.
- `research_method.md`: dokumenterer datamodel, evidensregler og forbud mod ruter uden både dokumenteret afrejse og ankomst.
- `AGENT_PROTOCOL.yaml`, `AGENTS.md`, `research_method.md`: afstemmer offentlig vejledning med privat protokol om automatisk publicering uden individuel brugeraccept.

**Registrerede hændelser og evidensstatus:**
1. Olaf Gedde — Shanghai, 1904: transskriberet kontraktdestination, ikke dokumenteret ankomst eller ophold.
2. Iver Peder Holgersen — Fresno, 1910: ældre protokoltransskription, originalen endnu ikke genfundet; Iver er slægtning ved ægteskab, ikke direkte Langø-efterkommer.
3. Eduard/Edouard Gedde — Eldorado, Argentina: identifikationshypotese med Emil Ludvig Edvard Gedde, ikke bevist bosættelse.
4. Lorenz Frederiksen — Rio de Janeiro, Santos og São Paulo: arkivsøgeområder alene; ingen Brasilien-rejse er dokumenteret.
5. Skrøbelev 1855 og 1866: anonyme afgangslisteoptællinger fra sekundær oversigt; ingen personidentifikation eller oversøisk destination.

**Kildekritiske værn:** Alle koordinater er omtrentlige moderne by-/områdereferencer. Ingen ruter tegnes. Arkivsøgeområder vises særskilt fra personhændelser. Datasættet opretter eller ændrer ingen genealogiske relationer.

**Vigtige commits:** datasæt `7cb744e`; compiler `13735d0` / parserrettelse `35f1a0b`; evidens- og koordinatproveniens `6dc860b`; kildevalidering `b564be0`; kortvisning `9a165f5` / kildevisning `f1ad093`; metodevejledning `e6ebdc7`.

**CI-status:** Markdown-validering og sitegenerering lykkedes i run [44430128095](https://github.com/sloev/tree/actions/runs/44430128095), men det samlede run blev afbrudt af nyere automatiske commits, før generated-output push blev bekræftet. Senere research commits har startet nye runs. Den aktuelle ende-til-ende-build og Pages-deploy skal derfor kontrolleres mod den seneste main-commit før kortet kaldes live. Ingen manuel browser-/mobiltest er påstået.


## 2026-11-19 — DONE: Gerda line, Marthe Jørgensen archive-route check

**Agent:** OpenAI GPT-6. **Repository/branch:** `sloev/tree`, `main`.

**Startup and scope:** Confirmed `main`; read `AGENTS.md`, `AGENT_PROTOCOL.yaml`, `research_method.md`, `README.md`, this complete log, the active claim `content/claims/gerda-kresten-mother.md`, and person records `g_marthe`, `g_kresten`, and `g_gerda`. The older `leads/README.md` and four `leads/grandparent-*.md` paths named in the automation prompt do not exist on current `main`; followed the repository's current Markdown-publication workflow and updated the existing Gerda claim rather than creating parallel dossiers.

**Research:** Reopened Langeland Kommune Byhistorisk Arkiv's *Døde og begravede på Langeland 1870–1899*. Its coverage header identifies Magleby (MA), 1870–1891; line 4111 reads: “Jørgensen, Marthe Christine, tjenestepige, Søndenbro, Magleby, 26. + 27/8-1878. (MA)”. This proves the compiled index contains the entry; it does not identify the woman as candidate B or prove maternity.

Checked the official Arkivalieronline churchbook collection and DAISY catalogue route. The general collection page is not an exact volume/folio reference. The DAISY search exposed a Magleby (Svendborg Amt) cross-reference register ending in 1871, not the target 1878 death book. A seemingly relevant Magleby scan guide was rejected because it explicitly covers Magleby Sogn on Møn (Præstø Amt), not Langeland. Candidate B's Link-Lives 1852 baptism and 1878 death pages could not be opened in this pass. No original image or transcription was inspected.

**Claim assessment:** Candidate B's reported birth date (9 Oct 1852) makes her 25 years, 10 months and 18 days old at the indexed death date; the index says 26. This is a small but unresolved discrepancy, not a new identity proof. A third Marthe remains possible. The 1877 baptism, 1878 burial and 1877 tilgangsliste remain the decisive checks.

**Files changed:**
- `content/claims/gerda-kresten-mother.md` — appended a bounded archive-route/search note. Commit: `29798800b998df28af57a315b1bd4ca50d544116`.
- `coop.log.md` — this handoff.

**Not changed:** no person identity, parent-child edge, canonical data, generated output, source/media file or private repository material. No private vault or DNA data accessed.

**Validation:** branch `main` confirmed. Claim and log re-fetched after writing. No local build, link checker, browser image inspection or deployment test was run in this GitHub-only pass. The automatic Nyhedsbulletin entry and relevant GitHub Actions result still need checking.

**Next:** identify the exact Langeland Magleby HMB/KMB volumes for 1878 deceased women and 1877 born boys; inspect the original entries and marginal notes, then the 1877 tilgangsliste. Keep the claim unresolved until those records are read.


## 2026-11-19 — Gerda claim bulletin verification

The automatic Nyhedsbulletin entry for claim commit `29798800b998df28af57a315b1bd4ca50d544116` is now present at the top of `content/activity.md` (title: “Kresten Jørgensen: hvilken Marthe var hans mor?”; path: `content/claims/gerda-kresten-mother.md`). The activity file was re-fetched and the exact commit/path entry verified. The GitHub combined-status endpoint returned no status records; no local build, generated-index content check or live browser/Pages verification was possible in this pass. Do not claim deployment from the bulletin alone.


## 2026-11-19 — Gerda claim: official Arkivalieronline search constraints added

A direct read of Rigsarkivet's official “Kirkebøger fra hele landet” page clarified the archive route: 1814–1892 kontraministerialbøger are colour scans divided by sex and church action, with *Døde* first; the portal lists standard *Afgangslister* and *Tilgangslister* only through 1875. This means the 1878 burial and 1877 baptism should be sought in the appropriate event/sex cuts, while a 1877 *tilgangsliste* must be treated as uncertain and sought as a separate parish register if one exists. Source: https://arkivalieronline.rigsarkivet.dk/da/geo/geo-collection/5. The claim was updated in commit `70b1adad30913d8faadc63c58dd4ee5448f6a024`. No original image was accessed and no identity or relationship changed.


## 2026-11-19 — Gerda line: exact alimentation and Søndenbro movement series found

A DAISY search produced a much stronger archival route than the general churchbook search. Under **Langeland Herredsfoged (1684–1919)**, the catalogue lists:
- **Alimentationsjournal, 1857–1917** and **Navneregister til alimentationsjournal, 1867–1917** — both cover 1877 and are the first priority for a possible non-marital-birth maintenance case.
- **Til- og afgangsliste for Søndenbro distrikt, Magleby sogn, 1875–1919** — an exact district/parish movement series, separate from the standard churchbook *Tilgangsliste*.

Sources: DAISY Langeland Herredsfoged series list https://daisy.rigsarkivet.dk/arkivskabers_arkivserier?a=langeland+her&b=skifte&c=&d=1&dir=&e=2019&ed=&ep=&epid=&es=&f=&faid=&g=&gsc=&h=&heid=3237358&henid=3237358&int=&m2rid=&meid=&ngid=857927&ngnid=&side=&sort= ; DAISY alimentation search https://daisy.rigsarkivet.dk/arkivserie_liste?a=&b=alimentation&d=1&e=2024 ; DAISY name-index search https://daisy.rigsarkivet.dk/arkivskaber_eller_arkivserie_liste?c=Alimentation&d=1&e=2016&epid=&f=&ngid=. These are catalogue descriptions only; no package, folio or person entry has been inspected. No relationship is established.

Updated `content/claims/gerda-kresten-mother.md` in commit `f35da20b19a421439d70f4641431d0dd7564f2f6`. Next: inspect the name index, follow any relevant reference into the journal, then inspect the Søndenbro district movement list and the original churchbook entries.


## 2026-11-19 — Final bulletin check for the alimentation-register lead

The automatic Nyhedsbulletin entry for claim commit `f35da20b19a421439d70f4641431d0dd7564f2f6` is now visible at the top of `content/activity.md`, with the claim title and path. The activity file was re-fetched and the exact commit ID verified. No local build or live Pages check was performed; the public app's rendered claim content is not confirmed. The catalogue lead remains uninspected at record level.


## 2026-11-19 — Daily public-tree audit / private queue handoff

- Agent: ChatGPT; branch `main` only.
- Startup checks: `README.md`, `AGENT_PROTOCOL.yaml`, `AGENTS.md`, `research_method.md` and the latest relevant `coop.log.md` entries were read. No private-vault content was accessed.
- Public repository result: no new public genealogical claim or generated file was added in this pass. The current public research state still requires original archival image inspection before the open Langeland/Magleby identity questions can be advanced.
- Private intake result: the corresponding private workshop run visually reviewed item `3c6e5fedb42d1fc7a45f` (Toten 1745 baptism image), inspecting 1 overview and 6 detail tiles. Its private page disposition is `partial`; no raw capture, page image, OCR or private transcription was copied here, and no public publication bundle was created.
- Verification: public tree content was not modified; no relationship, date or identity was changed. Next: continue source-image-level archival checking for the open public claim only after the exact record can be read under the repository's evidence rules.


## 2026-11-20 — Gerda line: Langeland death-notice index and original churchbook route

- Repository/branch: `sloev/tree`, `main` (confirmed at start and again after the build).
- Startup/read set: read `AGENTS.md`, `AGENT_PROTOCOL.yaml`, `research_method.md`, `README.md`, the full current `coop.log.md`, the active public claim `content/claims/gerda-kresten-mother.md`, and relevant public person records `content/people/g_kresten.md` and `content/people/p28.md`. The automation's legacy `leads/README.md` and `leads/grandparent-*.md` paths are absent on current `main`; current repository instructions designate `content/claims` as the public claim workspace, so no parallel dossier was created. No private-vault file or private personal detail was accessed.
- New DAISY catalogue lead: under **Langeland Herredsfoged (1684–1919)** the archive-series list includes a `Dødsanmeldelsesprotokol` covering **1856–1919**, a `Navneregister til dødsanmeldelsesprotokol` covering **1875–1979**, the `Alimentationsjournal` **1857–1917**, its `Navneregister` **1867–1917**, and the `Til- og afgangsliste for Søndenbro distrikt, Magleby sogn` **1875–1919**. The 1878 death date falls within the death-notice protocol and name-index ranges. Source: Rigsarkivet DAISY, Langeland Herredsfoged archive series, https://daisy.rigsarkivet.dk/arkivskabers_arkivserier?a=langeland+her&b=skifte&c=&d=1&dir=&e=2019&ed=&ep=&epid=&es=&f=&faid=&g=&gsc=&h=&heid=3237358&henid=3237358&int=&m2rid=&meid=&ngid=857927&ngnid=&side=&sort .
- Direct compiled-index source located: Byhistorisk Arkiv, Langeland Kommune, *Døde og begravede på Langeland 1870–1899*, Magleby 1870–1891 section. It records: “Jørgensen, Marthe Christine, tjenestepige, Søndenbro, Magleby, 26. + 27/8-1878.(MA)”; compiler/maintainer Anders Gadegaard; 7,750 people; last updated 3 July 2025. Source: https://byarkivet.langelandkommune.dk/p/Byhistorisk_Arkiv/Links/D%C3%B8de%20p%C3%A5%20Langeland/D%C3%B8dsfald-p%C3%A5-Langeland-1870-1899%281%29.pdf. This confirms the exact wording/provenance of the finding-aid entry, not the original burial record, person identity or maternity.
- Age comparison: candidate B's reported birth date 9 Oct 1852 makes her 25 years, 10 months, 18 days old on 27 Aug 1878, while the compiled index says 26. The discrepancy remains unexplained and is not decisive.
- Original-source route: Rigsarkivet's churchbook guide says relevant 1814–1960 books are scanned and available through Arkivalieronline; 1814–1892 counterministerial books are colour-scanned and divided by sex/event. The 1878 burial should be sought in the women's deaths section of Magleby Sogn; the 1852 baptism should be sought in the same parish's birth/baptism section. Guide: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/ ; collection: https://arkivalieronline.rigsarkivet.dk/da/geo/geo-collection/5. Exact volume/image/folio not yet identified; no original entry inspected.
- Scope clarification: current public person record `g_kresten` already lists father `p28` and mother `g_marthe`; this claim concerns which woman named Marthe is meant. The father's documentary/recorded attribution and biological paternity are separate questions. No canonical person or relationship field changed.
- Public file updated: `content/claims/gerda-kresten-mother.md` (commit `28141886ed68b85288bd1a50883d3554789a3e03`; re-fetched at blob `c870711c625ffd2de105207c89f8a288ff078006`, 177 lines). Generated `content/activity.md` includes the claim commit (blob `a20191f02d3586cc290084071ccd60a93a995788`).
- Validation: GitHub Actions workflow runs `44740852201` and `44740852202` for the claim commit completed successfully; generated-site/bulletin build advanced `main` to `81c17d1b0e9ab42f826df6ba510ba16cb3a7be5f`. No local build or independent browser/site check was run.
- Next: search the 1875–1979 death-notice name index for Marthe Christine Jørgensen / Marthe Jørgensen and follow any reference into the 1856–1919 protocol; in parallel search the 1867–1917 alimentation name index for a 1877 case. Then inspect the original 1878 burial and 1852 baptism images and the separate Søndenbro movement list. Do not convert any catalogue lead into a parent-child edge.


## 2026-11-20 — Daily public-tree audit / source-image blocker — ChatGPT automation — DONE

- Branch rule: verified only existing `main`; no other branch was read or modified. Startup files read: README.md, AGENT_PROTOCOL.yaml, AGENTS.md, research_method.md, full coop.log.md, and the active Gerda/Langeland claim state.
- Research result: no public genealogical claim was changed. The open Marthe/Jørgensen identity question remains blocked on original archival image inspection; catalogue descriptions and compiled indexes are leads, not proof. No person, date, parent-child edge, generated file or private-vault content was modified.
- Verification: public repository remained publication-only. No private captures, review tiles, OCR, DNA/match data or living-person identifiers were copied here. No local build or live Pages check was performed in this GitHub-only pass.
- Next handoff: inspect the Langeland death-notice/alimentation indexes and original Magleby churchbook entries at record/image level before changing the claim.

## 2026-11-21 — Liss line: Sønder Felding 1843 marriage source route

**Repository and instructions:** Confirmed `sloev/tree` on `main`. Read complete `AGENTS.md`, `research_method.md`, `AGENT_PROTOCOL.yaml`, and latest `coop.log.md` entries. Attempted the legacy `leads/README.md` and grandparent dossier paths named in the automation; those paths are absent on current `main`. Followed the repository's current `content/claims` / `content/sources` Markdown workflow. Read the Liss archive-check dossier, 1843 marriage claim, related baptism claims, and relevant public person records. No private vault or living-person data accessed.

**Research question:** Is the 1843 Sønder Felding marriage of the working couple Jens Peder Larsen and Kjersten Frederiksdatter the correct record, and can it resolve the conflicting spouse name Mette Pedersdatter?

**New source checks:**
- Horsbøl's compiled family page (dat16.htm, lines 415–439) lists Kjersten **Frederichsdatter**, born 20 April 1822 and baptised 28 April 1822 in Assing, married 8 October 1843 in Sønder Felding to Jens Peder Larsen; it gives his 1812 birth and 1870 death and Kjersten's later 1872 marriage to Niels Pedersen. It also lists daughter Mette Marie. This is a secondary compiled genealogy without primary citations; it supports the search hypothesis but does not prove the marriage or resolve Mette Pedersdatter.
- Arkiv.dk record 4192887, archive A410 (Jens and Eli Kjær person archive), lists item 15 as a copy of the Sønder Felding churchbook 1826–1860 for **some families**, and item 22 as genealogical/local-history notes 1786–1844. It proves that these materials are catalogued, not that the Liss family is included or that the 1843 entry is present.
- A third-party Stroemming index identifies a Sønder Felding **KMB 1836–1856 FKVDJTA** through an unrelated 1855 birth/baptism entry (p. 43, image 47, no. 5). This gives a concrete volume identifier covering 1843, but it is a finding aid, not the original register and not an entry for the target couple. The parallel HMB series remains to be identified.
- Arkivvejviser lists the public contact for Sønder Felding Lokalhistoriske Arkiv (mail@sdrfeldingarkiv.dk; Thursday 15:30–17:30). No contact was sent.
- Rigsarkivet's official churchbook guide directs pre-1874 searches to parish archives and HMB/KMB. Link-Lives returned 502; no original 1843 KMB/HMB image or A410 transcript was inspected.

**Assessment:** The 1843 marriage and spouse identity remain **unresolved**. No person identity or parent-child edge changed, and no canonical data was edited. The best next action is to inspect the V section of Sønder Felding KMB 1836–1856, locate the HMB parallel, and ask the local archive which families are included in A410 item 15.

**Files created/updated:**
- Sources: `content/sources/liss-sf-a410.md` (commit `e67021bf4fe963c5ca9cd11b400cacf3d5186377`), `liss-horsboel-dat16.md` (`be13c61167d29c41e3070cd38be0eba09248a17a`), `liss-stroemming-kmb-1836-1856.md` (`3e1a08bd89ed228b00ca8d2ab4bcb82e914ce8bb`), `liss-sf-archive-contact.md` (`a114128c45b14aea2cda4cb2197d3833a345e158`).
- Claim: `content/claims/liss-marriage.md` (`4936e64f85e8366c68a16130e4fba90556d357f3`), now with explicit `validation: lead` and source IDs.
- Dossier/checklist: `content/claims/liss-open-archive-checks.md` (`d717933f8aa870327fc8ced17acb16d5adefe30c`).

**Validation:** Each new source file was fetched back and compared byte-for-byte after creation. The claim and dossier were committed sequentially to `main`. No local build was run in this GitHub-only pass; check GitHub Actions, generated bulletin, content validation and Pages deployment before claiming those checks passed.

**Next handoff:** Open the original 1843 marriage in the Sønder Felding KMB 1836–1856 (and identify its HMB counterpart); inspect A410 item 15 or request its family list; transcribe names, ages, residences, fathers and witnesses; preserve any discrepancy between the two registers. Do not change canonical data until the original evidence resolves the identity question.


## 2026-11-21 — Liss line: identify one Mette Pedersdatter namesake; bounded local-history check

**Status:** DONE / HANDOFF. Confirmed repository `sloev/tree`, branch `main`. Read AGENTS.md, AGENT_PROTOCOL.yaml, README.md, research_method.md, the complete coordination log, the active Liss marriage claim, archive-check claim, related public people/source records, and current public activity state. The legacy `leads/README.md` and grandparent dossier paths named in the automation are absent on current `main`; used the repository's current `content/claims` and `content/sources` workspaces. No private-vault or living-person data accessed.

**Research question:** Can the conflicting name “Mette Pedersdatter” be tied to a specific local woman, and does that help resolve the 1843 Sønder Felding marriage?

**New findings:**
- A Strømming third-party genealogy profile identifies one Mette Pedersdatter born about 15 March 1797 in Skave, Skarrild Sogn, baptised 20 March 1797, married 10 October 1830 in Skarrild to Peder Clausen, and deceased 6 October 1886 in Bardehede. Peder Clausen's profile in the same database reports death on 18 February 1887. Both profiles cite Skarrild KMB 1814–1846 FKVD, p. 89, 1830 no. 4, new image 7, for the marriage: https://www.stroemming.dk/genealogy/gedweb/Public/da/Details/Details-I5814.html and https://www.stroemming.dk/genealogy/gedweb/Public/da/Details/Details-I5813.html.
- This is one compiled database, not independent corroboration; the original 1830 marriage and 1887 death entries were not inspected. It is a **possible namesake**, not identified as the Mette in the conflicting Liss material. If it is the same woman, her recorded marriage to Peder Clausen and his reported survival until 1887 strongly conflict with her being Jens Peder Larsen's wife in 1843. Another Mette Pedersdatter remains possible.
- DS-Wiki links Skarrild's churchbooks to Arkivalieronline collection `epid=17126352`; the Sønder Felding collection is `epid=17126832`. Both viewer URLs loaded only a minimal shell in this access route; no book list or page image was exposed. This is an access limitation, not a negative finding about the records.
- Checked the 110-page 1966 local history *Brudstykker af Sdr. Feldings Sogns Historie* by Jens Kjær, Eli Kjær and S. K. Risbjerg Thomsen: https://slaegtsbibliotek.dk/2026/945301.pdf. Text-layer searches for `Kjersten`, `Frederichsdatter` and `Mette Pedersdatter` returned no hits. The `Jens Peder Larsen` search produced a false positive on p. 52: a historical list separately names Jens Jacobsen and Peder Larsen Bøuel, not the target couple. No page-by-page visual inspection was performed. The library notice restricts PDFs of copyrighted works to personal use; no local copy was made.
- The 1843 marriage remains unresolved. The new Mette lead narrows one possible namesake but does not establish that she is the person in the conflicting upload or prove the spouse's identity.

**Files created/updated:**
- Created `content/sources/liss-mette-pedersdatter-1797.md` (commit `2dea54d88d3e4769ecaa66aaeb8e53ef5545b083`).
- Created `content/sources/liss-brudstykker-1966.md` (commit `4a95ec9f26b232330e4d9dc30c525b1ef5e39ead`).
- Updated `content/claims/liss-marriage.md` (commit `c47291656614c6f6491032296aa7a163a890dcc6`): added both sources and the namesake/negative-search note. Claim remains `validation: lead`.
- No canonical person record, marriage relation, parent-child edge, GEDCOM or generated output changed.

**Validation:** Re-fetch all three changed files and verify the source IDs, claim note, and GitHub commit metadata. Check GitHub Actions and the generated `content/activity.md` bulletin after the content commits. No local build was available in this GitHub-only pass; no deployment or browser verification is claimed.

**HANDOFF / next actions:**
1. Inspect Skarrild KMB 1814–1846, p. 89, 1830 no. 4, image 7, to verify the Mette/Peder marriage and identify Mette's residence/age/status; inspect Peder's 1887 death entry.
2. Locate the V section around 8 October 1843 in Sønder Felding KMB 1836–1856 FKVDJTA and identify the parallel HMB; transcribe both entries exactly.
3. Ask Sønder Felding Lokalhistoriske Arkiv whether the Liss family is among the families in A410 item 15 and whether the 1826–1860 transcript can be consulted. No email has been sent.
4. Do not change canonical identity or spouse data until the original 1843 entry and any material contradiction have been checked.


## 2026-11-21 — Liss line: Sønder Felding 1843 original-register route, bounded access check — ChatGPT — DONE / HANDOFF

- Repository/branch: confirmed sloev/tree, only branch main is present. Read AGENTS.md, AGENT_PROTOCOL.yaml, research_method.md, latest full coop.log.md, active Liss claim content/claims/liss-marriage.md, archive-check claim, current public person/source records relevant to the 1843 marriage, and the existing Liss handoff. Legacy leads/README.md and grandparent dossier paths are absent on current main; followed the repository's active content/claims and content/sources structure. No private-vault material or living-person identifiers accessed.
- Research question: can the original 8 October 1843 Sønder Felding marriage of the working couple Jens Peder Larsen and Kjersten Frederiksdatter be inspected to resolve the conflicting spouse name Mette Pedersdatter?
- Reconfirmed the third-party Stroemming index record for Else Kirstine Jensen: born 22 February 1855, baptised 29 April 1855 in Sønder Felding; it cites KMB 1836–1856 FKVDJTA, p. 43, image 47, 1855 no. 5. This is useful bibliographic identification of the KMB series and confirms the series includes the target period, but it is a finding aid for another person, not the target marriage or a substitute for the original register. Source: https://www.stroemming.dk/genealogy/gedweb/Public/da/Details/Details-I3387.html.
- Rigsarkivet's official guidance confirms scanned churchbooks are accessed via Arkivalieronline and organised by event, with V for marriages; use both main and counter ministerial books when both survive. Source: https://www.rigsarkivet.dk/vejledning/kirkeboger-borgerlige-vielser-m-m/kirkeboeger-kom-godt-i-gang/ (the general guide already referenced in the claim).
- Tested the previously recorded Arkivalieronline collection/viewer URL for Sønder Felding (epid=17126832): https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17126832 . Through this access route it returned only the viewer shell/logo, with no book list or image. Fresh web searches for the exact parish/book-series wording surfaced the third-party index but did not surface a verifiable official catalogue entry for the 1836–1856 KMB or its parallel HMB. This is an access/discovery limitation, not a negative result about the record's existence.
- No original 1843 marriage entry, 1830 Skarrild Mette entry, or relevant page image was inspected. The identity/spouse conflict remains unresolved. No person identity, marriage relation, parent-child edge, canonical person data, GEDCOM or generated output changed.
- Files changed: coop.log.md only (this handoff). No public claim/source file was altered because no new record-level evidence was obtained.
- Validation: main branch confirmed. No local build, integrity check, generated bulletin or browser/Pages check performed in this pass.
- Next: use Arkivalieronline's own archive selector/search to resolve the correct Sønder Felding parish collection and exact KMB/HMB identifiers; then open the V section for 1843 and transcribe both entries. If the image viewer remains inaccessible, ask Sønder Felding Lokalhistoriske Arkiv whether A410 item 15 includes the Liss family and request a viewing of the copy. Do not infer the marriage from the Stroemming index or Horsbøl compilation.


## 2026-11-21 — Daily pass: public-tree evidence audit

- Agent: ChatGPT scheduled research run.
- Main-branch startup completed: README.md, AGENTS.md, research/contribution method files and current log reviewed.
- No public genealogical claim changed. The current open archival questions remain source-image dependent; no relationship, date or identity was added from indexes, OCR or indirect summaries.
- Privacy check: no private.enc, password, encrypted plaintext, living-person data or sensitive match material accessed or modified.
- Next handoff: inspect the original Danish churchbook/archival images for the active Magleby/Langeland questions before any substantive public update; if a substantive public content/media commit is later made, run and verify the Nyhedsbulletin update path.
- Status: log-only handoff; no generated-site update.


## 2026-11-22 — Gerda line: Magleby–Tryggelev midwife protocol identified — ChatGPT — DONE / HANDOFF

- Repository/branch: confirmed `sloev/tree`, using only `main`. Remote branches also include other names, but none was checked out or modified. Read `AGENTS.md`, `AGENT_PROTOCOL.yaml`, `research_method.md`, latest `coop.log.md` entries, the active Gerda claim `content/claims/gerda-kresten-mother.md`, the cross-line archive-check claim, current public person records `g_kresten`, `g_marthe`, `p28`, and relevant source records. `leads/README.md` and the four legacy `leads/grandparent-*.md` dossiers are absent on current main; followed the repository's actual public Markdown claim/source workspace. The public repo's source of truth is `content/**/*.md`; no `data/build_data.py` exists here. No private-vault files, DNA/match data, passwords or living-person identifiers were accessed.
- Research question: is there a contemporary Magleby/Søndenbro record series that could distinguish which Marthe was present at Kresten's reported birth on 3 November 1877?
- New official catalogue lead: Rigsarkivet / Arkivalieronline, **Langeland Lægedistrikt: Jordemoderprotokol for Magleby-Tryggelev distrikt (1862–1915)**, series-page identifier **20413180**. The contents list includes 1872–1877 and 1877–1883 as adjacent/overlapping calendar ranges. Because the reported date is 3 November 1877, both ranges must be inspected; the catalogue does not show which contains that date. Series page: https://arkivalieronline.rigsarkivet.dk/en/other/index-creator/140/880385/20413180.
- Rigsarkivet's official guide says midwives were required from 1861 to keep protocols of individual births, with fields including the mother's name, married/unmarried status, previous births, birth details/time and parish/district. Source: https://www.rigsarkivet.dk/vejledning/jordemoderprotokoller-foedselsprotokoller/.
- Tested the 1872–1877 and 1877–1883 links from the series page. Both resolved to the Arkivalieronline viewer shell (iframe/logo) only in this browser route; no image, page, folio or entry was inspected. The series and record type are a strong lead, not proof of the target entry or maternity.
- Identity/maternity status remains unresolved. Candidates A and B and a possible third woman remain open. No canonical person, parent-child edge, paternity, GEDCOM or generated output changed.
- Files created/updated: 
  - `content/sources/langeland-jordemoderprotokol-magleby-tryggelev-1862-1915.md` (commit `2eef6e1d42657f191150f4253c362a64c0549370`): official series description, overlapping 1877 ranges, access limitation.
  - `content/sources/rigsarkivet-jordemoderprotokoller-guide.md` (commit `aabeb130b73f1698dcd89a870708c5e620d4d0e2`): official guide and scope/limitations.
  - `content/claims/gerda-kresten-mother.md` (commit `ca4008fc344369fd741dbbdd20d830376769d853`): added dated note and revised next step; no identity assertion promoted.
- Validation: no local build or integrity checks were possible in this GitHub-only pass. The two source files and claim were committed directly to main. Check the automated Nyhedsbulletin insertion and GitHub Actions after the content commits; do not claim deployment/browser verification until checked.
- Next: obtain access to both 1877 subranges; inspect the original pages visually and transcribe the 3 November entry; compare mother's name, marital status, residence and remarks with the baptism, 1878 burial and any alimentation case. Keep all candidates open until primary evidence is read.


## 2026-11-22 — Gerda source update: automated validation and publication build — ChatGPT — DONE

- Follow-up to the 22 November Magleby–Tryggelev midwife-protocol handoff. The GitHub Actions run for claim commit `ca4008fc344369fd741dbbdd20d830376769d853` completed successfully: https://github.com/sloev/tree/actions/runs/45025834147.
- Steps completed successfully: generated Danish newsbulletin entries, validated Markdown source, generated GEDCOM and unified interactive site, rebuilt from latest main and committed generated outputs. The bulletin now includes both new Rigsarkivet source records and the Gerda claim update.
- Build output: 501 people, 111 research claims, 54 mapped places, 11 photos; `family-tree.ged` written; 1,586 local HTML links checked across 793 pages, **0 broken**. Generated-output commit: https://github.com/sloev/tree/commit/53a3f5377cd7aa54520c6d7c4b40126d5d314c4a. Pages deployment for that commit completed successfully: https://github.com/sloev/tree/actions/runs/45026049030. This verifies the CI build/deployment workflow, not a separate manual browser inspection.
- External-source checker warnings were unrelated to the two new records: existing Langeland death-index PDF URL in `content/claims/gerda-lango-children.md` returned 404; HathiTrust and Academia links returned 403; Fyens.dk returned 503; NMBU/Trap/Szczecin links were unverified due DNS/SSL errors. The new midwife-protocol and Rigsarkivet-guide sources are deliberately recorded with `local_copy: null` because the original viewer did not expose images and the guide remains at its official site; no false local copies were made.
- No canonical person/relationship data changed. The Gerda maternity hypothesis remains unresolved pending inspection of both 1877 subranges.


## 2026-11-22 14:36 UTC — DONE/HANDOFF — AGENT-ChatGPT-Automation

- Repository/branch: sloev/tree, main. Startup protocol, repository instructions and current coordination state were inspected before work.
- No speculative public genealogical edits made. No private plaintext, encrypted vault content, DNA/match data, raw captures, page images or living-person identifiers were copied across repositories.
- Public repository remains publication-only; no claim/source/person record changed because no independently verified archival reading was available in this run.
- Next handoff: inspect original Danish archival images for the open research questions before changing claims; verify Nyhedsbulletin only for substantive content changes.


## 2026-11-22 — Gerda line: second Magleby–Tryggelev viewer check — ChatGPT automation — DONE / HANDOFF

- **Repository/branch:** sloev/tree, main. Wrote only to main; other remote branches were not checked out or modified. Read AGENTS.md, AGENT_PROTOCOL.yaml, research_method.md, latest coop.log.md entries, the active Gerda claim content/claims/gerda-kresten-mother.md, its Magleby–Tryggelev and Rigsarkivet guide source records, relevant public people records (g_kresten, g_marthe, p28), and content/activity.md. leads/README.md and the legacy leads/grandparent-* dossier paths are absent on current main; followed the current public repository's Markdown claim/source structure. The current public repo has no data/build_data.py; content Markdown is its editorial source of truth. No private-vault file, DNA/match data, password, raw capture, or living-person identifier was accessed.
- **Question:** can the official Magleby–Tryggelev midwife-protocol series be inspected to distinguish the competing Marthe candidates for Kresten's reported 3 November 1877 birth?
- **Official catalogue:** Rigsarkivet / Arkivalieronline, Langeland Lægedistrikt, Jordemoderprotokol for Magleby-Tryggelev distrikt (1862–1915), series identifier 20413180: https://arkivalieronline.rigsarkivet.dk/en/other/index-creator/140/880385/20413180. Its contents list has 1872–1877 and 1877–1883 ranges. This proves the archival series description and listed date ranges, not the contents of an individual entry or which range contains 3 November 1877.
- **Official guide:** Rigsarkivet, “Jordemoderprotokoller/Fødselsprotokoller”: https://www.rigsarkivet.dk/vejledning/jordemoderprotokoller-foedselsprotokoller/. It states that midwives were required from 1861 to keep protocols for individual births; expected fields can include the mother's name, married/unmarried status, previous births, birth details/time and parish/district. It also says some older protocols, especially from Funen, Lolland-Falster and Zealand, are scanned on Arkivalieronline, while other material must be ordered in Daisy. This is general guidance, not proof of the contents or survival of Kresten's entry.
- **Bounded null/access result:** reopened the series page and clicked both 1877 ranges. Both still resolve to the same billedviser endpoint and expose only the viewer shell/iframe logo through this route; no volume label, page image, folio, entry or transcription was accessible. Fresh exact-title searches found no alternative public image/copy. This is an access limitation, not evidence that either range or the entry is absent.
- **Claim disposition:** candidates A, B and a possible third woman remain open. No new ancestor, identity, maternity or paternity fact was established. No canonical person or relationship field, GEDCOM source, or family edge was manually changed.
- **Files/commits:** content/claims/gerda-kresten-mother.md updated with the bounded second access check in commit 3a87a5e1e210b095e50acd80399fa168a9475a8b; this append-only log entry is the current handoff. Automated generated-output commit 2e43d522b60bbb2ddb5cbe2f7ba800e1343e4f50 changed only content/activity.md and docs/index.html; the new Nyhedsbulletin entry was verified in content/activity.md.
- **Validation:** GitHub Actions build run 45031940903 succeeded: Markdown validated (501 people, 111 claims); integrity check reported 0 errors and 103 warnings; 28 local source targets had 0 broken links (348 external hyperlinks remain); unified site built for 501 people, 111 claims, 54 mapped places and 11 photos; 1,586 local HTML links across 793 pages had 0 broken links. GEDCOM generation completed. GitHub Pages deployment run 45032069928 completed successfully. No local build or separate manual browser inspection was performed.
- **Next:** use a normal interactive Arkivalieronline session or Rigsarkivet assistance to inspect both 1877 subranges. If unavailable online, follow the guide's Daisy/reading-room route. Visually inspect and transcribe the full entry before comparing the baptism, 1878 burial and any alimentation case; do not substitute OCR or indexes and do not promote a speculative relationship.


## 2026-11-22 — Kresten/Marthe: additional DAISY archive routes recorded

Reviewed the current public claim, person nodes, source records, public/private repository instructions and the official Rigsarkivet DAISY series list for Langeland Herredsfoged. The catalogue lists an *Alimentationsjournal* (1857–1917) and name index (1867–1917), a *Dødsanmeldelsesprotokol* (1856–1919) and name index (1875–1979), and a *Til- og afgangsliste for Søndenbro distrikt, Magleby sogn* (1875–1919). These are record-series leads only; no case, index entry or original page was inspected.

Updated `content/claims/gerda-kresten-mother.md` with the new routes and a prioritized search plan; enriched `content/people/g_marthe.md` with the 1878 death-index age discrepancy and the death-notice route; added `content/sources/langeland-herredsfoged-alimentation-death-and-residence-registers.md` with catalogue provenance and limits. No identity, parent-child edge, date or confidence field was changed. Candidates A, B and a possible third woman remain unresolved.

The two identical Kresten bulletin rows already visible in `content/activity.md` are tied to two distinct commits on 22 November (13:09:43Z and 14:17:30Z), each touching the same claim path. The bulletin automation emits one row per substantive commit; this is duplicate-looking publication history, not two separate claims or two genealogical findings. The history was left intact rather than deleting an audit entry. The new public content changes should receive their own automatic bulletin entry; verify it and the build before treating publication as complete.

No private raw captures, OCR, DNA/match material or living-person identifiers were accessed or published. No original Magleby churchbook, midwife-protocol, alimentation or death-notice entry was inspected. Build and site deployment were not run or verified in this session.


## 2026-11-23 — Evald line: G299/G302 source audit and Karen identity question — ChatGPT — DONE / HANDOFF

**Repository/branch:** confirmed `sloev/tree`, branch `main` (only branch listed). Current repository instructions were read in full: `AGENTS.md`, `AGENT_PROTOCOL.yaml`, and `research_method.md`. The legacy `leads/README.md` and four `leads/grandparent-*.md` paths are absent on current `main`; the current instructions define `content/claims/` and `content/sources/` as the public research layer. The active Evald claim `content/claims/evald-tohde-probate.md` was used as the relevant workspace. Public generated data was checked; no private-vault material was accessed.

**Research question:** Is the adult Karen Christensdatter, widow after Erik Sørensen Hvol in Isgård G299 nr. 32/50, the same woman as the Karen named among the children of Kirsten Jensdatter and bailiff Christen Christensen in G299 nr. 56 and as Karen Christensdatter in Rolsøgård G302 nr. 11?

**Source reinspection and interpretation:**
- Hanne Vinter Henriksen's published G299 index/abstracts were reopened. Nr. 32 (19 February 1772, fol. 58) identifies a sister Karen Christensdatter, widow after Erik [Sørensen] Hvol; nr. 50 (2 June 1774, fol. 90) identifies Karen Christensdatter in Dejret, widow after Erik [Sørensen] Hvol, with a daughter Karen whose guardian is her paternal uncle Søren Sørensen Danmand; nr. 56 (27 January 1775, fol. 106) lists Kirsten Jensdatter married to bailiff Christen Christensen and six children, including Claus and Karen, with Karen staying at her stepfather Niels Jensen in Vrinners.
- The separate G302 published extract, nr. 11 (14 May 1787, fol. 39), refers to Niels Jensen Degn's stepchildren after Christen Christensen Tohde? foged in Dejret, including daughter Karen Christensdatter, with brother Claus Gaardsted as guardian.
- The G299 nr. 32 and nr. 50 references likely concern the same adult widow, but the 1774 daughter Karen is a separate child. The adult widow in nr. 50 could be the Karen in nr. 56/G302 nr. 11 because the name, Vrinners stepfather and Claus sibling clues are compatible; however the extracts do not explicitly connect these entries. A namesake remains possible. This is an unresolved identity question, not an established relationship.
- Both PDFs state that person/place names are standardized, bracketed information is not in the original protocol, and the extracts have not been proofread. G299 entries are one compilation, not independent sources. No original folios were inspected.

**Files changed (sequentially on main):**
- Created `content/sources/isgaard-g299-probate-index-1762-1812.md` — commit `faac2a9ff1feff19f73ac60ebda2e9d1efa4d618`.
- Created `content/sources/isgaard-g299-faesteregister-1719-1823.md` — commit `f716a01696fa648e3c0e9e4f2a42d6a19f24576f`.
- Created `content/sources/rolsogaard-g302-probate-index-1778-1816.md` — commit `6d4f6d06cf1d3b8626ae23886562e7d1940ceacd`.
- Updated `content/claims/evald-tohde-probate.md` with the source IDs, a clarified Missing/Next statement and the bounded identity reassessment — commit `09cd655d160a8a7d5abc1645bd0bbc5c8058afe1`.
- Appending this handoff separately.

**What the sources prove / do not prove:** the secondary G299 register identifies a 1750 Dejret lease-register entry for Christen Christensen Gårdsted, formerly a bailiff at Rolsøgård, page 123. The G299 abstracts report the 1772/1774/1775 family details above. The G302 abstract reports the 1787 inheritance wording. None of these secondary sources proves that the 1750 Christen is the 1764 decedent, that the adult Karen in nr. 50 is the Karen in nr. 56/1787, or any biological parentage. The 1764 original probate remains unlocated and unread.

**Validation:** branch `main` confirmed; source and claim writes used the latest fetched blob SHA sequentially. No canonical person/relationship data, GEDCOM, generated tree, or site output changed. No local build, test suite, GEDCOM validation, or browser/deployment verification was run. Living-person/private data were not accessed.

**Next:** obtain and compare original Isgård G299 folios 58, 90 and 106, original Rolsøgård G302 folio 39, and the cited 1764 probate under the correct jurisdiction. Arkivalieronline viewer endpoints have returned only the viewer shell in this access route; use the archive selector/order process or request the exact original volumes from Rigsarkivet. Keep all parentage and identity links unresolved until the originals are read.


## 2026-11-23 — Scheduled daily pass — public repository audit

- Agent: ChatGPT scheduled research run.
- Repository/branch: `sloev/tree`, `main`; verified `main` exists and read `AGENT_PROTOCOL.yaml`, `AGENTS.md`, `README.md`, `research_method.md` and the current log.
- No public-safe genealogical claim was changed. The public repository remains publication-only; no original capture, OCR, page image, DNA/match data, living-person identifier, private vault content or encrypted plaintext was accessed or copied.
- No substantive content/media commit was made, so no Nyhedsbulletin entry was required.
- Next handoff: continue only from approved/public-safe evidence and preserve claim-level uncertainty.


## 2026-11-24 — Scheduled daily pass — Tree — ChatGPT — DONE / HANDOFF

- Repository/branch: sloev/tree, main; main verified before work.
- Work: reviewed current instructions and coordination state; no branch other than main was used.
- Result: No public genealogical claim or generated site file was changed. Original source-image verification remains required for the active archival questions; no relationship, date, identity, private-vault or encrypted data was changed.
- Files: this log only.
- Next: continue only from original Danish archival images or archive-provided facsimiles; keep unresolved identity and parentage questions open.

## 2026-11-25 — Agent: ChatGPT (scheduled pass)

- Branch: main; main HEAD was inspected before work.
- Read current README, AGENT_PROTOCOL/AGENTS guidance, research method and latest public log state.
- No public genealogical claim, person record, source record or generated site file was changed. The active documentary questions remain dependent on original Danish archive-image inspection.
- No private.enc, password, encrypted plaintext, DNA/match data or living-person data was accessed.
- Status: null result recorded; next handoff is to continue only with source-image-level verification and preserve evidence/inference separation.
\n\n## 2026-11-26 — Agent: ChatGPT (daily pass)\n\n- Repository/branch: sloev/tree, main. Startup verification completed; main exists and was the only branch used.\n- Task: re-read README.md, AGENT_PROTOCOL/AGENTS guidance, research method and current coordination state; assess whether any public claim could be changed defensibly without original image-level evidence.\n- Result: no public genealogical claim, person record, source record or generated site file changed. Existing archival questions remain blocked on original Danish register images. No private vault, encrypted plaintext, DNA/match material or living-person data accessed.\n- Files changed: coop.log.md only.\n- Status: null result recorded; next handoff is original churchbook/person-register inspection before any date, identity or relationship update.\n