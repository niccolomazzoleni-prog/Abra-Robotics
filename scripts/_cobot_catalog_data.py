# -*- coding: utf-8 -*-
"""Catalogo cobot Fairino — prezzi vendita EUR (calcolo interno, non esposto sul sito)."""
from __future__ import annotations

USD_EUR = 0.93
MARKUP = 2.0  # margine interno

IMG = "images/manifattura"

# tuple: slug, group, tag, title, subtitle, blurb, specs, rows, use_case, alibaba_usd
# group: robot | palletizing

CATALOG: tuple[tuple, ...] = (
    (
        "fairino-fr3",
        "robot",
        "Compatto · Precisione",
        "Fairino FR3",
        "Cobot 6 assi · 3 kg",
        "Cobot compatto 3 kg e sbraccio 922 mm per pick & place di precisione, ispezione e assemblaggio leggero in spazi ridotti.",
        [
            ("Payload", "3 kg"),
            ("Sbraccio", "922 mm"),
            ("Ripetibilità", "±0,02 mm"),
            ("Velocità TCP", "1 m/s"),
        ],
        [
            ("Gradi libertà", "6"),
            ("Protezione", "IP54"),
            ("Programmazione", "Pendant · Web App · ROS2"),
            ("Montaggio", "Qualsiasi orientamento"),
        ],
        "Pick & place precisione, ispezione, assemblaggio leggero in celle compatte.",
        3100.0,
    ),
    (
        "fairino-fr5",
        "robot",
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
        "robot",
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
        "fairino-fr16",
        "robot",
        "Machine Tending · Logistica",
        "Fairino FR16",
        "Cobot 6 assi · 16 kg",
        "Cobot 16 kg con sbraccio 1.034 mm per machine tending, handling medio e applicazioni logistica interna ad alto throughput.",
        [
            ("Payload", "16 kg"),
            ("Sbraccio", "1.034 mm"),
            ("Ripetibilità", "±0,05 mm"),
            ("Velocità TCP", "1,5 m/s"),
        ],
        [
            ("Gradi libertà", "6"),
            ("Protezione", "IP54"),
            ("Programmazione", "Pendant · Web App · ROS2"),
            ("Certificazioni", "CE · ISO 10218 · ISO/TS 15066"),
        ],
        "Machine tending, carico/scarico macchine, handling casse e fine linea.",
        8200.0,
    ),
    (
        "fairino-fr20",
        "robot",
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
    (
        "fairino-fr30",
        "robot",
        "Palletizzazione heavy-duty",
        "Fairino FR30",
        "Cobot 6 assi · 30 kg",
        "Cobot top di gamma 30 kg e sbraccio 1.403 mm per palletizzazione ad alta produttività e handling pesante in fine linea.",
        [
            ("Payload", "30 kg"),
            ("Sbraccio", "1.403 mm"),
            ("Ripetibilità", "±0,1 mm"),
            ("Velocità TCP", "1,5 m/s"),
        ],
        [
            ("Gradi libertà", "6"),
            ("Protezione", "IP54 (IP65 optional)"),
            ("Programmazione", "Pendant · Web App · ROS2/C++"),
            ("Certificazioni", "CE · ISO 10218 · ISO/TS 15066"),
        ],
        "Palletizzazione EUR, depalletizzazione, carico macchine con payload elevato.",
        18200.0,
    ),
    (
        "fairino-palletizing-station",
        "palletizing",
        "Workstation · Senza robot",
        "Fairino Palletizing Station",
        "Struttura pallet · robot escluso",
        "Workstation modulare Fairino per palletizzazione: telaio, interfaccia robot e software pallet pattern. Robot cobot non incluso — compatibile FR10–FR30.",
        [
            ("Dimensioni", "1.200 × 1.100 mm"),
            ("Peso struttura", "~330 kg"),
            ("Alimentazione", "110–240 VAC"),
            ("Robot", "Non incluso"),
        ],
        [
            ("Compatibilità", "Fairino FR10 · FR16 · FR20 · FR30"),
            ("Software", "Pallet pattern integrato"),
            ("Lead time indicativo", "~25 giorni lavorativi"),
        ],
        "Base meccanica per celle palletizzazione — abbina il cobot Fairino giusto al tuo ciclo.",
        5500.0,
    ),
    (
        "fairino-palletizing-fr10",
        "palletizing",
        "Cella turnkey · 10 kg",
        "Cella palletizzazione FR10",
        "Fairino FR10 + workstation",
        "Soluzione chiavi in mano: cobot Fairino FR10 integrato su workstation palletizzazione con programmazione pattern e avvio assistito Abra.",
        [
            ("Robot", "Fairino FR10 · 10 kg"),
            ("Workstation", "Palletizing Station"),
            ("Pallet", "EUR standard"),
            ("Ciclo tipico", "Fine linea"),
        ],
        [
            ("Incluso Abra", "Assessment · commissioning base"),
            ("Non incluso", "Gripper vacuum dedicato · safety scanner"),
            ("Certificazioni", "CE · valutazione rischio su progetto"),
        ],
        "Palletizzazione fine linea per PMI — installazione rapida senza recinto.",
        16500.0,
    ),
    (
        "fairino-palletizing-fr20",
        "palletizing",
        "Cella turnkey · 20 kg",
        "Cella palletizzazione FR20",
        "Fairino FR20 + workstation",
        "Cella palletizzazione heavy-duty con Fairino FR20 (20 kg) e workstation: ideale per casse, sacchi e pallet EUR in logistica interna.",
        [
            ("Robot", "Fairino FR20 · 20 kg"),
            ("Workstation", "Palletizing Station"),
            ("Reach", "1.854 mm"),
            ("Payload max", "20 kg"),
        ],
        [
            ("Incluso Abra", "Assessment · layout cella · go-live"),
            ("Applicazioni", "Palletizzazione · depalletizzazione"),
            ("Lead time", "4–6 settimane tipiche"),
        ],
        "Automazione pallet fine linea con payload elevato e ROI 12–24 mesi.",
        19800.0,
    ),
)

IMAGE_FILE: dict[str, str] = {
    "fairino-fr3": "fairino-fr5.png",
    "fairino-fr16": "fairino-fr10.png",
    "fairino-fr30": "fairino-fr20.png",
    "fairino-palletizing-station": "fairino-fr20.png",
    "fairino-palletizing-fr10": "fairino-fr10.png",
    "fairino-palletizing-fr20": "fairino-fr20.png",
}

CHIPS_BY_SLUG: dict[str, tuple[str, ...]] = {
    "fairino-fr3": ("3 kg", "922 mm", "±0,02 mm", "6 assi"),
    "fairino-fr5": ("5 kg", "922 mm", "±0,02 mm", "6 assi"),
    "fairino-fr10": ("10 kg", "1.400 mm", "±0,05 mm", "6 assi"),
    "fairino-fr16": ("16 kg", "1.034 mm", "±0,05 mm", "6 assi"),
    "fairino-fr20": ("20 kg", "1.854 mm", "±0,05 mm", "6 assi"),
    "fairino-fr30": ("30 kg", "1.403 mm", "±0,1 mm", "6 assi"),
    "fairino-palletizing-station": ("1.200 mm", "330 kg", "Modulare", "No robot"),
    "fairino-palletizing-fr10": ("FR10", "10 kg", "Turnkey", "Fine linea"),
    "fairino-palletizing-fr20": ("FR20", "20 kg", "Turnkey", "Heavy-duty"),
}


def sell_price_eur(alibaba_usd: float) -> int:
    return int(round(alibaba_usd * MARKUP * USD_EUR))


def price_display(alibaba_usd: float) -> str:
    eur = sell_price_eur(alibaba_usd)
    return f"da {f'{eur:,}'.replace(',', '.')},00 €"


def image_for(slug: str) -> str:
    fname = IMAGE_FILE.get(slug, f"fairino-{slug.replace('fairino-', '')}.png")
    return f"{IMG}/{fname}"


def catalog_by_group(group: str) -> list[tuple]:
    return [row for row in CATALOG if row[1] == group]
