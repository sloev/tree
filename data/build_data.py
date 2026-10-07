"""Source of truth for the family tree.

Run `python3 data/build_data.py` to regenerate data/family.json.
Every fact carries a confidence level and, where possible, an archive reference:
  LL:<key>  = Rigsarkivet Link Lives record (https://link-lives.dk/soeg/)
  AO:<id>   = Arkivalieronline image (https://api.rigsarkivet.dk/ao/v1/images/<id>)
  DFS:<cid> = Danish Family Search record (https://www.danishfamilysearch.dk/cid<cid>)
  ARK:<id>  = arkiv.dk record (https://arkiv.dk/vis/<id>)
"""
import json, os

# Places: name -> (lat, lon, region)
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
    "Vosnæsgaard, Skødstrup": (56.258, 10.364, "Aarhus area"),
    "Bogensholm, Vistoft (Mols)": (56.205, 10.462, "Mols"),
    "Slagelse": (55.402, 11.354, "Zealand"),
    "Copenhagen": (55.676, 12.568, "Zealand"),
    "Viby (Roskilde amt)": (55.548, 12.022, "Zealand"),
    "Malmö": (55.605, 13.003, "Scania, Sweden"),
    "Gjellerup / Hammerum": (56.135, 9.055, "Central Jutland"),
    "Hadsten": (56.327, 10.049, "East Jutland"),
    "Silkeborg": (56.170, 9.548, "Central Jutland"),
    "Ollerup": (55.110, 10.523, "Funen"),
    "Svendborg": (55.061, 10.607, "Funen"),
    "Hune": (57.181, 9.660, "North Jutland"),
    "Egernsund": (54.906, 9.603, "Southern Jutland"),
    "Broager": (54.889, 9.674, "Southern Jutland"),
}

P = []
def person(id, name, sex, *, ahnen=None, line=None, rel=None, born=None, bplace=None,
           died=None, dplace=None, occ=(), conf="record", note=None, src=(), res=(),
           father=None, mother=None, living=False, sibof=None):
    P.append(dict(id=id, name=name, sex=sex, ahnen=ahnen, line=line, rel=rel,
                  born=born, bplace=bplace, died=died, dplace=dplace, occ=list(occ),
                  conf=conf, note=note, src=list(src), res=[list(r) for r in res],
                  father=father, mother=mother, living=living, sibof=sibof))

# ---------------- Generation 1-2: you and parents ----------------
person("p1", "Johannes Gårdsted Valbjørn", "M", ahnen=1, line="self", living=True, conf="told",
       father="p2", mother="p3", note="Born Johannes Gårdsted Jørgensen.")
person("p2", "Jørgen Jørgensen", "M", ahnen=2, line="jorgensen", living=True, conf="told",
       father="p4", mother="p5")
person("p3", "Vivi Frederiksen Gedde", "F", ahnen=3, line="maternal", living=True, conf="told",
       father="p6", mother="p7")
person("u1", "Arne Gaardsted Jørgensen", "M", rel="uncle (father's brother)", line="jorgensen",
       living=True, conf="told", father="p4", mother="p5")
person("u2", "Ole Gårdsted Jørgensen", "M", rel="uncle (father's brother)", line="jorgensen",
       living=True, conf="told", father="p4", mother="p5")

