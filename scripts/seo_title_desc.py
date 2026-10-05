#!/usr/bin/env python3
"""Regole SEO condivise per title e meta description (usate dai generatori e da
scripts/seo_fix_ottobre.py): title <= 60 caratteri, description 120-158."""
from __future__ import annotations
import re

MAX_TITLE = 60
MAX_DESC = 158


def seo_title(name: str, brand: str = "Abra Robotics") -> str:
    """'<nome> | Abra Robotics' accorciato senza tagliare parole."""
    name = re.sub(r"\s+", " ", name).strip()
    for cand in (f"{name} | {brand}", f"{name} | Abra", name):
        if len(cand) <= MAX_TITLE:
            return cand
    # togli la parte descrittiva dopo " — " / " - " (es. "Unitree X — Robot Quadrupede")
    short = re.split(r"\s+[—–-]\s+", name)[0]
    for cand in (f"{short} | Abra", short):
        if len(cand) <= MAX_TITLE:
            return cand
    # meglio un title lungo che due prodotti con lo stesso title troncato
    return name


def seo_desc(text: str, fallback_tail: str = "") -> str:
    """Description tra ~120 e 158 caratteri: completa le corte, accorcia le lunghe a fine frase o parola."""
    t = re.sub(r"\s+", " ", text).strip()
    if len(t) < 70 and fallback_tail:
        t = (t.rstrip(".") + ". " + fallback_tail).strip()
    if len(t) <= MAX_DESC:
        return t
    cut = t[:MAX_DESC]
    end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if end >= 100:
        return cut[: end + 1]
    return cut.rsplit(" ", 1)[0].rstrip(",;:—–-") + "…"
