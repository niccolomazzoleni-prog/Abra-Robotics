#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collega Stripe LIVE: crea Payment Link e aggiorna prodotti/stripe-config.js.

Uso (dalla root del progetto):
  1. Crea/aggiorna .env con:
       STRIPE_SECRET_KEY=sk_live_...
       STRIPE_PUBLISHABLE_KEY=pk_live_...
     (chiavi da https://dashboard.stripe.com/apikeys — modalità Live)
  2. python scripts/connect_stripe_live.py

La secret key NON va mai nel repo — solo in .env locale (gitignored).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "prodotti" / "_gen_stripe.py"
ENV = ROOT / ".env"


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def main() -> None:
    if not GEN.is_file():
        raise SystemExit(f"Script non trovato: {GEN}")
    load_dotenv(ENV)

    sk = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
    pk = (os.environ.get("STRIPE_PUBLISHABLE_KEY") or "").strip()
    if not sk.startswith("sk_live_"):
        raise SystemExit(
            "STRIPE_SECRET_KEY deve essere una chiave LIVE (sk_live_...).\n"
            "Aggiorna .env con le chiavi da https://dashboard.stripe.com/apikeys "
            "(attiva la modalità Live in alto a destra)."
        )
    if pk and not pk.startswith("pk_live_"):
        raise SystemExit(
            "STRIPE_PUBLISHABLE_KEY deve essere pk_live_... (coerente con sk_live_)."
        )

    print("Stripe LIVE — generazione Payment Link da end-user.json …\n")
    subprocess.run([sys.executable, str(GEN), "--live"], cwd=str(GEN.parent), check=True)
    print("\nOK. Controlla prodotti/stripe-config.js (pk_live_ + URL senza /test_/) e fai commit + push.")


if __name__ == "__main__":
    main()
