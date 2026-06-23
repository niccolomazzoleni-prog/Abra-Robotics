# -*- coding: utf-8 -*-
"""Contenuti tecnici verificati per catalogo-manifest.json (fonti: unitree.com, docs.quadruped.de, RoboStore)."""
from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_OVERRIDES_PATH = _ROOT / "data" / "product-images.json"

# immagine relativa a ROOT sito (senza ../)
IMAGE: dict[str, str] = {
    "G1-AIR": "prodotti/assets/images/g1-01.jpg",
    "G1-U1": "prodotti/assets/variants/g1-u1/img-01.png",
    "G1-U2": "prodotti/assets/variants/g1-u2/img-01.png",
    "G1-U3": "prodotti/assets/variants/g1-u3/img-01.png",
    "G1-U4": "prodotti/assets/variants/g1-u4/img-01.png",
    "G1-U5": "prodotti/assets/variants/g1-u5/img-01.png",
    "G1-U6": "prodotti/assets/variants/g1-u6/img-01.png",
    "G1-U7": "prodotti/assets/variants/g1-u7/img-01.png",
    "G1-U9": "prodotti/assets/variants/g1-u3/img-01.png",
    "G1-U4-37DOF": "prodotti/assets/variants/g1-u4/img-01.png",
    "G1-U10": "prodotti/assets/variants/g1-u7/img-01.png",
    "G1-COMP": "prodotti/assets/variants/g1-comp/img-01.png",
    "H2-AIR": "images/prodotti/unitree-h2-hero.png",
    "H2-EDU": "images/prodotti/unitree-h2-hero.png",
    "R1-D": "images/manifattura/unitree-r1-d.png",
    "R1-AIR": "images/manifattura/unitree-r1.png",
    "R1-U1": "images/manifattura/unitree-r1.png",
    "R1-U2": "images/manifattura/unitree-r1.png",
    "R1-U3": "images/manifattura/unitree-r1.png",
    "R1-U4": "images/manifattura/unitree-r1.png",
    "R1-U5": "images/manifattura/unitree-r1.png",
    "R1-U6": "images/manifattura/unitree-r1.png",
    "GO2-AIR": "images/prodotti/unitree-go2-card.png",
    "GO2-PRO": "images/prodotti/unitree-go2-card.png",
    "GO2-EDU-STD": "images/prodotti/unitree-go2-card.png",
    "GO2-EDU-SMART": "images/prodotti/unitree-go2-card.png",
    "GO2-EDU-ULT": "images/prodotti/unitree-go2-card.png",
    "AS2-AIR": "images/prodotti/unitree-go2-card.png",
    "AS2-PRO": "images/prodotti/unitree-go2-card.png",
    "AS2-EDU": "images/prodotti/unitree-go2-card.png",
    "GO2W-U2": "images/prodotti/unitree-go2w-card.png",
    "GO2W-U3": "images/prodotti/unitree-go2w-card.png",
    "GO2W-U4": "images/prodotti/unitree-go2w-card.png",
    "GO2W-U5": "images/prodotti/unitree-go2w-card.png",
    "B2": "images/prodotti/unitree-b2.png",
    "B2-LIDAR": "images/prodotti/unitree-b2.png",
    "B2W": "images/prodotti/unitree-b2w.png",
    "B2W-LIDAR": "images/prodotti/unitree-b2w.png",
    "A2-STD": "images/prodotti/unitree-a2.png",
    "A2-PRO": "images/prodotti/unitree-a2-pro.png",
    "A2W-STD": "images/prodotti/unitree-a2w.png",
    "A2W-PRO": "images/prodotti/unitree-a2w.png",
    "HAND-DEX3-1-NO-TAC": "images/accessori/dex3-1-official.jpg",
    "HAND-DEX3-1-TAC": "images/accessori/dex3-1-official.jpg",
    "HAND-FINGERS-NO-TAC": "images/accessori/inspire-rh56.png",
    "HAND-FINGERS-TAC": "images/accessori/inspire-rh56.png",
    "BIONIC-REVO2-BASIC": "images/accessori/inspire-rh56.png",
    "H2-REMOTE": "images/accessori/rc-g1.jpg",
    "H2-BATTERY": "images/accessori/batt-h1.png",
    "H2-CHARGER-FAST": "images/accessori/batt-h1.png",
    "H2-COMPUTE-I8": "images/accessori/compute-intel-i8.png",
    "H2-COMPUTE-ORIN-NX": "images/accessori/compute-orin-nx.png",
    "H2-COMPUTE-AGX-ORIN": "images/accessori/compute-agx-orin.png",
    "H2-COMPUTE-AGX-THOR": "images/accessori/compute-agx-thor.png",
    "H2-HAND-DEX5": "images/accessori/dex5-1.jpg",
    "H2-HAND-DEX5P": "images/accessori/dex5-1.jpg",
    "H2-HAND-DEX3": "images/accessori/dex3-1-official.jpg",
    "H2-HAND-DEX3-TAC": "images/accessori/dex3-1-official.jpg",
    "H2-HAND-INSPIRE-DFQ": "images/accessori/inspire-rh56.png",
    "H2-HAND-INSPIRE-FTP": "images/accessori/inspire-rh56.png",
    "H2-HAND-REVO2-BASIC": "images/accessori/inspire-rh56.png",
    "H2-HAND-REVO2-TACTILE": "images/accessori/inspire-rh56.png",
    "H2-GRIPPER-DEX1-STD": "images/accessori/dex1-1-v1.jpg",
    "H2-GRIPPER-DEX1-ADV": "images/accessori/dex1-1-v2.jpg",
    "H2-GRIPPER-DEX1-FLAG": "images/accessori/dex1-1-v2.jpg",
    "ARM-Z1-AIR": "images/accessori/z1.jpg",
    "ARM-Z1-PRO": "images/accessori/z1.jpg",
    "Z1-GRIPPER-STD": "images/accessori/z1-gripper.jpg",
    "Z1-GRIPPER-D435I": "images/accessori/z1-d435i.jpg",
    "Z1-GRIPPER-D405": "images/accessori/z1-d405.jpg",
    "R1-HAND-DEX3-NO-TAC": "images/accessori/dex3-1-official.jpg",
    "R1-HAND-DEX3-TAC": "images/accessori/dex3-1-official.jpg",
    "R1-REVO2-BASIC": "images/accessori/inspire-rh56.png",
    "R1-REVO2-HAPTIC": "images/accessori/inspire-rh56.png",
    "G1-REMOTE": "images/accessori/rc-g1.jpg",
    "G1-BATTERY": "images/accessori/batt-g1.jpg",
    "G1-CHARGER": "images/accessori/batt-g1.jpg",
    "G1-FRAME": "images/accessori/g1-gantry.jpg",
    "R1-REMOTE": "images/accessori/rc-g1.jpg",
    "R1-CHARGER": "images/accessori/batt-go2.webp",
    "R1-FRAME": "images/accessori/g1-gantry.jpg",
    "GO2-REMOTE": "images/accessori/rc-go2.jpg",
    "GO2-SELF-CHARGE": "images/accessori/go2-charging.png",
    "D1-ARM": "images/accessori/d1.jpg",
    "GO2-CHARGER-STD": "images/accessori/batt-go2.webp",
    "GO2-CHARGER-FAST": "images/accessori/batt-go2.webp",
    "GO2-FOOT-PAD": "images/accessori/batt-go2.webp",
    "B2-CONTROLLER": "images/accessori/rc-g1.jpg",
    "B2-BATT-STD": "images/accessori/batt-b2.jpg",
    "B2-BATT-LOW-T": "images/accessori/batt-b2.jpg",
    "B2-BATT-HIGH-T": "images/accessori/batt-b2.jpg",
    "B2-FOOT-PAD": "images/accessori/batt-b2.jpg",
    "B2-FRAME": "images/accessori/g1-gantry.jpg",
    "HELIOS-5515": "images/accessori/hesai-xt16.png",
    "ORIN-NX-UPGRADE": "images/accessori/compute-orin-nx.png",
    "B2-CHARGING-BOARD": "images/accessori/go2-charging.png",
    "A2-CONTROLLER": "images/accessori/rc-g1.jpg",
    "A2-BATTERY": "images/accessori/batt-go2.webp",
}

