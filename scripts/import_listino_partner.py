#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sincronizza prezzi Gold/End-User/spedizione dal PDF partner ufficiale."""
from __future__ import annotations

import csv
import re
import zipfile
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    raise SystemExit("Installa pypdf: pip install pypdf")

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "listini" / "interno" / "listino-master.csv"
PDF_UMANOIDI = Path(r"C:\Users\stell\Downloads\25112025_ListinoUmanoidi_Partner.pdf")
ZIP_QUADRUPEDI = Path(r"C:\Users\stell\Downloads\Fw_ Listini prezzi partner + schede tecniche Unitree.zip")

# PDF name (upper, prefix match) -> SKU
PDF_TO_SKU: list[tuple[str, str]] = [
    ("G1 AIR", "G1-AIR"),
    ("G1-U1", "G1-U1"),
    ("G1-U2", "G1-U2"),
    ("G1-U3 (DEX", "G1-U3"),
    ("G1-U4 (DEX 3-1 FORCE CONTROLLED - WITH TACTILE SENSORS - 43 DOF)", "G1-U4"),
    ("G1-U4 (DEX 3-1 FORCE CONTROLLED - WITH TACTILE SENSORS - 37 DOF)", "G1-U4-37DOF"),
    ("G1-U5", "G1-U5"),
    ("G1-U6", "G1-U6"),
    ("G1-U7", "G1-U7"),
    ("G1-U9", "G1-U9"),
    ("G1-U10", "G1-U10"),
    ("G1-COMP", "G1-COMP"),
    ("H2 AIR", "H2-AIR"),
    ("H2 EDU", "H2-EDU"),
    ("R1 AIR", "R1-AIR"),
    ("R1-U1", "R1-U1"),
    ("R1-U2", "R1-U2"),
    ("R1-U3", "R1-U3"),
    ("R1-U4", "R1-U4"),
    ("R1-U5", "R1-U5"),
    ("R1-U6", "R1-U6"),
    ("G1 REMOTE CONTROLLER", "G1-REMOTE"),
    ("G1 BATTERY CHARGER", "G1-CHARGER"),
    ("G1 BATTERY", "G1-BATTERY"),
    ("G1 PROTECTION FRAME", "G1-FRAME"),
    ("HAND DEX3-1 WHITOUT", "HAND-DEX3-1-NO-TAC"),
    ("HAND DEX3-1 WHIT TACTILE", "HAND-DEX3-1-TAC"),
    ("DEXTEROUS HAND 5 FINGERS WHITOUT", "HAND-FINGERS-NO-TAC"),
    ("DEXTEROUS HAND 5 FINGERS WHIT TACTILE", "HAND-FINGERS-TAC"),
    ("BIONIC REVO 2 BASIC", "BIONIC-REVO2-BASIC"),
    ("H2 REMOTE CONTROLLER", "H2-REMOTE"),
    ("H2 BATTERY (SINGLE)", "H2-BATTERY"),
    ("H2 FAST CHARGER", "H2-CHARGER-FAST"),
    ("H2 DEDICATED INTEL CORE I8", "H2-COMPUTE-I8"),
    ("H2 DEDICATED NVIDIA JETSON NX ORIN", "H2-COMPUTE-ORIN-NX"),
    ("H2 DEDICATED NVIDIA JETSON AGX ORIN", "H2-COMPUTE-AGX-ORIN"),
    ("H2 DEDICATED NVIDIA JETSON AGX THOR", "H2-COMPUTE-AGX-THOR"),
    ("H2 DEDICATED DEX5-1 FIVE-FINGER", "H2-HAND-DEX5"),
    ("H2 DEDICATED DEX5-1P", "H2-HAND-DEX5P"),
    ("H2 DEDICATED DEX3-1 FORCE-CONTROL THREE-FINGER DEXTEROUS HAND (TACTILE", "H2-HAND-DEX3-TAC"),
    ("H2 DEDICATED DEX3-1 FORCE-CONTROL THREE-FINGER DEXTEROUS HAND", "H2-HAND-DEX3"),
    ("H2 DEDICATED INSPIER DFQ", "H2-HAND-INSPIRE-DFQ"),
    ("H2 DEDICATED INSPIER FTP", "H2-HAND-INSPIRE-FTP"),
    ("H2 DEDICATED BRAINCO BIONIC DEXTEROUS HAND REVO 2 TACTILE EDITION", "H2-HAND-REVO2-TACTILE"),
    ("H2 DEDICATED BRAINCO BIONIC DEXTEROUS HAND REVO 2 BASIC EDITION", "H2-HAND-REVO2-BASIC"),
    ("H2 DEDICATED DEX1-1 GRIPPER STANDARD", "H2-GRIPPER-DEX1-STD"),
    ("H2 DEDICATED DEX1-1 GRIPPER ADVANCED", "H2-GRIPPER-DEX1-ADV"),
    ("H2 DEDICATED DEX1-1 GRIPPER FLAGSHIP", "H2-GRIPPER-DEX1-FLAG"),
    ("R1 REMOTE CONTROLLER", "R1-REMOTE"),
    ("R1 BATTERY (SINGLE)", "R1-BATTERY"),
    ("R1 CHARGER", "R1-CHARGER"),
    ("R1 PROTECTION FRAME", "R1-FRAME"),
    ("R1 HAND DEX3-1 (NO", "R1-HAND-DEX3-NO-TAC"),
    ("R1 HAND DEX3-1 (CON", "R1-HAND-DEX3-TAC"),
    ("R1 BRAINCO BIONIC REVO 2 BASIC", "R1-REVO2-BASIC"),
    ("R1 BRAINCO BIONIC REVO 2 HAPTIC", "R1-REVO2-HAPTIC"),
    ("GO2 AIR PACKAGE", "GO2-AIR"),
    ("GO2 PRO PACKAGE", "GO2-PRO"),
    ("GO EDU STANDARD", "GO2-EDU-STD"),
    ("GO2 EDU SMART", "GO2-EDU-SMART"),
    ("GO2 EDU LASER SMART", "GO2-EDU-LASER"),
    ("GO2 EDU ULTIMATE", "GO2-EDU-ULT"),
    ("GO2W-U1", "GO2W-U1"),
    ("GO2W-U2", "GO2W-U2"),
    ("GO2W-U3", "GO2W-U3"),
    ("GO2W-U4", "GO2W-U4"),
    ("GO2W-U5", "GO2W-U5"),
    ("B2 B2 + LIDAR", "B2-LIDAR"),
    ("B2 B2", "B2"),
    ("B2-W B2W + LIDAR", "B2W-LIDAR"),
    ("B2-W B2W", "B2W"),
    ("A2 STANDARD", "A2-STD"),
    ("A2 PRO", "A2-PRO"),
    ("A2-W STANDARD", "A2W-STD"),
    ("A2-W PRO", "A2W-PRO"),
    ("GO2 REMOTE CONTROLLER", "GO2-REMOTE"),
    ("GO2 SELF-CHARGING BOARD", "GO2-SELF-CHARGE"),
    ("D1 ROBOTIC ARM", "D1-ARM"),
    ("GO2 BATTERY LONG RANGE", "GO2-BATT-LR"),
    ("GO2 BATTERY STANDARD", "GO2-BATT-STD"),
    ("GO2 CHARGER STANDARD", "GO2-CHARGER-STD"),
    ("GO2 CHARGER FAST", "GO2-CHARGER-FAST"),
    ("GO2 FOOT PAD", "GO2-FOOT-PAD"),
    ("ARM Z1 AIR", "ARM-Z1-AIR"),
    ("ARM Z1 PRO", "ARM-Z1-PRO"),
    ("Z1 STANDARD GRIPPER", "Z1-GRIPPER-STD"),
    ("Z1 GRIPPER + D435", "Z1-GRIPPER-D435I"),
    ("Z1 GRIPPER + D405", "Z1-GRIPPER-D405"),
    ("B2 CONTROLLER", "B2-CONTROLLER"),
    ("B2 STANDARD BATTERY", "B2-BATT-STD"),
    ("B2 BATTERY LOW TEMPERATURE", "B2-BATT-LOW-T"),
    ("B2 BATTERY HIGH TEMPERATURE", "B2-BATT-HIGH-T"),
    ("B2 FOOT PAD", "B2-FOOT-PAD"),
    ("PROTECTION FRAME", "B2-FRAME"),
    ("HELIOS 5515", "HELIOS-5515"),
    ("ORIN NX EXTERNAL UPGRADE", "ORIN-NX-UPGRADE"),
    ("B2 CHARGING BOARD", "B2-CHARGING-BOARD"),
    ("A2 CONTROLLER", "A2-CONTROLLER"),
    ("A2 BATTERIA", "A2-BATTERY"),
    ("A2 CARICATORE", "A2-CHARGER"),
]

