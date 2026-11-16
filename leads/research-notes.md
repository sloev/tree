# First investigation notes — uploaded ancestry leads

**Date:** 16 November 2026  
**Repository:** `sloev/tree`, `main` only  
**Scope:** initial audit of the four uploaded files and targeted source checks. This is a research checkpoint, not a completed proof of every line.

## 1. Lorenz Heinrich Frederiksen — legal and biological paternity must be separated

The current canonical narrative (`family-tree.md`) gives two incompatible accounts:

- The Egernsund civil birth register (1932 no. 4) reportedly has a marginal note dated 11 July 1932 recording land worker Wilhelm Krogh of Snogbæk as the legally acknowledged/registered father, based on a paternity declaration of 5 April 1932 and a court decision of 10 June 1932.
- Family knowledge instead identifies farmer's son Sophus Petersen of Påkjær, Nybøl, as Lorenz's biological father and says Wilhelm accepted paternity. The narrative explicitly says the tree follows family knowledge and that only DNA can decide the biological question.

The current data model has Lorenz (p6) linked to Sophus as father and Peter Frederiksen as stepfather. That is a recorded project hypothesis, not a conclusion demonstrated by the civil-register marginal note.

### Archival route now identified

Rigsarkivet's current guide for 1919–1970 says a paternity case began with the police; if paternity was disputed, the civil court decided it, while the maintenance/alimentation case is held in the county archive. It recommends starting with the county archive and searching:

1. `Alimentationsjournal` (and any register to it);
2. `Almindelig Journal`;
3. `Journalsager` / `Alimentationssager`.

If the case is not located there, search the civil court's case list and judgment book, then police paternity protocols. The guide states that paternity/alimentation case material is subject to a 75-year access period.

The official Landsarkivet for Sønderjylland archive overview says the Aabenraa and Sønderborg counties were merged into **Aabenraa-Sønderborg Amt effective 1 April 1932**. Its archive description includes alimentations cases and identifies registers/journals/journal files for 1920–1935, with the relevant unprinted finding aid held in the reading room. Since the reported judgment is 10 June 1932, Aabenraa-Sønderborg Amt is the first county archive to investigate, not the pre-merger Sønderborg Amt archive.

**Important limitation:** the exact case, journal number, judgment, and underlying evidence have not yet been located. This is a precise archive route, not a claim that the files have been read.

Sources:
- Rigsarkivet, “Faderskabssager – Kom godt i gang!”: https://www.rigsarkivet.dk/vejledning/faderskab-og-adoption/faderskabssager-kom-godt-i-gang/
- Rigsarkivet, *Landsarkivet for Sønderjylland: En arkivoversigt* (2002), pp. 91–92 / PDF lines 6228–6325: https://www.rigsarkivet.dk/wp-content/uploads/2022/06/Landsarkivet-for-Soenderjylland-En-arkivoversigt.pdf
- Project's current source narrative: https://github.com/sloev/tree/blob/main/family-tree.md

## 2. Jens Peder Larsen — spouse correction

The uploaded Expanded Master Dossier identifies Mette Pedersdatter as Jens Peder Larsen's spouse. This conflicts with both the current project narrative and the Horsbøl genealogy index.

Horsbøl identifies:
- Jens Peder Larsen, born 29 February 1812 at Pårup Melgaard, Assing; died 25 May 1870 at Sønder Omme, Kirkeby; buried 2 June 1870.
- Kjersten Frederiksdatter, born 20 April 1822 at Tarp, Sønder Felding.
- Marriage: 8 October 1843 in Sønder Felding.
- A child named Mette Marie is listed beneath the couple.
- Kjersten later appears in a second marriage dated 11 June 1872 to Niels Pedersen.

The uploaded “Mette Pedersdatter” spouse name may be a confusion with daughter Mette Marie. This is a secondary-source correction only; the original 1843 marriage register should still be transcribed before canonical data is edited.

Sources:
- Horsbøl, genealogical entry: https://www.horsboel.dk/familie/grind/dat16.htm (lines 415–439 in the opened page)
- Existing project narrative: https://github.com/sloev/tree/blob/main/family-tree.md

