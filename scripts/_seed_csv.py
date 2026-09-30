#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera listino-master.csv con tutti i 92 SKU (eseguire una volta)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "listini" / "interno" / "listino-master.csv"

PAGE_MAP = {
    "G1-AIR": ("prodotti/unitree-g1.html", "pubblicato"),
    "G1-U1": ("prodotti/unitree-g1-edu-standard.html", "pubblicato"),
    "G1-U2": ("prodotti/unitree-g1-edu-plus.html", "pubblicato"),
    "G1-U3": ("prodotti/unitree-g1-edu-ultimate-a.html", "pubblicato"),
    "G1-U4": ("prodotti/unitree-g1-edu-ultimate-b.html", "pubblicato"),
    "G1-U5": ("prodotti/unitree-g1-edu-ultimate-c.html", "pubblicato"),
    "G1-U6": ("prodotti/unitree-g1-edu-ultimate-d.html", "pubblicato"),
    "G1-U7": ("prodotti/unitree-g1-edu-ultimate-e.html", "pubblicato"),
    "G1-COMP": ("prodotti/unitree-g1-comp.html", "pubblicato"),
    "H1-S": ("prodotti/unitree-h2.html", "presente"),
    "H1": ("prodotti/unitree-h2.html", "presente"),
    "H1-M": ("", "mancante"),
    "R1-U1": ("prodotti/unitree-r1-edu.html", "pubblicato"),
    "R1-U3": ("universita-ricerca.html", "presente"),
    "GO2-AIR": ("", "mancante"),
    "GO2-PRO": ("prodotti/unitree-go2-pro.html", "pubblicato"),
    "GO2-EDU-STD": ("prodotti/unitree-go2-edu.html", "pubblicato"),
    "GO2-EDU-SMART": ("prodotti/unitree-go2-edu-smart.html", "pubblicato"),
    "GO2-EDU-ULT": ("prodotti/unitree-go2-enterprise-u2.html", "pubblicato"),
    "A2-STD": ("prodotti/unitree-a2.html", "pubblicato"),
    "A2-PRO": ("prodotti/unitree-a2-pro.html", "pubblicato"),
    "B2": ("universita-ricerca.html", "presente"),
    "B2-LIDAR": ("prodotti/unitree-b2.html", "pubblicato"),
}

