"""Story compiler: content/stories/*.md HTML fragments → STORIES 4-tuples."""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


def _esc_html(s: str) -> str:
    return (
        str(s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _clean_name(n: str) -> str:
    return re.sub(r"\s*\(.*?\)", "", str(n or ""), count=1)


def _js(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str).replace("</", "<\\/")


def compile_stories(stories_dir: Path, people_by_id: dict) -> str:
    """Compile content/stories/*.md HTML fragments into STORIES 4-tuples.

    Bodies are raw HTML fragments (not Markdown). Only [[id]] / [[id|label]]
    tokens are expanded to match the runtime L() helper exactly:
      <button class=\"linkish\" data-pid=\"ID\">NAME</button>
    """
    token_re = re.compile(r"\[\[([a-z0-9_]+)(?:\|([^\]]+))?\]\]")

    def expand_token(match: re.Match) -> str:
        pid = match.group(1)
        label = match.group(2)
        person = people_by_id.get(pid)
        if person is None:
            return f"<!-- unknown person: {pid} -->"
        if label is not None:
            name = label
        else:
            name = _clean_name(person.get("name") or pid)
        return f'<button class="linkish" data-pid="{pid}">{_esc_html(name)}</button>'

    stories = []
    if not stories_dir.is_dir():
        return _js([])

    for path in sorted(stories_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", raw, re.S)
        if not m:
            raise SystemExit(f"Story missing YAML front matter: {path}")
        meta = yaml.safe_load(m.group(1)) or {}
        body = m.group(2)
        if body.startswith("\n"):
            body = body[1:]
        if body.endswith("\n"):
            body = body[:-1]
        line = str(meta.get("line") or "maternal")
        title = str(meta.get("title") or path.stem)
        people = [str(x) for x in (meta.get("people") or [])]
        sort_key = meta.get("sort", 0)
        body_html = token_re.sub(expand_token, body)
        stories.append((sort_key, [line, title, body_html, people]))

    stories.sort(key=lambda item: (item[0], item[1][1]))
    return _js([item[1] for item in stories])