# ---------------- Generation 3: grandparents ----------------
person("p4", "Evald Johannes Gaardsted-Jørgensen", "M", ahnen=4, line="jorgensen",
       born="1922-09-20", bplace="Kolind", died="2008-11", dplace="Svendborg",
       father="p8", mother="p9",
       occ=["Schoolteacher", "Folk high school teacher, Ollerup Gymnastikhøjskole", "Parish clerk (kordegn), Svendborg 1976–81",
            "Parish priest, Hune & Rødhus (Jetsmark) 1981–89", "Author"],
       res=[(1922, "Kolind", "born at Kolind Mark"), (1925, "Gjellerup / Hammerum", "child at the poorhouse his father managed"),
            (1932, "Hadsten", "family moved here; Ågade, then Ballevej"), (1953, "Silkeborg", "teacher's exam, Silkeborg Seminarium"),
            (1965, "Ollerup", "teacher at Ollerup Gymnastikhøjskole"), (1976, "Svendborg", "parish clerk"),
            (1981, "Hune", "parish priest"), (1990, "Ollerup", "retired, Toften 6"), (2003, "Svendborg", "after Liss's death")],
       note="Baptised 8 Oct 1922 in Kolind Church by pastor J.P. Jensen. Godparents: widow Rasmine Kristine Gaardsted (grandmother), "
            "poorhouse manager Martin Marinus Gaardsted of Bregnet and bachelor Axel Vilhelm Alfred Gaardsted (uncles). "
            "Surname formally changed to Gaardsted-Jørgensen by name certificate 1983/1985 (margin note). "
            "Novels incl. 'De kom til en by' (1999, about the move to Hadsten in 1932), 'Skriv hjem, Niels', 'Jos og hans verden'; "
            "'Leck Fischer. Signalement af en digter' (1973). His personal archive incl. a family tree is in Hadsten Lokalarkiv (A37).",
       src=["AO:27841253 (Kolind church book 1920–36, Fødte Mandkøn 1922 no. 6)", "DFS:18978912 (census 1925)", "ARK:2162357", "ARK:906257",
            "ARK:3079233", "ARK:7091946", "litteraturpriser.dk"])
person("p5", "Liss Gaardsted-Jørgensen (née Pedersen)", "F", ahnen=5, line="jorgensen",
       born="1931-04-18", died="2002", occ=["Parish clerk (kordegn), trained in Hune"],
       note="Married Evald 1953, aged 22; three sons (Jørgen, Arne, Ole). One of seven children; siblings include "
            "Karen Margrethe Enevoldsen (née Pedersen) and Ane Elvira Pedersen. Birth date from Evald's personal archive "
            "(Hadsten Lokalarkiv). Her parents are not yet identified.",
       src=["ARK:2162357", "litteraturpriser.dk", "FamilySearch Family Tree: Liss Jørgensen (født Pedersen) 1931–2002"], res=[(1953, "Ollerup", "married life"), (1981, "Hune", "")])
person("p6", "Lorenz Heinrich Frederiksen", "M", ahnen=6, line="maternal", conf="record",
       born="1932-01-12", bplace="Egernsund", died="2009-05-06", dplace="Svendborg", father="p12", mother="p13",
       res=[(1932, "Egernsund", "born; baptised at home 1 Jan 1933"), (2009, "Svendborg", "died; buried Sankt Jørgens Kirkegård")],
       note="Baptism entry (Broager Vestre distrikt 1933 no. 1): born 12 Jan 1932 in Egernsund, baptised at home 1 Jan 1933; "
            "parents labourer Peter Frederiksen and wife Else Gedde Jensen, Egernsund (per letter from the civil registrar "
            "11/7 1932). Godparents: the father; labourer Lorenz Frederiksen and wife Catharina, Egernsund (his grandparents); "
            "farmer Jens Jensen's wife, Dalsgaard. Family information says Peter Frederiksen was not his biological father. "
            "Buried with his wife Gerda at Sankt Jørgens Kirkegård, Svendborg.",
       src=["AO:Broager Vestre distrikt kontraministerialbog 1906–48, Fødte 1933 no. 1 (bsid 201141, image 112)",
            "BillionGraves via MyHeritage (collection 10147): Lorenz H. [Lorenz Heinrich] Frederiksen, Sankt Jørgens Kirkegård, Svendborg",
            "MyHeritage: 1940 Denmark Census, 'Lorens Henrick Frederiksen'"])
person("p12", "Peter Frederiksen", "M", ahnen=12, line="frederiksen", born="1902-02-15", bplace="Broager",
       father="p24", mother="p25", occ=["Farm servant, Broager (1921)", "Labourer (arbejder), Egernsund (1932)"],
       note="Lorenz's father in law (named in the baptism entry). Family information says he was not Lorenz's biological father.",
       src=["LL:12-15018348", "LL:14-2208771", "LL:25-5954688", "AO:Broager Vestre 1933 no. 1"])
