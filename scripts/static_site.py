#!/usr/bin/env python3
"""Markdown + media -> static HTML. No JSON runtime."""
from pathlib import Path
import html, re, shutil, os
ROOT=Path(__file__).resolve().parents[1]; CONTENT=ROOT/"content"; DOCS=ROOT/"docs"
LABEL={"record":"Godt belagt","told":"Familieoplysning","probable":"Kræver mere belæg","possible":"Foreløbig hypotese"}
STATUS={"needs":"Kræver mere belæg","hypothesis":"Foreløbig hypotese","family":"Familieoplysning","conflict":"Kildekonflikt"}
LINES={"self":"Dig selv","jorgensen":"Jørgensen-linjen","gaardsted":"Gaardsted-linjen","rousing":"Rousing-linjen (Fuglslev)","maternal":"Morfars fars slægt: Petersen, Nybøl og Dybbøl","gedde":"Gedde- og von Kleist-linjen","larsen":"Mormors slægt: Larsen, Holgersen og Langø","frederiksen":"Stedfarens slægt (Frederiksen, Broager)"}
def e(x): return html.escape(str(x if x is not None else ""),quote=True)
def read(p):
 import yaml
 raw=p.read_text(encoding="utf-8"); z=re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z",raw,re.S)
 if not z: raise ValueError(str(p)+" has no front matter")
 m=yaml.safe_load(z.group(1)) or {}
 if not isinstance(m,dict) or not m.get("id") or not m.get("schema"): raise ValueError(str(p)+" needs id and schema")
 return {"m":m,"body":z.group(2).strip()}
def group(folder,schema):
 d=CONTENT/folder; a=[read(p) for p in sorted(d.glob("*.md"))] if d.exists() else []
 a=[x for x in a if x["m"].get("schema")==schema]
 ids=[x["m"]["id"] for x in a]
 if len(ids)!=len(set(ids)): raise ValueError("Duplicate IDs in "+folder)
 return a
def inline(s):
 s=e(s); s=re.sub(r"\[([^\]]+)\]\((https?://[^ )]+)\)",r'<a href="\2" rel="noopener">\1</a>',s)
 s=re.sub(r"\*\*(.+?)\*\*",r"<strong>\1</strong>",s); return re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)",r"<em>\1</em>",s)
def md(s,page=None):
 import markdown
 # Source Markdown points to repository-local images; generated pages use the published copy.
 if page:
  s=s.replace("../../images/","../media/")
  s=s.replace("../../media/files/captures/","../media/files/captures/")
 return markdown.markdown(s, extensions=["tables","fenced_code","sane_lists"])
def slug(x):
 s=str(x).lower().replace("æ","ae").replace("ø","oe").replace("å","aa")
 return re.sub(r"[^a-z0-9]+","-",s).strip("-") or "item"
def private(p):
 m=p["m"]; y=str(m.get("born") or "")
 if m.get("public_consent") is True and not m.get("private"): return False
 return m.get("private") is True or m.get("living") is True or bool(re.match(r"^(19(2[6-9]|[3-9]\d)|20\d\d)",y) and not m.get("died"))
def pname(p): return "Privat person" if private(p) else str(p["m"].get("name") or p["m"]["id"])
def href(page,target): return Path(os.path.relpath(target,Path(page).parent)).as_posix()
def a(page,target,label): return '<a href="'+e(href(page,target))+'">'+e(label)+'</a>'
def layout(page,title,body,active=""):
 nav=[("index.html","Forside","home"),("persons/index.html","Personer","people"),("research/index.html","Forskning","research"),("sources/index.html","Kilder","sources"),("places/index.html","Steder","places"),("family-tree.ged","GEDCOM","ged")]
 links="".join('<a '+('aria-current="page" ' if active==k else '')+'href="'+e(href(page,"docs/"+p))+'">'+t+'</a>' for p,t,k in nav)
 return '<!doctype html><html lang="da"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+' · Slægten Gårdsted &amp; Gedde</title><link rel="stylesheet" href="'+e(href(page,"docs/assets/site.css"))+'"></head><body><header><a class="brand" href="'+e(href(page,"docs/index.html"))+'">Slægten Gårdsted <span>&amp; Gedde</span></a><nav>'+links+'</nav></header><main>'+body+'</main><footer>Genereret direkte fra Markdown og mediefiler · <a href="https://github.com/sloev/tree">Kildekode</a></footer></body></html>'
