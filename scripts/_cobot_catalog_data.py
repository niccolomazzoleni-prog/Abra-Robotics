# -*- coding: utf-8 -*-
"""Catalogo cobot Fairino — prezzi da riferimento Alibaba + 100% markup (×2), cambio USD/EUR 0,93."""
from __future__ import annotations

USD_EUR = 0.93
MARKUP = 2.0  # rincaro 100% sul prezzo Alibaba

# Riferimenti Alibaba (2026, listing base robot arm senza cella turnkey):
# FR5 ~$3.288–$3.588 → media $3.400
# FR10 ~$5.000–$9.500 → media $6.500
# FR20 ~$6.500–$8.888 → media $7.750

IMG = "images/manifattura"

CATALOG: tuple[tuple, ...] = (
    (
        "fairino-fr5",
        "Pick & Place · Machine Tending",
        "Fairino FR5",
        "Cobot 6 assi · 5 kg",
        "Cobot collaborativo a 6 assi con 5 kg di payload e sbraccio 922 mm. Ideale per pick & place, avvitatura, machine tending CNC e assemblaggio leggero. Certificato CE, ISO 10218 e ISO/TS 15066.",
        [
            ("Payload", "5 kg"),
            ("Sbraccio", "922 mm"),
            ("Ripetibilità", "±0,02 mm"),
            ("Velocità TCP", "1 m/s"),
        ],
        [
            ("Gradi libertà", "6"),
            ("Protezione", "IP54 (IP65 optional)"),
            ("Programmazione", "Pendant 10,1\" · Web App · ROS2"),
            ("Montaggio", "Qualsiasi orientamento"),
            ("Alimentazione tipica", "276 W"),
        ],
        "Pick & place, avvitatura, machine tending su CNC, assemblaggio leggero elettronica.",
        3400.0,
    ),
    (
        "fairino-fr10",
        "Machine Tending · Palletizzazione",
        "Fairino FR10",
        "Cobot 6 assi · 10 kg",
        "Cobot industriale 10 kg e sbraccio 1.400 mm per machine tending, palletizzazione fine linea e dispensing. Rapporto payload/prezzo tra i migliori della categoria collaborativa.",
        [
            ("Payload", "10 kg"),
            ("Sbraccio", "1.400 mm"),
            ("Ripetibilità", "±0,05 mm"),
            ("Velocità TCP", "1,5 m/s"),
        ],
        [
            ("Gradi libertà", "6"),
            ("Protezione", "IP54 (IP66 optional)"),
            ("Programmazione", "Pendant 10,1\" · Web App · ROS2"),
            ("Montaggio", "Qualsiasi orientamento"),
            ("Certificazioni", "CE · ISO 10218 · ISO/TS 15066"),
        ],
        "Machine tending presse e CNC, palletizzazione fine linea, dispensing.",
        6500.0,
    ),
    (
        "fairino-fr20",
        "Palletizzazione · Handling pesante",
        "Fairino FR20",
        "Cobot 6 assi · 20 kg",
        "Cobot heavy-duty 20 kg con sbraccio 1.854 mm per palletizzazione, depalletizzazione e handling di semilavorati pesanti. Soluzione collaborativa senza recinto fisso.",
        [
            ("Payload", "20 kg"),
            ("Sbraccio", "1.854 mm"),
            ("Ripetibilità", "±0,05 mm"),
            ("Gradi libertà", "6"),
        ],
        [
            ("Protezione", "IP54 (IP65 optional)"),
            ("Programmazione", "Pendant 10,1\" · Web App · ROS2"),
            ("Montaggio", "Qualsiasi orientamento"),
            ("Certificazioni", "CE · ISO 10218 · ISO/TS 15066"),
            ("Velocità TCP", "1,5 m/s"),
        ],
        "Palletizzazione, depalletizzazione, handling di semilavorati pesanti.",
        7750.0,
    ),
)


def sell_price_eur(alibaba_usd: float) -> int:
    return int(round(alibaba_usd * MARKUP * USD_EUR))


def price_display(alibaba_usd: float) -> str:
    eur = sell_price_eur(alibaba_usd)
    return f"da {f'{eur:,}'.replace(',', '.')},00 €"


def image_for(slug: str) -> str:
    return f"{IMG}/fairino-{slug.replace('fairino-', '')}.png"


# chip labels per landing lp-cobot
CHIPS_BY_SLUG: dict[str, tuple[str, ...]] = {
    "fairino-fr5": ("5 kg", "922 mm", "±0,02 mm", "6 assi"),
    "fairino-fr10": ("10 kg", "1.400 mm", "±0,05 mm", "6 assi"),
    "fairino-fr20": ("20 kg", "1.854 mm", "±0,05 mm", "6 assi"),
}
