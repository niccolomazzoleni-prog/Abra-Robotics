#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collega Stripe sandbox: crea Payment Link e aggiorna prodotti/stripe-config.js.

Uso (dalla root del progetto):
  1. Crea .env con STRIPE_SECRET_KEY=sk_test_... (e opz. STRIPE_PUBLISHABLE_KEY)
  2. python scripts/connect_stripe_sandbox.py

La secret key NON va mai nel repo — solo in .env locale (gitignored).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "prodotti" / "_gen_stripe.py"


def main() -> None:
    if not GEN.is_file():
        raise SystemExit(f"Script non trovato: {GEN}")
    print("Stripe sandbox — generazione Payment Link da _prezzi.py …\n")
    subprocess.run([sys.executable, str(GEN)], cwd=str(GEN.parent), check=True)
    print("\nOK. Controlla prodotti/stripe-config.js e fai commit + push.")


if __name__ == "__main__":
    main()