person("p13", "Else Gedde Jensen", "F", ahnen=13, line="maternal", conf="record",
       note="Lorenz's mother, named in his baptism entry. 'Gedde' is part of her name, and is where your mother's surname Gedde comes from. "
            "Not in the Southern Jutland indexes, so probably born elsewhere in Denmark. Godmother 'farmer Jens Jensen's wife, "
            "Dalsgaard' may be her mother (unconfirmed).",
       src=["AO:Broager Vestre 1933 no. 1"])
person("p24", "Lorenz Heinrich Frederiksen", "M", ahnen=24, line="frederiksen", born="1870-01-23", bplace="Broager",
       died="1957-01-04", dplace="Egernsund", father="p48", mother="p49", occ=["Labourer (arbejder), Egernsund (1932)"],
       note="Married Cathrina Maria Magdalena Hansen 8 Oct 1895 in Broager. Godfather to his grandson and namesake in 1933. "
            "Member of the Danish association DSK in 1942 (membership card in Broagerlands Lokalarkiv).",
       res=[(1870, "Broager", "born"), (1921, "Broager", "census"), (1932, "Egernsund", "")],
       src=["LL:12-14989547", "LL:12-14313283", "LL:13-1051959", "LL:25-5953605", "ARK:1158725", "AO:Broager Vestre 1933 no. 1"])
person("p25", "Cathrina Maria Magdalena Hansen", "F", ahnen=25, line="frederiksen", born="1872-12-28", bplace="Broager",
       father="p50", mother="p51", src=["LL:12-14990795", "LL:13-1051962", "LL:25-5953606"])
person("p48", "Peter Christian Frederiksen", "M", ahnen=48, line="frederiksen", born="1839-05-04", bplace="Broager",
       father="p96", mother="p97", note="Married Anna Kirstine Marie Paulsen 9 Dec 1860 in Broager.", src=["LL:13-4957004", "LL:12-14989548"])
person("p49", "Anna Kirstine Marie Paulsen", "F", ahnen=49, line="frederiksen", born="1834-11-11", bplace="Broager",
       died="1893-05-22", dplace="Broager", father="p98", mother="p99", src=["LL:13-4957007", "LL:11-7302858"])
person("p50", "Carl Peter Hansen", "M", ahnen=50, line="frederiksen", bplace="Broager", src=["LL:12-14990796", "LL:13-1051963"])
person("p51", "Eline Maria Magdalena Hansen", "F", ahnen=51, line="frederiksen", src=["LL:12-14990797", "LL:13-1051964"])
person("p96", "Frederik Frederiksen", "M", ahnen=96, line="frederiksen", src=["LL:13-4957005"])
person("p97", "Anne Kirstine Peters", "F", ahnen=97, line="frederiksen", src=["LL:13-4957006"])
person("p98", "Jens Paulsen", "M", ahnen=98, line="frederiksen", src=["LL:13-4957008", "LL:11-7302859"])
person("p99", "Kathrine Marie Lorensen", "F", ahnen=99, line="frederiksen", src=["LL:13-4957009", "LL:11-7302860"])
sibs_later = True
person("p7", "Gerda Frederiksen", "F", ahnen=7, line="maternal", conf="record",
       born="1935-08-17", died="2019-07-18", dplace="Svendborg",
       note="Buried at Sankt Jørgens Kirkegård, Svendborg, with her husband Lorenz. Maiden name not yet known.",
       src=["BillionGraves via MyHeritage (collection 10147): Gerda Frederiksen, Sankt Jørgens Kirkegård, Svendborg"])

