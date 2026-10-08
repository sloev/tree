"""Kildegrundlaget for stamtræet (source of truth).

Kør `python3 data/build_data.py` for at generere data/family.json.
Hver oplysning har en sikkerhedsgrad og så vidt muligt en arkivhenvisning:
  LL:<nøgle>  = Rigsarkivets Link Lives-post (https://link-lives.dk/soeg/)
  AO:<id>     = Arkivalieronline-billede (https://api.rigsarkivet.dk/ao/v1/images/<id>)
  DFS:<cid>   = Danish Family Search-post (https://www.danishfamilysearch.dk/cid<cid>)
  ARK:<id>    = arkiv.dk-post (https://arkiv.dk/vis/<id>)
  PHT:1897    = H.W. Harbou, "Slægten von Kleist i Danmark", Personalhistorisk Tidsskrift 1897 s. 95 ff.
                (https://www.v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf)

Sikkerhed (conf): told = oplyst af dig, record = arkivkilde, probable = sandsynlig, possible = mulig.
Ahnentafel-numre (ahnen) følger den biologiske slægt: far = 2n, mor = 2n+1.
"""
import json, os

# Steder: navn -> (bredde, længde, landsdel)
PLACES = {
    "Kolind": (56.358, 10.594, "Djursland"),
    "Tirstrup": (56.296, 10.688, "Djursland"),
    "Fuglslev": (56.305, 10.638, "Djursland"),
    "Rosmus": (56.302, 10.597, "Djursland"),
    "Ebeltoft": (56.195, 10.680, "Djursland"),
    "Hoed": (56.392, 10.790, "Djursland"),
    "Thorsager": (56.335, 10.453, "Djursland"),
    "Bregnet": (56.297, 10.479, "Djursland"),
    "Ørsted (Rougsø)": (56.533, 10.329, "Djursland"),
    "Vosnæsgaard, Skødstrup": (56.258, 10.364, "Aarhus-egnen"),
    "Bogensholm, Vistoft (Mols)": (56.205, 10.462, "Mols"),
    "Slagelse": (55.402, 11.354, "Sjælland"),
    "København": (55.676, 12.568, "København"),
    "Viby (Roskilde amt)": (55.548, 12.022, "Sjælland"),
    "Syv (Roskilde amt)": (55.566, 12.058, "Sjælland"),
    "Hoven": (55.857, 8.733, "Vestjylland"),
    "Skarrild": (56.023, 8.857, "Vestjylland"),
    "Herlufmagle": (55.322, 11.763, "Sjælland"),
    "Næstved": (55.230, 11.760, "Sjælland"),
    "Fredensborg": (55.975, 12.403, "Nordsjælland"),
    "Helsingør": (56.036, 12.613, "Nordsjælland"),
    "Malmö": (55.605, 13.003, "Skåne (Sverige)"),
    "Gjellerup / Hammerum": (56.135, 9.055, "Midtjylland"),
    "Hadsten": (56.327, 10.049, "Østjylland"),
    "Tamdrup": (55.900, 9.920, "Østjylland"),
    "Silkeborg": (56.170, 9.548, "Midtjylland"),
    "Lejrskov (Ferup)": (55.517, 9.297, "Sydjylland"),
    "Ollerup": (55.110, 10.523, "Fyn"),
    "Vester Starup": (55.660, 8.540, "Sydvestjylland"),
    "Fåborg (Varde)": (55.660, 8.690, "Sydvestjylland"),
    "Ringkøbing": (56.090, 8.244, "Vestjylland"),
    "Sønder Felding": (55.948, 8.786, "Vestjylland"),
    "Svendborg": (55.061, 10.607, "Fyn"),
    "Hune": (57.181, 9.660, "Nordjylland"),
    "Egernsund": (54.906, 9.603, "Sønderjylland"),
    "Broager": (54.889, 9.674, "Sønderjylland"),
    "Rinkenæs": (54.889, 9.553, "Sønderjylland"),
    "Ulkebøl": (54.913, 9.820, "Sønderjylland"),
    "Snogbæk": (54.937, 9.716, "Sønderjylland"),
    "Notmark (Als)": (54.990, 9.940, "Sønderjylland"),
    "Sønderborg": (54.909, 9.792, "Sønderjylland"),
    "Nybøl (Paakjær)": (54.928, 9.647, "Sønderjylland"),
    "Magleby (Nordenbro), Langeland": (54.815, 10.735, "Langeland"),
    "Humble (Kædeby), Langeland": (54.858, 10.695, "Langeland"),
    "Langø, Lindelse Nor": (54.876, 10.676, "Langeland"),
    "Lindelse": (54.880, 10.718, "Langeland"),
    "Rudkøbing": (54.937, 10.710, "Langeland"),
    "Skrøbelev": (54.945, 10.745, "Langeland"),
    "Tranekær": (55.000, 10.858, "Langeland"),
    "Tved (Svendborg)": (55.075, 10.662, "Fyn"),
}

# Slægtslinjer (farve i grafikken)
LINES = {
    "jorgensen": "Jørgensen-linjen",
    "gaardsted": "Gaardsted-linjen",
    "rousing": "Rousing-linjen (Fuglslev)",
    "maternal": "Morfars fars slægt: Petersen, Nybøl og Dybbøl",
    "gedde": "Gedde- og von Kleist-linjen",
    "frederiksen": "Stedfarens slægt (Frederiksen, Broager)",
    "larsen": "Mormors slægt: Larsen, Holgersen og Langø",
}

P = []
def person(id, name, sex, *, ahnen=None, line=None, rel=None, born=None, bplace=None,
           died=None, dplace=None, occ=(), conf="record", note=None, src=(), res=(),
           father=None, mother=None, living=False, sibof=None, step=None, spouse=None):
    P.append(dict(id=id, name=name, sex=sex, ahnen=ahnen, line=line, rel=rel,
                  born=born, bplace=bplace, died=died, dplace=dplace, occ=list(occ),
                  conf=conf, note=note, src=list(src), res=[list(r) for r in res],
                  father=father, mother=mother, living=living, sibof=sibof, step=step, spouse=spouse))

# ================= Dig og dine forældre =================
# ================= Bedsteforældre =================
person("p4", "Evald Johannes Gaardsted-Jørgensen", "M", ahnen=4, line="jorgensen",
       born="1922-09-20", bplace="Kolind", died="2008-11", dplace="Svendborg",
       father="p8", mother="p9", spouse="p5",
       occ=["Lærer", "Højskolelærer, Ollerup Gymnastikhøjskole", "Kordegn, Svendborg 1976–81",
            "Sognepræst, Hune og Rødhus (Jetsmark) 1981–89", "Forfatter"],
       res=[(1922, "Kolind", "født på Kolind Mark"), (1925, "Gjellerup / Hammerum", "barn på fattiggården, som faren bestyrede"),
            (1932, "Hadsten", "familien flyttede hertil; Ågade, senere Ballevej"), (1953, "Silkeborg", "lærereksamen, Silkeborg Seminarium"),
            (1965, "Ollerup", "lærer på Ollerup Gymnastikhøjskole"), (1976, "Svendborg", "kordegn"),
            (1981, "Hune", "sognepræst"), (1990, "Ollerup", "pensioneret, Toften 6"), (2003, "Svendborg", "efter Liss' død")],
       note="Døbt 8. okt. 1922 i Kolind Kirke af pastor J.P. Jensen. Faddere: enken Rasmine Kristine Gaardsted (farmor), "
            "fattiggårdsbestyrer Martin Marinus Gaardsted, Bregnet, og ungkarl Axel Vilhelm Alfred Gaardsted (morbrødre). "
            "Navneforandring til Gaardsted-Jørgensen ved navnebevis 1983/1985 (randnote). "
            "Romaner bl.a. 'De kom til en by' (1999, om flytningen til Hadsten 1932), 'Skriv hjem, Niels' og 'Jos og hans verden'; "
            "'Leck Fischer. Signalement af en digter' (1973). Hans personarkiv med en egen slægtstavle ligger i Hadsten Lokalarkiv (A37).",
       src=["AO:27841253 (Kolind kirkebog 1920–36, fødte drenge 1922 nr. 6)", "DFS:18978912 (folketælling 1925)", "ARK:2162357", "ARK:906257",
            "ARK:3079233", "ARK:7091946", "litteraturpriser.dk"])
person("p5", "Liss Gaardsted-Jørgensen (f. Pedersen)", "F", ahnen=5, line="jorgensen",
       born="1931-04-18", died="2002", occ=["Kordegn, uddannet i Hune"], spouse="p4", father="p10", mother="p11",
       note="Gift med Evald 1953, 22 år gammel; tre sønner. Et af syv søskende. Fødselsdatoen stammer fra Evalds personarkiv "
            "(Hadsten Lokalarkiv). Født 18. april 1931 på Drewsensvej 14 i Silkeborg og døbt 24. maj 1931 i Silkeborg Kirke (skrevet 'Lis'). "
            "Forældre: maskinarbejder Jens Nielsen Pedersen og Hulda Kristensen. Gudfar bl.a. hendes farfar, gårdejer Niels Pedersen.",
       src=["AO:Silkeborg kirkebog 1930–33, fødte piger 1931 nr. 25 (billede 28329752)", "ARK:2162357", "litteraturpriser.dk", "FamilySearch Family Tree: Liss Jørgensen (født Pedersen) 1931–2002"], bplace="Silkeborg",
       res=[(1953, "Ollerup", "gift"), (1981, "Hune", "")])
person("p6", "Lorenz Heinrich Frederiksen", "M", ahnen=6, line="maternal", conf="record",
       born="1932-01-12", bplace="Egernsund", died="2009-05-06", dplace="Svendborg", father="sofus", mother="p13",
       step="pf12", spouse="p7",
       res=[(1932, "Egernsund", "født; hjemmedøbt 1. jan. 1933"), (2009, "Svendborg", "død; begravet på Sankt Jørgens Kirkegård")],
       note="Det borgerlige fødselsregister for Egernsund (1932 nr. 4, anmeldt 16. jan. 1932) siger, at Else Gedde Frederiksen, "
            "f. Jensen, fødte ham 12. jan. 1932 kl. 5.30. En randnote af 11. juli 1932 siger, at landarbejder Wilhelm Krogh "
            "fra Snogbæk er den biologiske far. Det bygger på hans faderskabserklæring af 5. april 1932 og en retsafgørelse "
            "af 10. juni 1932. Stedfaren Peter Frederiksen gav drengen sit efternavn. "
            "Det stemmer med familiens fortælling om, at Lorenz først som voksen fandt ud af, at Peter ikke var hans far. "
            "Familiens viden er, at den biologiske far var gårdmandssønnen Sophus Petersen fra Påkjær i Nybøl, at landarbejder Wilhelm Krogh tog skylden, "
            "og at Peter Frederiksen blev betalt for at gifte sig med Else. Stamtræet følger familiens viden. "
            "Ifølge dåbsindførslen i Broager Vestre distrikt (1933 nr. 1) var fadderne stedfaren selv, "
            "arbejdsmand Lorenz Frederiksen og hustru Catharina, Egernsund, samt gårdejer Jens Jensens hustru fra Dalsgaard. "
            "Lorenz er begravet sammen med hustruen Gerda på Sankt Jørgens Kirkegård i Svendborg.",
       src=["AO:Egernsund standsregister, fødte 1928–33, 1932 nr. 4 (bsid 37658, billede 125)",
            "AO:Broager Vestre distrikt kontraministerialbog 1906–48, fødte 1933 nr. 1 (bsid 201141, billede 112)",
            "BillionGraves via MyHeritage (samling 10147): Lorenz H. Frederiksen, Sankt Jørgens Kirkegård, Svendborg",
            "MyHeritage: Folketælling 1940, 'Lorens Henrick Frederiksen'"])
