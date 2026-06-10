#!/usr/bin/env python3
"""Rimuove sfondo bianco/chiaro dalle immagini AMR usate in catalogo e schede."""
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
AMR = ROOT / "images" / "manifattura" / "amr"
CATALOG = ROOT / "data" / "amr-catalog.json"


def catalog_files() -> list[Path]:
    items = json.loads(CATALOG.read_text(encoding="utf-8"))
    names: set[str] = set()
    for row in items:
        names.add(Path(row["file"]).name)
        if row.get("video"):
            names.add(Path(row["video"]).name)
    out = []
    for name in sorted(names):
        p = AMR / name
        if p.suffix.lower() in {".mp4", ".jpg", ".jpeg"}:
            continue
        if p.is_file() and p.stat().st_size > 2000:
            out.append(p)
    return out


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
        if x < 0 or x >= w or y < 0 or y >= h:
            continue
        if (x, y) in seen:
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


def dewhite_pass(path: Path, thresh: int = 244, feather: int = 16) -> None:
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


def white_pct(path: Path) -> float:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    white = total = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 10:
                continue
            total += 1
            if r > 235 and g > 235 and b > 235:
                white += 1
    return 100 * white / max(total, 1)


def aggressive_dewhite(path: Path, thresh: int = 228, feather: int = 13) -> None:
  """Per foto prodotto con fondo bianco interno (es. Juno su sfondo studio)."""
  im = Image.open(path).convert("RGBA")
  px = im.load()
  w, h = im.size
  for y in range(h):
    for x in range(w):
      r, g, b, a = px[x, y]
      if a < 10:
        continue
      m = min(r, g, b)
      if m >= thresh:
        px[x, y] = (r, g, b, 0)
      elif m >= thresh - feather:
        na = int(255 * (thresh - m) / feather)
        px[x, y] = (r, g, b, min(a, max(0, 255 - na)))
  im.save(path, optimize=True)


def main() -> None:
    for path in catalog_files():
        before = white_pct(path)
        flood_clear(path)
        dewhite_pass(path)
        after = white_pct(path)
        if after > 12:
            aggressive_dewhite(path)
            after = white_pct(path)
        print(f"{path.name}: white {before:.1f}% -> {after:.1f}%")
    xp = AMR / "ep-xp15.png"
    if xp.is_file():
        flood_clear(xp)
        dewhite_pass(xp)
        print(f"ep-xp15.png: white {white_pct(xp):.1f}%")


if __name__ == "__main__":
    main()
