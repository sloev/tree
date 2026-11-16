# Review of new research-extension files

Reviewed: 16 November 2026

## Files reviewed

The following seven new files were present in `leads/`:
- `file-vx6.file` — research-extension overview, confidence/source key, and Line 1 (von Kleist / Muttrin)
- `file-5fb.file` — Line 2 (Gedde / Gjedde)
- `file-rag.file` — Line 3 (Gaardsted)
- `file-xdx.file` — Line 4 (Syv / Vibygård and Rosmus)
- `file-9cd.file` — Line 5 (Langeland / Magleby / Nordenbro / Snøde / Tved)
- `file-jsa.file` — Line 6 (Kresten, Langø household, emigrants, Wilhelm Krogh, Sophus' possible fourth daughter)
- `file-m4r.file` — Line 7 (South-West Jutland, Nybøl, Næstved, Malmö)

The files describe themselves as segments 1–7 of 8. Segment 8 (open questions, method and import checklist) was not present in the directory at the time of review. The overview claims 41 new people and four generations above the existing von Kleist line, but the person-level proposals have mixed confidence and must not be imported as a block.

## Overall assessment

This is a useful research-extension package, especially because it ties proposed changes to existing GEDCOM IDs, states confidence grades, identifies source codes, and separates new people from document schedules. The strongest material is the named archival-record work in the Gaardsted and Vibygård sections, the direct source conflict on Ove Samuel Gedde, and the explicit warning not to splice the two von Kleist reconstructions.

However, some entries marked A or B are more confident than the evidence currently warrants. In particular, an index extract is not the original probate, and a relationship inferred from an ambiguous index clause should not be imported as proven parentage. Treat the extension as a research plan and proposed patch, not an approved GEDCOM update.

## Critical corrections and cautions

### 1. Gaardsted: sibling clue strong; Tohde parentage not yet established

The G302 index entry for Niels Jensen Degn's probate (14 May 1787, no. 11, fol. 39) names Karen Christensdatter and describes Claus Gaardsted as her brother and tenant farmer at Vosnæsgård. It also refers to Christen Christensen Tohde, foged in Dejret, with a 1764 probate.

This is a strong lead for Karen and Claus as siblings. But the index's syntax — especially “afdødes stedbørn efter Christen Christensen Tohde? ... til datter Karen Christensdatter” — must be resolved against the original probate and the 1764 file. It does not yet safely establish that Tohde was the biological father of both Karen and Claus. The question mark attached to “Tohde” also means the surname transcription itself is uncertain.

Do not yet add Christen Christensen Tohde as father of Claus, change Claus's name to Claus Christensen, or assign a FAMC. First inspect the 1787 original and locate the 1764 probate. Also search Claus's own probate and the 1811 Bogensholm auction as the extension proposes.

Source index: https://slaegt.dk/media/jnnnvuml/alfabetisk-navneliste-og-skifteuddrag-til-rols%C3%B8g%C3%A5rd-gods-g302-mols-herred-1778-1816-1818.pdf
Secondary transcription: https://www.milloup.dk/hvh/download/skifter/rolsoegaard_gods_skifter.htm

### 2. Gedde: Ove Samuel's 1778/1788 conflict is real and significant

The new Gedde segment identifies the central issue correctly: the current GEDCOM has Ove Samuel born 28 February 1778, while Morten Clausen's genealogy gives 28 May 1788 in Fredrikstad and Anker's 1885 biography gives 28 May 1788. Harbou's 1897 article, “Slægten von Kleist i Danmark,” identifies Frederikke Louise Dorthea von Kleist's husband as Ove Samuel Gedde, born 28 February 1778 and died 10 March 1843. Anker identifies Hans Christopher Gedde as father of Ove Samuel, gives the 28 May 1788 birth, and names the two marriages of Hans Christopher.

Thus two substantial published genealogical sources identify the same Ove Samuel as the husband of Frederikke Louise and give different birth dates. This is not resolved by simply preferring one secondary source. The “two men merged” possibility raised by the extension is a legitimate hypothesis, but not proven by the ordinal in an online genealogy alone.

Sources:
- Anker 1885: https://runeberg.org/acj330bio/0110.html
- Harbou 1897: https://v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf
- Online genealogy lead: http://mortenclausen.dk/GEDHT/fam155xx/fam15556.htm

**Next decisive work:** inspect the original 1778 and 1788 baptism candidates, the 1806 marriage, and the 1843 Helsingør burial/death record. Keep both dates and the possible two-person hypothesis in the research notes until identity is resolved. The new file's confidence grade for Hans Christopher as father is too high if based only on Anker/Geni; it is a strong published-source claim, not a primary-record confirmation.

### 3. von Kleist: excellent documentary roadmap, but two chains must remain separate

The Damen volume (2025) explicitly identifies Dubislaff/Bratta as son of Henning (I.M.8) and Margarethe von Wedelstädt, names five sons in the 13 April 1477 collective enfeoffment, and states that the sons were enfeoffed in 1486 after their father's death. This is strong family-history evidence and gives specific charter references (125 and 192) for follow-up.

The extension appropriately warns that Chain A (the numbered Muttrin-Damen family-history line) and Chain B (Geneanet's Prissebur reconstruction) must not be spliced. The many Kameke/Borcke relationships are marked C and derive from Geneanet; they should remain hypotheses, not imported parentage.

One correction in the extension's C-1 should not be applied as written: the Muttrin family-history text available in the 2012 edition explicitly says Prissebur appears in Urkunde 83 of 1364 as “Prißebur, der Klest heißt von Muttrin.” The Damen volume separately says Jarislav brought Damen to the family around 1365. These are different statements. Keep the 1364 Muttrin documentary reference distinct from the c.1365 Damen acquisition. Recheck the precise 2025 Muttrin edition before editing the website's note.

Sources:
- 2025 Damen volume: https://www.v-kleist.com/FG/Muttrin/Damen.pdf
- Muttrin volume text (2012 edition): https://www.yumpu.com/de/document/view/7707886/geschlechts-v-kleist-familienverband-derer-v-kleist-ev
- Harbou 1897: https://v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf

### 4. Syv / Vibygård: the 1820 probate extract is valuable; identity remains C

The extension quotes a Vibygaard probate extract dated 31 December 1820 for Maren Poulsdatter, wife of Hans Jensen, gardener, naming four adult children: Poul, Jens, Peder and Ane. The occupational and geographic convergence with the existing Syv-branch Hans Jensen is compelling.

But the extension itself correctly says the identification is C until the 1822 Syv marriage entry confirms that the groom was a widower after Maren Poulsdatter. Do not yet add the four children, Maren, or a first FAM to the canonical GEDCOM. Inspect the cited Vibygaard probate leaves and the 1822 marriage entry first.

Source transcription: https://aurelia-clemons.dk/vibygdx.htm

### 5. Rosmus: preserve the two Mette candidates

The extension sets out Mette Pedersdatter Hallis and Mette Sørensdatter Helles as competing readings for the 6 July 1811 marriage. It recommends reading the original marriage entry and not changing the tree based on the tertiary GEDCOM extract. This is the right approach. Keep both candidates and the conflict visible until the original Rosmus register is read.

### 6. Kresten / Marthe: good evidence plan; no resolution yet

The extension preserves two possible Marthe Jørgensen identities and gives a sensible order of tests: full 1877 baptism entry, 1878 burial of candidate B, Magleby tilgangsliste, and later census/children checks. The foster-parent evidence favours candidate B as a hypothesis but does not prove maternity. Keep the mother unresolved.

### 7. Langeland, emigration, Malmö, Nybøl and other branches

Lines 5–7 are primarily document schedules rather than newly proven ancestry. They are valuable because they name the specific registers, date ranges, existing GEDCOM IDs and reasons to inspect them. Preserve them as open leads, not as new relationships.

Particularly useful searches:
- 1787 Nordenbro probate after Christian Hansen: possible sibling group for Christian Hansen who married in 1829, not a demonstrated link.
- Fangel, Snøde, Magleby, Humble, Tved and Rudkøbing church books: named register targets.
- Jørgen Christensen and Bodil Margrethe's nine children: seven reportedly emigrated; individual protocol entries and overseas records still needed.
- Iver Peder Holgersen (Fresno 1910), Olaf Gedde (Shanghai 1904), Emil Gedde (Argentina 1922): preserve existing protocol details and follow destination records.
- Wilhelm Krogh: resolve “Tastrup” vs “Vastrup” from the original marginal note before selecting a German locality/Standesamt.
- Sophus Petersen's fourth daughter: family report only; search Nybøl beyond the three located entries before assuming a fourth birth.
- Lovisa Larsson: Swedish parish and household examination records are the correct next route.
- Assing, Hoven, Sønder Felding, Nybøl and Næstved: good primary-register worklist.

The recommendation to scan and preserve the family-held “Dødsliste for Sydlangeland 1900–1970” and Langø memoir is also worth retaining as a source-preservation task.

## Recommended work order

1. **Ove Samuel identity/date:** original baptism candidates (1778 and 1788), 1806 marriage, 1843 burial.
2. **Gaardsted:** original G302 probate fol. 39 and the 1764 Tohde probate; then Claus's own probate/1811 auction.
3. **Vibygård:** 1822 Syv marriage entry and original 1820 Vibygaard probate.
4. **von Kleist:** reconcile Chain A with the numbered 2025 family-history references; inspect charter 125 (1477) and 192 (1486); keep Geneanet Chain B separate.
5. **Rosmus and Kresten:** inspect the exact original church-book entries.
6. **Emigration and regional register schedules:** work by parish and contract number, recording negative results.

## Import policy

Do not apply the extension's “41 persons” as a batch. For each proposed person or relationship, require:
- exact existing GEDCOM ID (where applicable);
- source and page/folio/image reference;
- a transcription or faithful abstract;
- relationship type (biological, legal, social, step, foster, guardian, spouse);
- confidence grade and reason;
- conflict/negative-search note;
- proof that the person is not already represented under another ID.

The extension's A/B/C/D labels are useful but should be recalibrated when a claim relies on an index extract, a tertiary tree, or an unverified transcription. No canonical data was changed in this review.
