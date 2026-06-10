#!/usr/bin/env python3
"""Genera merchant-feed.xml per Google Merchant Center (Unitree + AMR)."""
from __future__ import annotations

import glob
import html
import re
import sys
from pathlib import Path

_PROD = Path(__file__).resolve().parent
sys.path.insert(0, str(_PROD))
try:
    from _site import SITE  # noqa: E402
except ImportError:
    SITE = "https://abrarobotics.com"

SITE_SLASH = SITE + "/"


def grab(pattern: str, text: str, default: str = "") -> str:
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default


def parse_price(text: str) -> str | None:
    m = re.search(r'"price":\s*"(\d+\.\d{1,2})"', text)
    if not m:
        return None
    return f"{float(m.group(1)):.2f} EUR"


def parse_brand(text: str, default: str = "Unitree") -> str:
    m = re.search(r'"brand":\s*\{\s*"@type":\s*"Brand",\s*"name":\s*"([^"]+)"', text)
    return m.group(1) if m else default


def image_url(text: str, path: str) -> str:
    gal = grab(r'id="gallery-main-img"\s+src="([^"]*)"', text)
    if gal:
        if gal.startswith("http"):
            return gal
        if gal.startswith("../"):
            return SITE + "/" + gal[3:]
        return SITE_SLASH + "prodotti/" + gal.lstrip("./")
    og = grab(r'<meta\s+property="og:image"\s+content="(.*?)"', text)
    if og.startswith("http"):
        return og
    return SITE + "/" + og.lstrip("/")


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def load_items() -> tuple[list[dict], list[str]]:
    items: list[dict] = []
    skipped: list[str] = []
    patterns = ["unitree-*.html", "amr-*.html"]
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            text = open(path, encoding="utf-8").read()
            price = parse_price(text)
            if not price:
                skipped.append(path)
                continue
            title = html.unescape(grab(r"<title>(.*?)</title>", text)).split("|")[0].strip()
            desc = html.unescape(grab(r'<meta\s+name="description"\s+content="(.*?)"', text))
            link = grab(r'<link\s+rel="canonical"\s+href="(.*?)"', text, SITE_SLASH + "prodotti/" + path)
            brand = parse_brand(text)
            product_type = "AMR" if path.startswith("amr-") else "Robot Unitree"
            items.append({
                "id": path.replace(".html", ""),
                "title": title,
                "description": desc,
                "link": link,
                "image": image_url(text, path),
                "price": price,
                "brand": brand,
                "product_type": product_type,
            })
    return items, skipped


def main() -> None:
    items, skipped = load_items()
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
      <g:brand>{esc(it['brand'])}</g:brand>
      <g:condition>new</g:condition>
      <g:product_type>{esc(it['product_type'])}</g:product_type>
      <g:google_product_category>Business &amp; Industrial &gt; Material Handling</g:google_product_category>
      <g:identifier_exists>no</g:identifier_exists>
    </item>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Abra Robotics — Catalogo prodotti</title>
    <link>{SITE_SLASH}</link>
    <description>Feed prodotti Unitree e AMR per Google Merchant Center</description>
{chr(10).join(rows)}
  </channel>
</rss>
"""
    out = Path(__file__).resolve().parent.parent / "merchant-feed.xml"
    out.write_text(xml, encoding="utf-8")
    amr_n = sum(1 for i in items if i["id"].startswith("amr-"))
    print(f"Scritto {out.name} con {len(items)} prodotti ({amr_n} AMR).")
    if skipped:
        print(f"\nSALTATI senza prezzo ({len(skipped)}):")
        for s in skipped[:20]:
            print("  -", s)


if __name__ == "__main__":
    main()