# SKU -> metadata for new rows
NEW_SKU_META: dict[str, dict] = {
    "H2-AIR": {"categoria": "UMANOIDI", "nome": "H2 AIR", "pubblicabile": "true", "pagina_sito": "prodotti/unitree-h2-air.html", "stato_sito": "pubblicato", "note": "Listino partner 25/11/2025"},
    "H2-EDU": {"categoria": "UMANOIDI", "nome": "H2 EDU", "pubblicabile": "true", "pagina_sito": "prodotti/unitree-h2.html", "stato_sito": "pubblicato", "note": "Scheda ricca esistente"},
    "R1-AIR": {"categoria": "UMANOIDI", "nome": "R1 AIR", "pubblicabile": "true", "pagina_sito": "prodotti/unitree-r1-air.html", "stato_sito": "pubblicato", "note": "Sostituisce B1-AIR errato"},
    "H2-REMOTE": {"categoria": "COMPONENTISTICA", "nome": "H2 REMOTE CONTROLLER", "pubblicabile": "true"},
    "H2-BATTERY": {"categoria": "COMPONENTISTICA", "nome": "H2 BATTERY (Single)", "pubblicabile": "true"},
    "H2-CHARGER-FAST": {"categoria": "COMPONENTISTICA", "nome": "H2 FAST CHARGER", "pubblicabile": "true"},
    "H2-COMPUTE-I8": {"categoria": "COMPONENTISTICA", "nome": "H2 Intel Core i8 Computing Board", "pubblicabile": "true"},
    "H2-COMPUTE-ORIN-NX": {"categoria": "COMPONENTISTICA", "nome": "H2 Jetson Orin NX Computing Board", "pubblicabile": "true"},
    "H2-COMPUTE-AGX-ORIN": {"categoria": "COMPONENTISTICA", "nome": "H2 Jetson AGX Orin Computing Board", "pubblicabile": "true"},
    "H2-COMPUTE-AGX-THOR": {"categoria": "COMPONENTISTICA", "nome": "H2 Jetson AGX Thor Computing Board", "pubblicabile": "true"},
    "H2-HAND-DEX5": {"categoria": "MANI_BRACCI", "nome": "H2 Dex5-1 Five-Finger Hand", "pubblicabile": "true"},
    "H2-HAND-DEX5P": {"categoria": "MANI_BRACCI", "nome": "H2 Dex5-1P Five-Finger Hand", "pubblicabile": "true"},
    "H2-HAND-DEX3": {"categoria": "MANI_BRACCI", "nome": "H2 Dex3-1 Force-Control Hand", "pubblicabile": "true"},
    "H2-HAND-DEX3-TAC": {"categoria": "MANI_BRACCI", "nome": "H2 Dex3-1 Hand (Tactile)", "pubblicabile": "true"},
    "H2-HAND-INSPIRE-DFQ": {"categoria": "MANI_BRACCI", "nome": "H2 Inspire DFQ Dexterous Hand", "pubblicabile": "true"},
    "H2-HAND-INSPIRE-FTP": {"categoria": "MANI_BRACCI", "nome": "H2 Inspire FTP Dexterous Hand", "pubblicabile": "true"},
    "H2-HAND-REVO2-BASIC": {"categoria": "MANI_BRACCI", "nome": "H2 BrainCo REVO 2 Basic Hand", "pubblicabile": "true"},
    "H2-HAND-REVO2-TACTILE": {"categoria": "MANI_BRACCI", "nome": "H2 BrainCo REVO 2 Tactile Hand", "pubblicabile": "true"},
    "H2-GRIPPER-DEX1-STD": {"categoria": "MANI_BRACCI", "nome": "H2 Dex1-1 Gripper Standard", "pubblicabile": "true"},
    "H2-GRIPPER-DEX1-ADV": {"categoria": "MANI_BRACCI", "nome": "H2 Dex1-1 Gripper Advanced", "pubblicabile": "true"},
    "H2-GRIPPER-DEX1-FLAG": {"categoria": "MANI_BRACCI", "nome": "H2 Dex1-1 Gripper Flagship", "pubblicabile": "true"},
}

