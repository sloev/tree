"""Automatisk anesøgning i Link Lives: fødsel -> forældrenes vielse -> forældrenes fødsler -> ..."""
import re, json, sys
from ll import search, record, get, fmt
STOP = {'født', 'f', 'f.', 'gift'}
def toks(n): return {t for t in re.split(r'[\s.\-]+', (n or '').lower()) if t and t not in STOP}
def norm(t): return t.replace('th', 't').replace('ph', 'f').replace('ch', 'k').replace('c', 'k').replace('z', 's').replace('ie', 'i').replace('aa','å').rstrip('e')
def ov(a, b): A = {norm(x) for x in toks(a)}; B = {norm(x) for x in toks(b)}; return len(A & B)
def role(grp, r): return next((s for s in grp if s.get('role_display') == r), None)
def bdate(s): return (s.get('standard') or {}).get('birth_date') or s.get('birthyear_display')
def q(query, size=15):
    try: return [h['_source'] for h in search('pas', query, size=size)['hits']['hits']]
    except Exception as e: return []
def find_marriage(F, M, y, place=''):
    best = None
    for who, other, r1, r2 in ((M, F, 'Brud', 'Brudgom'), (F, M, 'Brudgom', 'Brud')):
        must = [{'term': {'source_id': 13}}, {'match': {'name_searchable_fz': {'query': who, 'minimum_should_match': '2<75%'}}},
                {'range': {'event_year_sortable': {'gte': y - 30, 'lte': y + 2}}}]
        should = [{'match': {'sourceplace_searchable': place}}] if place else []
        for h in q({'bool': {'must': must, 'should': should}}, 40):
            if h.get('role_display') != r1 or ov(h.get('name_display'), who) < min(2, len(toks(who))): continue
            grp = record(h['key']); o = role(grp, r2)
            if not o: continue
            sc = ov(o.get('name_display'), other)
            if sc >= min(2, len(toks(other))):
                sc += ov(h.get('name_display'), who) + (2 if place and place.split()[0] in (h.get('sourceplace_display') or '') else 0)
                if not best or sc > best[0]: best = (sc, grp)
        if best: break
    return best[1] if best else None
def find_birth(name, bd, place=''):
    if not bd: return None
    bd = str(bd); y = int(bd[:4])
    tries = []
    if re.match(r'\d{4}-\d\d-\d\d', bd):
        tries.append({'bool': {'must': [{'term': {'source_id': 12}}, {'match_phrase': {'standard.birth_date': bd}}, {'match': {'name_searchable_fz': name}}]}})
    must = [{'term': {'source_id': 12}}, {'range': {'event_year_sortable': {'gte': y, 'lte': y + 1}}}, {'match': {'firstnames_searchable_fz': name.split()[0]}}]
    if place: must.append({'match': {'sourceplace_searchable': place}})
    if place: tries.append({'bool': {'must': must, 'should': [{'match': {'name_searchable_fz': name}}]}})
    for qq in tries:
        for h in q(qq, 20):
            if h.get('role_display') == 'Barn' and ov(h.get('name_display'), name) >= min(2, len(toks(name))):
                hb = str(bdate(h) or '')
                if re.match(r'\d{4}-\d\d-\d\d', bd) and re.match(r'\d{4}-\d\d-\d\d', hb):
                    from datetime import date
                    d1 = date(*map(int, bd.split('-'))); d2 = date(*map(int, hb.split('-')))
                    if abs((d2 - d1).days) > 60: continue
                return record(h['key'])
    return None
def census_parents(child_name, child_bd):
    """Finder forældrenes navne og fødselsdatoer via barnets husstand i folketællingerne 1901-1921 (og 1880-90)."""
    out = {}
    if not child_bd: return out
    hits = q({'bool': {'must': [{'terms': {'source_id': [9, 23, 24, 25, 22, 8, 7, 6, 5, 4, 3, 2, 1]}}, {'match_phrase': {'standard.birth_date': child_bd}} if re.match(r'\d{4}-\d\d-\d\d', str(child_bd)) else {'term': {'birthyear_sortable': int(str(child_bd)[:4])}},
                                {'match': {'name_searchable_fz': child_name}}]}}, 20)
    for h in sorted(hits, key=lambda h: h.get('source_id') in (9, 23, 24, 25), reverse=True):
        if ov(h.get('name_display'), child_name) < min(2, len(toks(child_name))): continue
        hh = (h.get('standard') or {}).get('household_id')
        if not hh: continue
        mem = q({'bool': {'must': [{'term': {'source_id': h['source_id']}}, {'term': {'standard.household_id': hh}}]}}, 40)
        for m in mem:
            r = (m.get('standard') or {}).get('household_position') or m.get('role_display') or ''
            if r in ('husfader', 'husmoder') and m['key'] != h['key']:
                out.setdefault(r, (m.get('name_display'), bdate(m), m.get('birthplace_display'), m['key']))
        if len(out) == 2: break
    return out
