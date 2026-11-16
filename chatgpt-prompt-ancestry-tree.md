# Prompt for ChatGPT — Rebuild the ancestry tree as an ultra-compact "file tree"

Copy everything below the line into ChatGPT.

---

## Context

I have a static genealogy site hosted on GitHub Pages (`https://sloev.github.io/tree`). The whole site is a **single self-contained `index.html`** with inline `<style>` and `<script>` — no build step, no framework, no React/Vue, just vanilla JS + CSS. The repo is `github.com/sloev/tree`.

One section, the "Stamtræ" (ancestry tree), currently renders as a tree of **196px-wide cards** with colored left borders, generation labels, up/down nav buttons, and connecting lines. On desktop it scrolls horizontally; on mobile it stacks vertically. It works, but it is **visually noisy, takes too much space, and feels nothing like a tree**. I want it rebuilt.

## What I want — an "IDE file tree" look

Rebuild the Stamträ so it looks and behaves like the file explorer in VS Code / Sublime / JetBrains: **one person per line, ultra-compact, indented by depth, with clear visual hierarchy.** Concretely:

1. **One node = one line.** No more cards. Each person is a single row roughly 26–30px tall on desktop, ~36px on mobile. The whole tree should fit comfortably in a viewport without zooming out.
2. **Depth shown by indentation**, exactly like a file tree. Each level is indented by a fixed step (≈18–22px). Draw a faint vertical guide line at each indent level (1px, low-contrast) so the eye can follow the structure — the classic file-tree gutter.
3. **Every depth level gets its own color.** Use the existing `generationPalette` array (`['#2563eb','#ea580c','#059669','#c026d3','#ca8a04','#0891b2','#dc2626','#4f46e5']`) and cycle it by depth. Show the color as:
   - a 3px-wide left stripe on the row (or a small colored chevron / dot at the start of the line), AND
   - the color of the indentation guide line at that level.