# ---------------- Generation 4 ----------------
person("p8", "Aage Evald Oskar Jørgensen", "M", ahnen=8, line="jorgensen", born="1890-10-17", bplace="Slagelse",
       father="p16", mother="p17",
       occ=["Night watchman, Copenhagen (1918)", "Farm manager (gårdbestyrer), Kolind (1921–22)", "Poorhouse manager, Gjellerup (1925)"],
       res=[(1890, "Slagelse", "born"), (1918, "Copenhagen", "night watchman"), (1921, "Kolind", "in the Gaardsted household"),
            (1925, "Gjellerup / Hammerum", "manager of Gjellerup fattiggård"), (1932, "Hadsten", "moved with family")],
       note="Married Jensine Gaardsted in Kolind Church on 29 Oct 1921.",
       src=["LL:12-16940206", "LL:9-1795573", "LL:17-1153878", "LL:25-1032486", "AO:27841253", "DFS:18978910"])
person("p9", "Jensine Mariane Magdalene Gaardsted", "F", ahnen=9, line="gaardsted", born="1894-06-06", bplace="Kolind",
       father="p18", mother="p19", occ=["Housemaid, Copenhagen (1915)"],
       res=[(1894, "Kolind", "born"), (1915, "Copenhagen", "housemaid"), (1925, "Gjellerup / Hammerum", "manager's wife"), (1932, "Hadsten", "")],
       src=["LL:9-1332311", "LL:14-3965870", "LL:17-936099", "AO:27841253", "DFS:18978911"])
person("s_ester", "Ester Kristine Jørgensen", "F", rel="Evald's sister", line="jorgensen", born="1924", father="p8", mother="p9",
       src=["DFS:18978913"])

# ---------------- Generation 5 ----------------
person("p16", "Jørgen Anton Jørgensen", "M", ahnen=16, line="jorgensen", born="1857-10-06", bplace="Copenhagen",
       died="1914-08-04", dplace="Slagelse", father="p32", mother="p33",
       occ=["Typographer, Copenhagen", "Typographer, Sorø Amts Bogtrykkeri, Slagelse"],
       res=[(1857, "Copenhagen", "born, Vor Frue parish"), (1886, "Copenhagen", "married"), (1889, "Slagelse", "moved"), (1914, "Slagelse", "died")],
       note="Married Lovisa Larsson 31 Jan 1886, Sankt Johannes, Copenhagen.",
       src=["LL:12-13117126", "LL:14-7547225", "LL:7-586580", "LL:13-4147709", "LL:9-1795568", "LL:11-230038"])
person("p17", "Lovisa (Louise) Larsson", "F", ahnen=17, line="jorgensen", born="1862-06-28", bplace="Malmö",
       died="1910-10-12", dplace="Slagelse", father="p34", occ=["Housemaid, Copenhagen (1885)"],
       res=[(1862, "Malmö", "born"), (1885, "Copenhagen", "housemaid"), (1901, "Slagelse", "")],
       src=["LL:8-200847", "LL:9-1795569", "LL:11-231267"])
person("p18", "Hans Peter Gaardsted", "M", ahnen=18, line="gaardsted", born="1852-05-03", bplace="Tirstrup",
       died="1913-03-26", dplace="Kolind", father="p36", mother="p37",
       occ=["Farmhand, Ebeltoft (1880)", "Smallholder / house-owning farmer, Kolind"],
       res=[(1852, "Tirstrup", "born"), (1880, "Ebeltoft", "farmhand"), (1883, "Kolind", "smallholding 'Petersminde', Højsletvej")],
       src=["LL:12-3665481", "LL:7-1041647", "LL:9-1332308", "LL:11-3881351"])
person("p19", "Rasmine Christine Andersen", "F", ahnen=19, line="rousing", born="1855-09-16", bplace="Fuglslev",
       died="after 1922", father="p38", mother="p39",
       res=[(1855, "Fuglslev", "born"), (1880, "Ebeltoft", ""), (1890, "Kolind", ""), (1922, "Kolind", "widow, godmother to Evald")],
       src=["LL:12-9158976", "LL:6-849934", "LL:25-1032484", "AO:27841253"])

