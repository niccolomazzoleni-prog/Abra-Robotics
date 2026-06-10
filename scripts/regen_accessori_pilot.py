#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigenera solo le 10 schede accessori pilota con sezioni arricchite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "prodotti"))

from catalogo_contenuti import IMAGE, MANIFEST  # noqa: E402
from genera_catalogo_completo import (  # noqa: E402
    COLLECTION,
    CSV_PATH,
    PRODOTTI,
    buy_area,
    gallery_path,
    key_specs,
    manifest_entry,
    parse_price,
    product_schema,
    read_csv,
    slug_file,
    spec_rows,
)
from site_nav import render_site_nav  # noqa: E402

PILOT_SKUS = (
    "HAND-DEX3-1-NO-TAC",
    "HAND-DEX3-1-TAC",
    "BIONIC-REVO2-BASIC",
    "ARM-Z1-AIR",
    "ARM-Z1-PRO",
    "G1-BATTERY",
    "ORIN-NX-UPGRADE",
    "GO2-SELF-CHARGE",
    "Z1-GRIPPER-D435I",
    "HELIOS-5515",
)

PILOT_DATA = json.loads(
    (ROOT / "data" / "products" / "accessori-pilot.json").read_text(encoding="utf-8")
)
TEMPLATE = (ROOT / "prodotti" / "_template-compact.html").read_text(encoding="utf-8")


def stats_section(entry: dict) -> str:
    specs = entry.get("specs") or []
    if len(specs) < 2:
        return ""
    parts = []
    for label, val in specs[:3]:
        num = "".join(c for c in val if c.isdigit() or c in ",.")
        unit = val.replace(num, "").strip() if num else ""
        target = (num.replace(",", ".").split("–")[0].split("-")[0] or "0")
        u = f'<span class="stat-unit">{unit}</span>' if unit else ""
        parts.append(
            f'        <div class="product-stat">\n'
            f'          <span class="stat-number"><span class="counter" data-target="{target}">0</span>{u}</span>\n'
            f'          <span class="stat-label">{label}</span>\n'
            f"        </div>"
        )
    return f"""  <section class="section section-dark" style="padding-bottom:0;">
    <div class="container">
      <div class="product-stats" id="stats-section">
{chr(10).join(parts)}
      </div>
    </div>
  </section>"""


def included_section(sku: str) -> str:
    pilot = PILOT_DATA.get(sku, {})
    cards = pilot.get("included", [])
    if not cards:
        return ""
    html = "\n".join(
        f'        <div class="included-card">\n'
        f'          <span class="included-card-label">{lbl}</span>\n'
        f'          <span class="included-card-name">{name}</span>\n'
        f"        </div>"
        for lbl, name in cards
    )
    return f"""  <section class="section">
    <div class="container">
      <div class="included-strip light-strip">
{html}
      </div>
    </div>
  </section>"""


