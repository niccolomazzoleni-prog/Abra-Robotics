# -*- coding: utf-8 -*-
"""Specs accordion cobot Fairino — da datasheet ufficiale / fairino.com."""
from __future__ import annotations

ACCORDION_BY_SLUG: dict[str, list[tuple[str, list[tuple[str, str]]]]] = {
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
}


def included_cards(slug: str, title: str) -> list[tuple[str, str]]:
    base = [
        ("Robot", title),
        ("Brand", "Fairino"),
        ("Integrazione", "Abra Robotics Italia"),
    ]
    extra = {
        "fairino-fr5": ("Pendant", "10,1\" touch (opz.)"),
        "fairino-fr10": ("Reach", "1.400 mm"),
        "fairino-fr20": ("Payload", "20 kg"),
    }
    if slug in extra:
        base.append(extra[slug])
    return base
