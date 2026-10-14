#!/usr/bin/env python3
"""Scarica le immagini e i video prodotto UFFICIALI (siti dei produttori) e li
salva in images/official/*.webp e videos/official/*.mp4.

Fonti e destinazioni sono in data/immagini-ufficiali.json (url + pagina di
provenienza). Solo siti ufficiali: unitree.com, shop.unitree.com (store
ufficiale Unitree), livoxtech.com, hesaitech.com, inspire-robots.com.
Non usare mai immagini di rivenditori terzi.

Uso:
  python scripts/immagini_ufficiali.py            # scarica solo i file mancanti
  python scripts/immagini_ufficiali.py --force    # riscarica tutto
"""
from __future__ import annotations

import io
import json
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "immagini-ufficiali.json"
MAX_W = 1600
QUALITY = 85


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def to_webp(data: bytes, dest: Path, crop=None) -> None:
    im = Image.open(io.BytesIO(data))
    im.load()
    if crop:
        im = im.crop(tuple(crop))
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if has_alpha else "RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=QUALITY, method=6)


def placeholder(dest: Path) -> None:
    """Segnaposto neutro (grigio chiaro + logo Abra in trasparenza)."""
    size = 800
    im = Image.new("RGB", (size, size), (243, 243, 245))
    logo_path = ROOT / "images" / "logo-icon.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((160, 160))
        alpha = logo.getchannel("A").point(lambda v: v * 0.25)
        logo.putalpha(alpha)
        im.paste(logo, ((size - logo.width) // 2, (size - logo.height) // 2), logo)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=QUALITY)


def main() -> None:
    force = "--force" in sys.argv
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ok = fail = 0
    for slug, e in data.items():
        dest = ROOT / e["file"]
        if dest.exists() and not force:
            continue
        try:
            if not e.get("url"):
                placeholder(dest)
            elif dest.suffix == ".mp4":
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(fetch(e["url"]))
            else:
                to_webp(fetch(e["url"]), dest, e.get("crop"))
            ok += 1
            print(f"  OK   {e['file']}")
        except Exception as exc:  # noqa: BLE001
            fail += 1
            print(f"  FAIL {slug}: {exc}")
    print(f"Fatto: {ok} scaricati, {fail} errori.")


if __name__ == "__main__":
    main()
