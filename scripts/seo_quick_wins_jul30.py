#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick SEO wins: nav/footer hubs, catalog/listino SKUs, AS2 images, hub↔blog links."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_INSERT = '<a href="as2.html">Unitree AS2</a>\n<a href="h2.html">Unitree H2</a>\n'
NAV_ANCHOR = '<a href="umanoidi.html">Umanoidi</a>\n'
FOOTER_INSERT = '<a href="as2.html">Unitree AS2</a>\n<a href="h2.html">Unitree H2</a>\n'
FOOTER_ANCHOR = '<a href="umanoidi.html">Umanoidi</a>\n'

# Pages with relative root links (not in subdirs)
ROOT_PAGES = [
    "index.html",
    "umanoidi.html",
    "quadrupedi.html",
    "catalogo-unitree.html",
    "listino-unitree.html",
    "accessori.html",
    "manifattura-logistica.html",
    "blog.html",
    "assessment.html",
    "finanziamenti.html",
    "chi-siamo.html",
    "catalogo.html",
    "catalogo-cobot.html",
    "catalogo-amr.html",
    "lp-unitree.html",
    "lp-umanoidi.html",
    "lp-quadrupedi.html",
    "g1-d.html",
]


def patch_nav_footer(path: Path) -> bool:
    t = path.read_text(encoding="utf-8", errors="replace")
    orig = t
    if 'href="as2.html">Unitree AS2</a>' not in t and 'href="as2.html">AS2</a>' not in t:
        # desktop + mobile prodotti dropdown: after Umanoidi
        t = t.replace(
            NAV_ANCHOR + '<a href="accessori.html">Accessori</a>',
            NAV_ANCHOR + NAV_INSERT + '<a href="accessori.html">Accessori</a>',
        )
        # footer prodotti
        t = t.replace(
            FOOTER_ANCHOR + '<a href="accessori.html">Accessori</a>',
            FOOTER_ANCHOR + FOOTER_INSERT + '<a href="accessori.html">Accessori</a>',
        )
    if t != orig:
        path.write_text(t, encoding="utf-8")
        return True
    return False


def fix_quadrupedi() -> None:
    p = ROOT / "quadrupedi.html"
    t = p.read_text(encoding="utf-8", errors="replace")
    t = t.replace(
        "<title>Robot quadrupede Unitree Go2, A2, B2 | Abra Robotics</title>",
        "<title>Robot quadrupede Unitree AS2, Go2, A2, B2 | Abra Robotics</title>",
    )
    t = t.replace(
        'content="Robot quadrupede Unitree in Italia: Go2, A2 e B2 per ispezione e industria. Specifiche, prezzi e supporto Abra Robotics."',
        'content="Robot quadrupede Unitree in Italia: AS2, Go2, A2 e B2 per ispezione e industria. Specifiche, prezzi e hub AS2 — Abra Robotics."',
    )
    # Fix wrong AS2 card images (were a2-pro.png)
    replacements = [
        (
            'alt="Unitree AS2 Air, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/a2-pro.png"',
            'alt="Unitree AS2 Air, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/unitree-as2-card.png"',
        ),
        (
            'alt="Unitree AS2-X, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/a2-pro.png"',
            'alt="Unitree AS2-X, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/unitree-as2-card.png"',
        ),
        (
            'alt="Unitree AS2 EDU, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/a2-pro.png"',
            'alt="Unitree AS2 EDU, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/unitree-as2-card.png"',
        ),
        (
            'alt="Unitree AS2 Pro, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/a2-pro.png"',
            'alt="Unitree AS2 Pro, quadrupede Unitree" loading="lazy" onerror="this.parentElement.classList.add(\'no-img\');" src="images/prodotti/unitree-as2-pro.png"',
        ),
    ]
    for a, b in replacements:
        t = t.replace(a, b)
    # blog link near AS2 hub mention if missing
    if "blog/unitree-as2-italia.html" not in t:
        t = t.replace(
            'vedi anche <a href="as2.html">hub AS2</a>.',
            'vedi anche <a href="as2.html">hub AS2</a> e la guida <a href="blog/unitree-as2-italia.html">Unitree AS2 in Italia</a>.',
        )
    p.write_text(t, encoding="utf-8")
    print("patched quadrupedi.html")


