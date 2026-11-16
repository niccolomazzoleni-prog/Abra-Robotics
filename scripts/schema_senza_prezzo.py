#!/usr/bin/env python3
"""Toglie dai dati strutturati i Product senza offerta, recensioni o valutazione.

Google li segna come errore ("Either offers, review, or aggregateRating should be specified") e non
mostrerebbe comunque un risultato avanzato: succede sulle schede con prezzo su richiesta (G1 Plus,
marchi partner, alcuni ricambi) e nelle offerte generiche della home. Il testo della pagina resta
com'e'; i Product con prezzo non vengono toccati.
Uso: python scripts/schema_senza_prezzo.py [file ...]   (senza argomenti: tutto il sito)"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SALTA = {"node_modules", "admin", "editor", "condivisi", "scripts", "apps-script", "docs"}
BLOCCO = re.compile(r'(\s*)<script type="application/ld\+json">(.*?)</script>', re.S)


def is_type(x, t: str) -> bool:
    v = x.get("@type") if isinstance(x, dict) else None
    return v == t or (isinstance(v, list) and t in v)


def senza_prezzo(x) -> bool:
    return is_type(x, "Product") and not any(x.get(k) for k in ("offers", "review", "aggregateRating"))


def offerta_vuota(x) -> bool:
    return is_type(x, "Offer") and not x.get("price") and senza_prezzo(x.get("itemOffered"))


def pulisci(x):
    """Restituisce (nuovo valore, cambiato); nuovo valore None = elemento da togliere."""
    if senza_prezzo(x) or offerta_vuota(x):
        return None, True
    cambiato = False
    if isinstance(x, list):
        out = []
        for v in x:
            n, c = pulisci(v)
            cambiato |= c
            if n is not None:
                out.append(n)
        return out, cambiato
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            n, c = pulisci(v)
            cambiato |= c
            if n is None or (c and n == []):
                continue
            out[k] = n
        return out, cambiato
    return x, False


def tratta(path: Path) -> int:
    t = path.read_text(encoding="utf-8")
    if "application/ld+json" not in t or "Product" not in t:
        return 0
    tolti = 0

    def sost(m: re.Match) -> str:
        nonlocal tolti
        try:
            dati = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        nuovo, cambiato = pulisci(dati)
        if not cambiato:
            return m.group(0)
        tolti += 1
        if nuovo is None or nuovo == [] or (isinstance(nuovo, dict) and set(nuovo) <= {"@context"}):
            return ""
        a_capo = "\n" in m.group(2).strip()
        testo = json.dumps(nuovo, ensure_ascii=False, indent=2 if a_capo else None)
        nl = "\n" if a_capo else ""
        return f'{m.group(1)}<script type="application/ld+json">{nl}{testo}{nl}</script>'

    nuovo = BLOCCO.sub(sost, t)
    if tolti:
        path.write_text(nuovo, encoding="utf-8")
    return tolti


def main(args: list[str]) -> None:
    files = [Path(a).resolve() for a in args] or [
        p for p in ROOT.rglob("*.html")
        if not SALTA.intersection(p.relative_to(ROOT).parts) and not p.name.startswith("_")]
    toccati = [f for f in files if tratta(f)]
    print(f"schema_senza_prezzo: {len(toccati)} pagine corrette")
    for f in toccati[:60]:
        print("  ", f.relative_to(ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
