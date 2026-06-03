#!/usr/bin/env python3
"""Rimuove lo sfondo dalle immagini umanoidi (pagina umanoidi.html).

Strategia robusta: unione di due maschere di sfondo
  A) rembg con modello isnet-general-use (gestisce i fori interni: asola testa, ecc.)
  B) flood-fill del near-bianco dai bordi (rimuove lo sfondo connesso al bordo,
     incluso lo spazio tra le gambe che comunica col bordo inferiore)
Il corpo del robot (non connesso allo sfondo) resta intatto.
Non distruttivo: salva -nobg.png accanto agli originali.
"""
import os
import numpy as np
from PIL import Image, ImageDraw
from rembg import remove, new_session

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF_THRESH = 60        # tolleranza flood-fill (somma diff per canale): ~near-bianco
SENT = (255, 0, 255)  # colore sentinella

IMAGES = [
    "prodotti/assets/images/g1-01.jpg",
    "prodotti/assets/variants/g1-u1/img-01.jpg",
    "prodotti/assets/variants/g1-u2/img-01.jpg",
    "prodotti/assets/variants/g1-u3/img-01.jpg",
    "prodotti/assets/variants/g1-u4/img-01.jpg",
    "prodotti/assets/variants/g1-u5/img-01.jpg",
    "prodotti/assets/variants/g1-u6/img-01.jpg",
    "prodotti/assets/variants/g1-u7/img-01.jpg",
    "prodotti/assets/variants/g1-u8/img-01.jpg",
    "prodotti/assets/variants/g1-comp/img-01.jpg",
]

# Immagini con prop bianchi (es. pallone) connessi allo sfondo: niente flood-fill,
# altrimenti ne "mangia" le parti bianche. Si usa la sola maschera AI.
NO_FLOODFILL = ("g1-comp",)

session = new_session("isnet-general-use")

def border_floodfill_bg(rgb):
    """Maschera (HxW bool) dello sfondo near-bianco raggiungibile dai bordi."""
    w, h = rgb.size
    tmp = rgb.copy()
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    for s in seeds:
        ImageDraw.floodfill(tmp, s, SENT, thresh=FF_THRESH)
    arr = np.asarray(tmp)
    return np.all(arr == np.array(SENT), axis=-1)

for rel in IMAGES:
    orig = os.path.join(BASE, rel)
    out = os.path.splitext(orig)[0] + "-nobg.png"      # nome usato dall'HTML
    src = os.path.splitext(orig)[0] + "-abra.jpg"       # preferisci la versione rebrandizzata
    if not os.path.exists(src):
        src = orig
    if not os.path.exists(src):
        print("  ! manca", rel); continue

    rgb = Image.open(src).convert("RGB")
    rgba = rgb.convert("RGBA")

    # A) maschera rembg (alpha morbido)
    cut = remove(rgba, session=session, post_process_mask=True)
    a_rembg = np.asarray(cut.getchannel("A"))           # 0..255
    bg_rembg = a_rembg < 12

    # Unione con flood-fill dai bordi (saltato per immagini con prop bianchi)
    alpha = a_rembg.copy()
    if not any(tag in rel for tag in NO_FLOODFILL):
        bg_ff = border_floodfill_bg(rgb)
        alpha[bg_ff] = 0
    alpha[bg_rembg] = 0

    out_arr = np.dstack([np.asarray(rgb), alpha.astype(np.uint8)])
    Image.fromarray(out_arr, "RGBA").save(out)
    removed = int((alpha == 0).sum())
    print(f"  OK {os.path.relpath(out, BASE)}  bg_px={removed}")

print("\nFatto.")
