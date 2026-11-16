FAMILY TREE EXPORT PACKAGE - "Slægten Gårdsted og Gedde" (sloev.github.io/tree)
================================================================================

CONTENTS
--------
family-tree-full-export.txt     Main export (15,000+ lines, all sections A-I):
                                A  index of all 523 persons
                                B  full person dossiers: dates, places over time,
                                   occupations, parents/spouse/children, works,
                                   media, every source with its resolved fetch URL
                                C  photo gallery (11 photos, see below)
                                D  related media links (17 external links)
                                E  documented works (books/music/art)
                                F  source registry + URL patterns
                                G  place gazetteer (~200 places with coordinates)
                                H  family lines + occupation categories
                                I  TREE EXPANSION 2026-11-16: 34 new ancestors
                                   (Gedde line one generation further back via DBL;
                                   von Kleist medieval chain back to 1289 via
                                   Harbou 1897 + Muttrin 2025), corrections,
                                   social connections, exact next records to fetch

family-tree-expanded.ged        NEW: GEDCOM 5.5.1 with all 523 persons and 159
                                families, built from the corrected parent links
                                (imports into any genealogy software)

family-tree.ged                 The site's own original GEDCOM (489 persons),
                                kept for reference - same person ids as the site

family-tree-data.json           The site's embedded DATA JSON, extracted verbatim
                                (489 persons, places, photos, links, sources, lines)

family-tree-data-expanded.json  Same data + the 34 new ancestors + corrected fields
                                for 18 existing persons (documented in Section I)

family-tree-images/             The 11 site photos, extracted from the base64
                                blobs embedded in the page HTML (the images/*.jpg
                                URLs on the site 404 - these JPGs are the real ones)

QUICK FACTS
-----------
- 523 person records (489 from the site + 34 new ancestors), 98 of them
  living/private: shown as "Privat person" (data is AES-encrypted on the site,
  only the owner password can decrypt - so they stay private here too)
- Sources: 626 source citations with resolved fetch URLs; new sources added:
  DBL (runeberg.org), MUT (v-kleist.com Muttrin PDF), Wikipedia, SNL,
  slaegtsbibliotek.dk
- Date formats preserved as on the site: "1922-09-20" full date, "2008-11" month,
  "ca. 1750"/"efter 1800" approximations
- arkiv.dk links return HTTP 403 to command-line fetchers but open in a browser
- All new persons are marked conf=probable/possible: documented in published
  genealogy/biography, not yet verified page-by-page in original archives

Generated 2026-11-16.