person("p7", "Gerda Frederiksen (f. Larsen)", "F", ahnen=7, line="larsen", conf="record",
       born="1935-08-17", bplace="Magleby (Nordenbro), Langeland", died="2019-07-18", dplace="Svendborg", spouse="p6",
       father="p14", mother="p15",
       res=[(1935, "Magleby (Nordenbro), Langeland", "født; hjemmedøbt 18. aug. 1935"), (1950, "Magleby (Nordenbro), Langeland", "konfirmeret i Magleby Kirke"),
            (2019, "Svendborg", "død; begravet på Sankt Jørgens Kirkegård")],
       note="Født 17. aug. 1935 i Nordenbro, Magleby sogn på Sydlangeland, og hjemmedøbt dagen efter. Fremstillet i Magleby Kirke 3. nov. 1935. "
            "Forældre: tømrer Laurits Edvard Larsen og Karen Margrethe Holgersen. Faddere: gårdmand Johannes Nielsen og hustru, Haugbølle, "
            "samt bødker Aksel Holgersen, Kædeby (hendes morfar). "
            "Gennem sin mormor Kristine er hun oldebarn af Marius Christensen, 'Kongen af Langø', som købte øen Langø i Lindelse Nor i 1894 "
            "og i 1911 byggede dæmningen til Langeland. Begravet på Sankt Jørgens Kirkegård i Svendborg sammen med sin mand Lorenz.",
       src=["DFS:kbid157287 (Magleby kirkebog 1929–62, fødte piger 1935 nr. 13)", "DFS:kbid189407 (konfirmation 1950)",
            "BillionGraves via MyHeritage (samling 10147): Gerda Frederiksen, Sankt Jørgens Kirkegård, Svendborg", "Familiens oplysninger (pigenavn Larsen, Langø)"])
person("p14", "Laurits Edvard Larsen", "M", ahnen=14, line="larsen", born="1898-12-24", bplace="Magleby (Nordenbro), Langeland",
       father="p28", mother="p29", spouse="p15", occ=["Tømrer, Nordenbro (1935)"],
       res=[(1898, "Magleby (Nordenbro), Langeland", "født"), (1913, "Magleby (Nordenbro), Langeland", "konfirmeret"), (1935, "Magleby (Nordenbro), Langeland", "tømrer")],
       src=["LL:12-6022525", "LL:14-3799804", "LL:23-1129717", "LL:25-1187745", "DFS:kbid157287"])
person("p15", "Karen Margrethe Holgersen", "F", ahnen=15, line="larsen", born="1906-09-18", bplace="Humble (Kædeby), Langeland",
       father="p30", mother="p31", spouse="p14", res=[(1911, "Humble (Kædeby), Langeland", "hos forældrene"), (1935, "Magleby (Nordenbro), Langeland", "")],
       note="Datter af bødker Axel Erik Holgersen og Kristine Adamine Margrethe f. Christensen fra Langø.",
       src=["DFS:kbid157287", "LL:23-771415"])
person("p28", "Lars Thomsen Larsen", "M", ahnen=28, line="larsen", born="1859-11-01", bplace="Magleby (Nordenbro), Langeland",
       died="1911–1921", father="p56", mother="p57", spouse="p29",
       note="I folketællingen 1911 bor han i Magleby med hustruen Hansine og sønnerne Aksel Peder, Hans Sigurd og Laurits Edvard. Hansine er enke i 1921.",
       src=["LL:12-16296348", "LL:23-1129713"])
person("p29", "Hansine Petersen", "F", ahnen=29, line="larsen", born="1859-12-01", bplace="Magleby (Nordenbro), Langeland",
       father="p58", mother="p59", spouse="p28", res=[(1921, "Magleby (Nordenbro), Langeland", "enke, hos sønnen Laurits")],
       src=["LL:12-16299531", "LL:23-1129714", "LL:25-1187744"])
person("p30", "Axel Erik Holgersen", "M", ahnen=30, line="larsen", born="1882-07-26", bplace="Tved (Svendborg)",
       father="p60", mother="p61", spouse="p31", occ=["Bødkerlærling, Humble (1901)", "Bødker, Kædeby (1904–35)"],
       res=[(1882, "Tved (Svendborg)", "født på Tved Mark"), (1901, "Humble (Kædeby), Langeland", "bødkerlærling"), (1904, "Humble (Kædeby), Langeland", "gift"),
            (1935, "Humble (Kædeby), Langeland", "bødker, gudfar til barnebarnet Gerda")],
       note="Gift 26. juli 1904 i Humble med Kristine Adamine Margrethe Christensen fra Langø.",
       src=["LL:12-15691757", "LL:13-2027009", "LL:9-1908303", "LL:24-817272", "LL:25-805032", "DFS:kbid157287"])
person("p31", "Kristine Adamine Margrethe Christensen", "F", ahnen=31, line="larsen", born="1884-10-06", bplace="Rudkøbing",
       father="p62", mother="p63", spouse="p30", occ=["Tjenestepige, Humble (1901)"],
       res=[(1884, "Rudkøbing", "født"), (1898, "Humble (Kædeby), Langeland", "konfirmeret"), (1904, "Humble (Kædeby), Langeland", "gift")],
       note="Datter af 'Kongen af Langø', Marius Christensen. Hun er Gerdas mormor.",
       src=["LL:12-15579549", "LL:14-3122525", "LL:9-1908174", "LL:13-2027012", "LL:24-817273", "LL:25-805033"])
person("p56", "Lars Larsen", "M", ahnen=56, line="larsen", born="1832-08-30", bplace="Magleby (Nordenbro), Langeland", spouse="p57", father="p112", mother="p113",
       occ=["Daglejer ved landbruget, Magleby (1901)"],
       note="Gift 27. aug. 1859 i Magleby (Langeland) med Maren Christiansen.", src=["LL:12-16285744", "LL:13-5236614", "LL:12-16296349", "LL:7-1520193", "LL:22-1228475", "LL:9-1903457"])
person("p57", "Maren Christiansen", "F", ahnen=57, line="larsen", born="1837-05-03", bplace="Magleby (Nordenbro), Langeland", spouse="p56", father="p114", mother="p115", src=["LL:12-16287085", "LL:13-5236615", "LL:12-16296350", "LL:9-1903458"])
person("p58", "Peder Hansen Berentzen", "M", ahnen=58, line="larsen", born="1818-02-22", bplace="Lindelse", spouse="p59", father="p116", mother="p117",
       note="Gift 11. juni 1852 i Rudkøbing med Marthe Madsen.", src=["LL:12-15525501", "LL:13-5084744", "LL:12-16299532"])
person("p59", "Marthe Madsen", "F", ahnen=59, line="larsen", born="1823-09-07", bplace="Tranekær", spouse="p58", src=["LL:13-5084745", "LL:12-16299533"])
person("p60", "Peder Iver Holgersen", "M", ahnen=60, line="larsen", born="1851-12-10", bplace="Tved (Svendborg)", father="p120", mother="p121", occ=["Indsidder"], spouse="p61", res=[(1890, "Tved (Svendborg)", "")],
       note="Gift 26. nov. 1878 i Vor Frue Kirke, Svendborg, med Karen Nielsen.", src=["LL:12-15688495", "LL:13-5270320", "LL:12-15691758", "Familiens håndskrevne ark (Nordenbro)"])
person("p61", "Karen Nielsen", "F", ahnen=61, line="larsen", born="ca. 1855", spouse="p60", src=["LL:13-5270321", "LL:12-15691759"])
person("p62", "Marius Michelsen Christensen", "M", ahnen=62, line="larsen", born="1858-04-14", bplace="Rudkøbing",
       father="p124", mother="p125", spouse="p63",
       occ=["Landbruger og ejer af øen Langø (1894–)", "Bygger af Langø-dæmningen (1911)"],
       res=[(1858, "Rudkøbing", "født"), (1883, "Rudkøbing", "gift"), (1894, "Langø, Lindelse Nor", "købte Langø"), (1921, "Langø, Lindelse Nor", "")],
       note="'Kongen af Langø'. Han købte øen Langø i Lindelse Nor i 1894 sammen med hustruen Ane Marie, og i 1911 byggede han med håndkraft "
            "og hjælp fra sønner og svigersøn den 334 m lange dæmning, som gjorde øen landfast. Ifølge familien gik Langø senere i arv til "
            "efterkommere med navnet Pedersen. Flere af familiens slægtninge fra Sydlangeland udvandrede til Amerika. "
            "Barnebarnet Lisbeth Skov, født Christensen, fortæller i 'En Langø-piges erindringer', at øen før 1894 havde hørt under "
            "Hjortholm gods og siden tre gårde i Haugbølle, som brugte den til græsning: kreaturerne blev svømmet over om foråret og hjem om efteråret. "
            "En skomager havde købt øen og bygget et simpelt hus, men den kom på tvangsauktion, hvorefter Marius og Ane Marie købte den.",
       src=["LL:12-15570702", "LL:13-5085956", "LL:9-1827830", "LL:24-817715", "LL:25-805444", "Fyens Stiftstidende: Historien om en dæmning",
            "Lisbeth Skov f. Christensen: En Langø-piges erindringer (privattryk, familiens eksemplar)"])
person("p63", "Ane Marie Jørgensen", "F", ahnen=63, line="larsen", born="1859-09-07", bplace="Skrøbelev", spouse="p62", father="p126", mother="p127",
       res=[(1894, "Langø, Lindelse Nor", "")], src=["LL:12-15556964", "LL:13-5085957", "LL:9-1827831", "LL:25-805445"])
person("p112", "Lars Thomsen", "M", ahnen=112, line="larsen", spouse="p113", src=["LL:12-16285745"])
person("p113", "Anne Katrine Jensdatter", "F", ahnen=113, line="larsen", spouse="p112", src=["LL:12-16285746"])
person("p114", "Christian Hansen", "M", ahnen=114, line="larsen", born="ca. 1806", spouse="p115",
       note="Gift 13. nov. 1829 i Magleby (Langeland) med Marie Madsdatter.", src=["LL:13-5235043", "LL:12-16287086"])
person("p115", "Marie Madsdatter", "F", ahnen=115, line="larsen", born="ca. 1807", spouse="p114", src=["LL:13-5235044", "LL:12-16287087"])
person("p116", "Hans Jørgensen", "M", ahnen=116, line="larsen", spouse="p117", src=["LL:12-15525502"])
person("p117", "Kirsten", "F", ahnen=117, line="larsen", spouse="p116", note="Efternavnet er ikke indekseret.", src=["LL:12-15525503"])
person("p120", "Holger Eriksen", "M", ahnen=120, line="larsen", born="ca. 1814", spouse="p121",
       note="Gift 8. dec. 1838 i Tved (Svendborg) med Anne Cathrine Hansdatter.", src=["LL:13-5107079", "LL:12-15688496"])
person("p121", "Anne Cathrine Hansdatter", "F", ahnen=121, line="larsen", born="ca. 1815", spouse="p120", src=["LL:13-5107080", "LL:12-15688497"])
person("p126", "Jørgen Christensen", "M", ahnen=126, line="larsen", spouse="p127", src=["LL:12-15556965"])
person("p127", "Bodil Margrethe Clausen", "F", ahnen=127, line="larsen", spouse="p126", src=["LL:12-15556966"])
person("p124", "Christen Michelsen", "M", ahnen=124, line="larsen", spouse="p125", src=["LL:12-15570703"])
person("p125", "Rasmine Hansen", "F", ahnen=125, line="larsen", spouse="p124", src=["LL:12-15570704"])

person("p10", "Jens Nielsen Pedersen", "M", ahnen=10, line="jorgensen", born="1891-04-14", bplace="Vester Starup",
       father="p20", mother="p21", spouse="p11", res=[(1891, "Vester Starup", "født"), (1916, "Ringkøbing", "gift"), (1921, "Vester Starup", ""), (1925, "Silkeborg", "")],
       note="Gift 11. juni 1916 i Ringkøbing med Hulda Christensen. I 1925 bor familien i Silkeborg med døtrene Karen Margrethe (1917), Anna Elvira (1918) "
            "og Nelly (1921). Maskinarbejder i Silkeborg ved Liss' fødsel i 1931.",
       src=["AO:Silkeborg kirkebog 1931 nr. 25", "LL:12-9781230", "LL:13-2793204", "LL:25-2149351", "DFS:21838177 (folketælling 1925, Silkeborg)"])
person("p11", "Hulda Christensen", "F", ahnen=11, line="jorgensen", born="1895-09-25", bplace="Sønder Felding",
       father="p22", mother="p23", spouse="p10", res=[(1895, "Sønder Felding", "født i Ilderhede"), (1925, "Silkeborg", "")],
       src=["LL:12-5952889", "LL:13-2793207", "LL:25-2149352", "DFS:21838178"])
person("p20", "Niels Pedersen", "M", ahnen=20, line="jorgensen", born="1861-10-25", bplace="Vester Starup", spouse="p21", father="p40", mother="p41",
       occ=["Gårdejer (1931)"],
       note="Gift 29. nov. 1889 i Vester Starup med Ane Else Pedersen. Gudfar til barnebarnet Liss i 1931.", src=["LL:12-9787230", "LL:13-3654108", "LL:12-9781231", "AO:Silkeborg kirkebog 1931 nr. 25"])
