#!/usr/bin/env python3
"""Blocco "Prodotti correlati" (link statici) in ogni scheda prodotto italiana.

Collega ogni scheda alle altre versioni dello stesso robot e ai suoi accessori,
cosi' Google trova tutte le schede scorrendo il sito e il visitatore ha il
passo successivo. Idempotente: riscrive solo il blocco tra i marcatori.
Uso: python3 scripts/genera_correlati.py  (lanciato anche da regenerate_from_public.py)"""
from __future__ import annotations

import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from miniature import HEIGHT, WIDTH, thumb_src  # noqa: E402
PROD = ROOT / "prodotti"
START, END = "<!-- CORRELATI -->", "<!-- /CORRELATI -->"
MAX_LINKS = 8
CSS_START, CSS_END = "/* CORRELATI:START */", "/* CORRELATI:END */"
CSS = """.correlati{padding:48px 0;border-top:1px solid var(--gray-200,#e5e5e5)}
.correlati h2{font-size:1.4rem;margin:0 0 20px}
.correlati .rel-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.correlati .rel-card{display:flex;flex-direction:column;height:100%;box-sizing:border-box;border:1px solid var(--gray-200,#e5e5e5);border-radius:16px;overflow:hidden;background:#fff;color:var(--black,#0a0a0a);text-decoration:none;transition:border-color .15s,box-shadow .15s,transform .15s}
.correlati .rel-card:hover,.correlati .rel-card:focus-visible{border-color:var(--black,#0a0a0a);box-shadow:0 8px 24px rgba(0,0,0,.07);transform:translateY(-2px)}
.correlati .rel-media{display:block;position:relative;overflow:hidden;aspect-ratio:4/3;background:var(--gray-50,#fafafa);border-bottom:1px solid var(--gray-100,#f5f5f5)}
.correlati .rel-media img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:contain;padding:12px;box-sizing:border-box}
.correlati .rel-body{display:flex;flex-direction:column;gap:3px;padding:12px 14px 14px;flex:1}
.correlati .rel-tag{font-size:.8rem;line-height:1.2;color:#6b6b6b}
.correlati .rel-name{font-size:.95rem;font-weight:500;line-height:1.3;color:var(--black,#0a0a0a)}
.correlati .rel-price{margin-top:auto;padding-top:6px;font-size:1rem;font-weight:600;color:var(--black,#0a0a0a)}
.correlati .rel-all{margin:20px 0 0;font-size:.95rem}
.correlati .rel-all a{color:var(--black,#0a0a0a);font-weight:500;text-decoration:underline;text-underline-offset:3px}
@media (max-width:960px){.correlati .rel-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:640px){.correlati{padding:36px 0}
.correlati .rel-grid{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain;padding-bottom:6px;scrollbar-width:none}
.correlati .rel-grid::-webkit-scrollbar{display:none}
.correlati .rel-grid>li{flex:0 0 70%;max-width:260px;scroll-snap-align:start}
.correlati .rel-tag{font-size:14px}.correlati .rel-name{font-size:15px}.correlati .rel-price{font-size:16px}}"""


def family(name: str) -> str:
    first = name.upper().replace("UNITREE ", "").split()[0].rstrip("-/")
    m = re.match(r"([A-Z]{1,3}\d{1,2})", first)
    return m.group(1) if m else first


SMALL = {"di", "da", "con", "a", "e", "per", "lunga", "in", "del", "della", "su", "senza", "scheda", "batteria", "caricabatterie",
         "caricatore", "modulo", "telecomando", "rapido", "standard", "autonomia", "ricarica", "espansione", "calcolo", "schermo",
         "mano", "pinza", "braccio", "base", "kit", "telecamera", "profondità", "supporto", "cavo", "alimentatore"}
