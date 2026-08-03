#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix product pages: prices, G1-D duplicates, thin hand specs, SEO stubs."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EU_PATH = ROOT / "listini" / "pubblico" / "end-user.json"
PROD = ROOT / "prodotti"
SITE = "https://abrarobotics.com"


def fmt_eur(value: float) -> str:
    s = f"{value:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def sync_prices(eu: dict) -> int:
    """Align Offer.price + buy-box-amount with end-user.json."""
    fixed = 0
    for sku, entry in eu.items():
        slug = entry.get("slug")
        price = entry.get("prezzo_eur")
        if not slug or price is None:
            continue
        path = PROD / slug
        if not path.exists():
            print(f"  ! missing page for {sku}: {slug}")
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        price_f = float(price)
        price_str = f"{price_f:.2f}"
        amount = f"{fmt_eur(price_f)} €"
        if entry.get("prezzo_da"):
            amount = f"da €{fmt_eur(price_f).split(',')[0]}"  # keep short "da €39.170" style if used
            # Prefer consistent Italian with decimals when buy-box uses full form
            if "buy-box-amount" in text and "da €" not in text and "A partire" not in text:
                amount = f"A partire da {fmt_eur(price_f)} €"
            elif 'buy-box-amount" style' in text or "da €" in text:
                # Aggregate / "da €" style pages — sync integer thousands
                amount = f"da €{fmt_eur(price_f).split(',')[0]}"

        # Simple Offer price (not AggregateOffer lowPrice)
        if '"@type": "Offer"' in text or '"@type":"Offer"' in text:
            text2, n = re.subn(
                r'("price"\s*:\s*")[^"]*(")',
                rf"\g<1>{price_str}\g<2>",
                text,
                count=1,
            )
            if n:
                text = text2

        # AggregateOffer lowPrice
        if "AggregateOffer" in text:
            text = re.sub(
                r'("lowPrice"\s*:\s*")[^"]*(")',
                rf"\g<1>{price_f:.0f}\g<2>",
                text,
                count=1,
            )

        # buy-box amount inside LISTINO block or first occurrence
        if f"<!-- LISTINO:sku:{sku} -->" in text:
            start = f"<!-- LISTINO:sku:{sku} -->"
            end = f"<!-- /LISTINO:sku:{sku} -->"
            m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, re.S)
            if m:
                block = m.group(1)
                if entry.get("prezzo_da"):
                    box_amount = f"A partire da {fmt_eur(price_f)} €"
                    if "da €" in block and "A partire" not in block:
                        box_amount = f"da €{fmt_eur(price_f).split(',')[0]}"
                else:
                    box_amount = f"{fmt_eur(price_f)} €"
                block2 = re.sub(
                    r'(<span class="buy-box-amount"[^>]*>)[^<]*(</span>)',
                    rf"\g<1>{box_amount}\g<2>",
                    block,
                    count=1,
                )
                text = text[: m.start(1)] + block2 + text[m.end(1) :]
        elif "buy-box-amount" in text and not entry.get("prezzo_da"):
            text = re.sub(
                r'(<span class="buy-box-amount"[^>]*>)[^<]*(</span>)',
                rf"\g<1>{fmt_eur(price_f)} €\g<2>",
                text,
                count=1,
            )

        if text != original:
            path.write_text(text, encoding="utf-8")
            fixed += 1
            print(f"  price OK {sku} -> {slug} ({price_str})")
    return fixed


REDIRECT_HTML = """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Redirect — {title} | Abra Robotics</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{canonical}">
  <meta http-equiv="refresh" content="0; url={canonical}">
  <script>location.replace({canonical_js});</script>
</head>
<body>
  <p>Questa pagina è stata unificata. Vai a <a href="{href}">{title}</a>.</p>
</body>
</html>
"""