person("p40", "Jens Pedersen", "M", ahnen=40, line="jorgensen", spouse="p41", src=["LL:12-9787231"])
person("p41", "Kirsten Marie Nielsen", "F", ahnen=41, line="jorgensen", spouse="p40", src=["LL:12-9787232"])
person("p42", "Peder Jensen", "M", ahnen=42, line="jorgensen", spouse="p43", src=["LL:12-11080622"])
person("p43", "Karen Johnsen", "F", ahnen=43, line="jorgensen", spouse="p42", src=["LL:12-11080623"])
person("p21", "Ane Else Pedersen", "F", ahnen=21, line="jorgensen", born="1859-04-14", bplace="Fåborg (Varde)", spouse="p20", father="p42", mother="p43", src=["LL:12-11080621", "LL:13-3654109", "LL:12-9781232"])
person("p22", "Mads Christensen (Kristensen)", "M", ahnen=22, line="jorgensen", spouse="p23", born="1852-01-18", bplace="Hoven",
       occ=["Husmand, Sønder Felding (1901)"],
       note="Født 18. jan. 1852 i Hoven sogn, søn af Christen Andersen og Kirsten Christensdatter. Gift 1875 i Grindsted med Karen Jensen. "
            "Husmand i Sønder Felding, hvor datteren Hulda blev født 1895.",
       src=["LL:12-8842498 (fødsel Hoven 1852)", "LL:13-3794323 (vielse Grindsted 1875)", "LL:9-1496473 (FT 1901 Sønder Felding)",
            "LL:23-1723336 (FT 1911, født i Hoven)", "LL:13-2793208", "LL:12-5952890"])
person("p23", "Karen Jensen", "F", ahnen=23, line="jorgensen", spouse="p22", born="1852-08-29", bplace="Skarrild",
       note="Født 29. aug. 1852 i Skarrild sogn, datter af Jens Peder Larsen og Kjersten Frederiksdatter. Vielsen i Grindsted 1875 "
            "giver samme dato og nævner faren; folketællingen 1901 skriver 29. juli.",
       src=["LL:12-8975343 (fødsel Skarrild 1852)", "LL:13-3794324 (vielse Grindsted 1875)", "LL:9-1496474 (FT 1901)", "LL:7-1186700 (FT 1880, født i Skarrild)",
            "LL:13-2793209", "LL:12-5952891"])

# ================= Oldeforældre =================
person("p8", "Aage Evald Oskar Jørgensen", "M", ahnen=8, line="jorgensen", born="1890-10-17", bplace="Slagelse",
       father="p16", mother="p17", spouse="p9",
       occ=["Natvægter, København (1918)", "Gårdbestyrer, Kolind (1921–22)", "Bestyrer af Gjellerup fattiggård (1925)"],
       res=[(1890, "Slagelse", "født"), (1918, "København", "natvægter"), (1921, "Kolind", "i familien Gaardsteds hus"),
            (1925, "Gjellerup / Hammerum", "bestyrer af Gjellerup fattiggård"), (1932, "Hadsten", "flyttede hertil med familien")],
       note="Gift med Jensine Gaardsted i Kolind Kirke 29. okt. 1921.",
       src=["LL:12-16940206", "LL:9-1795573", "LL:17-1153878", "LL:25-1032486", "AO:27841253", "DFS:18978910"])
person("p9", "Jensine Mariane Magdalene Gaardsted", "F", ahnen=9, line="gaardsted", born="1894-06-06", bplace="Kolind",
       father="p18", mother="p19", occ=["Tjenestepige, København (1915)"], spouse="p8",
       res=[(1894, "Kolind", "født"), (1915, "København", "tjenestepige"), (1925, "Gjellerup / Hammerum", "bestyrerens hustru"), (1932, "Hadsten", "")],
       src=["LL:9-1332311", "LL:14-3965870", "LL:17-936099", "AO:27841253", "DFS:18978911"])
person("s_ester", "Ester Kristine Jørgensen", "F", rel="Evalds søster", line="jorgensen", born="1924", father="p8", mother="p9",
       src=["DFS:18978913"])

person("p12", "Wilhelm Krogh", "M", rel="tog skylden: anerkendte faderskabet til Lorenz i 1932", line="maternal", born="1908-10-09",
       occ=["Landarbejder (karl), Snogbæk (1932)"], res=[(1932, "Snogbæk", "landarbejder")],
       note="Ifølge familien tog han skylden for gårdmandssønnen Sophus Petersen fra Påkjær. I det borgerlige register står han som Lorenz' far. Født 9. okt. 1908 i 'Tastrup' (eller 'Vastrup'; skriften er svær at læse), "
            "Landkreis Flensburg, dengang i Tyskland. Faderskabet står i randnoten i Egernsund-registret: han anerkendte "
            "faderskabet 5. april 1932, og retten afgjorde sagen 10. juni 1932. Hans forældre og hans videre liv er endnu ikke fundet. "
            "De står i tyske registre (Flensburg). Der boede en anden Krogh-familie i Nybøl: arbejder Detlef Krogh (f. 8. maj 1905), gift 1929 i Broager "
            "med Cecilie Marie f. Hansen, fik døtre i Nybøl 1936 og 1940. I 1921 boede Detlef Krogh (f. 1849) og Botilde (f. 1850) i Nybøl. "
            "De kan være Wilhelms bror og bedsteforældre, men det er ikke bekræftet.",
       src=["AO:Egernsund standsregister, fødte 1928–33, 1932 nr. 4, randnote 11.7.1932 (bsid 37658, billede 125)", "AO:Nybøl kirkebog 1931–58, fødte piger 1936 og 1940 (Detlef Krogh)"])
person("sofus", "Sophus (Sofus) Petersen", "M", ahnen=12, line="maternal", conf="told",
       born="1903-06-28", bplace="Nybøl (Paakjær)", died="1945-08-24", dplace="Nybøl (Paakjær)", father="sofus_f", mother="sofus_m",
       res=[(1903, "Nybøl (Paakjær)", "født på forældrenes gård"), (1945, "Nybøl (Paakjær)", "død; begravet på Nybøl Kirkegård")],
       spouse="sofus_w", occ=["Gårdmandssøn, Påkjær gård i Nybøl", "Gårdejer, Nybøl (1938–43)"],
       note="Født 28. juni 1903 og døbt 24. juli 1903 i Nybøl Kirke (kirkebogen 1903 nr. 12) som søn af gårdmand ('Hufner') Peter Petersen "
            "og hustru Anna Cathrine Marie f. Petersen i Nybøl. Faddere: gæstgiver Johannes Hansen i Hostrup, tjenestekarl Jürgen Jacobsen "
            "i Nybøl og ugift Marie Iversen i Schottsbüllfeld. Fødselsdatoen passer præcist med gravstenen på Nybøl Kirkegård. "
            "Familien har fået at vide, at Lorenz' far hed Sophus og var fra Påkjær gård i Nybøl, og at han som gårdmandssøn ikke kunne vedstå "
            "faderskabet. I stedet tog landarbejder Wilhelm Krogh skylden: han anerkendte faderskabet i 1932, og retten stadfæstede det, så det er "
            "Krogh, der står i standsregistret. Påkjær ligger i Nybøl sogn tæt ved Snogbæk, hvor Krogh "
            "var karl i 1932. Sophus døde kun 42 år gammel. Han og hustruen Christine fik tre døtre: Gerda og to andre, hvoraf "
            "den ene flyttede til Norge. De er Lorenz' halvsøstre. En DNA-test kan bekræfte slægtskabet.",
       src=["AO:Nybøl kirkebog 1880–1931, dåb 1903 nr. 12 (bsid 202179, billede 88)", "LL:12-15057041 (indekseret med dåbsdatoen 24.7.1903)",
            "Gravsten på Nybøl Kirkegård (foto fra familien): 'Minde over en elsket Mand og Fader Sofus Petersen, Paakjær, * 28. Juni 1903 † 24. Aug. 1945'",
            "Familiens oplysninger", "AO:Nybøl kirkebog 1931–58, fødte piger 1938 nr. 6, 1940 nr. 4, 1943 nr. 5"])
person("sofus_w", "Christine Petersen (f. Jensen)", "F", rel="Sophus Petersens hustru", line="maternal", born="1907-02-21", bplace="Notmark (Als)",
       note="Gift med Sophus i Nybøl Kirke i efteråret 1937 (kirkebogen angiver både 2. oktober og 2. november 1937). Født i Notmark; kirkebogen 1940–43 angiver fødselsåret 1908, gravstenen 1907.",
       died="1985-06-25", dplace="Nybøl (Paakjær)", spouse="sofus", conf="record",
       src=["Gravsten på Nybøl Kirkegård (foto fra familien): 'og vor kære Moder Christine Petersen f. Jensen * 21. Feb. 1907 † 25. Juni 1985'"])
person("sofus_f", "Peter Petersen", "M", ahnen=24, line="maternal", born="1866-09-22", bplace="Nybøl (Paakjær)",
       spouse="sofus_m", father="sofus_ff", mother="sofus_fm", occ=["Gårdmand (landmand), Nybøl"], conf="record",
       note="Søn af Mathias Petersen. Gift 6. juni 1895 i Nybøl med Anna Cathrine Marie Petersen. I folketællingen 1921 er han landmand i Nybøl "
            "med hustru, børnene Peter, Jørgen, Marie, Hans og Viggo, en tjenestekarl og to tjenestepiger.",
       src=["LL:13-4983073", "LL:12-15059287", "LL:25-6006023", "AO:Nybøl kirkebog 1903 nr. 12"])
person("sofus_m", "Anna Cathrine Marie Petersen", "F", ahnen=25, line="maternal", born="1869-08-12", bplace="Dybbøl", spouse="sofus_f",
       father="sofus_mf", mother="sofus_mm",
       conf="record", note="Datter af Lorenz Petersen. Født i Rageböl ifølge folketællingen 1921.",
       src=["LL:13-4983076", "LL:12-14359019", "LL:25-6006024"])
person("p13", "Else Gedde Jensen", "F", ahnen=13, line="gedde", conf="record",
       born="1912-08-31", bplace="Lejrskov (Ferup)", father="p26", mother="p27", spouse="pf12",
       res=[(1912, "Lejrskov (Ferup)", "født på forældrenes gård i Ferup"), (1932, "Egernsund", "gift med Peter Frederiksen")],
       note="Født 31. aug. 1912 i Ferup, Lejrskov sogn, og døbt 20. okt. 1912 i Lejrskov Kirke. Faddere: frøken Mathilde Gedde, "
            "København (moster/grandtante på Gedde-siden), Kirstine Jensen og købmand Jørgen Jensen, Haderslev. "
            "Her kommer navnet Gedde fra: Else fik det som mellemnavn efter sin mor, Paula Gedde. "
            "I januar 1932 var hun gift med arbejdsmand Peter Frederiksen i Egernsund.",
       src=["AO:Lejrskov kirkebog, fødte piger 1912 nr. 17 (bsid 165996, billede 94)", "LL:12-4852565",
            "AO:Egernsund standsregister 1932 nr. 4", "AO:Broager Vestre 1933 nr. 1"])
person("pf12", "Peter Frederiksen", "M", rel="Lorenz' stedfar; ifølge familien betalt for at gifte sig med Else", line="frederiksen", born="1902-02-15",
       bplace="Egernsund", father="p24", mother="p25", spouse="p13",
       occ=["Tjenestekarl, Broager (1921)", "Arbejdsmand, Egernsund (1932)"],
       note="Gift med Else Gedde Jensen. Han står som far i Lorenz' dåbsindførsel, og Lorenz fik hans efternavn, "
            "men ifølge randnoten i det borgerlige register er han ikke den biologiske far. Familien fortæller, at han blev betalt for at gifte sig med Else.",
       src=["LL:12-15018348", "LL:14-2208771", "LL:25-5954688", "AO:Egernsund standsregister 1932 nr. 4", "AO:Broager Vestre 1933 nr. 1"])

# ================= Tipoldeforældre =================
person("p16", "Jørgen Anton Jørgensen", "M", ahnen=16, line="jorgensen", born="1857-10-06", bplace="København",
       died="1914-08-04", dplace="Slagelse", father="p32", mother="p33", spouse="p17",
       occ=["Typograf, København", "Typograf, Sorø Amts Bogtrykkeri, Slagelse"],
       res=[(1857, "København", "født, Vor Frue sogn"), (1886, "København", "gift"), (1889, "Slagelse", "flyttede hertil"), (1914, "Slagelse", "død")],
       note="Gift med Lovisa Larsson 31. jan. 1886 i Sankt Johannes Kirke, København.",
       src=["LL:12-13117126", "LL:14-7547225", "LL:7-586580", "LL:13-4147709", "LL:9-1795568", "LL:11-230038"])
