#!/usr/bin/env python3
"""Genera schede cobot Fairino e catalogo-cobot.html."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "prodotti"))

from _cobot_catalog_data import (  # noqa: E402
    CATALOG,
    CHIPS_BY_SLUG,
    IMG,
    image_for,
    price_display,
    sell_price_eur,
)
from _cobot_specs_data import ACCORDION_BY_SLUG, included_cards  # noqa: E402
from site_nav import render_site_nav  # noqa: E402

try:
    from _site import SITE  # noqa: E402
except ImportError:
    SITE = "https://abrarobotics.com"

TEMPLATE = (ROOT / "prodotti" / "_template-cobot.html").read_text(encoding="utf-8")
OUT_DIR = ROOT / "prodotti"
MANIFEST_PATH = ROOT / "data" / "cobot-products.json"
BRAND = "Fairino"
GOOGLE_CATEGORY = "Business & Industrial > Industrial Machinery > Robotic Arms"

WA_BAR_HTML = """  <div class="wa-bar" id="wa-bar">
    <p><svg width="20" height="20" viewBox="0 0 24 24" fill="#fff" style="flex-shrink:0"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg> Vuoi ricevere più informazioni?</p>
    <a href="https://wa.me/393408592926" target="_blank" rel="noopener" class="wa-btn">Contattaci su WhatsApp</a>
    <button class="wa-bar-close" id="wa-bar-close" aria-label="Chiudi">&times;</button>
  </div>"""

PROCESS_HTML = """      <div class="process-steps-product">
        <div class="step">
          <span class="step-number">01</span>
          <h3>Assessment</h3>
          <p>Analizziamo ciclo, payload, safety e layout cella. Sopralluogo incluso nel prezzo «da».</p>
        </div>
        <div class="step">
          <span class="step-number">02</span>
          <h3>Progettazione</h3>
          <p>Selezione gripper, percorso robot, integrazione I/O e programmazione base applicazione.</p>
        </div>
        <div class="step">
          <span class="step-number">03</span>
          <h3>Go-live</h3>
          <p>Installazione e commissioning — tipicamente 2–3 settimane per cobot standalone.</p>
        </div>
      </div>"""


def filename_for(slug: str) -> str:
    return f"cobot-{slug}.html"


def sku_for(slug: str) -> str:
    return f"cobot-{slug}"


def trim_desc(text: str, max_len: int = 160) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rsplit(" ", 1)[0] + "…"


def keyspecs_html(specs: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'            <div class="key-spec"><span class="key-spec-value">{v}</span>'
        f'<span class="key-spec-label">{k}</span></div>'
        for k, v in specs[:4]
    )


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


def included_html(slug: str, title: str) -> str:
    return "\n".join(
        f'        <div class="included-card">\n'
        f'          <span class="included-card-label">{lbl}</span>\n'
        f'          <span class="included-card-name">{name}</span>\n'
        f"        </div>"
        for lbl, name in included_cards(slug, title)
    )


def specs_accordion_html(slug: str) -> str:
    parts = []
    for i, (title, rows) in enumerate(ACCORDION_BY_SLUG.get(slug, [])):
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


def media_main(slug: str, title: str, group: str) -> str:
    img_rel = f"../{image_for(slug)}"
    style = (
        "max-width:100%;max-height:480px;width:100%;object-fit:contain;padding:24px;"
        "filter:drop-shadow(0 8px 24px rgba(0,0,0,.35));"
    )
    if group == "palletizing":
        vid = "../videos/fairino-palletizing.mp4"
        return (
            f'<video src="{vid}" poster="{img_rel}" autoplay loop muted playsinline '
            f'style="{style}"></video>'
        )
    return f'<img id="gallery-main-img" src="{img_rel}" alt="{title}" style="{style}">'


def buy_area(alibaba_usd: float) -> str:
    vis = price_display(alibaba_usd)
    return f"""          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price">
                <span class="buy-box-amount">{vis}</span>
                <span class="buy-box-sub">IVA esclusa · prezzo indicativo</span>
              </div>
            </div>
            <ul class="buy-box-perks">
              <li><span class="bp-ico">✓</span> Assessment applicativo incluso</li>
              <li><span class="bp-ico">✓</span> Configurazione base e supporto Abra</li>
              <li><span class="bp-ico">✓</span> Consegna stimata 3–5 settimane</li>
            </ul>
            <div class="buy-box-cta"><a href="#form" class="btn btn-primary">Richiedi preventivo</a></div>
            <p class="buy-box-note">Prezzo indicativo — gripper e safety su preventivo dedicato.</p>
          </div>"""


def product_schema(name: str, desc: str, img: str, price: float, filename: str, sku: str) -> str:
    img_url = f"{SITE}/{img}"
    nm, ds = name.replace('"', '\\"'), desc.replace('"', '\\"')
    canon = f"{SITE}/prodotti/{filename}"
    breadcrumb = f"""  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},
    {{"@type": "ListItem", "position": 2, "name": "Catalogo Cobot", "item": "{SITE}/catalogo-cobot.html"}},
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
  "brand": {{"@type": "Brand", "name": "Fairino"}},
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
    return product + "\n" + breadcrumb


