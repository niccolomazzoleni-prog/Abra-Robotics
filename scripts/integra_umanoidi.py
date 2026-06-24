#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integra gamma umanoidi completa: G1-D U1-U10, H2 Plus, pagine famiglia e hub umanoidi.html."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from catalogo_contenuti import MANIFEST, build_manifest_entry, image_for  # noqa: E402
from genera_catalogo_completo import (  # noqa: E402
    TEMPLATE,
    buy_area,
    fmt_eur,
    gallery_path,
    key_specs,
    product_schema,
    spec_rows,
)
from site_nav import render_site_nav  # noqa: E402

END_USER = ROOT / "listini" / "pubblico" / "end-user.json"
MANIFEST_PATH = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
PRODOTTI = ROOT / "prodotti"
NOTE = "IVA esclusa, spedizione e dazio inclusi"
# G1-D: dual-arm su colonna/ruote — asset da Unitree + Meko (NON immagini G1 bipede)
G1D_STD_IMG = "images/manifattura/unitree-g1-d-standard.png"
G1D_FLAG_IMG = "images/manifattura/unitree-g1-d-flagship.png"
H2_PLUS_IMG = "images/prodotti/unitree-h2-plus-hero.png"


def g1d_image(sku: str) -> str:
    return G1D_FLAG_IMG if sku in {"G1D-U6", "G1D-U7", "G1D-U8", "G1D-U9", "G1D-U10"} else G1D_STD_IMG

# Prezzi Reichelt (EUR, fonte reichelt.com, giu 2026) + markup Abra 9–13% per SKU
G1D_REICHELT_MARKUP: dict[str, tuple[float, float]] = {
    "G1D-U1":  (30700.0, 11.0),
    "G1D-U2":  (42900.0, 10.0),
    "G1D-U3":  (45400.0, 12.0),
    "G1D-U4":  (39800.0, 9.0),
    "G1D-U5":  (44550.0, 13.0),
    "G1D-U6":  (42100.0, 10.5),
    "G1D-U7":  (54200.0, 11.5),
    "G1D-U8":  (56700.0, 12.5),
    "G1D-U9":  (51050.0, 9.5),
    "G1D-U10": (55850.0, 13.0),
}

G1D_META = [
    ("G1D-U1", "Standard A", "Fissa", "Dex1-1 gripper 2 dita", "19"),
    ("G1D-U2", "Standard B", "Fissa", "Dex3-1 no tattile", "31"),
    ("G1D-U3", "Standard C", "Fissa", "Dex3-1 con tattile", "31"),
    ("G1D-U4", "Standard D", "Fissa", "BrainCo Revo2 Basic 5 dita", "29"),
    ("G1D-U5", "Standard E", "Fissa", "BrainCo Revo2 Touch tattile", "29"),
    ("G1D-U6", "Flagship A", "Mobile ruote", "Dex1-1 gripper 2 dita", "21"),
    ("G1D-U7", "Flagship B", "Mobile ruote", "Dex3-1 no tattile", "33"),
    ("G1D-U8", "Flagship C", "Mobile ruote", "Dex3-1 con tattile", "33"),
    ("G1D-U9", "Flagship D", "Mobile ruote", "BrainCo Revo2 Basic", "31"),
    ("G1D-U10", "Flagship E", "Mobile ruote", "BrainCo Revo2 Touch", "31"),
]


def g1d_abra_price(sku: str) -> float:
    base, pct = G1D_REICHELT_MARKUP[sku]
    return round(base * (1 + pct / 100), 2)


def build_g1d_catalog() -> list[tuple]:
    out = []
    for sku, tier, base, hands, dof in G1D_META:
        out.append((sku, tier, base, hands, dof, g1d_abra_price(sku), g1d_image(sku)))
    return out


G1D_CATALOG = build_g1d_catalog()

G1D_COMMON_SPECS = [
    ("Bracci", "7×2 DoF"),
    ("Payload braccio", "~3 kg"),
    ("Altezza colonna", "1260–1680 mm"),
    ("Compute", "Jetson Orin NX 100 TOPS"),
    ("Camere", "Binoculare testa + HD polso ×2"),
    ("SDK", "ROS2 · data pipeline AI"),
    ("Fonte", "unitree-robot.com/G1-D"),
]


def slug_g1d(sku: str) -> str:
    return f"unitree-{sku.lower().replace('_', '-')}.html"