# ---------------- Generation 6 ----------------
person("p32", "Niels Jørgensen", "M", ahnen=32, line="jorgensen", born="c.1826",
       bplace=None, died="1885–1892", dplace="Copenhagen",
       occ=["Grocer (høker), Copenhagen (1860)", "Labourer (arbejdsmand), Copenhagen (1880–85)"],
       res=[(1860, "Copenhagen", "grocer"), (1885, "Copenhagen", "labourer")],
       note="Birthplace written 'Hove/Høje sogn, Svendborg amt' — parish not identified.",
       src=["LL:6-420495", "LL:7-586576", "LL:8-31142"])
person("p33", "Johanne Sophie Hansen", "F", ahnen=33, line="jorgensen", born="c.1825", bplace="Viby (Roskilde amt)",
       died="c.1910", dplace="Copenhagen", occ=["Widow on old-age support (1901)"],
       src=["LL:6-420496", "LL:9-407995", "LL:17-1567270"])
person("p34", "Niels Larsen", "M", ahnen=34, line="jorgensen", bplace="Malmö", note="Swedish; named in daughter's death record.",
       src=["LL:11-231268"])
person("p36", "Jochum (Joachim) Gaardsted", "M", ahnen=36, line="gaardsted", born="1792-09-23", bplace="Vosnæsgaard, Skødstrup",
       died="1865-06-18", dplace="Tirstrup", father="p72", mother="p73",
       occ=["Farmer and parish bailiff (gårdmand og sognefoged), Tirstrup"],
       res=[(1792, "Vosnæsgaard, Skødstrup", "born on the manor his father leased"), (1801, "Bogensholm, Vistoft (Mols)", "child on his father's estate"),
            (1833, "Rosmus", "2nd marriage"), (1834, "Tirstrup", "farmer & sognefoged until death")],
       note="Baptism confirmed 2 Oct 1792 in Skødstrup Church; godparents included the Majorinde Weinegel, Generalinde Trampe, "
            "Major Folsch of Aarhus and Sehested of Fredericia. 1st wife Marie Kjerstine Christensdatter; "
            "2nd marriage 19 Oct 1833 in Rosmus to Ane Sophie Jensdatter.",
       src=["AO:Skødstrup FKVD 1780–1809, p.75 (bsid 736476, image 43)", "LL:1-475273", "LL:2-530881", "LL:5-717919", "LL:13-1706737", "LL:11-1962320"])
person("p37", "Ane Sophie Jensdatter", "F", ahnen=37, line="gaardsted", born="c.1812", bplace="Rosmus",
       died="1886-02-27", dplace="Tirstrup", src=["LL:2-530882", "LL:13-1706738", "LL:11-1962058"])
person("p38", "Anders Rasmussen Rousing", "M", ahnen=38, line="rousing", born="1818-03-12", bplace="Fuglslev",
       died="1886-12-20", dplace="Fuglslev", father="p76", mother="p77",
       occ=["Cottager (boelsmand), Fuglslev (1845)", "Farmer (gårdmand), Fuglslev (1850–60)", "Retired farmer (1880)"],
       note="Married Mariane Hansdatter 3 Sep 1841 in Fuglslev.",
       src=["LL:12-3667395", "LL:13-3522464", "LL:6-849928", "LL:11-4601883"])
person("p39", "Mariane Hansdatter", "F", ahnen=39, line="rousing", born="1817-04-11", bplace="Fuglslev",
       died="1885-07-26", dplace="Fuglslev", father="p78", mother="p79", occ=["Servant at Fuglslev mill (1834–40)"],
       src=["LL:12-3667695", "LL:2-515660", "LL:11-4602105"])

# ---------------- Generation 7 ----------------
person("p72", "Claus Gaardsted", "M", ahnen=72, line="gaardsted", born="c.1750", died="1811",
       dplace="Bogensholm, Vistoft (Mols)",
       occ=["Tenant of the manor (forpagter), Vosnæsgaard (1787–c.1796)", "Owner of Bogensholm estate (1796/97–1811)"],
       res=[(1787, "Vosnæsgaard, Skødstrup", "forpagter"), (1797, "Bogensholm, Vistoft (Mols)", "bought the estate for 10,000 rdl")],
       note="Married twice; Kirsten Marie Jørgensdatter was his 2nd wife. His widow sold Bogensholm at auction in 1811 for 31,000 rdl. "
            "Arrived at Vosnæsgaard after 1784; his own birthplace and parents are unknown.",
       src=["LL:0-414804", "LL:1-475533", "AO:Skødstrup FKVD 1780–1809, p.75", "Trap Danmark / danskeherregaarde.dk (Bogensholm)"])
