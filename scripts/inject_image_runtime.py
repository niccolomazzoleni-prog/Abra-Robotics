#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inietta image-runtime.js nelle schede prodotto (prima di product.js / ecommerce.js)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti"
TAG = '<script src="../scripts/image-runtime.js"></script>\n'


def inject_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "image-runtime.js" in text:
        return False
    for anchor in (
        '  <script src="product.js"></script>\n',
        '  <script src="ecommerce.js"></script>\n',
    ):
        if anchor in text:
            path.write_text(text.replace(anchor, TAG + anchor, 1), encoding="utf-8")
            return True
    return False


def main() -> None:
    n = 0
    for path in sorted(PRODOTTI.glob("unitree-*.html")):
        if inject_file(path):
            n += 1
    print(f"Iniettato image-runtime in {n} schede")


if __name__ == "__main__":
    main()
