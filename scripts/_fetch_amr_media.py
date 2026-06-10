"""Discover and download AMR images/GIFs."""
import json
import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "images" / "manifattura" / "amr"
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def dl(name: str, url: str, min_size=5000) -> bool:
    dest = OUT / name
    try:
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=30).read()
        if len(data) < min_size:
            print(f"  SKIP {name}: {len(data)} bytes")
            return False
        dest.write_bytes(data)
        print(f"  OK {name}: {len(data)} bytes")
        return True
    except Exception as e:
        print(f"  FAIL {name}: {e}")
        return False


def elmark_imgs(slug: str) -> list[str]:
    url = f"https://elmark-automation.com/shop/mobile-industrial-robots/{slug}"
    html = get(url)
    imgs = re.findall(
        r"https://elmark-automation\.com/media/catalog/product/cache/2e57f2e6b7aebba8e22d3e7cb24fad8f/[^\"'\\]+\.png",
        html.replace("\\/", "/"),
    )
    return list(dict.fromkeys(imgs))


def mir_site_gifs() -> list[str]:
    for url in [
        "https://mobile-industrial-robots.com/",
        "https://mobile-industrial-robots.com/marketplace/mir250/",
        "https://mobile-industrial-robots.com/marketplace/mir600/",
        "https://mobile-industrial-robots.com/marketplace/mir1200-pallet-jack/",
        "https://mobile-industrial-robots.com/marketplace/mir1350/",
    ]:
        try:
            html = get(url)
            gifs = re.findall(r"https?://[^\"'\s>]+\.gif", html, re.I)
            imgs = re.findall(r"https?://[^\"'\s>]+\.(?:png|webp|jpg)", html, re.I)
            print(f"\n{url}")
            for u in gifs[:5]:
                print(f"  GIF {u}")
            for u in imgs:
                if any(x in u.lower() for x in ("mir", "pallet", "robot", "amr")) and "logo" not in u.lower():
                    print(f"  IMG {u[:100]}")
        except Exception as e:
            print(f"FAIL {url}: {e}")
    return []


def neura_mav_imgs() -> list[str]:
    html = get("https://neura-robotics.com/products/mav/")
    # product renders, 3d, hero
    found = []
    for pat in [
        r'https://neura-robotics\.com/wp-content/uploads/[^\"\'\s>]+\.(?:png|jpg|webp|gif)',
        r'srcset="([^"]+)"',
        r'data-src="([^"]+)"',
    ]:
        for m in re.findall(pat, html):
            if isinstance(m, str) and m.startswith("http"):
                found.append(m.split()[0] if " " in m else m)
            elif "," in m:
                for part in m.split(","):
                    u = part.strip().split()[0]
                    if u.startswith("http"):
                        found.append(u)
    out = []
    for u in found:
        low = u.lower()
        if any(x in low for x in ("favicon", "maira", "logo", "icon")):
            continue
        if "mav" in low or "navigation" in low or "robot" in low or "product" in low:
            out.append(u)
    return list(dict.fromkeys(out))


print("=== ELMARK PRODUCT IMAGES ===")
for slug, fname in [
    ("autonomous-mobile-robot-mir1200", "mir1200"),
    ("autonomous-mobile-robot-mir1350", "mir1350"),
    ("autonomous-mobile-robot-mir250", "mir250"),
    ("autonomous-mobile-robot-mir600", "mir600"),
]:
    try:
        imgs = elmark_imgs(slug)
        print(f"\n{slug}: {len(imgs)} images")
        for i, u in enumerate(imgs[:6]):
            print(f"  [{i}] {u.split('/')[-1]}")
        if imgs:
            dl(f"{fname}-1.png", imgs[0])
            for i, u in enumerate(imgs[1:4], 2):
                dl(f"{fname}-{i}.png", u, min_size=3000)
    except Exception as e:
        print(f"ERR {slug}: {e}")

print("\n=== NEURA MAV ===")
for u in neura_mav_imgs()[:15]:
    print(u)
for u in neura_mav_imgs():
    if "MAV" in u or "mav" in u.lower():
        if dl("neura-mav-hero.png", u):
            break
# try full-size navigation render
dl("neura-mav-1500.png", "https://neura-robotics.com/wp-content/uploads/2025/05/MAV_NEURA_Robotics_Navigation_Image-1536x512.png", min_size=10000)
dl("neura-mav-product.png", "https://neura-robotics.com/wp-content/uploads/2025/05/MAV-rgb-black-1-1536x349.png", min_size=8000)

print("\n=== MIR OFFICIAL GIFS ===")
mir_site_gifs()

# Unchained DE
try:
    html = get("https://unchainedrobotics.de/en/products/robot/mobile-robots/amr/neura-mav-1500")
    shop = re.findall(r"https://cdn\.shopify\.com/s/files/[^\"'\s>]+\.(?:png|jpg|webp|gif)", html)
    print("\n=== UNCHAINED NEURA ===")
    for u in shop[:6]:
        print(u)
        if "mav" in u.lower() or len(shop) == 1:
            dl("neura-mav-shopify.png", u, min_size=5000)
except Exception as e:
    print(f"Unchained: {e}")

try:
    html = get("https://unchainedrobotics.de/en/products/robot/mobile-robots/amr/ep-equipment-xp15")
    shop = re.findall(r"https://cdn\.shopify\.com/s/files/[^\"'\s>]+\.(?:png|jpg|webp|gif)", html)
    print("\n=== UNCHAINED XP15 ===")
    for u in shop[:4]:
        print(u)
    if shop:
        dl("ep-xp15-shopify.png", shop[0], min_size=5000)
except Exception as e:
    print(f"Unchained XP15: {e}")

# EP official better photo
dl("ep-xp15-hero.jpg", "https://ep-equipment.com/amr/wp-content/uploads/sites/2/2025/11/DSC01539-1024x1024.jpg", min_size=20000)