def consolidate_g1d() -> None:
    """Keep richer unitree-g1-d-* pages; turn unitree-g1d-* into redirects."""
    mapping = {
        "unitree-g1d-standard.html": (
            "unitree-g1-d-standard.html",
            "Unitree G1-D Standard",
        ),
        "unitree-g1d-flagship.html": (
            "unitree-g1-d-flagship.html",
            "Unitree G1-D Flagship",
        ),
    }
    for old, (keep, title) in mapping.items():
        keep_path = PROD / keep
        old_path = PROD / old
        if not keep_path.exists():
            print(f"  ! keep missing {keep}")
            continue
        canonical = f"{SITE}/prodotti/{keep}"
        html = REDIRECT_HTML.format(
            title=title,
            canonical=canonical,
            canonical_js=json.dumps(canonical),
            href=keep,
        )
        old_path.write_text(html, encoding="utf-8")
        print(f"  redirect {old} -> {keep}")

    # catalog links
    cat = ROOT / "catalogo-unitree.html"
    t = cat.read_text(encoding="utf-8")
    t2 = t.replace("prodotti/unitree-g1d-standard.html", "prodotti/unitree-g1-d-standard.html")
    t2 = t2.replace("prodotti/unitree-g1d-flagship.html", "prodotti/unitree-g1-d-flagship.html")
    if t2 != t:
        cat.write_text(t2, encoding="utf-8")
        print("  catalogo-unitree.html links updated")

    # other references
    for path in ROOT.rglob("*.html"):
        if path.name.startswith("_") or "node_modules" in path.parts:
            continue
        if path.name in mapping:
            continue
        rel = str(path.relative_to(ROOT))
        if any(x in path.parts for x in ("admin", "offerte-ai", "listini")):
            continue
        t = path.read_text(encoding="utf-8", errors="replace")
        t2 = t
        for old, (keep, _) in mapping.items():
            t2 = t2.replace(f"prodotti/{old}", f"prodotti/{keep}")
            t2 = t2.replace(f'href="{old}"', f'href="{keep}"')
            t2 = t2.replace(f"/{old}", f"/{keep}")
        if t2 != t:
            path.write_text(t2, encoding="utf-8")
            print(f"  href fix {rel}")


