#!/usr/bin/env python3
"""Scarica immagini prodotto ufficiali da unitree.com (CDN unitree.com + oss-global-cdn)."""
from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# path relativo a images/ → URL ufficiale Unitree
DOWNLOADS: dict[str, str] = {
    # R1-D — unitree.com/mobile/R1-D/
    "manifattura/unitree-r1-d.png": "https://www.unitree.com/images/71d58b69974c4f51b36c24ab72be29dc_1508x1100.png",
    "manifattura/unitree-r1-d-hero.png": "https://www.unitree.com/images/629fd2b320cf4952a9bf4333f49d1f01_1920x1080.png",
    # R1 EDU — hero famiglia (umanoide bipede; NON e9607… che è Go2W su CDN Unitree)
    "manifattura/unitree-r1.png": "__local__",
    # H2 — unitree.com/H2/ (umanoide full-body)
    "prodotti/unitree-h2-card.png": "https://www.unitree.com/images/32686742408341c5af3b5dc2f4c85b0e_3840x2160.jpg",
    "prodotti/unitree-h2-hero.png": "https://www.unitree.com/images/32686742408341c5af3b5dc2f4c85b0e_3840x2160.jpg",
    "universita/unitree-h2.png": "https://www.unitree.com/images/32686742408341c5af3b5dc2f4c85b0e_3840x2160.jpg",
    # Go2W — unitree.com/go2-w/
    "prodotti/unitree-go2w-card.png": "https://www.unitree.com/images/11d0a76afbb74e8fb7f692652b4c33e0_800x800.png",
    "prodotti/unitree-go2w-hero.png": "https://www.unitree.com/images/038fa156aa884270afeb255789da44b2_1478x788.png",
    # As2 — asset ufficiale Abra (quadrupede grigio/blu, sfondo nero)
    "prodotti/unitree-as2-pro.png": "__local__",
    "prodotti/unitree-as2-card.png": "__local__",
    # Go2 — unitree.com/go2/ (quadrupede prodotto, foto unica condivisa)
    "prodotti/unitree-go2-card.png": "https://www.unitree.com/images/f60e629392fc4164a865869f9d51cf63_1920x1080.png",
    "prodotti/unitree-go2-edu.png": "https://www.unitree.com/images/f60e629392fc4164a865869f9d51cf63_1920x1080.png",
    "prodotti/unitree-go2-air.png": "https://www.unitree.com/images/f60e629392fc4164a865869f9d51cf63_1920x1080.png",
    # A2-W — unitree.com/mobile/A2-W/
    "prodotti/unitree-a2w.png": "https://www.unitree.com/images/9f5f59e4cfb34826a8adc62e571fb269_1000x1510.png",
    "prodotti/unitree-a2w-hero.png": "https://www.unitree.com/images/776f7a26c88a4661b0f50240783b3eb4_1920x1016.png",
    # A2 — unitree.com/mobile/A2/
    "prodotti/unitree-a2.png": "https://www.unitree.com/images/9124f2efd3c04a16a2846bd1d516e757_1920x1080.jpg",
    "prodotti/unitree-a2-pro.png": "https://www.unitree.com/images/b8f82abe4aa34240b0e72438869c3ca4_1920x1080.jpg",
    # B2 — unitree.com/b2/
    "prodotti/unitree-b2.png": "https://www.unitree.com/images/f951770ea2e74197a6b0c089d13efc5a_800x800.png",
    "prodotti/unitree-b2-hero.png": "https://oss-global-cdn.unitree.com/static/576f0e6518824d7299556a07a9674325_1920x1080.jpg",
    # B2W — unitree.com/b2-w/
    "prodotti/unitree-b2w.png": "https://www.unitree.com/images/21a982b50f674ec3986ba52c73d284f7_1920x1080.png",
    # G1-D — unitree.com/mobile/G1-D + Meko SRL + RoboStore (dual-arm su colonna, NON G1 bipede)
    "manifattura/unitree-g1-d-standard.png": "https://static.wixstatic.com/media/0d5672_c3513cf910874a2ab6a1e36ae3405682~mv2.png",
    "manifattura/unitree-g1-d-flagship.png": "https://static.wixstatic.com/media/0d5672_252fdf1a7f574a178b409709ee3b567b~mv2.png",
    "manifattura/unitree-g1-d-nobg.png": "https://www.unitree.com/images/06b395ae98ec49c0a6344dfa49e10aab_1450x1834.png",
    "manifattura/unitree-g1-d-hero.png": "https://robostore.com/cdn/shop/files/unitree-g1-d-ultimate-wheeled-dual-arm-humanoid-robot-1514665.jpg",
    # H2 Plus — unitree.com/mobile/H2plus/ (NON H2 EDU)
    "prodotti/unitree-h2-plus-hero.png": "https://www.unitree.com/images/7a417fe9fa774a00922ae10306f20aff_1560x2260.jpg",
    "prodotti/unitree-h2-plus-card.png": "https://www.unitree.com/images/14dcccb4690d4344bd6754f13f78d342_1386x1284.png",
    # Accessori / compute — pagine prodotto Unitree
    "accessori/dex3-1-official.jpg": "https://www.unitree.com/images/62b5ebbd23cc428489bf358a2d463b9e_1920x1080.jpg",
    "accessori/compute-orin-nx.png": "https://oss-global-cdn.unitree.com/static/de6f3d3261a240cd9c2d88e67ea29291_400x400.png",
    "accessori/compute-agx-orin.png": "https://www.unitree.com/images/a89249d4e2284243b8379205259bcd0c_1920x1877.png",
    "accessori/compute-agx-thor.png": "https://www.unitree.com/images/6d2e9f7a1e034ed5b0da345888bbc5fc_3840x2160.jpg",
    "accessori/compute-intel-i8.png": "https://www.unitree.com/images/4bd5086c153f4729830aa43ee668d9df_428x404.png",
}


def main() -> None:
    ok, fail = 0, 0
    for rel, url in DOWNLOADS.items():
        if url == "__local__":
            print(f"Skip {rel} (asset locale)")
            continue
        dest = ROOT / "images" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        clean = url.split("?")[0]
        try:
            print(f"Downloading {rel}...")
            req = urllib.request.Request(clean, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                dest.write_bytes(resp.read())
            print(f"  OK {dest.stat().st_size} bytes")
            ok += 1
        except Exception as e:
            print(f"  FAIL {rel}: {e}")
            fail += 1
    print(f"\nCompletato: {ok} OK, {fail} errori")


if __name__ == "__main__":
    main()