# SKU non presenti nel PDF partner — prezzi/manual da unitree.com
MANUAL_SKUS: dict[str, dict] = {
    "R1-D": {
        "categoria": "UMANOIDI",
        "nome_prodotto": "Dual-Arm Humanoid Robot (R1-D)",
        "prezzo_gold_eur": "8571,43",
        "prezzo_enduser_eur": "12000,00",
        "spedizione_eur": "500,00",
        "note": "SKU unico Abra. Configurazioni Unitree: R1-A5/A7/A5-D/A7-D (scheda ufficiale, non SKU separati). Prezzo indicativo; Unitree from $4290",
        "pubblicabile": "true",
        "pagina_sito": "prodotti/unitree-r1-d.html",
        "stato_sito": "pubblicato",
    },
}

DEPRECATE_SKUS = {
    "H1-S", "H1", "H1-M", "B1-AIR",
    "H1S-HAND-TOP", "H1M-HAND-TOP",
    "H1-REMOTE", "H1-BATTERY", "H1-CHARGER-FAST",
    "H1-COMPUTE-100T", "H1-COMPUTE-200T", "H1-FRAME",
}


def fmt_eur(v: float) -> str:
    return f"{v:.2f}".replace(".", ",")


def parse_pdf(path: Path) -> dict[str, dict]:
    text = "".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
    out: dict[str, dict] = {}
    for line in text.split("\n"):
        line = line.strip()
        nums = re.findall(r"(\d{1,3}(?:\.\d{3})*,\d{2})", line)
        if len(nums) < 5:
            continue
        # Nome prima del primo prezzo (evita troncamento su "Revo 2", "37 DOF", ecc.)
        pos = line.find(nums[0])
        name = line[:pos].strip().upper() if pos > 0 else line.strip().upper()
        out[name] = {
            "gold": float(nums[0].replace(".", "").replace(",", ".")),
            "pub": float(nums[3].replace(".", "").replace(",", ".")),
            "ship": float(nums[4].replace(".", "").replace(",", ".")),
            "raw": line,
        }
    return out


