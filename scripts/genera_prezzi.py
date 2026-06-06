#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera listini/pubblico/end-user.json dal CSV master e aggiorna marker HTML."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "listini" / "interno" / "listino-master.csv"
JSON_PATH = ROOT / "listini" / "pubblico" / "end-user.json"
MANIFEST_PATH = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
NOTE_PUBBLICO = "IVA esclusa, spedizione e dazio inclusi"
PRICE_FROM_SKUS = {"R1-D"}


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}

def sku_pages_from_csv(rows: list[dict[str, str]]) -> dict[str, str]:
    """Mapping SKU → pagina da colonna pagina_sito del CSV."""
    out: dict[str, str] = {}
    for row in rows:
        page = (row.get("pagina_sito") or "").strip()
        if page and row.get("sku"):
            out[row["sku"]] = page
    return out

CARD_MARKERS: dict[str, tuple[str, str]] = {
    "G1-U1": ("universita-ricerca.html", "G1 EDU"),
    "R1-U3": ("universita-ricerca.html", "R1 EDU"),
    "H2-EDU": ("universita-ricerca.html", "H2 EDU"),
    "GO2-EDU-SMART": ("universita-ricerca.html", "Go2 EDU+"),
    "A2-STD": ("universita-ricerca.html", "A2"),
    "B2": ("universita-ricerca.html", "B2"),
}


def fmt_eur(value: float) -> str:
    s = f"{value:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_eur_symbol(value: float) -> str:
    return f"€ {fmt_eur(value)}"


def fmt_da_eur(value: float) -> str:
    return f"da € {fmt_eur(value)}"


def read_csv() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append(row)
    return rows


def generate_json(rows: list[dict[str, str]]) -> dict:
    manifest = load_manifest()
    out: dict = {}
    for row in rows:
        if row.get("pubblicabile", "").lower() != "true":
            continue
        price_raw = (row.get("prezzo_enduser_eur") or "").strip()
        if not price_raw or price_raw == "—":
            continue
        sku = row["sku"]
        entry: dict = {
            "nome": row["nome_prodotto"],
            "prezzo_eur": float(price_raw.replace(",", ".")),
            "note": NOTE_PUBBLICO,
        }
        if sku in manifest:
            m = manifest[sku]
            if m.get("immagine"):
                entry["immagine"] = m["immagine"]
            if m.get("slug"):
                entry["slug"] = m["slug"]
            if m.get("categoria"):
                entry["categoria"] = m["categoria"]
        if sku in PRICE_FROM_SKUS:
            entry["prezzo_da"] = True
        out[sku] = entry
    return out


def update_listino_block(content: str, sku: str, price_text: str, note: str) -> str:
    start = f"<!-- LISTINO:sku:{sku} -->"
    end = f"<!-- /LISTINO:sku:{sku} -->"
    pattern = re.compile(
        re.escape(start) + r"(.*?)" + re.escape(end),
        re.DOTALL,
    )

    def replacer(match: re.Match[str]) -> str:
        block = match.group(1)
        price_vis = price_text.replace("€ ", "") if price_text.startswith("€ ") else price_text
        amount = f"A partire da {price_vis} €" if sku in PRICE_FROM_SKUS else f"{price_vis} €"
        if "buy-box-amount" in block:
            block = re.sub(
                r'(<span class="buy-box-amount">)[^<]*(</span>)',
                rf"\g<1>{amount}\g<2>",
                block,
                count=1,
            )
        if "product-price" in block:
            block = re.sub(
                r'(<span class="product-price">)[^<]*(</span>)',
                rf"\g<1>{price_text}\g<2>",
                block,
                count=1,
            )
        if "product-price-note" in block:
            block = re.sub(
                r'(<span class="product-price-note">)[^<]*(</span>)',
                rf"\g<1>{note}\g<2>",
                block,
                count=1,
            )
        return start + block + end

    return pattern.sub(replacer, content)


