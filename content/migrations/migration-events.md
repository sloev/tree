---
id: migration-events
schema: migration-events/v1
events:
  - id: shanghai-contract-1904
    person_id: s_p54_6
    claim_id: lorenz-gedde-emigration
    event_type: contract_destination
    place: Shanghai
    country: Kina
    latitude: 31.2304
    longitude: 121.4737
    coordinate_basis: "Omtrentlig moderne bykoordinat; ikke historisk præcis adresse."
    source_reference: "Personpost s_p54_6, felt src; Københavns Politis kontrakt 3534 (11.07.1904)."
    source_ids: []
    date: "1904-07-11"
    layer: documentary-lead
    evidence_label: "Kontraktreference, transskription"
    identity_label: "Knyttet til Olaf Geddes personpost"
    note: "Københavns Politis udvandrerprotokol angiver Shanghai som rejsemål. Det dokumenterer kontraktens destination, ikke faktisk ankomst eller senere ophold. Originalkontrakten skal genkontrolleres."
  - id: fresno-contract-1910
    person_id: s_p60_2
    claim_id: gerda-iver-emigration
    event_type: contract_destination_transcription
    place: Fresno, Californien
    country: USA
    latitude: 36.7378
    longitude: -119.7871
    coordinate_basis: "Omtrentlig moderne bykoordinat; ikke historisk præcis adresse."
    source_reference: "Personpost s_p60_2, felt src; tidligere transskription af kontrakt 4443 (08.09.1910)."
    source_ids: []
    date: "1910-09-08"
    layer: documentary-lead
    evidence_label: "Protokoltransskription; original ikke genfundet"
    identity_label: "Sandsynlig personkobling; originalkontrol mangler"
    note: "En tidligere transskription af kontrakt 4443 angiver Fresno som rejsemål og damperen United States. Den originale protokolside er endnu ikke genfundet. Senere Alameda-vejvisere er et muligt identitetsspor, ikke bevis for ankomst til Fresno."
  - id: eldorado-identification-hypothesis
    person_id: s_p54_3
    claim_id: lorenz-gedde-eduard-eldorado
    event_type: settlement_identification_hypothesis
    place: Eldorado, Misiones
    country: Argentina
    latitude: -26.4
    longitude: -54.65
    coordinate_basis: "Omtrentlig moderne bykoordinat; ikke historisk præcis adresse."
    source_reference: "De Danskes Vej, bd. III, trykt s. 80; Udvandrerarkivets billedhenvisninger B9886 og B9790."
    source_ids:
      - de-danskes-vej-argentina-eldorado-gedde
    date: "1922"
    layer: hypothesis
    evidence_label: "Identifikationshypotese"
    identity_label: "Eduard/Edouard Gedde kan være Emil Ludvig Edvard Gedde"
    note: "Trykt omtale og Gedde-fotografihenvisninger peger mod Eldorado. Identiteten mellem Eduard/Edouard og Emil er ikke bevist; punktet er ikke en bekræftet ankomst eller bosættelse."
  - id: brazil-rio-archive-search
    person_id: p6
    claim_id: lorenz-brazil-sailor-archive-route
    event_type: archive_search_target
    place: Rio de Janeiro
    country: Brasilien
    latitude: -22.9068
    longitude: -43.1729
    coordinate_basis: "Omtrentlig moderne bykoordinat for arkivsøgeområde; ikke et registreret havneanløb."
    source_reference: "Rigsarkivets vejledning om Centralkartotek over søfolk; claim lorenz-brazil-sailor-archive-route."
    source_ids:
      - rigsarkivet-soefolk-i-handelsfladen
    layer: research-target
    evidence_label: "Arkivsøgeområde"
    identity_label: "Ingen rejse eller ankomst dokumenteret"
    note: "Rio de Janeiro er nævnt som et muligt arkivmæssigt søgeområde for skibsankomster. Punktet siger intet om Lorenz' faktiske rejser."
  - id: brazil-santos-archive-search
    person_id: p6
    claim_id: lorenz-brazil-sailor-archive-route
    event_type: archive_search_target
    place: Santos
    country: Brasilien
    latitude: -23.9608
    longitude: -46.3336
    coordinate_basis: "Omtrentlig moderne bykoordinat for arkivsøgeområde; ikke et registreret havneanløb."
    source_reference: "Rigsarkivets vejledning om Centralkartotek over søfolk; claim lorenz-brazil-sailor-archive-route."
    source_ids:
      - rigsarkivet-soefolk-i-handelsfladen
    layer: research-target
    evidence_label: "Arkivsøgeområde"
    identity_label: "Ingen rejse eller ankomst dokumenteret"
    note: "Santos er et muligt arkivmæssigt søgeområde, hvis Lorenz' sømandskartotek senere viser relevante skibstogter."
  - id: brazil-sao-paulo-archive-search
    person_id: p6
    claim_id: lorenz-brazil-sailor-archive-route
    event_type: archive_search_target
    place: São Paulo
    country: Brasilien
    latitude: -23.5505
    longitude: -46.6333
    coordinate_basis: "Omtrentlig moderne bykoordinat for arkivsøgeområde; ikke en registreret bopæl."
    source_reference: "Museu da Imigração som senere arkivsøgevej; claim lorenz-brazil-sailor-archive-route."
    source_ids:
      - rigsarkivet-soefolk-i-handelsfladen
    layer: research-target
    evidence_label: "Arkivsøgeområde"
    identity_label: "Ingen rejse eller ankomst dokumenteret"
    note: "Museu da Imigração og lokale registre er en senere søgevej, ikke dokumentation for Lorenz' ophold."
local_notes:
  - id: skroebelev-departure-lists-1855
    place: Skrøbelev, Langeland
    date: "1855"
    claim_id: gerda-emigrant-family
    source_reference: "Henning Bender, Den oversøiske udvandring fra Danmark 1840–1920 + kilder, foredrag 25.04.2024."
    evidence_label: "Sognetælling i sekundær oversigt"
    note: "Henning Benders oversigt opgør én person i Skrøbelevs afgangslister i 1855. Navnet er ikke identificeret; det må ikke knyttes til Jørgen, Bodil eller et barn uden original kirkebogsindførsel."
  - id: skroebelev-departure-lists-1866
    place: Skrøbelev, Langeland
    date: "1866"
    claim_id: gerda-emigrant-family
    evidence_label: "Sognetælling i sekundær oversigt"
    note: "Henning Benders oversigt opgør én person i Skrøbelevs afgangslister i 1866. Navnet og destinationen er ukendte; dette er et lokalt arkivspor, ikke dokumentation for oversøisk udvandring."
---

Kanonisk, kildehenvist datasæt til kortets udvandrings- og søgespor. Hændelsestyper holdes adskilt: kontraktdestination, identifikationshypotese og arkivsøgeområde er ikke det samme som dokumenteret ankomst eller bosættelse. Der tegnes ingen ruter uden særskilte, dokumenterede afrejse- og ankomsthændelser.
