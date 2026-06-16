#!/usr/bin/env python3
"""Genera merchant-feed.xml per Google Merchant Center (Unitree + AMR + Cobot)."""
from __future__ import annotations

import glob
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

_PROD = Path(__file__).resolve().parent
_ROOT = _PROD.parent
sys.path.insert(0, str(_PROD))
try:
    from _site import SITE  # noqa: E402
except ImportError:
    SITE = "https://abrarobotics.com"

SITE_SLASH = SITE + "/"

# Categorie Google per prefisso prodotto (fallback se assente nel JSON-LD)
_CATEGORY_DEFAULT = {
    "amr-": "Business & Industrial > Material Handling",
    "cobot-": "Business & Industrial > Industrial Machinery > Robotic Arms",
    "unitree-": "Business & Industrial > Robotics",
}

# product_type leggibile per prefisso
_PRODUCT_TYPE = {
    "amr-": "AMR",
    "cobot-": "Cobot Fairino",
    "unitree-": "Robot Unitree",
}


def grab(pattern: str, text: str, default: str = "") -> str:
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default


def grab_meta_desc(text: str) -> str:
    # [^"]* evita di attraversare virgolette, gestisce name/content e content/name
    m = re.search(
        r'<meta\s+(?:name="description"\s+content="([^"]*)"|content="([^"]*)"\s+name="description")',
        text,
        re.I,
    )
    if not m:
        return ""
    return html.unescape((m.group(1) or m.group(2) or "").strip())


def parse_price(text: str) -> str | None:
    m = re.search(r'"price":\s*"(\d+\.\d{1,2})"', text)
    if not m:
        return None
    return f"{float(m.group(1)):.2f} EUR"


def parse_brand(text: str, default: str = "Unitree") -> str:
    m = re.search(r'"brand":\s*\{\s*"@type":\s*"Brand",\s*"name":\s*"([^"]+)"', text)
    return m.group(1) if m else default


def parse_mpn(text: str) -> str:
    m = re.search(r'"mpn":\s*"([^"]+)"', text)
    return m.group(1) if m else ""


def parse_category(text: str) -> str:
    m = re.search(r'"category":\s*"([^"]+)"', text)
    return m.group(1) if m else ""


def image_url(text: str) -> str:
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


def load_availability() -> dict[str, str]:
    """Mappa slug famiglia → status GMC ('in stock' / 'preorder')."""
    avail_file = _ROOT / "availability.json"
    if not avail_file.exists():
        return {}
    data = json.loads(avail_file.read_text(encoding="utf-8"))
    raw = data.get("products", data)
    result: dict[str, str] = {}
    for key, info in raw.items():
        status = info.get("status", "unknown")
        if status == "available":
            result[key] = "in stock"
        elif status == "date":
            result[key] = "preorder"
        else:
            result[key] = "in stock"
    return result


def resolve_availability(product_id: str, avail_map: dict[str, str]) -> str:
    """Ricava lo stato di disponibilita reale per un prodotto Unitree."""
    if not product_id.startswith("unitree-") or not avail_map:
        return "in stock"
    slug = product_id[len("unitree-"):]  # es. "go2-pro", "g1-edu-standard-a"
    # Tenta dal piu lungo al piu corto per evitare che "g1" catturi "g1d"
    for key in sorted(avail_map, key=len, reverse=True):
        if slug == key or slug.startswith(key + "-"):
            return avail_map[key]
    return "in stock"


def category_for(product_id: str, from_html: str) -> str:
    if from_html:
        return from_html
    for prefix, cat in _CATEGORY_DEFAULT.items():
        if product_id.startswith(prefix):
            return cat
    return "Business & Industrial > Robotics"


