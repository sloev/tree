"""Deprecated compatibility entry point.

The former Python-authored genealogy database has been consolidated into data/tree.json.
Use python3 data/build.py, then python3 data/export.py and python3 site/build.py.
This file intentionally no longer writes data/family.json.
"""
raise SystemExit("data/build_data.py is retired; edit data/tree.json and run python3 data/build.py")
