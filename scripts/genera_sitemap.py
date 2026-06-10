#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera sitemap.xml con tutte le pagine indicizzabili."""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "prodotti"))
try:
    from _site import SITE  # noqa: E402
except ImportError:
    SITE = "https://abrarobotics.com"

EXCLUDE_FILES = {
    "index.backup.html",
    "index-zenixa.html",
    "restyle-preview.html",
    "catalogo.html",
    "grazie.html",
    "condizioni-di-vendita.html",
    "checklist.html",
}

EXCLUDE_DIRS = {"admin", "node_modules", "__pycache__"}

PRIORITY = {
    "index.html": 1.0,
    "catalogo-unitree.html": 0.9,
    "catalogo-amr.html": 0.9,
    "catalogo-cobot.html": 0.9,
    "quadrupedi.html": 0.9,
    "umanoidi.html": 0.9,
    "accessori.html": 0.85,
    "manifattura-logistica.html": 0.85,
    "universita-ricerca.html": 0.85,
    "finanziamenti.html": 0.85,
    "assessment.html": 0.85,
    "chi-siamo.html": 0.8,
    "listino-unitree.html": 0.75,
    "lp-quadrupedi.html": 0.8,
    "lp-umanoidi.html": 0.8,
    "lp-amr.html": 0.8,
    "lp-cobot.html": 0.8,
    "r1-d.html": 0.75,
}

CHANGEFREQ = {
    "index.html": "weekly",
    "catalogo-unitree.html": "weekly",
    "listino-unitree.html": "weekly",
}


def is_noindex(text: str) -> bool:
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', text, re.I)
    if not m:
        return False
    return "noindex" in m.group(1).lower()


def priority_for(path: Path) -> str:
    name = path.name
    if name in PRIORITY:
        return f"{PRIORITY[name]:.1f}"
    if path.parent.name == "prodotti" and name.startswith("unitree-"):
        return "0.8"
    if path.parent.name == "prodotti" and name.startswith("amr-"):
        return "0.85"
    if path.parent.name == "prodotti" and name.startswith("cobot-"):
        return "0.85"
    if name.endswith("-policy.html") or name == "note-legali.html":
        return "0.3"
    return "0.6"


def changefreq_for(path: Path) -> str:
    return CHANGEFREQ.get(path.name, "monthly")


def collect_urls() -> list[tuple[str, str, str]]:
    today = date.today().isoformat()
    urls: list[tuple[str, str, str]] = []

    for html in sorted(ROOT.rglob("*.html")):
        rel = html.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if rel.name.startswith("_"):
            continue
        if rel.name in EXCLUDE_FILES:
            continue
        text = html.read_text(encoding="utf-8", errors="replace")
        if is_noindex(text):
            continue
        loc = SITE + "/" + rel.as_posix().replace("index.html", "").rstrip("/")
        if loc.endswith("/") and not loc.endswith("://"):
            loc = loc.rstrip("/") or SITE + "/"
        if rel.name == "index.html" and len(rel.parts) == 1:
            loc = SITE + "/"
        urls.append((loc, changefreq_for(html), priority_for(html)))

    # dedupe preserving order
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for loc, cf, pr in urls:
        if loc in seen:
            continue
        seen.add(loc)
        out.append((loc, cf, pr))
    return out


def build_xml(urls: list[tuple[str, str, str]]) -> str:
    today = date.today().isoformat()
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for loc, cf, pr in urls:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = loc
        SubElement(url, "lastmod").text = today
        SubElement(url, "changefreq").text = cf
        SubElement(url, "priority").text = pr
    raw = tostring(urlset, encoding="unicode")
    return minidom.parseString(raw).toprettyxml(indent="  ")


def main() -> None:
    urls = collect_urls()
    xml = build_xml(urls)
    out = ROOT / "sitemap.xml"
    out.write_text(xml, encoding="utf-8")
    print(f"Scritto {out} — {len(urls)} URL")


if __name__ == "__main__":
    main()
