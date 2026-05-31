"""
Pipeline:
1) restore originale (con logo RoboStore)
2) crop 1024x1024 centrato sul logo RoboStore
3) mask: trasparente sulla bbox del logo, opaca altrove
4) OpenAI gpt-image-1 /v1/images/edits -> crop pulito
5) ricompone nel grande
6) sovrappone logo ABRA ROBOTICS (PNG) nella stessa zona, multiply blend
"""
import os, io, base64, sys, json
from pathlib import Path
import requests
import numpy as np
import cv2
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent
PROJ = ROOT.parent.parent
ORIG_DIR = ROOT / "_originals" / "images"
DEST_DIR = ROOT / "images"
LOGO_PATH = PROJ / "images" / "logo.png"

# Carica API key da ~/.openai_env
env_file = Path.home() / ".openai_env"
for line in env_file.read_text().splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip()
API_KEY = os.environ["OPENAI_API_KEY"]

# (file, box_logo_robostore)
JOBS = {
    # filename: (mask_box, logo_center). logo_center=None -> usa il centro della mask box.
    "g1-01.jpg":      ((820, 445, 1185, 510),   None),
    "g1-04.jpg":      ((855, 1005, 1410, 1105), (1090, 1055)),
    "g1-05.jpg":      ((1300, 435, 1580, 510),  None),
    "g1-06.png":      ((20, 1855, 590, 1990),   (265, 1922)),
    "collage-01.jpg": ((725, 1240, 1410, 1380), (1030, 1307)),
    "collage-05.jpg": ((1010, 720, 1370, 810),  None),
}

CROP_SIZE = 1024
PROMPT = (
    "Restore the chest plate of a humanoid robot with a completely smooth, "
    "blank, polished metallic silver surface. Absolutely no text whatsoever. "
    "No letters, no words, no logos, no brand marks, no watermarks, no symbols, "
    "no characters of any kind. Clean uniform metal with subtle realistic "
    "highlights and panel lines only. Studio product photography."
)


def get_crop_bounds(box, img_w, img_h, crop=CROP_SIZE):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    half = crop // 2
    cx0 = max(0, min(img_w - crop, cx - half))
    cy0 = max(0, min(img_h - crop, cy - half))
    return cx0, cy0, cx0 + crop, cy0 + crop


def build_mask(crop_size, logo_box_in_crop, feather=8):
    """Maschera RGBA 1024x1024. Trasparente dentro la box (zona da rigenerare), opaca fuori."""
    lx0, ly0, lx1, ly1 = logo_box_in_crop
    # alpha: 255 ovunque, 0 dentro la box
    alpha = Image.new("L", (crop_size, crop_size), 255)
    inner = Image.new("L", (lx1 - lx0, ly1 - ly0), 0)
    alpha.paste(inner, (lx0, ly0))
    # white RGB (irrelevante), alpha indica cosa preservare
    mask = Image.new("RGBA", (crop_size, crop_size), (255, 255, 255, 255))
    mask.putalpha(alpha)
    return mask


def openai_inpaint(crop_png_bytes, mask_png_bytes, prompt=PROMPT):
    url = "https://api.openai.com/v1/images/edits"
    files = {
        "image": ("image.png", crop_png_bytes, "image/png"),
        "mask":  ("mask.png",  mask_png_bytes, "image/png"),
    }
    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": f"{CROP_SIZE}x{CROP_SIZE}",
        "quality": "high",
        "n": "1",
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    r = requests.post(url, headers=headers, files=files, data=data, timeout=180)
    if r.status_code != 200:
        raise RuntimeError(f"OpenAI API {r.status_code}: {r.text[:600]}")
    b64 = r.json()["data"][0]["b64_json"]
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")


def overlay_abra_logo(img_pil, box_orig, logo_path=LOGO_PATH, width_ratio=0.85, center=None):
    """Sovrappone logo ABRA ROBOTICS al posto del RoboStore.
    box_orig: usato per dimensionare il logo (in base alla larghezza)
    center: (cx, cy) override. Se None, usa il centro della box.
    """
    x0, y0, x1, y1 = box_orig
    box_w = x1 - x0
    if center is not None:
        cx, cy = center
    else:
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2

    logo = Image.open(logo_path).convert("RGBA")
    lw, lh = logo.size
    target_w = int(box_w * width_ratio)
    scale = target_w / lw
    target_h = int(lh * scale)
    logo = logo.resize((target_w, target_h), Image.LANCZOS)

    base = img_pil.convert("RGBA")
    pos = (cx - target_w // 2, cy - target_h // 2)
    base.alpha_composite(logo, dest=pos)
    return base.convert("RGB")


def process(filename):
    box, logo_center = JOBS[filename]
    src = ORIG_DIR / filename
    dst = DEST_DIR / filename
    pil = Image.open(src).convert("RGB")
    W, H = pil.size
    cx0, cy0, cx1, cy1 = get_crop_bounds(box, W, H)
    crop = pil.crop((cx0, cy0, cx1, cy1))

    # mask coords nel crop
    logo_box_in_crop = (box[0] - cx0, box[1] - cy0, box[2] - cx0, box[3] - cy0)
    mask = build_mask(CROP_SIZE, logo_box_in_crop)

    # serializza per API
    crop_buf = io.BytesIO(); crop.save(crop_buf, format="PNG"); crop_buf.seek(0)
    mask_buf = io.BytesIO(); mask.save(mask_buf, format="PNG"); mask_buf.seek(0)

    print(f"[{filename}] calling OpenAI gpt-image-1 edits...")
    edited_crop = openai_inpaint(crop_buf.getvalue(), mask_buf.getvalue())
    print(f"[{filename}] received {edited_crop.size}")

    # Post-process: prendi SOLO la zona del logo dal risultato AI,
    # lasciando il resto del crop intatto. Feather sui bordi.
    crop_np    = np.array(crop).astype(np.float32)             # (1024,1024,3)
    edited_np  = np.array(edited_crop).astype(np.float32)
    lx0, ly0, lx1, ly1 = logo_box_in_crop
    # Dilato il core di N px (alpha=1 esteso), poi blur leggero solo per smussare bordi
    margin = 18
    alpha = np.zeros((CROP_SIZE, CROP_SIZE), dtype=np.float32)
    alpha[max(0, ly0 - margin):min(CROP_SIZE, ly1 + margin),
          max(0, lx0 - margin):min(CROP_SIZE, lx1 + margin)] = 1.0
    alpha = cv2.GaussianBlur(alpha, (0, 0), sigmaX=3, sigmaY=3)
    alpha = np.clip(alpha, 0, 1)[:, :, None]
    blended = edited_np * alpha + crop_np * (1 - alpha)
    merged_crop = Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8))

    # ricomponi nel grande
    pil.paste(merged_crop, (cx0, cy0))

    # sovrapponi logo ABRA ROBOTICS al posto del RoboStore
    pil = overlay_abra_logo(pil, box, center=logo_center)

    # salva
    if filename.endswith(".png"):
        pil.save(dst, optimize=True)
    else:
        pil.save(dst, quality=92, subsampling=1, optimize=True)
    print(f"[{filename}] saved -> {dst}")


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(JOBS.keys())
    for f in targets:
        process(f)
