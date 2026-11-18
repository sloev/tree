# Slægten Gårdsted og Gedde

En slægtsbog bygget på danske kirkebøger, folketællinger, arkivalier og familiehistorie.

- Hjemmeside: https://sloev.github.io/tree/
- GEDCOM: family-tree.ged

## Kilde til sandhed: Markdown og mediefiler

Alt redaktionelt indhold ligger under `content/`. Bygningen læser Markdown-filer og lokale mediefiler direkte. Der er ingen `tree.json` eller anden redigerbar JSON-datakilde.

| Indhold | Kilde |
|---|---|
| Personer | `content/people/<id>.md` |
| Forskningsspor | `content/claims/<id>.md` |
| Supplerende personrelationer og bopælsforløb | `content/person-enrichment.md` |
| Supplerende forskningskoblinger og kilder | `content/research-enrichment.md` |
| Forsideaktivitet og nyhedsbulletiner | `content/activity.md` |
| Kilder | `content/sources/<id>.md` |
| Mediemetadata | `content/media/<id>.md` |
| Steder | `content/places/<id>.md` |
| Historiske forhold | `content/unions/<id>.md` |
| Kortgeometri og forsidekonfiguration | `content/maps/denmark.md`, `content/site-config.md` |
| Krypteret privatpersondata | `content/private-vault.md` |
| Mediefiler | `images/` og `media/files/` |

Hver indholdspost har YAML-front matter med stabilt id og schema. Personrelationer angives med `father`, `mother`, `spouse` og relaterede felter; forskningsspor knyttes til personer med `person_ids`.

## Den interaktive hjemmeside

Hele webstedet bruger én interaktiv applikation og ét designsystem: faner, anetræ, personkort, forskningsspor, kort, statistikker, kilder og billedgalleri. HTML, CSS og interaktioner ligger i `site/template.html`; `scripts/interactive_site.py` kompilerer alle Markdown-poster til det fælles datalag.

Alle person-, sted-, forsknings-, kilde- og mediepermalinks åbner den relevante detalje i samme applikation (`?person=`, `?place=`, `?claim=`, `?source=`, `?media=`). Ældre `.html`-adresser er kun redirects, så gamle links fortsat virker uden at skabe et parallelt webdesign. `docs/index.html` er et build-output, ikke en redigerbar kilde eller en `tree.json`. Der findes ingen separat statisk sidegenerator.

## Byg lokalt

    python3 -m pip install -r requirements.txt
    python3 scripts/compile_content.py --check
    python3 scripts/compile_content.py
    python3 site/build.py

Det genererer `family-tree.ged`, `build/family-tree.ged` og `docs/` fra Markdown og mediefiler.

## Privatliv

Nulevende personer og personer født i 1926 eller senere uden registreret dødsdato vises anonymiseret som standard. Det oprindelige kodeordsbaserede unlock-flow er bevaret: den krypterede vault ligger i `content/private-vault.md`, mens klartekstoplysninger først dekrypteres lokalt i browseren efter korrekt kodeord. Personnoter og kilder for private personer indgår ikke i den offentlige data-payload.

## Forskningsstandard

Forskningssporene i `content/claims/` er den aktive forskningslog. Skeln mellem originalkilder, registre, publiceret slægtshistorie og familieoplysninger. Angiv arkiv, serie, sogn, år, opslag/billede, ordret tekst, stabil URL og hvad kilden ikke beviser.

Al ny kildeindtagelse sker i det private `sloev/tree_private`-repository. Her behandles rå captures, OCR, billeder, transskriptioner og forskning. Kun manuelt godkendte, offentligt sikre Markdown-/mediefiler overføres via en pull request. Det offentlige repository er publikationslaget; det modtager ikke rå captures eller OCR-arbejdskopier. DNA-matchcaptures og identificerende matchdata forbliver private.


## Arbejdsmetode og agent-samarbejde

Den bindende arbejdsgang for fremtidige ændringer ligger i [research_method.md](research_method.md). Agenter skal også læse [AGENTS.md](AGENTS.md) og seneste poster i [coop.log.md](coop.log.md).

- Al ny kildeindtagelse sker udelukkende i det private [sloev/tree_private](https://github.com/sloev/tree_private)-repository under `Ingest_me/`.
- Dette repository er alene publikationslaget. Kun manuelt godkendte, offentligt sikre forskningsposter og mediefiler overføres via en gennemgået pull request.
- Rå captures, OCR-udkast, sidebilleder, DNA-matchdata og identificerende oplysninger om nulevende personer publiceres aldrig her.
- Forskningsspor skal åbent angive status, valideringsgrad, evidens, modsigelser og mangler.
- Klikbare dokumentbeviser skal være lokale repo-kopier. Oprindelig URL, arkivsignatur og adgangsdato bevares som provenance.
- Søg aktivt efter lovligt billedbevis, og markér om det er direkte, kontekstuelt, illustrativt eller uverificeret.
- Links og lokale mediefiler skal kontrolleres; brudte links må ikke accepteres som færdigt arbejde.
