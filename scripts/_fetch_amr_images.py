"""Fetch AMR product images for catalog."""
import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "images" / "manifattura" / "amr"
OUT.mkdir(parents=True, exist_ok=True)

STATIC = {
    "mir600-pallet-lift.png": "https://elmark-automation.com/media/catalog/product/cache/2e57f2e6b7aebba8e22d3e7cb24fad8f/M/i/MiR600_EU_Pallet_Lift_Light.png",
    "mir1200-pallet.png": "https://elmark-automation.com/media/catalog/product/cache/2e57f2e6b7aebba8e22d3e7cb24fad8f/M/i/MiR1200_Pallet_Jack_EU_Light.png",
}

PAGES = {
    "ep-xp15.png": [
        "https://ep-equipment.com/amr/product/xp15/",
        "https://unchainedrobotics.de/en/products/robot/mobile-robots/amr/ep-equipment-xp15",
        "https://viistif.com/en/product/xp15/",
    ],
    "neura-mav-1500.png": [
        "https://neura-robotics.com/products/mav/",
        "https://unchainedrobotics.de/en/products/robot/mobile-robots/amr/neura-mav-1500",
    ],
}


def fetch_page(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


def find_images(html: str) -> list[str]:
    found = []
    for pat in [
        r"https://cdn\.shopify\.com/s/files/[^\"'\s>]+\.(?:jpg|png|webp)",
        r"https://[^\"'\s>]+\.(?:jpg|png|webp)",
        r'data-amsrc="(https://[^"]+\.(?:png|jpg|webp))"',
        r'"img":"(https:\\/\\/[^"]+\.(?:png|jpg|webp))"',
    ]:
        for m in re.findall(pat, html):
            u = m.replace("\\/", "/")
            low = u.lower()
            if any(x in low for x in ("logo", "loader", "favicon", "icon", "banner", "cropped-favicon")):
                continue
            if "mav" in low and "maira" not in low:
                found.append(u)
            elif "xp15" in low or "x_mover" in low or "dsc01539" in low:
                found.append(u)
            elif "mir1200" in low or "pallet_jack" in low:
                found.append(u)
            elif "shopify" in low and ("xp15" in low or "mav" in low):
                found.append(u)
            elif "ep-equipment" in low or "viistif" in low:
                found.append(u)
    # fallback: any large product-ish image
    if not found:
        for m in re.findall(r"https://[^\"'\s>]+\.(?:jpg|png|webp)", html):
            low = m.lower()
            if not any(x in low for x in ("logo", "loader", "favicon", "icon")):
                found.append(m)
    return list(dict.fromkeys(found))


def download(name: str, url: str) -> bool:
    dest = OUT / name
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=20).read()
        if len(data) < 8000:
            print(f"SKIP {name}: too small ({len(data)} bytes)")
            return False
        dest.write_bytes(data)
        print(f"OK {name} ({len(data)} bytes)")
        return True
    except Exception as e:
        print(f"FAIL {name}: {e}")
        return False


for name, url in STATIC.items():
    download(name, url)

for name, pages in PAGES.items():
    if (OUT / name).exists() and (OUT / name).stat().st_size > 8000:
        continue
    for page in pages:
        try:
            html = fetch_page(page)
            imgs = find_images(html)
            print(f"\n{name} <- {page} ({len(imgs)} candidates)")
            for img in imgs[:8]:
                print(f"  {img[:120]}")
            for img in imgs:
                if download(name, img):
                    break
            if (OUT / name).exists() and (OUT / name).stat().st_size > 8000:
                break
        except Exception as e:
            print(f"page {page}: {e}")
