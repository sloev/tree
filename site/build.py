"""Builds site/index.html (the visual family tree) from data/family.json."""
import base64, json, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(root, "data", "family.json"), encoding="utf-8"))
geo = json.load(open(os.path.join(root, "data", "map.json")))
imgs = []
for ph in data["photos"]:
    b = open(os.path.join(root, ph["file"]), "rb").read()
    imgs.append("data:image/jpeg;base64," + base64.b64encode(b).decode())
tpl = open(os.path.join(root, "site", "template.html"), encoding="utf-8").read()
out = (tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False))
          .replace("__MAP__", json.dumps(geo))
          .replace("__IMGS__", json.dumps(imgs)))
open(os.path.join(root, "site", "index.html"), "w", encoding="utf-8").write(out)
print("wrote site/index.html", len(out) // 1024, "KB")