FALLBACK_IMAGE = {
    "UMANOIDI": "images/g1-hero.png",
    "MANI_BRACCI": "images/accessori/dex3-1.jpg",
    "COMPONENTISTICA": "images/accessori/batt-g1.jpg",
}

# Contenuti per SKU (titolo, sottotitolo, descrizione, specs, fonte)
MANIFEST: dict[str, dict] = {}

def _entry(titolo, sottotitolo, descrizione, specs, fonte="unitree.com"):
    return {
        "titolo": titolo,
        "sottotitolo": sottotitolo,
        "descrizione": descrizione,
        "specs": specs,
        "fonte_specs": fonte,
    }

# --- UMANOIDI G1 ---
_g1_base = [
    ("Altezza", "~132 cm"), ("Peso", "~35 kg"), ("DoF", "23"),
    ("Velocità max", "2 m/s"), ("Coppia ginocchio", "90 N·m"),
    ("Percezione", "LiDAR MID-360 + RealSense D435i"), ("Autonomia", "~2 ore"),
]
MANIFEST["G1-AIR"] = _entry(
    "Unitree G1 Air",
    "Umanoide compatto con LiDAR 3D e depth camera per navigazione autonoma.",
    "G1 Air è la configurazione base della piattaforma G1: 23 gradi di libertà, LiDAR LIVOX MID-360 e Intel RealSense D435i per SLAM e percezione. Ideale per demo, POC e prime applicazioni di robotica umanoide in Italia.",
    _g1_base,
)
for sku, dof, mani, comp, extra in [
    ("G1-U1", "23", "Dummy (no polsi)", "Jetson Orin NX 100 TOPS", "EDU Standard · Expansion Dock"),
    ("G1-U2", "29", "Dummy + polsi", "Jetson Orin NX 100 TOPS", "Vita 3 DoF · braccio singolo 7 DoF"),
    ("G1-U3", "43", "Dex3-1 force-controlled", "Jetson Orin NX 100 TOPS", "Mani dexterous senza tattile"),
    ("G1-U4", "43", "Dex3-1 con tattile", "Jetson Orin NX 100 TOPS", "Sensori tattili sulle mani"),
    ("G1-U5", "40", "Inspire RH56DFQ 5 dita", "Jetson Orin NX 100 TOPS", "Mani Inspire senza tattile"),
    ("G1-U6", "40", "Inspire RH56DFTP 5 dita", "Jetson Orin NX 100 TOPS", "Mani Inspire con tattile"),
    ("G1-U7", "37", "REVO 2 Basic 5 dita", "Jetson Orin NX 100 TOPS", "Mani BrainCo REVO 2"),
    ("G1-U9", "37", "Dex3-1 no tactile", "Jetson Orin NX 100 TOPS", "Configurazione 37 DoF"),
    ("G1-U4-37DOF", "37", "Dex3-1 con tattile", "Jetson Orin NX 100 TOPS", "Variante 37 DoF tattile"),
    ("G1-U10", "35", "REVO 2 Basic", "Jetson Orin NX 100 TOPS", "35 DoF · REVO 2"),
]:
    specs = [
        ("DoF totali", dof), ("Mani", mani), ("Computing", comp),
        ("Coppia ginocchio", "120 N·m"), ("LiDAR", "LIVOX MID-360"),
        ("SDK", "ROS2 · Python · C++"), ("Variante", extra),
    ]
    MANIFEST[sku] = _entry(
        f"Unitree G1 {sku.replace('G1-', '')}",
        f"Piattaforma G1 EDU — {extra}.",
        f"Configurazione G1 {extra}: piattaforma umanoide da ricerca con {dof} DoF, computing NVIDIA Jetson Orin e percezione 3D integrata. Distribuita in Italia da Abra Robotics.",
        specs,
    )
