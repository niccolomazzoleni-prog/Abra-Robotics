#!/usr/bin/env python3
"""Rimuove sfondo bianco dalle PNG MiR (Elmark/Storyblok) → alpha trasparente."""
from pathlib import Path

from PIL import Image

AMR = Path(__file__).resolve().parents[1] / "images" / "manifattura" / "amr"

# Solo PNG statiche MiR (i video MP4 restano invariati)
TARGETS = [
    "mir250-base.png",
    "mir250-shelf.png",
    "mir250-hook.png",
    "mir600-base.png",
    "mir600-hero.png",
    "mir1350-hero.png",
    "mir1200-palletjack.png",
    "mir250-hero.png",
    "mir1350-teaser.png",
]


def dewhite(path: Path, thresh: int = 242, feather: int = 18) -> None:
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
    print(f"OK {path.name} ({w}x{h})")


def main() -> None:
    for name in TARGETS:
        p = AMR / name
        if p.is_file() and p.stat().st_size > 3000:
            dewhite(p)
        else:
            print(f"SKIP {name}")


if __name__ == "__main__":
    main()