person("p73", "Kirsten Marie Jørgensdatter", "F", ahnen=73, line="gaardsted", born="c.1752", died="after 1811",
       src=["LL:0-414805", "LL:1-475272"])
person("p76", "Rasmus Jensen Rousing", "M", ahnen=76, line="rousing", born="c.1780", bplace="Fuglslev",
       died="1858-05-25", dplace="Fuglslev", father="p152", mother="p153",
       occ=["Freeholder farmer and parish bailiff (selvejer gårdmand og sognefoged), Fuglslev"], conf="record",
       src=["LL:2-515582", "LL:11-4601884", "LL:11-4601476"])
person("p77", "Karen Christensdatter", "F", ahnen=77, line="rousing", born="c.1780", died="1855-04-25", dplace="Fuglslev",
       src=["LL:2-515583", "LL:11-4601630"])
person("p78", "Hans Jacobsen", "M", ahnen=78, line="rousing", born="c.1794",
       note="Married Maren Rasmusdatter 6 Jul 1817 in Fuglslev.", src=["LL:13-1705838", "LL:12-3667696"])
person("p79", "Maren Rasmusdatter", "F", ahnen=79, line="rousing", born="c.1798", src=["LL:13-1705839"])

# ---------------- Generation 8-9 (probable) ----------------
person("p152", "Jens Rasmussen", "M", ahnen=152, line="rousing", born="c.1755", bplace="Fuglslev", conf="probable",
       father="p304", occ=["Farmer (bonde og gårdbeboer), Fuglslev"],
       note="Rasmus Jensen, aged 20, lives in his household in 1801.", src=["LL:1-473834", "LL:0-415717"])
person("p153", "Margrethe Christensdatter", "F", ahnen=153, line="rousing", born="c.1758", conf="probable", src=["LL:1-473835"])
person("p304", "Rasmus Jensen", "M", ahnen=304, line="rousing", born="c.1718", bplace="Fuglslev", conf="possible",
       occ=["Farmer (bonde og gårdmand), Fuglslev (1787)"], note="Possible father of Jens Rasmussen (naming pattern only).",
       src=["LL:0-415357"])

# ---------------- Siblings and other relatives (width) ----------------
def sibs(parents, line, rel, rows):
    f, m = parents
    for i, (name, sex, born, extra) in enumerate(rows):
        person(f"s_{f}_{i}", name, sex, rel=rel, line=line, born=born, father=f, mother=m,
               occ=extra.get("occ", []), died=extra.get("died"), note=extra.get("note"))

