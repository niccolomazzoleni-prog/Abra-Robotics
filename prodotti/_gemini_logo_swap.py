#!/usr/bin/env python3
"""Sostituisce il watermark 'ROBOSTORE' sul petto dei robot con il logo Abra Robotics,
usando il modello immagine di Gemini (Nano Banana).

Richiede:  GEMINI_API_KEY nell'ambiente.
Uso:       set -a; source ~/.gemini_env; set +a; python3 _gemini_logo_swap.py
Output:    accanto a ogni input crea  <nome>-abra.jpg  (non distruttivo).
           Dopo, ri-eseguire _remove_bg_umanoidi.py puntando agli -abra per i PNG finali.
"""
import os, sys
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-image")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.environ.get("ABRA_LOGO", "/Users/niccolomazzoleni/Downloads/Abra_Logo_Transparent (3).png")  # logo Abra di riferimento

# Immagini su cui sostituire il logo (originali, NON i -nobg.png)
IMAGES = [
    "prodotti/assets/variants/g1-u1/img-01.jpg",
    "prodotti/assets/variants/g1-u2/img-01.jpg",
    "prodotti/assets/variants/g1-u3/img-01.jpg",
    "prodotti/assets/variants/g1-u4/img-01.jpg",
    "prodotti/assets/variants/g1-u5/img-01.jpg",
    "prodotti/assets/variants/g1-u6/img-01.jpg",
    "prodotti/assets/variants/g1-u7/img-01.jpg",
    "prodotti/assets/variants/g1-u8/img-01.jpg",
    "prodotti/assets/images/g1-01.jpg",
]

PROMPT = (
    "Edit the provided product photo of a robot. The robot has a 'ROBOSTORE' "
    "logo/wordmark printed on its body (e.g. on the chest). Replace ONLY that logo with "
    "the provided Abra Robotics logo (second image), matching its position, scale, "
    "perspective, surface curvature, lighting and subtle reflections so it looks "
    "physically printed on the surface.\n"
    "CRITICAL: keep the output IDENTICAL to the input in every other way. Same exact "
    "framing, same composition, same full-body view, same zoom level, same aspect ratio "
    "and same image dimensions. Do NOT crop, do NOT zoom in, do NOT recompose or change "
    "the camera. The ENTIRE robot must remain visible from head to feet (full body), "
    "with empty margin all around it exactly like the input; never cut off legs, feet or "
    "head. Same robot, same pose, same background, same colors. Only the logo changes. "
    "If no 'ROBOSTORE' logo is visible, return the image unchanged."
)

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("ERRORE: GEMINI_API_KEY non impostata nell'ambiente.")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    logo = Image.open(LOGO)

    # Forza l'aspect ratio dell'output (es. GEMINI_ASPECT=1:1) per evitare crop/reframe.
    cfg = None
    aspect = os.environ.get("GEMINI_ASPECT")
    if aspect:
        cfg = types.GenerateContentConfig(image_config=types.ImageConfig(aspect_ratio=aspect))

    # Se passo dei path come argomenti, lavoro solo su quelli (utile per il test).
    targets = sys.argv[1:] if len(sys.argv) > 1 else IMAGES
    print(f"Modello: {MODEL} · immagini: {len(targets)}")

    for rel in targets:
        src = os.path.join(BASE, rel)
        if not os.path.exists(src):
            print("  ! manca", rel); continue
        img = Image.open(src)
        try:
            resp = client.models.generate_content(model=MODEL, contents=[PROMPT, img, logo], config=cfg)
        except Exception as e:
            print(f"  ERR {rel}: {e}"); continue

        saved = False
        for part in resp.candidates[0].content.parts:
            if getattr(part, "inline_data", None) and part.inline_data.data:
                out = os.path.splitext(src)[0] + "-abra.jpg"
                Image.open(BytesIO(part.inline_data.data)).convert("RGB").save(out, quality=92)
                print(f"  OK {os.path.relpath(out, BASE)}")
                saved = True
                break
        if not saved:
            print(f"  ! nessuna immagine restituita per {rel} (rivedi prompt/modello)")

if __name__ == "__main__":
    main()
