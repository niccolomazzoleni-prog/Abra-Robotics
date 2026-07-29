#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply upward-margin estimated End-User prices where listino has no SKU price.

Estimates (public refs + sibling listino), rounded UP, labeled stimato:
- AS2-W: public ~USD 36.7k → EU End-User w/ duty da €42.900 (AS2 Pro = €29.900)
- H2-D: above H2 (€63.700) → da €79.900
- H2 Plus: Thor + GR00T premium → da €149.900 preordine
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ESTIMATES = {
    "unitree-as2-w.html": {
        "sku": "AS2-W",
        "euro": 42900.0,
        "label": "da 42.900 €",
        "note": "Prezzo End-User indicativo stimato (listino Unitree non ancora pubblicato in IT) · IVA esclusa · conferma su preventivo",
        "availability": "https://schema.org/PreOrder",
    },
    "unitree-h2-d.html": {
        "sku": "H2-D",
        "euro": 79900.0,
        "label": "da 79.900 €",
        "note": "Prezzo End-User indicativo stimato (configurazione tipica) · IVA esclusa · conferma su preventivo",
        "availability": "https://schema.org/PreOrder",
    },
    "unitree-h2-plus.html": {
        "sku": "H2-PLUS",
        "euro": 149900.0,
        "label": "da 149.900 €",
        "note": "Preordine indicativo stimato fine 2026 · IVA esclusa · conferma su preventivo",
        "availability": "https://schema.org/PreOrder",
    },
}


def patch_product(path: Path, meta: dict) -> None:
    t = path.read_text(encoding="utf-8", errors="replace")
    price = f"{meta['euro']:.2f}"
    label = meta["label"]
    note = meta["note"]
    avail = meta["availability"]
    url = f"https://abrarobotics.com/prodotti/{path.name}"

    old_buy = (
        '<span class="buy-box-amount" style="font-size:1.5rem;">Prezzo su richiesta</span>'
    )
    new_buy = (
        f'<span class="buy-box-amount" style="font-size:1.5rem;">{label}</span>'
        f'<p style="font-size:0.78rem;color:var(--gray-500);margin:8px 0 0;line-height:1.4;">{note}</p>'
    )
    if old_buy not in t:
        raise SystemExit(f"buy box not found: {path.name}")
    t = t.replace(old_buy, new_buy, 1)

    offer_block = (
        '  "brand": {"@type": "Brand", "name": "Unitree"},\n'
        f'  "offers": {{"@type": "Offer", "priceCurrency": "EUR", "price": "{price}",\n'
        '    "priceValidUntil": "2026-12-31",\n'
        '    "itemCondition": "https://schema.org/NewCondition",\n'
        f'    "availability": "{avail}",\n'
        f'    "url": "{url}",\n'
        '    "seller": {"@type": "Organization", "name": "Abra Robotics", "url": "https://abrarobotics.com"}}}'
    )
    t2, n = re.subn(
        r'  "brand": \{"@type": "Brand", "name": "Unitree"\}\}',
        offer_block,
        t,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"Product schema brand not found: {path.name}")
    path.write_text(t2, encoding="utf-8")
    print("patched", path.name, label)


def patch_manifest() -> None:
    p = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    mapping = {
        "AS2-W": 42900,
        "H2-D": 79900,
        "H2-PLUS": 149900,
    }
    for sku, prezzo in mapping.items():
        if sku not in data:
            raise SystemExit(f"missing sku {sku}")
        data[sku]["prezzo_da"] = prezzo
        data[sku]["prezzo_su_richiesta"] = False
        data[sku]["prezzo_stimato"] = True
        data[sku]["prezzo_nota"] = "Indicativo stimato · conferma su preventivo"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("patched catalogo-manifest.json")