def match_sku(pdf_name: str) -> str | None:
    upper = pdf_name.upper()
    for prefix, sku in sorted(PDF_TO_SKU, key=lambda x: -len(x[0])):
        if upper.startswith(prefix.upper()):
            return sku
    return None


def load_prices() -> dict[str, dict]:
    prices: dict[str, dict] = {}
    if not PDF_UMANOIDI.exists():
        raise FileNotFoundError(f"Manca PDF umanoidi: {PDF_UMANOIDI}")
    for name, data in parse_pdf(PDF_UMANOIDI).items():
        sku = match_sku(name)
        if sku:
            prices[sku] = {**data, "pdf_name": name}

    quad_path = None
    if ZIP_QUADRUPEDI.exists():
        with zipfile.ZipFile(ZIP_QUADRUPEDI) as zf:
            for n in zf.namelist():
                if "Quadrupedi" in n and n.endswith(".pdf"):
                    quad_path = ROOT / "listini" / "interno" / "_tmp_quadrupedi.pdf"
                    quad_path.write_bytes(zf.read(n))
                    break
    if quad_path and quad_path.exists():
        for name, data in parse_pdf(quad_path).items():
            sku = match_sku(name)
            if sku:
                prices[sku] = {**data, "pdf_name": name}
        quad_path.unlink(missing_ok=True)
    return prices


