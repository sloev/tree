# Agent instructions — sloev/tree

## Project boundary (mandatory)
This repository is exclusively the Gårdsted and Gedde family-history project and its website.

- Work only on genealogy, family-tree data, source citations, family-history research, and this repository's website/build.
- Never import, copy, summarize, or publish material from `sloev/earlysmolweb` here. In particular, Iceland, UUCP, EUnet, networking history, and early Internet research belong exclusively in `sloev/earlysmolweb`. They must never appear in this repository's content, news bulletin, source lists, data, commits, or generated site unless the user explicitly changes this boundary.
- Do not use one repository's task list, notes, files, or research as context for work in the other. If a request is ambiguous, stop and ask which repository it concerns.
- Before editing, confirm the repository is `sloev/tree` and the branch is `main`. Work directly on `main`; do not create feature branches.
- Keep generated files consistent with their source files. Do not edit generated HTML as a substitute for editing its source template/data.
- Never claim a website is published or updated until the build/deployment has actually completed and been checked.

## Family-tree website requirements
- Mobile-first, responsive layout; never require horizontal panning to read or navigate the tree.
- Render the ancestry tree as a compact, single-column file explorer: one person per row, with depth shown by indentation and subtle vertical guide lines. Keep rows readable on desktop and touch-friendly on mobile.
- All known branches are expanded by default. Users may collapse/expand individual subtrees; persist those choices for the current browser session.
- Use the shared generation palette for row accents and indentation guides. Maternal and paternal people at the same depth share a colour; adjacent generations use distinct colours. Never require horizontal panning.
- Keep previous/next controls for other people at the same generation, ordered by ahnentafel position. Provide accessible tree keyboard navigation for visible rows and subtree expansion.
- Preserve the tree entry points (renderPed, setRoot, highlight, nodes) and ahnentafel indexing. Do not change genealogy data as part of presentation work.
- Use one shared, high-contrast generation colour for both maternal and paternal nodes at a given depth; make adjacent generations visually distinct. Do not use family-line colours as the primary node colour.
- Keep the home navigation item labelled "Forside" first.
- Preserve privacy protections for living people and private stubs. Do not decrypt or expose private data without explicit, scoped authorization.
- Keep the research bulletin strictly about the family tree and its genealogy research.
