#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pagina del marchio Unitree (docs/seo-piano-europa-2027.md, fase 1).

Una sola pagina per "unitree" / "unitree italia": catalogo-unitree.html.
- voce "Unitree Italia" in menu e footer di tutte le pagine italiane (le nuove la prendono da site_nav.py);
- lp-unitree.html con canonical verso il catalogo (esce dalla sitemap) e link interni spostati sul catalogo;
- titolo, H1, testo introduttivo e schema del catalogo allineati a genera_catalogo_completo.py.
Idempotente: si puo' rilanciare.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from genera_catalogo_completo import BRAND_HUBS, BRAND_INTRO, SITE  # noqa: E402

LANG_DIRS = {"en", "de", "es", "fr", "pl", "sv", "da", "no", "nl", "cs", "fi", "pt", "uk"}
SKIP_DIRS = {".git", ".claude", "admin", "editor", "node_modules", "docs", "listini", "apps-script"}
NAV_RE = re.compile(r'(?P<ind>[ \t]*)<a href="(?P<pre>(?:\.\./)*)catalogo\.html">Catalogo completo</a>')


def italian_pages() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.html"):
        parts = p.relative_to(ROOT).parts
        if parts[0] in LANG_DIRS or SKIP_DIRS & set(parts) or p.name.endswith("-en.html"):
            continue
        out.append(p)
    return out


def add_nav_link(s: str) -> str:
    def sub(m: re.Match) -> str:
        before = s[max(0, m.start() - 160):m.start()]
        if 'catalogo-unitree.html">Unitree Italia</a>' in before:
            return m.group(0)
        return f'{m.group("ind")}<a href="{m.group("pre")}catalogo-unitree.html">Unitree Italia</a>\n{m.group(0)}'
    return NAV_RE.sub(sub, s)


def retarget_lp(s: str) -> str:
    return re.sub(r'href="((?:\.\./)*|/|https://abrarobotics\.com/)lp-unitree\.html"', r'href="\1catalogo-unitree.html"', s)


def fix_lp_unitree() -> None:
    p = ROOT / "lp-unitree.html"
    s = p.read_text(encoding="utf-8")
    s = s.replace(f'<link rel="canonical" href="{SITE}/lp-unitree.html">', f'<link rel="canonical" href="{SITE}/catalogo-unitree.html">')
    # hreflang verso se stessa contraddice il canonical: via
    s = re.sub(r'\s*<link href="https://abrarobotics\.com/lp-unitree\.html" hreflang="[^"]+" rel="alternate"/>', "", s)
    p.write_text(s, encoding="utf-8")


def fix_catalogo() -> None:
    p = ROOT / "catalogo-unitree.html"
    s = p.read_text(encoding="utf-8")
    rep = {
        "<title>Catalogo Unitree Italia: tutti i prodotti e prezzi | Abra</title>":
            "<title>Unitree Italia: catalogo e prezzi di tutti i robot | Abra</title>",
        '<meta name="description" content="Catalogo completo Unitree con prezzi End-User pubblici: umanoidi, quadrupedi, mani, batterie e accessori. Filiera Unitree Italia.">':
            '<meta name="description" content="Unitree in Italia: catalogo completo con prezzi End-User pubblici di umanoidi, quadrupedi, bracci e accessori. Spedizione e dazio inclusi, supporto in italiano.">',
        '<meta property="og:title" content="Catalogo Unitree — Abra Robotics">':
            '<meta property="og:title" content="Unitree Italia: catalogo e prezzi — Abra Robotics">',
        '<p class="label">Catalogo pubblico End-User</p>': '<p class="label">Filiera di distribuzione Unitree Italia</p>',
        "<h1>Tutti i prodotti Unitree</h1>": "<h1>Unitree in Italia: catalogo e prezzi</h1>",
    }
    for a, b in rep.items():
        s = s.replace(a, b)
    old_p = re.search(r'<p style="color:var\(--gray-600\);max-width:640px;">(Listino pubblico End-User — IVA esclusa, spedizione e dazio inclusi\. \d+ prodotti con scheda e prezzo trasparente\.)</p>', s)
    if old_p:
        s = s.replace(old_p.group(0),
                      f'<p style="color:var(--gray-600);max-width:720px;">{BRAND_INTRO}</p>\n'
                      f'    <p style="color:var(--gray-600);max-width:720px;">{old_p.group(1)} Chi vende Unitree in Italia e come scegliere: '
                      '<a href="blog/unitree-italia-guida-completa.html">guida completa a Unitree in Italia</a>.</p>')
    if '"name": "Robot Unitree in Italia"' not in s:
        lds = (
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Unitree Italia", "item": f"{SITE}/catalogo-unitree.html"}]},
            {"@context": "https://schema.org", "@type": "ItemList", "name": "Robot Unitree in Italia",
             "itemListElement": [{"@type": "ListItem", "position": i, "name": f"Unitree {n}", "url": f"{SITE}/{u}"}
                                 for i, (n, u) in enumerate(BRAND_HUBS, 1)]})
        block = "\n".join(f'  <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
        s = re.sub(r'(<meta property="og:image" content="[^"]*">)', lambda m: m.group(1) + "\n" + block, s, count=1)
    p.write_text(s, encoding="utf-8")


def main() -> None:
    nav = lp = 0
    for p in italian_pages() + [q for q in ROOT.rglob("*.html") if q.relative_to(ROOT).parts[0] in LANG_DIRS]:
        s = p.read_text(encoding="utf-8")
        s2 = retarget_lp(s) if p.name != "lp-unitree.html" else s
        lp += s2 != s
        if p.relative_to(ROOT).parts[0] not in LANG_DIRS and not p.name.endswith("-en.html"):
            s3 = add_nav_link(s2)
            nav += s3 != s2
            s2 = s3
        if s2 != s:
            p.write_text(s2, encoding="utf-8")
    fix_lp_unitree()
    fix_catalogo()
    print(f"voce Unitree Italia aggiunta in {nav} pagine · link a lp-unitree spostati in {lp} pagine")


if __name__ == "__main__":
    main()