def patch_hubs() -> None:
    as2 = ROOT / "as2.html"
    t = as2.read_text(encoding="utf-8")
    t = t.replace(
        '<span class="card-price">su preventivo</span><a class="btn btn-primary btn-sm" href="prodotti/unitree-as2-w.html">',
        '<span class="card-price">da 42.900 € <small>(stim.)</small></span><a class="btn btn-primary btn-sm" href="prodotti/unitree-as2-w.html">',
        1,
    )
    as2.write_text(t, encoding="utf-8")

    h2 = ROOT / "h2.html"
    t = h2.read_text(encoding="utf-8")
    t = t.replace(
        '<span class="key-spec-label">Listino</span><span class="key-spec-value">RFQ</span>',
        '<span class="key-spec-label">Prezzo</span><span class="key-spec-value">da 79.9k</span>',
        1,
    )
    t = t.replace(
        '<span class="card-price">su preventivo</span><a class="btn btn-primary btn-sm" href="prodotti/unitree-h2-d.html">',
        '<span class="card-price">da 79.900 € <small>(stim.)</small></span><a class="btn btn-primary btn-sm" href="prodotti/unitree-h2-d.html">',
        1,
    )
    t = t.replace(
        '<span class="card-price">preordine</span><a class="btn btn-primary btn-sm" href="prodotti/unitree-h2-plus.html">',
        '<span class="card-price">da 149.900 € <small>(stim.)</small></span><a class="btn btn-primary btn-sm" href="prodotti/unitree-h2-plus.html">',
        1,
    )
    t = t.replace(
        "H2-D e H2 Plus su preventivo/preordine.",
        "H2-D da ~79.900 € e H2 Plus da ~149.900 € (stime indicative, conferma su preventivo).",
    )
    h2.write_text(t, encoding="utf-8")
    print("patched hubs")


def patch_llms() -> None:
    for name in ("llms.txt", "llm.txt"):
        p = ROOT / name
        t = p.read_text(encoding="utf-8")
        t = t.replace(
            "| AS2-W (wheeled) | su preventivo |",
            "| AS2-W (wheeled) | da 42.900 € (stim. indicativo) |",
        )
        t = t.replace(
            "| H2-D | su preventivo |",
            "| H2-D | da 79.900 € (stim. indicativo) |",
        )
        t = t.replace(
            "| H2 Plus | preordine fine 2026 (AGX Thor, Sharpa Wave, Isaac GR00T) |",
            "| H2 Plus | da 149.900 € stim. preordine fine 2026 (AGX Thor, Sharpa Wave, Isaac GR00T) |",
        )
        p.write_text(t, encoding="utf-8")
    print("patched llms")


def patch_quadrupedi() -> None:
    p = ROOT / "quadrupedi.html"
    t = p.read_text(encoding="utf-8")
    old = (
        "<h3>Unitree AS2-W</h3>\n"
        '<p class="robot-subtitle">Quadrupede wheeled serie AS</p>'
    )
    # price is a few lines below; replace the preventivo near AS2-W only
    idx = t.find("Unitree AS2-W")
    if idx < 0:
        raise SystemExit("AS2-W not in quadrupedi")
    chunk = t[idx : idx + 1200]
    if "su preventivo" not in chunk:
        raise SystemExit("preventivo not near AS2-W")
    chunk2 = chunk.replace(
        "su preventivo",
        "da 42.900 € <small>(stim.)</small>",
        1,
    )
    t = t[:idx] + chunk2 + t[idx + 1200 :]
    p.write_text(t, encoding="utf-8")
    print("patched quadrupedi")


def patch_umanoidi() -> None:
    p = ROOT / "umanoidi.html"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    changed = False
    for needle, price in (
        ("unitree-h2-d.html", "da 79.900 € <small>(stim.)</small>"),
        ("unitree-h2-plus.html", "da 149.900 € <small>(stim.)</small>"),
    ):
        i = t.find(needle)
        if i < 0:
            continue
        # look backwards for card-price / preventivo in ~800 chars before link
        start = max(0, i - 900)
        window = t[start:i]
        for old in ("su preventivo", "preordine", "Prezzo su richiesta"):
            j = window.rfind(old)
            if j >= 0:
                window = window[:j] + price + window[j + len(old) :]
                t = t[:start] + window + t[i:]
                changed = True
                break
    if changed:
        p.write_text(t, encoding="utf-8")
        print("patched umanoidi")
    else:
        print("umanoidi: no RFQ cards found (ok)")


def main() -> None:
    for fname, meta in ESTIMATES.items():
        patch_product(ROOT / "prodotti" / fname, meta)
    patch_manifest()
    patch_hubs()
    patch_llms()
    patch_quadrupedi()
    patch_umanoidi()


if __name__ == "__main__":
    main()
