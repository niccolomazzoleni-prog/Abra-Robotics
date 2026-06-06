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
    "GO2-EDU-SMART": ("prodotti/unitree-go2-edu-plus.html", "pubblicato"),
    "GO2-EDU-ULT": ("prodotti/unitree-go2-enterprise-u2.html", "pubblicato"),
    "A2-STD": ("prodotti/unitree-a2.html", "pubblicato"),
    "A2-PRO": ("prodotti/unitree-a2-pro.html", "pubblicato"),
    "B2": ("universita-ricerca.html", "presente"),
    "B2-LIDAR": ("prodotti/unitree-b2.html", "pubblicato"),
}

PRODUCTS = [
    # UMANOIDI (41)
    ("UMANOIDI", "G1-AIR", "G1 AIR", 16210.38, 23997.41, 2000.00, "Mapping G1 Base sito → G1 AIR", True),
    ("UMANOIDI", "G1-U1", "G1-U1 (Expansion Dock 100Tflops - 23 DOF)", 24957.27, 37562.52, 2000.00, "", True),
    ("UMANOIDI", "G1-U2", "G1-U2 (Waist 3 DOF, single arm 7 DOF, 100Tflops - 29 DOF)", 30258.42, 45783.80, 2000.00, "", True),
    ("UMANOIDI", "G1-U3", "G1-U3 (DEX 3-1 Force controlled, no tactile - 43 DOF)", 39093.66, 50489.93, 2000.00, "", True),
    ("UMANOIDI", "G1-U4", "G1-U4 (DEX 3-1 Force controlled with tactile - 43 DOF)", 40860.70, 62226.36, 2000.00, "", True),
    ("UMANOIDI", "G1-U5", "G1-U5 (Five fingers INSPIRE ROBOTS RH56DFQ - no tactile)", 40860.70, 62226.36, 2000.00, "", True),
    ("UMANOIDI", "G1-U6", "G1-U6 (Five fingers INSPIRE ROBOTS RH56DFTP - with tactile)", 44394.80, 67707.21, 2000.00, "", True),
    ("UMANOIDI", "G1-U7", "G1-U7 (Powerful five finger REVO 2 Basic - 37 DOF)", 37326.61, 56745.51, 2000.00, "", True),
    ("UMANOIDI", "G1-U9", "G1-U9 (DEX 3-1 Force controlled, no tactile - 37 DOF)", 33792.51, 51264.65, 2000.00, "", True),
    ("UMANOIDI", "G1-U4-37DOF", "G1-04 (DEX 3-1 Force controlled with tactile - 37 DOF)", 35559.56, 54005.08, 2000.00, "Possibile typo G1-U4 nel listino fornitore", True),
    ("UMANOIDI", "G1-U10", "G1-U10 (Powerful five finger REVO 2 Basic - 35 DOF)", 32025.46, 46534.23, 2000.00, "", True),
    ("UMANOIDI", "G1-COMP", "G1-COMP", 27607.84, 41673.16, 2000.00, "", True),
    ("UMANOIDI", "H1-S", "H1-S", 82021.31, 95804.28, 2500.00, "Sito mostra H2 EDU — H1 non distribuito come H2 in IT", True),
    ("UMANOIDI", "H1", "H1", 88483.10, 95804.28, 2500.00, "Sito mostra H2 EDU", True),
    ("UMANOIDI", "H1-M", "H1-M", 100298.64, 114905.14, 3000.00, "", True),
    ("UMANOIDI", "B1-AIR", "B1 AIR", 7288.79, 10158.26, 2000.00, "", True),
    ("UMANOIDI", "R1-U1", "R1-U1 (Expansion Dock 100Tflops - 23 DOF)", 11351.00, 16461.24, 2000.00, "Pagina R1 EDU Standard", True),
    ("UMANOIDI", "R1-U2", "R1-U2 (Waist 3 DOF, single arm 7 DOF, 100Tflops - 29 DOF)", 13338.93, 19544.22, 2000.00, "", True),
    ("UMANOIDI", "R1-U3", "R1 / R1-U3 (DEX 3-1 Force controlled, no tactile - 43 DOF)", 21555.70, 32287.20, 2000.00, "Card università R1 EDU", True),
    ("UMANOIDI", "R1-U4", "R1-U4 (DEX 3-1 Force controlled with tactile - 43 DOF)", 23322.75, 35027.63, 2000.00, "", True),
    ("UMANOIDI", "R1-U5", "R1-U5 (Five fingers BRAINCO BIONIC REVO 2 - no tactile)", 19788.66, 29546.77, 2000.00, "", True),
    ("UMANOIDI", "R1-U6", "R1-U6 (Five fingers BRAINCO BIONIC REVO 2 - with tactile)", 23322.75, 35027.63, 2000.00, "", True),
    ("UMANOIDI", "GO2-AIR", "GO2 AIR PACKAGE", 1032.14, 2718.47, 500.00, "", True),
    ("UMANOIDI", "GO2-PRO", "GO2 PRO PACKAGE", 2592.37, 4043.76, 500.00, "", True),
    ("UMANOIDI", "GO2-EDU-STD", "GO2 EDU STANDARD", 5819.64, 12799.48, 500.00, "", True),
    ("UMANOIDI", "GO2-EDU-SMART", "GO2 EDU SMART", 8028.45, 15450.06, 500.00, "Mapping Go2 EDU+ sito → SMART", True),
    ("UMANOIDI", "GO2-EDU-LASER", "GO2 EDU LASER SMART (+ LIVOX MID 360)", 10886.43, None, 700.00, "Non spec. / Coming soon", False),
    ("UMANOIDI", "GO2-EDU-ULT", "GO2 EDU ULTIMATE VERSION (+ HESAI XT16)", 12211.71, 20075.00, 700.00, "", True),
    ("UMANOIDI", "GO2W-U1", "GO2W-U1", 235.85, 18717.85, 700.00, "Gold €235 sospetto — verificare", False),
    ("UMANOIDI", "GO2W-U2", "GO2W-U2", 10002.00, 24784.30, 700.00, "", True),
    ("UMANOIDI", "GO2W-U3", "GO2W-U3 (+ LIVOX MID360)", 12653.47, 28724.90, 700.00, "", True),
    ("UMANOIDI", "GO2W-U4", "GO2W-U4 (+ HESAI XT16)", 13537.00, 33909.90, 700.00, "", True),
    ("UMANOIDI", "GO2W-U5", "GO2W-U5 (+ HESAI XT16 & Camera Gimbal)", 24050.93, 38809.53, 700.00, "", True),
    ("UMANOIDI", "B2", "B2", 44118.13, 76076.34, 2500.00, "Card università B2", True),
    ("UMANOIDI", "B2-LIDAR", "B2+LIDAR", 51186.32, 77954.23, 2500.00, "Scheda unitree-b2.html", True),
    ("UMANOIDI", "B2W", "B2W", 58254.51, 80283.58, 2500.00, "", True),
    ("UMANOIDI", "B2W-LIDAR", "B2W+LIDAR", 65633.80, 100188.74, 2800.00, "", True),
    ("UMANOIDI", "A2-STD", "A2 STANDARD", 20828.00, 30648.48, 2000.00, "", True),
    ("UMANOIDI", "A2-PRO", "A2 PRO", 27607.84, 41673.16, 2000.00, "", True),
    ("UMANOIDI", "A2W-STD", "A2-W STANDARD", 25399.00, 38247.63, 2000.00, "", True),
    ("UMANOIDI", "A2W-PRO", "A2-W PRO", 32025.46, 48524.23, 2000.00, "", True),
    # MANI (16)
    ("MANI_BRACCI", "HAND-DEX3-1-NO-TAC", "HAND DEX3-1 WITHOUT TACTILE (Single)", 4625.02, 10577.40, 200.00, "", True),
    ("MANI_BRACCI", "HAND-DEX3-1-TAC", "HAND DEX3-1 WITH TACTILE (Single)", 5508.54, 12806.96, 200.00, "", True),
    ("MANI_BRACCI", "HAND-FINGERS-NO-TAC", "DEXTEROUS HAND FINGERS WITHOUT TACTILE (Single)", 5819.54, 13118.05, 500.00, "", True),
    ("MANI_BRACCI", "HAND-FINGERS-TAC", "DEXTEROUS HAND FINGERS WITH TACTILE (Single)", 7586.69, 14725.40, 500.00, "", True),
    ("MANI_BRACCI", "BIONIC-REVO2-BASIC", "BIONIC REVO 2 BASIC (No sensori tattili)", 3845.20, 5791.95, 300.00, "", True),
    ("MANI_BRACCI", "H1S-HAND-TOP", "H1-S DEXTEROUS HAND (Single) TOP", 7586.69, 14103.00, 500.00, "", True),
    ("MANI_BRACCI", "H1M-HAND-TOP", "H1-M DEXTEROUS HAND (Single) TOP", 7586.69, 14103.20, 500.00, "", True),
    ("MANI_BRACCI", "ARM-Z1-AIR", "ARM Z1 AIR", 6246.06, 9450.21, 400.00, "", True),
    ("MANI_BRACCI", "ARM-Z1-PRO", "ARM Z1 PRO", 7924.75, 12001.61, 400.00, "", True),
    ("MANI_BRACCI", "Z1-GRIPPER-STD", "Z1 STANDARD GRIPPER", 1377.34, 2107.17, 50.00, "", True),
    ("MANI_BRACCI", "Z1-GRIPPER-D435I", "Z1 GRIPPER + D435I CAMERA", 2260.66, 3477.38, 50.00, "", True),
    ("MANI_BRACCI", "Z1-GRIPPER-D405", "Z1 GRIPPER + D405 CAMERA", 2260.66, 3477.38, 50.00, "", True),
    ("MANI_BRACCI", "R1-HAND-DEX3-NO-TAC", "R1 HAND DEX3-1 (No sensori tattili)", 4626.89, 6889.99, 500.00, "", True),
    ("MANI_BRACCI", "R1-HAND-DEX3-TAC", "R1 HAND DEX3-1 (Con sensori tattili)", 5510.41, 8200.20, 500.00, "", True),
    ("MANI_BRACCI", "R1-REVO2-BASIC", "R1 BrainCo BIONIC REVO 2 BASIC (No sensori)", 3535.96, 5312.38, 300.00, "", True),
    ("MANI_BRACCI", "R1-REVO2-HAPTIC", "R1 BrainCo BIONIC REVO 2 HAPTIC (Con sensori)", 5303.01, 8052.80, 300.00, "", True),
    # COMPONENTISTICA (35)
    ("COMPONENTISTICA", "G1-REMOTE", "G1 REMOTE CONTROLLER", 324.58, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "G1-BATTERY", "G1 BATTERY", 633.81, 925.83, 100.00, "", True),
    ("COMPONENTISTICA", "G1-CHARGER", "G1 BATTERY CHARGER", 140.20, 188.87, 50.00, "", True),
    ("COMPONENTISTICA", "G1-FRAME", "G1 PROTECTION FRAME", 472.46, 618.46, 200.00, "", True),
    ("COMPONENTISTICA", "H1-REMOTE", "H1 REMOTE CONTROLLER", 324.58, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "H1-BATTERY", "H1 BATTERY (Single)", 1578.73, 2162.76, 500.00, "", True),
    ("COMPONENTISTICA", "H1-CHARGER-FAST", "H1 FAST CHARGER", 272.73, 304.40, 50.00, "", True),
    ("COMPONENTISTICA", "H1-COMPUTE-100T", "H1 100 TFLOP COMPUTING MODULE", 3491.79, 5243.87, 300.00, "", True),
    ("COMPONENTISTICA", "H1-COMPUTE-200T", "H1 200TFLOP COMPUTING MODULE", 6672.47, 10176.64, 300.00, "", True),
    ("COMPONENTISTICA", "H1-FRAME", "H1 PROTECTION FRAME", 1017.92, 1472.74, 300.00, "", True),
    ("COMPONENTISTICA", "R1-REMOTE", "R1 REMOTE CONTROLLER", 324.58, 445.05, 100.00, "", True),
    ("COMPONENTISTICA", "R1-BATTERY", "R1 BATTERY (Single)", 1048.61, None, 500.00, "Non spec.", False),
    ("COMPONENTISTICA", "R1-CHARGER", "R1 CHARGER", 140.20, 188.87, 50.00, "", True),
    ("COMPONENTISTICA", "R1-FRAME", "R1 PROTECTION FRAME (Incluso in EDU)", 316.91, 482.91, 50.00, "", True),
    ("COMPONENTISTICA", "GO2-REMOTE", "GO2 REMOTE CONTROLLER", 324.58, 448.27, 100.00, "", True),
    ("COMPONENTISTICA", "GO2-SELF-CHARGE", "GO2 SELF-CHARGING BOARD", 810.52, 1074.69, 100.00, "", True),
    ("COMPONENTISTICA", "D1-ARM", "D1 ROBOTIC ARM", 3388.09, 5140.17, 200.00, "", True),
    ("COMPONENTISTICA", "GO2-BATT-LR", "GO2 BATTERY LONG RANGE", 633.61, None, 100.00, "Non spec.", False),
    ("COMPONENTISTICA", "GO2-BATT-STD", "GO2 BATTERY STANDARD", 457.11, None, 100.00, "Non spec.", False),
    ("COMPONENTISTICA", "GO2-CHARGER-STD", "GO2 CHARGER STANDARD", 96.03, 131.37, 50.00, "", True),
    ("COMPONENTISTICA", "GO2-CHARGER-FAST", "GO2 CHARGER FAST", 140.20, 219.72, 50.00, "", True),
    ("COMPONENTISTICA", "GO2-FOOT-PAD", "GO2 FOOT PAD", 87.19, 103.90, 50.00, "", True),
    ("COMPONENTISTICA", "B2-CONTROLLER", "B2 CONTROLLER", 324.58, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "B2-BATT-STD", "B2 STANDARD BATTERY", 3480.17, 4940.24, 800.00, "", True),
    ("COMPONENTISTICA", "B2-BATT-LOW-T", "B2 BATTERY LOW TEMPERATURE", 3480.17, 4940.24, 800.00, "", True),
    ("COMPONENTISTICA", "B2-BATT-HIGH-T", "B2 BATTERY HIGH TEMPERATURE", 5247.22, 7680.67, 800.00, "", True),
    ("COMPONENTISTICA", "B2-FOOT-PAD", "B2 FOOT PAD", 156.71, 185.91, 100.00, "", True),
    ("COMPONENTISTICA", "B2-FRAME", "B2 PROTECTION FRAME", 428.28, 549.06, 200.00, "", True),
    ("COMPONENTISTICA", "HELIOS-5515", "HELIOS 5515 LIDAR", 7275.50, 11169.11, 200.00, "", True),
    ("COMPONENTISTICA", "ORIN-NX-UPGRADE", "ORIN NX EXTERNAL UPGRADE", 2754.27, 4214.34, 100.00, "", True),
    ("COMPONENTISTICA", "B2-CHARGING-BOARD", "B2-CHARGING BOARD", 3637.80, 5684.55, 100.00, "", True),
    ("COMPONENTISTICA", "A2-CONTROLLER", "A2 CONTROLLER", 324.58, 446.25, 100.00, "", True),
    ("COMPONENTISTICA", "A2-BATTERY", "A2 BATTERIA", 887.22, 1473.91, 100.00, "", True),
    ("COMPONENTISTICA", "A2-CHARGER", "A2 CARICATORE", 545.46, None, 100.00, "Non spec.", False),
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
