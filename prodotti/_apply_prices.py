#!/usr/bin/env python3
"""Applica i prezzi End-User -5% alle schede prodotto (prezzo visibile + schema JSON-LD).
I prodotti senza prezzo confermato vengono lasciati BIANCHI (prezzo vuoto).
"""
import re, os

def it(v):
    s = f"{v:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

# pagina -> prezzo End-User -5% (None = lasciare bianco)
PRICES = {
    "unitree-g1.html": 22797.54,
    "unitree-g1-edu-standard.html": 35684.39,
    "unitree-g1-edu-plus.html": 43494.61,
    "unitree-g1-edu-ultimate-a.html": 47965.43,
    "unitree-g1-edu-ultimate-b.html": 59115.04,
    "unitree-g1-edu-ultimate-c.html": 59115.04,
    "unitree-g1-edu-ultimate-d.html": 64321.85,
    "unitree-g1-edu-ultimate-e.html": 53908.23,
    "unitree-g1-edu-ultimate-f.html": None,   # U8 - non in listino, bianco
    "unitree-g1-comp.html": 39589.50,
    "unitree-r1-edu.html": 30672.84,
    "unitree-go2-pro.html": 3841.57,
    "unitree-go2-edu.html": 12159.51,
    "unitree-go2-edu-plus.html": 14677.56,
    "unitree-go2-enterprise-u2.html": None,   # da confermare, bianco
    "unitree-a2.html": 29116.06,
    "unitree-a2-pro.html": 39589.50,
    "unitree-b2.html": 74056.52,
}

for page, price in PRICES.items():
    if not os.path.exists(page):
        print("  ! manca", page); continue
    t = open(page, encoding="utf-8").read()
    if price is None:
        vis, sch = "", ""
        tag = "BIANCO"
    else:
        vis, sch = f"{it(price)} €", f"{price:.2f}"
        tag = vis
    t, nv = re.subn(r'(<span class="buy-box-amount">)[^<]*(</span>)', lambda m: m.group(1)+vis+m.group(2), t)
    t, ns = re.subn(r'("price":\s*")[^"]*(")', lambda m: m.group(1)+sch+m.group(2), t)
    open(page, "w", encoding="utf-8").write(t)
    print(f"  {page}: {tag}  (visibile={nv}, schema={ns})")

print("Fatto.")
