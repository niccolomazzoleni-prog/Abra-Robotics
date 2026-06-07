#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigenera catalogo e schede compatte usando solo file pubblici (no CSV interno). Per CI."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from catalogo_contenuti import image_for  # noqa: E402
from genera_catalogo_completo import (  # noqa: E402
    MANIFEST_PATH,
    generate_page,
    load_manifest,
    parse_price,
    regenerate_catalogo_html,
    slug_file,
)

END_USER = ROOT / "listini" / "pubblico" / "end-user.json"


def sync_end_user_images(manifest: dict) -> None:
    if not END_USER.is_file():
        return
    data = json.loads(END_USER.read_text(encoding="utf-8"))
    for sku, entry in data.items():
        if sku in manifest and manifest[sku].get("immagine"):
            entry["immagine"] = manifest[sku]["immagine"]
    END_USER.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rows_from_end_user() -> list[dict]:
    data = json.loads(END_USER.read_text(encoding="utf-8"))
    rows = []
    for sku, v in data.items():
        rows.append({
            "sku": sku,
            "nome_prodotto": v.get("nome", sku),
            "prezzo_enduser_eur": str(v.get("prezzo_eur", "")).replace(".", ","),
            "pubblicabile": "true",
            "categoria": v.get("categoria", ""),
            "pagina_sito": f"prodotti/{v.get('slug', slug_file(sku))}",
            "stato_sito": "pubblicato",
        })
    return rows


def sync_manifest_images(manifest: dict) -> dict:
    for sku, entry in manifest.items():
        cat = entry.get("categoria", "")
        entry["immagine"] = image_for(sku, cat)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def inject_image_runtime() -> None:
    from inject_image_runtime import main as inject_main

    inject_main()


def main() -> None:
    inject_image_runtime()
    manifest = load_manifest()
    manifest = sync_manifest_images(manifest)
    rows = rows_from_end_user()
    created = 0
    for row in rows:
        if not parse_price(row.get("prezzo_enduser_eur", "")):
            continue
        if generate_page(row, manifest):
            created += 1
    sync_end_user_images(manifest)
    regenerate_catalogo_html(rows, manifest)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "patch_html_images.py")], check=False)
    print(f"Rigenerate {created} schede · catalogo-unitree.html aggiornato")


if __name__ == "__main__":
    main()
