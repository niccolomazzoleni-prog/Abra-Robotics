#!/usr/bin/env python3
"""Estrae URL immagini da pagine prodotto Unitree."""
import re
import urllib.request

PAGES = {
    "H2-desktop": "https://www.unitree.com/H2/",
    "B2-desktop": "https://www.unitree.com/b2/",
    "B2W-desktop": "https://www.unitree.com/b2-w/",
    "B2W-mobile": "https://www.unitree.com/mobile/b2-w/",
    "G1-desktop": "https://www.unitree.com/G1/",
    "go2-desktop": "https://www.unitree.com/go2/",
    "H2": "https://www.unitree.com/mobile/H2/",
    "H2plus": "https://www.unitree.com/H2plus/",
    "R1-D": "https://www.unitree.com/mobile/R1-D/",
    "R1": "https://www.unitree.com/R1/",
    "go2-w": "https://www.unitree.com/go2-w/",
    "A2-W": "https://www.unitree.com/mobile/A2-W/",
    "A2": "https://www.unitree.com/mobile/A2/",
    "B2": "https://www.unitree.com/mobile/B2/",
    "B2-W": "https://www.unitree.com/mobile/B2-W/",
    "Go2": "https://www.unitree.com/mobile/go2/",
    "G1": "https://www.unitree.com/mobile/G1/",
    "Dex3": "https://www.unitree.com/mobile/Dex3-1/",
    "Dex5": "https://www.unitree.com/mobile/Dex5-1/",
    "Z1": "https://www.unitree.com/mobile/Z1/",
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")

for name, url in PAGES.items():
    try:
        html = fetch(url)
        imgs = sorted(set(re.findall(r"https?://[^\s\"'<>]+\.(?:png|jpg|jpeg|webp)", html, re.I)))
        print(f"\n=== {name} ===")
        for i in imgs:
            if any(k in i for k in ("800x800", "1920x1080", "1508x1100", "1478x788", "1000x1510", "1920x1016", "428x404", "400x400")):
                print(i.split("?")[0])
    except Exception as e:
        print(f"\n=== {name} FAIL: {e}")
