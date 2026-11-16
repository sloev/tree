# Cooperation log — sloev/tree

Append-only coordination log for the Gårdsted / Gedde family-history project. Agents read the latest entries before starting and append a dated handoff on completion. Work only on main. Never expose private data. Treat data/build_data.py as source of truth.

---

## 2026-11-16 — Grok agent: inspection and null result

**Agent:** Grok (xAI)
**Task:** Read research_method.md, AGENTS.md, leads/README.md, and lead/tree-research.md; confirm branch policy; record status of open genealogical leads without accessing private data.
**Branch policy:** main only; no branches or PRs.
**Files inspected:** README.md, AGENTS.md, research_method.md (stub), leads/README.md, lead/tree-research.md, data/ (structure only).
**Files touched:** coop.log.md (this new file).

**Findings:**
- research_method.md is a 224-byte placeholder referencing a missing /tmp file; it does not contain the expected research method, milestones, or handoffs. Active instructions are in AGENTS.md and leads/README.md (four grandparent dossiers are the authoritative research workspace).
- Canonical data remains data/build_data.py / data/family.json. Private records stay encrypted in data/private.enc. No private data decrypted or inspected.
- Open public leads (from ledger and prior handoffs) include Dybbøl 18 September 1866 marriage image for Rasmus Jensen / Anne Christine Hansen (p52/p53), and Zedler inspection for earlier von Woyten. No new primary evidence located in this pass.
- Null result: no new genealogical facts, relationships, or sources added. No changes to build_data.py or family.json.

**Status:** Research method file requires restoration. Four grandparent dossiers remain the active workspace. No expansion this run.

**Unresolved / next concrete steps:**
1. Restore a complete research_method.md from repository history or local agent records if available.
2. Continue systematic retrieval of the Dybbøl Ab 4 1866 marriage image via Arkivalieronline for transcription.
3. Inspect Zedler vol. 59 “Woyden, Woyten” for exact statements on earlier von Woyten figures.
4. Do not modify canonical data without primary evidence meeting the evidence rule in lead/tree-research.md.

**Handoff:** Small commits on main only. Never expose private data. Repositories remain strictly separated from earlysmolweb.