MANIFEST["G1-COMP"] = _entry(
    "Unitree G1 Comp",
    "Umanoide atletico per competizioni e sfide ad alta dinamica.",
    "G1 Comp è ottimizzato per prestazioni dinamiche: testa articolata, velocità oltre 2 m/s e struttura rinforzata per competizioni robotiche e ricerca sulla locomozione veloce.",
    [("DoF", "25"), ("Velocità", ">2 m/s"), ("Uso", "Competizioni · atletica"), ("Mani", "Dummy + polsi upgrade")],
)

# --- H2 ---
_h2_base = [
    ("Altezza", "~180 cm"), ("Peso", "~70 kg"), ("DoF", "31"),
    ("Coppia ginocchio", "360 N·m"), ("Coppia braccio", "120 N·m"),
    ("Percezione", "LiDAR 3D + depth camera"), ("SDK", "ROS2 · Python · C++"),
]
MANIFEST["H2-AIR"] = _entry(
    "Unitree H2 Air",
    "Umanoide full-size entry per ricerca e sviluppo avanzato.",
    "H2 Air è la configurazione base della piattaforma H2: umanoide full-size con 31 DoF, percezione 360° e computing espandibile. Ideale per laboratori che introducono robotica umanoide di nuova generazione.",
    _h2_base + [("Variante", "Air · configurazione base")],
    "unitree.com/h2",
)
MANIFEST["H2-EDU"] = _entry(
    "Unitree H2 EDU",
    "Umanoide full-size per ricerca avanzata — computing e mani espandibili.",
    "H2 EDU è la piattaforma umanoide top di Unitree: ~180 cm, 31 DoF, coppia fino a 360 N·m alle gambe, moduli NVIDIA Jetson opzionali e mani dexterous dedicate. Distribuito in Italia da Abra Robotics per università e R&D.",
    _h2_base + [("Variante", "EDU · ricerca avanzata"), ("Mani", "Dex3/Dex5/Inspire opzionali")],
    "unitree.com/h2",
)

# --- R1 ---
MANIFEST["R1-D"] = _entry(
    "Unitree Dual-Arm Humanoid Robot",
    "Robot umanoide dual-arm ad alta DoF — deploy rapido e sviluppo secondario full-stack.",
    "Dual-Arm Humanoid Robot (serie R1-D) è la piattaforma Unitree per manipolazione bimanuale: bracci 5 o 7 DoF, base fissa o mobile con LiDAR, modulo visivo binoculare e framework di sviluppo maturo per ricerca e applicazioni industriali leggere. Specifiche da unitree.com/mobile/R1-D.",
    [
        ("DoF totali", "15–31"),
        ("DoF braccio", "5×2 / 7×2"),
        ("Payload braccio", "2–4 kg"),
        ("Coppia spalla", "60 N·m"),
        ("Precisione pinza", "±0,1 mm"),
        ("Lunghezza braccio", "420 / 555 mm"),
        ("Computing testa", "CPU 8-core + 10 TOPS"),
        ("Camera", "Binoculare FOV 146°×124°"),
        ("Microfono", "Array 4 mic + dual speaker 3W"),
        ("Connettività", "Wi-Fi 6 · Bluetooth 5.2"),
        ("Autonomia", "~1,5 h (batteria)"),
        ("Configurazioni Unitree", "R1-A5 · R1-A7 · R1-A5-D · R1-A7-D (tabella ufficiale, non SKU Abra)"),
        ("Base", "Fissa o mobile (LiDAR + 3 DoF chassis)"),
        ("End-effector", "Gripper 2 dita / mano 3-5 dita"),
        ("Compute opzionale", "NVIDIA Jetson Orin 40–100 TOPS"),
        ("Sviluppo secondario", "Full-stack · drag-and-drop teaching"),
        ("Garanzia", "12 mesi"),
    ],
    "unitree.com/mobile/R1-D",
)

