#!/usr/bin/env python3
"""Collega i prezzi del blog alle schede prodotto, in forma visiva.

Nel testo degli articoli un prezzo si scrive {{P:<slug-prodotto>}} (con «IVA esclusa») o
{{p:<slug-prodotto>}} (solo la cifra), oppure è già un link <a class="prezzo" data-prodotto=...>.
Lo script legge nome, foto e prezzo dal JSON-LD della scheda prodotti/<slug>.html e scrive un
«chip» (miniatura + prezzo) che porta alla scheda; al passaggio del mouse si apre una mini card
(foto, nome, prezzo, «Vedi scheda»). Così il blog resta allineato al listino.

Uso: python3 scripts/aggiorna_prezzi_blog.py [file.html ...]   (senza argomenti: blog/ e */blog/)
"""
from __future__ import annotations

import glob
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = re.compile(r"\{\{([Pp]):([a-z0-9-]+)\}\}")  # P = con etichetta IVA, p = solo cifra
LINK = re.compile(r'<a class="prezzo" data-prodotto="([a-z0-9-]+)"[^>]*>.*?</a>( <span class="prezzo-iva">[^<]*</span>| IVA esclusa| excl\. VAT)?', re.S)

IVA = {"it": "IVA esclusa", "en": "excl. VAT", "de": "zzgl. MwSt.", "fr": "HT", "es": "sin IVA", "nl": "excl. btw",
       "pl": "netto", "cs": "bez DPH", "sv": "exkl. moms", "da": "ekskl. moms", "no": "eks. mva", "fi": "alv 0 %"}
VEDI = {"it": "Vedi scheda", "en": "View product", "de": "Zum Produkt", "fr": "Voir la fiche", "es": "Ver ficha",
        "nl": "Bekijk product", "pl": "Zobacz produkt", "cs": "Zobrazit produkt", "sv": "Se produkten", "da": "Se produktet",
        "no": "Se produktet", "fi": "Katso tuote"}
_cache: dict[str, dict | None] = {}


def scheda(slug: str) -> dict | None:
    """Nome, foto e prezzo dal JSON-LD Product della scheda italiana."""
    if slug in _cache:
        return _cache[slug]
    f = ROOT / "prodotti" / f"{slug}.html"
    info = None
    if f.exists():
        s = f.read_text(encoding="utf-8")
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                d = json.loads(b)
            except ValueError:
                continue
            for x in d if isinstance(d, list) else d.get("@graph", [d]):
                if not isinstance(x, dict) or x.get("@type") != "Product":
                    continue
                off = x.get("offers") or {}
                off = off[0] if isinstance(off, list) else off
                img = x.get("image") or ""
                img = img[0] if isinstance(img, list) else img
                img = img.get("url", "") if isinstance(img, dict) else img
                if off.get("price"):
                    info = {"nome": x.get("name", slug), "prezzo": float(off["price"]),
                            "img": re.sub(r"^https?://[^/]+", "", img)}
                    break
            if info:
                break
    _cache[slug] = info
    return info


def formatta(v: float, lang: str) -> str:
    n = f"{round(v):,}"
    if lang == "en":
        return "€" + n
    if lang in ("fr", "pl", "cs", "sv", "no", "fi"):
        return n.replace(",", " ") + " €"
    return n.replace(",", ".") + " €"


def lingua(path: Path) -> str:
    first = path.relative_to(ROOT).parts[0]
    return "it" if first == "blog" else first


def link(slug: str, path: Path, label: bool) -> str | None:
    info = scheda(slug)
    if info is None:
        print(f"ATTENZIONE {path.name}: nessun prezzo per {slug} (scheda mancante o su richiesta), lasciato com'era")
        return None
    lang = lingua(path)
    if lang == "it":
        href = "../" * (len(path.relative_to(ROOT).parts) - 1) + f"prodotti/{slug}.html"
    elif (ROOT / "en" / "prodotti" / f"{slug}-en.html").exists():
        href = f"/en/prodotti/{slug}-en.html"   # le altre lingue usano la scheda inglese
    else:
        href = f"/prodotti/{slug}.html"
    p, nome, img = formatta(info["prezzo"], lang), html.escape(info["nome"]), html.escape(info["img"])
    iva = IVA.get(lang, IVA["en"])
    thumb = f'<img src="{img}" alt="" width="20" height="20" loading="lazy">' if img else ""
    card = (f'<span class="prezzo-card" aria-hidden="true">'
            + (f'<img src="{img}" alt="" loading="lazy">' if img else "")
            + f'<b>{nome}</b><span>{p} {iva}</span><em>{VEDI.get(lang, VEDI["en"])} →</em></span>')
    a = (f'<a class="prezzo" data-prodotto="{slug}" href="{href}" title="{nome}">'
         f'{thumb}<span class="prezzo-num">{p}</span>{card}</a>')
    return a + (f' <span class="prezzo-iva">{iva}</span>' if label else "")


def main(files: list[str]) -> None:
    paths = [Path(f).resolve() for f in files] or [
        Path(p) for p in glob.glob(str(ROOT / "blog" / "*.html")) + glob.glob(str(ROOT / "*" / "blog" / "*.html"))]
    changed = 0
    for p in paths:
        s = p.read_text(encoding="utf-8")
        s2 = PLACEHOLDER.sub(lambda m: link(m.group(2), p, m.group(1) == "P") or m.group(0), s)
        s2 = LINK.sub(lambda m: link(m.group(1), p, bool(m.group(2))) or m.group(0), s2)
        if 'class="prezzo"' in s2 and "prezzi.js" not in s2:
            s2 = s2.replace("</body>", '<script defer src="/blog/prezzi.js"></script>\n</body>', 1)
        if s2 != s:
            p.write_text(s2, encoding="utf-8")
            changed += 1
    print(f"prezzi aggiornati in {changed} file")


if __name__ == "__main__":
    main(sys.argv[1:])
