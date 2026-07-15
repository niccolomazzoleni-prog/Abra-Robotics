#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera schede prodotto su preventivo + hub G1-D + card catalogo."""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from genera_catalogo_completo import (  # noqa: E402
    TEMPLATE,
    buy_area,
    gallery_path,
    key_specs,
    product_family,
    product_schema,
    spec_rows,
)
from site_nav import render_site_nav  # noqa: E402

PRODOTTI = ROOT / "prodotti"
IMAGES = ROOT / "images" / "prodotti"
MANIFEST = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"

# URL immagini ufficiali Unitree (CDN) — fallback locale se download fallisce
IMAGE_URLS: dict[str, str] = {
    "g1-d-standard": "https://www.unitree.com/images/563d33a0fe6146f9919f82e0e2799244_800x800.png",
    "g1-d-flagship": "https://www.unitree.com/images/e9607f806eb4483f93b5a5553446c2bc_800x800.png",
    "g1-d": "images/manifattura/unitree-g1-d-nobg.png",
    "as2-w": "https://www.unitree.com/images/2e06005b29aa4a629c131f0a6448b4f0_800x800.png",
    "go2-x": "https://www.unitree.com/images/f951770ea2e74197a6b0c089d13efc5a_800x800.png",
    "h2-plus": "https://www.unitree.com/images/8745aebc0c9c43a2a954ec08eed18805_800x800.png",
    "h2-d": "https://www.unitree.com/images/76658a29925a49a397efe2f726f5e1e3_800x800.png",
    "d1-t-standard": "https://www.unitree.com/images/148d8cc897044981ac31186d69ce369f_800x800.png",
    "d1-t-full": "https://www.unitree.com/images/11d0a76afbb74e8fb7f692652b4c33e0_800x800.png",
    "lidar-l1": "https://www.unitree.com/images/300fef5490a64cf48378253f0a54b394_428x404.png",
    "lidar-l2": "https://www.unitree.com/images/282a1e13f6414f6a9a249557a9639d31_428x404.png",
    "dex2-5": "https://www.unitree.com/images/8ce7b07719ba4b58adca7d7268e0651e_428x404.png",
    "r3": "https://www.unitree.com/images/4bd5086c153f4729830aa43ee668d9df_428x404.png",
}