MANIFEST["R1-AIR"] = _entry(
    "Unitree R1 Air",
    "Umanoide compatto entry-level per education e prototipazione.",
    "R1 Air è la porta d'ingresso alla famiglia R1: umanoide leggero e accessibile per percorsi formativi, demo e prime applicazioni di robotica umanoide in Italia.",
    [("Altezza", "~122 cm"), ("Peso", "~25 kg"), ("DoF", "23"), ("Computing", "Jetson Orin"), ("Uso", "Education · entry")],
)

for sku, dof, mani, note in [
    ("R1-U1", "23", "Dummy", "Expansion Dock 100 TOPS"),
    ("R1-U2", "29", "Dummy + polsi", "Vita 3 DoF · 100 TOPS"),
    ("R1-U3", "43", "Dex3-1 no tactile", "Manipolazione 43 DoF"),
    ("R1-U4", "43", "Dex3-1 tattile", "Feedback tattile"),
    ("R1-U5", "—", "BrainCo REVO 2 no tactile", "Mani bioniche 5 dita"),
    ("R1-U6", "—", "BrainCo REVO 2 haptic", "Mani con sensori"),
]:
    specs = [
        ("Altezza", "~122 cm"), ("Peso", "~25–29 kg"), ("DoF", dof if dof != "—" else "24+"),
        ("Mani", mani), ("Computing", "Jetson Orin fino a 100 TOPS"),
        ("Autonomia", "~1 ora"), ("SDK", "ROS2 · Python · C++"),
        ("Configurazione", note),
    ]
    MANIFEST[sku] = _entry(
        f"Unitree R1 {sku.replace('R1-', '')}",
        f"Umanoide R1 EDU — {note}.",
        f"R1 è l'umanoide entry-level Unitree per università e laboratori. La variante {sku.replace('R1-', '')} include {note}, con SDK aperto e form factor compatto rispetto al G1.",
        specs,
    )

# --- GO2 ---
_go2_common = [("Peso", "~15 kg"), ("Giunti", "12 motorizzati"), ("Pendenza max", "40°"), ("Gradini", "fino a 16 cm")]
MANIFEST["GO2-AIR"] = _entry("Unitree Go2 Air", "Quadrupede entry con LiDAR 3D L1.",
    "Go2 Air è il pacchetto base Go2: percezione LiDAR 3D, connettività Wi-Fi 6 e 4G, ideale per demo e prototipi di robotica quadrupede.",
    _go2_common + [("Velocità", "2 m/s"), ("Computing", "8-core CPU"), ("LiDAR", "3D L1")])
MANIFEST["GO2-PRO"] = _entry("Unitree Go2 Pro", "Quadrupede consumer con LiDAR e connettività avanzata.",
    "Go2 Pro aggiunge modulo 4G e percezione LiDAR 3D L1 a campo 360°×90°. Payload fino a 10 kg, velocità 1,7 m/s.",
    _go2_common + [("Velocità", "1,7 m/s"), ("Payload", "10 kg"), ("LiDAR", "3D L1")])
MANIFEST["GO2-EDU-STD"] = _entry("Unitree Go2 EDU Standard", "Quadrupede education con Jetson Orin Nano 40 TOPS.",
    "Go2 EDU Standard abilita sviluppo a bordo con NVIDIA Jetson Orin Nano (40 TOPS), LiDAR 4D L2 e SDK aperto ROS/Python.",
    _go2_common + [("Computing", "Orin Nano 40 TOPS"), ("LiDAR", "4D L2"), ("Autonomia", "2–4 h")])
MANIFEST["GO2-EDU-SMART"] = _entry("Unitree Go2 EDU Smart", "Go2 EDU con Jetson Orin 100 TOPS.",
    "Go2 EDU Smart monta NVIDIA Jetson Orin NX da 100 TOPS per AI onboard, navigazione SLAM e ricerca su robotica mobile. Configurazione mappata sulla pagina Go2 EDU+ del sito.",
    _go2_common + [("Computing", "Orin NX 100 TOPS"), ("LiDAR", "4D L2"), ("Velocità", "2 m/s")])
MANIFEST["GO2-EDU-ULT"] = _entry("Unitree Go2 EDU Ultimate", "Go2 EDU con LiDAR Hesai XT16.",
    "Versione Ultimate del Go2 EDU con sensore Hesai XT16 per perception ad alta risoluzione in ambienti industriali e di ricerca outdoor.",
    _go2_common + [("LiDAR", "Hesai XT16"), ("Computing", "Orin NX 100 TOPS")])