def person(s): return {'key': s['key'], 'name': s.get('name_display'), 'born': bdate(s), 'bplace': s.get('birthplace_display'), 'where': s.get('sourceplace_display')}
def climb(birth_grp, depth):
    child = role(birth_grp, 'Barn'); F = role(birth_grp, 'Far'); M = role(birth_grp, 'Mor')
    node = {'birth': person(child) if child else None, 'father': None, 'mother': None}
    if depth == 0 or not (F and M): 
        if F: node['father'] = {'name': F.get('name_display'), 'key': F['key']}
        if M: node['mother'] = {'name': M.get('name_display'), 'key': M['key']}
        return node
    y = child.get('event_year_sortable') or 1800
    place = (child.get('sourceplace_display') or '').split(',')[0].replace(' sogn','')
    mar = find_marriage(F['name_display'], M['name_display'], int(y), place)
    for side, who, pr in (('father', F, 'Brudgom'), ('mother', M, 'Brud')):
        n = {'name': who.get('name_display'), 'key': who['key']}
        if mar:
            sp = role(mar, pr); n.update({'marriage': mar[0]['key'], 'married': mar[0].get('event_year_display'), 'mplace': mar[0].get('sourceplace_display'), 'born': bdate(sp), 'bplace': sp.get('birthplace_display'), 'age_key': sp['key']})
            pf = role(mar, pr + ('mens far' if pr == 'Brudgom' else 'ens far')); pm = role(mar, pr + ('mens mor' if pr == 'Brudgom' else 'ens mor'))
            n['parents_named'] = [x.get('name_display') for x in (pf, pm) if x]
            places = [(sp.get('birthplace_display') or '').split(',')[0].replace(' sogn','').strip(), (mar[0].get('sourceplace_display') or '').split(',')[0].replace(' sogn','').strip(), place]
            bg = None
            for pl in [p for p in places if p]:
                bg = find_birth(sp.get('name_display'), bdate(sp), pl)
                if bg: break
            if bg: n['up'] = climb(bg, depth - 1)
        if not n.get('born'):
            cp = census_parents(child.get('name_display'), bdate(child))
            c = cp.get('husfader' if side == 'father' else 'husmoder')
            if c and ov(c[0], who.get('name_display')) >= 1:
                n.update({'born': c[1], 'bplace': c[2], 'census_key': c[3]})
                bp = (c[2] or '').split(',')[0].replace(' sogn','')
                bg = find_birth(c[0], c[1], bp) or find_birth(who.get('name_display'), c[1], bp)
                if bg: n['up'] = climb(bg, depth - 1)
        node[side] = n
    return node
def show(node, ind=0):
    p = ' ' * ind
    if node.get('birth'): b = node['birth']; print(f"{p}* {b['name']} f. {b['born']} [{b['key']}] {b['where']}")
    for side in ('father', 'mother'):
        n = node.get(side)
        if not n: continue
        print(f"{p}  {'Far' if side=='father' else 'Mor'}: {n['name']} f. {n.get('born')} {n.get('bplace') or ''} | vielse {n.get('married')} {n.get('mplace') or ''} [{n.get('marriage')}] forældre: {n.get('parents_named')} census:{n.get('census_key')}")
        if n.get('up'): show(n['up'], ind + 4)
if __name__ == '__main__':
    key, depth = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4
    tree = climb(record(key), depth); show(tree)
    json.dump(tree, open(f'/tmp/claude-0/dl/climb_{key}.json', 'w'), ensure_ascii=False, indent=1)
def up(name, bd, depth=4, place=''):
    bg = find_birth(name, bd, place)
    if not bg: print('  (ingen fødselspost fundet for', name, bd, ')'); return None
    t = climb(bg, depth); show(t); return t
