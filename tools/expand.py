"""Udvider anetavlen automatisk ud fra Link Lives (Rigsarkivet) og skriver resultatet til data/auto_ancestors.json.

For hver ane uden kendte forældre:
  1. fødselsposten (fra anens LL:12-kilde eller søgt på navn + dato + sogn) giver forældrenes navne,
  2. forældrenes vielse giver fødselsår/-sted og deres forældres navne,
  3. forældrenes egne fødselsposter giver præcise datoer og næste generation.
Hver ny person får de præcise Link Lives-nøgler som kilder. Kør: python3 tools/expand.py [runder]
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from climb import q, record, role, ov, toks, bdate, find_marriage, find_birth
from ll import get

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "auto_ancestors.json")
STOP = {"vester", "øster", "nørre", "sønder", "store", "lille", "kirke", "sankt", "vor", "frue", "sogn", "amt", "by", "mark", "langeland", "danmark", "herred", "købstad", "i", "ved", "pr", "og", "s", "a"}

def parish_tokens(*strs):
    out = []
    for s in strs:
        for t in re.split(r"[^a-zæøåäöü]+", (s or "").lower()):
            if len(t) > 2 and t not in STOP and t not in out: out.append(t)
    return out

def yr(s):
    m = re.search(r"\d{4}", str(s or "")); return int(m.group()) if m else None

def birth_group_from_src(p):
    for s in p.get("src", []):
        m = re.match(r"LL:(12-\d+)", s)
        if not m: continue
        g = record(m.group(1)); c = role(g, "Barn")
        if c and first(c.get("name_display")) == first(p["name"]) and ov(c.get("name_display"), p["name"]) >= min(2, len(toks(p["name"])), len(toks(c.get("name_display")))) and role(g, "Far"): return g
    return None

def first(n):
    return (re.split(r"[\s(]+", (n or "").strip().lower()) or [""])[0]

def place_of(rec):
    return (rec.get("sourceplace_display") or "").split(",")[0].replace(" sogn", "").strip()

def main(rounds=3):
    fam = json.load(open(os.path.join(ROOT, "data", "family.json"), encoding="utf-8"))
    auto = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else []
    people = [p for p in fam["people"] if p.get("ahnen") and not p.get("private")]
    known = {p["ahnen"]: p for p in people}
    for a in auto: known.setdefault(a["ahnen"], a)
    tried = set()
    # Aner kendt kun ved navn (fra barnets dåb): find forældrenes vielse og tilføj alder, fødested og kilde som "patch".
    for n, p in sorted(known.items()):
        if n < 4 or n % 2 or p.get("born") or (n + 1) not in known or p.get("_auto"): continue
        if any(a.get("patch") and a["ahnen"] == n for a in auto): continue
        mo = known[n + 1]; child = known.get(n // 2)
        if not child or mo.get("born"): continue
        g = birth_group_from_src(child)
        if not g and yr(child.get("born")):
            cb = str(child.get("born")); cb = cb if re.match(r"\d{4}", cb) else str(yr(cb))
            for pl in parish_tokens(child.get("bplace"), child.get("bplace_text"), child.get("_parish")):
                try: g = find_birth(re.sub(r"\(.*?\)", "", child["name"]).strip(), cb, pl)
                except Exception: g = None
                if g and role(g, "Far") and ov(role(g, "Far").get("name_display"), p["name"]) >= min(2, len(toks(p["name"]))): break
                g = None
        if not g: continue
        F, M = role(g, "Far"), role(g, "Mor")
        if not (F and M): continue
        cy = yr(bdate(role(g, "Barn"))) or yr(child.get("born")) or 1850
        try: mar = find_marriage(F["name_display"], M["name_display"], cy, place_of(role(g, "Barn")))
        except Exception as e: print("  !", e); mar = None
        if not mar: continue
        for who, r in ((p, "Brudgom"), (mo, "Brud")):
            sp = role(mar, r)
            if not sp: continue
            pt = {"ahnen": who["ahnen"], "id": who["id"], "patch": True, "born": bdate(sp),
                  "bplace_text": (sp.get("birthplace_display") or "").split(",")[0].replace(" sogn", "").strip().title() or None,
                  "src": ["LL:" + sp["key"] + f" (vielse {place_of(mar[0]).title()} {mar[0].get('event_year_display') or ''})"],
                  "note": f"Gift {mar[0].get('event_year_display') or ''} i {place_of(mar[0]).title()}.", "_parish": place_of(mar[0])}
            pf = role(mar, r + ("mens far" if r == "Brudgom" else "ens far")); pm = role(mar, r + ("mens mor" if r == "Brudgom" else "ens mor"))
            pt["_parents"] = [(x.get("name_display"), x["key"]) for x in (pf, pm) if x]
            auto[:] = [a for a in auto if not (a.get("patch") and a["ahnen"] == pt["ahnen"])] + [pt]
            who.update(born=pt["born"], bplace=None, _parish=pt["_parish"], bplace_text=pt["bplace_text"])
            print(f"  ~ {who['ahnen']}: {who['name']} f. {pt['born']} {pt['bplace_text'] or ''} (vielse)", flush=True)
        json.dump(auto, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for rnd in range(rounds):
        frontier = [p for n, p in sorted(known.items()) if n > 1 and (2*n not in known or 2*n+1 not in known) and n not in tried]
        print(f"runde {rnd+1}: {len(frontier)} aner uden forældre", flush=True)
        added = 0
        for p in frontier:
            n = p["ahnen"]; tried.add(n)
            g = birth_group_from_src(p)
            pb = str(p.get("born") or "")
            pb = pb if re.match(r"\d{4}", pb) else (str(yr(pb)) if yr(pb) else "")
            if not g and pb:
                for pl in parish_tokens(p.get("bplace"), p.get("bplace_text"), p.get("_parish")):
                    try: g = find_birth(p["name"], pb, pl)
                    except Exception as e: print("  !", p["name"], e, flush=True); g = None
                    if g: break
            if not g: continue
            child, F, M = role(g, "Barn"), role(g, "Far"), role(g, "Mor")
            cy = yr(bdate(child)) or yr(p.get("born")) or 1800
            cpar = place_of(child)
            # opdater anen selv med fødselskilden
            if not (p in auto or p.get("_auto")) and not any(s.startswith("LL:" + child["key"]) for s in p.get("src", [])):
                pt = next((a for a in auto if a.get("patch") and a["ahnen"] == n), None)
                if not pt: pt = {"ahnen": n, "id": p["id"], "patch": True, "src": [], "note": ""}; auto.append(pt)
                pt["src"].insert(0, "LL:" + child["key"] + f" (fødsel {cpar.title()} {cy})"); pt["born"] = bdate(child) or pt.get("born"); pt["bplace_text"] = cpar.title()
            if p in auto or p.get("_auto"):
                p.setdefault("src", [])
                if "LL:" + child["key"] not in p["src"]: p["src"].append("LL:" + child["key"])
                if not p.get("born") or len(str(p.get("born"))) < 10: p["born"] = bdate(child) or p.get("born")
                p["bplace_text"] = p.get("bplace_text") or cpar.title()
            line = p.get("line")
            mar = find_marriage(F["name_display"], M["name_display"], cy, cpar) if (F and M) else None
            for k, who, r in ((2*n, F, "Brudgom"), (2*n+1, M, "Brud")):
                if not who or k in known: continue
                np = {"ahnen": k, "id": f"a{k}", "name": who["name_display"].replace(" Født ", " f. "), "sex": "M" if k % 2 == 0 else "F",
                      "line": line, "src": ["LL:" + who["key"]], "_auto": True, "_parish": cpar,
                      "note": f"Nævnt som {'far' if k % 2 == 0 else 'mor'} i {('fødselsposten' )} for {p['name']} ({cpar.title()}, {cy})."}
                if mar:
                    sp = role(mar, r)
                    np["src"].append("LL:" + sp["key"])
                    np["born"] = bdate(sp)
                    np["bplace_text"] = (sp.get("birthplace_display") or "").split(",")[0].replace(" sogn", "").strip().title() or None
                    np["married"] = f"{mar[0].get('event_year_display') or ''} i {place_of(mar[0]).title()}"
                    np["note"] += f" Gift {np['married']}."
                    pf = role(mar, r + ("mens far" if r == "Brudgom" else "ens far")); pm = role(mar, r + ("mens mor" if r == "Brudgom" else "ens mor"))
                    np["_parents"] = [(x.get("name_display"), x["key"]) for x in (pf, pm) if x]
                    # forældrenes egen fødsel
                    for pl in parish_tokens(np.get("bplace_text"), place_of(mar[0]), cpar):
                        bg = find_birth(sp.get("name_display"), bdate(sp), pl) if bdate(sp) else None
                        if not bg: continue
                        bf = role(bg, "Far")
                        if np["_parents"] and bf and ov(bf.get("name_display"), np["_parents"][0][0]) < 1: continue
                        b = role(bg, "Barn"); np["born"] = bdate(b) or np["born"]; np["bplace_text"] = place_of(b).title()
                        np["src"].insert(0, "LL:" + b["key"]); break
                known[k] = np; auto.append(np); added += 1
                print(f"  + {k}: {np['name']} f. {np.get('born')} {np.get('bplace_text') or ''}", flush=True)
            json.dump(auto, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        # navne fra vielser uden fødselspost bliver næste generation (kun navn + kilde)
        for a in list(auto):
            n = a["ahnen"]
            if a.get("patch") and a.get("_parents") and (2*n in known or 2*n+1 in known): continue
            for i, (nm, key) in enumerate(a.get("_parents") or []):
                k = 2*n + i
                if k in known or not nm: continue
                np = {"ahnen": k, "id": f"a{k}", "name": nm.replace(" Født ", " f. "), "sex": "M" if k % 2 == 0 else "F", "line": known[n].get("line"),
                      "src": ["LL:" + key], "_auto": True, "_parish": a.get("_parish"),
                      "note": f"Nævnt som {'far' if i == 0 else 'mor'} i {known[n]['name']}s vielse."}
                known[k] = np; auto.append(np); added += 1
                print(f"  + {k}: {np['name']} (fra vielse)", flush=True)
        json.dump(auto, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"runde {rnd+1}: {added} nye", flush=True)
        if not added: break

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