# --- AS2 (Unitree As2 — unitree.com/As2, 2026) ---
_as2_common = [
    ("Peso", "~18 kg"),
    ("DoF", "12"),
    ("Velocità max", "fino a 5 m/s"),
    ("Coppia max giunto", "~90 N·m"),
    ("Dimensioni in piedi", "720×378×457 mm"),
]
MANIFEST["AS2-AIR"] = _entry(
    "Unitree As2 Air",
    "Quadrupede compatto entry — dinamica ~2× Go2.",
    "As2 Air è la variante entry della gamma As2 Unitree: telaio leggero ~18 kg, payload fino a ~10 kg in marcia e ~45 kg statico. Adatto a demo e prime valutazioni rispetto a Go2 EDU.",
    _as2_common + [("Payload marcia", "~10 kg"), ("Payload statico", "~45 kg"), ("Autonomia", "~2 h / ~10 km"), ("Protezione", "—")],
    "unitree.com/As2",
)
MANIFEST["AS2-PRO"] = _entry(
    "Unitree As2 Pro",
    "Quadrupede industriale IP54 — sorveglianza e ispezione.",
    "As2 Pro è la configurazione industrial-ready: protezione IP54 su componenti core, LiDAR ultra-wide-angle, doppia camera frontale e posteriore, payload fino a ~15 kg in marcia e ~65 kg statico. Evoluzione del Go2 con maggiore carico utile, resistenza a polvere e spruzzi d'acqua.",
    _as2_common + [("IP", "IP54"), ("Payload marcia", "~15 kg"), ("Payload statico", "~65 kg"), ("Autonomia", ">4 h / ~20 km"), ("LiDAR", "Ultra-wide-angle"), ("Camera", "Frontale + posteriore"), ("Batteria", "648 Wh long range")],
    "unitree.com/As2",
)
MANIFEST["AS2-EDU"] = _entry(
    "Unitree As2 EDU",
    "As2 programmabile — ROS 2 e SDK Unitree.",
    "As2 EDU combina le specifiche Pro (IP54, payload elevato) con ecosistema developer: ROS 2, Python, C++ e secondary development per payload custom e ricerca.",
    _as2_common + [("IP", "IP54"), ("Payload marcia", "~15 kg"), ("SDK", "ROS 2 · Python · C++"), ("Autonomia", ">4 h"), ("LiDAR", "Ultra-wide-angle")],
    "unitree.com/As2",
)

# --- GO2W ---
_go2w = [("Peso", "~18 kg"), ("Dimensioni", "70×43×50 cm"), ("Velocità", "0–2,5 m/s"),
         ("Payload", "≈8 kg (max 12 kg)"), ("Ruote", "4× pneumatiche 7\""), ("Autonomia", "1,5–3 h"),
         ("Pendenza", "35°"), ("Salto ostacolo", "<70 cm")]
MANIFEST["GO2W-U2"] = _entry("Unitree Go2W-U2", "Quadrupede wheel-leg — rotola e cammina.",
    "Go2W combina gambe articolate e ruote motrici: rotola su superfici piane e passa in modalità walking per scale e ostacoli fino a 70 cm. Fonte: unitree.com/go2-w.",
    _go2w + [("Computing", "8-core CPU"), ("LiDAR", "3D opzionale")], "unitree.com/go2-w")
MANIFEST["GO2W-U3"] = _entry("Unitree Go2W-U3", "Go2W con LiDAR Livox MID-360 integrato.",
    "Go2W-U3 aggiunge il LiDAR Livox MID-360 per SLAM e navigazione autonoma su piattaforma wheel-leg.",
    _go2w + [("LiDAR", "Livox MID-360 3D")], "unitree.com/go2-w")
MANIFEST["GO2W-U4"] = _entry("Unitree Go2W-U4", "Go2W con LiDAR Hesai XT16.",
    "Go2W-U4 integra Hesai XT16 per perception 3D ad alta densità su ispezione e ricerca outdoor.",
    _go2w + [("LiDAR", "Hesai XT16")], "unitree.com/go2-w")
MANIFEST["GO2W-U5"] = _entry("Unitree Go2W-U5", "Go2W top con XT16 e camera gimbal.",
    "Configurazione top con Hesai XT16 e camera gimbal per sorveglianza, ispezione e teleoperazione avanzata.",
    _go2w + [("LiDAR", "Hesai XT16"), ("Camera", "Gimbal integrata")], "unitree.com/go2-w")

# --- B2 / A2 ---
MANIFEST["B2"] = _entry("Unitree B2", "Quadrupede industriale IP67 — >6 m/s, >40 kg payload.",
    "B2 è il quadrupede industriale Unitree: velocità oltre 6 m/s, payload continuo >40 kg, autonomia >5 ore, IP67 e batterie hot-swap.",
    [("Velocità", ">6 m/s"), ("Payload", ">40 kg"), ("IP", "IP67"), ("Autonomia", ">5 h / 20 km"),
     ("Coppia ginocchio", "360 N·m"), ("Computing", "Intel i5 + i7")], "docs.quadruped.de/b2")
MANIFEST["B2-LIDAR"] = _entry("Unitree B2 + LiDAR", "B2 con LiDAR 3D automotive 32 canali.",
    "B2 preconfigurato con LiDAR 3D automotive per navigazione autonoma, ispezione e deployment industriale.",
    [("Base", "Unitree B2"), ("LiDAR", "32 canali 3D"), ("Velocità", ">6 m/s"), ("IP", "IP67")])
