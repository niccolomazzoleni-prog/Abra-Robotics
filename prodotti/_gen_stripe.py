#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera su Stripe un Prodotto + Prezzo + Payment Link per OGNI scheda con
stato "acquista", leggendo i prezzi da _prezzi.py (FONTE UNICA), e scrive gli
URL dei Payment Link in stripe-config.js.

  ⚠️  ESEGUITO IN LOCALE DA TE, NON committato in alcun output sensibile.
      La secret key arriva da variabile d'ambiente: NON finisce mai nel repo.

USO:
    pip install stripe
    export STRIPE_SECRET_KEY=sk_test_xxx        # TEST mode (consigliato per provare)
    export STRIPE_PUBLISHABLE_KEY=pk_test_xxx   # opzionale
    python3 _gen_stripe.py                       # crea e aggiorna stripe-config.js
    python3 _gen_stripe.py --live                # usa SITE_URL di produzione per i redirect

Note:
- Idempotente sui Prodotti (cerca per metadata.slug e riusa).
- Crea un nuovo Prezzo + Payment Link a ogni run (i Price Stripe sono
  immutabili): rilancialo solo quando cambi un prezzo in _prezzi.py.
- after_completion -> redirect a /grazie.html con l'id sessione.
"""
import glob
import os
import re
import sys

try:
    import stripe
except ImportError:
    sys.exit("Manca la libreria Stripe. Esegui:  pip install stripe")

from _prezzi import PREZZI, euro  # FONTE UNICA prezzi

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
SITE_URL = "https://niccolomazzoleni-prog.github.io/Abra-Robotics"  # base per success redirect
SHIP_COUNTRIES = ["IT", "FR", "DE", "ES", "AT", "BE", "NL", "PT", "CH"]  # B2B EU
DEFAULT_PUB_KEY = "pk_test_51TfGsx4sActfFZskv4KaRe70MlFYfSXz7pziwpQdY832en8IfMIqALSs1efCtwiGntjHG0Xr1CLemyDZQUW7lgyP003xdWD4si"


def load_dotenv(path: str) -> None:
    """Carica .env nella root senza dipendenze extra."""
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_dotenv(os.path.join(ROOT, ".env"))

stripe.api_key = (os.environ.get("STRIPE_SECRET_KEY") or "").strip()
if not stripe.api_key:
    sys.exit(
        "STRIPE_SECRET_KEY non impostata.\n"
        "Crea .env nella root con STRIPE_SECRET_KEY=sk_test_... oppure:\n"
        "  $env:STRIPE_SECRET_KEY='sk_test_...'  (PowerShell)\n"
        "  python scripts/connect_stripe_sandbox.py"
    )
PUB_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", DEFAULT_PUB_KEY)
GAS_URL = os.environ.get("GOOGLE_SCRIPT_URL", "INSERISCI_QUI_IL_TUO_URL_APPS_SCRIPT")


def product_name(slug):
    """Nome leggibile dal <title> della scheda (parte prima di '—' o '|')."""
    f = os.path.join(BASE, slug)
    if os.path.exists(f):
        m = re.search(r"<title>(.*?)</title>", open(f, encoding="utf-8").read(), re.S)
        if m:
            return re.split(r"\s[—\-|]\s", m.group(1).strip())[0].strip()
    return slug.replace("unitree-", "Unitree ").replace(".html", "").replace("-", " ").title()


def upsert_product(slug, name):
    """Cerca il prodotto per metadata.slug, altrimenti lo crea (idempotente)."""
    try:
        res = stripe.Product.search(query=f"metadata['slug']:'{slug}'", limit=1)
        if res.data:
            return res.data[0].id
    except Exception:
        pass
    return stripe.Product.create(name=name, metadata={"slug": slug}).id


def make_payment_link(slug, name, cent):
    pid = upsert_product(slug, name)
    price = stripe.Price.create(product=pid, unit_amount=cent, currency="eur")
    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        metadata={"slug": slug},
        billing_address_collection="required",
        shipping_address_collection={"allowed_countries": SHIP_COUNTRIES},
        after_completion={
            "type": "redirect",
            "redirect": {"url": f"{SITE_URL}/grazie.html?session_id={{CHECKOUT_SESSION_ID}}"},
        },
    )
    return link.url


def existing_payment_links() -> dict[str, str]:
    """Mantiene i link già configurati e tutte le schede HTML del catalogo."""
    out: dict[str, str] = {}
    cfg = os.path.join(BASE, "stripe-config.js")
    if os.path.isfile(cfg):
        text = open(cfg, encoding="utf-8").read()
        for m in re.finditer(r'"([^"]+\.html)":\s*"([^"]*)"', text):
            out[m.group(1)] = m.group(2)
    for path in sorted(glob.glob(os.path.join(BASE, "unitree-*.html"))):
        slug = os.path.basename(path)
        out.setdefault(slug, "")
    return out


def write_config(links):
    out = os.path.join(BASE, "stripe-config.js")
    merged = existing_payment_links()
    merged.update(links)
    body = [
        "/* Stripe — generato da _gen_stripe.py (sandbox/test). NON contiene segreti. */",
        f'window.STRIPE_PUBLISHABLE_KEY = "{PUB_KEY}";',
        f'window.GOOGLE_SCRIPT_URL = "{GAS_URL}";',
        "window.STRIPE_PAYMENT_LINKS = {",
    ]
    for slug in sorted(merged):
        body.append(f'  "{slug}": "{merged[slug]}",')
    body.append("};\n")
    open(out, "w", encoding="utf-8").write("\n".join(body))
    print("Scritto", out)


def main():
    links = {}
    for slug, p in PREZZI.items():
        if p["stato"] != "acquista" or p["cent"] <= 0:
            print(f"- skip {slug} (stato={p['stato']}, cent={p['cent']})")
            continue
        name = product_name(slug)
        url = make_payment_link(slug, name, p["cent"])
        links[slug] = url
        print(f"OK {slug}: {name} -> {euro(p['cent'])} -> {url}")
    write_config(links)
    print("\nFatto. Controlla stripe-config.js e fai commit (contiene solo URL pubblici).")


if __name__ == "__main__":
    main()