def generate_one(row: tuple) -> dict:
    slug, group, tag, title, subtitle, blurb, specs, rows, use_case, alibaba_usd = row
    filename = filename_for(slug)
    sku = sku_for(slug)
    price = float(sell_price_eur(alibaba_usd))
    og_image = image_for(slug)
    meta = trim_desc(f"{title}: {subtitle}. {price_display(alibaba_usd)} IVA esclusa. Cobot Fairino in Italia con Abra Robotics.")
    lang_title = f"{title} — Cobot Fairino | Abra Robotics"

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
        "%%USE_CASE%%": use_case,
        "%%OG_IMAGE%%": og_image,
        "%%PRICE_AMOUNT%%": f"{price:.2f}",
        "%%KEYSPECS%%": keyspecs_html(specs),
        "%%STATS%%": stats_html(specs),
        "%%INCLUDED%%": included_html(slug, title),
        "%%SPECS_ACCORDION%%": specs_accordion_html(slug),
        "%%SPEC_MINI%%": spec_mini_html(specs, rows),
        "%%PROCESS%%": PROCESS_HTML,
        "%%WA_BAR%%": WA_BAR_HTML,
        "%%MEDIA_MAIN%%": media_main(slug, title, group),
        "%%BUY_AREA%%": buy_area(alibaba_usd),
        "%%PRODUCT_SCHEMA%%": product_schema(title, meta, og_image, price, filename, sku),
        "%%SITE_NAV%%": render_site_nav("../"),
    }
    for k, v in repl.items():
        html = html.replace(k, v)

    (OUT_DIR / filename).write_text(html, encoding="utf-8")
    return {
        "slug": slug,
        "group": group,
        "sku": sku,
        "filename": filename,
        "title": title,
        "subtitle": subtitle,
        "tag": tag,
        "blurb": blurb,
        "alibaba_usd": alibaba_usd,
        "price_eur": price,
        "price_display": price_display(alibaba_usd),
        "url": f"{SITE}/prodotti/{filename}",
        "image": f"{SITE}/{og_image}",
    }


def catalog_card(item: dict) -> str:
    img = image_for(item["slug"])
    family = "Soluzione palletizzazione" if item.get("group") == "palletizing" else "Fairino · Cobot 6 assi"
    return f"""        <article class="cat-card">
          <div class="cat-media amr-media"><img src="{img}" alt="{item['title']}" loading="lazy"></div>
          <div class="cat-body">
            <p class="cat-family">{family}</p>
            <h3>{item['title']}</h3>
            <p class="cat-sub">{item['subtitle']}</p>
            <p class="cat-blurb">{item['blurb'][:120]}…</p>
            <p class="cat-price">{item['price_display']}</p>
            <a href="prodotti/{item['filename']}" class="btn btn-primary btn-sm">Vedi scheda →</a>
          </div>
        </article>"""


