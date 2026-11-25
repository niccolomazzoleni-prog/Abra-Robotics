#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sezioni video delle applicazioni, schema VideoObject e sitemap-video.xml.

Unica fonte: data/video-libreria.json (video, testi e pagine in cui compaiono).
- In ogni pagina di "sezioni" scrive il blocco tra <!-- vlib:start --> e <!-- vlib:end -->
  (video con data-src e poster, lazy load in assets/video-lib.js, JSON-LD VideoObject).
  Se il blocco manca (per esempio dopo che genera_hub_modelli.py ha riscritto la pagina)
  lo reinserisce prima del segnaposto "prima_di", che deve comparire una sola volta.
- In applicazioni.html scrive la griglia delle pagine applicazione (<!-- vlib-app:... -->).
- Scrive sitemap-video.xml: ogni video compare una volta, sulla sua pagina principale.
Idempotente. Uso: python3 scripts/genera_video.py
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://abrarobotics.com"
DATA = json.loads((ROOT / "data" / "video-libreria.json").read_text(encoding="utf-8"))
VIDEO = DATA["video"]
UPLOAD = DATA["data_caricamento"]
APP = {a["pagina"]: a for a in DATA["applicazioni"]}
START, END = "<!-- vlib:start -->", "<!-- vlib:end -->"
ASTART, AEND = "<!-- vlib-app:start -->", "<!-- vlib-app:end -->"
ASSETS = '<link rel="stylesheet" href="assets/video-lib.css"/><script defer src="assets/video-lib.js"></script>'


def e(s: str) -> str:
    return html.escape(s, quote=True)


def mmss(s: int) -> str:
    return f"{s // 60}:{s % 60:02d}"


def iso(s: int) -> str:
    m, r = divmod(s, 60)
    return f"PT{m}M{r}S" if m else f"PT{r}S"


def video_ld(slug: str) -> dict:
    v = VIDEO[slug]
    return {
        "@type": "VideoObject",
        "@id": f"{SITE}/videos/applicazioni/{slug}.mp4#video",
        "name": v["titolo"],
        "description": v["descrizione"],
        "thumbnailUrl": f"{SITE}/images/video/{slug}.webp",
        "uploadDate": UPLOAD,
        "duration": iso(v["secondi"]),
        "contentUrl": f"{SITE}/videos/applicazioni/{slug}.mp4",
        "inLanguage": "it",
        "publisher": {"@id": f"{SITE}/#organization"},
    }


def card(slug: str) -> str:
    v = VIDEO[slug]
    meta = " · ".join(x for x in (v["tipo"], mmss(v["secondi"]), v["nota"]) if x)
    muted = "" if v["nota"] == "con audio" else " muted"
    return (
        f'<figure class="vlib-card"><video controls{muted} playsinline preload="none" width="1280" height="720" '
        f'data-src="videos/applicazioni/{slug}.mp4" poster="images/video/{slug}.webp" aria-label="{e(v["titolo"])}"></video>'
        f'<figcaption><strong>{e(v["titolo"])}</strong><span>{e(v["descrizione"])}</span><small>{e(meta)}</small></figcaption></figure>'
    )


def links(page: str) -> str:
    altre = [a for p, a in APP.items() if p != page]
    lab = "Altre applicazioni in video" if page in APP else "Le applicazioni in video"
    return f'<p class="vlib-links"><span>{lab}:</span> ' + " ".join(
        f'<a href="{a["pagina"]}">{e(a["nome"])}</a>' for a in altre) + ' <a href="applicazioni.html">Tutte le applicazioni</a></p>'