def build():
 people=group("people","person/v1"); claims=group("claims","claim/v1"); sources=group("sources","source/v1"); media=group("media","media/v1"); places=group("places","place/v1"); unions=group("unions","union/v1")
 if len(people)<100: raise SystemExit("Too few people; not replacing docs/")
 byid={str(p["m"]["id"]):p for p in people}; place_by_name={str(x["m"].get("name") or x["m"]["id"]):x for x in places}; cp={}; union_by_person={}
 for u in unions:
  if u["m"].get("public") is True:
   for pid in u["m"].get("partners",[]) or []: union_by_person.setdefault(str(pid),[]).append(u)
 for c in claims:
  for pid in c["m"].get("person_ids",[]) or []: cp.setdefault(str(pid),[]).append(c)
 DOCS.mkdir(exist_ok=True); (DOCS/"assets").mkdir(exist_ok=True)
 css="""*{box-sizing:border-box}body{margin:0;background:#f7f6f0;color:#202820;font:16px/1.65 Georgia,serif}a{color:#315f4b;text-underline-offset:3px}header{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1rem max(1rem,calc((100vw - 1100px)/2));background:#fffefa;border-bottom:1px solid #dcded3}.brand{font-weight:bold;font-size:1.1rem;text-decoration:none;color:#202820}.brand span{color:#355b49}nav{display:flex;flex-wrap:wrap;gap:.5rem 1rem;font:600 .88rem system-ui}nav a{text-decoration:none;color:#657064}nav a[aria-current=page]{color:#355b49;text-decoration:underline}main{max-width:1100px;margin:2rem auto;padding:0 1.2rem;min-height:70vh}h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.15;font-weight:500}h2{font-size:1.5rem;font-weight:500;margin:2rem 0 .8rem}.lede{font-size:1.15rem;max-width:70ch;color:#485348}.eyebrow,.meta,.muted{font:.82rem/1.5 system-ui;color:#657064}.hero{padding:2rem 0;border-bottom:1px solid #dcded3}.stats,.grid,.facts{display:flex;flex-wrap:wrap;gap:1rem;margin:1.3rem 0}.stat,.card,.fact{background:#fffefa;border:1px solid #dcded3;border-radius:9px;padding:.9rem 1rem}.stat b{display:block;font:700 1.4rem system-ui}.grid .card{flex:1 1 230px}.facts .fact{flex:1 1 160px}.fact b{display:block;font:600 .75rem system-ui;color:#657064}.list{padding:0;list-style:none}.list li{padding:.7rem 0;border-bottom:1px solid #dcded3}table{width:100%;border-collapse:collapse;background:#fffefa}td,th{text-align:left;padding:.65rem;border-bottom:1px solid #dcded3}th{font:600 .8rem system-ui;color:#657064}.pill{background:#eaf0e8;border-radius:20px;padding:.12rem .55rem;font:.75rem system-ui}.search{width:100%;max-width:34rem;padding:.8rem;border:1px solid #aeb8aa;border-radius:7px;font:inherit;margin:.4rem 0 1rem}.prose{max-width:78ch}img{max-width:100%;height:auto}footer{border-top:1px solid #dcded3;padding:1.5rem max(1rem,calc((100vw - 1100px)/2));font:.8rem system-ui;color:#657064}@media(max-width:700px){header{align-items:flex-start;flex-direction:column}}"""
 (DOCS/"assets/site.css").write_text(css+"\n",encoding="utf-8")
 for x in media:
  f=x["m"].get("file")
  if f:
   src=(ROOT/str(f)).resolve()
   if ROOT.resolve() in src.parents and src.is_file():
    dst=DOCS/"media"/Path(f).name; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); x["published"]="docs/media/"+Path(f).name
 # Person pages
 for p in people:
  m=p["m"]; pid=str(m["id"]); page="docs/people/"+slug(pid)+".html"; hidden=private(p); facts=[]
  if hidden: facts=[("Privatliv","Personoplysninger er skjult")]
  else:
   for label,key in [("Født","born"),("Fødested","bplace"),("Død","died"),("Dødssted","dplace"),("Erhverv","occ"),("Kildestatus","conf"),("Slægtslinje","line")]:
    v=m.get(key)
    if v: facts.append((label,"; ".join(map(str,v)) if isinstance(v,list) else LABEL.get(v,LINES.get(v,v))))
  def fact_value(label,value):
   if label in ("Fødested","Dødssted") and str(value) in place_by_name:
    place=place_by_name[str(value)]
    return a(page,"docs/places/"+slug(place["m"]["id"])+".html",str(value))
   return e(value)
  fh="".join('<div class="fact"><b>'+e(k)+'</b>'+fact_value(k,v)+'</div>' for k,v in facts); rels=[]
  if not hidden:
   for role,key in [("Far","father"),("Mor","mother"),("Ægtefælle","spouse")]:
    rid=str(m.get(key) or "")
    if rid in byid: rels.append("<li>"+role+": "+a(page,"docs/people/"+slug(rid)+".html",pname(byid[rid]))+"</li>")
   kids=[q for q in people if not private(q) and (q["m"].get("father")==pid or q["m"].get("mother")==pid)]
   if kids: rels.append("<li>Børn: "+", ".join(a(page,"docs/people/"+slug(q["m"]["id"])+".html",pname(q)) for q in kids)+"</li>")
  relhtml="<ul>"+"".join(rels)+"</ul>" if rels else '<p class="muted">Ingen offentligt viste relationer.</p>'
  historical=""
  if not hidden and union_by_person.get(pid):
   visible=[]
   for u in union_by_person[pid]:
    partners=[str(x) for x in u["m"].get("partners",[]) or []]; other=next((x for x in partners if x!=pid),None)
    if other in byid and not private(byid[other]): visible.append("<li>"+a(page,"docs/people/"+slug(other)+".html",pname(byid[other]))+" — "+e(STATUS.get(u["m"].get("status"),u["m"].get("status","")))+"</li>")
   if visible: historical="<h2>Historiske forhold</h2><ul>"+"".join(visible)+"</ul>"
  research=""
  if not hidden and cp.get(pid): research="<h2>Forskningsspor</h2><ul>"+"".join('<li>'+a(page,"docs/research/"+slug(c["m"]["id"])+".html",c["m"].get("title") or c["m"]["id"])+"</li>" for c in cp[pid])+"</ul>"
  notes="" if hidden else md(p["body"],page)
  citations="" if hidden or not m.get("src") else '<h2>Kildehenvisninger</h2><ul>'+ "".join("<li>"+e(v)+"</li>" for v in m.get("src",[])) + "</ul>"
  body='<p class="eyebrow">Personregister · '+e(pid)+'</p><h1>'+e(pname(p))+'</h1><div class="facts">'+fh+'</div><h2>Familie</h2>'+relhtml+historical+research+citations+'<section class="prose"><h2>Noter</h2>'+notes+'</section>'
  dest=DOCS/"people"/(slug(pid)+".html"); dest.parent.mkdir(exist_ok=True); dest.write_text(layout(page,pname(p),body,"people"),encoding="utf-8")
 # Persons index
 page="docs/persons/index.html"; rows=[]
 for p in sorted(people,key=lambda x:(pname(x).casefold(),str(x["m"]["id"]))):
  m=p["m"]; n=pname(p); search=(n+" "+str(m.get("bplace",""))+" "+str(m["id"])).casefold()
  rows.append('<tr data-search="'+e(search)+'"><td>'+a(page,"docs/people/"+slug(m["id"])+".html",n)+'</td><td>'+e("Privat" if private(p) else m.get("born",""))+'</td><td>'+e(LINES.get(m.get("line"),m.get("line","")))+'</td><td><span class="pill">'+e("Privat" if private(p) else LABEL.get(m.get("conf"),"Ikke angivet"))+'</span></td></tr>')
 (DOCS/"persons").mkdir(exist_ok=True)
 body='<p class="eyebrow">Register</p><h1>Personer</h1><p class="lede">'+str(len(people))+' personposter. Hver person har sin egen permanente HTML-side.</p><label for="q">Søg i personregisteret</label><input class="search" id="q" type="search" placeholder="Navn, sted eller ID"><table><thead><tr><th>Navn</th><th>Født</th><th>Linje</th><th>Kildestatus</th></tr></thead><tbody>'+"".join(rows)+'</tbody></table><script>document.getElementById("q").addEventListener("input",e=>{let q=e.target.value.toLocaleLowerCase("da");document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.dataset.search.includes(q));});</script>'
 (DOCS/"persons/index.html").write_text(layout(page,"Personer",body,"people"),encoding="utf-8")
 # Claims, rendered as independent pages
 claim_rows=[]
 for c in claims:
  m=c["m"]; cid=str(m["id"]); page="docs/research/"+slug(cid)+".html"; parts=[]
  for sec in ("Claim","Evidence","Missing","Next"):
   z=re.search(r"^##\s+"+sec+r"\s*\n(.*?)(?=^##\s|\Z)",c["body"],re.S|re.M|re.I)
   if z and z.group(1).strip(): parts.append("<h2>"+sec+"</h2><div class=\"prose\">"+md(z.group(1),page)+"</div>")
  ppl=[a(page,"docs/people/"+slug(pid)+".html",pname(byid[str(pid)])) for pid in m.get("person_ids",[]) or [] if str(pid) in byid and not private(byid[str(pid)])]
  src=[]
  for s in m.get("sources",[]) or []:
   if isinstance(s,dict) and s.get("url"): src.append('<li><a href="'+e(s["url"])+'">'+e(s.get("label") or s["url"])+'</a></li>')
   elif isinstance(s,str) and s.startswith("http"): src.append('<li><a href="'+e(s)+'">'+e(s)+'</a></li>')
  title=m.get("title") or cid; status=STATUS.get(m.get("status","needs"),m.get("status","needs"))
  body='<p class="eyebrow">Forskningsspor · '+e(m.get("branch",""))+'</p><h1>'+e(title)+'</h1><p><span class="pill">'+e(status)+'</span></p><div class="prose">'+md(c["body"],page)+'</div>'
  if ppl: body+='<h2>Tilknyttede personer</h2><ul>'+"".join("<li>"+x+"</li>" for x in ppl)+"</ul>"
  if src: body+='<h2>Kilder og videre læsning</h2><ul>'+"".join(src)+"</ul>"
  dest=DOCS/"research"/(slug(cid)+".html"); dest.parent.mkdir(exist_ok=True); dest.write_text(layout(page,title,body,"research"),encoding="utf-8")
  claim_rows.append('<li><span class="pill">'+e(status)+'</span> '+a("docs/research/index.html",page,title)+' <span class="meta">'+e(m.get("branch",""))+'</span></li>')
 (DOCS/"research").mkdir(exist_ok=True)
 (DOCS/"research/index.html").write_text(layout("docs/research/index.html","Forskning",'<p class="eyebrow">Forskningslog</p><h1>Forskningsspor</h1><p class="lede">'+str(len(claims))+' aktive spor.</p><ul class="list">'+"".join(claim_rows)+'</ul>',"research"),encoding="utf-8")
 # Sources
 source_rows=[]
 for s in sources:
  m=s["m"]; sid=str(m["id"]); page="docs/sources/"+slug(sid)+".html"; title=m.get("label") or m.get("title") or sid
  extra="".join('<p><b>'+lab+':</b> '+e(m[k])+'</p>' for k,lab in [("url","URL"),("archive","Arkiv"),("reference","Reference"),("file","Lokal fil")] if m.get(k))
  local_copy=m.get("local_copy")
  if local_copy:
   src=(ROOT/str(local_copy)).resolve()
   if ROOT.resolve() not in src.parents or not src.is_file(): raise SystemExit(f"Missing/outside source local_copy: {sid}: {local_copy}")
   published=DOCS/"media"/"files"/"captures"/src.name
   published.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,published)
   extra+='<p><b>Lokal kopi:</b> '+a(page,"docs/media/files/captures/"+src.name,"Åbn lokal kopi")+'</p>'
  dest=DOCS/"sources"/(slug(sid)+".html"); dest.parent.mkdir(exist_ok=True); dest.write_text(layout(page,title,'<p class="eyebrow">Kilde</p><h1>'+e(title)+'</h1>'+extra+'<div class="prose">'+md(s["body"],page)+'</div>',"sources"),encoding="utf-8")
  source_rows.append('<li>'+a("docs/sources/index.html",page,title)+'</li>')
 (DOCS/"sources").mkdir(exist_ok=True)
 (DOCS/"sources/index.html").write_text(layout("docs/sources/index.html","Kilder",'<p class="eyebrow">Dokumentation</p><h1>Kilder</h1><ul class="list">'+"".join(source_rows)+'</ul>',"sources"),encoding="utf-8")
 # Places and media: each record receives a stable, ID-based permalink.
 place_rows=[]
 for x in places:
  m=x["m"]; pid=str(m["id"]); name=str(m.get("name") or pid)
  page="docs/places/"+slug(pid)+".html"
  coords=m.get("data")
  coord_text=", ".join(map(str,coords)) if isinstance(coords,list) else str(coords or "")
  linked_people=[]
  for person in people:
   pm=person["m"]
   if not private(person) and (pm.get("bplace")==name or pm.get("dplace")==name):
    label="født her" if pm.get("bplace")==name else "død her"
    linked_people.append('<li>'+a(page,"docs/people/"+slug(pm["id"])+".html",pname(person))+' <span class="meta">'+label+'</span></li>')
  body='<p class="eyebrow">Sted · '+e(pid)+'</p><h1>'+e(name)+'</h1>'
  if coord_text: body+='<p class="meta">'+e(coord_text)+'</p>'
  body+='<h2>Tilknyttede personer</h2><ul class="list">'+("".join(linked_people) if linked_people else '<li class="meta">Ingen offentligt tilknyttede personer registreret.</li>')+'</ul>'
  if x["body"]: body+='<h2>Noter</h2><div class="prose">'+md(x["body"],page)+'</div>'
  dest=DOCS/"places"/(slug(pid)+".html"); dest.parent.mkdir(exist_ok=True); dest.write_text(layout(page,name,body,"places"),encoding="utf-8")
  place_rows.append('<li>'+a("docs/places/index.html",page,name)+' <span class="meta">'+e(coord_text)+'</span></li>')
 (DOCS/"places").mkdir(exist_ok=True)
 (DOCS/"places/index.html").write_text(layout("docs/places/index.html","Steder",'<p class="eyebrow">Geografi</p><h1>Steder</h1><p class="lede">Hvert registreret sted har sin egen permanente side.</p><ul class="list">'+"".join(place_rows)+'</ul>',"places"),encoding="utf-8")
 cards=[]
 for x in media:
  m=x["m"]
  if x.get("published"):
   mid=str(m["id"]); page="docs/media/"+slug(mid)+".html"; title=str(m.get("title") or mid)
   detail='<p class="eyebrow">Medie · '+e(mid)+'</p><h1>'+e(title)+'</h1><img src="'+e(href(page,x["published"]))+'" alt="'+e(title)+'"><p>'+e(m.get("caption") or x["body"])+'</p><p class="meta">'+e(m.get("credit",""))+'</p><p class="meta">Evidensrolle: '+e(m.get("evidence_role") or "unverified")+'</p>'
   if m.get("original_url"): detail+='<p class="meta">Oprindelig placering (provenance): <code>'+e(m["original_url"])+'</code></p>'
   dest=DOCS/"media"/(slug(mid)+".html"); dest.parent.mkdir(exist_ok=True); dest.write_text(layout(page,title,detail,"sources"),encoding="utf-8")
   cards.append('<article class="card"><a href="'+e(href("docs/media/index.html",page))+'"><img loading="lazy" src="'+e(href("docs/media/index.html",x["published"]))+'" alt="'+e(title)+'"></a><h3>'+a("docs/media/index.html",page,title)+'</h3><p>'+e(m.get("caption") or x["body"])+'</p><p class="meta">'+e(m.get("credit",""))+'</p></article>')
 if cards:
  (DOCS/"media").mkdir(exist_ok=True)
  (DOCS/"media/index.html").write_text(layout("docs/media/index.html","Billeder",'<h1>Billeder og dokumenter</h1><div class="grid">'+"".join(cards)+'</div>',"sources"),encoding="utf-8")
 # Home
 home='<section class="hero"><p class="eyebrow">En dokumenteret slægtshistorie</p><h1>Slægten Gårdsted &amp; Gedde</h1><p class="lede">En slægtsbog bygget på kirkebøger, folketællinger, arkivalier og familiehistorie. Hver person og hvert forskningsspor har sin egen permanente side.</p><div class="stats"><div class="stat"><b>'+str(len(people))+'</b>personer</div><div class="stat"><b>'+str(len(claims))+'</b>forskningsspor</div><div class="stat"><b>'+str(len(sources))+'</b>kilder</div><div class="stat"><b>'+str(len(media))+'</b>mediefiler</div></div></section><h2>Gå på opdagelse</h2><div class="grid"><article class="card"><h3>Personregister</h3><p>Personer og familierelationer.</p>'+a("docs/index.html","docs/persons/index.html","Åbn personregister →")+'</article><article class="card"><h3>Forskning</h3><p>Belæg, åbne spørgsmål og næste kildekontroller.</p>'+a("docs/index.html","docs/research/index.html","Se forskningsspor →")+'</article><article class="card"><h3>Kilder</h3><p>Kildehenvisninger fra Markdown-filerne.</p>'+a("docs/index.html","docs/sources/index.html","Se kilder →")+'</article><article class="card"><h3>Steder</h3>'+a("docs/index.html","docs/places/index.html","Se stedregister →")+'</article><article class="card"><h3>GEDCOM</h3><a href="family-tree.ged">Hent slægtstræet →</a></article></div><h2>Seneste forskningsspor</h2><ul class="list">'+"".join(claim_rows[-8:][::-1])+'</ul>'
 (DOCS/"index.html").write_text(layout("docs/index.html","Forside",home,"home"),encoding="utf-8")
 (DOCS/".nojekyll").write_text("",encoding="utf-8")
 print("Static HTML:",len(people),"people;",len(claims),"claims;",len(sources),"sources;",len(media),"media")