person("p17", "Lovisa (Louise) Larsson", "F", ahnen=17, line="jorgensen", born="1862-06-28", bplace="Malmö",
       died="1910-10-12", dplace="Slagelse", father="p34", occ=["Tjenestepige, København (1885)"], spouse="p16",
       res=[(1862, "Malmö", "født"), (1885, "København", "tjenestepige"), (1901, "Slagelse", "")],
       src=["LL:8-200847", "LL:9-1795569", "LL:11-231267"])
person("p18", "Hans Peter Gaardsted", "M", ahnen=18, line="gaardsted", born="1852-05-03", bplace="Tirstrup",
       died="1913-03-26", dplace="Kolind", father="p36", mother="p37", spouse="p19",
       occ=["Tjenestekarl, Ebeltoft (1880)", "Husmand/parcellist, Kolind"],
       res=[(1852, "Tirstrup", "født"), (1880, "Ebeltoft", "tjenestekarl"), (1883, "Kolind", "husmandsstedet 'Petersminde', Højsletvej")],
       src=["LL:12-3665481", "LL:7-1041647", "LL:9-1332308", "LL:11-3881351"])
person("p19", "Rasmine Christine Andersen", "F", ahnen=19, line="rousing", born="1855-09-16", bplace="Fuglslev",
       died="efter 1922", father="p38", mother="p39", spouse="p18",
       res=[(1855, "Fuglslev", "født"), (1880, "Ebeltoft", ""), (1890, "Kolind", ""), (1922, "Kolind", "enke, gudmor til Evald")],
       src=["LL:12-9158976", "LL:6-849934", "LL:25-1032484", "AO:27841253"])
person("p26", "Jens Jensen", "M", ahnen=26, line="gedde", born="1866-12-31", bplace="Dybbøl", father="p52", mother="p53", spouse="p27",
       occ=["Gårdejer, Ferup (Lejrskov)"], res=[(1907, "København", "gift"), (1912, "Lejrskov (Ferup)", "gårdejer")],
       note="Søn af Rasmus Jensen og Christine Hansen. Gift 29. okt. 1907 i Mariendal Kirke, København, med Paula Gedde. "
            "Muligvis den 'gårdejer Jens Jensen, Dalsgaard', hvis hustru var gudmor til Lorenz i 1933. Det er ikke bekræftet.",
       src=["LL:12-14358775", "LL:13-432734", "LL:12-4852564", "AO:Lejrskov kirkebog 1912 nr. 17"])
person("p27", "Paula Mathilde Christle Gedde", "F", ahnen=27, line="gedde", born="1880-12-30", bplace="Tamdrup",
       father="p54", mother="p55", spouse="p26", res=[(1880, "Tamdrup", "født på faderens gård"), (1907, "København", "gift"),
       (1912, "Lejrskov (Ferup)", "gårdejerkone")],
       note="Mor til mindst fem børn i Lejrskov 1908–13 (navnene på de yngste er skjult i indekset af hensyn til privatlivet).",
       src=["LL:13-432737", "LL:12-4851845", "LL:12-4852565", "AO:Lejrskov kirkebog 1912 nr. 17"])

person("p24", "Lorenz Heinrich Frederiksen", "M", rel="stedfarens far", line="frederiksen", born="1870-01-23", bplace="Broager",
       died="1957-01-04", dplace="Egernsund", father="p48", mother="p49", occ=["Arbejdsmand, Egernsund (1932)"], spouse="p25",
       note="Gift med Cathrina Maria Magdalena Hansen 8. okt. 1895 i Broager. Gudfar og navnefar til Lorenz i 1933. "
            "Medlem af den danske forening DSK i 1942 (medlemskort i Broagerlands Lokalarkiv).",
       res=[(1870, "Broager", "født"), (1921, "Broager", "folketælling"), (1932, "Egernsund", "")],
       src=["LL:12-14989547", "LL:12-14313283", "LL:13-1051959", "LL:25-5953605", "ARK:1158725", "AO:Broager Vestre 1933 nr. 1"])
person("p25", "Cathrina Maria Magdalena Hansen", "F", rel="stedfarens mor", line="frederiksen", born="1872-12-28", bplace="Broager",
       father="p50", mother="p51", spouse="p24", src=["LL:12-14990795", "LL:13-1051962", "LL:25-5953606"])

# ================= 5. generation =================
person("p32", "Niels Jørgensen", "M", ahnen=32, line="jorgensen", born="ca. 1826", died="1885–1892", dplace="København",
       spouse="p33", occ=["Høker, København (1860)", "Arbejdsmand, København (1880–85)"],
       res=[(1860, "København", "høker"), (1885, "København", "arbejdsmand")],
       note="Gift 7. juli 1854 i Vor Frue Kirke, København, med Johanne Sophie Hansdatter. Fødestedet er skrevet 'Hove/Høje sogn, Svendborg amt'; sognet er ikke identificeret.",
       src=["LL:13-4281756", "LL:6-420495", "LL:7-586576", "LL:8-31142"])
person("p33", "Johanne Sophie Hansen (Hansdatter)", "F", ahnen=33, line="jorgensen", born="1825", bplace="Syv (Roskilde amt)",
       died="ca. 1910", dplace="København", occ=["Tjenestepige i Syv (1840)", "Enke på alderdomsunderstøttelse (1901)"], spouse="p32",
       note="Født 1825 i Syv sogn ved Roskilde, datter af gartner Hans Jensen og Margrethe Pedersdatter. Faren havde været gartner på Vibygård, "
            "derfor står hun senere som født i Viby. Konfirmeret i Syv 1839, tjenestepige 1840, rejste fra sognet 1841–45.",
       src=["LL:12-13566085 (fødsel Syv 1825)", "LL:2-680489 (FT 1834 Syv)", "LL:14-8189952 (konfirmation Syv 1839)", "LL:3-794367 (FT 1840 Syv, tjeneste)",
            "LL:15-1948556 (afgang Syv 1845)", "LL:6-420496", "LL:9-407995", "LL:17-1567270"])
person("p34", "Niels Larsen", "M", ahnen=34, line="jorgensen", bplace="Malmö", note="Svensk; nævnt i datterens dødsindførsel.",
       src=["LL:11-231268"])
person("p36", "Jochum (Joachim) Gaardsted", "M", ahnen=36, line="gaardsted", born="1792-09-23", bplace="Vosnæsgaard, Skødstrup",
       died="1865-06-18", dplace="Tirstrup", father="p72", mother="p73", spouse="p37",
       occ=["Gårdmand og sognefoged, Tirstrup"],
       res=[(1792, "Vosnæsgaard, Skødstrup", "født på herregården, som faren forpagtede"), (1801, "Bogensholm, Vistoft (Mols)", "barn på farens gods"),
            (1833, "Rosmus", "andet ægteskab"), (1834, "Tirstrup", "gårdmand og sognefoged til sin død")],
       note="Døbt 2. okt. 1792 i Skødstrup Kirke. Fadderne var bl.a. majorinde Weinegel, generalinde Trampe, "
            "major Folsch i Aarhus og Sehested i Fredericia. Første hustru var Marie Kjerstine Christensdatter. "
            "Han giftede sig anden gang 19. okt. 1833 i Rosmus med Ane Sophie Jensdatter.",
       src=["AO:Skødstrup kirkebog 1780–1809, s. 75 (bsid 736476, billede 43)", "LL:1-475273", "LL:2-530881", "LL:5-717919", "LL:13-1706737", "LL:11-1962320"])
person("p37", "Ane Sophie Jensdatter", "F", ahnen=37, line="gaardsted", born="1812-02-16", bplace="Rosmus",
       died="1886-02-27", dplace="Tirstrup", spouse="p36",
       note="Født 16. feb. 1812 i Attrup, Rosmus sogn, datter af gårdmand Jens Hansen og Mette Pedersdatter; hjemmedøbt 17. feb. "
            "Rosmus' fødsler før 1814 er ikke indekseret; posten er læst direkte i kirkebogen. Folketællingerne 1834–45 giver også 1812 og Rosmus.",
       src=["AO:Rosmus kirkebog 1789–1816, 1812 fødte piger (billede 28238652)", "LL:4-726530 (FT 1845, født i Rosmus)", "LL:2-530882", "LL:13-1706738", "LL:11-1962058"])
person("p38", "Anders Rasmussen Rousing", "M", ahnen=38, line="rousing", born="1818-03-12", bplace="Fuglslev",
       died="1886-12-20", dplace="Fuglslev", father="p76", mother="p77", spouse="p39",
       occ=["Boelsmand, Fuglslev (1845)", "Gårdmand, Fuglslev (1850–60)", "Aftægtsmand (1880)"],
       note="Gift med Mariane Hansdatter 3. sep. 1841 i Fuglslev.",
       src=["LL:12-3667395", "LL:13-3522464", "LL:6-849928", "LL:11-4601883"])
person("p39", "Mariane Hansdatter", "F", ahnen=39, line="rousing", born="1817-04-11", bplace="Fuglslev",
       died="1885-07-26", dplace="Fuglslev", father="p78", mother="p79", occ=["Tjenestepige på Fuglslev Mølle (1834–40)"], spouse="p38",
       src=["LL:12-3667695", "LL:2-515660", "LL:11-4602105"])
person("p52", "Rasmus Jensen", "M", ahnen=52, line="gedde", born="1838-10-16", bplace="Broager", spouse="p53", father="p104", mother="p105",
       note="Gift 18. sep. 1866 i Dybbøl med Anne Christine Hansen; sønnen Jens blev født i Dybbøl nytårsaften samme år.",
       src=["LL:12-15007344", "LL:13-4977279", "LL:12-14358776", "LL:13-432735"])
person("p53", "Anne Christine Hansen", "F", ahnen=53, line="gedde", spouse="p52", father="p106", mother="p107",
       src=["LL:13-4977282", "LL:12-14358777", "LL:13-432736"])
person("p104", "Jens Jensen", "M", ahnen=104, line="gedde", spouse="p105", src=["LL:13-4977280"])
person("p105", "Ane Cathrine Christensen", "F", ahnen=105, line="gedde", spouse="p104", src=["LL:13-4977281"])
person("p106", "Hans Hansen", "M", ahnen=106, line="gedde", spouse="p107", src=["LL:13-4977283"])
person("p107", "Ellen Kock", "F", ahnen=107, line="gedde", spouse="p106", src=["LL:13-4977284"])
person("p110", "Johan Alexander Ludvigsen", "M", ahnen=110, line="gedde", spouse="p111", res=[(1847, "Næstved", "")], src=["LL:12-17734084"])
person("p111", "Margaretha Dorothea Elisabeth Bølin", "F", ahnen=111, line="gedde", spouse="p110", src=["LL:12-17734085"])
person("p54", "Edvard Hammer Gedde", "M", ahnen=54, line="gedde", born="1845-09-08", bplace="Herlufmagle", died="1925-12-27",
       father="p108", mother="p109", spouse="p55",
       occ=["Proprietær, Tamdrup (1880)", "Vognmand og foderstofhandler, København"],
       res=[(1845, "Herlufmagle", "født"), (1870, "Næstved", "gift"), (1880, "Tamdrup", "proprietær"), (1907, "København", "vognmand")],
       note="Gift 8. juli 1870 i Sankt Peders Kirke, Næstved, med Vitta Ludvigsen. Mellemnavnet Hammer har han efter "
            "farens plejefar, dr.theol. Edvard Snedorph Hammer, sognepræst i Herlufmagle.",
       src=["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)", "LL:5-674514", "LL:13-5702405", "LL:7-1280754", "LL:13-432738", "LL:11-652493"])
person("p55", "Vitta Dorthea Henriette Mathilde Ludvigsen", "F", ahnen=55, line="gedde", born="1847-10-04", bplace="Næstved", father="p110", mother="p111",
       died="1927-01-17", spouse="p54", note="Kaldt Mathilde.", src=["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)", "LL:12-17734083", "LL:6-812043", "LL:13-5702406", "LL:7-1280755", "LL:13-432739"])
person("p48", "Peter Christian Frederiksen", "M", rel="stedfarens farfar", line="frederiksen", born="1839-05-04", bplace="Rinkenæs",
       father="p96", mother="p97", spouse="p49", note="Gift med Anna Kirstine Marie Paulsen 9. dec. 1860 i Broager.",
       src=["LL:12-14275364", "LL:13-4957004", "LL:12-14989548"])
person("p49", "Anna Kirstine Marie Paulsen", "F", rel="stedfarens farmor", line="frederiksen", born="1834-11-11", bplace="Ulkebøl",
       died="1893-05-22", dplace="Broager", father="p98", mother="p99", spouse="p48",
       src=["LL:12-15092343", "LL:13-4957007", "LL:11-7302858"])
