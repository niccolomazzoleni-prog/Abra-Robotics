#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggiorna percorsi immagine nell'HTML statico da data/product-images.json."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "data" / "product-images.json"
MANIFEST = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
SITE = "https://niccolomazzoleni-prog.github.io/Abra-Robotics/"

sys.path.insert(0, str(ROOT / "scripts"))
from catalogo_contenuti import IMAGE  # noqa: E402


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def image_path(entry) -> str:
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        if entry.get("path"):
            return entry["path"]
        if entry.get("gallery"):
            return entry["gallery"][0]
    return ""


def rel_variants(path: str) -> list[tuple[str, str]]:
    """Solo sostituzioni relative sicure (no URL assoluti)."""
    if not path or path.startswith("http"):
        return []
    pairs: list[tuple[str, str]] = []
    if path.startswith("images/"):
        pairs.append((path, f"../{path}"))
        pairs.append((f"../{path}", path))
    return pairs


def abs_url(path: str) -> str:
    clean = path.lstrip("./").removeprefix("../")
    return f"{SITE}{clean}"


def old_paths_for_sku(sku: str, new_path: str) -> set[str]:
    olds = {IMAGE.get(sku, "")}
    if sku == "B2":
        olds.update({"images/prodotti/unitree-b2-hero.png", "images/prodotti/unitree-b2.png"})
    return {p for p in olds if p and p != new_path}


def patch_product_file(path: Path, sku: str, new_path: str) -> int:
    old_candidates = old_paths_for_sku(sku, new_path)
    if not old_candidates or not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8")
    n = 0
    for old_path in old_candidates:
        for a, b in rel_variants(old_path):
            for new_a, new_b in [(new_path, f"../{new_path}")]:
                for old, new in ((a, new_a), (b, new_b)):
                    if old in text:
                        c = text.count(old)
                        text = text.replace(old, new)
                        n += c
        for old_abs in (abs_url(old_path), f"{SITE}{old_path}"):
            new_abs = abs_url(new_path)
            if old_abs in text and old_abs != new_abs:
                c = text.count(old_abs)
                text = text.replace(old_abs, new_abs)
                n += c
    if n:
        path.write_text(text, encoding="utf-8")
    return n


def patch_landing_by_href(path: Path, slug_to_image: dict[str, str]) -> int:
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8")
    total = 0
    for slug, img in slug_to_image.items():
        if not img:
            continue
        href = f"prodotti/{slug}"
        pattern = re.compile(
            rf"(<article[^>]*>.*?{re.escape(href)}.*?</article>)",
            re.DOTALL | re.IGNORECASE,
        )
        for m in pattern.finditer(text):
            block = m.group(1)
            new_block = block
            for old in set(IMAGE.values()):
                if old.startswith("images/") and old in new_block:
                    new_block = new_block.replace(f'src="{old}"', f'src="{img}"')
                    new_block = new_block.replace(f"src='{old}'", f"src='{img}'")
            if new_block != block:
                text = text[: m.start(1)] + new_block + text[m.end(1) :]
                total += 1
                break
    if total:
        path.write_text(text, encoding="utf-8")
    return total


def main() -> None:
    overrides = load_json(OVERRIDES)
    manifest = load_json(MANIFEST)

    product_hits = 0
    for sku, entry in overrides.items():
        new_path = image_path(entry)
        if not new_path or sku not in manifest:
            continue
        slug = manifest[sku].get("slug")
        if slug:
            product_hits += patch_product_file(ROOT / "prodotti" / slug, sku, new_path)

    slug_to_image = {
        manifest[sku]["slug"]: image_path(overrides[sku])
        for sku in overrides
        if sku in manifest and image_path(overrides[sku])
    }
    landing_hits = 0
    for name in ("quadrupedi.html", "universita-ricerca.html", "manifattura-logistica.html", "index.html"):
        landing_hits += patch_landing_by_href(ROOT / name, slug_to_image)

    print(f"Patch prodotti: {product_hits} · landing: {landing_hits}")


if __name__ == "__main__":
    main()
