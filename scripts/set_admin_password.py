#!/usr/bin/env python3
"""Imposta la password dell'area admin (hash SHA-256 in data/admin-auth.json)."""
from __future__ import annotations

import hashlib
import json
import sys
from getpass import getpass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUTH_PATH = ROOT / "data" / "admin-auth.json"


def main() -> None:
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
    else:
        pwd = getpass("Nuova password admin: ")
        confirm = getpass("Conferma: ")
        if pwd != confirm:
            print("Le password non coincidono.")
            sys.exit(1)
    if len(pwd) < 8:
        print("Usa almeno 8 caratteri.")
        sys.exit(1)
    h = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
    data = {"password_sha256": h}
    AUTH_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUTH_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"OK — hash salvato in {AUTH_PATH}")
    print("Committa e pusha: git add data/admin-auth.json && git commit -m 'admin: password' && git push")


if __name__ == "__main__":
    main()
