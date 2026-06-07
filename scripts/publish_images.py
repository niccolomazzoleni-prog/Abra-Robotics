#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applica override immagini da data/product-images.json, scarica URL e rigenera il sito."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES_PATH = ROOT / "data" / "product-images.json"


def load_overrides() -> dict:
    if not OVERRIDES_PATH.is_file():
        return {}
    return json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))


def download_url(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    clean = url.split("?")[0]
    req = urllib.request.Request(clean, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


def apply_overrides(overrides: dict, *, download: bool = True) -> tuple[int, int]:
    ok, skip = 0, 0
    for sku, entry in overrides.items():
        if isinstance(entry, str):
            path, url = entry, None
        elif isinstance(entry, dict):
            path = entry.get("path", "")
            url = entry.get("source_url") or entry.get("url")
        else:
            continue
        if not path:
            skip += 1
            continue
        dest = ROOT / path.replace("/", "\\") if sys.platform == "win32" else ROOT / path
        if download and url:
            print(f"  {sku}: scarico → {path}")
            try:
                download_url(url, dest)
                ok += 1
            except Exception as e:
                print(f"  FAIL {sku}: {e}")
        elif dest.is_file():
            print(f"  {sku}: file locale OK ({path})")
            ok += 1
        else:
            print(f"  {sku}: manca file {path}")
            skip += 1
    return ok, skip


def apply_from_zip(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            target = ROOT / name.replace("/", "\\") if sys.platform == "win32" else ROOT / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(name))
            print(f"  estratto {name}")


def regenerate() -> None:
    steps = [
        [sys.executable, str(ROOT / "scripts" / "build_catalogo_manifest.py")],
        [sys.executable, str(ROOT / "scripts" / "genera_catalogo_completo.py")],
    ]
    for cmd in steps:
        print(f"\n> {' '.join(cmd)}")
        subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Pubblica immagini prodotto e rigenera catalogo")
    ap.add_argument("--from-zip", type=Path, help="Estrae ZIP esportato da admin/immagini.html")
    ap.add_argument("--no-download", action="store_true", help="Non scaricare source_url, solo rigenera")
    ap.add_argument("--no-regen", action="store_true", help="Solo scarica/estrai, senza rigenerare HTML")
    args = ap.parse_args()

    if args.from_zip:
        print(f"Estrazione {args.from_zip}…")
        apply_from_zip(args.from_zip)

    overrides = load_overrides()
    if overrides:
        print(f"\nOverride in {OVERRIDES_PATH} ({len(overrides)} SKU)…")
        apply_overrides(overrides, download=not args.no_download)
    else:
        print("Nessun override in data/product-images.json")

    if not args.no_regen:
        print("\nRigenerazione sito…")
        regenerate()
        print("\nCompletato. Verifica in locale poi commit + push.")


if __name__ == "__main__":
    main()