def lp_model_card(row: tuple, item: dict) -> str:
    slug, _group, tag, title, *_ = row
    chips = CHIPS_BY_SLUG.get(slug, ())
    chips_html = "".join(f"<span>{c}</span>" for c in chips)
    img = image_for(slug)
    return f"""
        <a class="model-card" href="prodotti/{item['filename']}">
          <div class="model-media"><img src="{img}" alt="{title}"></div>
          <div class="model-body">
            <h3>{title}</h3>
            <span class="model-tag">{tag}</span>
            <div class="model-chips">{chips_html}</div>
            <span class="model-price">{item['price_display']} <small>IVA escl.</small></span>
            <span class="model-link">Scheda prodotto →</span>
          </div>
        </a>"""


def _patch_lp_block(text: str, start: str, end: str, cards: str) -> str:
    if start not in text or end not in text:
        return text
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{cards}\n{end}{after}"


def patch_lp_cobot(manifest: list[dict]) -> None:
    lp_path = ROOT / "lp-cobot.html"
    if not lp_path.exists():
        return
    text = lp_path.read_text(encoding="utf-8")
    by_slug = {m["slug"]: m for m in manifest}
    robot_cards = "\n".join(
        lp_model_card(row, by_slug[row[0]])
        for row in CATALOG
        if row[1] == "robot" and row[0] in by_slug
    )
    pallet_cards = "\n".join(
        lp_model_card(row, by_slug[row[0]])
        for row in CATALOG
        if row[1] == "palletizing" and row[0] in by_slug
    )
    text = _patch_lp_block(text, "<!-- COBOT_MODELS_START -->", "<!-- COBOT_MODELS_END -->", robot_cards)
    text = _patch_lp_block(text, "<!-- COBOT_PALLET_START -->", "<!-- COBOT_PALLET_END -->", pallet_cards)
    lp_path.write_text(text, encoding="utf-8")