UPPER = {"edu": "EDU", "lidar": "LiDAR", "mah": "mAh", "usb": "USB", "uwb": "UWB", "agx": "AGX", "nx": "NX", "vr": "VR",
         "d435i": "D435i", "d405": "D405", "xt16": "XT16", "go2": "Go2", "go2-w": "Go2-W", "dfq": "DFQ", "ftp": "FTP", "rtk": "RTK", "gps": "GPS", "dof": "DoF", "expansion": "Expansion"}


def nice_fam(fam: str) -> str:
    return UPPER.get(fam.lower(), fam)


VARIANT_WORDS = {"standard", "ultimate", "professional", "smart", "flagship", "plus", "basic"}


def label(name: str) -> str:
    out = []
    for i, raw in enumerate(name.split()):
        pre, w, post = re.match(r"^([(\[]*)(.*?)([)\],.]*)$", raw).groups()
        lw = w.lower()
        if lw in UPPER:
            w = UPPER[lw]
        elif re.fullmatch(r"[a-z]{1,3}\d{1,3}[a-z]?(-[a-z0-9]+)?", lw):
            w = w.upper()
        elif re.fullmatch(r"\d+[a-z]+", lw):
            w = lw.upper().replace("TFLOPS", " TFLOPS").replace("TOPS", " TOPS")
        elif len(w) == 1 and w.isupper() and i and re.sub(r"\W", "", name.split()[i - 1]).lower() in VARIANT_WORDS:
            pass  # lettera di versione Unitree: "Standard A", "Ultimate E"
        elif lw in VARIANT_WORDS and i + 1 < len(name.split()) and re.fullmatch(r"[A-Z][),]*", name.split()[i + 1]):
            w = w[:1].upper() + w[1:].lower()
        elif i and lw in SMALL:
            w = lw
        else:
            w = w[:1].upper() + w[1:].lower()
        out.append(pre + w + post)
    return re.sub(r"([–-])([a-z])(\d)", lambda m: m.group(1) + m.group(2).upper() + m.group(3), " ".join(out))


def eur(x) -> str:
    return f"{x:,.0f}".replace(",", ".")


# "Vedi tutti": pagina hub della famiglia (percorso, nome mostrato; None = nome famiglia)
HUB = {"G1": ("../umanoidi.html#fam-g1", None), "H2": ("../umanoidi.html#fam-h2", None), "R1": ("../umanoidi.html#fam-r1", None),
       "GO2": ("../quadrupedi.html#fam-go2", "Go2"), "AS2": ("../quadrupedi.html#fam-as2", None), "A2": ("../quadrupedi.html#fam-a2", None),
       "B2": ("../quadrupedi.html#fam-b2", None), "Cobot Fairino": ("../cobot.html", "cobot Fairino"), "AMR": ("../amr.html", "AMR")}
TAG = {"UMANOIDI": "Configurazione", "COMPONENTISTICA": "Ricambio", "MANI_BRACCI": "Accessorio", "ACC": "Accessorio"}


def card(x: dict) -> str:
    name = html.escape(x["name"] if x.get("plain") else label(x["name"]))
    tag = x.get("tag") or TAG.get(x["cat"], "")
    if tag.lower() in x["name"].lower():  # "(Ricambio)" gia' nel nome: niente etichetta doppia
        tag = ""
    img = thumb_src(x.get("img") or "", "../")
    media = (f'<span class="rel-media"><img src="{html.escape(img)}" alt="{name}" width="{WIDTH}" height="{HEIGHT}" '
             f'loading="lazy" decoding="async"></span>') if img else '<span class="rel-media"></span>'
    price = f'<span class="rel-price">da {eur(x["price"])} €</span>' if x["price"] else ""
    return (f'<li><a class="rel-card" href="{x["slug"]}">{media}<span class="rel-body">'
            + (f'<span class="rel-tag">{tag}</span>' if tag else "") + f'<span class="rel-name">{name}</span>{price}</span></a></li>')