PRODUCTS: list[dict] = [
    {
        "sku": "G1D-STANDARD",
        "filename": "unitree-g1-d-standard.html",
        "titolo": "Unitree G1-D Standard",
        "sottotitolo": "Dual-arm su piantana fissa · acquisizione dati AI",
        "descrizione": "Unitree G1-D Standard: piattaforma umanoide dual-arm su colonna fissa per acquisizione dati, manipolazione bimanuale e deployment industriale. Varianti U1–U5 con gripper Dex1, Dex3 o mani Revo2. Non è il G1 bipede — locomozione tramite base fissa.",
        "categoria": "UMANOIDI",
        "coll_file": "g1-d.html",
        "coll_name": "G1-D",
        "img_key": "g1-d-standard",
        "specs": [
            ["Gamma", "G1D-U1 … G1D-U5"],
            ["Base", "Piantana fissa"],
            ["Bracci", "7×2 DoF"],
            ["Payload braccio", "~3 kg"],
            ["DoF totali", "19–31 (per variante)"],
            ["Altezza colonna", "1260–1680 mm"],
            ["Autonomia", "~2 h (upper body)"],
        ],
    },
    {
        "sku": "G1D-FLAGSHIP",
        "filename": "unitree-g1-d-flagship.html",
        "titolo": "Unitree G1-D Flagship",
        "sottotitolo": "Dual-arm su base mobile · LiDAR · diff-drive",
        "descrizione": "Unitree G1-D Flagship: stessa upper body dello Standard con base mobile a ruote (diff-drive 1,5 m/s), LiDAR e autonomia estesa (~6 h). Varianti U6–U10. Ideale per data collection mobile e pilot industriali multi-stazione.",
        "categoria": "UMANOIDI",
        "coll_file": "g1-d.html",
        "coll_name": "G1-D",
        "img_key": "g1-d-flagship",
        "specs": [
            ["Gamma", "G1D-U6 … G1D-U10"],
            ["Base", "Mobile diff-drive + LiDAR"],
            ["Velocità chassis", "1,5 m/s"],
            ["Bracci", "7×2 DoF"],
            ["DoF totali", "21–33 (per variante)"],
            ["Autonomia", "~6 h (upper + chassis)"],
        ],
    },
    {
        "sku": "AS2-W",
        "filename": "unitree-as2-w.html",
        "titolo": "Unitree AS2-W",
        "sottotitolo": "Quadrupede wheeled serie AS",
        "descrizione": "Unitree AS2-W: variante wheeled della serie AS per ispezione e sorveglianza su superfici piane con maggiore autonomia e stabilità rispetto al puro quadrupede. Configurazione e listino su preventivo Abra.",
        "categoria": "UMANOIDI",
        "coll_file": "quadrupedi.html",
        "coll_name": "Quadrupedi",
        "img_key": "as2-w",
        "specs": [["Famiglia", "AS2-W"], ["Tipo", "Quadrupede wheeled"], ["Uso", "Ispezione / patrol"]],
    },
    {
        "sku": "GO2-X",
        "filename": "unitree-go2-x.html",
        "titolo": "Unitree Go2 X",
        "sottotitolo": "Quadrupede consumer/pro avanzato",
        "descrizione": "Unitree Go2 X: nuova referenza della gamma Go2. Specifiche e configurazione disponibili su preventivo — Abra conferma SKU, accessori e tempi con la supply chain Unitree.",
        "categoria": "UMANOIDI",
        "coll_file": "quadrupedi.html",
        "coll_name": "Quadrupedi",
        "img_key": "go2-x",
        "specs": [["Famiglia", "Go2 X"], ["Tipo", "Quadrupede"], ["SDK", "Da confermare su variante"]],
    },
    {
        "sku": "H2-PLUS",
        "filename": "unitree-h2-plus.html",
        "titolo": "Unitree H2 Plus",
        "sottotitolo": "Reference NVIDIA Isaac GR00T · ~182 cm",
        "descrizione": "Unitree H2 Plus: umanoide full-size con Jetson AGX Thor T5000, mani Sharpa Wave e piattaforma Isaac GR00T. Disponibilità prevista fine 2026 — preordine e configurazione su preventivo Abra.",
        "categoria": "UMANOIDI",
        "coll_file": "umanoidi.html",
        "coll_name": "Umanoidi",
        "img_key": "h2-plus",
        "specs": [
            ["Altezza", "~182 cm"],
            ["DoF", "75 (31 corpo + 44 mani)"],
            ["Compute", "Jetson AGX Thor T5000"],
            ["Disponibilità", "Fine 2026 (prev.)"],
        ],
    },
    {
        "sku": "H2-D",
        "filename": "unitree-h2-d.html",
        "titolo": "Unitree H2-D",
        "sottotitolo": "H2 con piantana / supporto fisso",
        "descrizione": "Unitree H2-D: versione H2 con piantana o supporto fisso per manipolazione bimanuale in cella, data collection e deployment industriale senza locomozione bipede. Preventivo su configurazione.",
        "categoria": "UMANOIDI",
        "coll_file": "umanoidi.html",
        "coll_name": "Umanoidi",
        "img_key": "h2-d",
        "specs": [["Base", "Piantana / supporto fisso"], ["Piattaforma", "H2 upper body"], ["Uso", "Manipolazione / AI data"]],
    },
    {
        "sku": "D1T-STD",
        "filename": "unitree-d1-t-standard.html",
        "titolo": "Unitree D1-T Standard",
        "sottotitolo": "Torso / braccio D1 serie T",
        "descrizione": "Unitree D1-T Standard: configurazione standard del braccio/torso D1-T per ricerca e integrazione. Prezzo e lead time su preventivo Abra.",
        "categoria": "MANI_BRACCI",
        "coll_file": "accessori.html",
        "coll_name": "Accessori",
        "img_key": "d1-t-standard",
        "specs": [["Variante", "D1-T Standard"], ["Tipo", "Braccio / torso"]],
    },
    {
        "sku": "D1T-FULL",
        "filename": "unitree-d1-t-full.html",
        "titolo": "Unitree D1-T Full",
        "sottotitolo": "Configurazione completa D1-T",
        "descrizione": "Unitree D1-T Full: configurazione full del sistema D1-T con accessori e compute inclusi nella variante richiesta. Preventivo dedicato.",
        "categoria": "MANI_BRACCI",
        "coll_file": "accessori.html",
        "coll_name": "Accessori",
        "img_key": "d1-t-full",
        "specs": [["Variante", "D1-T Full"], ["Tipo", "Braccio / torso completo"]],
    },
    {
        "sku": "LIDAR-L1",
        "filename": "unitree-lidar-l1.html",
        "titolo": "Unitree LiDAR L1",
        "sottotitolo": "Modulo LiDAR L1 standalone",
        "descrizione": "Unitree LiDAR L1: sensore LiDAR compatibile con quadrupedi Go2 (integrato su Go2 Pro/Enterprise). Modulo standalone disponibile su preventivo.",
        "categoria": "COMPONENTISTICA",
        "coll_file": "accessori.html",
        "coll_name": "Accessori",
        "img_key": "lidar-l1",
        "specs": [["Modello", "LiDAR L1"], ["Uso", "SLAM / navigazione Go2"]],
    },
    {
        "sku": "LIDAR-L2",
        "filename": "unitree-lidar-l2.html",
        "titolo": "Unitree LiDAR L2",
        "sottotitolo": "Modulo LiDAR L2 standalone",
        "descrizione": "Unitree LiDAR L2: sensore LiDAR avanzato per Go2 EDU e mapping 3D. Modulo standalone su preventivo Abra.",
        "categoria": "COMPONENTISTICA",
        "coll_file": "accessori.html",
        "coll_name": "Accessori",
        "img_key": "lidar-l2",
        "specs": [["Modello", "LiDAR L2"], ["Uso", "Mapping 3D / Go2 EDU"]],
    },
    {
        "sku": "DEX2-5",
        "filename": "unitree-dex2-5.html",
        "titolo": "Unitree Dex2 / Dex5",
        "sottotitolo": "Mani e gripper Dex serie 2 e 5",
        "descrizione": "Unitree Dex2 e Dex5: end-effector e mani destre/sinistre per piattaforme H2 e G1. Configurazione Dex2 o Dex5 su preventivo con compatibilità robot.",
        "categoria": "MANI_BRACCI",
        "coll_file": "accessori.html",
        "coll_name": "Accessori",
        "img_key": "dex2-5",
        "specs": [["Famiglia", "Dex2 / Dex5"], ["Compatibilità", "H2, G1 (variante)"]],
    },
    {
        "sku": "R3",
        "filename": "unitree-r3.html",
        "titolo": "Unitree R3",
        "sottotitolo": "Telecomando / accessorio R3",
        "descrizione": "Unitree R3: telecomando wireless per piattaforme Unitree (es. G1). Disponibilità e prezzo su preventivo — indica robot e firmware in fase di richiesta.",
        "categoria": "COMPONENTISTICA",
        "coll_file": "accessori.html",
        "coll_name": "Accessori",
        "img_key": "r3",
        "specs": [["Prodotto", "Telecomando R3"], ["Compatibilità", "G1 e piattaforme Unitree"]],
    },
]

