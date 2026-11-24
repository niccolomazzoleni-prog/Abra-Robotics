#!/usr/bin/env python3
"""Allinea <lastmod> di sitemap.xml alla data dell'ultimo commit di ogni pagina.

Senza questo, Google (e lo script di indicizzazione serale) vede pagine modificate
come "già aggiornate" e non le ripassa. Cambia solo le date, non aggiunge né toglie URL.
Uso: python3 scripts/aggiorna_lastmod.py
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://abrarobotics.com/"


def data_commit(path: str) -> str | None:
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or None


def main() -> None:
    sm = ROOT / "sitemap.xml"
    xml = sm.read_text(encoding="utf-8")
    cambiate = 0

    def rep(m: re.Match) -> str:
        nonlocal cambiate
        loc, spazio, vecchia = m.group(1), m.group(2), m.group(3)
        rel = loc[len(SITE):] or "index.html"
        if rel.endswith("/"):
            rel += "index.html"
        nuova = data_commit(rel) if (ROOT / rel).exists() else None
        if nuova and nuova > vecchia[:10]:
            cambiate += 1
            return f"<loc>{loc}</loc>{spazio}<lastmod>{nuova}</lastmod>"
        return m.group(0)

    xml2 = re.sub(r"<loc>([^<]+)</loc>(\s*)<lastmod>([^<]+)</lastmod>", rep, xml)
    if xml2 != xml:
        sm.write_text(xml2, encoding="utf-8")
    print(f"lastmod aggiornati: {cambiate}")


if __name__ == "__main__":
    main()
