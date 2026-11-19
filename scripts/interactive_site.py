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
TEMPLATE = ROOT / "site" / "template-leaflet-maps.html"
DOCS = ROOT / "docs"