def write_catalog(manifest: list[dict]) -> None:
    robots = "\n".join(catalog_card(m) for m in manifest if m.get("group") == "robot")
    pallets = "\n".join(catalog_card(m) for m in manifest if m.get("group") == "palletizing")
    n = len(manifest)
    page = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catalogo Cobot Fairino | Abra Robotics</title>
  <meta name="description" content="Catalogo cobot Fairino FR3–FR30 e soluzioni palletizzazione. Prezzi indicativi IVA esclusa. Integrazione e supporto Abra in Italia.">
  <link rel="canonical" href="https://abrarobotics.com/catalogo-cobot.html">
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <style>
    .cat-hero {{ padding: calc(40px + 72px + 48px) 48px 40px; border-bottom: 1px solid var(--gray-200); }}
    .cat-hero h1 {{ font-size: clamp(2rem,4vw,3rem); margin: 12px 0; }}
    .cat-body-page {{ padding: 48px; }}
    .cat-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
    .cat-card {{ background: rgba(255,255,255,0.75); backdrop-filter: blur(10px); border: 1px solid var(--gray-200); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; }}
    .cat-body {{ padding: 18px; display: flex; flex-direction: column; flex: 1; gap: 6px; }}
    .cat-card h3 {{ font-size: 0.95rem; margin: 0; font-weight: 700; }}
    .cat-sub {{ font-size: 0.78rem; color: var(--gray-500); margin: 0; }}
    .cat-blurb {{ font-size: 0.82rem; color: var(--gray-600); margin: 4px 0; flex: 1; line-height: 1.45; }}
    .cat-price {{ font-size: 1.1rem; font-weight: 900; margin: 4px 0 8px; }}
    .cat-family {{ font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gray-400); margin: 0; }}
    .cat-media.amr-media {{ aspect-ratio: 4/3; background: #0a0a0a; display:flex; align-items:center; justify-content:center; }}
    .cat-media.amr-media img {{ width:100%; height:100%; object-fit:contain; padding:20px; }}
    .amr-note {{ background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 20px 24px; margin-bottom: 40px; font-size: 0.92rem; color: var(--gray-600); }}
  </style>
</head>
<body>
  <div class="top-bar"><p>Catalogo Cobot · IVA esclusa · <a href="lp-cobot.html">Landing cobot</a></p></div>
{render_site_nav("")}
  <header class="cat-hero">
    <p class="label">Manifattura</p>
    <h1>Catalogo Cobot Fairino</h1>
    <p style="color:var(--gray-600);max-width:680px;">{n} configurazioni Fairino — cobot a 6 assi e celle palletizzazione. Prezzi «da» indicativi, IVA esclusa.</p>
  </header>
  <main class="cat-body-page">
    <div class="amr-note">
      <p><strong>Inclusi nel prezzo «da»:</strong> assessment applicativo, analisi di fattibilità e prima configurazione Abra.</p>
      <p style="margin:0;"><strong>Non inclusi</strong> (preventivo dedicato): gripper, visione, safety scanner, spedizione e commissioning avanzato.</p>
    </div>
    <nav class="cat-jump" aria-label="Sezioni catalogo cobot" style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:32px;">
      <a href="#cat-robot" style="font-size:0.85rem;padding:8px 14px;border:1px solid var(--gray-200);border-radius:999px;text-decoration:none;color:var(--black);">Robot cobot</a>
      <a href="#cat-pallet" style="font-size:0.85rem;padding:8px 14px;border:1px solid var(--gray-200);border-radius:999px;text-decoration:none;color:var(--black);">Palletizzazione</a>
      <a href="lp-cobot.html" style="font-size:0.85rem;padding:8px 14px;border:1px solid var(--gray-200);border-radius:999px;text-decoration:none;color:var(--black);">Landing cobot</a>
    </nav>
    <section class="cat-group" id="cat-robot" style="margin-bottom:48px;">
      <h2 style="font-size:1.35rem;margin:0 0 8px;">Robot cobot FR Series</h2>
      <p style="color:var(--gray-600);margin:0 0 16px;max-width:720px;">Da FR3 compatto a FR30 heavy-duty. CE, ISO 10218 e ISO/TS 15066.</p>
      <div class="cat-grid">
{robots}
      </div>
    </section>
    <section class="cat-group" id="cat-pallet">
      <h2 style="font-size:1.35rem;margin:0 0 8px;">Soluzioni palletizzazione</h2>
      <p style="color:var(--gray-600);margin:0 0 16px;max-width:720px;">Workstation modulare o celle chiavi in mano con cobot integrato. Ideali per fine linea senza recinto.</p>
      <div class="cat-grid">
{pallets}
      </div>
    </section>
  </main>
  <footer class="footer" style="margin-top:48px;">
    <div class="container footer-bottom">
      <p class="footer-copy">© 2026 Abra Robotics di Niccolò Mazzoleni. P.IVA 04800170278 — Portogruaro (VE).</p>
    </div>
  </footer>
  <script src="script.js"></script>
{WA_BAR_HTML}
</body>
</html>
"""
    (ROOT / "catalogo-cobot.html").write_text(page, encoding="utf-8")


def main() -> None:
    manifest = [generate_one(row) for row in CATALOG]
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_catalog(manifest)
    patch_lp_cobot(manifest)
    print(f"Wrote {len(manifest)} schede cobot-*.html")
    print("Patched lp-cobot.html")
    print(f"Wrote {MANIFEST_PATH}")
    print("Wrote catalogo-cobot.html")


if __name__ == "__main__":
    main()
