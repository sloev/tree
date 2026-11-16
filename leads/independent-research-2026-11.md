# Independent research and GEDCOM audit

Research date: 16 November 2026. This note records an independent comparison of the uploaded structured JSON and GEDCOM, plus external source checks. It is not a replacement tree; no unsupported parentage has been added.

## 1. GEDCOM completeness audit

The supplied JSON contains 489 person objects. The GEDCOM contains 485 individual (INDI) records. Matching the JSON person IDs against GEDCOM xrefs identifies exactly four JSON people with no GEDCOM individual record:

| JSON ID | Person | JSON source/evidence | Assessment |
|---|---|---|---|
| p74 | Karen Christensdatter | Dansk Slægtsforskning, Rolsøgård estate (G302), probate no. 11, 14 May 1787, fol. 39 | The JSON record has no dates, parents, spouse or children; no GEDCOM individual exists. Do not infer a relationship from the probate citation alone. |
| woyten_benedictus | Benedictus (Benedict) von Woyten | von Kleist family archive, English translation, p. 123 | Named as Christina von Woyten's father in the family-history source. |
| stojentin_elisabeth | Elisabeth von Stojentin | von Kleist family archive, English translation, p. 123 | Named as Christina's mother in the family-history source. |
| below_otto_pustamin | Otto von Below of Pustamin | von Kleist family archive, English translation, p. 123 | Named as Christina's earlier husband; this is a spouse relationship, not a parent relationship. |

The GEDCOM has no IDs absent from the JSON (485/485 matched). This proves the GEDCOM is a reduced export of the JSON, not a complete representation of it. It does not prove the JSON itself is complete or correct.

The three von Woyten/Stojentin/Below people are especially important: the von Kleist family archive translation states that Christina, widow of Otto von Below of Pustamin, was the daughter of Benedictus von Woyten of Versin and Elisabeth von Stojentin of Giesebitz; she later married Georg von Kleist. The export's JSON preserves these people and links, while the GEDCOM omits all three individuals. See https://v-kleist.com/FG/english/Dubberow_translation.pdf, p. 123.

Karen Christensdatter is different: she is a source-only, currently unlinked person in the JSON. The cited Rolsøgård probate index is a promising route to identifying her, but without reading the original probate and matching the people, she should remain unlinked. Source: https://slaegt.dk/media/jnnnvuml/alfabetisk-navneliste-og-skifteuddrag-til-rols%C3%B8g%C3%A5rd-gods-g302-mols-herred-1778-1816-1818.pdf.

## 2. Independent check: the Gaardsted / Vosnæsgaard line

The uploaded data identifies Jochum (Joachim) Gaardsted, born 23 September 1792 at Vosnæsgaard, as a child of Claus Gaardsted and Kirsten Marie Jørgensdatter. The archive scan caption identifies a Skødstrup baptism entry in 1792 and names “Hr. Forpagter Gaardsted paa Vosnæsgaard” and his wife Kirstine Marie Jørgensdatter. This is the key contemporary source to inspect at full resolution before treating the relationship and exact date as fully transcribed.

Independent contextual corroboration:
- Djurslandsdatabasen's surname index lists Joachim Gaardsted, born 1792 at Vosnøsgård and died 1865 in Tirstrup parish. It also lists Hans Peter Gaardsted, born 1852 in Tirstrup, and several other Gaardsted family members. This is a secondary compiled database, useful as a discovery aid, not a substitute for parish registers: https://djursslaegt.djursdatabasen.dk/efternavne/EFTERNAVNG.htm.
- Trap Danmark's Vistoft parish history says Bogensholm was bought by Claus Gaardsted in 1796 for 10,000 rigsdaler and later sold by his widow in 1811. This independently confirms the landowner Claus Gaardsted and the family/estate context, but does not itself prove he was Jochum's father: https://trap5.lex.dk/sogn/vistoft-sogn-mols-herred/.
- A contemporary royal rescript dated 6 August 1803 addresses Claus Gaardsted as owner of Bogensholm and orders him to pay the customary church offerings. This is strong contemporary evidence that a Claus Gaardsted owned Bogensholm by 1803: https://da.wikisource.org/wiki/Side:Kongelige_Rescripter,_Resolutioner_og_Collegialbreve_for_Danmark_og_Norge_udtogsvis_udgivne_i_chronologisk_Orden._VI._Deel._12._Bind_(1803%E2%80%931804).pdf/258.

