#!/usr/bin/env python3
"""Correzioni SEO on-page (ottobre 2026), idempotente. Uso: python3 scripts/seo_fix_ottobre.py"""
from __future__ import annotations
import html as H, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_title_desc import seo_title, seo_desc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://abrarobotics.com/"
SKIP = {".claude", "node_modules", "admin", "editor", "offerte-ai", "stripe", "apps-script", "scripts", "docs"}
TITLES = {  # pagine principali oltre 60 caratteri
    "index.html": "Robot Unitree in Italia: prezzi G1, H2, AS2, Go2 | Abra",
    "lp-amr.html": "Robot AMR in Italia: movimentazione interna | Abra",
    "lp-unitree.html": "Robot Unitree in Italia: umanoidi e quadrupedi | Abra",
    "software.html": "Software custom per robot Unitree | Abra Robotics",
    "lp-quadrupedi.html": "Robot quadrupedi in Italia: modelli e prezzi | Abra",
    "blog/unitree-g1-guida-operativa.html": "Unitree G1: accensione, telecomando e rete | Abra",
    "blog/unitree-italia-guida-completa.html": "Unitree in Italia: guida 2026 a modelli e prezzi | Abra",
    "en/index-en.html": "Unitree robots in Italy: G1, H2, AS2, Go2 prices | Abra",
}
CANONICAL = {  # duplicati -> pagina di riferimento
    "prodotti/unitree-g1d-standard.html": "prodotti/unitree-g1-d-standard.html",
    "prodotti/unitree-g1d-flagship.html": "prodotti/unitree-g1-d-flagship.html",
    "lp-umanoidi-v1.html": "lp-umanoidi.html",
    "en/lp-umanoidi-v1-en.html": "en/lp-umanoidi-en.html",
}
NOINDEX = ["restyle-preview.html", "index-zenixa.html"]
TAIL_IT = "Prezzo, specifiche e disponibilità in Italia con Abra Robotics."
TAIL_EN = "Price, specs and availability in Italy from Abra Robotics."

import subprocess


def original_title(rel: str) -> str | None:
    """Title della versione su main prima di queste correzioni (per ricalcolare senza perdere parole)."""
    try:
        old = subprocess.run(["git", "show", f"main:{rel}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    m = re.search(r"<title>(.*?)</title>", old, re.S)
    return H.unescape(m.group(1).strip()) if m else None


stats = {k: 0 for k in ("title", "desc", "canonical", "og", "noindex")}
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT).as_posix()
    if rel.split("/")[0] in SKIP or f.name.startswith("_"):
        continue
    s = o = f.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s:
        continue
    en = rel.startswith("en/")
    # title
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if m:
        cur = H.unescape(m.group(1).strip())
        orig = original_title(rel) or cur
        new = TITLES.get(rel)
        if not new and (len(orig) > 60 or len(cur) < len(orig) - 20):
            base = re.sub(r"\s*\|\s*Abra( Robotics)?\s*$", "", orig)
            new = seo_title(base)
        if new and new != cur:
            s = s.replace(m.group(0), f"<title>{H.escape(new, quote=False)}</title>", 1)
            stats["title"] += 1
    # meta description
    m = re.search(r'(<meta[^>]*name="description"[^>]*content=")([^"]*)(")', s) or re.search(r'(<meta[^>]*content=")([^"]*)("[^>]*name="description")', s)
    if m:
        cur = H.unescape(m.group(2))
        new = seo_desc(cur, TAIL_EN if en else TAIL_IT)
        if new != cur:
            s = s.replace(m.group(0), m.group(1) + H.escape(new, quote=True) + m.group(3), 1)
            stats["desc"] += 1
    # canonical dei duplicati
    if rel in CANONICAL:
        target = SITE + CANONICAL[rel]
        s2 = re.sub(r'(<link[^>]*rel="canonical"[^>]*href=")[^"]*(")', r"\g<1>" + target + r"\2", s)
        s2 = re.sub(r'(<link[^>]*href=")[^"]*("[^>]*rel="canonical")', r"\g<1>" + target + r"\2", s2)
        if s2 != s:
            s = s2; stats["canonical"] += 1
    # noindex pagine di prova
    if rel in NOINDEX and 'name="robots"' not in s:
        s = s.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow"/>', 1); stats["noindex"] += 1
    # Open Graph mancante
    if 'property="og:title"' not in s and 'name="robots" content="noindex' not in s:
        t = H.unescape((re.search(r"<title>(.*?)</title>", s, re.S) or [None, ""])[1]).strip()
        d = H.unescape((re.search(r'name="description"[^>]*content="([^"]*)"', s) or re.search(r'content="([^"]*)"[^>]*name="description"', s) or [None, ""])[1])
        c = (re.search(r'rel="canonical"[^>]*href="([^"]*)"', s) or re.search(r'href="([^"]*)"[^>]*rel="canonical"', s) or [None, SITE + rel])[1]
        img = re.search(r'<img[^>]*src="([^"]+\.(?:png|jpe?g|webp))"', s.split("</nav>", 1)[-1])
        if img:
            src = img.group(1)
            src = src if src.startswith("http") else SITE + str(Path(rel).parent / src).replace("\\", "/")
            src = re.sub(r"[^/]+/\.\./", "", src).replace("/./", "/")
        else:
            src = SITE + "images/logo.png"
        og = (f'<meta property="og:type" content="{"article" if rel.startswith("blog/") else "website"}"/>\n'
              f'<meta property="og:site_name" content="Abra Robotics"/>\n'
              f'<meta property="og:title" content="{H.escape(t)}"/>\n'
              f'<meta property="og:description" content="{H.escape(d)}"/>\n'
              f'<meta property="og:url" content="{c}"/>\n'
              f'<meta property="og:image" content="{src}"/>\n'
              f'<meta property="og:locale" content="{"en_GB" if en else "it_IT"}"/>\n'
              f'<meta name="twitter:card" content="summary_large_image"/>\n')
        s = s.replace("</head>", og + "</head>", 1); stats["og"] += 1
    if s != o:
        f.write_text(s, encoding="utf-8")
print(stats)
