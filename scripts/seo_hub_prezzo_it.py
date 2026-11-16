#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hub IT scritti a mano (as2.html, h2.html) che rispondono a "unitree [modello] prezzo" (docs/seo-piano-italia.md, IT-2).

Gli altri hub li fa genera_hub_modelli.py; questi due sono pagine a mano, quindi si aggiornano qui con gli
stessi dati e regole (listino end-user.json via load(), USO_IT, PRONTA_CONSEGNA, CONSEGNA_IT):
- H1 con "prezzo" e prezzo di partenza dal listino nelle prime righe;
- tabella delle linee di prodotto (una riga per linea, configurazioni a lettera raggruppate) con prezzo,
  a chi serve e consegna;
- Product/AggregateOffer con i prezzi del listino.
Idempotente: si puo' rilanciare dopo ogni aggiornamento del listino.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from genera_hub_modelli import CONSEGNA_IT, FAMILIES, PRONTA_CONSEGNA, eur, load, uso_it  # noqa: E402

SITE = "https://abrarobotics.com"
MARK = ("<!-- HUB:PREZZI (scripts/seo_hub_prezzo_it.py) -->", "<!-- /HUB:PREZZI -->")
LD_ID = "hub-prezzi-ld"


def lead_as2(p: dict) -> str:
    return (f"L'Unitree AS2 costa da {eur(p['AS2-AIR'], False)} € IVA esclusa nella versione AS2 Air, con spedizione e dazio "
            f"in Italia inclusi (listino End-User); le versioni EDU per lo sviluppo partono da {eur(p['AS2-EDU'], False)} €.")


def lead_h2(p: dict) -> str:
    return (f"L'Unitree H2 costa da {eur(p['H2-AIR'], False)} € IVA esclusa nella versione H2 Basic (Air), con spedizione e "
            f"dazio in Italia inclusi (listino End-User); le versioni a busto dual-arm H2-A partono da {eur(p['H2-A-STD-A'], False)} €.")


PAGES = {"as2": ("as2.html", lead_as2), "h2": ("h2.html", lead_h2)}


def groups(rows: list[dict]) -> list[dict]:
    """Una riga per linea di prodotto: 'H2-D Standard A'...'M' -> 'H2-D Standard' con il prezzo piu' basso."""
    out: dict[str, dict] = {}
    for r in rows:
        if not r["price"]:
            continue
        g = re.sub(r"\s[A-N]$", "", r["name"])
        cur = out.get(g)
        if cur is None:
            out[g] = {"name": g, "price": r["price"], "slug": r["slug"], "n": 1, "pronta": r["sku"] in PRONTA_CONSEGNA}
        else:
            cur["n"] += 1
            if r["price"] < cur["price"]:
                cur.update(price=r["price"], slug=r["slug"])
    return sorted(out.values(), key=lambda g: g["price"])


def table_html(key: str, name: str, gs: list[dict]) -> str:
    tr = "\n".join(
        f'<tr><td><a href="prodotti/{g["slug"]}">{html.escape(g["name"])}</a>'
        + (f' <span style="color:var(--gray-500)">({g["n"]} configurazioni)</span>' if g["n"] > 1 else "")
        + f'</td><td>da {eur(g["price"], False)} €</td><td>{html.escape(uso_it(key, g["name"]))}</td>'
        f'<td>{"pronta consegna" if g["pronta"] else "60 giorni"}</td></tr>'
        for g in gs)
    return (f'{MARK[0]}\n<section class="section" style="padding-top:24px"><div class="container">\n'
            f'<h2>Versioni e prezzi Unitree {name}</h2>\n'
            f'<p>Prezzi End-User IVA esclusa, spedizione e dazio in Italia inclusi. Ogni ordine si conferma con un preventivo '
            f'aggiornato. {CONSEGNA_IT}</p>\n'
            '<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:.95rem">'
            '<thead><tr><th style="text-align:left;padding:8px">Versione</th><th style="text-align:left;padding:8px">'
            'Prezzo (IVA esclusa)</th><th style="text-align:left;padding:8px">A chi serve</th>'
            '<th style="text-align:left;padding:8px">Consegna</th></tr></thead><tbody>\n'
            f'{tr}\n</tbody></table></div>\n</div></section>\n{MARK[1]}')


def product_ld(key: str, name: str, page: str, rows: list[dict]) -> str:
    prices = [r["price"] for r in rows if r["price"]]
    ld = {"@context": "https://schema.org", "@type": "Product", "name": f"Unitree {name}",
          "brand": {"@type": "Brand", "name": "Unitree"}, "image": f"{SITE}/{FAMILIES[key]['image']}", "url": f"{SITE}/{page}",
          "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": f"{min(prices):.2f}",
                     "highPrice": f"{max(prices):.2f}", "offerCount": len(prices),
                     "seller": {"@type": "Organization", "name": "Abra Robotics", "url": SITE}}}
    return f'<script type="application/ld+json" id="{LD_ID}">{json.dumps(ld, ensure_ascii=False)}</script>'


def main() -> None:
    data = load()
    for key, (page, lead) in PAGES.items():
        name = FAMILIES[key]["name"]
        rows = data[key]["robots"]
        price = {r["sku"]: r["price"] for r in rows}
        p = ROOT / page
        s = p.read_text(encoding="utf-8")
        s = re.sub(r"<h1>.*?</h1>", f"<h1>Unitree {name} prezzo in Italia: listino {date.today().year}</h1>", s, count=1, flags=re.S)
        s = re.sub(r'(<p class="lead">)(?:<span data-prezzo="">.*?</span> )?',
                   lambda m: f'{m.group(1)}<span data-prezzo="">{html.escape(lead(price), quote=False)}</span> ', s, count=1)
        block = table_html(key, name, groups(rows))
        if MARK[0] in s:
            s = re.sub(re.escape(MARK[0]) + r".*?" + re.escape(MARK[1]), lambda m: block, s, count=1, flags=re.S)
        else:
            i = s.index("</div></header>", s.index("collection-hero")) + len("</div></header>")
            s = s[:i] + "\n" + block + s[i:]
        ld = product_ld(key, name, page, rows)
        if f'id="{LD_ID}"' in s:
            s = re.sub(rf'<script type="application/ld\+json" id="{LD_ID}">.*?</script>', lambda m: ld, s, count=1, flags=re.S)
        else:
            s = s.replace("</head>", f"{ld}\n</head>", 1)
        p.write_text(s, encoding="utf-8")
        print(f"{page}: {len(groups(rows))} linee, {len([r for r in rows if r['price']])} configurazioni")


if __name__ == "__main__":
    main()
