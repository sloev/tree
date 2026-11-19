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
