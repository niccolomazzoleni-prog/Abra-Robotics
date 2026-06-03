#!/usr/bin/env python3
"""Sostituisce il collage parallax (4 foto uguali) con una griglia di card a sfondo
scuro che evidenziano le spec, riusando i valori gia' presenti nelle caption.
"""
import re, os

PAGES = [
    "unitree-g1.html",
    "unitree-g1-edu-standard.html", "unitree-g1-edu-plus.html",
    "unitree-g1-edu-ultimate-a.html", "unitree-g1-edu-ultimate-b.html",
    "unitree-g1-edu-ultimate-c.html", "unitree-g1-edu-ultimate-d.html",
    "unitree-g1-edu-ultimate-e.html", "unitree-g1-edu-ultimate-f.html",
]

START = '<div class="parallax-cols"'

def matched_block(html, start):
    """Ritorna (i, j) del blocco div bilanciato che inizia a `start`."""
    i = html.find(start)
    if i < 0:
        return None
    depth = 0
    for m in re.finditer(r'<div\b|</div>', html[i:]):
        depth += 1 if m.group().startswith('<div') else -1
        if depth == 0:
            return i, i + m.end()
    return None

for p in PAGES:
    if not os.path.exists(p):
        print("  ! manca", p); continue
    html = open(p, encoding="utf-8").read()
    span = matched_block(html, START)
    if not span:
        print(f"  ! parallax non trovato in {p}"); continue
    i, j = span
    block = html[i:j]
    pairs = re.findall(
        r'parallax-caption-value">(.*?)</span>\s*<span class="parallax-caption-label">(.*?)</span>',
        block, re.S)
    if not pairs:
        print(f"  ! nessuna spec in {p}"); continue
    cards = "\n".join(
        f'          <div class="spec-card"><span class="spec-card-value">{v.strip()}</span>'
        f'<span class="spec-card-label">{l.strip()}</span></div>'
        for v, l in pairs)
    new = f'<div class="spec-cards">\n{cards}\n        </div>'
    html = html[:i] + new + html[j:]
    open(p, "w", encoding="utf-8").write(html)
    print(f"  OK {p}: {len(pairs)} card -> " + " | ".join(v.strip() for v, _ in pairs))

print("Fatto.")
