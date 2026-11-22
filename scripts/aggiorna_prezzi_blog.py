#!/usr/bin/env python3
"""Collega i prezzi del blog alle schede prodotto.

Nel testo degli articoli un prezzo si scrive {{P:<slug-prodotto>}} oppure è già un link
<a class="prezzo" data-prodotto="<slug>" ...>. Lo script legge il prezzo dal JSON-LD della
scheda prodotti/<slug>.html e scrive il link con il prezzo attuale, così il blog non resta
indietro quando cambia il listino.

Uso: python3 scripts/aggiorna_prezzi_blog.py [file.html ...]   (senza argomenti: tutto blog/ e */blog/)
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = re.compile(r"\{\{([Pp]):([a-z0-9-]+)\}\}")  # P = con "IVA esclusa", p = solo cifra
LINK = re.compile(r'<a class="prezzo" data-prodotto="([a-z0-9-]+)"[^>]*>[^<]*</a>( IVA esclusa| excl\. VAT)?')
LABEL = {"it": "IVA esclusa", "en": "excl. VAT"}


def prezzo(slug: str) -> float | None:
    f = ROOT / "prodotti" / f"{slug}.html"
    if not f.exists():
        return None
    m = re.search(r'"price":\s*"?([\d.]+)"?', f.read_text(encoding="utf-8"))
    return float(m.group(1)) if m else None


def formatta(v: float, lang: str) -> str:
    n = f"{round(v):,}"
    return ("€" + n) if lang == "en" else (n.replace(",", ".") + " €")


def lingua(path: Path) -> str:
    rel = path.relative_to(ROOT).parts
    return "it" if rel[0] == "blog" else ("en" if rel[0] == "en" else rel[0])


def link(slug: str, path: Path, label: bool = True) -> str | None:
    v = prezzo(slug)
    if v is None:
        print(f"ATTENZIONE {path.name}: nessun prezzo per {slug} (scheda mancante o su richiesta), lasciato com'era")
        return None
    lang = lingua(path)
    if lang == "it":
        href = "../" * (len(path.relative_to(ROOT).parts) - 1) + f"prodotti/{slug}.html"
    elif (ROOT / "en" / "prodotti" / f"{slug}-en.html").exists():
        href = f"/en/prodotti/{slug}-en.html"   # le altre lingue usano la scheda inglese
    else:
        href = f"/prodotti/{slug}.html"
    a = f'<a class="prezzo" data-prodotto="{slug}" href="{href}">{formatta(v, lang)}</a>'
    return a + (" " + LABEL.get(lang, LABEL["en"]) if label else "")


def main(files: list[str]) -> None:
    paths = [Path(f).resolve() for f in files] or [Path(p) for p in glob.glob(str(ROOT / "blog" / "*.html")) + glob.glob(str(ROOT / "*" / "blog" / "*.html"))]
    changed = 0
    for p in paths:
        s = p.read_text(encoding="utf-8")
        s2 = PLACEHOLDER.sub(lambda m: link(m.group(2), p, m.group(1) == "P") or m.group(0), s)
        s2 = LINK.sub(lambda m: link(m.group(1), p, bool(m.group(2))) or m.group(0), s2)
        if s2 != s:
            p.write_text(s2, encoding="utf-8")
            changed += 1
    print(f"prezzi aggiornati in {changed} file")


if __name__ == "__main__":
    main(sys.argv[1:])