def section(page: str, cfg: dict) -> str:
    ld = {"@context": "https://schema.org", "@graph": [video_ld(s) for s in cfg["video"]]}
    body = "".join(card(s) for s in cfg["video"])
    extra = links(page) if (cfg.get("link") or page in APP) else ""
    return (
        f'{START}\n<section class="vlib-sec" id="video"><div class="vlib-wrap">'
        f'<p class="vlib-k">Video</p><h2>{e(cfg["titolo"])}</h2><p class="vlib-lead">{e(cfg["intro"])}</p>'
        f'<div class="vlib-grid">{body}</div>{extra}</div></section>\n'
        f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n{ASSETS}\n{END}\n'
    )


def put(text: str, block: str, start: str, end: str, anchor: str | None, page: str) -> str:
    if start in text:
        a, b = text.index(start), text.index(end) + len(end)
        if text[b:b + 1] == "\n":
            b += 1
        return text[:a] + block + text[b:]
    if not anchor or text.count(anchor) != 1:
        sys.exit(f"{page}: blocco assente e segnaposto {anchor!r} non unico")
    i = text.index(anchor)
    return text[:i] + block + text[i:]


def app_grid() -> str:
    cards = "".join(
        f'<a class="vlib-app" href="{a["pagina"]}"><img src="images/video/{a["poster"]}.webp" alt="{e(a["nome"])}" '
        f'width="1280" height="720" loading="lazy"/><span>{e(a["nome"])}</span></a>' for a in DATA["applicazioni"])
    return (
        f'{ASTART}\n<section class="page-sec"><div class="wrap"><h2 class="h2 reveal">Le applicazioni in video.</h2>'
        f'<p class="lead reveal">Simulazioni sul digital twin di celle e reparti: cosa fa il robot, passo per passo.</p>'
        f'<div class="vlib-apps">{cards}</div></div></section>\n{ASSETS}\n{AEND}\n'
    )


def sitemap() -> str:
    by_page: dict[str, list[str]] = {}
    for slug, v in VIDEO.items():
        by_page.setdefault(v["pagina"], []).append(slug)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">']
    for page, slugs in by_page.items():
        out.append(f"  <url>\n    <loc>{SITE}/{page}</loc>")
        for s in slugs:
            v = VIDEO[s]
            out.append(
                "    <video:video>\n"
                f"      <video:thumbnail_loc>{SITE}/images/video/{s}.webp</video:thumbnail_loc>\n"
                f"      <video:title>{escape(v['titolo'])}</video:title>\n"
                f"      <video:description>{escape(v['descrizione'])}</video:description>\n"
                f"      <video:content_loc>{SITE}/videos/applicazioni/{s}.mp4</video:content_loc>\n"
                f"      <video:duration>{v['secondi']}</video:duration>\n"
                f"      <video:publication_date>{UPLOAD}</video:publication_date>\n"
                "      <video:family_friendly>yes</video:family_friendly>\n"
                "    </video:video>")
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main() -> None:
    for slug in VIDEO:
        for p in (ROOT / "videos" / "applicazioni" / f"{slug}.mp4", ROOT / "images" / "video" / f"{slug}.webp"):
            if not p.is_file():
                sys.exit(f"manca {p.relative_to(ROOT)}")
    written = []
    for page, cfg in DATA["sezioni"].items():
        path = ROOT / page
        text = path.read_text(encoding="utf-8")
        new = put(text, section(page, cfg), START, END, cfg.get("prima_di"), page)
        if new != text:
            path.write_text(new, encoding="utf-8")
            written.append(page)
    path = ROOT / "applicazioni.html"
    text = path.read_text(encoding="utf-8")
    new = put(text, app_grid(), ASTART, AEND,
              '<section class="page-sec"><div class="wrap"><h2 class="h2 reveal">Dove la robotica', "applicazioni.html")
    if new != text:
        path.write_text(new, encoding="utf-8")
        written.append("applicazioni.html")
    (ROOT / "sitemap-video.xml").write_text(sitemap(), encoding="utf-8")
    print("video:", len(VIDEO), "· pagine aggiornate:", " ".join(written) or "nessuna")


if __name__ == "__main__":
    main()