def main() -> None:
    items = json.loads((ROOT / "listini" / "pubblico" / "end-user.json").read_text(encoding="utf-8"))
    rows = []
    for v in items.values():
        slug = v.get("slug")
        f = PROD / (slug or "_")
        if not slug or not f.is_file() or 'http-equiv="refresh"' in f.read_text(encoding="utf-8"):
            continue
        rows.append({"slug": slug, "name": v.get("nome", ""), "fam": family(v.get("nome", "")), "cat": v.get("categoria"), "price": v.get("prezzo_eur"), "img": v.get("immagine")})
    # cobot Fairino e AMR non sono nel listino Unitree: famiglie dai loro dati
    for data, fam in (("cobot-products.json", "Cobot Fairino"), ("amr-products.json", "AMR")):
        try:
            prods = json.loads((ROOT / "data" / data).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for v in prods:
            fn = v.get("filename")
            if fn and (PROD / fn).is_file():
                rows.append({"slug": fn, "name": v.get("title", fn), "fam": fam, "cat": "UMANOIDI" if v.get("group", "robot") == "robot" else "ACC",
                             "price": v.get("price_eur"), "plain": True, "img": v.get("image"),
                             "tag": "Modello" if v.get("group", "robot") == "robot" else "Accessorio"})
    by_fam = defaultdict(list)
    for r in rows:
        by_fam[r["fam"]].append(r)
    done = 0
    for r in rows:
        f = PROD / r["slug"]
        s = f.read_text(encoding="utf-8")
        same = [x for x in by_fam[r["fam"]] if x["slug"] != r["slug"]]
        robots = [x for x in same if x["cat"] == "UMANOIDI"]
        acc = [x for x in same if x["cat"] != "UMANOIDI"]
        # un robot mostra prima gli accessori, un accessorio prima i robot compatibili
        pick = (acc + robots) if r["cat"] == "UMANOIDI" else (robots + acc)
        pick = sorted(pick[:40], key=lambda x: (x["cat"] == r["cat"], x["price"] or 0))[:MAX_LINKS]
        if not pick:
            continue
        title = f"Altri {html.escape(r['fam'])}" if r.get("plain") else (f"Altri prodotti {html.escape(nice_fam(r['fam']))}" if r["fam"] else "Prodotti correlati")
        lis = "\n".join(card(x) for x in pick)
        tutti = ""
        hub = HUB.get(r["fam"])
        if hub and len(same) > len(pick):
            tutti = f'\n<p class="rel-all"><a href="{hub[0]}">Vedi tutti i prodotti {html.escape(hub[1] or nice_fam(r["fam"]))} ({len(same)})</a></p>'
        block = (f'{START}\n<section class="correlati"><div class="container">\n<h2>{title}</h2>\n<ul class="rel-grid">\n{lis}\n</ul>'
                 f'{tutti}\n</div></section>\n{END}')
        if START in s:
            n = re.sub(re.escape(START) + r"[\s\S]*?" + re.escape(END), lambda m: block, s, count=1)
        elif '<footer class="footer"' in s:
            n = s.replace('<footer class="footer"', block + '\n<footer class="footer"', 1)
        else:
            continue
        # CSS: nelle schede con product.css sta li'; le poche schede con stile proprio tengono il blocco inline
        n = re.sub(r'\s*<style id="correlati-css">[\s\S]*?</style>', "", n)
        if 'href="product.css' not in n:
            n = n.replace("</head>", f'<style id="correlati-css">{CSS}</style>\n</head>', 1)
        if n != s:
            f.write_text(n, encoding="utf-8")
            done += 1
    css = PROD / "product.css"
    t = css.read_text(encoding="utf-8")
    blocco = f"{CSS_START}\n{CSS}\n{CSS_END}"
    if CSS_START in t:
        t2 = re.sub(re.escape(CSS_START) + r"[\s\S]*?" + re.escape(CSS_END), lambda m: blocco, t)
    else:
        t2 = t.rstrip("\n") + "\n\n" + blocco + "\n"
    if t2 != t:
        css.write_text(t2, encoding="utf-8")
    print(f"correlati: {done} schede aggiornate su {len(rows)}")


if __name__ == "__main__":
    main()
