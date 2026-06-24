#!/usr/bin/env python3
"""Allinea categoria QUADRUPEDI su listino e manifest (struttura sito quadrupedi.html)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTINO = ROOT / "listini" / "pubblico" / "end-user.json"
MANIFEST = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"

# Piattaforme quadrupede — non accessori (batterie, charger, controller restano COMPONENTISTICA)
QUADRUPED_SKUS = frozenset({
    "GO2-AIR", "GO2-PRO", "GO2-EDU-STD", "GO2-EDU-SMART", "GO2-EDU-ULT", "GO2-EDU-LASER",
    "GO2W-U2", "GO2W-U3", "GO2W-U4", "GO2W-U5",
    "AS2-AIR", "AS2-PRO", "AS2-EDU",
    "A2-STD", "A2-PRO", "A2W-STD", "A2W-PRO",
    "B2", "B2W", "B2-LIDAR", "B2W-LIDAR",
})


def fix_listino(data: dict) -> int:
    n = 0
    for sku in QUADRUPED_SKUS:
        if sku not in data:
            continue
        if data[sku].get("categoria") != "QUADRUPEDI":
            data[sku]["categoria"] = "QUADRUPEDI"
            n += 1
    return n


def fix_manifest(data: dict) -> int:
    n = 0
    for sku in QUADRUPED_SKUS:
        if sku not in data:
            continue
        if data[sku].get("categoria") != "QUADRUPEDI":
            data[sku]["categoria"] = "QUADRUPEDI"
            n += 1
    return n


def main() -> None:
    if not LISTINO.exists():
        raise SystemExit(f"Manca {LISTINO}")
    listino = json.loads(LISTINO.read_text(encoding="utf-8"))
    ln = fix_listino(listino)
    LISTINO.write_text(json.dumps(listino, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Listino: {ln} SKU -> QUADRUPEDI")

    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        mn = fix_manifest(manifest)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Manifest: {mn} SKU -> QUADRUPEDI")


if __name__ == "__main__":
    main()