def read_csv() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def write_csv(rows: list[dict]) -> None:
    fields = ["categoria", "sku", "nome_prodotto", "prezzo_gold_eur", "prezzo_enduser_eur",
              "spedizione_eur", "note", "pubblicabile", "pagina_sito", "stato_sito"]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    prices = load_prices()
    rows = read_csv()
    by_sku = {r["sku"]: r for r in rows}
    updated = 0

    # Deprecate H1/B1
    new_rows = []
    for row in rows:
        sku = row["sku"]
        if sku in DEPRECATE_SKUS:
            continue
        if sku in prices:
            p = prices[sku]
            row["prezzo_gold_eur"] = fmt_eur(p["gold"])
            row["prezzo_enduser_eur"] = fmt_eur(p["pub"])
            row["spedizione_eur"] = fmt_eur(p["ship"])
            updated += 1
        new_rows.append(row)
        by_sku[sku] = row

    # Add new SKUs from PDF
    for sku, meta in NEW_SKU_META.items():
        if sku in by_sku:
            continue
        if sku not in prices:
            print(f"  WARN: {sku} non trovato nel PDF")
            continue
        p = prices[sku]
        new_rows.append({
            "categoria": meta["categoria"],
            "sku": sku,
            "nome_prodotto": meta["nome"],
            "prezzo_gold_eur": fmt_eur(p["gold"]),
            "prezzo_enduser_eur": fmt_eur(p["pub"]),
            "spedizione_eur": fmt_eur(p["ship"]),
            "note": meta.get("note", "Listino partner 25/11/2025"),
            "pubblicabile": meta.get("pubblicabile", "true"),
            "pagina_sito": meta.get("pagina_sito", ""),
            "stato_sito": meta.get("stato_sito", "mancante"),
        })
        updated += 1

    # Fix specific pubblicabile flags from plan
    for row in new_rows:
        sku = row["sku"]
        if sku == "R1-BATTERY":
            row["pubblicabile"] = "true"
            row["prezzo_enduser_eur"] = fmt_eur(prices["R1-BATTERY"]["pub"]) if "R1-BATTERY" in prices else row["prezzo_enduser_eur"]
        if sku == "GO2-EDU-LASER" and "GO2-EDU-LASER" in prices:
            row["pubblicabile"] = "true"
            row["prezzo_enduser_eur"] = fmt_eur(prices["GO2-EDU-LASER"]["pub"])
        if sku == "A2-CHARGER" and "A2-CHARGER" in prices:
            row["pubblicabile"] = "true"
            row["prezzo_enduser_eur"] = fmt_eur(prices["A2-CHARGER"]["pub"])
        if sku == "GO2W-U1" and "GO2W-U1" in prices:
            row["prezzo_gold_eur"] = fmt_eur(prices["GO2W-U1"]["gold"])
            # resta non pubblicabile (gold ok)

    # SKU manuali (es. R1-D da unitree.com, assente nel PDF partner)
    by_sku_final = {r["sku"]: r for r in new_rows}
    for sku, meta in MANUAL_SKUS.items():
        by_sku_final[sku] = {"sku": sku, **meta}
    new_rows = list(by_sku_final.values())

    write_csv(new_rows)
    print(f"Aggiornati {updated} SKU da PDF partner")
    if MANUAL_SKUS:
        print(f"SKU manuali: {', '.join(MANUAL_SKUS)}")
    print(f"Righe CSV: {len(new_rows)} (rimossi {len(DEPRECATE_SKUS)} SKU H1/B1)")
    missing = [s for s in prices if s not in {r["sku"] for r in new_rows}]
    if missing:
        print("PDF senza riga CSV:", ", ".join(sorted(missing)[:20]))


if __name__ == "__main__":
    main()
