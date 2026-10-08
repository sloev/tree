import json,sys,urllib.request
ES="https://data.link-lives.rigsarkivet.dk"
def search(index,query,size=200,sort=None):
    body={"size":size,"query":query}
    if sort: body["sort"]=sort
    req=urllib.request.Request(f"{ES}/{index}/_search",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    import time
    for k in range(8):  # Link Lives svarer 503 under belastning: vent og prøv igen
        try: return json.load(urllib.request.urlopen(req,timeout=120))
        except Exception as e:
            if k==7: raise
            time.sleep(min(60, 3*2**k))
def fmt(s):
    st=s.get("standard") or {}
    return f'{s.get("key"):>12} {s.get("event_type_display") or "":11} {(s.get("standard") or {}).get("event_date") or s.get("event_year_display") or "":10} | {s.get("name_display")} b.{(s.get("standard") or {}).get("birth_date") or s.get("birthyear_display")} age:{(s.get("standard") or {}).get("age","")} {s.get("birthplace_display") or ""} | {s.get("sourceplace_display")} | occ:{s.get("occupation_searchable") or ""} | role:{st.get("household_position") or s.get("role_display") or ""} hh:{st.get("household_id","")} ms:{st.get("marital_status","")}'
if __name__=="__main__":
    q=json.loads(sys.argv[1]); idx=sys.argv[2] if len(sys.argv)>2 else "pas"
    r=search(idx,q,sort=[{"event_year_sortable":"asc"}] if idx=="pas" else None)
    print("total",r["hits"]["total"]["value"])
    for h in r["hits"]["hits"]: print(fmt(h["_source"]))

def get(key):
    r=search("pas",{"term":{"key":key}},size=1)["hits"]["hits"]
    return r[0]["_source"] if r else None
def record(key):
    s=get(key)
    if not s: return []
    sid=s["source_id"]; g=s["pa_grouping_id_wp4"]
    if not g: return [s]
    r=search("pas",{"bool":{"must":[{"term":{"source_id":sid}},{"term":{"pa_grouping_id_wp4":g}}]}},size=60)
    return [h["_source"] for h in r["hits"]["hits"]]
def lifecourse(key):
    sid,pid=key.split("-")
    r=search("lifecourses",{"bool":{"should":[{"term":{"links.paKeys":key}},{"match":{"pa_ids":pid}}]}},size=5)
    out=[]
    for h in r["hits"]["hits"]:
        lc=h["_source"]
        keys=set()
        for l in lc.get("links",[]): keys.update(l.get("paKeys",[]))
        if key in keys: out.append((lc["life_course_id"],[pa for pa in lc.get("person_appearance",[])]))
    return out
