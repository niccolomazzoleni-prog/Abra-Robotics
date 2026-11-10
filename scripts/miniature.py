#!/usr/bin/env python3
"""Miniature (320 px, webp) per le schede "correlati" delle pagine prodotto e per le liste degli hub.

- thumb_src(img, prefix): percorso della miniatura se esiste gia' in images/thumbs/, altrimenti
  l'immagine originale (i generatori non hanno bisogno di Pillow: in CI le miniature gia' committate bastano).
- python3 scripts/miniature.py : crea le miniature mancanti per le sole immagini usate (listino End-User,
  cobot Fairino, AMR). Il nome deriva dal percorso senza estensione, quindi resta valido quando
  immagini_webp.py converte il PNG/JPG originale in .webp. Idempotente. Richiede Pillow.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THUMBS = ROOT / "images" / "thumbs"
WIDTH = 320
HEIGHT = 240  # riquadro 4:3 della scheda; l'immagine ci sta dentro con object-fit: contain


def rel(img: str) -> str:
    """Percorso relativo alla radice del sito (toglie dominio e barra iniziale)."""
    return re.sub(r"^(https?://(www\.)?abrarobotics\.com)?/?", "", (img or "").split("?")[0])


def thumb_rel(img: str) -> str:
    stem = re.sub(r"\.(png|jpe?g|webp|gif|avif)$", "", rel(img), flags=re.I)
    stem = re.sub(r"^images/", "", stem)
    return "images/thumbs/" + re.sub(r"[^A-Za-z0-9._-]+", "__", stem) + ".webp"


def thumb_src(img: str, prefix: str = "") -> str:
    """Miniatura se presente, altrimenti l'originale (con lo stesso prefisso relativo)."""
    if not img:
        return ""
    t = thumb_rel(img)
    if (ROOT / t).is_file():
        return prefix + t
    return prefix + rel(img)


def usate() -> list[str]:
    out: dict[str, None] = {}
    items = json.loads((ROOT / "listini" / "pubblico" / "end-user.json").read_text(encoding="utf-8"))
    for v in items.values():
        if v.get("immagine"):
            out[rel(v["immagine"])] = None
    for data in ("cobot-products.json", "amr-products.json"):
        try:
            prods = json.loads((ROOT / "data" / data).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for v in prods:
            if v.get("image"):
                out[rel(v["image"])] = None
    return list(out)


def main() -> None:
    from PIL import Image

    THUMBS.mkdir(parents=True, exist_ok=True)
    made = tot = 0
    size = 0
    for img in usate():
        src = ROOT / img
        if not src.is_file():
            alt = src.with_suffix(".webp")  # l'originale PNG/JPG puo' essere stato sostituito dalla .webp
            if not alt.is_file():
                print("manca:", img, file=sys.stderr)
                continue
            src = alt
        dst = ROOT / thumb_rel(img)
        tot += 1
        if not (dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime):
            im = Image.open(src)
            im.load()
            alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
            im = im.convert("RGBA" if alpha else "RGB")
            im.thumbnail((WIDTH, 320), Image.LANCZOS)  # larghezza max 320 px, altezza max 320 px
            im.save(dst, "WEBP", quality=78, method=6)
            made += 1
        size += dst.stat().st_size
    print(f"miniature: {made} create, {tot} totali, {size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