PRODUCTS = [
    # UMANOIDI (41)
    ("UMANOIDI", "G1-AIR", "G1 AIR", None, 23997.41, 2000.00, "Mapping G1 Base sito → G1 AIR", True),
    ("UMANOIDI", "G1-U1", "G1-U1 (Expansion Dock 100Tflops - 23 DOF)", None, 37562.52, 2000.00, "", True),
    ("UMANOIDI", "G1-U2", "G1-U2 (Waist 3 DOF, single arm 7 DOF, 100Tflops - 29 DOF)", None, 45783.80, 2000.00, "", True),
    ("UMANOIDI", "G1-U3", "G1-U3 (DEX 3-1 Force controlled, no tactile - 43 DOF)", None, 50489.93, 2000.00, "", True),
    ("UMANOIDI", "G1-U4", "G1-U4 (DEX 3-1 Force controlled with tactile - 43 DOF)", None, 62226.36, 2000.00, "", True),
    ("UMANOIDI", "G1-U5", "G1-U5 (Five fingers INSPIRE ROBOTS RH56DFQ - no tactile)", None, 62226.36, 2000.00, "", True),
    ("UMANOIDI", "G1-U6", "G1-U6 (Five fingers INSPIRE ROBOTS RH56DFTP - with tactile)", None, 67707.21, 2000.00, "", True),
    ("UMANOIDI", "G1-U7", "G1-U7 (Powerful five finger REVO 2 Basic - 37 DOF)", None, 56745.51, 2000.00, "", True),
    ("UMANOIDI", "G1-U9", "G1-U9 (DEX 3-1 Force controlled, no tactile - 37 DOF)", None, 51264.65, 2000.00, "", True),
    ("UMANOIDI", "G1-U4-37DOF", "G1-04 (DEX 3-1 Force controlled with tactile - 37 DOF)", None, 54005.08, 2000.00, "Possibile typo G1-U4 nel listino fornitore", True),
    ("UMANOIDI", "G1-U10", "G1-U10 (Powerful five finger REVO 2 Basic - 35 DOF)", None, 46534.23, 2000.00, "", True),
    ("UMANOIDI", "G1-COMP", "G1-COMP", None, 41673.16, 2000.00, "", True),
    ("UMANOIDI", "H1-S", "H1-S", None, 95804.28, 2500.00, "Sito mostra H2 EDU — H1 non distribuito come H2 in IT", True),
    ("UMANOIDI", "H1", "H1", None, 95804.28, 2500.00, "Sito mostra H2 EDU", True),
    ("UMANOIDI", "H1-M", "H1-M", None, 114905.14, 3000.00, "", True),
    ("UMANOIDI", "B1-AIR", "B1 AIR", None, 10158.26, 2000.00, "", True),
    ("UMANOIDI", "R1-U1", "R1-U1 (Expansion Dock 100Tflops - 23 DOF)", None, 16461.24, 2000.00, "Pagina R1 EDU Standard", True),
    ("UMANOIDI", "R1-U2", "R1-U2 (Waist 3 DOF, single arm 7 DOF, 100Tflops - 29 DOF)", None, 19544.22, 2000.00, "", True),
    ("UMANOIDI", "R1-U3", "R1 / R1-U3 (DEX 3-1 Force controlled, no tactile - 43 DOF)", None, 32287.20, 2000.00, "Card università R1 EDU", True),
    ("UMANOIDI", "R1-U4", "R1-U4 (DEX 3-1 Force controlled with tactile - 43 DOF)", None, 35027.63, 2000.00, "", True),
    ("UMANOIDI", "R1-U5", "R1-U5 (Five fingers BRAINCO BIONIC REVO 2 - no tactile)", None, 29546.77, 2000.00, "", True),
    ("UMANOIDI", "R1-U6", "R1-U6 (Five fingers BRAINCO BIONIC REVO 2 - with tactile)", None, 35027.63, 2000.00, "", True),
    ("UMANOIDI", "GO2-AIR", "GO2 AIR PACKAGE", None, 2718.47, 500.00, "", True),
    ("UMANOIDI", "GO2-PRO", "GO2 PRO PACKAGE", None, 4043.76, 500.00, "", True),
    ("UMANOIDI", "GO2-EDU-STD", "GO2 EDU STANDARD", None, 12799.48, 500.00, "", True),
    ("UMANOIDI", "GO2-EDU-SMART", "GO2 EDU SMART", None, 15450.06, 500.00, "Mapping Go2 EDU+ sito → SMART", True),
    ("UMANOIDI", "GO2-EDU-LASER", "GO2 EDU LASER SMART (+ LIVOX MID 360)", None, None, 700.00, "Non spec. / Coming soon", False),
    ("UMANOIDI", "GO2-EDU-ULT", "GO2 EDU ULTIMATE VERSION (+ HESAI XT16)", None, 20075.00, 700.00, "", True),
    ("UMANOIDI", "GO2W-U1", "GO2W-U1", None, 18717.85, 700.00, "", False),
    ("UMANOIDI", "GO2W-U2", "GO2W-U2", None, 24784.30, 700.00, "", True),
    ("UMANOIDI", "GO2W-U3", "GO2W-U3 (+ LIVOX MID360)", None, 28724.90, 700.00, "", True),
    ("UMANOIDI", "GO2W-U4", "GO2W-U4 (+ HESAI XT16)", None, 33909.90, 700.00, "", True),
    ("UMANOIDI", "GO2W-U5", "GO2W-U5 (+ HESAI XT16 & Camera Gimbal)", None, 38809.53, 700.00, "", True),
    ("UMANOIDI", "B2", "B2", None, 76076.34, 2500.00, "Card università B2", True),
    ("UMANOIDI", "B2-LIDAR", "B2+LIDAR", None, 77954.23, 2500.00, "Scheda unitree-b2.html", True),
    ("UMANOIDI", "B2W", "B2W", None, 80283.58, 2500.00, "", True),
    ("UMANOIDI", "B2W-LIDAR", "B2W+LIDAR", None, 100188.74, 2800.00, "", True),
    ("UMANOIDI", "A2-STD", "A2 STANDARD", None, 30648.48, 2000.00, "", True),
    ("UMANOIDI", "A2-PRO", "A2 PRO", None, 41673.16, 2000.00, "", True),
    ("UMANOIDI", "A2W-STD", "A2-W STANDARD", None, 38247.63, 2000.00, "", True),
    ("UMANOIDI", "A2W-PRO", "A2-W PRO", None, 48524.23, 2000.00, "", True),
    # MANI (16)
    ("MANI_BRACCI", "HAND-DEX3-1-NO-TAC", "HAND DEX3-1 WITHOUT TACTILE (Single)", None, 10577.40, 200.00, "", True),
    ("MANI_BRACCI", "HAND-DEX3-1-TAC", "HAND DEX3-1 WITH TACTILE (Single)", None, 12806.96, 200.00, "", True),
    ("MANI_BRACCI", "HAND-FINGERS-NO-TAC", "DEXTEROUS HAND FINGERS WITHOUT TACTILE (Single)", None, 13118.05, 500.00, "", True),
    ("MANI_BRACCI", "HAND-FINGERS-TAC", "DEXTEROUS HAND FINGERS WITH TACTILE (Single)", None, 14725.40, 500.00, "", True),
    ("MANI_BRACCI", "BIONIC-REVO2-BASIC", "BIONIC REVO 2 BASIC (No sensori tattili)", None, 5791.95, 300.00, "", True),
    ("MANI_BRACCI", "H1S-HAND-TOP", "H1-S DEXTEROUS HAND (Single) TOP", None, 14103.00, 500.00, "", True),
    ("MANI_BRACCI", "H1M-HAND-TOP", "H1-M DEXTEROUS HAND (Single) TOP", None, 14103.20, 500.00, "", True),
    ("MANI_BRACCI", "ARM-Z1-AIR", "ARM Z1 AIR", None, 9450.21, 400.00, "", True),
    ("MANI_BRACCI", "ARM-Z1-PRO", "ARM Z1 PRO", None, 12001.61, 400.00, "", True),
    ("MANI_BRACCI", "Z1-GRIPPER-STD", "Z1 STANDARD GRIPPER", None, 2107.17, 50.00, "", True),
    ("MANI_BRACCI", "Z1-GRIPPER-D435I", "Z1 GRIPPER + D435I CAMERA", None, 3477.38, 50.00, "", True),
    ("MANI_BRACCI", "Z1-GRIPPER-D405", "Z1 GRIPPER + D405 CAMERA", None, 3477.38, 50.00, "", True),
    ("MANI_BRACCI", "R1-HAND-DEX3-NO-TAC", "R1 HAND DEX3-1 (No sensori tattili)", None, 6889.99, 500.00, "", True),
    ("MANI_BRACCI", "R1-HAND-DEX3-TAC", "R1 HAND DEX3-1 (Con sensori tattili)", None, 8200.20, 500.00, "", True),
    ("MANI_BRACCI", "R1-REVO2-BASIC", "R1 BrainCo BIONIC REVO 2 BASIC (No sensori)", None, 5312.38, 300.00, "", True),
    ("MANI_BRACCI", "R1-REVO2-HAPTIC", "R1 BrainCo BIONIC REVO 2 HAPTIC (Con sensori)", None, 8052.80, 300.00, "", True),
    # COMPONENTISTICA (35)
    ("COMPONENTISTICA", "G1-REMOTE", "G1 REMOTE CONTROLLER", None, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "G1-BATTERY", "G1 BATTERY", None, 925.83, 100.00, "", True),
    ("COMPONENTISTICA", "G1-CHARGER", "G1 BATTERY CHARGER", None, 188.87, 50.00, "", True),
    ("COMPONENTISTICA", "G1-FRAME", "G1 PROTECTION FRAME", None, 618.46, 200.00, "", True),
    ("COMPONENTISTICA", "H1-REMOTE", "H1 REMOTE CONTROLLER", None, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "H1-BATTERY", "H1 BATTERY (Single)", None, 2162.76, 500.00, "", True),
    ("COMPONENTISTICA", "H1-CHARGER-FAST", "H1 FAST CHARGER", None, 304.40, 50.00, "", True),
    ("COMPONENTISTICA", "H1-COMPUTE-100T", "H1 100 TFLOP COMPUTING MODULE", None, 5243.87, 300.00, "", True),
    ("COMPONENTISTICA", "H1-COMPUTE-200T", "H1 200TFLOP COMPUTING MODULE", None, 10176.64, 300.00, "", True),
    ("COMPONENTISTICA", "H1-FRAME", "H1 PROTECTION FRAME", None, 1472.74, 300.00, "", True),
    ("COMPONENTISTICA", "R1-REMOTE", "R1 REMOTE CONTROLLER", None, 445.05, 100.00, "", True),
    ("COMPONENTISTICA", "R1-BATTERY", "R1 BATTERY (Single)", None, None, 500.00, "Non spec.", False),
    ("COMPONENTISTICA", "R1-CHARGER", "R1 CHARGER", None, 188.87, 50.00, "", True),
    ("COMPONENTISTICA", "R1-FRAME", "R1 PROTECTION FRAME (Incluso in EDU)", None, 482.91, 50.00, "", True),
    ("COMPONENTISTICA", "GO2-REMOTE", "GO2 REMOTE CONTROLLER", None, 448.27, 100.00, "", True),
    ("COMPONENTISTICA", "GO2-SELF-CHARGE", "GO2 SELF-CHARGING BOARD", None, 1074.69, 100.00, "", True),
    ("COMPONENTISTICA", "D1-ARM", "D1 ROBOTIC ARM", None, 5140.17, 200.00, "", True),
    ("COMPONENTISTICA", "GO2-BATT-LR", "GO2 BATTERY LONG RANGE", None, None, 100.00, "Non spec.", False),
    ("COMPONENTISTICA", "GO2-BATT-STD", "GO2 BATTERY STANDARD", None, None, 100.00, "Non spec.", False),
    ("COMPONENTISTICA", "GO2-CHARGER-STD", "GO2 CHARGER STANDARD", None, 131.37, 50.00, "", True),
    ("COMPONENTISTICA", "GO2-CHARGER-FAST", "GO2 CHARGER FAST", None, 219.72, 50.00, "", True),
    ("COMPONENTISTICA", "GO2-FOOT-PAD", "GO2 FOOT PAD", None, 103.90, 50.00, "", True),
    ("COMPONENTISTICA", "B2-CONTROLLER", "B2 CONTROLLER", None, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "B2-BATT-STD", "B2 STANDARD BATTERY", None, 4940.24, 800.00, "", True),
    ("COMPONENTISTICA", "B2-BATT-LOW-T", "B2 BATTERY LOW TEMPERATURE", None, 4940.24, 800.00, "", True),
    ("COMPONENTISTICA", "B2-BATT-HIGH-T", "B2 BATTERY HIGH TEMPERATURE", None, 7680.67, 800.00, "", True),
    ("COMPONENTISTICA", "B2-FOOT-PAD", "B2 FOOT PAD", None, 185.91, 100.00, "", True),
    ("COMPONENTISTICA", "B2-FRAME", "B2 PROTECTION FRAME", None, 549.06, 200.00, "", True),
    ("COMPONENTISTICA", "HELIOS-5515", "HELIOS 5515 LIDAR", None, 11169.11, 200.00, "", True),
    ("COMPONENTISTICA", "ORIN-NX-UPGRADE", "ORIN NX EXTERNAL UPGRADE", None, 4214.34, 100.00, "", True),
    ("COMPONENTISTICA", "B2-CHARGING-BOARD", "B2-CHARGING BOARD", None, 5684.55, 100.00, "", True),
    ("COMPONENTISTICA", "A2-CONTROLLER", "A2 CONTROLLER", None, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "A2-BATTERY", "A2 BATTERIA", None, 1473.91, 100.00, "", True),
    ("COMPONENTISTICA", "A2-CHARGER", "A2 CARICATORE", None, None, 100.00, "Non spec.", False),
    ("COMPONENTISTICA", "A2-EXPANSION", "A2 EXPANSION DOCK", None, None, None, "Coming soon", False),
]

FIELDS = [
    "categoria", "sku", "nome_prodotto", "prezzo_gold_eur", "prezzo_enduser_eur",
    "spedizione_eur", "note", "pubblicabile", "pagina_sito", "stato_sito",
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for cat, sku, nome, gold, enduser, ship, note, pub in PRODUCTS:
        pagina, stato = PAGE_MAP.get(sku, ("", "mancante"))
        if pagina and stato == "mancante":
            stato = "presente"
        rows.append({
            "categoria": cat,
            "sku": sku,
            "nome_prodotto": nome,
            "prezzo_gold_eur": "" if gold is None else f"{gold:.2f}".replace(".", ","),
            "prezzo_enduser_eur": "" if enduser is None else f"{enduser:.2f}".replace(".", ","),
            "spedizione_eur": "" if ship is None else f"{ship:.2f}".replace(".", ","),
            "note": note,
            "pubblicabile": "true" if pub else "false",
            "pagina_sito": pagina,
            "stato_sito": stato,
        })

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter=";")
        w.writeheader()
        w.writerows(rows)

    print(f"Scritti {len(rows)} prodotti in {OUT}")


if __name__ == "__main__":
    main()
