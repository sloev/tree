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

## 2026-11-19 — IN PROGRESS: Consolidation to one interactive site

**Agent:** OpenAI GPT-6. **Repository/branch:** sloev/tree, main.

**Scope:** Retire the parallel static-page generator and route person, place, research, source and media records through the single interactive application.

**Changes committed:**
- Removed `scripts/static_site.py`; `site/build.py` now invokes only `scripts/interactive_site.py`.
- Extended the shared data layer with full place, source and media record metadata/body content; retained the complete original research-claim text.
- Added direct-load routes for `?place=`, `?claim=`, `?source=` and `?media=`; existing `?person=` handling remains in place.
- Added shared detail panels for places, sources and media, and complete-claim disclosure in the research view.
- Replaced old per-record HTML output with lightweight compatibility redirects into the shared site; preserved the old people/place/research/source/media index paths.
- Updated README, content README, research method and the build workflow to enforce the single-template architecture.

**Validation status:** The updated GitHub Actions build and Pages deployment have been triggered, but are still queued/pending at this handoff. No successful build, generated-link check, browser interaction test or live deployment is claimed yet. The workflow now checks that the legacy generator is absent and that all record data layers/routes are present.

**Remaining checks:** Confirm the latest build run completes; inspect any failures and fix them; confirm generated redirects and local media copies; verify direct links and reload/back-forward behavior for all five record types plus `#tal` and `#personer`; confirm Pages deployment. Only then mark this migration DONE.

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
