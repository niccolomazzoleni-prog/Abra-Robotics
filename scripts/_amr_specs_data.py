# -*- coding: utf-8 -*-
"""Specs categorizzate AMR — fonti: mobile-industrial-robots.com, youibot.com, neura-robotics.com."""
from __future__ import annotations

# slug -> list of (category_title, [(label, value), ...])
# Valori da datasheet/pagine ufficiali costruttore (verificati 2026-06).

MIR250_PLATFORM = [
    ("Piattaforma e dimensioni", [
        ("Payload", "250 kg"),
        ("Dimensioni (L×P×H)", "800 × 580 × 300 mm"),
        ("Peso", "78 kg"),
        ("Velocità max", "2,0 m/s"),
        ("Corridoio minimo", "800 mm"),
        ("Protezione", "IP52"),
    ]),
    ("Navigazione e sicurezza", [
        ("Navigazione", "SLAM laser 2D/3D"),
        ("Scanner sicurezza", "2× laser SICK microScan3"),
        ("Certificazione", "PL d · ISO 3691-4"),
        ("Rampa max", "5°"),
    ]),
    ("Batteria e autonomia", [
        ("Tipo batteria", "Li-ion 24 V"),
        ("Autonomia", "~13 h (tipica)"),
        ("Ricarica", "Stazione MiR (opz.)"),
    ]),
    ("Software e integrazione", [
        ("Flotta", "MiR Fleet"),
        ("API", "REST · MQTT"),
        ("Standard", "VDA 5050 (opz.)"),
        ("Top module", "UR+ · custom"),
    ]),
]

MIR250_SHELF_EXTRA = [
    ("Modulo Shelf Carrier", [
        ("Funzione", "Trasporto scaffali e carrelli"),
        ("Payload modulo", "250 kg"),
        ("Uso tipico", "Shelf-to-person · kanban"),
    ]),
]

MIR250_HOOK_EXTRA = [
    ("Modulo Hook", [
        ("Funzione", "Traino carrelli e traini manuali"),
        ("Payload traino", "250 kg"),
        ("Vantaggio", "Nessuna modifica ai carrelli esistenti"),
    ]),
]

MIR600_PLATFORM = [
    ("Piattaforma e dimensioni", [
        ("Payload", "600 kg"),
        ("Dimensioni (L×P×H)", "1.350 × 920 × 320 mm"),
        ("Peso", "238 kg"),
        ("Velocità max", "2,0 m/s"),
        ("Corridoio minimo", "1.400 mm"),
        ("Protezione", "IP52"),
    ]),
    ("Navigazione e sicurezza", [
        ("Navigazione", "SLAM laser 2D/3D"),
        ("Scanner sicurezza", "2× laser SICK microScan3"),
        ("Certificazione", "PL d · ISO 3691-4"),
    ]),
    ("Batteria e autonomia", [
        ("Tipo batteria", "Li-ion 48 V"),
        ("Autonomia", "~8 h (tipica)"),
    ]),
    ("Software e integrazione", [
        ("Flotta", "MiR Fleet"),
        ("API", "REST · MQTT"),
        ("Top module", "UR+ · pallet · shelf"),
    ]),
]

MIR600_PALLET_EXTRA = [
    ("Modulo Pallet Lift", [
        ("Payload lift", "600 kg"),
        ("Pallet", "EUR 800 × 1.200 mm"),
        ("Funzione", "Pick-up · trasporto · deposito"),
    ]),
]

MIR600_SHELF_EXTRA = [
    ("Modulo Shelf Lift", [
        ("Payload", "600 kg"),
        ("Funzione", "Sollevamento sottoscocca shelf/carrelli"),
        ("Uso", "Shelf-to-person industriale"),
    ]),
]

MIR1350_PLATFORM = [
    ("Piattaforma e dimensioni", [
        ("Payload", "1.350 kg"),
        ("Dimensioni (L×P×H)", "1.350 × 920 × 320 mm"),
        ("Peso", "350 kg"),
        ("Velocità max", "1,2 m/s"),
        ("Protezione", "IP52"),
    ]),
    ("Navigazione e sicurezza", [
        ("Navigazione", "SLAM laser 2D/3D"),
        ("Certificazione", "PL d · ISO 3691-4"),
    ]),
    ("Batteria e autonomia", [
        ("Autonomia", "~6–10 h"),
    ]),
    ("Software e integrazione", [
        ("Flotta", "MiR Fleet"),
        ("API", "REST · MQTT"),
    ]),
]

MIR1350_PALLET_EXTRA = [
    ("Modulo Pallet Lift", [
        ("Payload lift effettivo", "1.250 kg"),
        ("Pallet", "EUR 800 × 1.200 mm"),
        ("Autonomia", "~10,5 h"),
    ]),
]

MIR1200 = [
    ("Transpallet autonomo", [
        ("Payload", "1.200 kg"),
        ("Tipo", "Pallet jack EU"),
        ("Pallet", "EUR standard"),
        ("Flotta", "MiR Fleet"),
    ]),
    ("Navigazione e sicurezza", [
        ("Navigazione", "SLAM laser"),
        ("Sicurezza", "ISO 3691-4"),
        ("Integrazione", "WMS / ERP API"),
    ]),
    ("Brand", [
        ("Produttore", "Mobile Industrial Robots (Teradyne)"),
    ]),
]

