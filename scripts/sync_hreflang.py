"""Rende reciproci gli hreflang: ogni pagina di un gruppo di traduzioni elenca TUTTE le versioni esistenti.
I gruppi si ricavano dai link hreflang gia' presenti (componenti connesse). Salta pagine noindex o con
canonical diverso da se' stesse. x-default = valore piu' comune nel gruppo. Idempotente.
Uso: python scripts/sync_hreflang.py [--dry]"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://abrarobotics.com/"
LANGS = {"en", "de", "fr", "es", "pl", "nl", "cs", "sv", "da", "no", "fi"}
TAG = re.compile(r'[ \t]*<link[^>]*hreflang=[^>]*>[ \t]*\n?')
ORDER = ["it", "en", "de", "fr", "es", "pl", "nl", "cs", "sv", "da", "nb", "fi"]


def lang_of(rel):
    first = rel.split("/")[0]
    return ("nb" if first == "no" else first) if first in LANGS and "/" in rel else "it"


def url_to_rel(u):
    r = u.replace(BASE, "")
    return r if r and not r.endswith("/") else r + "index.html"


def head(t):
    return t.split("</head>", 1)[0]


def eligible(h, rel):
    if re.search(r'<meta[^>]*name="robots"[^>]*noindex', h, re.I) or 'http-equiv="refresh"' in h:
        return False
    m = re.search(r'<link[^>]*canonical[^>]*href="([^"]+)"', h) or re.search(r'<link[^>]*href="([^"]+)"[^>]*canonical', h)
    return not m or url_to_rel(m.group(1)) == rel


def main(dry):
    pages, links, parent, canon = {}, {}, {}, {}
    for p in ROOT.glob("**/*.html"):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "node_modules/")):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        h = head(t)
        tags = re.findall(r'<link[^>]*hreflang=[^>]*>', h)
        if not tags:
            continue
        pages[rel] = (p, t, eligible(h, rel))
        m = re.search(r'<link[^>]*canonical[^>]*href="([^"]+)"', h) or re.search(r'<link[^>]*href="([^"]+)"[^>]*canonical', h)
        canon[rel] = m.group(1) if m else BASE + rel
        links[rel] = {re.search(r'hreflang="([^"]+)"', x).group(1): url_to_rel(re.search(r'href="([^"]+)"', x).group(1)) for x in tags}
        parent[rel] = rel

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for rel, d in links.items():
        for tgt in d.values():
            if tgt in pages:
                parent[find(tgt)] = find(rel)
    groups = {}
    for rel in pages:
        groups.setdefault(find(rel), []).append(rel)
    changed = 0
    for members in groups.values():
        ok = [m for m in members if pages[m][2]]
        if len(ok) < 2:
            continue
        bylang = {}
        for m in sorted(ok, key=lambda r: (r.count("/"), r)):
            bylang.setdefault(lang_of(m), m)
        xd = Counter(links[m].get("x-default") for m in ok if links[m].get("x-default") in pages and pages[links[m]["x-default"]][2])
        xdef = bylang.get("it") or (xd.most_common(1)[0][0] if xd else bylang.get("en"))
        lines = [f'<link href="{canon[bylang[l]]}" hreflang="{l}" rel="alternate"/>' for l in ORDER if l in bylang]
        lines.append(f'<link href="{canon[xdef]}" hreflang="x-default" rel="alternate"/>')
        block = "\n".join(lines) + "\n"
        for m in ok:
            p, t, _ = pages[m]
            hd, sep, rest = t.partition("</head>")
            first = TAG.search(hd)
            new = TAG.sub("", hd)
            new = new[:first.start()] + block + new[first.start():]
            if new != hd:
                changed += 1
                if not dry:
                    p.write_text(new + sep + rest, encoding="utf-8")
    print(("da modificare" if dry else "modificate"), changed, "pagine,", len(groups), "gruppi")


main("--dry" in sys.argv)
