#!/usr/bin/env python3
"""Genera schede prodotto AMR (Google Ads / Merchant) da CATALOG in _gen_amr_section."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "prodotti"))

from _gen_amr_section import CATALOG, IMG, get_assets, p  # noqa: E402
from site_nav import render_site_nav  # noqa: E402

try:
    from _site import SITE  # noqa: E402
except ImportError:
    SITE = "https://abrarobotics.com"

TEMPLATE = (ROOT / "prodotti" / "_template-amr.html").read_text(encoding="utf-8")
OUT_DIR = ROOT / "prodotti"
MANIFEST_PATH = ROOT / "data" / "amr-products.json"

GOOGLE_CATEGORY = "Business & Industrial > Material Handling"


def brand_for(slug: str, title: str) -> str:
    if slug.startswith("mir"):
        return "MiR"
    if slug.startswith("juno"):
        return "AutoXing"
    if slug in ("l300", "l1000"):
        return "YOUIBOT"
    if slug.startswith("mav") or "neura" in title.lower():
        return "Neura Robotics"
    if slug == "xp15":
        return "EP Equipment"
    return "AMR"


def price_eur(net: float) -> float:
    return float(int(round(net * 1.2)))


def price_display(net: float) -> str:
    return p(net)


def filename_for(slug: str) -> str:
    return f"amr-{slug}.html"


def sku_for(slug: str) -> str:
    return f"amr-{slug}"


def trim_desc(text: str, max_len: int = 160) -> str:
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1].rsplit(" ", 1)[0]
    return cut + "…"


def metadesc(title: str, subtitle: str, brand: str, net: float, blurb: str) -> str:
    price = price_display(net)
    base = f"{title}: {subtitle}. {price} IVA esclusa."
    extra = f" Integrazione {brand} in Italia con Abra Robotics."
    text = (base + " " + blurb[:80]).strip()
    if len(text) + len(extra) <= 160:
        text += extra
    return trim_desc(text)


def keyspecs_html(specs: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'            <div class="key-spec"><span class="key-spec-value">{v}</span>'
        f'<span class="key-spec-label">{k}</span></div>'
        for k, v in specs[:4]
    )


def specs_rows_html(specs: list[tuple[str, str]], rows: list[tuple[str, str]]) -> str:
    all_rows = list(specs) + list(rows)
    return "\n".join(f"<li><span>{k}</span><span>{v}</span></li>" for k, v in all_rows)


def media_main(slug: str, title: str) -> str:
    a = get_assets()[slug]
    img_rel = f"../{IMG}/{a['file']}"
    video = a.get("video")
    style = "max-width:100%;max-height:480px;width:100%;object-fit:contain;padding:24px;filter:drop-shadow(0 12px 20px rgba(0,0,0,.12));"
    if video:
        vid_rel = f"../{IMG}/{video}"
        return (
            f'<video src="{vid_rel}" poster="{img_rel}" autoplay loop muted playsinline '
            f'style="{style}"></video>'
        )
    return f'<img id="gallery-main-img" src="{img_rel}" alt="{title}" style="{style}">'


def buy_area(net: float) -> str:
    vis = price_display(net)
    amount = price_eur(net)
    return f"""          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price">
                <span class="buy-box-amount">{vis}</span>
                <span class="buy-box-sub">IVA esclusa · prezzo indicativo</span>
              </div>
            </div>
            <ul class="buy-box-perks">
              <li><span class="bp-ico">✓</span> Assessment e sopralluogo inclusi</li>
              <li><span class="bp-ico">✓</span> Progettazione percorsi e integrazione</li>
              <li><span class="bp-ico">✓</span> Consegna stimata ~4 settimane</li>
            </ul>
            <div class="buy-box-cta"><a href="#form" class="btn btn-primary">Richiedi preventivo</a></div>
            <p class="buy-box-note">Prezzo indicativo — quotazione aggiornata su richiesta.</p>
          </div>"""


def product_schema(
    name: str,
    desc: str,
    img: str,
    price: float,
    filename: str,
    brand: str,
    sku: str,
) -> str:
    img_url = img if img.startswith("http") else f"{SITE}/{img}"
    nm, ds = name.replace('"', '\\"'), desc.replace('"', '\\"')
    br = brand.replace('"', '\\"')
    canon = f"{SITE}/prodotti/{filename}"
    faq = f"""  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {{"@type": "Question", "name": "Il prezzo «da» è definitivo?", "acceptedAnswer": {{"@type": "Answer", "text": "No: è indicativo IVA esclusa. Il preventivo finale dipende da layout, integrazioni e top module."}}}},
    {{"@type": "Question", "name": "Quanto tempo serve per il go-live?", "acceptedAnswer": {{"@type": "Answer", "text": "Per AMR industriali stimiamo circa 4 settimane dal sopralluogo al primo percorso operativo."}}}}
  ]}}
  </script>"""
    breadcrumb = f"""  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},
    {{"@type": "ListItem", "position": 2, "name": "Catalogo AMR", "item": "{SITE}/catalogo-amr.html"}},
    {{"@type": "ListItem", "position": 3, "name": "{nm}", "item": "{canon}"}}
  ]}}
  </script>"""
    product = f"""  <script type="application/ld+json">
  {{"@context": "https://schema.org/", "@type": "Product",
  "name": "{nm}",
  "sku": "{sku}",
  "mpn": "{sku}",
  "image": ["{img_url}"],
  "description": "{ds}",
  "brand": {{"@type": "Brand", "name": "{br}"}},
  "category": "{GOOGLE_CATEGORY}",
  "itemCondition": "https://schema.org/NewCondition",
  "offers": {{
    "@type": "Offer",
    "priceCurrency": "EUR",
    "price": "{price:.2f}",
    "priceValidUntil": "2026-12-31",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock",
    "url": "{canon}",
    "seller": {{"@type": "Organization", "name": "Abra Robotics", "url": "{SITE}"}}
  }}}}
  </script>"""
    return product + "\n" + breadcrumb + "\n" + faq


def generate_one(row: tuple) -> dict:
    slug, _group, tag, title, subtitle, blurb, specs, rows, use_case, net = row
    brand = brand_for(slug, title)
    filename = filename_for(slug)
    sku = sku_for(slug)
    price = price_eur(net)
    og_image = f"{IMG}/{get_assets()[slug]['file']}"
    meta = metadesc(title, subtitle, brand, net, blurb)
    lang_title = f"{title} — Robot AMR {brand} | Abra Robotics"

    html = TEMPLATE
    repl = {
        "%%LANG_TITLE%%": lang_title,
        "%%METADESC%%": meta,
        "%%FILENAME%%": filename,
        "%%TITLE%%": title,
        "%%SUBTITLE%%": subtitle,
        "%%BADGE%%": tag,
        "%%DESC%%": blurb,
        "%%SKU%%": sku,
        "%%BRAND%%": brand,
        "%%USE_CASE%%": use_case,
        "%%OG_IMAGE%%": og_image,
        "%%PRICE_AMOUNT%%": f"{price:.2f}",
        "%%KEYSPECS%%": keyspecs_html(specs),
        "%%SPECS_ROWS%%": specs_rows_html(specs, rows),
        "%%MEDIA_MAIN%%": media_main(slug, title),
        "%%BUY_AREA%%": buy_area(net),
        "%%PRODUCT_SCHEMA%%": product_schema(
            title, meta, og_image, price, filename, brand, sku
        ),
        "%%SITE_NAV%%": render_site_nav("../"),
    }
    for k, v in repl.items():
        html = html.replace(k, v)

    path = OUT_DIR / filename
    path.write_text(html, encoding="utf-8")
    return {
        "slug": slug,
        "sku": sku,
        "filename": filename,
        "title": title,
        "brand": brand,
        "price_eur": price,
        "url": f"{SITE}/prodotti/{filename}",
        "image": f"{SITE}/{og_image}",
    }


def main() -> None:
    manifest = []
    for row in CATALOG:
        manifest.append(generate_one(row))
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(manifest)} schede in prodotti/amr-*.html")
    print(f"Wrote {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
