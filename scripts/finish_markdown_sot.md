# Markdown-first static-site migration — completed

The canonical genealogy and research records are stored in content/**/*.md, with binary media in images/ and media/files/.

The current pipeline does not use JSON snapshots or a browser-side data model:

    content/**/*.md + local media
       ├── scripts/compile_content.py -> family-tree.ged
       └── site/build.py -> docs/**/*.html + docs/media/*

The generated site has permanent person and research pages. GitHub Actions validates the Markdown, generates GEDCOM, and rebuilds docs/ on pushes to main.

Do not restore or use data/tree.json, archive/tree.json.backup, or the old JSON segments as build inputs. Continue editing only Markdown and referenced media.
