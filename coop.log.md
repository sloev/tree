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