person("p50", "Carl Peter Hansen", "M", rel="stedfarens morfar", line="frederiksen", born="1842-05-24", bplace="Egernsund", died="1909",
       father="p100", mother="p101", spouse="p51", src=["LL:12-14990796", "LL:13-1051963"])
person("p51", "Eline Helene Marie Hansen", "F", rel="stedfarens mormor", line="frederiksen", born="1850-03-24", died="1894", spouse="p50",
       src=["LL:12-14990797", "LL:13-1051964"])

# ================= 6. generation =================
person("p72", "Claus Gaardsted", "M", ahnen=72, line="gaardsted", born="ca. 1750", died="1811",
       dplace="Bogensholm, Vistoft (Mols)", spouse="p73",
       occ=["Forpagter af Vosnæsgaard (1787–ca. 1796)", "Ejer af herregården Bogensholm (1796/97–1811)"],
       res=[(1787, "Vosnæsgaard, Skødstrup", "forpagter"), (1797, "Bogensholm, Vistoft (Mols)", "købte godset for 10.000 rdl.")],
       note="Gift to gange; Kirsten Marie Jørgensdatter var hans anden hustru. Enken solgte Bogensholm på auktion i 1811 for 31.000 rdl. "
            "Han kom til Vosnæsgaard efter 1784. Hvor han er født, og hvem hans forældre var, er ukendt.",
       src=["LL:0-414804", "LL:1-475533", "AO:Skødstrup kirkebog 1780–1809, s. 75", "Trap Danmark / danskeherregaarde.dk (Bogensholm)"])
person("p73", "Kirsten Marie Jørgensdatter", "F", ahnen=73, line="gaardsted", born="ca. 1752", died="efter 1811", spouse="p72",
       src=["LL:0-414805", "LL:1-475272"])
person("p76", "Rasmus Jensen Rousing", "M", ahnen=76, line="rousing", born="ca. 1780", bplace="Fuglslev",
       died="1858-05-25", dplace="Fuglslev", father="p152", mother="p153", spouse="p77",
       occ=["Selvejergårdmand og sognefoged, Fuglslev"], src=["LL:2-515582", "LL:11-4601884", "LL:11-4601476"])
person("p77", "Karen Christensdatter", "F", ahnen=77, line="rousing", born="ca. 1780", died="1855-04-25", dplace="Fuglslev",
       spouse="p76", src=["LL:2-515583", "LL:11-4601630"])
person("p78", "Hans Jacobsen", "M", ahnen=78, line="rousing", born="ca. 1794", spouse="p79",
       note="Gift med Maren Rasmusdatter 6. juli 1817 i Fuglslev.", src=["LL:13-1705838", "LL:12-3667696"])
person("p79", "Maren Rasmusdatter", "F", ahnen=79, line="rousing", born="ca. 1798", spouse="p78", src=["LL:13-1705839"])
person("p108", "Ove Frederik Christopher Gedde", "M", ahnen=108, line="gedde", born="1808-07", bplace="Fredensborg",
       father="p216", mother="p217", spouse="p109",
       occ=["Cand.jur.", "Forvalter, Herlufmagle (1840–50)"],
       res=[(1808, "Fredensborg", "født, hjemmedøbt"), (1823, "Herlufmagle", "konfirmeret"),
            (1834, "København", "cand.jur., plejesøn af dr. Hammer"), (1840, "København", "gift i Helligånds Kirke"),
            (1845, "Herlufmagle", "forvalter")],
       note="Hjemmedøbt i Fredensborg, indført i kirkebogen 24. juli 1808 som søn af 'Hr. Capitaine ved Kronens Regiment Hr. Ove Samuel "
            "Giedde og Frue Frederikke Lovise Birthe født Kleist'. Faddere: oberstløjtnantinde Recke, jomfru Gradman fra Helsingør, "
            "kaptajn Giedde fra Helsingør og løjtnanterne Tønnesen og Bøgtrup. Han voksede op i Herlufmagle Præstegård hos sin moster "
            "Christine Sophie von Kleist og hendes mand, sognepræst dr.theol. Edvard Snedorph Hammer. "
            "Gift 16. okt. 1840 i Helligånds Kirke, København, med Charlotte Frederikke Christine Møller. "
            "I 1840–50 bestyrede han Viborggaard i Herlufmagle for mosteren, der var enke og ejede gården. Hendes bror, "
            "pensionist Ludvig Adam Kleist, boede der også. Begge var født i Assens.",
       src=["AO:Fredensborg Slotssogn kirkebog 1733–1814, s. 127 (bsid 594366, billede 65)", "LL:2-251474", "LL:14-7607995",
            "LL:3-593931", "LL:4-652578", "LL:5-674512", "PHT:1897"])
person("p109", "Charlotte Frederikke Christine Møller", "F", ahnen=109, line="gedde", born="1815", bplace="København", spouse="p108",
       src=["LL:5-674513"])
person("p96", "Friedrich Friedrichsen (Frederik Frederiksen)", "M", rel="stedfarens oldefar", line="frederiksen", spouse="p97",
       src=["LL:13-4957005"])
person("p97", "Anna Christina Peters (Christensen)", "F", rel="stedfarens oldemor", line="frederiksen", born="ca. 1815",
       note="Født i Vester Hostrup ifølge folketællingen.", spouse="p96", src=["LL:13-4957006"])
person("p98", "Jens Paulsen", "M", rel="stedfarens oldefar", line="frederiksen", born="ca. 1799", spouse="p99",
       occ=["Daglejer, Sønderborg (1845)"], note="Gift 24. feb. 1833 i Ulkebøl med Cathrine Marie Lausen.",
       src=["LL:13-4995190", "LL:4-956554", "LL:13-4957008", "LL:11-7302859"])
person("p99", "Cathrine Marie Lausen (Lorenzen)", "F", rel="stedfarens oldemor", line="frederiksen", born="ca. 1805", spouse="p98",
       src=["LL:13-4957009", "LL:11-7302860"])
person("p100", "Peter Hansen", "M", rel="stedfarens oldefar", line="frederiksen", born="1803", occ=["Teglværksarbejder, Egernsund"],
       note="Født i Brejning ifølge folketællingen.", spouse="p101", src=["Link Lives: folketællinger for Broager sogn 1845–60"])
person("p101", "Anna Christina Jensen", "F", rel="stedfarens oldemor", line="frederiksen", born="1813",
       note="Født i Gudum ifølge folketællingen.", spouse="p100", src=["Link Lives: folketællinger for Broager sogn 1845–60"])

# ================= 7. generation og videre =================
person("p152", "Jens Rasmussen", "M", ahnen=152, line="rousing", born="ca. 1755", bplace="Fuglslev", conf="probable",
       father="p304", occ=["Bonde og gårdbeboer, Fuglslev"], spouse="p153",
       note="Rasmus Jensen, 20 år, bor i hans husstand i 1801.", src=["LL:1-473834", "LL:0-415717"])
person("p153", "Margrethe Christensdatter", "F", ahnen=153, line="rousing", born="ca. 1758", conf="probable", spouse="p152",
       src=["LL:1-473835"])
person("p304", "Rasmus Jensen", "M", ahnen=304, line="rousing", born="ca. 1718", bplace="Fuglslev", conf="possible",
       occ=["Bonde og gårdmand, Fuglslev (1787)"], note="Mulig far til Jens Rasmussen. Det bygger kun på navnemønsteret.",
       src=["LL:0-415357"])

person("p216", "Ove Samuel Gedde", "M", ahnen=216, line="gedde", born="1778-02-28", died="1843-03-10", dplace="Helsingør",
       father="p432", mother="p433", spouse="p217",
       occ=["Officer: sekondløjtnant, kaptajn (1808), oberstløjtnant og bataljonschef ved Kronens Regiment",
            "Karakteriseret oberst, ridder af Dannebrog", "Borgerrepræsentant, Helsingør (1823–38)"],
       res=[(1808, "Fredensborg", "kaptajn; sønnen Ove Frederik født"), (1834, "Helsingør", "oberstløjtnant, Kronens Regiment"),
            (1843, "Helsingør", "død")],
       note="Gift 24. juni 1806 med Frederikke Louise Dorthea von Kleist. Kaldes 'von Gedde' i folketællingen 1834, hvor familien bor "
            "i Helsingør med datteren Henriette (f. 1819). "
            "Han er familiens bedste bud på 'kaptajnen' i fortællingen om navnet Gedde: Else Gedde Jensens tipoldefar og kaptajn i 1808. "
            "Der er dog intet i kilderne om, at han var i Trankebar.",
       src=["AO:Fredensborg Slotssogn kirkebog 1808", "LL:2-80373", "LL:3-51002", "LL:11-5877418", "LL:14-7607995", "PHT:1897",
            "Geni: Ove Samuel Gedde (1778–1843)"])
person("p217", "Frederikke Louise Dorthea von Kleist", "F", ahnen=217, line="gedde", born="1786-01-05", died="1870-01-24",
       father="p434", mother="p435", spouse="p216", res=[(1834, "Helsingør", "officershustru")],
       note="Kirkebogen 1808 kalder hende 'Frederikke Lovise Birthe født Kleist'. Datter af kammerherre Christian Frederik von Kleist. "
            "Hendes søster Christine Sophie var gift med pastor Hammer i Herlufmagle, og søsteren Juliane med den norske "
            "generalmajor Nicolai Wilhelm Gedde, sandsynligvis Ove Samuels bror.",
       src=["PHT:1897", "LL:2-80374", "LL:3-51003", "AO:Fredensborg Slotssogn kirkebog 1808"])

person("p432", "Hans Christopher Gedde", "M", ahnen=432, line="gedde", born="1738", died="1817", conf="probable",
       father="p864", spouse="p433", occ=["Generalmajor (dansk-norsk hær)"],
       note="Stamfar til den norske Gedde-slægt. Hans søn Nicolai Wilhelm Gedde (1779–1833) giftede sig med Frederikke Louises "
            "søster. Geni angiver ham som far til Ove Samuel, men det er ikke bekræftet i en primærkilde.",
       src=["Store norske leksikon: Gedde (slekt)", "lokalhistoriewiki.no: Gedde (borgerlig slekt)", "Geni: Ove Samuel Gedde"])
person("p433", "Øllegaard Sophie Fischer", "F", ahnen=433, line="gedde", born="ca. 1752", conf="probable", spouse="p432",
       note="Kaldes andre steder 'Frederikke Christiane Fischer'.",
       src=["lokalhistoriewiki.no: Gedde (borgerlig slekt)", "Geni: Ove Samuel Gedde"])
person("p864", "Samuel Christoph Gedde", "M", ahnen=864, line="gedde", born="1691-07-14", bplace="København",
       died="1766-02-02", dplace="København", conf="probable",
       occ=["Officer: underkonduktør (1710) til generalmajor (1760)"],
       note="Far til ti børn, bl.a. Hans Christopher (f. 1738). Ifølge Store norske leksikon har den borgerlige Gedde-slægt "
            "sandsynligvis ingen forbindelse til den uddøde adelsslægt Gjedde, som Trankebars grundlægger, admiral Ove Gjedde, tilhørte.",
       src=["Store norske leksikon: Gedde (slekt)"])

person("p434", "Christian Frederik von Kleist", "M", ahnen=434, line="gedde", born="1743-08-25", died="1799-07-12",
       father="p868", mother="p869", spouse="p435",
       occ=["Kornet ved Holstenske Kyrassérregiment (1758)", "Eskadronchef, karakteriseret major (1774)", "Kammerherre (1779)",
            "Godsejer ved Bredsted"],
       note="Gift 3. dec. 1770 med Anna Margrethe Schubart. Fire sønner og fire døtre, bl.a. generalmajor Carl Gottlieb von Kleist.",
       src=["PHT:1897"])
person("p435", "Anna Margrethe Schubart", "F", ahnen=435, line="gedde", born="1753-04-03", died="1842-08-24",
       father="p870", mother="p871", spouse="p434", src=["PHT:1897"])
person("p868", "Christian Adam von Kleist", "M", ahnen=868, line="gedde", born="1705-10-01", bplace="København",
       died="1778-10-31", father="p1736", mother="p1737", spouse="p869",
       occ=["Page og hofjunker (1731)", "Amtmand i Rendsborg (1740) og landråd i Holsten", "Kammerherre (1746), gehejmeråd (1766)",
            "Landfoged i Bredsted (1768)"],
       note="Døbt i Vor Frelsers Kirke på Christianshavn. Ridder af Dannebrog 1759. Død i Bredsted og begravet i Slesvig Domkirke.",
       src=["PHT:1897", "Dansk biografisk Lexikon IX s. 219"])
