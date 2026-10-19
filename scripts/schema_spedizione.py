#!/usr/bin/env python3
"""shippingDetails nello schema Product delle schede prodotto (Search Console, "Schede commercianti").

Si aggiunge SOLO dove la pagina dichiara che il prezzo comprende spedizione e dazio fino all'Italia
(condizioni di vendita, art. consegna): costo di spedizione 0 EUR, destinazione Italia.
Le schede senza questa dicitura (cobot, AMR e altri produttori, spedizione quotata a parte)
restano senza shippingDetails: dichiarare un costo sarebbe falso.
Idempotente. Uso: python scripts/schema_spedizione.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUSA = re.compile(r"spedizione e dazio (?:doganale )?inclusi|shipping and (?:customs )?dut(?:y|ies) included", re.I)
SHIPPING = {
    "@type": "OfferShippingDetails",
    "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "EUR"},
    "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "IT"},
}
LD = re.compile(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)')


def fix(s: str) -> str:
    if not INCLUSA.search(s.split("</head>", 1)[-1]):
        return s

    def rep(m: re.Match) -> str:
        try:
            j = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        changed = False
        for x in (j if isinstance(j, list) else j.get("@graph", [j])):
            if not isinstance(x, dict) or x.get("@type") != "Product":
                continue
            offers = x.get("offers")
            for o in (offers if isinstance(offers, list) else [offers]):
                if isinstance(o, dict) and o.get("price") and o.get("shippingDetails") != SHIPPING:
                    o["shippingDetails"] = SHIPPING
                    changed = True
        if not changed:
            return m.group(0)
        return m.group(1) + "\n" + json.dumps(j, ensure_ascii=False, indent=2) + "\n" + m.group(3)

    return LD.sub(rep, s)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    n = 0
    for f in sorted((ROOT / "prodotti").glob("*.html")) + sorted((ROOT / "en" / "prodotti").glob("*.html")):
        if f.name.startswith("_"):
            continue
        s = f.read_text(encoding="utf-8")
        t = fix(s)
        if t != s:
            f.write_text(t, encoding="utf-8")
            n += 1
    print(f"schede con shippingDetails aggiornate: {n}")


if __name__ == "__main__":
    main()
