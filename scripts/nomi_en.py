"""Nomi di listino (in italiano) resi in inglese per le pagine non italiane (EN e lingue europee).
Solo termini di catalogo; i codici e i nomi propri restano uguali. Uso: from nomi_en import nome_en"""
from __future__ import annotations

import re

# dal piu' lungo al piu' corto: le frasi composte prima delle parole singole
TERMINI = [
    ("con telecomando con schermo", "with screen remote controller"),
    ("Gimbal a Doppio Spettro", "dual-spectrum gimbal"),
    ("Doppia telecamera", "dual camera"),
    ("modulo 3-in-1", "3-in-1 module"),
    ("telecamera di profondità", "depth camera"),
    ("modulo Testa a 2 Gradi di Libertà", "2-DoF head module"),
    ("modulo Nvidia Orin NX per", "Nvidia Orin NX module for"),
    ("batteria a lunga autonomia", "long-range battery"),
    ("Batteria removibile del telaio", "removable chassis battery"),
    ("modulo UWB Companion", "UWB Companion module"),
    ("Modulo UWB follow con etichetta", "UWB follow module with tag"),
    ("scheda di calcolo Dedicata", "dedicated compute board"),
    ("modulo AGX Dedicato", "dedicated AGX module"),
    ("Gruppo Quattro Ruote", "four-wheel set"),
    ("kit di Conversione", "conversion kit"),
    ("Gruppo ruota singola", "single wheel assembly"),
    ("Scheda di controllo principale", "main control board"),
    ("Copertura protettiva IMU anca", "hip IMU protective cover"),
    ("Copertura in gomma collo posteriore", "back neck rubber cover"),
    ("Piastra frontale", "front wearing plate"),
    ("Suola del piede", "foot sole"),
    ("senza sensori tattili", "without tactile sensors"),
    ("con sensori tattili", "with tactile sensors"),
    ("Modulo di calcolo", "compute module"),
    ("scheda di calcolo", "compute board"),
    ("Piastra di ricarica a Contatto", "contact charging plate"),
    ("con pinza e telecamera", "with gripper and camera"),
    ("con pinza", "with gripper"),
    ("telecomando con schermo", "screen remote controller"),
    ("telecomando Dual-hand", "dual-hand remote controller"),
    ("mano Sharpawave", "SharpaWave hand"),
    ("Piattaforma di Raccolta Dati", "data collection platform"),
    ("Cloud Pubblico", "public cloud"),
    ("piantana fissa", "fixed stand"),
    ("base mobile", "mobile base"),
    ("dual-arm, base fissa o mobile", "dual-arm, fixed or mobile base"),
    ("caricabatterie rapido", "fast charger"),
    ("caricabatterie Standard", "standard charger"),
    ("caricabatterie", "charger"),
    ("scheda di ricarica", "charging board"),
    ("batteria Standard", "standard battery"),
    ("Batteria", "battery"),
    ("batteria", "battery"),
    ("basse temperature", "low temperature"),
    ("alta capacità", "high capacity"),
    ("Caricatore", "charger"),
    ("CARICATORE", "CHARGER"),
    ("BATTERIA", "BATTERY"),
    ("telecomando", "remote controller"),
    ("Sensore di Rilevamento Gas", "gas detection sensor"),
    ("Sensore di rilevamento gas", "gas detection sensor"),
    ("kit LiDAR", "LiDAR kit"),
    ("versione base", "basic version"),
    ("mano", "hand"),
    ("pinza", "gripper"),
    ("non tattile", "non-tactile"),
    ("tattile", "tactile"),
    ("senza ", "without "),
    ("con ", "with "),
]
IT = re.compile(r"\b(senza|tattile|con|telecomando|schermo|telecamera|batteria|caricabatterie|scheda|piantana|ruote?|gruppo|mano|pinza|piattaforma|modulo|supporto|lunga|ricarica|copertura|piastra|suola)\b", re.I)


def nome_en(name: str) -> str:
    out = name
    for it, en in TERMINI:
        out = re.sub(re.escape(it), en, out, flags=re.I)
    return out


def ancora_italiano(name: str) -> bool:
    return bool(IT.search(nome_en(name)))