CAT_LABEL = {
    "UMANOIDI": "Umanoidi & robot",
    "MANI_BRACCI": "Mani & bracci",
    "COMPONENTISTICA": "Componentistica",
}


def download_image(key: str, url: str) -> str:
    """Scarica immagine in images/prodotti/ e ritorna path relativo sito."""
    if url.startswith("images/"):
        return url
    dest = IMAGES / f"{key}.png"
    IMAGES.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            dest.write_bytes(data)
            print(f"  Scaricata {dest.name}")
        except Exception as e:
            print(f"  WARN download {key}: {e}")
            return "images/manifattura/unitree-g1-d-nobg.png"
    return f"images/prodotti/{dest.name}"


def build_page(p: dict, img_path: str) -> str:
    entry = {
        "titolo": p["titolo"],
        "sottotitolo": p["sottotitolo"],
        "descrizione": p["descrizione"],
        "specs": p["specs"],
    }
    title = p["titolo"]
    desc = p["descrizione"]
    filename = p["filename"]
    sku = p["sku"]
    coll_file = p["coll_file"]
    coll_name = p["coll_name"]
    cat = p["categoria"]
    gallery_src, og_image = gallery_path(img_path)
    metadesc = f"{title}. {desc[:120]}"

    html = TEMPLATE
    repl = {
        "%%LANG_TITLE%%": f"{title} | Abra Robotics",
        "%%METADESC%%": metadesc[:160],
        "%%FILENAME%%": filename,
        "%%COLLECTION_FILE%%": coll_file,
        "%%COLLECTION_NAME%%": coll_name,
        "%%BADGE%%": cat.replace("_", " · "),
        "%%TITLE%%": title,
        "%%SUBTITLE%%": p["sottotitolo"],
        "%%DESC%%": desc,
        "%%SKU%%": sku,
        "%%GALLERY_MAIN%%": gallery_src,
        "%%OG_IMAGE%%": og_image,
        "%%KEYSPECS%%": key_specs(entry),
        "%%SPECS_ROWS%%": spec_rows(entry),
        "%%SPECS_BLOCK%%": (
            f'        <div class="faq-item open">\n'
            f'          <button class="faq-question" type="button"><span>Dettagli prodotto</span><span class="faq-icon">+</span></button>\n'
            f'          <div class="faq-answer"><ul class="spec-table">{spec_rows(entry)}</ul></div>\n'
            f"        </div>"
        ),
        "%%EXTRA_SECTIONS%%": "",
        "%%BUY_AREA%%": buy_area(None, False, sku),
        "%%PRODUCT_SCHEMA%%": product_schema(title, desc[:200], og_image, None, filename, coll_file, coll_name),
        "%%SITE_NAV%%": render_site_nav("../"),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    return html


def update_manifest(products: list[dict], img_paths: dict[str, str]) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for p in products:
        sku = p["sku"]
        manifest[sku] = {
            "titolo": p["titolo"],
            "sottotitolo": p["sottotitolo"],
            "descrizione": p["descrizione"],
            "specs": p["specs"],
            "immagine": img_paths.get(p["img_key"], "images/manifattura/unitree-g1-d-nobg.png"),
            "categoria": p["categoria"],
            "slug": p["filename"],
            "prezzo_su_richiesta": True,
        }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def catalog_cards(products: list[dict], img_paths: dict[str, str]) -> str:
    cards = []
    for p in products:
        sku = p["sku"]
        fn = p["filename"]
        titolo = p["titolo"]
        family = product_family(sku, p["titolo"])
        cat_label = CAT_LABEL.get(p["categoria"], p["categoria"])
        img = img_paths.get(p["img_key"], "images/manifattura/unitree-g1-d-nobg.png")
        cards.append(
            f"""        <article class="cat-card" data-cat="{cat_label}" data-family="{family}" data-sku="{sku}" data-name="{titolo.lower()}">
          <a href="prodotti/{fn}" class="cat-media"><img src="{img}" alt="{titolo}" loading="lazy" onerror="this.style.display='none';this.parentElement.classList.add('no-img');"></a>
          <div class="cat-body">
            <p class="cat-family">{family}</p>
            <h3><a href="prodotti/{fn}">{titolo}</a></h3>
            <p class="cat-price">Prezzo su richiesta</p>
            <a href="prodotti/{fn}" class="btn btn-secondary btn-sm">Scheda prodotto</a>
          </div>
        </article>"""
        )
    return "\n".join(cards)


def patch_catalog(cards_html: str) -> None:
    cat_path = ROOT / "catalogo-unitree.html"
    text = cat_path.read_text(encoding="utf-8")
    marker = '    </div>\n    <p id="cat-empty"'
    if "unitree-g1-d-standard.html" in text:
        print("Catalogo già contiene G1-D — skip patch")
        return
    if marker not in text:
        raise SystemExit("Marker catalogo non trovato")
    text = text.replace(marker, cards_html + "\n" + marker, 1)
    # assicura filtro G1-D
    if 'value="G1-D"' not in text and "G1-D</option>" not in text:
        text = text.replace(
            '<option value="G1">G1</option>',
            '<option value="G1">G1</option><option value="G1-D">G1-D</option>',
            1,
        )
    cat_path.write_text(text, encoding="utf-8")


def write_g1_d_hub() -> None:
    hub = ROOT / "g1-d.html"
    if hub.exists():
        print("g1-d.html esiste già")
        return
    r1 = (ROOT / "r1-d.html").read_text(encoding="utf-8")
    # adatta da r1-d
    html = r1
    html = html.replace("R1-D", "G1-D").replace("R1-D", "G1-D")
    html = html.replace("r1-d.html", "g1-d.html")
    html = html.replace("unitree-r1-d-hero.png", "manifattura/unitree-g1-d-nobg.png")
    html = html.replace("Dual-Arm Humanoid", "G1-D Dual-Arm Platform")
    html = html.replace(
        "Unitree Dual-Arm Humanoid Robot",
        "Unitree G1-D — piattaforma dual-arm",
    )
    html = html.replace(
        "Piattaforma umanoide dual-arm di Unitree per deploy rapido",
        "Piattaforma umanoide dual-arm su colonna (Standard) o base mobile (Flagship) per acquisizione dati AI, manipolazione bimanuale e deployment industriale",
    )
    html = html.replace(
        'href="https://www.unitree.com/mobile/R1-D/"',
        'href="https://www.unitree.com/mobile/G1-D/"',
    )
    html = html.replace("unitree.com/mobile/R1-D", "unitree.com/mobile/G1-D")
    html = html.replace("unitree-r1-d.html", "unitree-g1-d-standard.html")
    html = html.replace("Scheda prodotto R1-D", "Gamma G1-D Standard")
    html = html.replace("A partire da 12.000,00 €", "Prezzo su richiesta")
    html = re.sub(
        r"<div style=\"margin-bottom:20px;.*?R1-A7-D.*?</div>",
        """<div style="margin-bottom:20px;padding:16px 20px;background:var(--gray-50);border:1px solid var(--gray-200);border-radius:8px;font-size:0.9rem;color:var(--gray-600);line-height:1.6;">
<strong>G1-D Standard vs Flagship.</strong> <strong>Standard (U1–U5)</strong> = piantana fissa. <strong>Flagship (U6–U10)</strong> = base mobile a ruote con LiDAR. Non è il G1 bipede che cammina su gambe.
<a href="prodotti/unitree-g1-d-standard.html">G1-D Standard →</a> · <a href="prodotti/unitree-g1-d-flagship.html">G1-D Flagship →</a>
</div>""",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<h2 style=\"font-size:1\.35rem.*?</table>\s*</div>",
        """<h2 style="font-size:1.35rem;margin-bottom:12px;">Gamma configurazioni G1-D</h2>
<p style="color:var(--gray-500);font-size:0.88rem;margin-bottom:20px;">Standard U1–U5 (piantana) e Flagship U6–U10 (mobile). Dettaglio varianti su preventivo Abra.</p>
<div class="robot-grid">
<article class="robot-card">
<div class="robot-media"><img src="images/prodotti/g1-d-standard.png" alt="Unitree G1-D Standard" loading="lazy"/></div>
<div class="robot-body"><h3>G1-D Standard</h3><p class="robot-subtitle">U1–U5 · piantana fissa</p>
<div class="robot-card-cta"><span class="card-price">Su richiesta</span><a class="btn btn-primary btn-sm" href="prodotti/unitree-g1-d-standard.html">Scheda →</a></div></div></article>
<article class="robot-card">
<div class="robot-media"><img src="images/prodotti/g1-d-flagship.png" alt="Unitree G1-D Flagship" loading="lazy"/></div>
<div class="robot-body"><h3>G1-D Flagship</h3><p class="robot-subtitle">U6–U10 · base mobile</p>
<div class="robot-card-cta"><span class="card-price">Su richiesta</span><a class="btn btn-primary btn-sm" href="prodotti/unitree-g1-d-flagship.html">Scheda →</a></div></div></article>
</div>""",
        html,
        count=1,
        flags=re.DOTALL,
    )
    hub.write_text(html, encoding="utf-8")
    print(f"Scritto {hub}")


def main() -> None:
    img_paths: dict[str, str] = {}
    for key, url in IMAGE_URLS.items():
        img_paths[key] = download_image(key, url)

    for p in PRODUCTS:
        path = PRODOTTI / p["filename"]
        img = img_paths.get(p["img_key"], "images/manifattura/unitree-g1-d-nobg.png")
        path.write_text(build_page(p, img), encoding="utf-8")
        print(f"Pagina: {path.name}")

    update_manifest(PRODUCTS, img_paths)
    cards = catalog_cards(PRODUCTS, img_paths)
    patch_catalog(cards)
    write_g1_d_hub()
    print("Fatto — prodotti su preventivo generati.")


if __name__ == "__main__":
    main()