person("p869", "Sophie Rosenkrantz", "F", ahnen=869, line="gedde", born="1714", died="1770-06-04",
       father="p1738", mother="p1739", spouse="p868", note="Dame de l'Union parfaite 1752. Begravet i Slesvig Domkirke.",
       src=["PHT:1897"])
person("p870", "Johan Valentin Schubart", "M", ahnen=870, line="gedde", occ=["Major i kavaleriet"], spouse="p871", src=["PHT:1897"])
person("p871", "Christiane Sophie Woldenberg", "F", ahnen=871, line="gedde", spouse="p870", src=["PHT:1897"])
person("p1736", "Cartz Ulrik von Kleist", "M", ahnen=1736, line="gedde", died="1722-11", father="p3472", mother="p3473",
       spouse="p1737",
       occ=["Premierløjtnant ved Fynske Infanteriregiment (1701)", "Kaptajn i Grenaderkorpset (1707)",
            "Oberstløjtnant (1712/1717)", "Herre til Drenow (Pommern)"],
       note="Fra Muttrin-linjen af den pommerske adelsslægt von Kleist. Han var i brandenborgsk tjeneste 1692–94 og "
            "i dansk tjeneste fra 1701. Han blev såret og taget til fange ved Helsingborg i 1710 og ved Gadebusch i 1712. "
            "Han døde i Rendsborg og blev begravet 17. nov. 1722. Parret fik 10 børn.",
       src=["PHT:1897"])
person("p1737", "Barbara Juliane von Kleist", "F", ahnen=1737, line="gedde", died="efter 1730", father="p3474", mother="p3475",
       spouse="p1736", note="Boede endnu i 1730 på godset Drenow i Pommern.", src=["PHT:1897"])
person("p1738", "Christian Rosenkrantz til Skovsbo", "M", ahnen=1738, line="gedde", occ=["Gehejmeråd", "Godsejer, Skovsbo (Fyn)"],
       spouse="p1739", src=["PHT:1897"])
person("p1739", "Frederikke Louise Krag", "F", ahnen=1739, line="gedde", spouse="p1738", src=["PHT:1897"])
person("p3472", "Pribislaff von Kleist", "M", ahnen=3472, line="gedde", spouse="p3473",
       occ=["Godsejer: Muttrin, Borntin, Döbel og Drenow (Pommern)"], src=["PHT:1897"])
person("p3473", "Esther von Kameke", "F", ahnen=3473, line="gedde", spouse="p3472", src=["PHT:1897"])
person("p3474", "Christian Casimir von Kleist", "M", ahnen=3474, line="gedde", born="1654", died="1722-02-01",
       father="p6948", mother="p6949", spouse="p3475",
       occ=["Premierløjtnant ved Prins Christians Regiment (1677)", "Kaptajn og chef for grenaderkompagniet ved Fynske Infanteriregiment (1685)",
            "Oberstløjtnant og kommandant i Oldenborg (1709)"],
       note="Arvede en del af Gross Tychow i Pommern. Han deltog i felttoget i hertugdømmerne i 1700 og døde i Oldenborg.",
       src=["PHT:1897"])
person("p3475", "Anna von Fürst", "F", ahnen=3475, line="gedde", died="1722", spouse="p3474", note="Fra Schlesien.", src=["PHT:1897"])
person("p6948", "Christian von Kleist", "M", ahnen=6948, line="gedde", died="1679",
       spouse="p6949", occ=["Brandenborgsk oberst", "Godsejer, Gross Tychow (Pommern)"],
       note="Stamfar til den gren af slægten, der 'i henimod halvandet hundrede år blomstrede i Danmark'.", src=["PHT:1897"])
person("p6949", "Hedvig Maria von Kleist", "F", ahnen=6949, line="gedde", father="p13898", mother="p13899", spouse="p6948",
       note="Hans første hustru. Hun bragte en del af Gross Tychow med ind i ægteskabet.", src=["PHT:1897"])
person("p13898", "Georg von Kleist", "M", ahnen=13898, line="gedde", occ=["Godsejer, Gross Tychow (Pommern)"], spouse="p13899",
       src=["PHT:1897"])
person("p13899", "Christina von Woyten", "F", ahnen=13899, line="gedde", spouse="p13898", src=["PHT:1897"])

# ================= Søskende og andre slægtninge (bredde) =================
def sibs(parents, line, rel, rows):
    f, m = parents
    for i, (name, sex, born, extra) in enumerate(rows):
        person(f"s_{f}_{i}", name, sex, rel=rel, line=line, born=born, father=f, mother=m,
               occ=extra.get("occ", []), died=extra.get("died"), note=extra.get("note"), src=extra.get("src", []),
               spouse=extra.get("spouse"))

sibs(("p16", "p17"), "jorgensen", "Aages søskende", [
    ("Johanne Marie Margrethe Jørgensen", "F", "1886-10-21", {"note": "Tvilling."}),
    ("Niels Sophus Holger Jørgensen", "M", "1886-10-21", {"note": "Tvilling."}),
    ("Agnes Ingeborg Jørgensen", "F", "1888-07-30", {}),
    ("Karl Alfred Peter Jørgensen", "M", "1892-10-24", {}),
    ("Ellen Sophie Elisabeth Jørgensen", "F", "1895-01-07", {}),
    ("Anna Louise Mathilde Jørgensen", "F", "1899-12-26", {}),
])
sibs(("p32", "p33"), "jorgensen", "Jørgen Antons søskende", [
    ("Hans Sophus Frederik Jørgensen", "M", "1855", {"occ": ["Possementmager"]}),
    ("Anna Margrethe Jørgensen", "F", "1855-11-18", {"occ": ["Syerske"]}),
    ("Peter Jørgensen", "M", "1862-04-05", {"occ": ["Skomager"]}),
    ("Agnes Mathilde Jørgensen", "F", "1871-08-03", {"occ": ["Syerske"]}),
])
sibs(("p18", "p19"), "gaardsted", "Jensines søskende", [
    ("Johanne Marie Gaardsted", "F", "1879-01-29", {"occ": ["Tjenestepige"], "note": "Boede hos sin mor, der var enke, i Kolind i 1921. Hun og søsteren Sofie skrev erindringer om Petersminde (Midtdjurs Lokalhistoriske Arkiv A847)."}),
    ("Sofie Gaardsted", "F", "1881", {"occ": ["Tjenestepige"]}),
    ("Agnes Kristiane Gaardsted", "F", "1883", {"occ": ["Tjenestepige"]}),
    ("Jokum Gaardsted", "M", "1886", {}),
    ("Martin Marinus Gaardsted", "M", "1888-11-10", {"occ": ["Fattiggårdsbestyrer, Bregnet (1922)"]}),
    ("Axel Villiam Gaardsted", "M", "1891-08-20", {"died": "1894-03-07"}),
    ("Petra Ottine Gaardsted", "F", "1897-02-25", {}),
    ("Axel Vilhelm Alfred Gaardsted", "M", "1900-12-05", {}),
])
sibs(("p36", "p37"), "gaardsted", "Hans Peters søskende", [
    ("Marie Kirstine Gaardsted", "F", "1839", {}),
    ("Jens Gaardsted", "M", "1841", {"died": "1914", "occ": ["Gårdejer, Tirstrup"]}),
    ("Mette Marie Gaardsted", "F", "1844", {"died": "1847"}),
    ("Johanne Gaardsted", "F", "1847", {}),
    ("Ernst Adolph Gaardsted", "M", "1849", {}),
])
person("s_claus_ch", "Claus Christian Gaardsted", "M", rel="Hans Peters halvbror", line="gaardsted",
       born="1832-07-28", died="1863", father="p36", note="Mor: Marie Kjerstine Christensdatter (Jochums første hustru).")
sibs(("p72", "p73"), "gaardsted", "Jochums søskende", [
    ("Ernst Adolph Gaardsted", "M", "1784", {"died": "1832-06-13", "occ": ["Gårdmand, Hoed"], "note": "Gift med Anne Andersdatter Kræmer; mindst 5 børn i Hoed."}),
    ("Poul Christian Gaardsted", "M", "1790", {}),
])
sibs(("p38", "p39"), "rousing", "Rasmines søskende", [
    ("Rasmus Andersen", "M", "1845", {}), ("Hans Andersen", "M", "1847", {}),
    ("Søren Andersen", "M", "1850", {}), ("Jensine Caroline Andersen", "F", "1852", {}),
])
sibs(("p76", "p77"), "rousing", "Anders' søskende", [
    ("Christen Rasmussen", "M", "1812", {}), ("Jens Christian Rasmussen", "M", "1816", {}),
])
# Elses søskende (Lejrskov). Navnene på børn født efter 1908 er skjult i Link Lives af hensyn til privatlivet.
sibs(("p26", "p27"), "gedde", "Elses søskende", [
    ("Aage Rasmus Gedde Jensen", "M", "1908-07-24", {"died": "1908-07-29", "src": ["LL:11-2421115"]}),
    ("Barn (navn skjult i indekset)", "U", "1909-09-09", {"src": ["LL:12-4851907"]}),
    ("Barn (navn skjult i indekset)", "U", "1911-03-20", {"src": ["LL:12-4852004"]}),
    ("Barn (navn skjult i indekset)", "U", "1913-11-10", {"src": ["LL:12-4852952"]}),
    ("Mathilde Gedde Jensen", "F", None, {"note": "Nævnt som nr. V blandt Jens og Paulas børn i familiens opgørelse; kan være et af de børn, hvis navn er skjult i indekset.", "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)"]}),
    ("Svend Gedde Jensen", "M", None, {"note": "Nr. VI i familiens opgørelse.", "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)"]}),
    ("Helga Gedde Jensen", "F", None, {"note": "Nr. VII i familiens opgørelse.", "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)"]}),
])
sibs(("p54", "p55"), "gedde", "Paulas søskende", [
    ("Ove Frederik Alexander Gedde", "M", "1871-04-25", {"died": "1906-03-11", "occ": ["Premierløjtnant ved Dragonerne (til 1900)", "Næstkommanderende ved Grænsegendarmeriet"],
        "note": "Sendt hjemmefra som 10-årig til sin faster Margrethe Ahlefeldt og hendes mand, fordi han var bestemt for en militær karriere. Gift 25. april 1900 med Charlotte Sophie Hedemann (1876–1955). Børn: Knud Gedde (1901–1954) og Anna Sophie Mathilde Gedde (1902–1985), gift van Jepmond.",
        "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)", "LL:11-4055588", "LL:7-1280756"]}),
    ("Stephan Peder Hammer Gedde", "M", "1874-04-27", {"died": "1948-06-22", "occ": ["Landbrugsuddannet", "Forvalter ved De Forenede Papirfabrikker"],
        "note": "Holdt sammen med søsteren 'Tulle' det gamle hjem ved lige efter forældrenes død.", "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)", "LL:7-1280758"]}),
    ("Elisabeth Charlotte Chrestle Doris Gedde", "F", "1875-02-25", {"died": "1909-07-13", "occ": ["Lærerinde"],
        "note": "Kaldt 'Pelle'. Hjalp som storesøster med at opdrage de små. Døde efter en blindtarmsoperation.", "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)", "LL:11-652492", "LL:7-1280757"]}),
    ("Emil Ludvig Edvard Gedde", "M", "1876-11-15", {"died": "1951", "occ": ["Landbrugsuddannet", "Udvandrer til Argentina (1922)"],
        "note": "Udvandrede i 1922 til Argentina med hustruen Olivia (Johanne Marie Olivia f. Eddelsen) og to børn, og døde der i 1951. Sønnen Ejler blev i Argentina og døde omkring 1990 uden kendte børn. Datteren Inge Regitze (f. 1911, død ca. 1950) vendte tilbage til Danmark i 1930'erne og blev gift med Arne Meyer; ingen børn. "
                "Udvandrerarkivet har to billeder fra den danske koloni i Eldorado, Argentina: 'De ældste medlemmer af den danske koloni' (1920–30), hvor "
                "'Gedde, landbrugskandidat, over 50 år' sidder forrest, og en konfirmationsfest 27. okt. 1935 med 'fru Gedde' og 'hr Gedde'.",
        "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)", "LL:23-1448261", "LL:12-2288945", "LL:7-1280759",
                "Det Danske Udvandrerarkiv, billeder B9886 (PH-1983-1307) og B9790 (PH-1983-1334)"]}),
    ("Ove Gedde", "M", "1877-03-31", {"died": "1894", "note": "Skyllet over bord som jungmand på skoleskibet 'Georg Stage' i 1894.", "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)", "LL:7-1280760"]}),
    ("Vilhelm Gedde", "M", "1879", {"src": ["LL:7-1280761"]}),
    ("Olaf Christian Kleist Gedde", "M", "ca. 1880", {"occ": ["Kommis (handelsmedhjælper)", "Udvandrer til Shanghai, Kina (1904)"],
        "note": "Udvandrerprotokollen: 'Gedde, Olaf, kommis, født Horsens, sidste bopæl København, 24 år, rejsemål Shanghai, Kina', kontrakt 3534 (Haugsted), 11. juli 1904. Født på Tamdrup-gården ved Horsens ca. 1880.",
        "src": ["LL:7-1280762", "Det Danske Udvandrerarkiv, Udvandrerprotokollen (Københavns Politi), kontrakt 3534, 11/7 1904"]}),
    ("Ellen Gedde", "F", "1889-05-15", {"died": "1977-07-21", "occ": ["Kontoruddannet"], "note": "Gift med Aage Laurentzen; ingen børn.", "src": ["Familiens slægtsopgørelse 'Familien Gedde' (maskinskrevet, familiens eksemplar)"]}),
])
sibs(("p108", "p109"), "gedde", "Edvards søskende", [
    ("Emilie Sophie Frederikke Gedde", "F", "1842-07-07", {"src": ["LL:12-17170629"]}),
    ("Margrethe Ida Marie Gedde", "F", "1849-04-11", {"src": ["LL:12-17159973"]}),
    ("Ove Frederik Gedde", "M", "1850-12-11", {"died": "1907-10-24", "src": ["LL:12-17159130", "LL:11-561887"]}),
])
sibs(("p216", "p217"), "gedde", "Ove Frederiks søskende", [
    ("Wilhelm Edvardt Sophus von Gedde", "M", "1809", {"occ": ["Sekondløjtnant i Kronens Regiment (1834)"], "src": ["LL:2-25989"]}),
    ("Henriette von Gedde", "F", "1819", {"src": ["LL:2-80375"]}),
])
sibs(("p434", "p435"), "gedde", "Frederikke Louises søskende", [
    ("Christine Sophie von Kleist", "F", "1771-08-28", {"died": "1862-03-31", "note": "Født i Assens. Gift 1795 med sognepræst dr.theol. Edvard Snedorph Hammer (1767–1829), Herlufmagle, ejer af Viborggaard. De var plejeforældre for Ove Frederik Christopher Gedde. Hun var enke og ejede Viborggaard i 1850.", "src": ["PHT:1897", "LL:5-673677"]}),
    ("Adam Ludvig Vilhelm von Kleist", "M", "1772-10-16", {"died": "1851-10-06", "occ": ["Kaptajn og kompagnichef"], "note": "Født i Assens. Boede i 1850 på Viborggaard i Herlufmagle.", "src": ["PHT:1897", "LL:5-674516"]}),
    ("Valentin Ulrik von Kleist", "M", "1773-12-31", {"died": "1827-07-23", "occ": ["Major, husarregimentet"], "src": ["PHT:1897"]}),
    ("Frederik Christian von Kleist", "M", "1775-01-08", {"died": "1848-05-21", "occ": ["Major, Sjællandske Jægerkorps"], "src": ["PHT:1897"]}),
    ("Carl Gottlieb von Kleist", "M", "1778-01-15", {"died": "1849-07-26", "occ": ["Generalmajor og kammerherre"], "src": ["PHT:1897"]}),
    ("Juliane Frederikke Margrethe von Kleist", "F", "1781-12-02", {"died": "1861-05-22", "note": "Gift 1811 med Nicolai Wilhelm Gedde (1779–1833), norsk generalmajor og chef for Ingeniørkorpset.", "src": ["PHT:1897"]}),
    ("Henriette Louise von Kleist", "F", "1795-11-30", {"died": "1827-04-12", "note": "Gift 1813 med kaptajnløjtnant Johan Adolf von der Recke.", "src": ["PHT:1897"]}),
])
sibs(("p868", "p869"), "gedde", "Christian Frederiks søskende", [
    ("Frederikke Louise von Kleist", "F", "1747-03-27", {"died": "1814-05-29", "src": ["PHT:1897"]}),
])

