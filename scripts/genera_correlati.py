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
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROD = ROOT / "prodotti"
START, END = "<!-- CORRELATI -->", "<!-- /CORRELATI -->"
MAX_LINKS = 8
CSS = ('<style id="correlati-css">.correlati{padding:40px 0;border-top:1px solid var(--gray-200,#e5e5e5)}'
       '.correlati h2{font-size:1.3rem;margin:0 0 14px}.correlati ul{list-style:none;margin:0;padding:0;display:grid;'
       'grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:8px}.correlati li a{display:flex;justify-content:space-between;'
       'gap:10px;padding:10px 12px;border:1px solid var(--gray-200,#e5e5e5);border-radius:8px;color:var(--black,#0a0a0a);'
       'text-decoration:none;font-size:.92rem}.correlati li a:hover{border-color:var(--black,#0a0a0a)}'
       '.correlati li span{color:var(--gray-600,#525252);white-space:nowrap}</style>')


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
        elif i and lw in SMALL:
            w = lw
        else:
            w = w[:1].upper() + w[1:].lower()
        out.append(pre + w + post)
    return re.sub(r"([–-])([a-z])(\d)", lambda m: m.group(1) + m.group(2).upper() + m.group(3), " ".join(out))


def eur(x) -> str:
    return f"{x:,.0f}".replace(",", ".")


def main() -> None:
    items = json.loads((ROOT / "listini" / "pubblico" / "end-user.json").read_text(encoding="utf-8"))
    rows = []
    for v in items.values():
        slug = v.get("slug")
        f = PROD / (slug or "_")
        if not slug or not f.is_file() or 'http-equiv="refresh"' in f.read_text(encoding="utf-8"):
            continue
        rows.append({"slug": slug, "name": v.get("nome", ""), "fam": family(v.get("nome", "")), "cat": v.get("categoria"), "price": v.get("prezzo_eur")})
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
                             "price": v.get("price_eur"), "plain": True})
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
        lis = "\n".join(
            f'<li><a href="{x["slug"]}">{html.escape(x["name"] if x.get("plain") else label(x["name"]))}' + (f' <span>da {eur(x["price"])} €</span>' if x["price"] else "") + "</a></li>"
            for x in pick)
        block = f'{START}\n<section class="correlati"><div class="container">\n<h2>{title}</h2>\n<ul>\n{lis}\n</ul>\n</div></section>\n{END}'
        if START in s:
            n = re.sub(re.escape(START) + r"[\s\S]*?" + re.escape(END), lambda m: block, s, count=1)
        elif '<footer class="footer"' in s:
            n = s.replace('<footer class="footer"', block + '\n<footer class="footer"', 1)
        else:
            continue
        if 'id="correlati-css"' not in n:
            n = n.replace("</head>", CSS + "\n</head>", 1)
        if n != s:
            f.write_text(n, encoding="utf-8")
            done += 1
    print(f"correlati: {done} schede aggiornate su {len(rows)}")


if __name__ == "__main__":
    main()
