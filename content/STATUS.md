# Content status

Markdown is the canonical source for the public genealogy and research site.

- 494 people in content/people/
- 78 research claims in content/claims/
- source records, media metadata and places in their corresponding content/ folders

## Website generation

The production build now reads Markdown front matter and body text directly. It does not read, write or embed tree.json or any other JSON data snapshot.

1. scripts/compile_content.py validates Markdown and generates family-tree.ged.
2. site/build.py renders ordinary HTML pages from content/ and copies referenced media into docs/media/.
3. GitHub Pages serves docs/.

The generated site contains a person directory, a permanent HTML page for every person, research indexes and individual claim pages, source pages, a place directory, a media gallery and a GEDCOM download. Navigation and page content work without JavaScript; the person search is a progressive enhancement.

Latest generated output checked on 2026-11-18: 494 person rows/pages, 78 research claims, 494 GEDCOM INDI records, and 135 GEDCOM FAM records. GEDCOM includes reciprocal FAMS/FAMC links. The public output contains no embedded DATA object or tree.json reference.

Living people and people born in 1926 or later without a recorded death date are anonymized in public HTML and GEDCOM output.

## Legacy data

The former JSON-based SPA and its generated JSON snapshots have been retired. data/tree_segments/ is retained only as historical archive material; it is not part of the build and must not be treated as an editable source.

## Private intake and publication

All new source captures and working research belong in the private companion repository `sloev/tree_private`. This public repository has no intake directory or OCR processing workflow. Only manually approved, public-safe research and media arrive here through a reviewed publication change.
