# Arbejdsmetode — Gårdsted og Gedde

Dette er den fælles, fremadrettede standard for brugeren og alle agenter. Læs også `AGENTS.md` og de seneste poster i `coop.log.md` før arbejde.

## Ufravigelige principper
1. **Kilder:** Kun Markdown under `content/` og lokale mediefiler er redaktionelle kilder. Ingen JSON-snapshots eller genererede filer må bruges som kilder.
2. **Kompilering:** Én compiler (`scripts/interactive_site.py`) og én HTML/CSS/JS-skabelon (`site/template.html`) genererer hele webstedet fra Markdown/media. Alle registre og detaljevisninger bruger samme interaktive grænseflade. Output må ikke håndredigeres.
3. **Åben forskning:** Vis fakta, hypoteser, konflikter, mangler og negative søgninger. Ingen sikkerhed må antydes, som kilderne ikke bærer.
4. **Lokal kildebevaring:** Klikbare links til dokumenter/billeder skal pege på lokale kopier i repoet. Registrér altid original URL/arkivsignatur og adgangsdato som provenance.
5. **Sporbarhed:** Påstand → claim → kildepost → lokal fil → oprindelig placering.

## 1. Privat kildeindtagelse og offentlig publicering
`sloev/tree_private` er eneste indtagelses- og forskningsarbejdsplads. Alle nye captures lægges i det private repositories `Ingest_me/`. GitHub Actions arkiverer originaler, konverterer dokumenter, fremstiller sidebilleder og OCR-udkast og opretter en append-only visuel review-kø til ChatGPT-assisteret gennemgang. OCR er aldrig autoritativ; hver side skal visuelt inspiceres og have en eksplicit disposition. Se private repositories README og `AI_review_queue/README.md`.
- Dette offentlige repository har ingen capture-indbakke, OCR-job eller råmaterialebehandling.
- Private `tree_private` publiceringsagenten udarbejder manifest-listede, offentligt sikre Markdown-/mediefiler i `publish/ready/`. GitHub Actions overfører dem automatisk til `sloev/tree:main` efter privacy- og evidenskontrol. Brugeren skal ikke godkende hvert enkelt fund eller merge PR’er.
- Foreløbige leads, hypoteser og modstridende oplysninger må offentliggøres, når de er offentligt sikre, kildehenviste og tydeligt mærket med valideringsgrad. Rå captures, sidebilleder, ureviewet OCR, DNA-/matchdata og identificerende oplysninger om nulevende forbliver private.
- Rå DNA-matchcaptures, genetiske data, matchlister og identificerende afledte oplysninger forbliver private.
- Kilde-/claim-poster i dette repository skal være uafhængigt dokumenteret og må ikke fremstille private match-hypoteser som historiske fakta.

## 2. Bulletin ved offentliggørelse
- OCR og sidebilleder dannes i det private repository. Det offentlige build kører ikke OCR på rå captures.
- Hver merged publicerings-PR ændrer normalt filer under `content/` og får mindst én automatisk bulletinpost i `content/activity.md`. Bulletin beskriver offentliggørelsesaktivitet, ikke automatisk et bekræftet genealogisk fund.
- **Håndskrift:** OCR må aldrig stå alene. Gennemgå hvert originalt sidebillede ved læsbar opløsning; lav en diplomatisk transskription (bevar linjeskift, forkortelser, stavemåder og usikkerheder), markér ulæselige tegn med `[?]`, og lav normaliseret læsning separat. Dobbelttjek navne, datoer, stednavne og relationstermer mod billedet. Registrér hvem/hvad der er læst og hvilke sider der ikke er læst. Hvis billedet ikke kan inspiceres, markér capture som BLOCKED — udled ikke indhold fra OCR alene.

## 3. Fra privat forskning til automatisk offentlig kildemateriale
Arbejd med allerede godkendte forskningsposter i det offentlige repository. Private captures forbliver i `tree_private`; de flyttes ikke til offentlige mapper. Før en offentlig kilde/claim oprettes, skal publiceringspakken indeholde:
1. Oprindelig URL/arkivsignatur, adgangsdato og provenance.
2. Kildeklassifikation og præcis diplomatisk transskription med side-/foliohenvisning.
3. En claim, der angiver hvad kilden beviser og ikke beviser, modstridende evidens og mangler.
4. Uafhængig privacy-gennemgang i agent/workflow; ingen levende DNA-matchdata eller identificerende detaljer. Dette er ikke en bruger-godkendelsesport.
5. Lokale, lovligt arkiverede kopier kun når publiceringsrettigheder og adgangsvilkår tillader det.

