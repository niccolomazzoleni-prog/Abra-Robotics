#!/usr/bin/env python3
"""Controlli SEO e dati sulle pagine nelle lingue europee (scripts/genera_lingue.py) prima di pubblicare.

- HTML leggibile, JSON-LD valido, title <= 60 e description 70-160 caratteri, lang della pagina
- canonical = URL della pagina, nessun noindex
- hreflang reciproci (ogni pagina citata cita a sua volta) e con x-default; tutti gli URL esistono
- link relativi verso file esistenti
- prezzi in tabella = listino pubblico
- niente nomi di concorrenti, niente "ufficiale", niente lineette lunghe nei testi
Uscita 1 se qualcosa non va. Uso: python3 scripts/verifica_lingue.py
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://abrarobotics.com"
CODES = ["de", "fr", "nl", "da", "sv", "no", "fi", "es", "pl", "cs", "uk"]
COMPETITORS = re.compile(r"meko|reichelt|quadruped\.de|eagle ?robots|mybotshop|generation ?robots|botland|funduino|robotshop", re.I)
OFFICIAL = re.compile(r"(offiziell|officiel|offici[eë]l|officiell|offisiell|virallinen|official|autoris\w*|autoriz\w*|auktoriser\w*|autorisert)\w*\s+(\w+\s+)?(händler|vertrieb|vertriebs\w*|partner|distribut\w*|revendeur|dealer|forhandler|återförsälj\w*|jälleenmyy\w*|wederverkop\w*|importeur|importør|reseller|verdeler)", re.I)


def url_to_path(u: str) -> Path | None:
    if not u.startswith(SITE):
        return None
    rel = u[len(SITE):].lstrip("/")
    p = ROOT / rel
    return p / "index.html" if (rel == "" or rel.endswith("/")) else p


def text_of(s: str) -> str:
    s = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", s)
    return re.sub(r"<[^>]+>", " ", s)


def main() -> None:
    prices = {}
    for v in json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8")).values():
        if isinstance(v, dict) and v.get("slug"):
            prices[v["slug"].split("/")[-1]] = v.get("prezzo_eur")
    errors: list[str] = []
    pages = [p for c in CODES if (ROOT / c).is_dir() for p in sorted((ROOT / c).glob("*.html"))]
    alt_of: dict[str, dict[str, str]] = {}
    for p in pages:
        rel = p.relative_to(ROOT).as_posix()
        s = p.read_text(encoding="utf-8")
        own = f"{SITE}/{rel}".replace("/index.html", "/")
        e = lambda m: errors.append(f"{rel}: {m}")  # noqa: E731
        try:
            HTMLParser().feed(s)
        except Exception as x:  # pragma: no cover
            e(f"HTML: {x}")
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(m)
            except ValueError as x:
                e(f"JSON-LD: {x}")
        t = re.search(r"<title>([^<]*)</title>", s)
        if not t or len(t.group(1)) > 60:
            e(f"title {len(t.group(1)) if t else 'mancante'}: {t.group(1) if t else ''}")
        d = re.search(r'<meta content="([^"]*)" name="description"', s)
        if not d or not (70 <= len(d.group(1)) <= 160):
            e(f"description {len(d.group(1)) if d else 'mancante'}")
        lang = p.parent.name
        want = {"no": "nb", "uk": "en-GB"}.get(lang, lang)
        if f'<html lang="{want}"' not in s:
            e("lang della pagina")
        c = re.search(r'<link href="([^"]+)" rel="canonical"', s)
        if not c or c.group(1) != own:
            e(f"canonical {c.group(1) if c else 'mancante'} != {own}")
        if re.search(r'name="robots" content="[^"]*noindex', s) or re.search(r'content="[^"]*noindex[^"]*" name="robots"', s):
            e("noindex")
        alts = dict((h, u) for h, u in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s))
        alt_of[own] = alts
        if "x-default" not in alts or alts.get(want) != own:
            e("hreflang: manca x-default o la pagina stessa")
        for h, u in alts.items():
            q = url_to_path(u)
            if not q or not q.is_file():
                e(f"hreflang {h} verso pagina inesistente {u}")
        for href in re.findall(r'(?:href|src)="([^"#?]+)', s):
            if href.startswith(("http", "mailto:", "tel:", "data:", "//")):
                continue
            target = (p.parent / href).resolve()
            if href.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                e(f"link rotto {href}")
        for slug, price in re.findall(r'<td><a href="\.\./(?:en/)?prodotti/([^"]+)">[^<]*</a></td><td class="p">([^<]*)</td>', s):
            base = slug.replace("-en.html", ".html")
            n = int(re.sub(r"\D", "", price) or 0)
            lp = prices.get(base)
            if lp is None or abs(round(lp) - n) > 1:
                e(f"prezzo {slug}: pagina {price} listino {lp}")
        body = text_of(s)
        if COMPETITORS.search(body):
            e(f"concorrente: {COMPETITORS.search(body).group(0)}")
        if OFFICIAL.search(body):
            e(f"'ufficiale': {body[max(0, OFFICIAL.search(body).start() - 40):OFFICIAL.search(body).end() + 40]!r}")
        if "—" in re.sub(r"(?s)<footer.*?</footer>", "", body):
            e("lineetta lunga nel testo")
    # reciprocita' hreflang (anche verso le pagine IT/EN)
    for own, alts in alt_of.items():
        for h, u in alts.items():
            if h == "x-default" or u == own:
                continue
            q = url_to_path(u)
            if not q or not q.is_file():
                continue
            back = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', q.read_text(encoding="utf-8")))
            if own not in back.values():
                errors.append(f"hreflang non reciproco: {u} non cita {own}")
    print(f"pagine controllate: {len(pages)}")
    for x in errors:
        print(" -", x)
    print("OK" if not errors else f"{len(errors)} problemi")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