A discrepancy exists in later estate histories: Trap's Vistoft parish page gives the purchase as 1796, while another indexed Trap edition/search result gives 1797. This one-year discrepancy should be resolved from the deed/auction record, not silently normalized.

## 3. Independent check: Ove Samuel Gedde

The export currently gives Ove Samuel Gedde's birth as 28 February 1778. The genealogical entry in Personalhistorisk Tidsskrift (Harbou, 1897) also gives 28 February 1778 and death 10 March 1843. This is independent published support for the date currently in the tree: https://v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf.

A conflicting 1885 biography by Carl Johan Anker gives 28 May 1788. The digitized page is explicitly marked as not proofread OCR and the entry appears to confuse Ove Samuel with his father Hans Christopher Gedde. Do not replace the 1778 date on the strength of that OCR. Original baptism evidence remains the preferred confirmation. Source: https://arkivkopia.se/bok/runeberg-acj330bio.

## 4. Lorenz Heinrich Frederiksen — what the independent research can and cannot establish

Rigsarkivet's current guidance confirms that cases from 1919–1970 began with the police; disputed paternity was decided by the civil court; maintenance/alimentation files are held in the county archive. It recommends starting with the county's alimentation journal, ordinary journal and case files, then checking civil-court case lists/judgment books and police records if needed: https://www.rigsarkivet.dk/vejledning/faderskab-og-adoption/faderskabssager-kom-godt-i-gang/.

The archive overview for Landsarkivet for Sønderjylland lists Aabenraa-Sønderborg Amt archives from 1932 onward, and says the 1920–1935 journal registers, journals and case files require an unprinted reading-room finding aid. This makes the Aabenraa-Sønderborg county archive a concrete next search location for the July 1932 registrar's letter and any associated paternity/maintenance case: https://www.rigsarkivet.dk/wp-content/uploads/2022/06/Landsarkivet-for-Soenderjylland-En-arkivoversigt.pdf.

I did not locate the actual paternity case, the 10 June 1932 judgment, or the complete underlying civil-register file in this web pass. Accordingly, the biological-father hypothesis (Sophus Petersen) remains unresolved. The church-register entry names Peter Frederiksen and Else Gedde Jensen as parents and refers to the registrar's letter; it is evidence of the register's recorded parentage, not proof of biological paternity.

## 5. Next research sequence

1. Obtain and inspect the original Skødstrup 1792 baptism page and trace Jochum through marriage, census and death records; then independently verify the parentage of Hans Peter Gaardsted (1852) and Jensine Gaardsted (1894).
2. Request the Aabenraa-Sønderborg Amt journal-register/journal and relevant case file for the July 1932 registrar's letter and Lorenz's paternity/maintenance proceedings. Search under Else Gedde Jensen, Peter Frederiksen, Wilhelm Krogh and Lorenz Heinrich Frederiksen, allowing for spelling variants.
3. Inspect the Rolsøgård 1787 probate folio 39 to identify Karen Christensdatter and determine whether she belongs in any existing line.
4. Preserve the von Woyten/Stojentin/Below relationships as source-supported in the JSON; if regenerating GEDCOM, include the three missing individuals and encode Christina's earlier marriage separately from her later marriage to Georg von Kleist.
5. Before any GEDCOM regeneration, audit every JSON person, parent, spouse, step/foster relationship, source and note against the export rules. A count match alone is insufficient.

## Method and limitations

- Compared 489 JSON person IDs with 485 GEDCOM INDI xrefs: four missing JSON people, zero GEDCOM-only people.
- External sources were used as corroboration and research directions, not as automatic imports.
- No new canonical relationship was written to the application data.
- The encrypted/private payload was not decrypted or inspected.