HAND_SPECS: dict[str, dict] = {
    "unitree-h2-hand-revo3-u21.html": {
        "sku": "H2-HAND-REVO3-U21",
        "subtitle": "Mano BrainCo REVO 3 a 21 DoF attivi — senza tattile, con camera RGB.",
        "desc": (
            "BrainCo REVO 3 U21 per Unitree H2: 21 gradi di libertà pienamente attivi, "
            "architettura direct-drive backdrivable, camera RGB integrata e controllo a 500 Hz "
            "(posizione, MIT force-position, ammettenza, zero-torque). Ideale per ricerca e "
            "manipolazione fine senza array tattile."
        ),
        "keys": [
            ("21", "DoF attivi"),
            ("No tattile", "Sensori"),
            ("RGB", "Visione"),
            ("500 Hz", "Controllo"),
            ("H2", "Compatibilità"),
        ],
        "specs": [
            ("Modello", "BrainCo REVO 3 U21"),
            ("DoF attivi", "21 (pollice 5 + 4 dita × 4)"),
            ("Tattile", "No"),
            ("Visione", "Camera RGB"),
            ("Altezza mano", "216 mm"),
            ("Larghezza palmo", "108 mm"),
            ("Diametro presa", "10–150 mm"),
            ("Forza presa attiva", "> 50 N"),
            ("Pinza polpastrello", "> 20 N"),
            ("Payload mano", "20 kg"),
            ("Payload 4 dita", "5 kg"),
            ("Tensione", "24–80 V"),
            ("Corrente max", "10 A @ 24 V"),
            ("Comunicazione", "RS485 (CAN FD / EtherCAT in sviluppo)"),
            ("Frequenza controllo", "500 Hz"),
            ("Ripetibilità", "0,1°"),
            ("Velocità", "3 Hz"),
            ("Compatibilità", "Unitree H2"),
        ],
    },
    "unitree-h2-hand-revo3-u21t.html": {
        "sku": "H2-HAND-REVO3-U21T",
        "subtitle": "REVO 3 U21T — 21 DoF con tattile a palmo completo e RGB.",
        "desc": (
            "BrainCo REVO 3 U21T per H2: stessa meccanica a 21 DoF della U21 con array tattile "
            "distribuito su tutta la mano (risoluzione 0,01 N, range 0–25 N) e camera RGB. "
            "Pensata per grasping adattivo, oggetti fragili e ricerca di manipolazione con feedback di forza."
        ),
        "keys": [
            ("21", "DoF attivi"),
            ("Tattile", "Palmo intero"),
            ("0,01 N", "Risoluzione"),
            ("RGB", "Visione"),
            ("H2", "Compatibilità"),
        ],
        "specs": [
            ("Modello", "BrainCo REVO 3 U21T"),
            ("DoF attivi", "21 (pollice 5 + 4 dita × 4)"),
            ("Tattile", "Array su tutta la mano"),
            ("Risoluzione tattile", "0,01 N"),
            ("Range tattile", "0–25 N"),
            ("Visione", "Camera RGB"),
            ("Altezza mano", "216 mm"),
            ("Larghezza palmo", "108 mm"),
            ("Diametro presa", "10–150 mm"),
            ("Forza presa attiva", "> 50 N"),
            ("Pinza polpastrello", "> 20 N"),
            ("Payload mano", "20 kg"),
            ("Tensione", "24–80 V"),
            ("Comunicazione", "RS485 (CAN FD / EtherCAT in sviluppo)"),
            ("Frequenza controllo", "500 Hz"),
            ("Compatibilità", "Unitree H2"),
        ],
    },
    "unitree-h2-hand-revo3-u21v.html": {
        "sku": "H2-HAND-REVO3-U21V",
        "subtitle": "REVO 3 U21V — tattile + visuotattile in punta dita, con RGB.",
        "desc": (
            "BrainCo REVO 3 U21V (Visual-Tactile) per H2: 21 DoF, tattile a palmo completo e "
            "sensori visuotattili in punta dita (deformazione rilevabile ~130 μm), più camera RGB. "
            "Configurazione top per ricerca embodied AI e manipolazione di precisione."
        ),
        "keys": [
            ("21", "DoF attivi"),
            ("Visuotattile", "Punte dita"),
            ("130 μm", "Deformazione min."),
            ("RGB", "Visione"),
            ("H2", "Compatibilità"),
        ],
        "specs": [
            ("Modello", "BrainCo REVO 3 U21V / U21VT"),
            ("DoF attivi", "21 (pollice 5 + 4 dita × 4)"),
            ("Tattile", "Palmo + visuotattile in punta"),
            ("Risoluzione tattile", "0,01 N"),
            ("Range tattile", "0–25 N"),
            ("Deformazione min. rilevabile", "130 μm"),
            ("Visione", "Camera RGB"),
            ("Altezza mano", "216 mm"),
            ("Larghezza palmo", "108 mm"),
            ("Diametro presa", "10–150 mm"),
            ("Forza presa attiva", "> 50 N"),
            ("Payload mano", "20 kg"),
            ("Tensione", "24–80 V"),
            ("Comunicazione", "RS485 (CAN FD / EtherCAT in sviluppo)"),
            ("Frequenza controllo", "500 Hz"),
            ("Compatibilità", "Unitree H2"),
        ],
    },
    "unitree-h2-hand-inspire-e2.html": {
        "sku": "H2-HAND-INSPIRE-E2",
        "subtitle": "Mano Inspire E2 a 5 dita con camera RGB per Unitree H2.",
        "desc": (
            "Inspire E2 Dexterous Hand per H2: mano antropomorfa a 5 dita con integrazione RGB, "
            "pensata per grasping general-purpose e demo di manipolazione su umanoide Unitree. "
            "Accessorio originale di canale, preventivo e lead time su conferma ordine."
        ),
        "keys": [
            ("5 dita", "Configurazione"),
            ("RGB", "Visione"),
            ("Inspire", "Famiglia"),
            ("H2", "Compatibilità"),
        ],
        "specs": [
            ("Modello", "Inspire E2 Dexterous Hand (With RGB)"),
            ("Configurazione", "Mano a 5 dita"),
            ("Visione", "Camera RGB"),
            ("Famiglia", "Inspire"),
            ("Tipo", "Accessorio dedicato H2"),
            ("Compatibilità", "Unitree H2"),
            ("Uso", "Manipolazione, HRI, ricerca"),
            ("Note", "Specifiche di dettaglio su scheda tecnica Unitree / Inspire a preventivo"),
        ],
    },
}


