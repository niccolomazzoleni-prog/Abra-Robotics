#!/usr/bin/env python3
"""Genera il feed XML per Google Merchant Center dalle schede prodotto.

Uso:  python3 _gen_merchant_feed.py
Output: ../merchant-feed.xml

NB: i prodotti senza prezzo (campo .product-price-value assente) vengono SALTATI
e segnalati: Merchant Center richiede il campo price. Eseguire quando i prezzi
sono confermati.
"""
import glob, re, html, sys

SITE = "https://niccolomazzoleni-prog.github.io/Abra-Robotics/"

def grab(pattern, text, default=""):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default

def parse_price(text):
    # prezzo dallo schema JSON-LD: "price": "73276.98" -> "73276.98 EUR"
    m = re.search(r'"price":\s*"(\d+\.\d{1,2})"', text)
    if not m:
        return None
    return f"{float(m.group(1)):.2f} EUR"

items, skipped = [], []
for path in sorted(glob.glob("unitree-*.html")):
    text = open(path, encoding="utf-8").read()
    price = parse_price(text)
    if not price:
        skipped.append(path)
        continue
    title = html.unescape(grab(r"<title>(.*?)</title>", text)).split("|")[0].strip()
    desc = html.unescape(grab(r'<meta\s+name="description"\s+content="(.*?)"', text))
    link = grab(r'<link\s+rel="canonical"\s+href="(.*?)"', text, SITE + "prodotti/" + path)
    # immagine prodotto reale (gallery main); fallback all'og:image
    gal = grab(r'id="gallery-main-img"\s+src="([^"]*)"', text)
    if gal:
        image = gal if gal.startswith("http") else SITE + "prodotti/" + gal.lstrip("./")
    else:
        image = grab(r'<meta\s+property="og:image"\s+content="(.*?)"', text)
    items.append({
        "id": path.replace(".html", ""),
        "title": title, "description": desc, "link": link,
        "image": image, "price": price,
    })

def esc(s):
    return html.escape(s, quote=False)

rows = []
for it in items:
    rows.append(f"""    <item>
      <g:id>{esc(it['id'])}</g:id>
      <g:title>{esc(it['title'])}</g:title>
      <g:description>{esc(it['description'])}</g:description>
      <g:link>{esc(it['link'])}</g:link>
      <g:image_link>{esc(it['image'])}</g:image_link>
      <g:availability>in stock</g:availability>
      <g:price>{esc(it['price'])}</g:price>
      <g:brand>Unitree</g:brand>
      <g:condition>new</g:condition>
      <g:identifier_exists>no</g:identifier_exists>
    </item>""")

xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Abra Robotics — Catalogo prodotti</title>
    <link>{SITE}</link>
    <description>Feed prodotti per Google Merchant Center</description>
{chr(10).join(rows)}
  </channel>
</rss>
"""

open("../merchant-feed.xml", "w", encoding="utf-8").write(xml)
print(f"Scritto ../merchant-feed.xml con {len(items)} prodotti.")
if skipped:
    print(f"\nSALTATI (senza prezzo, {len(skipped)}):")
    for s in skipped:
        print("  -", s)