def patch_hubs() -> None:
    as2 = ROOT / "as2.html"
    t = as2.read_text(encoding="utf-8", errors="replace")
    if "blog/unitree-as2-italia.html" not in t:
        t = t.replace(
            '<section class="seo-faq" id="faq">',
            '<section class="section" style="padding-top:0"><div class="container">'
            '<p style="font-size:0.95rem;color:var(--gray-600);max-width:40rem;">'
            'Approfondimento: <a href="blog/unitree-as2-italia.html">guida Unitree AS2 in Italia</a> · '
            '<a href="quadrupedi.html">tutti i quadrupedi</a> · '
            '<a href="listino-unitree.html">listino End-User</a>.'
            "</p></div></section>\n"
            '<section class="seo-faq" id="faq">',
        )
        as2.write_text(t, encoding="utf-8")
        print("patched as2.html blog link")

    h2 = ROOT / "h2.html"
    t = h2.read_text(encoding="utf-8", errors="replace")
    if "blog/unitree-h2-italia.html" not in t:
        t = t.replace(
            '<section class="seo-faq" id="faq">',
            '<section class="section" style="padding-top:0"><div class="container">'
            '<p style="font-size:0.95rem;color:var(--gray-600);max-width:40rem;">'
            'Approfondimento: <a href="blog/unitree-h2-italia.html">guida Unitree H2 in Italia</a> · '
            '<a href="umanoidi.html">tutti gli umanoidi</a> · '
            '<a href="listino-unitree.html">listino End-User</a>.'
            "</p></div></section>\n"
            '<section class="seo-faq" id="faq">',
        )
        h2.write_text(t, encoding="utf-8")
        print("patched h2.html blog link")


def card(sku: str, family: str, href: str, img: str, title: str, price: str, name: str) -> str:
    return f"""        <article class="cat-card" data-cat="Umanoidi & robot" data-family="{family}" data-sku="{sku}" data-name="{name}">
          <a href="{href}" class="cat-media"><img src="{img}" alt="{title}" loading="lazy" onerror="this.style.display='none';this.parentElement.classList.add('no-img');"></a>
          <div class="cat-body">
            <p class="cat-family">{family}</p>
            <h3><a href="{href}">{title}</a></h3>
            <p class="cat-price">{price}</p>
            <a href="{href}" class="btn btn-secondary btn-sm">Scheda prodotto</a>
          </div>
        </article>
"""


def patch_catalog() -> None:
    p = ROOT / "catalogo-unitree.html"
    t = p.read_text(encoding="utf-8", errors="replace")
    changed = False
    if 'data-sku="AS2-W"' not in t:
        block = card(
            "AS2-W",
            "AS2",
            "prodotti/unitree-as2-w.html",
            "images/prodotti/as2-w.png",
            "Unitree AS2-W",
            "da 42.900 €",
            "unitree as2-w",
        )
        # after AS2-PRO card closing
        needle = 'data-sku="AS2-PRO"'
        idx = t.find(needle)
        if idx < 0:
            raise SystemExit("AS2-PRO card not found")
        end = t.find("</article>", idx) + len("</article>\n")
        t = t[:end] + block + t[end:]
        changed = True
    if 'data-sku="H2-D"' not in t:
        block = (
            card(
                "H2-D",
                "H2",
                "prodotti/unitree-h2-d.html",
                "images/prodotti/h2-d.png",
                "Unitree H2-D",
                "da 79.900 €",
                "unitree h2-d",
            )
            + card(
                "H2-PLUS",
                "H2",
                "prodotti/unitree-h2-plus.html",
                "images/prodotti/h2-plus.png",
                "Unitree H2 Plus",
                "da 149.900 €",
                "unitree h2 plus",
            )
        )
        needle = 'data-sku="H2-EDU"'
        idx = t.find(needle)
        if idx < 0:
            raise SystemExit("H2-EDU card not found")
        end = t.find("</article>", idx) + len("</article>\n")
        t = t[:end] + block + t[end:]
        changed = True
    # intro hub links near toolbar
    if 'href="as2.html"' not in t:
        t = t.replace(
            '<div class="cat-toolbar">',
            '<p style="margin:0 0 1rem;font-size:0.95rem;color:var(--gray-600);">'
            'Hub famiglie: <a href="as2.html">Unitree AS2</a> · <a href="h2.html">Unitree H2</a> · '
            '<a href="umanoidi.html">Umanoidi</a> · <a href="quadrupedi.html">Quadrupedi</a>'
            "</p>\n    <div class=\"cat-toolbar\">",
            1,
        )
        changed = True
    if changed:
        p.write_text(t, encoding="utf-8")
        print("patched catalogo-unitree.html")
    else:
        print("catalogo already ok")