L300 = [
    ("Piattaforma", [
        ("Payload", "300 kg"),
        ("Dimensioni (L×P×H)", "800 × 619 × 330 mm"),
        ("Peso", "180 kg"),
        ("Lift", "60 mm · rotazione 360°"),
        ("Velocità max", "1,5 m/s"),
    ]),
    ("Navigazione", [
        ("Tipo", "Laser SLAM"),
        ("Precisione", "±5 mm"),
        ("Software", "YOUIFLEET"),
    ]),
    ("Autonomia", [
        ("Runtime", "~8 h"),
        ("Certificazioni", "CE"),
    ]),
]

L1000 = [
    ("Piattaforma", [
        ("Payload", "1.000 kg"),
        ("Dimensioni (L×P×H)", "1.060 × 838 × 300 mm"),
        ("Peso", "310 kg"),
        ("Lift", "60 mm sottoscocca"),
        ("Velocità max", "1,5 m/s"),
    ]),
    ("Navigazione", [
        ("Tipo", "Laser SLAM"),
        ("Precisione", "±5 mm"),
        ("Software", "YOUIFLEET"),
    ]),
    ("Autonomia", [
        ("Runtime", "~8 h"),
    ]),
]

JUNO_PLUS = [
    ("Piattaforma", [
        ("Payload", "200 kg"),
        ("Dimensioni", "900 × 600 × 1.240 mm"),
        ("Velocità max", "1,0 m/s"),
        ("Autonomia", "> 8 h"),
    ]),
    ("Navigazione", [
        ("Tipo", "SLAM 2D"),
        ("Funzioni", "Follow-me"),
        ("Ambiente", "Indoor / outdoor"),
    ]),
    ("Setup", [
        ("Deploy", "~1 h"),
    ]),
]

JUNO_LIFT = [
    ("Piattaforma", [
        ("Payload", "200 kg"),
        ("Dimensioni", "710 × 500 × 1.240 mm"),
        ("Lift", "Integrato"),
        ("Autonomia", "10 h"),
    ]),
    ("Navigazione", [
        ("Tipo", "SLAM 2D"),
        ("Funzioni", "Follow-me + lift"),
    ]),
]

MAV1500 = [
    ("Piattaforma", [
        ("Payload", "1.500 kg"),
        ("Dimensioni (L×P×H)", "1.530 × 910 × 294 mm"),
        ("Peso", "400 kg"),
        ("Lift", "0–55 mm"),
        ("Velocità max", "1,5 m/s"),
    ]),
    ("Sicurezza e IP", [
        ("Safety", "PL d Cat.3"),
        ("IP", "IP44 (IP54 opz.)"),
    ]),
    ("Software", [
        ("Protocolli", "ROS2 · OPC UA · VDA 5050"),
        ("Origine", "Progettato in Germania"),
    ]),
]

MAV_LARA = MAV1500 + [
    ("Cobot integrato", [
        ("Modello", "Neura LARA 5"),
        ("Payload cobot", "5 kg"),
        ("Reach", "800 mm"),
        ("Ripetibilità", "±0,02 mm"),
    ]),
]

XP15 = [
    ("Transpallet AMR", [
        ("Payload", "1.500 kg"),
        ("Dimensioni", "1.695 × 842 mm"),
        ("Peso", "335 kg"),
        ("Forche", "1.150–1.500 mm"),
    ]),
    ("Navigazione", [
        ("Sensori", "LiDAR 2D + camera"),
        ("Precisione", "±20 mm"),
        ("Modalità", "Autonomo + manuale"),
    ]),
    ("Alimentazione", [
        ("Batteria", "24 V / 60 Ah"),
        ("Velocità max", "1,25 m/s"),
    ]),
]

ACCORDION_BY_SLUG: dict[str, list] = {
    "mir250-base": MIR250_PLATFORM,
    "mir250-shelf": MIR250_PLATFORM + MIR250_SHELF_EXTRA,
    "mir250-hook": MIR250_PLATFORM + MIR250_HOOK_EXTRA,
    "mir600-base": MIR600_PLATFORM,
    "mir600-pallet": MIR600_PLATFORM + MIR600_PALLET_EXTRA,
    "mir600-shelf": MIR600_PLATFORM + MIR600_SHELF_EXTRA,
    "mir1350-base": MIR1350_PLATFORM,
    "mir1350-pallet": MIR1350_PLATFORM + MIR1350_PALLET_EXTRA,
    "mir1200": MIR1200,
    "l300": L300,
    "l1000": L1000,
    "juno-plus": JUNO_PLUS,
    "juno-lift": JUNO_LIFT,
    "mav-1500": MAV1500,
    "mav-lara": MAV_LARA,
    "xp15": XP15,
}


def included_cards(slug: str, title: str, brand: str) -> list[tuple[str, str]]:
    base = [
        ("Robot", title.split("—")[0].strip() if "—" in title else title),
        ("Brand", brand),
        ("Assessment", "Sopralluogo Abra"),
        ("Analisi", "Fattibilità iniziale"),
        ("Supporto", "Integrazione IT"),
    ]
    if slug.startswith("mir"):
        base[2] = ("MiR Fleet", "Licenza su preventivo")
    return base
