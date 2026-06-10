import re
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "images" / "manifattura" / "amr"
UA = {"User-Agent": "Mozilla/5.0"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def dl(name, url, min_size=5000):
    data = get(url)
    if len(data) < min_size:
        raise ValueError(f"too small {len(data)}")
    (OUT / name).write_bytes(data)
    print(f"OK {name} {len(data)}")


# MiR Storyblok stills + gallery
MIR = {
    "mir1200-palletjack.png": "https://a.storyblok.com/f/230581/1764x1920/13ab49ff91/mir1200-palletjack-transparent.png",
    "mir250-hero.png": "https://a.storyblok.com/f/230581/672x421/2ae31882e5/mir250-fallbackteaser.png",
    "mir600-hero.png": "https://a.storyblok.com/f/230581/672x421/347d9337e1/mir600-fallbackteaser.png",
    "mir1350-hero.png": "https://a.storyblok.com/f/230581/672x421/bdb745e5ae/mir1350-fallbackteaser.png",
    "mir250-action.jpg": "https://a.storyblok.com/f/230581/1405x799/9f9214a1f1/flexcon-modula-mir250-5.jpg",
    "mir1350-action.jpg": "https://a.storyblok.com/f/230581/3000x1997/e5188381c3/stellantis-caen-mir-alexandre-moulard-3.jpg",
    "mir1200-gallery-1.png": "https://a.storyblok.com/f/230581/206x132/fe6723ee1b/pallet_jack_on_mission.png/m/1400x0",
    "mir1200-gallery-2.png": "https://a.storyblok.com/f/230581/236x138/bb680383c2/palletjack_3d_sensors.png/m/1400x0",
}

# Neura MAV product renders + animated webp
NEURA = {
    "neura-mav-1500.webp": "https://neura-robotics.com/wp-content/uploads/2026/03/Mav_1_1.webp",
    "neura-mav-1500-side.webp": "https://neura-robotics.com/wp-content/uploads/2026/03/Mav_2_1.webp",
    "neura-mav-anim.webp": "https://neura-robotics.com/wp-content/uploads/2026/04/MAV_Trans01desktop-scaled.webp",
    "neura-mav-nav.png": "https://neura-robotics.com/wp-content/uploads/2025/05/MAV_NEURA_Robotics_Navigation_Image.png",
    "neura-mav-lara.webp": "https://neura-robotics.com/wp-content/uploads/2025/05/LARA_NEURA_Robotics_Navigation_Image.png",
}

EP = {
    "ep-xp15.jpg": "https://ep-equipment.com/amr/wp-content/uploads/sites/2/2025/11/DSC01539-1024x1024.jpg",
    "ep-xp15-gallery.jpg": "https://ep-equipment.com/amr/wp-content/uploads/sites/2/2025/10/X_mover__2_-removebg-preview-1.png",
}

YOUIBOT = {
    "youibot-l300-gallery.png": "https://youibot.usa18.mega--cloud.com/uploads/image/64254b192daa1.png",
    "youibot-l1000-gallery.png": "https://youibot.usa18.mega--cloud.com/uploads/image/64254a39d4605.png",
}

# Elmark MiR stills (known working URLs)
ELMARK = {
    "mir250-base.png": "https://elmark-automation.com/media/catalog/product/cache/2e57f2e6b7aebba8e22d3e7cb24fad8f/M/i/MiR250Light-1.png",
    "mir250-shelf.png": "https://elmark-automation.com/media/catalog/product/cache/2e57f2e6b7aebba8e22d3e7cb24fad8f/M/i/MiR250-ShelfCarrier_Light.png",
    "mir250-hook.png": "https://elmark-automation.com/media/catalog/product/cache/2e57f2e6b7aebba8e22d3e7cb24fad8f/M/i/MiR250-Hook_Front_Light.png",
    "mir600-base.png": "https://elmark-automation.com/media/catalog/product/cache/2e57f2e6b7aebba8e22d3e7cb24fad8f/M/i/MiR600-Front_Light.png",
}

print("=== MiR homepage media scan ===")
html = get("https://mobile-industrial-robots.com/").decode("utf-8", "replace")
for kind, pat in [("GIF", r"https://[^\"'\s>]+\.gif"), ("MP4", r"https://[^\"'\s>]+\.mp4"), ("WEBM", r"https://[^\"'\s>]+\.webm"), ("WEBP", r"https://a\.storyblok\.com/[^\"'\s>]+\.webp")]:
    found = sorted(set(re.findall(pat, html, re.I)))
    print(kind, len(found))
    for u in found[:10]:
        print(" ", u[:100])

for batch in (MIR, NEURA, EP, YOUIBOT, ELMARK):
    print()
    for name, url in batch.items():
        try:
            dl(name, url)
        except Exception as e:
            print(f"FAIL {name}: {e}")
