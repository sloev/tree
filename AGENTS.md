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
- The homepage tree is a continuous, non-collapsible hierarchy. Keep every known branch visible; do not introduce accordions, disclosure toggles, or hidden ancestry branches.
- On wide screens, present the hierarchy compactly from left to right, with generations forming successive columns. On narrow/mobile screens, reflow it into a compact vertical hierarchy so the complete tree remains accessible without horizontal panning.
- Left/right keyboard navigation moves through every person in the currently displayed tree at the same generation, in left-to-right order, and wraps at both ends.
- Use one shared, high-contrast generation colour for both maternal and paternal nodes at a given depth; make adjacent generations visually distinct. Do not use family-line colours as the primary node colour.
- Keep the home navigation item labelled "Forside" first.
- Preserve privacy protections for living people and private stubs. Do not decrypt or expose private data without explicit, scoped authorization.
- Keep the research bulletin strictly about the family tree and its genealogy research.
