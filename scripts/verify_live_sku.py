#!/usr/bin/env python3
import json, re, sys, urllib.request

LIVE = "https://niccolomazzoleni-prog.github.io/Abra-Robotics"
sku = sys.argv[1] if len(sys.argv) > 1 else "B2-LIDAR"

j = json.loads(urllib.request.urlopen(f"{LIVE}/data/product-images.json", timeout=20).read())
path = j[sku]["path"]
html = urllib.request.urlopen(f"{LIVE}/catalogo-unitree.html", timeout=20).read().decode()
m = re.search(rf'data-sku="{sku}".*?src="([^"]+)"', html, re.S)
cat = m.group(1) if m else "MISSING"
slug = "unitree-b2-lidar.html" if sku == "B2-LIDAR" else None
if not slug:
    slug = json.loads(open("listini/pubblico/catalogo-manifest.json", encoding="utf-8").read())[sku]["slug"]
prod = urllib.request.urlopen(f"{LIVE}/prodotti/{slug}", timeout=20).read().decode()
pm = re.search(r'gallery-main-img" src="([^"]+)"', prod)
page = pm.group(1) if pm else "MISSING"
code = urllib.request.urlopen(f"{LIVE}/{path}", timeout=20).getcode()
print(f"SKU: {sku}")
print(f"JSON: {path}")
print(f"Catalogo: {cat}")
print(f"Scheda: {page}")
print(f"File: HTTP {code}")
ok = path in cat and path.split("/")[-1] in page and code == 200
print("RISULTATO:", "OK" if ok else "FALLITO")
sys.exit(0 if ok else 1)
