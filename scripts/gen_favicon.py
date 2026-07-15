#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera favicon con font Nasalization (Typodermic / NASA worm)."""
from __future__ import annotations

import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "fonts" / "nasalization-rg.otf"
IMG = ROOT / "images"
BG = (10, 10, 10, 255)
FG = (255, 255, 255, 255)


def render_letter(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(img)
    fsize = int(size * 0.58)
    font = ImageFont.truetype(str(FONT), fsize)
    bbox = draw.textbbox((0, 0), "A", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1] - size * 0.02
    draw.text((x, y), "A", font=font, fill=FG)
    return img


def write_svg() -> None:
    font_b64 = base64.b64encode(FONT.read_bytes()).decode("ascii")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" role="img" aria-label="Abra Robotics">
  <defs>
    <style>
      @font-face {{
        font-family: "Nasalization";
        src: url("data:font/opentype;base64,{font_b64}") format("opentype");
        font-weight: 400;
        font-style: normal;
      }}
    </style>
  </defs>
  <rect width="32" height="32" rx="16" fill="#0a0a0a"/>
  <text x="16" y="22.5" text-anchor="middle" font-family="Nasalization, sans-serif" font-size="19" fill="#ffffff">A</text>
</svg>
"""
    (IMG / "favicon.svg").write_text(svg, encoding="utf-8")


def write_ico(sizes: list[int]) -> None:
    imgs = [render_letter(s) for s in sizes]
    imgs[0].save(IMG / "favicon.ico", format="ICO", sizes=[(s, s) for s in sizes], append_images=imgs[1:])


def main() -> None:
    if not FONT.is_file():
        raise SystemExit(f"Font mancante: {FONT}")

    for size, name in [(16, "favicon-16x16.png"), (32, "favicon-32x32.png"), (180, "apple-touch-icon.png")]:
        render_letter(size).save(IMG / name)

    write_ico([16, 32, 48])
    write_svg()
    print("Favicon Nasalization generati in images/")


if __name__ == "__main__":
    main()