def ensure_g1d_manifest() -> None:
    for sku, tier, base, hands, dof, _price, img in G1D_CATALOG:
        mob = "Base mobile diff-drive 1,5 m/s · LiDAR" if "Mobile" in base else "Base fissa (piantana)"
        bat = "~6 h (upper + chassis)" if "Mobile" in base else "~2 h (upper body)"
        MANIFEST[sku] = {
            "titolo": f"Unitree G1-D {tier} ({sku.replace('G1D-', '')})",
            "sottotitolo": f"Dual-arm su colonna · {base} · {hands}.",
            "descrizione": (
                f"Unitree G1-D {tier} ({sku}): piattaforma umanoide dual-arm su colonna per acquisizione dati AI, "
                f"manipolazione bimanuale e deployment industriale. {base}, {hands}, {dof} DoF totali. "
                f"Non è il G1 bipede: locomozione tramite piantana fissa o base a ruote (Flagship)."
            ),
            "specs": [
                ("Variante", f"{tier} · {sku}"),
                ("Base", mob),
                ("Mani", hands),
                ("DoF totali", dof),
                ("Autonomia", bat),
            ] + G1D_COMMON_SPECS,
            "fonte_specs": "unitree-robot.com/G1-D",
        }
        from catalogo_contenuti import IMAGE  # noqa: WPS433

        IMAGE[sku] = img

    MANIFEST["H2-PLUS"] = {
        "titolo": "Unitree H2 Plus",
        "sottotitolo": "Reference NVIDIA Isaac GR00T · ricerca accademica full-size.",
        "descrizione": (
            "Unitree H2 Plus: umanoide ~182 cm con 31 DoF corpo + mani Sharpa Wave (75 DoF totali), "
            "NVIDIA Jetson AGX Thor T5000 e piattaforma Isaac GR00T. Disponibilità prevista fine 2026 — "
            "preordine e configurazione su preventivo Abra."
        ),
        "specs": [
            ("Altezza", "~182 cm"),
            ("Peso", "~70 kg"),
            ("DoF", "75 (31 corpo + 44 mani)"),
            ("Compute", "Jetson AGX Thor T5000"),
            ("Payload braccio", "7 kg rated / 15 kg peak"),
            ("Coppia gamba", "360 N·m"),
            ("Batteria", "0,972 kWh · ~3 h"),
            ("Disponibilità", "Fine 2026 (prev.)"),
            ("Piattaforma", "NVIDIA Isaac GR00T"),
        ],
        "fonte_specs": "unitree.com/H2plus",
    }
    from catalogo_contenuti import IMAGE  # noqa: WPS433

    IMAGE["H2-PLUS"] = H2_PLUS_IMG


def patch_end_user() -> None:
    data = json.loads(END_USER.read_text(encoding="utf-8"))
    for sku, tier, base, hands, dof, price, img in G1D_CATALOG:
        data[sku] = {
            "nome": f"G1-D {tier} ({sku.replace('G1D-', '')}) — {hands}",
            "prezzo_eur": price,
            "note": NOTE,
            "immagine": img,
            "slug": slug_g1d(sku),
            "categoria": "UMANOIDI",
            "prezzo_da": False,
            "prezzo_fonte": "reichelt+markup",
            "disponibilita": "2026-08",
        }
    data["H2-PLUS"] = {
        "nome": "H2 Plus (NVIDIA Isaac GR00T Reference)",
        "prezzo_eur": 0,
        "note": "Preordine · disponibilità fine 2026 · prezzo su preventivo",
        "immagine": H2_PLUS_IMG,
        "slug": "unitree-h2-plus.html",
        "categoria": "UMANOIDI",
        "prezzo_su_richiesta": True,
        "disponibilita": "2026-12",
    }
    END_USER.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_catalogo_manifest() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    eu = json.loads(END_USER.read_text(encoding="utf-8"))
    for sku in list(G1D_CATALOG_SKUS()) + ["H2-PLUS"]:
        row = {
            "sku": sku,
            "nome_prodotto": eu[sku]["nome"],
            "categoria": "UMANOIDI",
            "prezzo_enduser_eur": str(eu[sku].get("prezzo_eur", "")),
            "pubblicabile": "true",
        }
        entry = build_manifest_entry(sku, row)
        entry["slug"] = eu[sku]["slug"]
        entry["categoria"] = "UMANOIDI"
        manifest[sku] = entry
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def G1D_CATALOG_SKUS():
    for item in G1D_CATALOG:
        yield item[0]