## 3. Ove Samuel Gedde — birth date discrepancy narrowed

Three dates are present across the source material:
- Canonical project data: 28 February 1778.
- P.I. Liebe and E. Borgstrøm, *Biografiske oplysninger om faste artilleriofficerer af linien...*, printed p. 509: 28 May 1778–10 March 1843. The title page says the work was compiled from Captain Georg Lutken's notes in the Rigsarkiv's Army Archive.
- Carl Johan Anker, *Biografiske data om 330 norske...* (1885), p. 94: 28 May 1788–10 March 1843. Project Runeberg explicitly labels the OCR page “never proofread”; the scan should be visually checked before treating the printed 1788 as certain.

The year 1778 is supported by the officer biography and the project's broader family narrative. The exact day/month remains unresolved: 28 February (project) versus 28 May (officer biography). The 1788 year in Anker conflicts with the 1778 officer biography and the project's date, and should be treated as a likely secondary-source discrepancy pending inspection of the original scan and baptism.

Sources:
- P.I. Liebe & E. Borgstrøm, *Biografiske oplysninger om faste artilleriofficerer af linien*, printed p. 509: https://slaegtsbibliotek.dk/910571.pdf
- Carl Johan Anker (1885), p. 94, unproofread OCR: https://runeberg.org/acj330bio/0110.html
- Existing canonical data: https://github.com/sloev/tree/blob/main/data/build_data.py

## 4. Langø — local-history claim corroborated; title record still needed

Langeland Byarkiv's register of articles in the yearbook *Øboer* lists “Langø og dæmningen” by Lisbeth Skov (2011) and summarises the claims:
- Marius Christensen and his wife Ane Marie bought Langø in 1894.
- Marius, with help from sons and a son-in-law, built a 334 m causeway in 1911.
- Ane Marie died in 1930; Marius remained on Langø until his death in 1934.
- Their children erected a memorial stone in 1934.

This is useful published local-history corroboration, but the article's family connection means the land transaction should still be checked against the title record. Arkiv.dk describes Rudkøbing Byhistoriske Arkiv collection A790 as containing real registers and land books (1790–2013) for Lindelse, Magleby and other Langeland parishes.

Next: request the Lindelse real-register entry and associated 1894 deed/tingbog entry; then search local authority or newspaper records for the 1911 causeway.

Sources:
- Langeland Byarkiv, “Register over artikler i Øboer”: https://byarkivet.langelandkommune.dk/boeger-brochurer/register-over-artikler-i-oeboer
- Arkiv.dk, collection A790: https://arkiv.dk/vis/3931656

## 5. Kresten Henriksen Jørgensen — initial null result

The upload states that Kresten Henriksen Jørgensen was born 3 November 1877 as an illegitimate son of Lars Thomsen Larsen (born 1859) and was raised by the mother's parents. The note says the family-chart entry is partly obscured by an ink blot; no mother or original register reference is supplied.

An exact-name web search and a check of the Strømming public index under K did not identify this person. The K index lists four people named Kresten, none matching the supplied name. This is not a comprehensive search of original registers and does not disprove the claim.

Next: inspect the original family chart; identify the mother and likely parish; search Magleby and neighbouring South Langeland birth/baptism registers for 1877, including illegitimate-birth columns; then follow confirmation and census entries.

Source checked:
- Strømming public K-name index: https://www.stroemming.dk/genealogy/gedweb/Public/da/Lists/allnames-K.html

## 6. What remains unverified

- No original paternity file or DNA evidence was obtained.
- No original 1843 marriage register image was transcribed for Jens Peder and Kjersten.
- No original baptism was located for Ove Samuel to resolve 28 February versus 28 May.
- No deed or land-book image was inspected for the 1894 Langø purchase.
- No original 1877 baptism or family-chart image was inspected for Kresten.
- The medieval von Kleist chain remains explicitly provisional as stated in the source dossier.

No canonical person records or relationships were changed in this pass. No private/encrypted files were accessed. No build or tests were run.
