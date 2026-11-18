# Content — Markdown source of truth

Alt indhold, der vises på hjemmesiden eller eksporteres til GEDCOM, vedligeholdes her som Markdown. Binære filer ligger i images/ eller media/files/.

    python3 -m pip install -r requirements.txt
    python3 scripts/compile_content.py --check
    python3 scripts/compile_content.py
    python3 site/build.py

## Schemas

| Path | Schema | Purpose |
|---|---|---|
| people/<id>.md | person/v1 | One person; stable id and family references |
| claims/<id>.md | claim/v1 | Research claim, evidence, gaps and notes |
| sources/<id>.md | source/v1 | Source citation |
| media/<id>.md | media/v1 | Media metadata; file points to a local binary |
| places/<id>.md | place/v1 | Place metadata and optional coordinates |
| unions/<id>.md | union/v1 | Historical unions and their evidence/status |
| stories/<id>.md | story/v1 | Long-form narrative |
| news/<slug>.md | news/v1 | Bulletin item |

Each file starts with YAML front matter containing id and schema. The site builder reads Markdown directly; it does not read or emit JSON data files.

## Generated output

docs/ contains the shared interactive application plus minimal compatibility redirects for old record URLs. All record details are rendered by `site/template.html`; no parallel static-page design is generated. family-tree.ged is generated from person front matter. Never hand-edit generated HTML or GEDCOM.
