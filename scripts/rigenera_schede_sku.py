#!/usr/bin/env python3
"""Rigenera solo le schede compatte degli SKU indicati (da listino pubblico + manifest),
poi riallinea SEO prezzo, correlati e merchant feed. Utile per correzioni puntuali
senza riscrivere tutte le schede.

Uso: python3 scripts/rigenera_schede_sku.py AS2-AIR GO2W-STD ...
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from genera_catalogo_completo import generate_page, load_manifest  # noqa: E402
from regenerate_from_public import rows_from_end_user  # noqa: E402


def main(skus: list[str]) -> None:
    manifest = load_manifest()
    rows = {r["sku"]: r for r in rows_from_end_user()}
    for sku in skus:
        if sku not in rows:
            print(f"SKU non a listino: {sku}")
            continue
        out = generate_page(rows[sku], manifest)
        print(f"{sku}: {out or 'saltata (pagina ricca, SKIP_OVERWRITE)'}")
    for script in ("genera_correlati.py", "seo_schede_prezzo.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script)], check=False)
    subprocess.run([sys.executable, str(ROOT / "prodotti" / "_gen_merchant_feed.py")], cwd=ROOT / "prodotti", check=False)


if __name__ == "__main__":
    main(sys.argv[1:])