def accordion_html(sku: str) -> str:
    pilot = PILOT_DATA.get(sku, {})
    cats = pilot.get("accordion", [])
    if not cats:
        return ""
    parts = []
    for i, (title, rows) in enumerate(cats):
        open_attr = " open" if i == 0 else ""
        trs = "\n".join(f"              <tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows)
        parts.append(
            f'        <details class="faq-item"{open_attr}>\n'
            f"          <summary>{title}</summary>\n"
            f'          <table class="specs-table">\n{trs}\n'
            f"          </table>\n"
            f"        </details>"
        )
    return "\n".join(parts)


def spec_mini_section(entry: dict) -> str:
    specs = entry.get("specs") or []
    if not specs:
        return ""
    cards = "\n".join(
        f'        <div class="spec-mini-card">\n'
        f'          <span class="spec-mini-value">{v}</span>\n'
        f'          <span class="spec-mini-label">{k}</span>\n'
        f"        </div>"
        for k, v in specs[:6]
    )
    return f"""  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="section-header" style="margin-bottom:24px;">
        <p class="label">Dati tecnici</p>
        <h2>In sintesi</h2>
      </div>
      <div class="spec-mini-grid">
{cards}
      </div>
    </div>
  </section>"""


PROCESS_SECTION = """  <section class="section section-dark">
    <div class="container">
      <div class="section-header">
        <p class="label label-light">Acquisto</p>
        <h2>Come funziona con Abra</h2>
      </div>
      <div class="process-steps-product">
        <div class="step">
          <span class="step-number">01</span>
          <h3>Preventivo</h3>
          <p>Richiedi quotazione aggiornata al cambio EUR/USD. Conferma compatibilità con la tua piattaforma.</p>
        </div>
        <div class="step">
          <span class="step-number">02</span>
          <h3>Ordine</h3>
          <p>Spedizione e dazio doganale inclusi. Distributore ufficiale Unitree in Italia.</p>
        </div>
        <div class="step">
          <span class="step-number">03</span>
          <h3>Consegna</h3>
          <p>Consegna stimata 2–4 settimane. Supporto tecnico dedicato.</p>
        </div>
      </div>
    </div>
  </section>"""


def extra_sections(sku: str, entry: dict) -> str:
    return "\n".join(
        s for s in (
            stats_section(entry),
            included_section(sku),
            spec_mini_section(entry),
            PROCESS_SECTION,
        ) if s
    )


def generate_pilot(row: dict, manifest: dict) -> str:
    sku = row["sku"]
    filename = slug_file(sku)
    entry = manifest_entry(sku, manifest, row)
    if sku in MANIFEST:
        entry = {**entry, **{k: MANIFEST[sku][k] for k in ("titolo", "sottotitolo", "descrizione", "specs", "fonte_specs") if k in MANIFEST[sku]}}
    if sku in IMAGE:
        entry["immagine"] = IMAGE[sku]

    cat = row["categoria"]
    coll_file, coll_name = COLLECTION.get(cat, ("catalogo-unitree.html", "Catalogo"))
    title = entry["titolo"]
    price = parse_price(row.get("prezzo_enduser_eur", ""))
    pub = row.get("pubblicabile") == "true"
    gallery_src, og_image = gallery_path(entry.get("immagine", ""))
    desc = entry.get("descrizione", "")
    metadesc = f"{title}. {entry.get('sottotitolo', '')}"[:160]

    acc = accordion_html(sku)
    specs_block = acc if acc else (
        f'        <div class="faq-item open">\n'
        f'          <button class="faq-question" type="button"><span>Dettagli prodotto</span><span class="faq-icon">+</span></button>\n'
        f'          <div class="faq-answer"><ul class="spec-table">{spec_rows(entry)}</ul></div>\n'
        f"        </div>"
    )

    html = TEMPLATE
    repl = {
        "%%LANG_TITLE%%": f"{title} | Abra Robotics",
        "%%METADESC%%": metadesc,
        "%%FILENAME%%": filename,
        "%%COLLECTION_FILE%%": coll_file,
        "%%COLLECTION_NAME%%": coll_name,
        "%%BADGE%%": cat.replace("_", " · "),
        "%%TITLE%%": title,
        "%%SUBTITLE%%": entry.get("sottotitolo", ""),
        "%%DESC%%": desc,
        "%%SKU%%": sku,
        "%%GALLERY_MAIN%%": gallery_src,
        "%%OG_IMAGE%%": og_image,
        "%%KEYSPECS%%": key_specs(entry),
        "%%SPECS_ROWS%%": spec_rows(entry),
        "%%SPECS_BLOCK%%": specs_block,
        "%%EXTRA_SECTIONS%%": extra_sections(sku, entry),
        "%%BUY_AREA%%": buy_area(price if pub else None, pub and price is not None, sku),
        "%%PRODUCT_SCHEMA%%": product_schema(
            title, desc[:200], og_image, price if pub else None, filename, coll_file, coll_name
        ),
        "%%SITE_NAV%%": render_site_nav("../"),
    }
    for k, v in repl.items():
        html = html.replace(k, v)

    path = PRODOTTI / filename
    path.write_text(html, encoding="utf-8")
    return filename


def main() -> None:
    rows = {r["sku"]: r for r in read_csv()}
    manifest = {}
    try:
        from genera_catalogo_completo import load_manifest
        manifest = load_manifest()
    except Exception:
        pass

    written = []
    for sku in PILOT_SKUS:
        if sku not in rows:
            print(f"SKIP {sku}: not in CSV")
            continue
        fn = generate_pilot(rows[sku], manifest)
        written.append(fn)
        print(f"OK {fn}")

    print(f"\nRigenerate {len(written)} schede pilota accessori.")


if __name__ == "__main__":
    main()
