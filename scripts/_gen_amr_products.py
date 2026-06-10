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
from _amr_specs_data import ACCORDION_BY_SLUG, included_cards  # noqa: E402
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


def stats_html(specs: list[tuple[str, str]]) -> str:
    out = []
    for label, val in specs[:3]:
        num = "".join(c for c in val if c.isdigit() or c in ",.")
        unit = val.replace(num, "").strip() if num else ""
        target = num.replace(",", ".") if num else "0"
        u = f'<span class="stat-unit">{unit}</span>' if unit else ""
        out.append(
            f'        <div class="product-stat">\n'
            f'          <span class="stat-number"><span class="counter" data-target="{target.split("–")[0].split("-")[0]}">0</span>{u}</span>\n'
            f'          <span class="stat-label">{label}</span>\n'
            f"        </div>"
        )
    return "\n".join(out)


def included_html(slug: str, title: str, brand: str) -> str:
    return "\n".join(
        f'        <div class="included-card">\n'
        f'          <span class="included-card-label">{lbl}</span>\n'
        f'          <span class="included-card-name">{name}</span>\n'
        f"        </div>"
        for lbl, name in included_cards(slug, title, brand)
    )


def specs_accordion_html(slug: str) -> str:
    cats = ACCORDION_BY_SLUG.get(slug, [])
    parts = []
    for i, (title, rows) in enumerate(cats):
        open_attr = " open" if i == 0 else ""
        trs = "\n".join(f"              <tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows)
        parts.append(
            f'          <details class="faq-item"{open_attr}>\n'
            f"            <summary>{title}</summary>\n"
            f'            <table class="specs-table">\n{trs}\n'
            f"            </table>\n"
            f"          </details>"
        )
    return "\n".join(parts)


def spec_mini_html(specs: list[tuple[str, str]], rows: list[tuple[str, str]]) -> str:
    all_rows = list(specs) + list(rows)
    return "\n".join(
        f'        <div class="spec-mini-card">\n'
        f'          <span class="spec-mini-value">{v}</span>\n'
        f'          <span class="spec-mini-label">{k}</span>\n'
        f"        </div>"
        for k, v in all_rows[:9]
    )


PROCESS_HTML = """      <div class="process-steps-product">
        <div class="step">
          <span class="step-number">01</span>
          <h3>Assessment</h3>
          <p>Analizziamo layout, percorsi e sistemi IT. Sopralluogo incluso nel prezzo «da».</p>
        </div>
        <div class="step">
          <span class="step-number">02</span>
          <h3>Progettazione</h3>
          <p>Mappatura, integrazione WMS/MES su progetto, configurazione flotta e top module.</p>
        </div>
        <div class="step">
          <span class="step-number">03</span>
          <h3>Go-live</h3>
          <p>Commissioning e messa in servizio del primo percorso — tipicamente ~4 settimane.</p>
        </div>
      </div>"""

WA_BAR_HTML = """  <div class="wa-bar" id="wa-bar">
    <p><svg width="20" height="20" viewBox="0 0 24 24" fill="#fff" style="flex-shrink:0"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg> Vuoi ricevere più informazioni?</p>
    <a href="https://wa.me/393408592926" target="_blank" rel="noopener" class="wa-btn">Contattaci su WhatsApp</a>
    <button class="wa-bar-close" id="wa-bar-close" aria-label="Chiudi">&times;</button>
  </div>"""


def media_main(slug: str, title: str) -> str:
    a = get_assets()[slug]
    img_rel = f"../{IMG}/{a['file']}"
    video = a.get("video")
    style = (
        "max-width:100%;max-height:480px;width:100%;object-fit:contain;padding:24px;"
        "filter:drop-shadow(0 12px 20px rgba(0,0,0,.12));mix-blend-mode:multiply;"
    )
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
        "%%STATS%%": stats_html(specs),
        "%%INCLUDED%%": included_html(slug, title, brand),
        "%%SPECS_ACCORDION%%": specs_accordion_html(slug),
        "%%SPEC_MINI%%": spec_mini_html(specs, rows),
        "%%PROCESS%%": PROCESS_HTML,
        "%%WA_BAR%%": WA_BAR_HTML,
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
