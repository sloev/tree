# Slægten Gårdsted og Gedde

En slægtsbog bygget på danske kirkebøger, folketællinger og lokalarkiver.

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

## Private personer

Nulevende og personer født inden for de sidste 100 år uden dødsdato står ikke i klartekst i repoet.
De ligger AES-256-GCM-krypteret i `data/private.enc` og vises som "Privat person" på den offentlige side,
indtil man låser op med kodeordet. Kodeordet står ikke i repoet.

```sh
FAMILY_PASSWORD=... python3 data/private_tool.py decrypt   # skriver data/private_people.json (ignoreres af git)
# ret i data/private_people.json
FAMILY_PASSWORD=... python3 data/private_tool.py encrypt   # krypterer igen og opdaterer data/private_stubs.json
```

`data/build_data.py` stopper med en fejl, hvis en person, der burde være privat, står i klartekst.