person("sofus_ff", "Mathias Petersen", "M", ahnen=48, line="maternal", born="ca. 1832", spouse="sofus_fm",
       father="sofus_fff", mother="sofus_ffm", note="Gift 13. okt. 1865 i Nybøl med Sophia Maria Nissen.", src=["LL:13-4984314", "LL:12-15059288"])
person("sofus_fm", "Sophia Maria Nissen", "F", ahnen=49, line="maternal", born="1842-03-15", bplace="Nybøl (Paakjær)", spouse="sofus_ff",
       father="sofus_fmf", mother="sofus_fmm", src=["LL:12-15058141", "LL:13-4984317", "LL:12-15059289"])
person("sofus_mf", "Lorens Petersen", "M", ahnen=50, line="maternal", born="1831-02-26", bplace="Nybøl (Paakjær)", spouse="sofus_mm",
       father="sofus_mff", mother="sofus_mfm", note="Gift 12. april 1860 i Dybbøl med Marie Jørgensen.", src=["LL:12-14384545", "LL:13-4698057", "LL:12-14359020"])
person("sofus_mm", "Marie Jørgensen", "F", ahnen=51, line="maternal", born="1834-05-22", spouse="sofus_mf",
       father="sofus_mmf", mother="sofus_mmm", note="Fødestedet er indekseret som 'Borup sogn'.", src=["LL:13-4698060", "LL:12-14359021"])
for pid, nm, sx, rl, sp, k in [("sofus_fff", "Peter Petersen", "M", "Sophus' oldefar", "sofus_ffm", "LL:13-4984315"),
                               ("sofus_ffm", "Maria Cathrine Lorensen", "F", "Sophus' oldemor", "sofus_fff", "LL:13-4984316"),
                               ("sofus_fmf", "Rasmus Nissen", "M", "Sophus' oldefar", "sofus_fmm", "LL:13-4984318"),
                               ("sofus_fmm", "Maren Zachariasen", "F", "Sophus' oldemor", "sofus_fmf", "LL:13-4984319"),
                               ("sofus_mff", "Lorens Petersen", "M", "Sophus' oldefar", "sofus_mfm", "LL:13-4698058"),
                               ("sofus_mfm", "Marie Petersen", "F", "Sophus' oldemor", "sofus_mff", "LL:13-4698059"),
                               ("sofus_mmf", "Lorens Peter Jørgensen", "M", "Sophus' oldefar", "sofus_mmm", "LL:13-4698061"),
                               ("sofus_mmm", "Anna Kathrine Mathiesen", "F", "Sophus' oldemor", "sofus_mmf", "LL:13-4698062")]:
    person(pid, nm, sx, ahnen={"sofus_fff": 96, "sofus_ffm": 97, "sofus_fmf": 98, "sofus_fmm": 99, "sofus_mff": 100, "sofus_mfm": 101,
                                "sofus_mmf": 102, "sofus_mmm": 103}[pid], line="maternal", spouse=sp, src=[k])
sibs(("sofus_f", "sofus_m"), "maternal", "Sophus Petersens søskende", [
    ("Lorenz Peter Petersen", "M", "1897-09-04", {"src": ["LL:12-15056684"]}),
    ("Peter Petersen", "M", "1898-10-07", {"occ": ["Landbrug hos forældrene (1921)"], "src": ["LL:12-15056755", "LL:25-6006025"]}),
    ("Asmus Petersen", "M", None, {"died": "1899-09-04", "src": ["LL:11-7250842"]}),
    ("Jørgen Petersen", "M", "1904", {"src": ["AO:Folketælling 1921, Nybøl (bsid 85824)"]}),
    ("Marie Petersen", "F", "1906", {"src": ["AO:Folketælling 1921, Nybøl (bsid 85824)"]}),
    ("Hans Petersen", "M", "1910", {"src": ["AO:Folketælling 1921, Nybøl (bsid 85824)"]}),
    ("Viggo Petersen", "M", "1913", {"src": ["AO:Folketælling 1921, Nybøl (bsid 85824)"]}),
])
sibs(("p10", "p11"), "jorgensen", "Liss' søskende", [
    ("Karen Margrethe Pedersen", "F", "1917", {"note": "Senere gift Enevoldsen.", "src": ["DFS:21838180 (folketælling 1925, Silkeborg)", "FamilySearch Family Tree"]}),
    ("Anna Elvira Pedersen", "F", "1918", {"src": ["DFS:21838181 (folketælling 1925, Silkeborg)", "FamilySearch Family Tree"]}),
    ("Nelly Pedersen", "F", "1921", {"src": ["DFS:21838182 (folketælling 1925, Silkeborg)"]}),
])
sibs(("p62", "p63"), "larsen", "Kristines søskende (Langø-familien)", [
    ("Christian Anton Christensen", "M", "1879-06-17", {"note": "Født i Skrøbelev før forældrenes vielse.", "src": ["LL:12-15557976"]}),
    ("Christian Jørgen Christensen", "M", "1887-12-01", {"note": "Født i København; konfirmeret i Humble 1902. Ikke fundet i de danske folketællinger efter 1901 og er måske en af udvandrerne.", "src": ["LL:12-7820110", "LL:14-3121379"]}),
    ("Martha Hansine Christensen", "F", "1890-05-25", {"occ": ["Tjenestepige (1911–16)"], "src": ["LL:12-15581805", "LL:23-2150898", "LL:24-1720949"]}),
    ("Georg Johannes Christensen", "M", "1892-10-10", {"note": "Hjemme på Langø i 1921.", "src": ["LL:12-5963476", "LL:25-805446"]}),
    ("Jens Peter Christensen", "M", "1895-01-24", {"note": "Født på Langø.", "src": ["LL:12-4983047", "LL:14-3121869"]}),
    ("Valdemar Emil Christensen", "M", "1899-03-06", {"note": "Født på Langø; hjemme i 1921.", "src": ["LL:12-4983393", "LL:25-805447"]}),
])
sibs(("p60", "p61"), "larsen", "Axel Eriks søskende", [
    ("Holger Vilhelm Nielsen Holgersen", "M", "ca. 1881", {"src": ["LL:22-1332441"]}),
    ("Kristian Holgersen", "M", "ca. 1886", {"src": ["LL:22-1332443"]}),
    ("Iver Peder Holgersen", "M", "ca. 1889", {"occ": ["Arbejder", "Udvandrer til Fresno, Californien (1910)"],
        "note": "Udvandrerprotokollen: 'Holgersen, Iver Peder, arbejder, født Tved, sidste bopæl Skalbjerg, 22 år, rejsemål Fresno, USA', 8. sep. 1910, med damperen United States. Efterkommere kan leve i Californien.",
        "src": ["LL:22-1332444", "Det Danske Udvandrerarkiv, Udvandrerprotokollen (Københavns Politi), kontrakt 4443, 8/9 1910"]}),
])
sibs(("p56", "p57"), "larsen", "Lars Thomsens søskende", [
    ("Karoline Larsen", "F", "ca. 1864", {"src": ["LL:22-1228477"]}),
    ("Jensine Marentine Larsen", "F", "ca. 1870", {"src": ["LL:7-1520195"]}),
    ("Laurentine Sophie Larsen", "F", "ca. 1874", {"src": ["LL:7-1520196", "LL:22-1228478"]}),
    ("Peder Christian Larsen", "M", "ca. 1878", {"src": ["LL:7-1520197", "LL:22-1228479"]}),
    ("Thomas Larsen", "M", "ca. 1881", {"src": ["LL:22-1228480"]}),
])
sibs(("p28", "p29"), "larsen", "Laurits Edvards søskende", [
    ("Aksel Peder Larsen", "M", "1888-02-13", {"src": ["LL:23-1129715"]}),
    ("Hans Sigurd Larsen", "M", "1894-04-13", {"src": ["LL:23-1129716"]}),
])

sibs(("p24", "p25"), "frederiksen", "stedfarens søskende", [
    ("Søn (unavngivet)", "M", "1896", {"died": "1896-05-19"}),
    ("Eline Christine Frederiksen", "F", "1897-04-28", {}),
    ("Barn af Lorenz og Cathrina", "M", "1905-07-15", {}),
])
sibs(("p48", "p49"), "frederiksen", "Lorenz Heinrichs (f. 1870) søskende", [
    ("Hans Frederik Frederiksen", "M", "1862-10-28", {}),
    ("Jens Frederiksen", "M", "1865-07-04", {}),
    ("Catharina Maria Frederiksen", "F", "1867-04-24", {"note": "Gift med Hans Hendrik Ohlsen 17. juni 1888 i Broager."}),
    ("Anna Christine Maria Frederiksen", "F", "1874-02-10", {}),
])

