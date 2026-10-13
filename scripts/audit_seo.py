#!/usr/bin/env python3
"""Audit SEO di tutto il sito (pagine indicizzabili): title/description/h1, canonical, hreflang reciproci,
link interni rotti, immagini senza alt, duplicati, sitemap vs pagine. Uso: python3 scripts/audit_seo.py [--dettagli]"""
from __future__ import annotations
import collections, html as H, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SITE = "https://abrarobotics.com"
SKIP_DIRS = {".claude", ".git", "node_modules", "admin", "editor", "offerte-ai", "fonts", "listini", "stripe", "apps-script", "lp-thank-you", "lp-thank-you-en", "__pycache__"}

def pages():
    for p in ROOT.rglob("*.html"):
        if set(p.relative_to(ROOT).parts) & SKIP_DIRS:
            continue
        yield p

def url_of(p):
    rel = p.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[:-10]
    return SITE + "/" + rel

def resolve(p, href):
    href = href.split("#")[0].split("?")[0]
    if not href or re.match(r"^(https?:|mailto:|tel:|data:|javascript:|//)", href):
        return None
    t = (ROOT / href.lstrip("/")) if href.startswith("/") else (p.parent / href)
    t = Path(str(t.resolve()))
    if href.endswith("/") or t.is_dir():
        t = t / "index.html"
    return t

issues = collections.defaultdict(list)
titles, descs = collections.defaultdict(list), collections.defaultdict(list)
alts = {}
indexable = {}
linked = set()
for p in pages():
    s = p.read_text(encoding="utf-8", errors="ignore")
    rel = p.relative_to(ROOT).as_posix()
    stub = 'http-equiv="refresh"' in s[:6000]
    noindex = bool(re.search(r'<meta[^>]*name="robots"[^>]*noindex|<meta[^>]*content="[^"]*noindex[^"]*"[^>]*name="robots"', s, re.I))
    for h in re.findall(r'(?:href|src)="([^"]+)"', s):
        t = resolve(p, h)
        if t is None:
            continue
        if not t.exists():
            issues["link rotto"].append(f"{rel} -> {h}")
        else:
            linked.add(t.resolve())
    if stub or noindex:
        continue
    indexable[p.resolve()] = rel
    t = re.search(r"<title>([\s\S]*?)</title>", s)
    t = H.unescape(t.group(1).strip()) if t else ""
    d = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', s) or re.search(r'<meta[^>]*content="([^"]*)"[^>]*name="description"', s)
    d = H.unescape(d.group(1).strip()) if d else ""
    if not t: issues["title mancante"].append(rel)
    elif len(t) > 65: issues["title lungo (>65)"].append(f"{rel} ({len(t)})")
    elif len(t) < 15: issues["title corto"].append(f"{rel} ({len(t)})")
    if not d: issues["description mancante"].append(rel)
    elif len(d) > 165: issues["description lunga (>165)"].append(f"{rel} ({len(d)})")
    elif len(d) < 50: issues["description corta"].append(f"{rel} ({len(d)})")
    titles[t].append(rel); descs[d].append(rel)
    body = re.sub(r"(?s)<(script|style|template)[^>]*>.*?</\1>", "", s)
    h1 = re.findall(r"<h1[\s>]", body)
    if len(h1) != 1: issues["h1 non unico"].append(f"{rel} ({len(h1)})")
    c = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', s) or re.search(r'<link[^>]*href="([^"]+)"[^>]*rel="canonical"', s)
    if not c: issues["canonical mancante"].append(rel)
    elif c.group(1) != url_of(p) and c.group(1) != url_of(p).replace("index.html", ""):
        issues["canonical verso altra pagina"].append(f"{rel} -> {c.group(1)}")
    for img in re.findall(r"<img\b[^>]*>", body):
        if not re.search(r'\balt="[^"]', img) and 'aria-hidden' not in img and 'role="presentation"' not in img:
            issues["immagine senza alt"].append(rel); break
    alts[rel] = dict((h, u) for h, u in re.findall(r'<link[^>]*hreflang="([^"]+)"[^>]*href="([^"]+)"', s) + [(h, u) for u, h in re.findall(r'<link href="([^"]+)" hreflang="([^"]+)"', s)])
for t, ps in titles.items():
    if t and len(ps) > 1: issues["title duplicato"].append(f"{t!r}: {', '.join(ps[:4])}{' ...' if len(ps) > 4 else ''}")
for d, ps in descs.items():
    if d and len(ps) > 1: issues["description duplicata"].append(f"{d[:60]!r}: {', '.join(ps[:4])}{' ...' if len(ps) > 4 else ''}")
# hreflang reciproci
own = {url_of(ROOT / r): r for r in alts}
for r, a in alts.items():
    me = url_of(ROOT / r)
    for h, u in a.items():
        if h == "x-default" or u == me: continue
        other = own.get(u) or own.get(u.rstrip("/") + "/")
        if not other:
            issues["hreflang verso pagina non indicizzabile o inesistente"].append(f"{r} -> {u}"); continue
        if me not in alts[other].values():
            issues["hreflang non reciproco"].append(f"{u} non cita {me}")
# sitemap
sm = set(re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8")))
idx_urls = {url_of(Path(p)): r for p, r in indexable.items()}
for u in sorted(sm - set(idx_urls)): issues["in sitemap ma non indicizzabile/inesistente"].append(u)
for u, r in sorted(idx_urls.items()):
    if u not in sm and not r.startswith(("lp-", "en/lp-")) and "-lc" not in r and "grazie" not in r: issues["indicizzabile ma non in sitemap"].append(r)
for p, r in indexable.items():
    if p not in linked and r not in ("index.html",): issues["pagina orfana (nessun link interno)"].append(r)
print(f"pagine indicizzabili: {len(indexable)}")
for k, v in sorted(issues.items(), key=lambda kv: -len(kv[1])):
    print(f"{len(v):5d}  {k}")
    if "--dettagli" in sys.argv:
        for x in v[:15]: print("        ", x)
