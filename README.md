# Slægten Gårdsted og Gedde

En slægtsbog bygget på danske kirkebøger, folketællinger og lokalarkiver.

- **Hjemmeside:** `docs/index.html`, udgivet med GitHub Pages fra `main`-grenen, mappen `/docs`.
- **Sammenfatning med kilder:** [`family-tree.md`](family-tree.md)
- **GEDCOM til MyHeritage, Geni, Ancestry eller Gramps:** [`family-tree.ged`](family-tree.ged)

## Én datakilde og automatisk build

Alle kanoniske slægtsdata og offentlige forskningsspor ligger i **[data/tree.json](data/tree.json)**. Det er den eneste datafil, der skal redigeres til almindelige opdateringer. Den indeholder personer, relationer, steder, kilder, billeder, kortdata og forskningspåstande.

- \`data/build.py\` validerer datakilden og skriver de afledte kompatibilitetsfiler.
- \`site/template.html\`, \`site/poster.html\` og øvrige layout-/assetfiler bestemmer præsentationen.
- \`site/build.py\` bygger hjemmesiden og plakatvisningen.
- \`data/export.py\` bygger GEDCOM fra samme datakilde.

Kør hele buildet lokalt:

\`\`\`sh
python3 data/build.py
python3 data/export.py
python3 site/build.py
\`\`\`

GitHub Actions kører automatisk samme kæde, når \`data/tree.json\` ændres. \`data/family.json\`, \`data/research.json\`, \`data/map.json\`, \`family-tree.ged\`, \`site/index.html\` og \`docs/\` er afledte output — redigér dem aldrig manuelt. \`data/build_data.py\` og de tidligere JSON-inputfiler er bevaret som historisk/legacy materiale, ikke som aktive datakilder.

## Private personer

Nulevende og personer født inden for de sidste 100 år uden dødsdato står ikke i klartekst i repoet.
De ligger AES-256-GCM-krypteret i `data/tree.json` under `family.private_blob` og vises som "Privat person" på den offentlige side,
indtil man låser op med kodeordet. Kodeordet står ikke i repoet.

```sh
FAMILY_PASSWORD=... python3 data/private_tool.py decrypt   # skriver data/private_people.json (ignoreres af git)
# ret i data/private_people.json
FAMILY_PASSWORD=... python3 data/private_tool.py encrypt   # krypterer igen og opdaterer den krypterede blob og pladsholdere i data/tree.json
```

`data/build.py` stopper med en fejl, hvis en person, der burde være privat, står i klartekst.


## Åben forskning og bidrag

Dette projekt er åbent i både kode, kilder, metode og revisioner. Den offentlige hjemmeside viser både det etablerede stamtræ og et særskilt forskningsspor med synlige modenhedsgrader. Et forslag i forskningssporet er ikke automatisk en accepteret forældre-/barn-relation.

Alle må gerne:

- foreslå en rettelse eller en ny person/forbindelse via [GitHub Issues](https://github.com/sloev/tree/issues);
- indsende kildehenvisninger, transskriptioner eller reproducerbare fund via en [Pull Request](https://github.com/sloev/tree/pulls);
- udfordre en eksisterende tolkning, også hvis det betyder at en tidligere konklusion skal nedgraderes eller trækkes tilbage.

Et nyttigt bidrag angiver så præcist som muligt arkiv, kirkebog/serie, sogn, år, opslag/side/billede, ordret relevant tekst, stabil URL og hvad kilden ikke beviser. Skeln mellem originalkilde, indeks, publiceret slægtshistorie og familieoplysning. Angiv hvilken konkret person eller relation påstanden vedrører. Ingen bør dele adgangskoder, private nulevende personers følsomme oplysninger eller materiale, de ikke har ret til at offentliggøre.

### Offentlig modenhedsstatus

| Status | Betydning |
|---|---|
| Godt belagt | Samtidige eller stærkt uafhængige kilder støtter den konkrete oplysning. |
| Kræver mere belæg | Et troværdigt spor, men afgørende originalkilde, identitet eller mellemled mangler. |
| Foreløbig hypotese | Mulig forbindelse eller søgeidé; må ikke læses som fastslået slægtskab. |
| Familieoplysning | Oplysningens proveniens er familien; det er ikke i sig selv en sikkerhedsgrad. |

Status gælder den enkelte påstand — især hver enkelt relation — ikke automatisk alle oplysninger om personen. Modstridende udsagn bevares med deres kilder og må ikke skjules ved at vælge en bekvem version.

### Sådan følger du ændringer

- [Seneste commits](https://github.com/sloev/tree/commits/main/) viser alle kilde-, data- og kodeændringer.
- [Forskningsdossierer](leads/README.md) forklarer aktive spørgsmål og næste arkivskridt.
- [Samarbejdsloggen](coop.log.md) dokumenterer forskningshandoffs, beslutninger, ændringer og hvad der endnu ikke er kontrolleret.
- [Nyhedsbulletinen og forskningssporet](https://sloev.github.io/tree/) viser de læsbare opdateringer på hjemmesiden.


### Automatisk udrulning af ændringer

Når `data/tree.json` ændres, sammenligner GitHub Actions persondata med forrige version. Ændrede personer får en gul prik i stamtræet i 30 dage, og en dateret opdatering indsættes i nyhedsbulletinen. Ændringer i dossierer under `leads/` udløser ikke et build: dossiererne er kun indgående forskningsmateriale, som først bliver offentligt, når et vurderet spor er indarbejdet i `data/tree.json`. Bygget regenererer alle afledte data, GEDCOM og hjemmesidens HTML.

Markeringen er en visuel ændringsindikator, ikke en kilde- eller sikkerhedsgrad. En ændring i et dossier, der ikke nævner en bestemt person på de ændrede linjer, giver en bulletinpost, men ingen vilkårlig personmarkør. Markørerne udløber efter 30 dage. Se `.github/workflows/rebuild-site.yml`, `data/build.py` og `tools/mark_recent_people.py` for implementeringen.

### Åben forskningsside — også det, der endnu ikke er bevist

Hjemmesiden skal være et **åbent forskningstræ**. Relevante, privatlivsmæssigt forsvarlige spor skal vises, mens de undersøges — ikke først når de er bevist. Et klik på en person eller forbindelse skal forklare status, kildernes oprindelse, hvad de faktisk viser, eventuelle modstridende oplysninger og præcis hvad der mangler. Mulige biologiske forbindelser må ikke ligne fastslåede slægtskabsforhold; vis dem særskilt og tydeligt foreløbigt.

Vi vil gerne have hjælp fra besøgende. Forskningssiden skal derfor gøre det let at finde åbne spørgsmål efter navn, sted, slægtslinje og status og give en konkret anvisning på, hvilken kirkebog, folio, folketælling, skifteprotokol eller anden kilde der kan afklare spørgsmålet. Bidrag kan sendes via [GitHub Issues](https://github.com/sloev/tree/issues) eller Pull Requests. Se [den fulde publicerings- og privatlivsmetode](research_method.md#9-open-public-research-and-community-contributions).

Åbenhed gælder historisk forskning, ikke private oplysninger: levende personer, private dokumenter, følsomme detaljer og ikke-offentliggjorte oplysninger om informanter skal fortsat beskyttes. En familieoplysning kan godt offentliggøres som familieoplysning, når det er forsvarligt; den må aldrig præsenteres som et dokumenteret faktum alene af den grund.


### Forskningsregister på hjemmesiden

Den første offentlige version af fanen **Forskningsspor** er nu lagt i koden. Den indeholder nu 27 åbne spor på tværs af de fire aktive bedsteforældregrene. Hvert spor viser status, det foreliggende belæg, hvad der mangler, næste kontrol og et link til arbejdsdossieret. Registerets redigerbare kildedata ligger i `data/research.json`; visningen bygges via `site/build.py`.

Registeret er fortsat en kurateret oversigt — ikke en fuldstændig offentliggørelse af alle dossier-noter. Den lokale bygge- og browserkontrol samt bekræftelse af GitHub Pages-deploy mangler fortsat.
