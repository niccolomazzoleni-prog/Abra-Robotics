#!/usr/bin/env python3
"""Pagine inglesi: link alle schede EN vere (/en/prodotti/X-en.html) invece che ai rimandi /prodotti/X-en.html.
I rimandi restano (passano il ranking), ma i link interni devono puntare alla pagina finale, altrimenti le schede EN
risultano senza link. Idempotente. Uso: python3 scripts/link_en_diretti.py"""
from __future__ import annotations
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / "en" / "prodotti"


def main() -> None:
    changed = 0
    for p in list((ROOT / "en").glob("*.html")) + list(EN.glob("*.html")):
        s = p.read_text(encoding="utf-8")
        prefix = "../../prodotti/" if p.parent == EN else "../prodotti/"
        here = "" if p.parent == EN else "prodotti/"
        def rep(m):
            name = m.group(2)
            return f'{m.group(1)}{here}{name}"' if (EN / name).is_file() else m.group(0)
        n = re.sub(r'(href=")' + re.escape(prefix) + r'([a-z0-9-]+-en\.html)"', rep, s)
        if n != s:
            p.write_text(n, encoding="utf-8")
            changed += 1
    print(f"link EN diretti: {changed} pagine")


if __name__ == "__main__":
    main()