MANIFEST["B2W"] = _entry("Unitree B2W", "B2 wheel-leg — ruote 225 mm, 120 kg statico.",
    "B2W è la variante wheeled del B2: ruote motrici da 225 mm, payload statico 120 kg, velocità >5 m/s e autonomia fino a 25 km con carico.",
    [("Peso", "~75 kg"), ("Payload cammino", ">40 kg"), ("Payload statico", "120 kg"),
     ("Velocità", ">5 m/s"), ("Ruote", "225 mm"), ("IP", "IP67")], "unitree.com/b2-w")
MANIFEST["B2W-LIDAR"] = _entry("Unitree B2W + LiDAR", "B2W con suite LiDAR integrata.",
    "B2W con sensori LiDAR 3D per ispezione autonoma e logistica su larga scala.",
    [("Base", "B2W"), ("LiDAR", "3D integrato"), ("Payload", ">40 kg in movimento")])
MANIFEST["A2-STD"] = _entry("Unitree A2 Standard", "Quadrupede industriale IP56 — 25 kg in movimento.",
    "A2 Standard: 25 kg payload in cammino, 100 kg statico, autonomia >5 h, Intel Core i7 e LiDAR industriale espandibile.",
    [("Velocità", "~5 m/s"), ("Payload", "25 kg"), ("IP", "IP56"), ("Autonomia", ">5 h"), ("Peso", "~37 kg")])
MANIFEST["A2-PRO"] = _entry("Unitree A2 Pro", "A2 con IP67 e dual LiDAR per ambienti ostili.",
    "A2 Pro aggiunge grado IP67 e dual LiDAR industriale per operazioni outdoor e ambienti umidi.",
    [("Velocità", "~5 m/s"), ("IP", "IP67"), ("LiDAR", "Dual industriale"), ("Payload", "25 kg")])
MANIFEST["A2W-STD"] = _entry("Unitree A2-W Standard", "A2 con configurazione wheel-leg.",
    "Variante wheel-leg dell'A2 per efficienza su superfici piane mantenendo capacità di transito su ostacoli.",
    [("Tipo", "Wheel-leg"), ("Velocità", "~5 m/s"), ("IP", "IP56"), ("Payload", "25 kg")])
MANIFEST["A2W-PRO"] = _entry("Unitree A2-W Pro", "A2-W Pro con IP67 e dual LiDAR.",
    "Top di gamma A2 wheel-leg per ispezione e ricerca in ambienti industriali severi.",
    [("Tipo", "Wheel-leg Pro"), ("IP", "IP67"), ("LiDAR", "Dual industriale")])

# --- MANI ---
MANIFEST["HAND-DEX3-1-NO-TAC"] = _entry("Hand Dex3-1 (senza tattile)", "Mano dexterous 3 dita — singola.",
    "Mano Dex3-1 Unitree a 3 dita con 7 DoF e peso ~710 g. Controllo di forza per grasping di precisione su G1/H1.",
    [("DoF", "7"), ("Peso", "~710 g"), ("Tattile", "No"), ("Tipo", "Singola")], "robostore.com")
MANIFEST["HAND-DEX3-1-TAC"] = _entry("Hand Dex3-1 (con tattile)", "Dex3-1 con sensori tattili integrati.",
    "Versione tattile della Dex3-1: feedback di contatto per manipolazione fine e grasping adattivo.",
    [("DoF", "7"), ("Sensori", "Tattili integrati"), ("Peso", "~710 g")])
MANIFEST["HAND-FINGERS-NO-TAC"] = _entry("Dexterous Hand Fingers (no tattile)", "Mano antropomorfa 5 dita.",
    "Mano a dita dexterous senza sensori tattili per manipolazione antropomorfa su piattaforme umanoidi.",
    [("Dita", "5"), ("Tattile", "No"), ("Tipo", "Singola")])
MANIFEST["HAND-FINGERS-TAC"] = _entry("Dexterous Hand Fingers (tattile)", "Mano 5 dita con feedback tattile.",
    "Mano dexterous con sensori tattili per HRI e manipolazione delicata.",
    [("Dita", "5"), ("Tattile", "Sì")])
MANIFEST["BIONIC-REVO2-BASIC"] = _entry("Bionic REVO 2 Basic", "Mano bionica 5 dita BrainCo — senza tattile.",
    "BrainCo REVO 2 Basic: 6 DoF, 11 giunti, forza di presa fino a 50 N, ripetibilità 0,1°.",
    [("DoF", "6"), ("Giunti", "11"), ("Forza presa", "50 N"), ("Tattile", "No")])
MANIFEST["H1S-HAND-TOP"] = _entry("H1-S Dexterous Hand TOP", "Mano dexterous top di gamma per H1-S.",
    "Mano dexterous singola di fascia alta compatibile con umanoide H1-S.",
    [("Compatibilità", "H1-S"), ("Tipo", "Singola TOP")])
MANIFEST["H1M-HAND-TOP"] = _entry("H1-M Dexterous Hand TOP", "Mano dexterous top di gamma per H1-M.",
    "Mano dexterous singola di fascia alta compatibile con umanoide H1-M.",
    [("Compatibilità", "H1-M"), ("Tipo", "Singola TOP")])
