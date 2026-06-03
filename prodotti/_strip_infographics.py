#!/usr/bin/env python3
"""Sulle schede umanoidi: rimuove i frame infografici RoboStore (img-02..05).
  - elimina il blocco gallery-thumbs e le frecce gallery-nav (resta la sola foto principale)
  - sostituisce ovunque img-02..05 con la foto rebrandizzata pulita (img-01-abra / g1-01-abra)
"""
import re, glob, os

PAGES = [
    "unitree-g1.html",
    "unitree-g1-edu-standard.html", "unitree-g1-edu-plus.html",
    "unitree-g1-edu-ultimate-a.html", "unitree-g1-edu-ultimate-b.html",
    "unitree-g1-edu-ultimate-c.html", "unitree-g1-edu-ultimate-d.html",
    "unitree-g1-edu-ultimate-e.html", "unitree-g1-edu-ultimate-f.html",
]

re_thumbs = re.compile(
    r'\s*<div class="gallery-thumbs">\s*(?:<div class="gallery-thumb[^>]*>\s*<img[^>]*>\s*</div>\s*)+</div>',
    re.S)
re_nav = re.compile(
    r'\s*<div class="gallery-nav">\s*<button[^>]*>[^<]*</button>\s*<button[^>]*>[^<]*</button>\s*</div>',
    re.S)

for p in PAGES:
    if not os.path.exists(p):
        print("  ! manca", p); continue
    t = open(p, encoding="utf-8").read()
    orig = t
    t, n_th = re_thumbs.subn("", t)
    t, n_nav = re_nav.subn("", t)
    # sostituzione immagini infografiche con la foto pulita rebrandizzata
    t = re.sub(r'(variants/g1-u\d+/)img-0[2-5]\.jpg', r'\1img-01-abra.jpg', t)
    t = re.sub(r'(images/)g1-0[2-5]\.jpg', r'\1g1-01-abra.jpg', t)
    left = len(re.findall(r'img-0[2-5]\.jpg|g1-0[2-5]\.jpg', t))
    if t != orig:
        open(p, "w", encoding="utf-8").write(t)
    print(f"  {p}: thumbs_rimossi={n_th} nav_rimossi={n_nav} ref_infografiche_residue={left}")

print("Fatto.")
