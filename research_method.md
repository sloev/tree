# Forskningsmetode — én offentlig sandhedskilde

Dette dokument beskriver arbejdsgangen for slægtsforskningen i `sloev/tree`.

## 1. Sandhedskilde og registrering

- `data/tree.json` er den eneste redigerbare sandhedskilde for personer, relationer, kilder, kort og forskning.
- Alle nye leads, kildefund, transskriptioner, rettelser, kildekonflikter, negative søgninger og næste handlinger registreres direkte i et eksisterende eller nyt forskningsspor under `tree.json` → `research.claims`.
- Findes spørgsmålet allerede, udvides samme spor. Opret ikke parallelle noter eller dubletter.
- Detaljeret historisk materiale fra tidligere dossierer ligger som `research_notes` på det relevante spor og vises i forskningsfanen.
- `data/family.json`, `data/research.json` og `data/map.json` er genererede kompatibilitetsfiler. Redigér dem aldrig manuelt.
- `family-tree.ged`, `family-tree.md`, `site/index.html` og `docs/` er afledte output.

## 2. Forskningssporets felter

Et spor skal som minimum have:
- stabilt unikt `id`, `branch`, `title` og status;
- konkret spørgsmål/påstand;
- hvad kilderne faktisk viser;
- hvad der mangler eller er modstridende;
- næste konkrete arkivkontrol;
- kilder med forklarende etiketter og stabile URL'er;
- relevante person-ID'er;
- `research_notes` med daterede, kildebevarende noter, når der er detaljeret historik.

Gyldige statusser: `needs`, `hypothesis`, `family`, `conflict`. Status gælder den enkelte påstand, ikke alle oplysninger om personen.

## 3. Kildekritik

Prioritér original kirkebog, folketælling, skifte, retssag, militærrulle, ejendomsakt eller civilregister. Skeln mellem originalkilde, arkivregistratur, indeks, publiceret slægtshistorie, online database og familieoplysning.

Registrér:
- arkivskaber, serie, sogn/sted, år, opslag/side/folio/sagsnummer;
- ordret tekst eller trofast transskription, når den er afgørende;
- hvad kilden direkte beviser, og hvad den ikke beviser;
- navnevarianter, modstridende datoer og negative søgninger;
- stabil URL og adgangsdato.

Et arkivkatalog viser, at en serie findes; det beviser ikke indholdet af en bestemt sag. Et indeks er et søgemiddel, ikke en erstatning for originalen.

## 4. Identitet og relationer

Sammenlæg ikke personer alene på grund af navn, erhverv, sogn eller omtrentligt årstal. Brug flere uafhængige identifikatorer.

Hold biologisk, juridisk/registreret, ægteskabelig, sted-, adoptiv-, pleje-, værge- og husstandsrelation adskilt. En paternitetserklæring eller dom viser, hvad der blev erklæret eller juridisk afgjort; den er ikke automatisk genetisk bevis. Et forskningsspor opretter ikke automatisk en relation i stamtræet.

## 5. Offentlighed og privatliv

Forskningsspor er offentlige som udgangspunkt, også når konklusionen er usikker. Vis usikkerhed tydeligt. Offentliggør ikke adgangskoder, private nulevende personers følsomme oplysninger eller oplysninger uden ret til offentliggørelse. Følg `data/PUBLIC_CONSENT.md` og de eksisterende anonymiseringsregler for nulevende og nyligt fødte personer.

Det private supplement og krypterede persondata må ikke kopieres ind i offentlige forskningsnoter. Hvis en kilde indeholder blandede oplysninger om afdøde og nulevende, registrér kun den historiske del, der forsvarligt kan offentliggøres.

## 6. Arbejdsgang

1. Læs `AGENTS.md`, denne metode og de relevante forskningsspor i `data/tree.json`.
2. Søg efter eksisterende spor, før et nyt oprettes.
3. Registrér fund og kildehenvisning direkte i sporet.
4. Opdatér status, mangler og næste handling.
5. Kør `python3 data/build.py`, `python3 data/export.py` og `python3 site/build.py` lokalt, når miljøet er til rådighed.
6. Kontrollér GitHub Actions build og Pages-udrulning. Påstå ikke, at siden er live, før det er bekræftet.

## 7. Repoets struktur

- `data/tree.json`: eneste redigerbare data- og forskningskilde.
- `data/build.py`, `data/export.py`: validering og eksport.
- `site/template.html`, `site/build.py`: præsentation og website-build.
- `images/`: kildebilleder og dokumentationsbilleder, der anvendes af træet.
- `tools/`: vedligeholdelses- og eksportværktøjer.
- `docs/`: genererede GitHub Pages-filer og plakater.
