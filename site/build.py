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

# Standalone copy for GitHub Pages (served from /docs on master).
docs = os.path.join(root, "docs")
os.makedirs(docs, exist_ok=True)
split = out.index('<div class="wrap">')
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + out[:split] + '</head>\n<body>\n' + out[split:] + '\n</body>\n</html>\n')
open(os.path.join(docs, "index.html"), "w", encoding="utf-8").write(page)
open(os.path.join(docs, ".nojekyll"), "w").close()
print("wrote docs/index.html")

# Slægtsplakat (zoombar online, udskrivbar). PDF'erne laves af site/make_pdfs.js.
ptpl = open(os.path.join(root, "site", "poster.html"), encoding="utf-8").read()
pdfs = [[f, f"https://sloev.github.io/tree/{f}"] for f in sorted(os.listdir(docs)) if f.endswith(".pdf")]
pdf_labels = {"plakat-A2-5-generationer.pdf": "A2, 5 generationer", "plakat-A1-alle-aner.pdf": "A1, alle aner",
              "plakat-A3-mors-side.pdf": "A3, mors side", "plakat-A3-fars-side.pdf": "A3, fars side"}
pdfs = [[pdf_labels.get(f, f), u] for f, u in pdfs]
pout = ptpl.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__PDFS__", json.dumps(pdfs, ensure_ascii=False))
open(os.path.join(root, "site", "plakat.html"), "w", encoding="utf-8").write(pout)
split = pout.index('<div class="bar">')
open(os.path.join(docs, "plakat.html"), "w", encoding="utf-8").write(
    '<!doctype html>\n<html lang="da">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + pout[:split] + '</head>\n<body>\n' + pout[split:] + '\n</body>\n</html>\n')
print("wrote site/plakat.html and docs/plakat.html")