MANIFEST["ARM-Z1-AIR"] = _entry("Unitree Z1 Air", "Braccio robotico 6-DoF con force control.",
    "Braccio Z1 Air: 6 DoF, payload 2 kg, force control integrato per manipolazione di precisione in laboratorio.",
    [("DoF", "6"), ("Payload", "2 kg"), ("Force control", "Sì")], "unitree.com/z1")
MANIFEST["ARM-Z1-PRO"] = _entry("Unitree Z1 Pro", "Braccio Z1 Pro — payload 3 kg.",
    "Z1 Pro estende il payload a 3 kg mantenendo precisione sub-millimetrica e controllo di forza.",
    [("DoF", "6"), ("Payload", "3 kg"), ("Force control", "Sì")])
for sku, nome, extra in [
    ("Z1-GRIPPER-STD", "Z1 Standard Gripper", "Pinza standard per Z1"),
    ("Z1-GRIPPER-D435I", "Z1 Gripper + D435i", "Pinza con RealSense D435i"),
    ("Z1-GRIPPER-D405", "Z1 Gripper + D405", "Pinza con RealSense D405"),
    ("R1-HAND-DEX3-NO-TAC", "R1 Hand Dex3-1", "Mano Dex3-1 per R1 senza tattile"),
    ("R1-HAND-DEX3-TAC", "R1 Hand Dex3-1 tattile", "Mano Dex3-1 per R1 con tattile"),
    ("R1-REVO2-BASIC", "R1 REVO 2 Basic", "BrainCo REVO 2 per R1"),
    ("R1-REVO2-HAPTIC", "R1 REVO 2 Haptic", "REVO 2 con feedback aptico"),
]:
    MANIFEST[sku] = _entry(f"Unitree {nome}", extra + ".",
        f"{nome} — accessorio originale Unitree per piattaforme di manipolazione. {extra}.",
        [("Prodotto", nome), ("Compatibilità", "Unitree R1 / Z1 / G1"), ("Tipo", "Accessorio manipolazione")])

# --- COMPONENTISTICA (template per famiglia) ---
def _comp(sku, nome, compat, specs_extra):
    MANIFEST[sku] = _entry(
        f"Unitree {nome.title()}" if not nome.startswith("Unitree") else nome,
        f"Componente originale — compatibile {compat}.",
        f"{nome} è un componente originale Unitree per {compat}. Ricambio o upgrade certificato, distribuito in Italia da Abra Robotics.",
        specs_extra + [("Compatibilità", compat), ("Origine", "Unitree OEM")],
    )

_comp("G1-REMOTE", "G1 Remote Controller", "G1", [("Tipo", "Telecomando"), ("Connettività", "Wi-Fi / BT")])
_comp("G1-BATTERY", "G1 Battery", "G1", [("Tipo", "Batteria high-performance"), ("Ricambio", "Sì")])
_comp("G1-CHARGER", "G1 Battery Charger", "G1", [("Tipo", "Caricabatterie"), ("Tensione", "Compatibile G1")])
_comp("G1-FRAME", "G1 Protection Frame", "G1", [("Tipo", "Telaio protezione"), ("Materiale", "Lega leggera")])
_comp("H2-REMOTE", "H2 Remote Controller", "H2", [("Tipo", "Telecomando")])
_comp("H2-BATTERY", "H2 Battery (Single)", "H2", [("Capacità", "Alta capacità"), ("Peso", "~5 kg")])
_comp("H2-CHARGER-FAST", "H2 Fast Charger", "H2", [("Tipo", "Caricatore rapido")])
_comp("H2-COMPUTE-I8", "H2 Intel Core i8 Computing Board", "H2", [("Compute", "Intel Core i8"), ("Tipo", "Modulo espansione")])
_comp("H2-COMPUTE-ORIN-NX", "H2 Jetson Orin NX Board", "H2", [("Compute", "Jetson Orin NX")])
_comp("H2-COMPUTE-AGX-ORIN", "H2 Jetson AGX Orin Board", "H2", [("Compute", "Jetson AGX Orin")])
_comp("H2-COMPUTE-AGX-THOR", "H2 Jetson AGX Thor Board", "H2", [("Compute", "Jetson AGX Thor")])
for sku, nome, extra in [
    ("H2-HAND-DEX5", "H2 Dex5-1 Hand", "Mano 5 dita per H2"),
    ("H2-HAND-DEX5P", "H2 Dex5-1P Hand", "Mano 5 dita avanzata"),
    ("H2-HAND-DEX3", "H2 Dex3-1 Hand", "Mano 3 dita force-controlled"),
    ("H2-HAND-DEX3-TAC", "H2 Dex3-1 Tactile", "Mano con sensori tattili"),
    ("H2-HAND-INSPIRE-DFQ", "H2 Inspire DFQ Hand", "Mano Inspire 5 dita"),
    ("H2-HAND-INSPIRE-FTP", "H2 Inspire FTP Hand", "Mano Inspire con tattile"),
    ("H2-HAND-REVO2-BASIC", "H2 REVO 2 Basic Hand", "BrainCo REVO 2"),
    ("H2-HAND-REVO2-TACTILE", "H2 REVO 2 Tactile Hand", "REVO 2 con tattile"),
    ("H2-GRIPPER-DEX1-STD", "H2 Dex1-1 Gripper Standard", "Gripper entry"),
    ("H2-GRIPPER-DEX1-ADV", "H2 Dex1-1 Gripper Advanced", "Gripper avanzato"),
    ("H2-GRIPPER-DEX1-FLAG", "H2 Dex1-1 Gripper Flagship", "Gripper top"),
]:
    MANIFEST[sku] = _entry(f"Unitree {nome}", f"Accessorio dedicato H2 — {extra}.",
        f"{nome}: accessorio originale Unitree per piattaforma H2. {extra}.",
        [("Prodotto", nome), ("Compatibilità", "Unitree H2"), ("Tipo", "Accessorio dedicato")])