def patch_listino_json() -> None:
    p = ROOT / "listini" / "pubblico" / "end-user.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    adds = {
        "AS2-W": {
            "nome": "AS2-W",
            "prezzo_eur": 42900.0,
            "note": "IVA esclusa · prezzo soggetto a variazioni · conferma su preventivo",
            "immagine": "images/prodotti/as2-w.png",
            "slug": "unitree-as2-w.html",
            "categoria": "UMANOIDI",
        },
        "H2-D": {
            "nome": "H2-D",
            "prezzo_eur": 79900.0,
            "note": "IVA esclusa · prezzo soggetto a variazioni · conferma su preventivo",
            "immagine": "images/prodotti/h2-d.png",
            "slug": "unitree-h2-d.html",
            "categoria": "UMANOIDI",
        },
        "H2-PLUS": {
            "nome": "H2 PLUS",
            "prezzo_eur": 149900.0,
            "note": "IVA esclusa · preordine fine 2026 · prezzo soggetto a variazioni",
            "immagine": "images/prodotti/h2-plus.png",
            "slug": "unitree-h2-plus.html",
            "categoria": "UMANOIDI",
        },
    }
    n = 0
    for k, v in adds.items():
        if k not in data:
            data[k] = v
            n += 1
    if n:
        # keep AS2-W near AS2-PRO
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"patched end-user.json (+{n})")
    else:
        print("end-user.json already ok")


def patch_listino_page() -> None:
    p = ROOT / "listino-unitree.html"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8", errors="replace")
    if 'href="as2.html"' not in t:
        # try common intro spots
        for needle in (
            '<h1',
            '<p class="lead"',
            '<div class="container">',
        ):
            i = t.find(needle)
            if i >= 0 and needle == '<p class="lead"':
                # append after lead paragraph end
                end = t.find("</p>", i)
                if end > 0:
                    insert = (
                        '</p>\n<p style="margin:0.5rem 0 0;font-size:0.9rem;color:var(--gray-600);">'
                        'Vedi anche hub <a href="as2.html">AS2</a> e <a href="h2.html">H2</a>.'
                    )
                    t = t[:i] + t[i:end] + insert + t[end + 4 :]
                    p.write_text(t, encoding="utf-8")
                    print("patched listino-unitree.html")
                    return
        print("listino: no lead to patch (ok)")
    else:
        print("listino already has hub links")


def main() -> None:
    n = 0
    for name in ROOT_PAGES:
        path = ROOT / name
        if path.exists() and patch_nav_footer(path):
            print("nav/footer", name)
            n += 1
    print(f"nav/footer pages: {n}")
    fix_quadrupedi()
    patch_hubs()
    patch_catalog()
    patch_listino_json()
    patch_listino_page()


if __name__ == "__main__":
    main()