sibs(("p16", "p17"), "jorgensen", "Aage's sibling", [
    ("Johanne Marie Margrethe Jørgensen", "F", "1886-10-21", {"note": "twin"}),
    ("Niels Sophus Holger Jørgensen", "M", "1886-10-21", {"note": "twin"}),
    ("Agnes Ingeborg Jørgensen", "F", "1888-07-30", {}),
    ("Karl Alfred Peter Jørgensen", "M", "1892-10-24", {}),
    ("Ellen Sophie Elisabeth Jørgensen", "F", "1895-01-07", {}),
    ("Anna Louise Mathilde Jørgensen", "F", "1899-12-26", {}),
])
sibs(("p32", "p33"), "jorgensen", "Jørgen Anton's sibling", [
    ("Hans Sophus Frederik Jørgensen", "M", "1855", {"occ": ["Passementmaker"]}),
    ("Anna Margrethe Jørgensen", "F", "1855-11-18", {"occ": ["Dressmaker"]}),
    ("Peter Jørgensen", "M", "1862-04-05", {"occ": ["Shoemaker"]}),
    ("Agnes Mathilde Jørgensen", "F", "1871-08-03", {"occ": ["Dressmaker"]}),
])
sibs(("p18", "p19"), "gaardsted", "Jensine's sibling", [
    ("Johanne Marie Gaardsted", "F", "1879-01-29", {"occ": ["Servant"], "note": "Lived with her widowed mother in Kolind 1921; with sister Sofie left memoirs of Petersminde (Midtdjurs Lokalhistoriske Arkiv A847)."}),
    ("Sofie Gaardsted", "F", "1881", {"occ": ["Servant"]}),
    ("Agnes Kristiane Gaardsted", "F", "1883", {"occ": ["Servant"]}),
    ("Jokum Gaardsted", "M", "1886", {}),
    ("Martin Marinus Gaardsted", "M", "1888-11-10", {"occ": ["Poorhouse manager, Bregnet (1922)"]}),
    ("Axel Villiam Gaardsted", "M", "1891-08-20", {"died": "1894-03-07"}),
    ("Petra Ottine Gaardsted", "F", "1897-02-25", {}),
    ("Axel Vilhelm Alfred Gaardsted", "M", "1900-12-05", {}),
])
sibs(("p36", "p37"), "gaardsted", "Hans Peter's sibling", [
    ("Marie Kirstine Gaardsted", "F", "1839", {}),
    ("Jens Gaardsted", "M", "1841", {"died": "1914", "occ": ["Farm owner, Tirstrup"]}),
    ("Mette Marie Gaardsted", "F", "1844", {"died": "1847"}),
    ("Johanne Gaardsted", "F", "1847", {}),
    ("Ernst Adolph Gaardsted", "M", "1849", {}),
])
person("s_claus_ch", "Claus Christian Gaardsted", "M", rel="Hans Peter's half-brother", line="gaardsted",
       born="1832-07-28", died="1863", father="p36", note="Mother: Marie Kjerstine Christensdatter (Jochum's 1st wife).")
sibs(("p72", "p73"), "gaardsted", "Jochum's sibling", [
    ("Ernst Adolph Gaardsted", "M", "1784", {"died": "1832-06-13", "occ": ["Farmer, Hoed"], "note": "Married Anne Andersdatter Kræmer; 5+ children in Hoed."}),
    ("Poul Christian Gaardsted", "M", "1790", {}),
])
sibs(("p38", "p39"), "rousing", "Rasmine's sibling", [
    ("Rasmus Andersen", "M", "1845", {}), ("Hans Andersen", "M", "1847", {}),
    ("Søren Andersen", "M", "1850", {}), ("Jensine Caroline Andersen", "F", "1852", {}),
])
sibs(("p76", "p77"), "rousing", "Anders's sibling", [
    ("Christen Rasmussen", "M", "1812", {}), ("Jens Christian Rasmussen", "M", "1816", {}),
])

person("s_liss_1", "Karen Margrethe Enevoldsen (née Pedersen)", "F", rel="Liss's sister", line="jorgensen", sibof="p5",
       src=["FamilySearch Family Tree"])
person("s_liss_2", "Ane Elvira Pedersen", "F", rel="Liss's sister", line="jorgensen", sibof="p5", src=["FamilySearch Family Tree"])

sibs(("p24", "p25"), "frederiksen", "Peter's sibling", [
    ("Son (unnamed)", "M", "1896", {"died": "1896-05-19"}),
    ("Eline Christine Frederiksen", "F", "1897-04-28", {}),
    ("Child of Lorenz & Cathrina", "M", "1905-07-15", {}),
])
sibs(("p48", "p49"), "frederiksen", "Lorenz Heinrich's sibling", [
    ("Hans Frederik Frederiksen", "M", "1862-10-28", {}),
    ("Jens Frederiksen", "M", "1865-07-04", {}),
    ("Catharina Maria Frederiksen", "F", "1867-04-24", {"note": "Married Hans Hendrik Ohlsen 17 Jun 1888 in Broager."}),
    ("Anna Christine Maria Frederiksen", "F", "1874-02-10", {}),
])