def enrich_hand_page(filename: str, data: dict) -> None:
    path = PROD / filename
    text = path.read_text(encoding="utf-8")
    original = text

    # subtitle
    text = re.sub(
        r'(<p class="product-subtitle">)[^<]*(</p>)',
        rf"\g<1>{data['subtitle']}\g<2>",
        text,
        count=1,
    )
    # key specs grid
    keys_html = "".join(
        f'<div class="key-spec"><span class="key-spec-value">{v}</span>'
        f'<span class="key-spec-label">{l}</span></div>'
        for v, l in data["keys"]
    )
    text = re.sub(
        r'<div class="key-specs-grid">.*?</div>',
        f'<div class="key-specs-grid">{keys_html}</div>',
        text,
        count=1,
        flags=re.S,
    )
    # description
    text = re.sub(
        r'(<p class="product-desc">)[^<]*(</p>)',
        rf"\g<1>{data['desc']}\g<2>",
        text,
        count=1,
    )
    # meta description + og/twitter (first occurrence each)
    meta_desc = data["desc"][:155] + ("…" if len(data["desc"]) > 155 else "")
    text = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        rf"\g<1>{meta_desc}\g<2>",
        text,
        count=1,
    )
    text = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        rf"\g<1>{meta_desc}\g<2>",
        text,
        count=1,
    )
    text = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        rf"\g<1>{meta_desc}\g<2>",
        text,
        count=1,
    )
    # JSON-LD description field
    text = re.sub(
        r'("description":\s*")[^"]*(")',
        rf'\g<1>{data["desc"].replace(chr(34), chr(39))}\g<2>',
        text,
        count=1,
    )
    # spec table
    rows = "".join(f"<li><span>{k}</span><span>{v}</span></li>" for k, v in data["specs"])
    text = re.sub(
        r'(<ul class="spec-table">).*?(</ul>)',
        rf"\g<1>{rows}\g<2>",
        text,
        count=1,
        flags=re.S,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  enriched {filename}")


def noindex_orphan_ultimate_f() -> None:
    """G1 Ultimate F (U8) has no listino SKU — keep page but noindex until priced."""
    for name in ("unitree-g1-edu-ultimate-f.html",):
        path = PROD / name
        if not path.exists():
            continue
        t = path.read_text(encoding="utf-8")
        t2 = re.sub(
            r'<meta name="robots" content="[^"]*">',
            '<meta name="robots" content="noindex, follow">',
            t,
            count=1,
        )
        if t2 == t and 'name="robots"' not in t:
            t2 = t.replace(
                "<title>",
                '<meta name="robots" content="noindex, follow">\n  <title>',
                1,
            )
        if t2 != t:
            path.write_text(t2, encoding="utf-8")
            print(f"  noindex {name}")


def update_manifest(eu: dict) -> None:
    path = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    added = 0
    for sku in (
        "H2-HAND-REVO3-U21",
        "H2-HAND-REVO3-U21T",
        "H2-HAND-REVO3-U21V",
        "H2-HAND-INSPIRE-E2",
    ):
        if sku in data:
            continue
        e = eu.get(sku, {})
        data[sku] = {
            "titolo": e.get("nome", sku),
            "sottotitolo": "Accessorio mano H2",
            "descrizione": e.get("nome", sku),
            "immagine": e.get("immagine", "images/accessori/brainco-revo3-u21.jpg"),
            "categoria": e.get("categoria", "MANI_BRACCI"),
            "slug": e.get("slug", ""),
        }
        added += 1
    if added:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  manifest +{added} SKU")


def fix_blog_index() -> None:
    """Fix broken og:image on blog.html; ensure ricerca card stays; leave seo-report unlisted (internal)."""
    path = ROOT / "blog.html"
    t = path.read_text(encoding="utf-8")
    bad = "https://abrarobotics.com/prodotti/assets/images/g1-01.jpg"
    good = "https://abrarobotics.com/images/g1-hero.png"
    if bad in t:
        path.write_text(t.replace(bad, good), encoding="utf-8")
        print("  blog.html og:image fixed")
    # noindex internal seo-report if indexable
    report = ROOT / "blog" / "seo-report-abra-2026.html"
    if report.exists():
        rt = report.read_text(encoding="utf-8")
        if "noindex" not in rt.lower():
            rt2 = re.sub(
                r'<meta name="robots" content="[^"]*">',
                '<meta name="robots" content="noindex, follow">',
                rt,
                count=1,
            )
            if rt2 == rt:
                rt2 = rt.replace(
                    "<title>",
                    '<meta name="robots" content="noindex, follow">\n<title>',
                    1,
                )
            report.write_text(rt2, encoding="utf-8")
            print("  noindex blog/seo-report-abra-2026.html")


def main() -> None:
    eu = json.loads(EU_PATH.read_text(encoding="utf-8"))
    print("== sync prices ==")
    n = sync_prices(eu)
    print(f"  updated {n} pages")
    print("== G1-D consolidate ==")
    consolidate_g1d()
    print("== enrich hands ==")
    for fn, data in HAND_SPECS.items():
        enrich_hand_page(fn, data)
    print("== ultimate F / manifest / blog ==")
    noindex_orphan_ultimate_f()
    update_manifest(eu)
    fix_blog_index()
    print("done")


if __name__ == "__main__":
    main()
