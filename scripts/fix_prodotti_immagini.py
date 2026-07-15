#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applica le immagini prodotto CORRETTE (verificate visivamente dalle pagine Unitree reali).
Le pagine Unitree sono SPA: le immagini condivise nel menu erano quelle che avevano
inquinato il primo tentativo. Qui usiamo le immagini specifiche di ogni pagina."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "images" / "prodotti"
TMP = ROOT / "images" / "_tmp"


def load(rel_or_abs) -> Image.Image:
    p = rel_or_abs if isinstance(rel_or_abs, Path) else ROOT / rel_or_abs
    return Image.open(p).convert("RGBA")


def main() -> None:
    # Immagini reali Unitree verificate (scaricate in images/_tmp)
    g1d_standard = load(TMP / "cand-g1d-d.png")   # confronto Standard(fisso)+Flagship
    g1d_flagship = load(TMP / "cand-g1d-b.png")   # G1-D dual-arm su base mobile
    h2_plus = load(TMP / "cand-h2plus-b.png")     # H2 Plus (dinamico, sfondo scuro)
    dex5 = load(TMP / "cand-dex5-b.png")          # mano Dex5 tattile

    # Immagini locali reali già corrette
    as2w = load("images/prodotti/as2-w.png")       # quadrupede a ruote (già ok)
    go2 = load("prodotti/assets/variants/go2-pro/img-01.png")  # Go2 studio
    h2 = load("images/prodotti/h2-edu.png")        # H2 umanoide (per H2-D)
    d1 = load("images/accessori/d1.jpg")           # braccio D1
    lidar = load("images/accessori/hesai-xt16.png")  # sensore LiDAR
    rc = load("images/accessori/rc-g1.jpg")        # telecomando G1 (R3)

    mapping = {
        "g1-d-standard.png": g1d_standard,
        "g1-d-flagship.png": g1d_flagship,
        "as2-w.png": as2w,
        "go2-x.png": go2,
        "h2-plus.png": h2_plus,
        "h2-d.png": h2,
        "d1-t-standard.png": d1,
        "d1-t-full.png": d1,
        "lidar-l1.png": lidar,
        "lidar-l2.png": lidar,
        "dex2-5.png": dex5,
        "r3.png": rc,
    }

    for name, img in mapping.items():
        img.save(DST / name, "PNG")
        print(f"OK {name}")

    # immagine hub g1-d.html (confronto)
    g1d_standard.save(DST / "g1-d-hub.png", "PNG")
    print("OK g1-d-hub.png")
    print("Fatto.")


if __name__ == "__main__":
    main()
