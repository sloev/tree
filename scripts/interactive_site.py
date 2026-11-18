#!/usr/bin/env python3
"""Compile every Markdown record into the sole shared interactive site and route data.

The HTML/CSS/interaction template is intentionally kept separate from the data compiler.
No tree.json or other editable JSON source is read or written.
"""
from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import shutil

from compile_content import read_records, private as is_private

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "site" / "template.html"
DOCS = ROOT / "docs"


def records(folder: str, schema: str):
    return read_records(folder, schema)


def site_slug(value: str) -> str:
    value = str(value).lower().replace("æ", "ae").replace("ø", "oe").replace("å", "aa")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-") or "item"


def js(value) -> str:
    # Prevent content values from terminating an inline script element.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def section(body: str, heading: str) -> str:
    match = re.search(
        r"^##\s+" + re.escape(heading) + r"\s*\n(.*?)(?=^##\s|\Z)",
        body, re.I | re.M | re.S,
    )
    return match.group(1).strip() if match else ""


def build():
    if not TEMPLATE.is_file():
        raise SystemExit("Missing site/template.html; refusing to replace the front page")

    people_records = records("people", "person/v1")
    claims_records = records("claims", "claim/v1")
    media_records = records("media", "media/v1")
    place_records = records("places", "place/v1")
    source_records = records("sources", "source/v1")
    # The site configuration is a single Markdown record at content/site-config.md.
    import yaml
    cfg_path = ROOT / "content" / "site-config.md"
    cfg_match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", cfg_path.read_text(encoding="utf-8"), re.S)
    if not cfg_match:
        raise SystemExit("content/site-config.md has no YAML front matter")
    config = yaml.safe_load(cfg_match.group(1)) or {}
    vault_path = ROOT / "content" / "private-vault.md"
    vault_match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", vault_path.read_text(encoding="utf-8"), re.S)
    if not vault_match:
        raise SystemExit("content/private-vault.md has no YAML front matter")
    vault = yaml.safe_load(vault_match.group(1)) or {}
    if vault.get("schema") != "private-vault/v1" or not isinstance(vault.get("blob"), dict):
        raise SystemExit("Private vault Markdown record is invalid")
    enrichment_path = ROOT / "content" / "person-enrichment.md"
    enrichment_match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", enrichment_path.read_text(encoding="utf-8"), re.S)
    if not enrichment_match:
        raise SystemExit("content/person-enrichment.md has no YAML front matter")
    enrichment = yaml.safe_load(enrichment_match.group(1)) or {}
    if enrichment.get("schema") != "person-enrichment/v1" or not isinstance(enrichment.get("people"), dict):
        raise SystemExit("Person enrichment Markdown record is invalid")
    research_path = ROOT / "content" / "research-enrichment.md"
    research_match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", research_path.read_text(encoding="utf-8"), re.S)
    if not research_match:
        raise SystemExit("content/research-enrichment.md has no YAML front matter")
    research_extra = yaml.safe_load(research_match.group(1)) or {}
    if research_extra.get("schema") != "research-enrichment/v1" or not isinstance(research_extra.get("claims"), dict):
        raise SystemExit("Research enrichment Markdown record is invalid")
    activity_path = ROOT / "content" / "activity.md"
    activity_match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", activity_path.read_text(encoding="utf-8"), re.S)
    if not activity_match:
        raise SystemExit("content/activity.md has no YAML front matter")
    activity = yaml.safe_load(activity_match.group(1)) or {}
    if activity.get("schema") != "activity/v1":
        raise SystemExit("Activity Markdown record is invalid")

    map_records = records("maps", "map/v1")
    if len(map_records) != 1:
        raise SystemExit("Expected exactly one content/maps map/v1 record")
    map_meta = map_records[0][0]
    map_data = {k: map_meta[k] for k in ("W", "H", "bbox", "dk", "se", "de") if k in map_meta}
    if not all(k in map_data for k in ("W", "H", "bbox", "dk", "se", "de")):
        raise SystemExit("Map Markdown record is missing required geometry fields")

    people = []
    for meta, body, _path in people_records:
        hidden = is_private(meta)
        person = dict(meta)
        extra = enrichment["people"].get(str(meta["id"]), {})
        person.update({
            "name": "Privat person" if hidden else str(meta.get("name") or meta["id"]),
            "private": hidden,
            "permalink": "?person=" + str(meta["id"]),
            "born": None if hidden else meta.get("born"),
            "bplace": None if hidden else meta.get("bplace"),
            "died": None if hidden else meta.get("died"),
            "dplace": None if hidden else meta.get("dplace"),
            "living": bool(meta.get("living")),
            "occ": [] if hidden else (meta.get("occ") or []),
            "src": [] if hidden else (meta.get("src") if "src" in meta else extra.get("src") or []),
            "res": [] if hidden else (meta.get("res") if "res" in meta else extra.get("res") or []),
            "note": "" if hidden else (meta.get("note") or body or None),
            "rel": None if hidden else (meta.get("rel") if "rel" in meta else extra.get("rel")),
            "sibof": None if hidden else (meta.get("sibof") if "sibof" in meta else extra.get("sibof")),
            "step": None if hidden else (meta.get("step") if "step" in meta else extra.get("step")),
            "spouse": None if hidden else meta.get("spouse"),
            "relationship_claims": None if hidden else (meta.get("relationship_claims") if "relationship_claims" in meta else extra.get("relationship_claims")),
            "father": meta.get("father"),
            "mother": meta.get("mother"),
            "sex": meta.get("sex") or "U",
            "line": meta.get("line") or "maternal",
            "conf": meta.get("conf") or "told",
        })
        people.append(person)

    places = {}
    place_urls = {}
    place_details = []
    for meta, place_body, _path in place_records:
        name = str(meta.get("name") or meta["id"])
        coords = meta.get("data")
        if isinstance(coords, list) and len(coords) >= 3:
            places[name] = coords
            place_slug = site_slug(meta["id"])
            place_urls[name] = "?place=" + str(meta["id"]) + "#kort"
        place_details.append({"id": str(meta["id"]), "name": name, "data": coords, "body": place_body, "meta": meta})

    photos = []
    imgs = []
    for meta, media_body, _path in media_records:
        file = str(meta.get("file") or "")
        if not file:
            continue
        source = (ROOT / file).resolve()
        if ROOT.resolve() not in source.parents or not source.is_file():
            continue
        photos.append({
            "id": str(meta.get("id") or Path(file).stem),
            "file": file,
            "title": meta.get("title") or Path(file).stem,
            "caption": meta.get("caption") or "",
            "credit": meta.get("credit") or "",
            "link": meta.get("link") or file,
            "person_ids": [str(x) for x in (meta.get("person_ids") or [])],
            "claim_ids": [str(x) for x in (meta.get("claim_ids") or [])],
            "source_ids": [str(x) for x in (meta.get("source_ids") or [])],
            "evidence_role": meta.get("evidence_role") or "unverified",
            "original_url": meta.get("original_url"),
            "accessed": meta.get("accessed"),
            "rights": meta.get("rights"),
            "body": media_body,
            "meta": meta,
        })

    claims = []
    for meta, body, _path in claims_records:
        extra = research_extra["claims"].get(str(meta["id"]), {})
        claims.append({
            "id": str(meta["id"]),
            "branch": meta.get("branch") or "",
            "title": meta.get("title") or str(meta["id"]),
            "status": meta.get("status") or "needs",
            "claim": section(body, "Claim"),
            "evidence": section(body, "Evidence"),
            "missing": section(body, "Missing"),
            "next": section(body, "Next"),
            "sources": meta.get("sources") if "sources" in meta else extra.get("sources") or [],
            "person_ids": meta.get("person_ids") if "person_ids" in meta else extra.get("person_ids") or [],
            "research_notes": meta.get("research_notes") if "research_notes" in meta else extra.get("research_notes") or [],
            "dossier": meta.get("dossier") or extra.get("dossier"),
        })

    if config.get("photo_order"):
        order = {str(name): index for index, name in enumerate(config["photo_order"])}
        photos.sort(key=lambda item: (order.get(item["file"], len(order)), item["file"]))

    # Keep image paths in exactly the same order as DATA.photos. The person
    # drawer resolves a photo object to its array index, then reads IMGS[index].
    # Building IMGS before the custom photo sort silently paired captions with
    # different image files (including the Sofus gravestone under Evald).
    imgs = ["media/" + Path(item["file"]).name for item in photos]

    source_details = [{"id": str(meta["id"]), "title": str(meta.get("label") or meta.get("title") or meta["id"]), "meta": meta, "body": body} for meta, body, _path in source_records]
    media_details = [{"id": str(meta["id"]), "title": str(meta.get("title") or meta["id"]), "meta": meta, "body": body} for meta, body, _path in media_records]
    data = {
        "people": people,
        "place_details": place_details,
        "source_details": source_details,
        "media_details": media_details,
        "places": places,
        "place_urls": place_urls,
        "lines": config.get("lines") or {},
        "cats": config.get("cats") or [],
        "photos": photos,
        "links": config.get("links") or [],
        "sources": config.get("sources") or [],
        "private_blob": vault["blob"],
    }
    research = {"claims": claims}

    bulletins = activity.get("bulletins") or []
    def bulletin_timestamp(item):
        value = item.get("created_at") or item.get("date") or ""
        try:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.timestamp()
        except (TypeError, ValueError, OverflowError):
            return 0

    bulletin_html = ""
    for item in sorted((x for x in bulletins if isinstance(x, dict)), key=bulletin_timestamp, reverse=True):
        date = html.escape(str(item.get("date") or ""))
        label = html.escape(str(item.get("date_label") or date))
        title = html.escape(str(item.get("title") or "Opdatering om slægtsforskningen"))
        body = html.escape(str(item.get("body") or ""))
        created_at = html.escape(str(item.get("created_at") or date))
        bulletin_html += (
            f'<article class="bulletin-item auto-bulletin" data-created-at="{created_at}">'
            f'<time datetime="{date}">{label}</time><span class="conf probable">Automatisk opdatering</span>'
            f'<h3>{title}</h3><p>{body}</p></article>'
        )

    # Homepage statistics are computed from Markdown source records, never snapshots.
    def confirmed_date(value):
        match = re.fullmatch(r"(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?", str(value or ""))
        if not match:
            return None
        try:
            return datetime(int(match.group(1)), int(match.group(2) or 1), int(match.group(3) or 1))
        except ValueError:
            return None

    def display_date(value):
        parsed = confirmed_date(value)
        if not parsed:
            return str(value or "")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value)):
            return parsed.strftime("%d.%m.%Y")
        if re.fullmatch(r"\d{4}-\d{2}", str(value)):
            return parsed.strftime("%m.%Y")
        return parsed.strftime("%Y")

    oldest = {"born": None, "died": None}
    for meta, _body, _path in people_records:
        if meta.get("conf") != "record" or is_private(meta):
            continue
        for field in ("born", "died"):
            parsed = confirmed_date(meta.get(field))
            if parsed and (oldest[field] is None or parsed < oldest[field][0]):
                oldest[field] = (parsed, meta)

    current_counts = {
        "people": len(people_records),
        "claims": len(claims_records),
        "sources": len(source_records),
        "places": len(place_records),
        "media": len(media_records),
    }
    snapshot = activity.get("stats_snapshot") or {
        "date": "2026-11-18", "people": 494, "claims": 78,
        "sources": 19, "places": 54, "media": 11,
    }
    count_labels = [("people", "personer"), ("claims", "forskningsspor"), ("sources", "kilder"), ("places", "steder")]
    growth = []
    for key, label in count_labels:
        previous = snapshot.get(key)
        if isinstance(previous, int):
            delta = current_counts[key] - previous
            growth.append(f"{delta:+d} {label}")
    snapshot_date = str(snapshot.get("date") or "sidste opgørelse")
    try:
        snapshot_date = datetime.strptime(snapshot_date[:10], "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        pass
    open_claims = sum(1 for meta, _body, _path in claims_records if meta.get("status") in ("needs", "hypothesis", "conflict"))
    stat_items = [
        ("Personer", current_counts["people"], "i stamtræet"),
        ("Forskningsspor", current_counts["claims"], "samlede poster"),
        ("Åbne spor", open_claims, "kræver mere arbejde"),
        ("Kilder", current_counts["sources"], "registrerede kildeposter"),
        ("Steder", current_counts["places"], "stedsposter"),
        ("Billedposter", current_counts["media"], "knyttet til slægten"),
    ]
    stats_html = '<div class="home-stats-grid">' + "".join(
        f'<div class="home-stat"><span class="home-stat-value">{value:,}</span><span class="home-stat-label">{html.escape(label)}</span><span class="home-stat-note">{html.escape(note)}</span></div>'
        for label, value, note in stat_items
    ) + '</div>'
    oldest_html = []
    for field, label in (("born", "Ældste dokumenterede fødsel"), ("died", "Ældste dokumenterede dødsfald")):
        item = oldest[field]
        if item:
            _parsed, meta = item
            name = str(meta.get("name") or meta.get("id"))
            link = "people/" + site_slug(meta["id"]) + ".html"
            oldest_html.append(f'<div class="home-oldest-item"><span>{html.escape(label)}</span><a href="{html.escape(link, quote=True)}">{html.escape(name)}</a><b>{html.escape(display_date(meta.get(field)))}</b></div>')
    growth_text = " · ".join(growth) if growth else "ingen sammenlignelige tal"
    stats_html += '<div class="home-stats-bottom">' + "".join(oldest_html) + f'<p class="home-growth">Ændring siden {html.escape(snapshot_date)}: {html.escape(growth_text)}</p></div>'

    template = TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "__DATA__": js(data),
        "__MAP__": js(map_data),
        "__RECENT__": js(activity.get("people") or {}),
        "__IMGS__": js(imgs),
        "__RESEARCH__": js(research),
        "__AUTO_BULLETIN__": bulletin_html,
        "__STATS__": stats_html,
        # Keep the original encrypted private-person unlock behavior.
        "__UNLOCK_JS__": (ROOT / "site" / "unlock.js").read_text(encoding="utf-8"),
    }
    for marker, value in replacements.items():
        if marker not in template:
            raise SystemExit(f"Template placeholder missing: {marker}")
        template = template.replace(marker, value)

    if "__" in template and re.search(r"__[A-Z_]+__", template):
        raise SystemExit("Unexpanded template placeholder remains")


    # Copy only approved, referenced media into the publication directory.
    media_out = DOCS / "media"
    media_out.mkdir(parents=True, exist_ok=True)
    for item in photos:
        src = (ROOT / item["file"]).resolve()
        if ROOT.resolve() in src.parents and src.is_file():
            shutil.copy2(src, media_out / Path(item["file"]).name)
    for meta, _body, _path in source_records:
        local_copy = meta.get("local_copy")
        if local_copy:
            src = (ROOT / str(local_copy)).resolve()
            if ROOT.resolve() not in src.parents or not src.is_file():
                raise SystemExit(f"Missing/outside source local_copy: {meta['id']}: {local_copy}")
            dst = media_out / "files" / "captures" / src.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    # Stable legacy paths are redirects, never a second rendering system.
    def write_redirect(path: Path, title: str, target: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        safe = html.escape(target, quote=True)
        page = (
            '<!doctype html><html lang="da"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta http-equiv="refresh" content="0;url=' + safe + '">'
            '<link rel="canonical" href="' + safe + '"><title>' +
            html.escape(title) + '</title></head><body><p>Åbner i den fælles slægtsvisning. '
            '<a href="' + safe + '">Fortsæt</a>.</p><script>location.replace(' +
            js(target) + ')</script></body></html>'
        )
        path.write_text(page, encoding="utf-8")

    legacy = [
        ("people", people_records, "person", lambda m: str(m.get("name") or m["id"])),
        ("places", place_records, "place", lambda m: str(m.get("name") or m["id"])),
        ("research", claims_records, "claim", lambda m: str(m.get("title") or m["id"])),
        ("sources", source_records, "source", lambda m: str(m.get("label") or m.get("title") or m["id"])),
        ("media", media_records, "media", lambda m: str(m.get("title") or m["id"])),
    ]
    index_targets = {
        "people": "../#personer", "places": "../#kort", "research": "../#forskning",
        "sources": "../#kilder", "media": "../#kilder",
    }
    for folder, items, query, title_for in legacy:
        out_dir = DOCS / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for meta, _body, _path in items:
            rid = str(meta["id"])
            suffix = {"person":"", "place":"#kort", "claim":"#forskning",
                      "source":"#kilder", "media":"#kilder"}[query]
            target = "../?" + query + "=" + rid + suffix
            write_redirect(out_dir / (site_slug(rid) + ".html"), title_for(meta), target)
        write_redirect(out_dir / "index.html", folder, index_targets[folder])

    persons_dir = DOCS / "persons"
    persons_dir.mkdir(parents=True, exist_ok=True)
    write_redirect(persons_dir / "index.html", "Personer", "../#personer")
    old_css = DOCS / "assets" / "site.css"
    if old_css.exists():
        old_css.unlink()

    site_output = ROOT / "site" / "index.html"
    site_output.write_text(template, encoding="utf-8")

    split_marker = '<div class="wrap">'
    if split_marker not in template:
        raise SystemExit("Original interactive page wrapper is missing")
    split = template.index(split_marker)
    page = (
        '<!doctype html>\n<html lang="da">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + template[:split] + '</head>\n<body>\n' + template[split:] + '\n</body>\n</html>\n'
    )
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(page, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    required = ('id="stamtrae"', 'id="drawer"', 'function renderPed', 'function renderKort', 'function renderTal')
    if not all(token in page for token in required):
        raise SystemExit("Interactive front-page smoke test failed")

    print(
        f"Built original interactive front page from Markdown: "
        f"{len(people)} people, {len(claims)} research claims, "
        f"{len(places)} mapped places, {len(photos)} photos"
    )


if __name__ == "__main__":
    build()