_comp("R1-REMOTE", "R1 Remote Controller", "R1", [("Tipo", "Telecomando")])
_comp("R1-CHARGER", "R1 Charger", "R1", [("Tipo", "Caricabatterie")])
_comp("R1-FRAME", "R1 Protection Frame", "R1", [("Tipo", "Telaio"), ("Nota", "Incluso in EDU")])
_comp("GO2-REMOTE", "Go2 Remote Controller", "Go2", [("Tipo", "Telecomando")])
_comp("GO2-SELF-CHARGE", "Go2 Self-Charging Board", "Go2 EDU+", [("Tipo", "Base ricarica wireless")])
_comp("D1-ARM", "D1 Robotic Arm", "Go2", [("Tipo", "Braccio servo"), ("Mount", "Go2")])
_comp("GO2-CHARGER-STD", "Go2 Charger Standard", "Go2", [("Tipo", "Caricatore standard")])
_comp("GO2-CHARGER-FAST", "Go2 Charger Fast", "Go2", [("Tipo", "Caricatore rapido"), ("Tensione", "33,6V")])
_comp("GO2-FOOT-PAD", "Go2 Foot Pad", "Go2", [("Tipo", "Pad piede"), ("Quantità", "Set ricambio")])
_comp("B2-CONTROLLER", "B2 Controller", "B2", [("Tipo", "Telecomando industriale")])
_comp("B2-BATT-STD", "B2 Standard Battery", "B2", [("Capacità", "45 Ah"), ("Energia", "2250 Wh")])
_comp("B2-BATT-LOW-T", "B2 Battery Low Temperature", "B2", [("Tipo", "Batteria bassa temperatura"), ("Range", "Fino -20°C")])
_comp("B2-BATT-HIGH-T", "B2 Battery High Temperature", "B2", [("Tipo", "Batteria alta temperatura")])
_comp("B2-FOOT-PAD", "B2 Foot Pad", "B2", [("Tipo", "Pad piede ricambio")])
_comp("B2-FRAME", "B2 Protection Frame", "B2", [("Tipo", "Telaio protezione")])
_comp("HELIOS-5515", "Helios 5515 LiDAR", "B2 / piattaforme", [("Tipo", "LiDAR 3D"), ("Uso", "Navigazione · SLAM")])
_comp("ORIN-NX-UPGRADE", "Orin NX External Upgrade", "G1 / Go2 / B2", [("Compute", "Jetson Orin NX"), ("Tipo", "Upgrade esterno")])
_comp("B2-CHARGING-BOARD", "B2 Charging Board", "B2", [("Tipo", "Pannello ricarica autonoma")])
_comp("A2-CONTROLLER", "A2 Controller", "A2", [("Tipo", "Telecomando")])
_comp("A2-BATTERY", "A2 Batteria", "A2", [("Tipo", "Batteria ricambio")])


def _load_image_overrides() -> dict[str, str]:
    if not _OVERRIDES_PATH.is_file():
        return {}
    try:
        raw = json.loads(_OVERRIDES_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    out: dict[str, str] = {}
    for sku, entry in raw.items():
        if isinstance(entry, str):
            out[sku] = entry
        elif isinstance(entry, dict) and entry.get("path"):
            out[sku] = entry["path"]
    return out


_IMAGE_OVERRIDES = _load_image_overrides()


def image_for(sku: str, categoria: str) -> str:
    if sku in _IMAGE_OVERRIDES:
        return _IMAGE_OVERRIDES[sku]
    return IMAGE.get(sku, FALLBACK_IMAGE.get(categoria, "images/g1-hero.png"))


def build_manifest_entry(sku: str, row: dict) -> dict:
    """Restituisce entry manifest per SKU; fallback se manca override."""
    cat = row.get("categoria", "")
    nome = row.get("nome_prodotto", sku)
    if sku in MANIFEST:
        e = dict(MANIFEST[sku])
    else:
        e = _entry(
            f"Unitree {nome.split('(')[0].strip()}",
            f"Prodotto Unitree — {nome}.",
            f"{nome}: componente o robot Unitree distribuito in Italia da Abra Robotics. Specifiche da confermare su preventivo.",
            [("Prodotto", nome), ("Categoria", cat.replace("_", " "))],
        )
    e["immagine"] = image_for(sku, cat)
    e["categoria"] = cat
    e["slug"] = row.get("pagina_sito", "").replace("prodotti/", "") or f"unitree-{sku.lower().replace('_', '-')}.html"
    return e