## 4. Valideringsgrad og åben forskning
Brug claimens eksisterende `status` (`needs`, `hypothesis`, `family`, `conflict`) til arbejdssituationen og feltet `validation` til styrken af evidensen:
- `unassessed`: ikke gennemgået / automatisk import.
- `lead`: mulig kilde eller forklaring, endnu intet selvstændigt bevis.
- `low`: indirekte, sekundær, familieoplysning eller svag identifikation.
- `moderate`: kildeunderstøttet, men væsentlige huller eller kun indirekte evidens.
- `high`: stærk direkte kilde eller flere uafhængige kilder; identitet og kontekst kontrolleret.
- `confirmed`: den præcise påstand er direkte dokumenteret af primærkilde eller tilsvarende evidenskæde, og væsentlige modsigelser er behandlet.
Valideringsgraden gælder kun den konkrete claim, aldrig automatisk hele personens historie. Konflikter skal forblive synlige. Hver claim har **Claim**, **Evidence**, **Missing**, **Next**. Skeln eksplicit mellem kildeudsagn og fortolkning; bevar historik i daterede noter.

## 5. Links, originalplacering og lokale kopier
- Klikbare dokument-/billedlinks i content skal være relative links til eksisterende filer i repoet.
- Registrér original placering som `original_url` (eller arkivkatalog), `accessed`, arkivsignatur og permanent ID i kildeposten.
- Hvis originalen er bag login, blokeret, ikke-downloadbar eller rettighedsbegrænset: ingen falsk kopi og intet eksternt klikbart dokumentlink. Registrér URL som almindelig tekst/kode, `local_copy: null`, begrundelse og opret lead til alternativ adgang.
- Interne Markdown-links skal være relative og målfilen skal eksistere. Undgå eksterne hyperlinks i person/claim/source/place/media-poster; original URL hører til provenance-felter.
- Build skal kontrollere relative links, fragmenter, billeder og filstier. Brudte links er build-fejl.
- Undtag kun eksterne links, der er nødvendige for ikke-dokumentære funktioner; begrund undtagelsen. Kildebeviser skal altid have lokal kopi eller være eksplicit markeret utilgængelige.

## 6. Billedevidner
Søg aktivt efter så meget **lovligt, relevant og efterprøveligt** billedbevis som muligt til personer, steder, ejendomme, gravsteder, dokumenter og claims: originalfotos, kirkebogssider, folketællinger, skifter, kort, matrikler, skødeprotokoller og gravsten.
- Bevar original filtype, højeste læsbare opløsning og hele siden. Afledte beskæringer må ikke erstatte originalen.
- Opret `content/media/<id>.md` med lokal `file`, `original_url`, `accessed`, ophav/rettigheder, dato, motiv, personer/steder, source/claim refs og rolle.
- Evidensrolle: `direct` (direkte kildebevis), `contextual` (miljø/bygning/periode), `illustrative` (ikke bevis) eller `unverified`.
- Knyt billeder til relevante personer, steder og claims. Identifikation på gruppefoto kræver særskilt begrundelse og valideringsgrad.
- Et billede beviser kun det, det faktisk viser. Respektér ophavsret, privatliv og adgangsvilkår.

## 7. Mapper og poster
- Personer: `content/people/<id>.md`
- Claims/forskningsspor: `content/claims/<id>.md`
- Kilder: `content/sources/<id>.md`
- Mediemetadata: `content/media/<id>.md`
- Steder: `content/places/<id>.md`; every place is compiled into the shared interactive data layer and linked from maps, person birth/death/residence references and the place register.
- Personvisning og permalinks: der findes kun ét autoritativt personkort — det udvidede interaktive kort, som åbnes fra stamtræet og personregisteret. Personens permanente URL er den samme interaktive forside med `?person=<id>` og skal åbne netop dette kort, også ved direkte adgang, deling og genindlæsning. Alle personlinks, herunder fra register, stamtræ, kort, diagrammer og andre personkort, skal åbne samme komponent med samme data. Opret ikke reducerede, parallelle biografisider. Gamle `people/<id>.html`-URL’er skal viderestille til den kanoniske visning. Personregisteret skal ligeledes føre til den fælles interaktive Personer-visning. Steder, forskningsspor, kilder og medier åbnes i samme interaktive websted via stabile query-permalinks (`?place=`, `?claim=`, `?source=`, `?media=`). Ældre `.html`-adresser og register-URL’er bevares kun som små redirects til den fælles visning; de må aldrig generere parallelle sider eller CSS.
- Historiske forhold: `content/unions/<id>.md`
- Binære filer: `images/`, `media/files/`
Relationer i GEDCOM må kun ændres på eksplicit evidens. Biologisk, juridisk, ægteskabelig, plejeforældre-, værge- og husstandsrelation må ikke sammenblandes.

