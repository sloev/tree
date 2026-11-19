#!/usr/bin/env python3
"""Assemble interactive_site from parts and run build."""
import sys
from pathlib import Path
# Ensure scripts/ is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))
parts = []
for i in range(4):
    mod = __import__(f"_is_part{i}")
    parts.append(mod.PART)
    del sys.modules[f"_is_part{i}"]
src = "".join(parts)
# Write assembled file next to us for subsequent imports/runs, then exec
assembled = Path(__file__).resolve().parent / "_interactive_site_assembled.py"
assembled.write_text(src, encoding="utf-8")
ns = {"__name__": "__main__", "__file__": str(assembled)}
exec(compile(src, str(assembled), "exec"), ns)