def load_items(avail_map: dict[str, str]) -> tuple[list[dict], list[str]]:
    items: list[dict] = []
    skipped: list[str] = []
    patterns = ["unitree-*.html", "amr-*.html", "cobot-*.html"]
    for pattern in patterns:
        for path in sorted(glob.glob(pattern)):
            text = open(path, encoding="utf-8").read()
            price = parse_price(text)
            if not price:
                skipped.append(f"{path} (nessun prezzo)")
                continue
            pid = path.replace(".html", "")
            title = html.unescape(grab(r"<title>(.*?)</title>", text)).split("|")[0].strip()
            desc = grab_meta_desc(text)
            link = grab(r'<link\s+rel="canonical"\s+href="(.*?)"', text, SITE_SLASH + "prodotti/" + path)
            brand = parse_brand(text)
            mpn = parse_mpn(text)
            cat_html = parse_category(text)
            product_type = next((v for k, v in _PRODUCT_TYPE.items() if pid.startswith(k)), "Robot")
            items.append({
                "id": pid,
                "title": title,
                "description": desc,
                "link": link,
                "image": image_url(text),
                "price": price,
                "brand": brand,
                "mpn": mpn,
                "product_type": product_type,
                "category": category_for(pid, cat_html),
                "availability": resolve_availability(pid, avail_map),
            })
    return items, skipped


def build_xml(items: list[dict]) -> str:
    rows = []
    for it in items:
        identifier_block = (
            f"      <g:mpn>{esc(it['mpn'])}</g:mpn>"
            if it["mpn"]
            else "      <g:identifier_exists>no</g:identifier_exists>"
        )
        rows.append(
            f"""    <item>
      <g:id>{esc(it['id'])}</g:id>
      <g:title>{esc(it['title'])}</g:title>
      <g:description>{esc(it['description'])}</g:description>
      <g:link>{esc(it['link'])}</g:link>
      <g:image_link>{esc(it['image'])}</g:image_link>
      <g:availability>{it['availability']}</g:availability>
      <g:price>{esc(it['price'])}</g:price>
      <g:brand>{esc(it['brand'])}</g:brand>
      <g:condition>new</g:condition>
      <g:product_type>{esc(it['product_type'])}</g:product_type>
      <g:google_product_category>{esc(it['category'])}</g:google_product_category>
{identifier_block}
    </item>"""
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Abra Robotics — Catalogo prodotti</title>
    <link>{SITE_SLASH}</link>
    <description>Feed prodotti Unitree, AMR e Cobot per Google Merchant Center</description>
{chr(10).join(rows)}
  </channel>
</rss>
"""


def validate_xml(content: str) -> bool:
    try:
        ET.fromstring(content.encode("utf-8"))
        return True
    except ET.ParseError as e:
        print(f"ERRORE XML: {e}", file=sys.stderr)
        return False


def main() -> None:
    avail_map = load_availability()
    items, skipped = load_items(avail_map)

    if not items:
        print("ERRORE: nessun prodotto trovato — feed non scritto.", file=sys.stderr)
        sys.exit(1)

    xml_content = build_xml(items)

    if not validate_xml(xml_content):
        print("ERRORE: XML non valido — feed non scritto.", file=sys.stderr)
        sys.exit(1)

    out = _ROOT / "merchant-feed.xml"
    out.write_text(xml_content, encoding="utf-8")

    # Riepilogo
    by_type: dict[str, int] = {}
    for it in items:
        by_type[it["product_type"]] = by_type.get(it["product_type"], 0) + 1
    preorder_n = sum(1 for it in items if it["availability"] == "preorder")
    mpn_n = sum(1 for it in items if it["mpn"])

    print(f"Scritto {out.name} con {len(items)} prodotti:")
    for t, n in sorted(by_type.items()):
        print(f"  {t}: {n}")
    if preorder_n:
        print(f"  Di cui in preorder: {preorder_n}")
    if mpn_n:
        print(f"  Con MPN: {mpn_n}")
    if skipped:
        print(f"\nSALTATI ({len(skipped)}):")
        for s in skipped[:20]:
            print("  -", s)


if __name__ == "__main__":
    main()
