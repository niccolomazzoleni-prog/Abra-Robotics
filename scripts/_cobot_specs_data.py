# -*- coding: utf-8 -*-
"""Specs accordion cobot Fairino — da datasheet ufficiale / fairino.com."""
from __future__ import annotations

ACCORDION_BY_SLUG: dict[str, list[tuple[str, list[tuple[str, str]]]]] = {
    "fairino-fr3": [
        ("Meccanica", [
            ("Payload nominale", "3 kg"),
            ("Sbraccio", "922 mm"),
            ("Ripetibilità", "±0,02 mm"),
            ("Gradi di libertà", "6"),
        ]),
        ("Controllo", [
            ("Programmazione", "Pendant · Web App"),
            ("SDK", "ROS2 · Python · C++"),
            ("Protezione", "IP54"),
        ]),
    ],
    "fairino-fr5": [
        ("Meccanica", [
            ("Payload nominale", "5 kg (max 7 kg)"),
            ("Sbraccio", "922 mm"),
            ("Ripetibilità", "±0,02 mm"),
            ("Velocità TCP", "1 m/s"),
            ("Gradi di libertà", "6"),
            ("Peso robot", "~18 kg"),
        ]),
        ("Sicurezza e certificazioni", [
            ("Tipo", "Cobot collaborativo 6 assi"),
            ("Certificazioni", "CE · ISO 10218 · ISO/TS 15066"),
            ("Protezione", "IP54 (IP65 optional)"),
            ("Sensori", "Coppia su ogni giunto"),
        ]),
        ("Controllo e software", [
            ("Programmazione", "Pendant 10,1\" · Web App"),
            ("SDK", "ROS2 · Python · C++"),
            ("I/O tool", "24 V / 1,5 A"),
            ("Montaggio", "Qualsiasi orientamento"),
        ]),
        ("Alimentazione", [
            ("Potenza tipica", "276 W"),
            ("Potenza di picco", "410 W"),
            ("Temperatura", "0–45 °C"),
        ]),
    ],
    "fairino-fr10": [
        ("Meccanica", [
            ("Payload nominale", "10 kg (max 14 kg)"),
            ("Sbraccio", "1.400 mm"),
            ("Ripetibilità", "±0,05 mm"),
            ("Velocità TCP", "1,5 m/s"),
            ("Gradi di libertà", "6"),
        ]),
        ("Sicurezza e certificazioni", [
            ("Tipo", "Cobot collaborativo 6 assi"),
            ("Certificazioni", "CE · ISO 10218 · ISO/TS 15066"),
            ("Protezione", "IP54 (IP66 optional)"),
        ]),
        ("Controllo e software", [
            ("Programmazione", "Pendant 10,1\" · Web App"),
            ("SDK", "ROS2 · Python · C++"),
            ("Montaggio", "Qualsiasi orientamento"),
        ]),
        ("Applicazioni tipiche", [
            ("Machine tending", "CNC · presse"),
            ("Logistica", "Palletizzazione fine linea"),
            ("Processo", "Dispensing · saldatura leggera"),
        ]),
    ],
    "fairino-fr20": [
        ("Meccanica", [
            ("Payload nominale", "20 kg"),
            ("Sbraccio", "1.854 mm"),
            ("Ripetibilità", "±0,05 mm"),
            ("Velocità TCP", "1,5 m/s"),
            ("Gradi di libertà", "6"),
        ]),
        ("Sicurezza e certificazioni", [
            ("Tipo", "Cobot collaborativo heavy-duty"),
            ("Certificazioni", "CE · ISO 10218 · ISO/TS 15066"),
            ("Protezione", "IP54 (IP65 optional)"),
        ]),
        ("Controllo e software", [
            ("Programmazione", "Pendant 10,1\" · Web App"),
            ("SDK", "ROS2 · Python · C++"),
        ]),
        ("Applicazioni tipiche", [
            ("Palletizzazione", "Fine linea · depalletizzazione"),
            ("Handling", "Semilavorati pesanti"),
            ("Integrazione", "Gripper vacuum · pinza parallela"),
        ]),
    ],
    "fairino-fr16": [
        ("Meccanica", [
            ("Payload nominale", "16 kg"),
            ("Sbraccio", "1.034 mm"),
            ("Ripetibilità", "±0,05 mm"),
            ("Gradi di libertà", "6"),
        ]),
        ("Applicazioni", [
            ("Machine tending", "CNC · presse"),
            ("Logistica", "Handling casse"),
            ("Certificazioni", "CE · ISO 10218"),
        ]),
    ],
    "fairino-fr30": [
        ("Meccanica", [
            ("Payload nominale", "30 kg (max 35 kg)"),
            ("Sbraccio", "1.403 mm"),
            ("Ripetibilità", "±0,1 mm"),
            ("Gradi di libertà", "6"),
        ]),
        ("Applicazioni", [
            ("Palletizzazione", "EUR · alta produttività"),
            ("Handling", "Carico pesante fine linea"),
            ("Protezione", "IP54 (IP65 optional)"),
        ]),
    ],
    "fairino-palletizing-station": [
        ("Workstation", [
            ("Dimensioni", "1.200 × 1.100 mm"),
            ("Peso", "~330 kg (senza robot)"),
            ("Alimentazione", "110–240 VAC"),
            ("Compatibilità", "FR10 · FR16 · FR20 · FR30"),
        ]),
        ("Software", [
            ("Funzione", "Pattern pallet integrati"),
            ("Integrazione", "Fairino Web App"),
        ]),
    ],
    "fairino-palletizing-fr10": [
        ("Cella turnkey", [
            ("Robot", "Fairino FR10 · 10 kg"),
            ("Workstation", "Palletizing Station"),
            ("Pallet", "EUR standard"),
        ]),
        ("Servizi Abra", [
            ("Incluso", "Assessment · commissioning base"),
            ("Opzionale", "Gripper vacuum · safety scanner"),
        ]),
    ],
    "fairino-palletizing-fr20": [
        ("Cella turnkey", [
            ("Robot", "Fairino FR20 · 20 kg"),
            ("Reach", "1.854 mm"),
            ("Workstation", "Palletizing Station"),
        ]),
        ("Servizi Abra", [
            ("Incluso", "Layout cella · go-live"),
            ("Applicazioni", "Palletizzazione · depalletizzazione"),
        ]),
    ],
}


def included_cards(slug: str, title: str) -> list[tuple[str, str]]:
    base = [
        ("Robot", title),
        ("Brand", "Fairino"),
        ("Integrazione", "Abra Robotics Italia"),
    ]
    extra = {
        "fairino-fr3": ("Payload", "3 kg"),
        "fairino-fr5": ("Pendant", "10,1\" touch (opz.)"),
        "fairino-fr10": ("Reach", "1.400 mm"),
        "fairino-fr16": ("Payload", "16 kg"),
        "fairino-fr20": ("Payload", "20 kg"),
        "fairino-fr30": ("Payload", "30 kg"),
        "fairino-palletizing-station": ("Tipo", "Solo struttura"),
        "fairino-palletizing-fr10": ("Robot", "FR10 incluso"),
        "fairino-palletizing-fr20": ("Robot", "FR20 incluso"),
    }
    if slug in extra:
        base.append(extra[slug])
    return base