# Occupation categories for statistics
CATS = [("Clergy & church", ["priest", "clerk", "kordegn"]), ("Teaching & writing", ["teacher", "author"]),
        ("Farming & estates", ["farm", "cottager", "smallholder", "estate", "forpagter", "bonde"]),
        ("Parish office", ["bailiff", "sognefoged"]), ("Crafts & print", ["typographer", "passement", "shoemaker", "dressmaker"]),
        ("Service & labour", ["servant", "housemaid", "farmhand", "labourer", "watchman"]),
        ("Trade", ["grocer"]), ("Poor relief", ["poorhouse"])]

PHOTOS = [
    dict(file="images/lorenz-baptism-broager-1933.jpg", title="Lorenz's baptism, Broager 1933",
         caption="Broager Vestre district church book, 1933 no. 1: Lorenz Heinrich, born 12 Jan 1932 in Egernsund. Parents Peter Frederiksen and Else Gedde Jensen.",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17216172"),
    dict(file="images/evald-baptism-kolind-1922.jpg", title="Evald's birth entry, Kolind 1922",
         caption="Kolind church book, boys born 1922, no. 6. Parents Aage Evald Oskar Jørgensen and Jensine Mariane Magdalene Gaardsted; margin note on the 1985 name change.",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=17124596"),
    dict(file="images/jochum-baptism-skodstrup-1792.jpg", title="Jochum's baptism, Skødstrup 1792",
         caption="'Hr. Forpagter Gaardsted paa Vosnæsgaard og hans Kone Kirstine Marie Jørgensdatter … Barnet var fød d. 23de Sept. … kaldet Jochum.'",
         credit="Rigsarkivet, Arkivalieronline", link="https://arkivalieronline.rigsarkivet.dk/da/billedviser?epid=24257049"),
    dict(file="images/vosnaesgaard-1839-rawert.jpg", title="Vosnæsgaard, 1839",
         caption="Drawing by O.J. Rawert, 1839. Claus Gaardsted leased this manor in the 1780s–90s; Jochum was born here.",
         credit="Rawert / Det Kgl. Bibliotek via Skødstrup Sogns Egnsarkiv", link="https://arkiv.dk/vis/2780543"),
]
LINKS = [
    ("Gjellerup poorhouse, 1914 (where Aage was manager in 1925)", "https://arkiv.dk/vis/2636314"),
    ("Group photo, Gjellerup poorhouse, 1914", "https://arkiv.dk/vis/2636339"),
    ("Bogensholm manor (Claus Gaardsted's estate 1797–1811)", "https://arkiv.dk/vis/4033299"),
    ("Confirmands at Rødhus Church 1988, with pastor Evald Gaardsted Jørgensen", "https://arkiv.dk/vis/5695529"),
    ("Hune Church", "https://arkiv.dk/vis/4306061"),
    ("Kolind station c.1920", "https://arkiv.dk/vis/4212435"),
    ("Tirstrup Church, 1920", "https://arkiv.dk/vis/2623461"),
    ("Fuglslev Church", "https://arkiv.dk/vis/6189757"),
    ("Grave of Lorenz H. Frederiksen and Gerda Frederiksen, Sankt Jørgens Kirkegård, Svendborg (BillionGraves record on MyHeritage)",
     "https://www.myheritage.dk/research/collection-10147/billiongraves?itemId=1483464614&action=showRecord"),
    ("Petersminde memoirs of Johanne & Sofie Gaardsted (archive)", "https://arkiv.dk/vis/4407757"),
    ("Evald Gaardsted-Jørgensen's personal archive, incl. his own family tree (Hadsten)", "https://arkiv.dk/vis/2162357"),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(dict(people=P, places=PLACES, cats=CATS, photos=PHOTOS, links=LINKS),
              open(os.path.join(here, "family.json"), "w"), ensure_ascii=False, indent=1)
    print(len(P), "people")
