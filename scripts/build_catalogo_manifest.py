#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera listini/pubblico/catalogo-manifest.json da CSV + catalogo_contenuti."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from catalogo_contenuti import build_manifest_entry  # noqa: E402

CSV_PATH = ROOT / "listini" / "interno" / "listino-master.csv"
OUT = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"


def main() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    out = {}
    for row in rows:
        if row.get("pubblicabile") != "true":
            continue
        price = (row.get("prezzo_enduser_eur") or "").strip()
        if not price or price == "—":
            continue
        sku = row["sku"]
        out[sku] = build_manifest_entry(sku, row)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Scritti {len(out)} prodotti in {OUT}")


if __name__ == "__main__":
    main()
