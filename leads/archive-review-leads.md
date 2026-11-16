# Archive review: new leads from the uploaded family-tree export

Reviewed 2026-11-16 from the text export, JSON, GEDCOM and embedded JPGs in the supplied ZIP. These notes distinguish what the export says from what is visible in the scans. The original ZIP remains preserved in this directory.

## 1. Lorenz Heinrich Frederiksen — church-register entry and competing fatherhood claims

Visible in the supplied Broager Vestre district church-book scan (image 08 in the ZIP; the export identifies it as entry no. 1 in the 1932–33 register):

- Child: Lorenz Heinrich.
- Birth: 12 January 1932, Egernsund.
- The handwritten baptism date appears to be 17 January; recheck the full-resolution register if the exact date matters.
- Parents are written as worker Peter Frederiksen and wife Else Gedde Jensen, Egernsund.
- A note refers to a letter from the civil registrar (Personregisterføreren) dated 11 July 1932.

This is primary-source evidence for the parentage recorded by the church register, but it does not establish biological paternity. The separate family account that Sophus Petersen was the biological father remains a claim requiring the paternity file and/or DNA evidence. Keep legal/registered, biological and social/stepfather relationships distinct.

Other relevant scans in the ZIP:
- Sophus Petersen's 1903 Nybøl baptism entry names him as son of farmer Peter Petersen and wife Anna Cathrine Marie Petersen, née Petersen; the entry gives birth 28 June and baptism 24 July.
- The family gravestone photo gives Sofus Petersen of Paakjær's dates as 28 June 1903–24 August 1945, and names wife Christine Petersen née Jensen (1907–1985).
- The 1921 Nybøl census scan is captioned as Peter Petersen's household, with Detlef and Botilde Krogh at the top. This is regional context only; it does not prove any relationship between Wilhelm Krogh and Lorenz.

Next documentary step: obtain the 1932 paternity/maintenance case and the civil-register basis referred to by the church entry. Continue with Aabenraa-Sønderborg county archive alimentation/journal records and relevant civil court/police records already identified in the research notes. Do not change the biological father field on the strength of this church-book entry.

## 2. Jochum (Joachim) Gaardsted — Skødstrup baptism, 1792

The handwritten entry in the ZIP names “Hr. Forpagter Gaardsted paa Vosnæsgaard” and his wife Kirstine Marie Jørgensdatter; the child is named Jochum and the text appears to give 23 September as the birth date. This supports the Vosnæsgaard/Gaardsted household context. Check the full register page and catalogue metadata before using the exact date or wording to resolve identity or chronology.

The included 1839 drawing of Vosnæsgaard is contextual illustration, not proof of the 1792 household.

## 3. Liss (Lis) Pedersen — Silkeborg birth, 1931

The archive caption identifies Silkeborg church book, girls born 1931 no. 25: Lis Pedersen, born 18 April at Drewsensvej 14; parents machine worker Jens Nielsen Pedersen and Hulda Kristensen. The export links the image to Rigsarkivet image endpoint https://api.rigsarkivet.dk/ao/v1/images/28329752. Treat the caption as the supplied transcription until the original register is independently reread.

## 4. Evald Johannes Gaardsted-Jørgensen — Kolind birth, 1922

The archive caption identifies Kolind church book, boys born 1922 no. 6, with parents Aage Evald Oskar Jørgensen and Jensine Mariane Magdalene Gaardsted, and a marginal note concerning the 1985 name change. The export links the source to Arkivalieronline episode 17124596. Inspect the complete register page before transcribing the marginal note.

## 5. Gedde family photograph, 1895

The family-held photograph is captioned as Edvard Hammer Gedde and Mathilde Ludvigsen with their 12 children, apparently made as a silver-wedding gift in 1895. The caption identifies child no. 8 as Paula Mathilde Christle/Chrestle Gedde (“Laue”), later Jensen. Treat identities and birth-order mapping as family-caption identifications until independently corroborated.

## 6. Langø memoir pages

Two scans from Lisbeth Skov's En Langø-piges erindringer are captioned as describing her grandparents Marius and Ane Marie Christensen buying Langø in 1894 for 4,000 kroner and naming their children. This is a valuable family-history lead, not a substitute for the deed/tingbog or municipal records. Retain the plan to verify purchase and causeway history against land and local-government records.

## 7. Data-format checks before import

- Text export header: 489 people (98 private/living, 391 public).
- JSON people array: 489 records; 98 are redacted living/private records.
- GEDCOM: 485 individual records. The discrepancy is unexplained; do not assume identical person coverage.
- Structured JSON also reports 54 places, 7 family lines, 9 categories, 11 photos, 17 related links and 6 source groups.
- The previously identified duplicate person ID (p13) and rejected Bornholm Lars Larsen link remain data-integrity issues; do not overwrite canonical relationships without a reconciliation pass.
- The JSON also contains an encrypted private_blob. It was not decrypted or inspected and is excluded from the extracted working copy.

## Source references carried by the export

- Liss: https://api.rigsarkivet.dk/ao/v1/images/28329752
- Lorenz: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17216172
- Sophus: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17217126
- 1921 census: https://arkivalieronline.rigsarkivet.dk/da/billedviser?bsid=85824#85824,13856442
- Jochum: https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=24257049
- Vosnæsgaard drawing: https://arkiv.dk/vis/2780543

The complete export contains all 17 related-media links and the source registry.