4. **Each line must be visually distinct.** Subtle 1px bottom border between rows in `--rule` color, and a very faint zebra stripe (`--hover`) on every other row. The hovered row gets a stronger `--hover` background. The selected/`sel` row gets a 2px `--gen-color` outline that hugs the row.
5. **Per-node collapse/expand.** Like file folders: if a node has parents (children in the tree), show a small chevron `▸`/`▾` (or `+`/`−`) at the far left of the row. Clicking it collapses/expands that subtree. Persist collapse state in `sessionStorage` keyed by ahnentafel number. A node with no parents shows no chevron, just an empty spacer of the same width so the name column stays aligned.
6. **Per-node up/down navigation between peers in the same generation.** Keep the existing `moveInGeneration(delta)` logic. At the **right edge of each row**, render two compact buttons `↑` and `↓` (≈24×24px, ghost style, only colored on hover/focus with the row's `--gen-color`). They move focus to the previous/next person at the same `aria-level` and call the existing `highlight(id)`. On mobile, keep them tappable (min 32×32px tap target via padding, visual size can stay small).
7. **Keyboard navigation, like a real file tree:**
   - `↑` / `↓` → previous/next *visible* row (depth-first order).
   - `←` → collapse current subtree if expanded; otherwise move to parent.
   - `→` → expand current subtree if collapsed; otherwise move to first parent.
   - `Enter` → `openPerson(id)` (open the detail panel).
   - `PageUp` / `PageDown` / `Home` / `End` → jump as expected.
   - Keep `role="tree"`, `role="treeitem"`, `aria-level`, `aria-expanded`, `aria-keyshortcuts`. Update them so they reflect the file-tree semantics.

## Row layout (desktop)

A single horizontal flex row, left to right:

```
[chevron] [gen color stripe] [indent gutter with guide lines] [name] — [years] · [birthplace]   [↑] [↓]
```

- `chevron`: 16px, muted, becomes `--ink` when the row is focused.
- `gen color stripe`: 3px tall full-height bar in `--gen-color`. Or, alternatively, a 8px round dot in `--gen-color` — pick whichever reads better at this density.
- `indent gutter`: width = `depth * indent-step`. Inside it, one vertical 1px guide line per ancestor level, colored with that level's `generationPalette` color at ~35% opacity.
- `name`: bold, `--f-body`, single line, `text-overflow: ellipsis` if it overflows. Sex shown as a tiny colored dot after the name (keep existing `sex-f`/`sex-m` styling).
- `years`: `--f-data` (IBM Plex Mono), `--ink-2`, format `1857–1914` (keep existing `life(p)` helper).
- `birthplace`: `--muted`, smaller, ellipsis on overflow.
- `↑`/`↓`: right-aligned, ghost buttons.

If a person is unknown (`!p` / `!['record','told'].includes(p.conf)`), render the row but **dashed** the gen-color stripe and italicize/mute the name (currently the `unknown`/`uncertain` classes do this — keep that behavior).

## Row layout (mobile, ≤640px)

Same row, but:
- Drop the birthplace to a second line (smaller, muted) only when there is room; otherwise hide it behind a long-press / info affordance. The name + years must always stay on line 1.
- Chevrons and ↑/↓ stay — they are essential for navigation on a small screen.
- Up the row height to ~36px so tap targets are comfortable.
- The whole tree scrolls **vertically only** (no horizontal scroll). Let long names ellipsis-truncate.

## Hard constraints — do NOT break these

- **Do not touch the data model.** The tree is built from a global `ahn[]` array using **ahnentafel** indexing: root = index `1`, father of `n` = `2n`, mother of `n` = `2n+1`. Each entry is a person object `p` with at least `p.id`, `p.name`, `p.sex`, `p.bplace`, `p.conf`, `p.living`. Unknown slots are `undefined` and render as "Ukendt far" / "Ukendt mor".
- **Keep the entry points** the rest of the page depends on:
  - `renderPed(root)` — rebuild the tree starting at ahnentafel index `root`.
  - `setRoot(r)` — switches root between "Hele træet" / "Fars side" / "Mors side".
  - `highlight(id)` — selects a person's row by id; called from elsewhere on the page.
  - `nodes` object (id → row element) — other code reads it; keep it populated, but now it maps to row elements instead of card elements.
  - `pedRoot` variable.
  - The `[data-root]` buttons (`Hele træet` / `Fars side` / `Mors side`) must still work.
  - The `#pedcount` element must still show `"N personer · op til N generationer · alle kendte grene vist"`.
- **Keep all existing CSS custom properties and fonts** (`--paper`, `--sheet`, `--ink`, `--ink-2`, `--muted`, `--rule`, `--rule-2`, `--accent`, `--hover`, `--f-display`, `--f-body`, `--f-data`, dark-mode overrides). Reuse them; only add new ones prefixed with `--ft-*` (file-tree).
- **Keep the existing lineage color system** (`--l-jorgensen`, `--l-gaardsted`, `--l-rousing`, `--l-frederiksen`, `--l-gedde`, `--l-larsen`, `--l-maternal`, `--l-self`) — the rest of the site uses it. The file-tree's per-level colors come from `generationPalette`, not from lineage; that's fine and is what the current code already does.
- **Keep the container markup** `<div class="ped-scroll" id="pedscroll"><div id="ped" class="ped-tree" role="tree" aria-label="Slægtens anetræ"></div></div>`. You may replace its inner contents and the CSS, but not these IDs / roles.
- **Keep Danish for all user-facing strings** (`Forrige person i samme generation`, `Næste person i generationen`, `Ukendt far`, `Ukendt mor`, etc.). The page is Danish; do not translate to English.
- **No external dependencies.** No npm, no CDN, no Tailwind, no framework. Pure CSS + vanilla JS, inline in `index.html`.
- **Accessibility:** keep `role="tree"`, `role="treeitem"`, `aria-level`, `aria-expanded`, `aria-keyshortcuts`, `aria-label`. Make sure focus is visible (existing `:focus-visible` outline in `--accent`). Buttons need `type="button"`.
- **Performance:** the tree can have ~150 visible nodes when fully expanded. Rendering must stay under one frame on a mid-range laptop. Avoid layout thrash.

## Files / sections to change

You are editing a single file. Inside `index.html`:

- The CSS block between the `/* stamtræ */` comment and the next section. **Remove** the old card-based CSS (`.ped-card`, `.ped-card-top`, `.ped-nav`, `.ped-name`, `.ped-meta`, `.ped-place`, `.ped-status`, `.ped-dot`, `.ped-children`, `.ped-branch:before` rules) and replace with the new file-tree CSS. Keep `.ped-scroll`, `.ped-tree`, `.homepage-tree` (container) rules, just adjust as needed.
- The `renderPed(root)` function and its inner `branch(n, depth)` closure (currently around line 665–711). Rewrite it to emit file-tree rows. Keep the `generationNodes` peer-tracking logic — it's what powers ↑/↓ nav.
- The `fitPedTree()` function — on desktop the tree now flows vertically, so the `transform: scale` / fit logic can be deleted; the scroll container just scrolls vertically. On mobile, same.
- Add a `keyShortcuts`/keyboard handler at the tree level (delegated to `#ped`) implementing the file-tree keyboard model described above.

You can keep the rest of the file untouched.

## Deliverable

Return the **full updated `index.html`** — do not give me diffs, give me the whole file so I can drop it in. Make sure:

- It still passes a basic `html` validator.
- The other sections of the page (Forside, Nyheder, Personer, Kort, Tal og levetider, Kilder og billeder) still render and function.
- Dark mode still works.
- Mobile layout (≤640px) is genuinely usable: no horizontal scroll inside the tree, tap targets ≥32px, chevrons and ↑/↓ visible.

## Acceptance criteria (self-check before returning)

1. With "Hele træet" selected and nothing collapsed, the tree shows ~150 rows in a single vertical column inside `#pedscroll`. No horizontal scrollbar appears on desktop at 1280px width.
2. Each row is one line, ≤30px tall on desktop, ≤36px on mobile.
3. Depth is visible via indentation, and each indent level has its own colored guide line.
4. Each row's left stripe (or dot) is colored by `generationPalette[depth % 8]`.
5. Clicking `▸` on a row collapses its subtree; clicking again expands it. State survives a page reload via `sessionStorage`.
6. Clicking a name opens the person detail panel (calls `openPerson(id)`).
7. `↑`/`↓` buttons at the right of each row move focus between peers at the same `aria-level` and call `highlight(id)`.
8. Keyboard: `↑/↓` moves between visible rows, `←/→` collapses/expands, `Enter` opens the person. Focus ring is visible.
9. Switching between `Hele træet` / `Fars side` / `Mors side` rebuilds the tree correctly and resets scroll to top.
10. `#pedcount` still reads e.g. `"157 personer · op til 14 generationer · alle kendte grene vist"`.
11. Dark mode (both `prefers-color-scheme: dark` and `data-theme="dark"`) renders cleanly.
12. Lighthouse accessibility score on the Stamträ section stays ≥95.

If anything is ambiguous, pick the option that is closer to the VS Code file-explorer look and tell me what you chose.
