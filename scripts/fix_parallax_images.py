#!/usr/bin/env python3
"""Corregge path immagini parallax rotte nelle schede prodotto."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODOTTI = ROOT / "prodotti"
EN = ROOT / "en" / "prodotti"
VARIANTS = PRODOTTI / "assets" / "variants"


def pick_images(variant: str) -> list[str]:
    folder = VARIANTS / variant
    if not folder.is_dir():
        return []
    names = {p.name for p in folder.iterdir() if p.is_file() and p.stat().st_size > 0}

    def first(*candidates: str) -> str | None:
        for c in candidates:
            if c in names:
                return f"assets/variants/{variant}/{c}"
        return None

    slots = [
        first("img-01-abra.png", "img-01.png"),
        first("img-02.jpg", "img-03.jpg"),
        first("img-04.jpg", "img-03.jpg"),
        first("img-05.jpg", "img-04.jpg"),
    ]
    fallback = first("img-01-abra.png", "img-01.png") or f"assets/variants/{variant}/img-01.png"
    return [s or fallback for s in slots]


def fix_parallax_block(html: str) -> str:
    m = re.search(
        r'(<div class="parallax-cols" id="parallax-container">.*?</div>\s*</div>\s*</div>\s*</section>)',
        html,
        re.DOTALL,
    )
    if not m:
        return html
    block = m.group(1)
    vm = re.search(r"assets/variants/([^/\"']+)/", block)
    if not vm:
        return html
    variant = vm.group(1)
    imgs = pick_images(variant)
    wraps = list(re.finditer(r'(<div class="parallax-img-wrap">\s*<img[^>]+src=")[^"]+(")', block))
    if not wraps:
        return html
    new_block = block
    for i, wm in enumerate(wraps):
        src = imgs[min(i, len(imgs) - 1)]
        old = wm.group(0)
        new = wm.group(1) + src + wm.group(2)
        new_block = new_block.replace(old, new, 1)
    return html.replace(block, new_block, 1)


def main() -> None:
    count = 0
    for base in (PRODOTTI, EN):
        if not base.exists():
            continue
        for html_path in sorted(base.glob("unitree-*.html")):
            text = html_path.read_text(encoding="utf-8")
            if "parallax-container" not in text:
                continue
            fixed = fix_parallax_block(text)
            if fixed != text:
                html_path.write_text(fixed, encoding="utf-8")
                count += 1
                print(f"Fixed {html_path.relative_to(ROOT)}")
    print(f"Done — {count} file aggiornati.")


if __name__ == "__main__":
    main()