# Erhvervskategorier til statistikken (søgeord matches mod erhverv i små bogstaver)
CATS = [("Kirke og præstegerning", ["præst", "kordegn"]), ("Undervisning og forfatterskab", ["lærer", "forfatter", "cand.jur"]),
        ("Officerer og hof", ["officer", "løjtnant", "kaptajn", "major", "oberst", "kornet", "kammerherre", "hofjunker", "amtmand", "gehejmeråd", "landfoged"]),
        ("Landbrug og godser", ["gård", "boelsmand", "husmand", "godsejer", "forpagter", "bonde", "proprietær", "forvalter", "herregård", "aftægt"]),
        ("Sognefoged og offentlige hverv", ["sognefoged", "borgerrepræsentant"]),
        ("Håndværk og tryk", ["typograf", "possement", "skomager", "syerske", "teglværk"]),
        ("Tjeneste og arbejde", ["tjeneste", "karl", "arbejdsmand", "landarbejder", "daglejer", "natvægter"]),
        ("Handel og vognmand", ["høker", "købmand", "vognmand"]), ("Fattigvæsen", ["fattiggård"])]

PHOTOS = [
    dict(file="images/liss-daab-silkeborg-1931.jpg", title="Farmor Liss' fødsel, Silkeborg 1931",
         caption="Silkeborg kirkebog, fødte piger 1931 nr. 25: 'Lis Pedersen', født 18. april på Drewsensvej 14. Forældre: maskinarbejder Jens Nielsen Pedersen og Hulda Kristensen.",
         credit="Rigsarkivet, Arkivalieronline", link="https://api.rigsarkivet.dk/ao/v1/images/28329752"),
    dict(file="images/langoe-erindringer.jpg", title="En Langø-piges erindringer",
         caption="Lisbeth Skov, født Christensen, barnebarn af Marius og Ane Marie: 'Min farfar og farmor, Marius og Ane Marie Christensen købte Langø i 1894.' Med luftfoto af dæmningen og stuehuset på Langø.",
         credit="Familiens eksemplar", link="https://da.wikipedia.org/wiki/Lindelse_Nor"),
    dict(file="images/sophus-daab-nybol-1903.jpg", title="Sophus' dåb, Nybøl 1903",
         caption="Nybøl kirkebog 1903 nr. 12: døbt 24. juli, født 28. juni, 'Sophus', ægte søn af gårdmand Peter Petersen og hustru Anna Cathrine Marie f. Petersen i Nybøl.",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17217126"),
    dict(file="images/sofus-petersen-gravsten.jpg", title="Sofus Petersens gravsten",
         caption="'Sofus Petersen, Paakjær, * 28. Juni 1903 † 24. Aug. 1945' og hustruen Christine Petersen f. Jensen (1907–1985). Gravstenen står på Nybøl Kirkegård. Familien formoder, at han var Lorenz' egentlige far.",
         credit="Foto fra familien", link="https://link-lives.dk/soeg/"),
    dict(file="images/nybol-folketaelling-1921.jpg", title="Nybøl, folketællingen 1921",
         caption="Gårdmand Peter Petersen i Nybøl med familie og tjenestefolk, og øverst Detlef og Botilde Krogh. Paakjær og Snogbæk ligger begge i Nybøl-egnen.",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?bsid=85824#85824,13856442"),
    dict(file="images/lorenz-baptism-broager-1933.jpg", title="Lorenz' dåb, Broager 1933",
         caption="Broager Vestre distrikts kirkebog, 1933 nr. 1: Lorenz Heinrich, født 12. jan. 1932 i Egernsund. Forældre: Peter Frederiksen og Else Gedde Jensen.",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17216172"),
    dict(file="images/evald-baptism-kolind-1922.jpg", title="Evalds fødsel, Kolind 1922",
         caption="Kolind kirkebog, fødte drenge 1922 nr. 6. Forældre: Aage Evald Oskar Jørgensen og Jensine Mariane Magdalene Gaardsted. Randnoten om navneforandringen 1985.",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17124596"),
    dict(file="images/jochum-baptism-skodstrup-1792.jpg", title="Jochums dåb, Skødstrup 1792",
         caption="'Hr. Forpagter Gaardsted paa Vosnæsgaard og hans Kone Kirstine Marie Jørgensdatter … Barnet var fød d. 23de Sept. … kaldet Jochum.'",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=24257049"),
    dict(file="images/vosnaesgaard-1839-rawert.jpg", title="Vosnæsgaard 1839",
         caption="Tegning af O.J. Rawert, 1839. Claus Gaardsted forpagtede herregården i 1780'erne og 90'erne, og Jochum blev født her.",
         credit="Rawert / Det Kgl. Bibliotek via Skødstrup Sogns Egnsarkiv", link="https://arkiv.dk/vis/2780543"),
]
LINKS = [
    ("Gjellerup fattiggård 1914 (Aage var bestyrer i 1925)", "https://arkiv.dk/vis/2636314"),
    ("Gruppebillede, Gjellerup fattiggård 1914", "https://arkiv.dk/vis/2636339"),
    ("Herregården Bogensholm (Claus Gaardsteds gods 1797–1811)", "https://arkiv.dk/vis/4033299"),
    ("Konfirmander i Rødhus Kirke 1988 med pastor Evald Gaardsted Jørgensen", "https://arkiv.dk/vis/5695529"),
    ("Hune Kirke", "https://arkiv.dk/vis/4306061"),
    ("Kolind station ca. 1920", "https://arkiv.dk/vis/4212435"),
    ("Tirstrup Kirke 1920", "https://arkiv.dk/vis/2623461"),
    ("Fuglslev Kirke", "https://arkiv.dk/vis/6189757"),
    ("Lorenz H. og Gerda Frederiksens gravsted, Sankt Jørgens Kirkegård, Svendborg (BillionGraves på MyHeritage)",
     "https://www.myheritage.dk/research/collection-10147/billiongraves?itemId=1483464614&action=showRecord"),
    ("Johanne og Sofie Gaardsteds erindringer om Petersminde (arkiv)", "https://arkiv.dk/vis/4407757"),
    ("Evald Gaardsted-Jørgensens personarkiv med hans egen slægtstavle (Hadsten)", "https://arkiv.dk/vis/2162357"),
    ("Udvandrerarkivet: De ældste medlemmer af den danske koloni i Eldorado, Argentina, med 'Gedde, landbrugskandidat' (1920–30)", "https://www.AalborgStadsarkiv.dk/UA_SoegISamlingen.asp?he=10714761249208"),
    ("Udvandrerarkivet: Konfirmation i Eldorado, Argentina, 27.10.1935, med hr. og fru Gedde", "https://www.AalborgStadsarkiv.dk/UA_SoegISamlingen.asp?he=2181393947310"),
    ("Udvandrerarkivets udvandrerprotokol (søg selv videre)", "https://www.aalborgstadsarkiv.dk/UA.asp?UA=UAProtokol"),
    ("Slægten von Kleist i Danmark (Personalhistorisk Tidsskrift 1897)", "https://www.v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf"),
    ("Admiral Ove Gjedde og grundlæggelsen af Trankebar (danmarkshistorien.lex.dk)",
     "https://danmarkshistorien.lex.dk/Grundl%C3%A6ggelsen_af_kolonien_Tranquebar,_1620-1630"),
]

# Kildetyper til kildeoversigten
SOURCES = [
    ("LL:", "Link Lives (Rigsarkivet)", "Indekserede kirkebøger 1557–1917 og folketællinger 1787–1921", "https://link-lives.dk/"),
    ("AO:", "Arkivalieronline (Rigsarkivet)", "Originale kirkebøger og standsregistre, læst direkte på billederne", "https://arkivalieronline.rigsarkivet.dk/"),
    ("DFS:", "Danish Family Search", "Folketællinger 1925–1940", "https://www.danishfamilysearch.dk/"),
    ("ARK:", "arkiv.dk", "Lokalarkiver: billeder, personarkiver, erindringer", "https://arkiv.dk/"),
    ("PHT:", "Personalhistorisk Tidsskrift 1897", "H.W. Harbou: Slægten von Kleist i Danmark", "https://www.v-kleist.com/FG_allg/Kleist_in_Daenemark.pdf"),
]

# ================= Automatisk fundne aner (tools/expand.py) =================
# Hvert led er fundet i Link Lives: fødselsposten navngiver forældrene, vielsen giver deres alder og fødested,
# og forældrenes egen fødselspost giver datoen. Kilderne er de præcise Link Lives-poster.
_auto_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auto_ancestors.json")
AUTO = json.load(open(_auto_path, encoding="utf-8")) if os.path.exists(_auto_path) else []
# Håndfundne led (læst i kirkebøger og folketællinger) ligger i manual_ancestors.json og går forud for de automatiske.
_man_path = os.path.join(os.path.dirname(_auto_path), "manual_ancestors.json")
MANUAL = json.load(open(_man_path, encoding="utf-8")) if os.path.exists(_man_path) else []
AUTO = MANUAL + [a for a in AUTO if not any(m["ahnen"] == a["ahnen"] and m.get("patch") == a.get("patch") for m in MANUAL)]
_by_ahnen = {p["ahnen"]: p for p in P if p.get("ahnen")}
for a in sorted(AUTO, key=lambda a: a["ahnen"]):
    k = a["ahnen"]
    if a.get("patch") and k in _by_ahnen:
        t = _by_ahnen[k]
        if a.get("born") and not t.get("born"): t["born"] = a["born"]
        if a.get("bplace_text") and not t.get("bplace"):
            if a["bplace_text"] in PLACES: t["bplace"] = a["bplace_text"]
            else: t["note"] = ((t.get("note") or "") + f" Født i {a['bplace_text']}.").strip()
        if a.get("note"): t["note"] = ((t.get("note") or "") + " " + a["note"]).strip()
        t["src"] = [s for s in a.get("src", []) if s not in t["src"]] + t["src"]
        continue
    if k in _by_ahnen or a.get("reject"): continue
    child = _by_ahnen.get(k // 2)
    if not child: continue
    bp = a.get("bplace_text") or None
    note = a.get("note") or ""
    if bp and bp not in PLACES: note += f" Født i {bp}."; bp = None
    person(a["id"], a["name"], a["sex"], ahnen=k, line=child.get("line"), born=a.get("born"), bplace=bp,
           died=a.get("died"), dplace=a.get("dplace"),
           occ=a.get("occ", ()), conf="record" if len(a.get("src", [])) > 1 else "told", note=note.strip(),
           src=a.get("src", []), spouse=f"a{k ^ 1}" if any(b["ahnen"] == k ^ 1 and not b.get("reject") and not b.get("patch") for b in AUTO) else None)
    _by_ahnen[k] = P[-1]
    child["father" if k % 2 == 0 else "mother"] = a["id"]

# ================= Private personer =================
# Nulevende og personer født inden for de sidste 100 år uden dødsdato står ikke i denne fil.
# De ligger krypteret i data/private.enc; her indlæses kun anonyme pladsholdere (data/private_stubs.json).
# Se data/private_tool.py for at redigere dem.
HERE = os.path.dirname(os.path.abspath(__file__))
STUBS = json.load(open(os.path.join(HERE, "private_stubs.json"), encoding="utf-8"))
P.extend(STUBS)
PRIVATE_BLOB = json.load(open(os.path.join(HERE, "private.enc")))

def must_be_private(p, this_year=2026):
    import re
    if p.get("private"): return False
    y = re.search(r"\d{4}", str(p.get("born") or ""))
    return bool(p.get("living") or (not p.get("died") and y and int(y.group()) >= this_year - 100))

if __name__ == "__main__":
    here = HERE
    leak = [p["id"] for p in P if must_be_private(p)]
    assert not leak, f"Disse personer skal flyttes til den krypterede fil: {leak}"
    ids = {p["id"] for p in P}
    assert len(ids) == len(P), "dublet-id"
    for p in P:
        for k in ("father", "mother", "sibof", "step", "spouse"):
            assert p[k] is None or p[k] in ids, (p["id"], k, p[k])
    json.dump(dict(people=P, places=PLACES, lines=LINES, cats=CATS, photos=PHOTOS, links=LINKS, sources=SOURCES, private_blob=PRIVATE_BLOB),
              open(os.path.join(here, "family.json"), "w"), ensure_ascii=False, indent=1)
    print(len(P), "personer")
