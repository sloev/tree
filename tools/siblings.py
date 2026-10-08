"""Finder søskende til alle aner i Link Lives og skriver dem til data/auto_siblings.json.

For hver ane med en indekseret dåb: søg alle dåb i samme sogn ±25 år, hvor faren har samme navn og moren samme
fornavn. Fanges også i nabosogne i samme amt, hvis begge forældres fulde navne passer. Spædbørnsdødsfald slås op
i begravelserne. Nulevende og personer født inden for 100 år uden dødsdato springes over (de hører til i den
krypterede fil). Kør: python3 tools/siblings.py
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from climb import q, record, role, ov, toks

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "auto_siblings.json")
THIS_YEAR = 2026

def gen(n): return n + ("'" if n[-1:].lower() in "sxz" else "s")
def first(n): return (re.split(r"[\s(]+", (n or "").strip().lower()) or [""])[0]
def norm1(n): return first(n).replace("ch", "k").replace("c", "k").replace("th", "t").replace("ph", "f").rstrip("e")
def yr(s):
    m = re.search(r"\d{4}", str(s or "")); return int(m.group()) if m else None
def std(r): return r.get("standard") or {}

def birth_group(p):
    for s in p.get("src", []):
        m = re.match(r"LL:(12-\d+)", s)
        if not m: continue
        g = record(m.group(1)); c = role(g, "Barn")
        if c and norm1(c.get("name_display")) == norm1(p["name"]) and role(g, "Far") and role(g, "Mor"): return g
    return None

def same_parents(g, F, M, strict):
    f, m = role(g, "Far"), role(g, "Mor")
    if not (f and m): return False
    fo = ov(f.get("name_display"), F) >= min(2, len(toks(F)))
    mo = norm1(m.get("name_display")) == norm1(M) and (not strict or ov(m.get("name_display"), M) >= min(2, len(toks(M))))
    return fo and mo

def died_young(name, by, parish):
    if not by: return None
    hs = q({"bool": {"must": [{"term": {"source_id": 11}}, {"match": {"name_searchable_fz": name}},
                              {"range": {"event_year_sortable": {"gte": by, "lte": by + 12}}},
                              {"match": {"sourceplace_searchable": parish}}]}}, 10)
    for h in hs:
        if h.get("role_display") == "Afdøde" and ov(h.get("name_display"), name) >= min(2, len(toks(name))) and abs((yr(h.get("birthyear_display")) or by) - by) <= 1:
            return h
    return None

def main():
    fam = json.load(open(os.path.join(ROOT, "data", "family.json"), encoding="utf-8"))
    P = fam["people"]
    out = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else []
    done = {o["_for"] for o in out}
    for p in sorted([p for p in P if p.get("ahnen") and p["ahnen"] >= 4 and not p.get("private") and p.get("father") and p.get("mother")], key=lambda p: p["ahnen"]):
        if p["id"] in done: continue
        g = birth_group(p)
        if not g: continue
        c, F, M = role(g, "Barn"), role(g, "Far")["name_display"], role(g, "Mor")["name_display"]
        parish = std(c).get("event_parish") or (c.get("sourceplace_display") or "").split(" sogn")[0]
        county = std(c).get("event_county") or ""
        y = yr(c.get("event_year_sortable")) or yr(p.get("born")) or 1850
        known = [x for x in P if x.get("father") == p["father"] and x.get("mother") == p["mother"]]
        seen_keys = {c["key"]}; found = []
        for scope, strict in ((parish, False),):  # amtsbred søgning gav for mange navnefæller
            if not scope: continue
            hits = q({"bool": {"must": [{"term": {"source_id": 12}}, {"match": {"name_searchable_fz": F}},
                                        {"range": {"event_year_sortable": {"gte": y - 25, "lte": y + 25}}},
                                        {"match": {"sourceplace_searchable": scope}}]}}, 100)
            fh = [h for h in hits if h.get("role_display") == "Far" and ov(h.get("name_display"), F) >= min(2, len(toks(F)))
                  and h["pa_grouping_id_wp4"] not in {x.get("_grp") for x in found}]
            grps = {}
            ids = [h["pa_grouping_id_wp4"] for h in fh]
            for i in range(0, len(ids), 60):
                for m in q({"bool": {"must": [{"term": {"source_id": 12}}, {"terms": {"pa_grouping_id_wp4": ids[i:i + 60]}}]}}, 300):
                    grps.setdefault(m["pa_grouping_id_wp4"], []).append(m)
            for h in fh:
                gg = grps.get(h["pa_grouping_id_wp4"], []); cc = role(gg, "Barn")
                if not cc or cc["key"] in seen_keys or not same_parents(gg, F, M, strict): continue
                seen_keys.add(cc["key"])
                bd = std(cc).get("birth_date") or std(cc).get("event_date") or cc.get("event_year_display")
                found.append({"_grp": h["pa_grouping_id_wp4"], "name": (cc.get("name_display") or "").strip(), "sex": "F" if std(cc).get("sex") == "f" else "M",
                              "born": bd, "bplace_text": (cc.get("sourceplace_display") or "").split(" sogn")[0].title(), "key": cc["key"],
                              "parish": std(cc).get("event_parish") or parish})
        n = 0
        for s in sorted(found, key=lambda s: str(s["born"])):
            by = yr(s["born"])
            dup = any((norm1(k["name"]) == norm1(s["name"]) and yr(k.get("born")) == by) or (k.get("born") and k["born"] == s["born"] and norm1(k["name"]) == norm1(s["name"])) for k in known)
            if dup or not s["name"] or len(s["name"]) < 2: continue
            if not by or by >= THIS_YEAR - 100: continue
            d = died_young(s["name"], by, s["parish"])
            e = {"_for": p["id"], "id": f"as_{p['id']}_{n}", "name": s["name"], "sex": s["sex"], "born": s["born"], "bplace_text": s["bplace_text"],
                 "father": p["father"], "mother": p["mother"], "line": p.get("line"), "rel": gen(p['name'].split(' (')[0].split()[0]) + " søskende",
                 "src": [f"LL:{s['key']} (dåb {s['bplace_text']} {by})"]}
            if d:
                e["died"] = d.get("event_year_display"); e["src"].append(f"LL:{d['key']} (begravet {e['died']})"); e["note"] = "Død som barn."
            out.append(e); n += 1
        if not n: out.append({"_for": p["id"], "none": True})
        print(f"{p['ahnen']:>5} {p['name'][:40]:40} {parish}: {n} nye søskende", flush=True)
        json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

JUNK = re.compile(r"d[øo]df[øo]dt|udøbt|uægte|twilling|tvilling|tidlig|drengebarn|pigebarn|^n\.?n\.?$", re.I)

def _date(b):
    from datetime import date
    m = re.match(r"(\d{4})-(\d\d)-(\d\d)", str(b or ""))
    return date(*map(int, m.groups())) if m else None

def clean(L, people):
    """Fjerner dubletter (Sønderjyllands dobbelte kirkebøger), dødfødte uden navn, børn hvis patronymikon ikke passer til faren,
    og hele søskendeflokke, hvor to fødsler ligger under 9 måneder fra hinanden (= to familier med samme navne)."""
    byid = {p["id"]: p for p in people}
    out, groups = [], {}
    for x in L:
        if x.get("none") or x.get("reject"): out.append(x); continue
        groups.setdefault(x["_for"], []).append(x)
    for anc, xs in groups.items():
        a = byid.get(anc); ay = yr(a.get("born")) if a else None
        fa = byid.get(xs[0]["father"], {}).get("name", "")
        keep, seen = [], set()
        for x in sorted(xs, key=lambda x: str(x["born"])):
            if JUNK.search(x["name"]): continue
            k = (norm1(x["name"]), str(x["born"])[:10])
            if k in seen: continue
            last = x["name"].split()[-1].lower() if len(x["name"].split()) > 1 else ""
            ftok = {t.lower() for t in fa.replace("(", " ").replace(")", " ").split()}
            if (last.endswith("sen") or last.endswith("datter")) and last not in ftok and not any(last.startswith(t[:4]) for t in ftok if len(t) > 3):
                continue
            if ay and yr(x["born"]) and abs(yr(x["born"]) - ay) > 22: continue
            seen.add(k); keep.append(x)
        dates = sorted(d for d in [_date(a.get("born")) if a else None] + [_date(x["born"]) for x in keep] if d)
        clash = any(0 < (d2 - d1).days < 270 for d1, d2 in zip(dates, dates[1:]))
        if clash:
            out.append({"_for": anc, "reject": True, "why": "to familier med samme navne i sognet", "n": len(keep)}); continue
        out.extend(keep)
    return out

if __name__ == "__main__":
    if "--clean" in sys.argv:
        fam = json.load(open(os.path.join(ROOT, "data", "family.json"), encoding="utf-8"))
        L = clean(json.load(open(OUT, encoding="utf-8")), fam["people"])
        json.dump(L, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(sum(1 for x in L if not x.get("none") and not x.get("reject")), "søskende;", sum(1 for x in L if x.get("reject")), "afviste flokke")
    else:
        main()