## 8. Agent-samarbejde via coop.log.md
Læs seneste log, AGENTS.md, denne metode og relevante claims før arbejde. Efter hver arbejdsblok logges: dato, agent, branch, scope, filer ændret, captures/kilder med original URL + lokal sti, fund pr. claim og validation (eller "intet nyt fund"), ændringer i personer/steder, kontroller med resultat, uløste spørgsmål og konkret handoff. Brug `IN PROGRESS`, `DONE`, `BLOCKED`, `HANDOFF`. Arbejd ikke parallelt i samme claim uden aftale. Påstå aldrig at en kilde er læst, fil lokal, link fungerende eller deployment live uden kontrol.

## 9. Build og release
Ved ændringer i content/media/images/template/compiler:
```sh
python3 -m pip install -r requirements.txt
python3 scripts/compile_content.py --check
python3 scripts/check_local_links.py
python3 scripts/check_integrity.py
python3 scripts/compile_content.py
python3 site/build.py
python3 scripts/check_generated_links.py
```
Buildet må ikke importere eller kalde en separat statisk sidegenerator. Kontrollér schemaer, interne referencer, lokale links/media, privacy og den fælles interaktive forside. Test direkte adgang, genindlæsning og browserhistorik for `?person=`, `?place=`, `?claim=`, `?source=` og `?media=` samt `#tal` og `#personer`. GitHub Actions skal køre på relevante ændringer og fejle ved manglende lokale filer/links. Commit kilder og scripts, ikke håndredigerede outputs. Bekræft workflow og Pages deployment før live-status.

## Capture er først DONE når
Capture er klassificeret, arkiveret lokalt eller dokumenteret utilgængelig; original placering og adgangsdato er gemt; source + claims er opdateret; relevante personer/steder/billeder er knyttet; links er kontrolleret; leads og coop.log er opdateret.


## 6. Migrationskort og geografiske hændelser

- Den kanoniske migrationskilde er `content/migrations/migration-events.md` med schema `migration-events/v1`. Kortgeometrien i `content/maps/denmark.md` forbliver én separat `map/v1`-post; migrationshændelser må ikke lægges ind som ekstra geometri-records.
- Hver hændelse skal have stabilt ID, person-ID, claim-ID, hændelsestype, sted/land, koordinater, evidenslabel, identitetsstatus, forklaring og provenance. Kildeposter angives med `source_ids`, når de findes; personpostens kildereferencer eller præcis claim-reference angives ellers i `source_reference`.
- Hold mindst disse typer adskilt: kontraktens rejsemål, transskriberet protokolreference, dokumenteret afrejse, dokumenteret ankomst, senere bopæl/bosættelse, identifikationshypotese og arkivsøgeområde. Et kontraktmål er ikke bevis for faktisk ankomst; et havneanløb er ikke bevis for landgang eller familieforhold.
- Tegn aldrig en rute alene ud fra et mål eller et forskningsspor. En rute kræver en dokumenteret afrejse og en særskilt dokumenteret ankomst, knyttet til samme person og rejseforløb. Hvis kun ét punkt er belagt, vis kun punktet og dets evidenslabel.
- Arkivsøgeområder (fx Rio de Janeiro, Santos og São Paulo i Brasilien) vises med særskilt symbol og må aldrig fremstilles som personens destination eller ophold.
- Koordinater er omtrentlige by-/områdereferencer, medmindre en præcis historisk adresse er dokumenteret. Vis koordinatforbeholdet i data og UI.
- Langelands lokale afgangslisteoptællinger uden navne vises som lokale arkivspor, ikke som personhændelser eller oversøiske rejser. De må først forbindes med en person efter kontrol af den originale kirkebogsindførsel.
- Nye poster skal automatisk indgå i den fælles `#kort`-visning via compilerlaget. Ingen hardcodede destinationslister i HTML-skabelonen.