def generate_product_page(sku: str) -> None:
    eu = json.loads(END_USER.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if sku not in eu:
        return
    row = {
        "sku": sku,
        "nome_prodotto": eu[sku]["nome"],
        "categoria": "UMANOIDI",
        "prezzo_enduser_eur": str(eu[sku].get("prezzo_eur") or ""),
        "pubblicabile": "true",
    }
    entry = manifest.get(sku) or build_manifest_entry(sku, row)
    filename = eu[sku]["slug"]
    path = PRODOTTI / filename
    if path.name in {
        "unitree-g1.html", "unitree-r1-d.html", "unitree-h2.html", "unitree-h2-air.html",
    } and path.exists():
        return

    title = entry["titolo"]
    price_raw = eu[sku].get("prezzo_eur")
    price = float(price_raw) if price_raw and not eu[sku].get("prezzo_su_richiesta") else None
    if eu[sku].get("prezzo_su_richiesta"):
        price = None
    gallery_src, og_image = gallery_path(entry.get("immagine", ""))
    desc = entry.get("descrizione", "")
    metadesc = f"{title}. {entry.get('sottotitolo', '')}"[:160]

    prezzo_da = eu[sku].get("prezzo_da")
    if sku.startswith("G1D-") and price:
        buy = g1d_buy_area(price)
        schema = g1d_product_schema(title, desc, og_image, price, filename)
    else:
        buy = buy_area(price if price else None, price is not None or prezzo_da, sku)
        schema = product_schema(
            title, desc[:200], og_image, price, filename, "umanoidi.html", "Umanoidi"
        )
    if eu[sku].get("prezzo_su_richiesta"):
        buy = """          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price"><span class="buy-box-amount" style="font-size:1.35rem;">Preordine · fine 2026</span>
              <span class="buy-box-sub">Prezzo su preventivo · IVA esclusa</span></div>
            </div>
            <ul class="buy-box-perks">
              <li><span class="bp-ico">✓</span> Reference NVIDIA Isaac GR00T</li>
              <li><span class="bp-ico">✓</span> Distributore ufficiale Unitree</li>
              <li><span class="bp-ico">✓</span> Lista d'attesa e configurazione con Abra</li>
            </ul>
            <div class="buy-box-cta"><a href="#form" class="btn btn-primary">Registra interesse</a></div>
          </div>"""

    html = TEMPLATE
    repl = {
        "%%LANG_TITLE%%": f"{title} | Abra Robotics",
        "%%METADESC%%": metadesc,
        "%%FILENAME%%": filename,
        "%%COLLECTION_FILE%%": "umanoidi.html",
        "%%COLLECTION_NAME%%": "Umanoidi",
        "%%BADGE%%": "UMANOIDI · G1-D" if sku.startswith("G1D") else "UMANOIDI",
        "%%TITLE%%": title,
        "%%SUBTITLE%%": entry.get("sottotitolo", ""),
        "%%DESC%%": desc,
        "%%SKU%%": sku,
        "%%GALLERY_MAIN%%": gallery_src,
        "%%OG_IMAGE%%": og_image,
        "%%KEYSPECS%%": key_specs(entry),
        "%%SPECS_ROWS%%": spec_rows(entry),
        "%%SPECS_BLOCK%%": (
            f'        <div class="faq-item open">\n'
            f'          <button class="faq-question" type="button"><span>Dettagli prodotto</span><span class="faq-icon">+</span></button>\n'
            f'          <div class="faq-answer"><ul class="spec-table">{spec_rows(entry)}</ul></div>\n'
            f"        </div>"
        ),
        "%%EXTRA_SECTIONS%%": "",
        "%%BUY_AREA%%": buy,
        "%%PRODUCT_SCHEMA%%": schema,
        "%%SITE_NAV%%": render_site_nav("../"),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    path.write_text(html, encoding="utf-8")
    print(f"  scheda {filename}")


def fmt_price_card(eu_entry: dict) -> str:
    if eu_entry.get("prezzo_su_richiesta"):
        return "Preordine 2026"
    p = eu_entry.get("prezzo_eur")
    if not p:
        return "Su preventivo"
    if eu_entry.get("prezzo_da"):
        return f"da {fmt_eur(float(p))} €"
    return f"{fmt_eur(float(p))} €"


def g1d_buy_area(price: float) -> str:
    vis = fmt_eur(price)
    return f"""          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price">
                <span class="buy-box-amount">{vis} €</span>
                <span class="buy-box-sub">Prezzo chiavi in mano · IVA esclusa</span>
              </div>
              <span class="buy-box-stock buy-box-stock--preorder"><span class="dot"></span> Preordine · ago 2026</span>
            </div>
            <ul class="buy-box-perks">
              <li><span class="bp-ico">✓</span> Spedizione e dazio doganale inclusi</li>
              <li><span class="bp-ico">✓</span> Distributore ufficiale Unitree</li>
              <li><span class="bp-ico">✓</span> Listino calcolato su Reichelt + margine Abra</li>
            </ul>
            <div class="buy-box-cta">
              <a href="#form" class="btn btn-primary buy-btn" data-buy-pending="1">Richiedi preordine</a>
              <a href="#form" class="btn btn-secondary">Preventivo configurazione</a>
            </div>
            <div class="buy-box-pay">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Pagamento sicuro · Stripe
              <span class="buy-box-cards"><span>VISA</span><span>MC</span><span>AMEX</span></span>
            </div>
<p class="buy-box-note">Prezzo End-User da listino Reichelt +9–13% · conferma su preventivo.</p>
          </div>"""


def g1d_product_schema(title: str, desc: str, img: str, price: float, filename: str) -> str:
    img_url = img if img.startswith("http") else f"https://abrarobotics.com/{img.lstrip('/')}"
    nm, ds = title.replace('"', '\\"'), desc.replace('"', '\\"')[:200]
    canon = f"https://abrarobotics.com/prodotti/{filename}"
    return f"""  <script type="application/ld+json">
  {{"@context": "https://schema.org/", "@type": "Product", "name": "{nm}",
  "sku": "{filename.replace('.html', '')}",
  "image": ["{img_url}"], "description": "{ds}",
  "itemCondition": "https://schema.org/NewCondition",
  "brand": {{"@type": "Brand", "name": "Unitree"}},
  "offers": {{"@type": "Offer", "priceCurrency": "EUR", "price": "{price:.2f}",
    "priceValidUntil": "2026-12-31",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/PreOrder",
    "url": "{canon}",
    "seller": {{"@type": "Organization", "name": "Abra Robotics", "url": "https://abrarobotics.com"}}}}}}
  </script>
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://abrarobotics.com/"}},
    {{"@type": "ListItem", "position": 2, "name": "Umanoidi", "item": "https://abrarobotics.com/umanoidi.html"}},
    {{"@type": "ListItem", "position": 3, "name": "G1-D", "item": "https://abrarobotics.com/g1-d.html"}},
    {{"@type": "ListItem", "position": 4, "name": "{nm}", "item": "{canon}"}}
  ]}}
  </script>"""


def card_html(
    tag: str,
    title: str,
    subtitle: str,
    img: str,
    specs: list[tuple[str, str]],
    price: str,
    href: str,
    family: str,
    tier: str = "",
) -> str:
    ks = "".join(
        f'<div class="key-spec"><span class="key-spec-label">{k}</span>'
        f'<span class="key-spec-value">{v}</span></div>'
        for k, v in specs[:4]
    )
    rows = "".join(f"<li><span>{k}</span><span>{v}</span></li>" for k, v in specs[4:8])
    tier_attr = f' data-tier="{tier}"' if tier else ""
    return f"""<article class="robot-card" id="{family}" data-family="{family}"{tier_attr}>
<div class="robot-media"><span class="robot-media-tag">{tag}</span>
<img alt="{title}" loading="lazy" onerror="this.parentElement.classList.add('no-img');" src="{img}"/>
</div>
<div class="robot-body">
<div><h3>{title}</h3><p class="robot-subtitle">{subtitle}</p></div>
<div class="key-specs">{ks}</div>
<ul class="spec-rows">{rows}</ul>
<div class="robot-card-cta">
<span class="robot-card-price">{price}</span>
<a class="btn btn-primary btn-sm" href="{href}">Vedi scheda →</a>
</div></div></article>"""


COLLECTION_STYLE = """
    .collection-hero { padding: calc(40px + 72px + 48px) 48px 48px; border-bottom: 1px solid var(--gray-200); }
    .collection-hero h1 { font-size: clamp(2rem,4vw,3rem); margin: 12px 0 16px; letter-spacing: -0.03em; }
    .collection-hero .lead { color: var(--gray-600); max-width: 820px; line-height: 1.65; }
    .hero-meta { display: flex; flex-wrap: wrap; gap: 28px; margin-top: 28px; }
    .hero-meta div { display: flex; flex-direction: column; gap: 2px; }
    .hero-meta strong { font-size: 1.4rem; font-weight: 900; }
    .hero-meta span { font-size: 0.75rem; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.06em; }
    .family-nav { display: flex; flex-wrap: wrap; gap: 10px; margin: 24px 0 8px; }
    .family-nav a { padding: 10px 18px; border-radius: 999px; border: 1px solid var(--gray-200); font-size: 0.82rem; font-weight: 700; text-decoration: none; color: var(--black); }
    .family-nav a:hover { border-color: var(--black); }
    .family-section { scroll-margin-top: 100px; padding-top: 48px; }
    .family-head { margin-bottom: 24px; max-width: 720px; }
    .family-head h2 { font-size: 1.75rem; margin: 8px 0; }
    .family-head p { color: var(--gray-600); line-height: 1.6; margin: 0; }
    .family-link { font-weight: 700; font-size: 0.9rem; }
    .robot-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
    .robot-grid.cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .robot-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; transition: transform .3s ease, box-shadow .3s ease; scroll-margin-top: 96px; }
    .robot-card:hover { transform: translateY(-4px); box-shadow: 0 18px 48px rgba(0,0,0,0.08); }
    .robot-media { position: relative; aspect-ratio: 4/3; background: linear-gradient(135deg, var(--gray-50), var(--gray-100)); border-bottom: 1px solid var(--gray-200); display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .robot-media img { width: 100%; height: 100%; object-fit: contain; padding: 20px; }
    .robot-media-tag { position: absolute; top: 14px; left: 14px; background: rgba(255,255,255,0.9); padding: 6px 12px; border-radius: 999px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--gray-600); z-index: 1; }
    .robot-body { padding: 22px; display: flex; flex-direction: column; gap: 14px; flex: 1; min-width: 0; }
    .robot-body h3 { margin: 0; font-size: 1.15rem; line-height: 1.25; }
    .robot-subtitle { color: var(--gray-500); font-size: 0.88rem; margin: 4px 0 0; line-height: 1.45; }
    .key-specs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .key-spec { background: var(--gray-50); border-radius: 8px; padding: 10px 12px; min-width: 0; }
    .key-spec-label { display: block; font-size: 0.68rem; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.05em; }
    .key-spec-value { font-weight: 800; font-size: 0.92rem; word-break: break-word; }
    .spec-rows { list-style: none; padding: 0; margin: 0; font-size: 0.86rem; }
    .spec-rows li { display: flex; justify-content: space-between; gap: 12px; padding: 8px 0; border-bottom: 1px solid var(--gray-100); }
    .spec-rows li span:first-child { color: var(--gray-500); flex-shrink: 0; }
    .spec-rows li span:last-child { text-align: right; }
    .robot-card-cta { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: auto; flex-wrap: wrap; }
    .robot-card-price { font-size: 1.05rem; font-weight: 900; letter-spacing: -0.02em; }
    .robot-card-cta .btn { flex-shrink: 0; white-space: nowrap; }
    .coll-filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }
    .coll-filters button { padding: 8px 16px; border-radius: 999px; border: 1px solid var(--gray-200); background: var(--white); font-size: 0.82rem; font-weight: 600; cursor: pointer; }
    .coll-filters button.active { background: var(--black); color: var(--white); border-color: var(--black); }
    .hub-grid-section { padding-top: 32px; }
    @media (max-width: 1100px) {
      .robot-grid.cols-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 768px) {
      .robot-grid,
      .robot-grid.cols-3 { grid-template-columns: 1fr !important; gap: 20px; }
      .collection-hero { padding: calc(40px + 72px + 20px) 20px 28px; }
      .collection-hero h1 { font-size: clamp(1.65rem, 7vw, 2.2rem); }
      .collection-hero .lead { font-size: 1rem; max-width: none; }
      .hero-meta { gap: 14px 22px; margin-top: 20px; }
      .hero-meta strong { font-size: 1.15rem; }
      .family-nav { flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch; padding-bottom: 6px; margin-right: -4px; scrollbar-width: none; }
      .family-nav::-webkit-scrollbar { display: none; }
      .family-nav a { flex-shrink: 0; font-size: 0.78rem; padding: 9px 14px; }
      .robot-media { aspect-ratio: 16/10; min-height: 200px; }
      .robot-media img { padding: 16px; }
      .robot-body { padding: 18px; gap: 12px; }
      .robot-body h3 { font-size: 1.2rem; }
      .robot-card-cta { flex-direction: column; align-items: stretch; gap: 10px; }
      .robot-card-cta .btn { width: 100%; justify-content: center; text-align: center; white-space: normal; }
      .robot-card-price { font-size: 1.12rem; }
      .hub-grid-section .container { padding-left: 20px; padding-right: 20px; }
    }
    @media (max-width: 480px) {
      .key-specs { grid-template-columns: 1fr; }
    }
"""


def read_nav_snippet() -> str:
    """Estrae nav da umanoidi.html esistente — usa g1.html dopo copia."""
    src = ROOT / "g1.html"
    if not src.exists():
        src = ROOT / "umanoidi.html"
    text = src.read_text(encoding="utf-8")
    start = text.find('<div class="top-bar">')
    end = text.find('<section class="collection-hero">')
    return text[start:end] if start >= 0 and end > start else ""


def read_footer() -> str:
    src = ROOT / "g1.html" if (ROOT / "g1.html").exists() else ROOT / "umanoidi.html"
    text = src.read_text(encoding="utf-8")
    start = text.find("<!-- Footer -->")
    end = text.find('<script src="script.js">')
    if end < 0:
        end = text.find("</body>")
    return text[start:end].strip() if start >= 0 and end > start else ""


def build_collection_page(
    title: str,
    desc: str,
    canonical: str,
    meta_line: list[tuple[str, str]],
    filter_buttons: str,
    cards: str,
    cta_title: str,
) -> str:
    meta_html = "".join(f"<div><strong>{a}</strong><span>{b}</span></div>" for a, b in meta_line)
    nav = read_nav_snippet()
    footer = read_footer()
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title} | Abra Robotics</title>
<meta name="description" content="{desc}"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="https://abrarobotics.com/{canonical}"/>
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet"/>
<link href="style.css" rel="stylesheet"/>
<style>{COLLECTION_STYLE}</style>
</head>
<body>
{nav}
<section class="collection-hero">
<div class="container">
<p class="label"><a href="umanoidi.html" style="color:inherit;text-decoration:none;">Umanoidi</a></p>
<h1>{title}</h1>
<p class="lead">{desc}</p>
<div class="hero-meta">{meta_html}</div>
</div>
</section>
<section class="section" style="padding-top:24px;">
<div class="container">
{filter_buttons}
<div class="robot-grid">{cards}</div>
</div>
</section>
<section class="section section-cta">
<div class="container"><div class="cta-content">
<h2>{cta_title}</h2>
<p class="cta-subtitle">Raccontaci il caso d'uso: ti aiutiamo a scegliere piattaforma, mani e computing. Risposta entro due ore lavorative.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:8px;">
<a class="btn btn-primary" href="assessment.html">Trova il robot giusto</a>
<a class="btn btn-secondary" href="https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF" rel="noopener noreferrer" target="_blank">Prenota una chiamata</a>
</div></div></div>
</section>
{footer}
<script src="script.js"></script>
<script>
(function(){{
  var bar=document.querySelector('.coll-filters'); if(!bar)return;
  var cards=[].slice.call(document.querySelectorAll('.robot-card[data-tier],.robot-card[data-family]'));
  bar.addEventListener('click',function(e){{
    var b=e.target.closest('button[data-filter]'); if(!b)return;
    bar.querySelectorAll('button').forEach(function(x){{x.classList.toggle('active',x===b);}});
    var f=b.dataset.filter;
    cards.forEach(function(c){{
      var show=f==='all'||c.dataset.tier===f||c.dataset.family===f;
      c.style.display=show?'':'none';
    }});
  }});
}})();
</script>
</body>
</html>"""


def generate_g1d_page() -> None:
    eu = json.loads(END_USER.read_text(encoding="utf-8"))
    cards = []
    for sku, tier, base, hands, dof, _p, img in G1D_CATALOG:
        u = sku.replace("G1D-", "")
        tier_key = "standard" if "Standard" in tier else "flagship"
        cards.append(
            card_html(
                f"{tier} · {base}",
                f"Unitree G1-D {tier} ({u})",
                hands,
                img,
                [
                    ("DoF", dof),
                    ("Base", base.split()[0]),
                    ("Payload", "~3 kg/braccio"),
                    ("Compute", "Orin NX 100T"),
                    ("Variante", sku),
                    ("SDK", "ROS2 · AI pipeline"),
                ],
                fmt_price_card(eu[sku]),
                f"prodotti/{slug_g1d(sku)}",
                "g1d",
                tier_key,
            )
        )
    html = build_collection_page(
        "Unitree G1-D — dual-arm su colonna",
        "Dieci configurazioni G1-D (U1–U10): piattaforma wheeled humanoid Unitree per data collection AI, manipolazione bimanuale e deployment industriale. Standard = base fissa; Flagship = base mobile a ruote con LiDAR.",
        "g1-d.html",
        [("10", "Modelli U1–U10"), ("17–33", "DoF"), ("100 TOPS", "Jetson Orin NX"), ("2026", "Disponibilità IT")],
        '<div aria-label="Filtra G1-D" class="coll-filters"><button class="active" data-filter="all">Tutti</button><button data-filter="standard">Standard (fissa)</button><button data-filter="flagship">Flagship (mobile)</button></div>',
        "\n".join(cards),
        "Quale G1-D per il tuo PoC industriale?",
    )
    (ROOT / "g1-d.html").write_text(html, encoding="utf-8")
    print("  g1-d.html")


def generate_hub_umanoidi() -> None:
    eu = json.loads(END_USER.read_text(encoding="utf-8"))
    families = [
        ("g1", "Unitree G1", "Bipede ricerca · Air, EDU U1–U8, Comp", "prodotti/assets/images/g1-01-nobg.png", "g1.html", "10 modelli · 23–43 DoF"),
        ("g1d", "Unitree G1-D", "Dual-arm su colonna · Standard + Flagship", G1D_STD_IMG, "g1-d.html", "U1–U10 · data AI · industria"),
        ("r1", "Unitree R1", "Bipede entry · AIR e EDU U1–U6", "images/manifattura/unitree-r1.png", "r1.html", "Compatto · ROS2 · lab"),
        ("r1d", "Unitree R1-D", "Dual-arm tavolo/mobile · manipolazione bimanuale", "images/manifattura/unitree-r1-d.png", "r1-d.html", "15–31 DoF · deploy rapido"),
        ("h2", "Unitree H2", "Full-size ~180 cm · Air e EDU", "images/universita/unitree-h2-nobg.png", "h2.html", "31 DoF · 360 N·m gamba"),
        ("h2plus", "Unitree H2 Plus", "NVIDIA Isaac GR00T · Sharpa Wave · fine 2026", H2_PLUS_IMG, "prodotti/unitree-h2-plus.html", "75 DoF · Jetson Thor"),
    ]
    fam_cards = ""
    for fid, name, sub, img, href, chips in families:
        if fid == "g1d":
            price = f"da {fmt_eur(g1d_abra_price('G1D-U1'))} €"
        elif fid == "r1d":
            price = fmt_price_card(eu["R1-D"])
        elif fid == "h2plus":
            price = "Preordine 2026"
        elif fid == "g1":
            price = fmt_price_card(eu["G1-AIR"])
        else:
            price = "Vedi gamma"
        fam_cards += card_html(
            "Famiglia umanoide",
            name,
            sub,
            img,
            [("Gamma", chips.split("·")[0].strip()), ("Tipo", sub.split("·")[0].strip())],
            price or "Vedi gamma",
            href,
            fid,
        )

    fam_cards = fam_cards.replace("Vedi scheda →", "Esplora gamma →")

    nav = read_nav_snippet()
    footer = read_footer()
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Robot Umanoidi Unitree — Tutta la gamma | Abra Robotics</title>
<meta name="description" content="Tutti i robot umanoidi Unitree in Italia: G1 bipede, G1-D dual-arm, R1, R1-D, H2 e H2 Plus. Schede, prezzi End-User e supporto Abra Robotics."/>
<link rel="canonical" href="https://abrarobotics.com/umanoidi.html"/>
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet"/>
<link href="style.css" rel="stylesheet"/>
<style>{COLLECTION_STYLE}
.family-nav a.active {{ background: var(--black); color: var(--white); border-color: var(--black); }}
</style>
</head>
<body>
{nav}
<section class="collection-hero">
<div class="container">
<p class="label">Robot Umanoidi</p>
<h1>Unitree — tutta la gamma umanoide</h1>
<p class="lead">Sei famiglie, un unico hub: bipedi da ricerca (G1, R1, H2), piattaforme dual-arm industriali (G1-D, R1-D) e il reference NVIDIA H2 Plus. Ogni famiglia ha schede tecniche, prezzi indicativi e supporto integrazione in Italia.</p>
<div class="hero-meta">
<div><strong>6</strong><span>Famiglie</span></div>
<div><strong>30+</strong><span>Configurazioni</span></div>
<div><strong>ROS2</strong><span>Nativo</span></div>
<div><strong>Italia</strong><span>Supply chain ufficiale</span></div>
</div>
<nav class="family-nav" aria-label="Famiglie umanoidi">
<a href="#g1">G1 bipede</a>
<a href="#g1d">G1-D dual-arm</a>
<a href="#r1">R1</a>
<a href="#r1d">R1-D</a>
<a href="#h2">H2</a>
<a href="#h2plus">H2 Plus</a>
</nav>
</div>
</section>
<section class="section hub-grid-section">
<div class="container">
<div class="robot-grid cols-3">
{fam_cards}
</div>
</div>
</section>
<section class="section section-cta">
<div class="container"><div class="cta-content">
<h2>Quale umanoide per il tuo progetto?</h2>
<p class="cta-subtitle">Locomozione bipede, dual-arm industriale o full-size da ricerca: ti orientiamo tra G1, G1-D, R1, R1-D, H2 e H2 Plus.</p>
<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:8px;">
<a class="btn btn-primary" href="assessment.html">Trova il robot giusto</a>
<a class="btn btn-secondary" href="listino-unitree.html">Listino End-User</a>
</div></div></div>
</section>
{footer}
<script src="script.js"></script>
</body>
</html>"""
    (ROOT / "umanoidi.html").write_text(html, encoding="utf-8")
    print("  umanoidi.html (hub)")


def generate_r1_h2_pages() -> None:
    eu = json.loads(END_USER.read_text(encoding="utf-8"))
    r1_skus = [
        ("R1-AIR", "Air", "Entry · demo", "images/prodotti/r1-air.png", "unitree-r1-air.html", "23", "8-core CPU"),
        ("R1-U1", "U1 EDU", "Expansion Dock 100T", "images/prodotti/r1-u1.png", "unitree-r1-edu.html", "23", "Orin NX"),
        ("R1-U2", "U2", "Vita 3DoF · braccio 7DoF", "images/prodotti/r1-u2.png", "unitree-r1-u2.html", "29", "Orin NX"),
        ("R1-U3", "U3", "Dex3-1", "images/prodotti/r1-u3.png", "unitree-r1-u3.html", "43", "Orin NX"),
        ("R1-U4", "U4", "Dex3-1 tattile", "images/prodotti/r1-u4.png", "unitree-r1-u4.html", "43", "Orin NX"),
        ("R1-U5", "U5", "Revo2 Basic", "images/prodotti/r1-u5.png", "unitree-r1-u5.html", "24+", "Orin NX"),
        ("R1-U6", "U6", "Revo2 haptic", "images/prodotti/r1-u6.png", "unitree-r1-u6.html", "24+", "Orin NX"),
    ]
    r1_cards = []
    for sku, tag, sub, img, slug, dof, comp in r1_skus:
        r1_cards.append(
            card_html(
                tag, f"Unitree R1 {tag}", sub, img,
                [("DoF", dof), ("Computing", comp), ("Altezza", "~122 cm"), ("SDK", "ROS2")],
                fmt_price_card(eu[sku]), f"prodotti/{slug}", "r1", "edu" if sku != "R1-AIR" else "air",
            )
        )
    (ROOT / "r1.html").write_text(
        build_collection_page(
            "Unitree R1 — umanoide entry",
            "R1 è l'umanoide compatto Unitree per università, lab e POC: più leggero del G1, ROS2 nativo, configurazioni EDU U1–U6 con mani dexterous opzionali.",
            "r1.html", [("7", "Modelli"), ("~122 cm", "Altezza"), ("ROS2", "Nativo"), ("EDU", "U1–U6")],
            '<div class="coll-filters"><button class="active" data-filter="all">Tutti</button><button data-filter="air">Air</button><button data-filter="edu">EDU</button></div>',
            "\n".join(r1_cards), "Quale R1 per il tuo lab?",
        ),
        encoding="utf-8",
    )
    h2_cards = [
        card_html("Air", "Unitree H2 Air", "Full-size entry", "images/prodotti/h2-air.png",
                  [("DoF", "31"), ("Altezza", "~180 cm"), ("Coppia gamba", "360 N·m"), ("SDK", "ROS2")],
                  fmt_price_card(eu["H2-AIR"]), "prodotti/unitree-h2-air.html", "h2", "air"),
        card_html("EDU", "Unitree H2 EDU", "Ricerca avanzata · mani opz.", "images/prodotti/h2-edu.png",
                  [("DoF", "31"), ("Compute", "Jetson espandibile"), ("Payload braccio", "120 N·m"), ("Mani", "Dex3/Dex5/Inspire")],
                  fmt_price_card(eu["H2-EDU"]), "prodotti/unitree-h2.html", "h2", "edu"),
        card_html("Plus · 2026", "Unitree H2 Plus", "NVIDIA Isaac GR00T reference", H2_PLUS_IMG,
                  [("DoF", "75"), ("Compute", "Jetson Thor T5000"), ("Mani", "Sharpa Wave ×2"), ("Disponibilità", "Fine 2026")],
                  "Preordine", "prodotti/unitree-h2-plus.html", "h2plus", "plus"),
    ]
    (ROOT / "h2.html").write_text(
        build_collection_page(
            "Unitree H2 — full-size",
            "H2 Air e EDU: umanoide full-size ~180 cm, top di gamma Unitree. H2 Plus (fine 2026): reference NVIDIA Isaac GR00T con 75 DoF e Jetson Thor.",
            "h2.html", [("3", "Linee"), ("~180 cm", "Altezza"), ("31–75", "DoF"), ("GR00T", "H2 Plus")],
            '<div class="coll-filters"><button class="active" data-filter="all">Tutti</button><button data-filter="air">Air</button><button data-filter="edu">EDU</button><button data-filter="plus">H2 Plus</button></div>',
            "\n".join(h2_cards), "H2 Air, EDU o H2 Plus?",
        ),
        encoding="utf-8",
    )
    print("  r1.html, h2.html")


def main() -> None:
    print("Integrazione umanoidi completa…")
    # Backup G1 collection → g1.html
    uman = ROOT / "umanoidi.html"
    g1_path = ROOT / "g1.html"
    if uman.exists() and not g1_path.exists():
        shutil.copy(uman, g1_path)
        t = g1_path.read_text(encoding="utf-8")
        t = t.replace("Unitree G1 — tutta la gamma", "Unitree G1 — bipede ricerca")
        t = t.replace('href="https://abrarobotics.com/umanoidi.html"', 'href="https://abrarobotics.com/g1.html"')
        t = t.replace('rel="canonical" href="https://abrarobotics.com/umanoidi.html"', 'rel="canonical" href="https://abrarobotics.com/g1.html"')
        t = t.replace('<p class="label">Robot Umanoidi</p>', '<p class="label"><a href="umanoidi.html" style="color:inherit;text-decoration:none;">Umanoidi</a> · G1</p>')
        g1_path.write_text(t, encoding="utf-8")
        print("  g1.html (ex umanoidi G1)")

    ensure_g1d_manifest()
    patch_end_user()
    patch_catalogo_manifest()

    for sku in list(G1D_CATALOG_SKUS()) + ["H2-PLUS"]:
        generate_product_page(sku)

    generate_g1d_page()
    generate_r1_h2_pages()
    generate_hub_umanoidi()
    print("Fatto.")


if __name__ == "__main__":
    main()