def update_card_block(content: str, sku: str, price_text: str) -> str:
    start = f"<!-- LISTINO:card:{sku} -->"
    end = f"<!-- /LISTINO:card:{sku} -->"
    pattern = re.compile(
        re.escape(start) + r"(.*?)" + re.escape(end),
        re.DOTALL,
    )

    def replacer(match: re.Match[str]) -> str:
        block = match.group(1)
        block = re.sub(
            r'(<span class="card-price">)[^<]*(</span>)',
            rf"\g<1>{price_text}\g<2>",
            block,
            count=1,
        )
        return start + block + end

    return pattern.sub(replacer, content)


def update_schema_price(content: str, price: float) -> str:
    return re.sub(
        r'("price":\s*")[^"]*(")',
        rf'\g<1>{price:.2f}\g<2>',
        content,
        count=1,
    )


def sync_html(rows: list[dict[str, str]]) -> None:
    by_sku = {r["sku"]: r for r in rows}
    touched: set[Path] = set()
    sku_pages = sku_pages_from_csv(rows)

    for sku, rel_path in sku_pages.items():
        row = by_sku.get(sku)
        if not row:
            continue
        path = ROOT / rel_path
        if not path.exists():
            print(f"  ! pagina mancante: {rel_path} ({sku})")
            continue

        price_raw = (row.get("prezzo_enduser_eur") or "").strip()
        if not price_raw or price_raw == "—" or row.get("pubblicabile", "").lower() != "true":
            continue

        price = float(price_raw.replace(",", "."))
        price_vis = fmt_eur(price)
        text = path.read_text(encoding="utf-8")
        original = text

        if f"<!-- LISTINO:sku:{sku} -->" in text:
            text = update_listino_block(text, sku, fmt_eur_symbol(price), NOTE_PUBBLICO)
        elif "buy-box-amount" in text:
            amount = f"A partire da {price_vis} €" if sku in PRICE_FROM_SKUS else f"{price_vis} €"
            text = re.sub(
                r'(<span class="buy-box-amount">)[^<]*(</span>)',
                rf"\g<1>{amount}\g<2>",
                text,
                count=1,
            )
        elif "product-price" in text:
            text = re.sub(
                r'(<span class="product-price">)[^<]*(</span>)',
                rf"\g<1>{fmt_eur_symbol(price)}\g<2>",
                text,
                count=1,
            )
            text = re.sub(
                r'(<span class="product-price-note">)[^<]*(</span>)',
                rf"\g<1>{NOTE_PUBBLICO}\g<2>",
                text,
                count=1,
            )

        if '"price"' in text:
            text = update_schema_price(text, price)

        if text != original:
            path.write_text(text, encoding="utf-8")
            touched.add(path)
            print(f"  OK {rel_path} <- {sku} ({price_vis} EUR)")

    for sku, (rel_path, _label) in CARD_MARKERS.items():
        row = by_sku.get(sku)
        if not row:
            continue
        price_raw = (row.get("prezzo_enduser_eur") or "").strip()
        if not price_raw or price_raw == "—":
            continue
        path = ROOT / rel_path
        if not path.exists():
            continue
        price = float(price_raw.replace(",", "."))
        text = path.read_text(encoding="utf-8")
        if f"<!-- LISTINO:card:{sku} -->" not in text:
            continue
        updated = update_card_block(text, sku, fmt_da_eur(price))
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            touched.add(path)
            print(f"  OK card {rel_path} <- {sku}")

    print(f"\nPagine aggiornate: {len(touched)}")


def main() -> None:
    if not CSV_PATH.exists():
        raise SystemExit(f"CSV non trovato: {CSV_PATH}")

    rows = read_csv()
    print(f"Letti {len(rows)} prodotti da CSV")

    data = generate_json(rows)
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Generato {JSON_PATH} ({len(data)} SKU pubblicabili)")

    print("\nSync HTML:")
    sync_html(rows)
    print("\nFatto.")


if __name__ == "__main__":
    main()
