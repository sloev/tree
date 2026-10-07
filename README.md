# Gaardsted-Jørgensen family tree

Ancestry of Johannes Gårdsted Valbjørn, researched from Danish church books, censuses and local archives.

- **Website:** `docs/index.html`, published with GitHub Pages from the `master` branch, `/docs` folder.
- **Summary with sources:** [`family-tree.md`](family-tree.md)
- **GEDCOM for MyHeritage, Geni, Ancestry or Gramps:** [`family-tree.ged`](family-tree.ged)

## Rebuilding

All facts live in `data/build_data.py`. After editing it, run:

```sh
python3 data/build_data.py   # writes data/family.json
python3 data/export.py       # writes family-tree.ged
python3 site/build.py        # writes site/index.html and docs/index.html
```
