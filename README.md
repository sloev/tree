# Slægten Gårdsted og Gedde

Johannes Gårdsted Valbjørns aner, fundet i danske kirkebøger, folketællinger og lokalarkiver.

- **Hjemmeside:** `docs/index.html`, udgivet med GitHub Pages fra `master`-grenen, mappen `/docs`.
- **Sammenfatning med kilder:** [`family-tree.md`](family-tree.md)
- **GEDCOM til MyHeritage, Geni, Ancestry eller Gramps:** [`family-tree.ged`](family-tree.ged)

## Genopbygning

Alle oplysninger står i `data/build_data.py`. Kør dette efter en ændring:

```sh
python3 data/build_data.py   # skriver data/family.json
python3 data/export.py       # skriver family-tree.ged
python3 site/build.py        # skriver site/index.html og docs/index.html
```

Personer tilføjes med `person(...)`. Søskende tilføjes med `sibs(...)`, og en person, hvis forældre ikke er i træet, kan knyttes til en søskende med `sibof=`.
