#!/usr/bin/env python3
"""Scarica immagini Youibot corrette e ripulisce trasparenza AMR (bianco + alone su nero)."""
from __future__ import annotations

import json
import urllib.request
from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
AMR = ROOT / "images" / "manifattura" / "amr"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Icone sbagliate (stat 300kg / 8h) → foto prodotto ufficiali L-series
YOUIBOT = {
    "youibot-l300-gallery.png": "https://youibot.usa18.mega--cloud.com/uploads/image/6422942ea21f0.png",
    "youibot-l300.png": "https://youibot.usa18.mega--cloud.com/uploads/image/64254b24bc660.png",
    "youibot-l1000.png": "https://youibot.usa18.mega--cloud.com/uploads/image/65b9edb21e4c3.png",
    "youibot-l1000-gallery.png": "https://youibot.usa18.mega--cloud.com/uploads/image/642293f4e1c02.png",
}


def dl(name: str, url: str) -> None:
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=30).read()
    if len(data) < 3000:
        raise ValueError(f"{name}: troppo piccolo ({len(data)} B)")
    (AMR / name).write_bytes(data)
    print(f"DL {name}: {len(data)} B")


def flood_clear(path: Path, thresh: int = 246, tolerance: int = 14) -> None:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    q: deque[tuple[int, int]] = deque()
    seen: set[tuple[int, int]] = set()
    for x in range(w):
        q.append((x, 0))
        q.append((x, h - 1))
    for y in range(h):
        q.append((0, y))
        q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h or (x, y) in seen:
            continue
        seen.add((x, y))
        r, g, b, a = px[x, y]
        if a < 8:
            continue
        m = min(r, g, b)
        if m >= thresh - tolerance:
            px[x, y] = (r, g, b, 0)
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) not in seen:
                    q.append((nx, ny))
    im.save(path, optimize=True)


def dewhite(path: Path, thresh: int = 244, feather: int = 16) -> None:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            m = min(r, g, b)
            if m >= thresh:
                px[x, y] = (r, g, b, 0)
            elif m >= thresh - feather:
                na = int(255 * (thresh - m) / feather)
                px[x, y] = (r, g, b, min(a, max(0, 255 - na)))
    im.save(path, optimize=True)


def defringe_black_bg(path: Path, dark: int = 28, halo: int = 195) -> None:
    """Rimuove sfondo nero + alone grigio/chiaro attorno ai render MiR Storyblok."""
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            m = max(r, g, b)
            mn = min(r, g, b)
            # nero puro o quasi
            if m <= dark:
                px[x, y] = (r, g, b, 0)
                continue
            # alone grigio chiaro (bassa saturazione, luminosità alta)
            sat = m - mn
            if m >= halo and sat <= 35:
                fade = min(255, int(255 * (m - halo) / 45))
                px[x, y] = (r, g, b, max(0, a - fade))
            elif m >= halo - 40 and sat <= 25:
                fade = int(120 * (m - (halo - 40)) / 40)
                px[x, y] = (r, g, b, max(0, a - fade))
    im.save(path, optimize=True)


def process_png(path: Path, black_bg: bool = False) -> None:
    if black_bg:
        defringe_black_bg(path)
    else:
        flood_clear(path)
        dewhite(path)


def catalog_pngs() -> list[tuple[Path, bool]]:
    catalog = json.loads((ROOT / "data" / "amr-catalog.json").read_text(encoding="utf-8"))
    out: list[tuple[Path, bool]] = []
    seen: set[str] = set()
    black_bg_names = {
        "mir250-hero.png", "mir600-hero.png", "mir1350-hero.png",
        "mir250-teaser.png", "mir600-teaser.png", "mir1350-teaser.png",
    }
    for row in catalog:
        name = Path(row["file"]).name
        if name in seen or not name.endswith(".png"):
            continue
        seen.add(name)
        p = AMR / name
        if p.is_file():
            out.append((p, name in black_bg_names))
    return out


def main() -> None:
    print("=== Youibot ===")
    for name, url in YOUIBOT.items():
        try:
            dl(name, url)
            process_png(AMR / name, black_bg=False)
            print(f"  OK process {name}")
        except Exception as e:
            print(f"  FAIL {name}: {e}")

    print("\n=== MiR / catalogo PNG ===")
    for path, black_bg in catalog_pngs():
        try:
            process_png(path, black_bg=black_bg)
            print(f"OK {path.name} ({'black' if black_bg else 'white'})")
        except Exception as e:
            print(f"FAIL {path.name}: {e}")

    for name in ("mir250-hero.png", "mir600-hero.png", "mir1350-hero.png"):
        p = AMR / name
        if p.is_file():
            process_png(p, black_bg=True)
            print(f"OK {name} (hero poster)")


if __name__ == "__main__":
    main()
