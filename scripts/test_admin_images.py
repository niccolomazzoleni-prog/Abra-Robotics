#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica che il flusso admin immagini → JSON → catalogo/schede sia coerente."""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "data" / "product-images.json"
MANIFEST = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
CATALOGO = ROOT / "catalogo-unitree.html"
LIVE = "https://niccolomazzoleni-prog.github.io/Abra-Robotics"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def image_path(entry) -> str:
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        return entry.get("path") or (entry.get("gallery") or [None])[0] or ""
    return ""


def catalog_img_for_sku(html: str, sku: str) -> str | None:
    m = re.search(
        rf'<article[^>]*data-sku="{re.escape(sku)}"[^>]*>.*?<img[^>]+src="([^"]+)"',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    return m.group(1) if m else None


def product_img_for_slug(html: str) -> str | None:
    m = re.search(r'id="gallery-main-img"[^>]+src="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'<img id="gallery-main-img" src="([^"]+)"', html)
    return m.group(1) if m else None


def norm_path(p: str) -> str:
    return p.replace("../", "").lstrip("/")


def check_live_json() -> list[str]:
    errs = []
    try:
        with urllib.request.urlopen(f"{LIVE}/data/product-images.json", timeout=20) as r:
            live = json.loads(r.read().decode())
        local = load(OVERRIDES)
        for sku, entry in local.items():
            lp = image_path(entry)
            live_p = image_path(live.get(sku, {}))
            if lp and live_p != lp:
                errs.append(f"LIVE JSON {sku}: atteso {lp}, live {live_p}")
    except Exception as ex:
        errs.append(f"LIVE JSON fetch: {ex}")
    return errs


def main() -> int:
    overrides = load(OVERRIDES)
    manifest = load(MANIFEST)
    catalog_html = CATALOGO.read_text(encoding="utf-8")
    failures: list[str] = []
    warnings: list[str] = []

    for sku, entry in overrides.items():
        path = image_path(entry)
        if not path:
            continue
        rel = norm_path(path)
        file_path = ROOT / rel
        if not file_path.is_file():
            failures.append(f"{sku}: file mancante {rel}")

        if sku not in manifest:
            warnings.append(f"{sku}: assente da catalogo-manifest.json")
            continue

        manifest_img = norm_path(manifest[sku].get("immagine", ""))
        if manifest_img != rel:
            failures.append(f"{sku}: manifest ha {manifest_img}, JSON {rel}")

        cat_src = catalog_img_for_sku(catalog_html, sku)
        if not cat_src:
            warnings.append(f"{sku}: non trovato in catalogo-unitree.html")
        elif norm_path(cat_src) != rel:
            failures.append(f"{sku}: catalogo img {cat_src}, atteso {rel}")

        slug = manifest[sku].get("slug", "")
        if slug:
            prod = ROOT / "prodotti" / slug
            if prod.is_file():
                prod_html = prod.read_text(encoding="utf-8")
                pimg = product_img_for_slug(prod_html)
                if pimg and norm_path(pimg) != rel:
                    # image-runtime.js può correggere a runtime
                    if "image-runtime.js" not in prod_html:
                        failures.append(f"{sku}: scheda {slug} img {pimg}, atteso {rel}")
                    else:
                        warnings.append(f"{sku}: scheda {slug} HTML statico {pimg} (runtime dovrebbe applicare {rel})")

    failures.extend(check_live_json())

    # Verifica CI workflow paths
    wf = (ROOT / ".github/workflows/regenerate-site.yml").read_text(encoding="utf-8")
    for needed in ("product-images.json", "patch_html_images", "quadrupedi.html", "listino-unitree.html"):
        if needed == "patch_html_images":
            if "patch_html_images" not in (ROOT / "scripts/regenerate_from_public.py").read_text(encoding="utf-8"):
                failures.append("regenerate_from_public.py non chiama patch_html_images.py")
        elif needed not in wf and needed != "patch_html_images":
            if needed == "listino-unitree.html" and "listino-unitree" not in wf:
                failures.append(f"CI workflow non committa {needed}")

    print("=== Test flusso admin immagini ===")
    print(f"Override in JSON: {len(overrides)} SKU")
    if warnings:
        print(f"\nAvvisi ({len(warnings)}):")
        for w in warnings[:20]:
            print(f"  ~ {w}")
        if len(warnings) > 20:
            print(f"  ... +{len(warnings) - 20}")
    if failures:
        print(f"\nFALLITI ({len(failures)}):")
        for f in failures:
            print(f"  X {f}")
        return 1
    print("\nOK: JSON, file, manifest e catalogo allineati.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
