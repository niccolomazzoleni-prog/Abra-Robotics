#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera schede prodotto, catalogo e listino da CSV prezzi + catalogo-manifest.json."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from layout_pubblico import PUBLIC_NOTICE, SITE_FOOTER, SITE_NAV  # noqa: E402
from site_nav import render_site_nav  # noqa: E402

CSV_PATH = ROOT / "listini" / "interno" / "listino-master.csv"
MANIFEST_PATH = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"
TEMPLATE = (ROOT / "prodotti" / "_template-compact.html").read_text(encoding="utf-8")
PRODOTTI = ROOT / "prodotti"
sys.path.insert(0, str(ROOT / "prodotti"))
from _site import SITE  # noqa: E402

CAT_LABEL = {
    "UMANOIDI": "Umanoidi & robot",
    "MANI_BRACCI": "Mani & bracci",
    "COMPONENTISTICA": "Componentistica",
}

# Pagine esistenti — non sovrascrivere (hanno contenuto ricco)
SKIP_OVERWRITE = {
    "unitree-g1.html", "unitree-g1-edu-standard.html", "unitree-g1-edu-plus.html",
    "unitree-g1-edu-ultimate-a.html", "unitree-g1-edu-ultimate-b.html",
    "unitree-g1-edu-ultimate-c.html", "unitree-g1-edu-ultimate-d.html",
    "unitree-g1-edu-ultimate-e.html", "unitree-g1-edu-ultimate-f.html",
    "unitree-g1-comp.html", "unitree-r1-edu.html", "unitree-go2-pro.html",
    "unitree-go2-edu.html", "unitree-go2-edu-plus.html", "unitree-go2-enterprise-u2.html",
    "unitree-a2.html", "unitree-a2-pro.html", "unitree-b2.html", "unitree-h2.html",
}

def product_family(sku: str, nome: str) -> str:
    s = sku.upper()
    n = nome.upper()
    if s.startswith("G1") or " G1" in n:
        return "G1"
    if s == "R1-D" or "R1-D" in n or "DUAL-ARM" in n:
        return "R1-D"
    if s.startswith("R1") or " R1" in n:
        return "R1"
    if s.startswith("H2") or " H2" in n:
        return "H2"
    if s.startswith("GO2W") or "GO2W" in n:
        return "Go2W"
    if s.startswith("GO2") or "GO2" in n:
        return "Go2"
    if s.startswith("B2W") or "B2W" in n or "B2-W" in n:
        return "B2W"
    if s.startswith("B2") or " B2" in n:
        return "B2"
    if s.startswith("A2W") or "A2-W" in n:
        return "A2W"
    if s.startswith("A2") or " A2" in n:
        return "A2"
    if s.startswith("H2-") or s.startswith("HAND") or s.startswith("ARM") or "GRIPPER" in s or "DEX" in n:
        return "Accessori"
    return "Accessori"


PRICE_FROM_SKUS = {"R1-D"}

FILENAME_MAP: dict[str, str] = {
    "H2-EDU": "unitree-h2.html",
    "H2-AIR": "unitree-h2-air.html",
    "R1-D": "unitree-r1-d.html",
    "G1-AIR": "unitree-g1.html",
    "G1-U1": "unitree-g1-edu-standard.html",
    "G1-U2": "unitree-g1-edu-plus.html",
    "G1-U3": "unitree-g1-edu-ultimate-a.html",
    "G1-U4": "unitree-g1-edu-ultimate-b.html",
    "G1-U5": "unitree-g1-edu-ultimate-c.html",
    "G1-U6": "unitree-g1-edu-ultimate-d.html",
    "G1-U7": "unitree-g1-edu-ultimate-e.html",
    "G1-COMP": "unitree-g1-comp.html",
    "R1-U1": "unitree-r1-edu.html",
    "GO2-PRO": "unitree-go2-pro.html",
    "GO2-EDU-STD": "unitree-go2-edu.html",
    "GO2-EDU-SMART": "unitree-go2-edu-plus.html",
    "GO2-EDU-ULT": "unitree-go2-enterprise-u2.html",
    "A2-STD": "unitree-a2.html",
    "A2-PRO": "unitree-a2-pro.html",
    "B2": "unitree-b2.html",
    "B2-LIDAR": "unitree-b2-lidar.html",
}

# Dopo genera_prezzi: B2 su unitree-b2.html, B2-LIDAR su unitree-b2-lidar.html

COLLECTION = {
    "UMANOIDI": ("umanoidi.html", "Umanoidi"),
    "MANI_BRACCI": ("accessori.html", "Accessori"),
    "COMPONENTISTICA": ("accessori.html", "Accessori"),
}

def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_catalogo_manifest.py")], check=True, cwd=str(ROOT))
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def manifest_entry(sku: str, manifest: dict, row: dict) -> dict:
    if sku in manifest:
        return manifest[sku]
    nome = row.get("nome_prodotto", sku)
    return {
        "titolo": nome if nome.startswith("Unitree") else f"Unitree {nome}",
        "sottotitolo": nome,
        "descrizione": f"{nome}: prodotto Unitree distribuito in Italia da Abra Robotics.",
        "specs": [["Prodotto", nome]],
        "immagine": "images/g1-hero.png",
        "categoria": row.get("categoria", ""),
        "slug": slug_file(sku),
    }


def slug_file(sku: str) -> str:
    if sku in FILENAME_MAP:
        return FILENAME_MAP[sku]
    return "unitree-" + sku.lower().replace("_", "-") + ".html"


def fmt_eur(v: float) -> str:
    s = f"{v:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def parse_price(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw or raw in ("—", "-"):
        return None
    return float(raw.replace(",", "."))


def buy_area(price: float | None, has_price: bool, sku: str = "") -> str:
    perks = """            <ul class="buy-box-perks">
              <li><span class="bp-ico">✓</span> Spedizione e dazio doganale inclusi</li>
              <li><span class="bp-ico">✓</span> Distributore ufficiale Unitree</li>
              <li><span class="bp-ico">✓</span> Consegna stimata 2–4 settimane</li>
            </ul>"""
    pay = """            <div class="buy-box-pay">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Pagamento sicuro · Stripe
              <span class="buy-box-cards"><span>VISA</span><span>MC</span><span>AMEX</span></span>
            </div>"""
    note = '<p class="buy-box-note">Prezzo indicativo — preventivo aggiornato su richiesta.</p>'
    if not has_price or price is None:
        return f"""          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price"><span class="buy-box-amount" style="font-size:1.5rem;">Prezzo su richiesta</span></div>
            </div>
{perks}
            <div class="buy-box-cta"><a href="#form" class="btn btn-primary">Richiedi preventivo</a></div>
          </div>"""
    vis = fmt_eur(price)
    amount = f"A partire da {vis} €" if sku in PRICE_FROM_SKUS else f"{vis} €"
    sub = "Prezzo indicativo · IVA esclusa" if sku in PRICE_FROM_SKUS else "Prezzo chiavi in mano · IVA esclusa"
    return f"""          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price">
                <span class="buy-box-amount">{amount}</span>
                <span class="buy-box-sub">{sub}</span>
              </div>
              <span class="buy-box-stock"><span class="dot"></span> Disponibile</span>
            </div>
{perks}
            <div class="buy-box-cta">
              <a href="#form" class="btn btn-primary buy-btn" data-buy-pending="1">Acquista ora</a>
              <a href="#form" class="btn btn-secondary">Richiedi preventivo</a>
            </div>
{pay}
{note}
          </div>"""


def product_schema(
    name: str,
    desc: str,
    img: str,
    price: float | None,
    filename: str,
    coll_file: str = "catalogo-unitree.html",
    coll_name: str = "Catalogo",
) -> str:
    img_url = img if img.startswith("http") else f"{SITE}/{img}"
    nm, ds = name.replace('"', '\\"'), desc.replace('"', '\\"')
    sku = filename.replace(".html", "")
    canon = f"{SITE}/prodotti/{filename}"
    offer = ""
    if price is not None:
        offer = f''',
  "offers": {{"@type": "Offer", "priceCurrency": "EUR", "price": "{price:.2f}",
    "priceValidUntil": "2026-12-31",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock",
    "url": "{canon}",
    "seller": {{"@type": "Organization", "name": "Abra Robotics", "url": "{SITE}"}}}}'''
    breadcrumb = f"""  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},
    {{"@type": "ListItem", "position": 2, "name": "{coll_name}", "item": "{SITE}/{coll_file}"}},
    {{"@type": "ListItem", "position": 3, "name": "{nm}", "item": "{canon}"}}
  ]}}
  </script>"""
    return f"""  <script type="application/ld+json">
  {{"@context": "https://schema.org/", "@type": "Product", "name": "{nm}",
  "sku": "{sku}",
  "image": ["{img_url}"], "description": "{ds}",
  "itemCondition": "https://schema.org/NewCondition",
  "brand": {{"@type": "Brand", "name": "Unitree"}}{offer}}}
  </script>
{breadcrumb}"""


def key_specs(entry: dict) -> str:
    specs = entry.get("specs") or []
    html = []
    for label, val in specs[:6]:
        html.append(
            f'            <div class="key-spec"><span class="key-spec-value">{val}</span>'
            f'<span class="key-spec-label">{label}</span></div>'
        )
    return "\n".join(html) if html else '            <div class="key-spec"><span class="key-spec-value">—</span><span class="key-spec-label">Scheda tecnica</span></div>'


def spec_rows(entry: dict) -> str:
    specs = entry.get("specs") or []
    return "\n".join(f"<li><span>{k}</span><span>{v}</span></li>" for k, v in specs)


def gallery_path(img: str) -> tuple[str, str]:
    rel = img or "images/g1-hero.png"
    if rel.startswith("prodotti/"):
        inner = rel[len("prodotti/"):]
        return inner, rel
    if rel.startswith("images/"):
        return f"../{rel}", rel
    return rel, f"prodotti/{rel}" if not rel.startswith("http") else rel


def generate_page(row: dict, manifest: dict) -> str | None:
    sku = row["sku"]
    filename = slug_file(sku)
    path = PRODOTTI / filename
    if path.name in SKIP_OVERWRITE and path.exists():
        return None

    entry = manifest_entry(sku, manifest, row)
    cat = row["categoria"]
    coll_file, coll_name = COLLECTION.get(cat, ("catalogo-unitree.html", "Catalogo"))
    title = entry["titolo"]
    price = parse_price(row.get("prezzo_enduser_eur", ""))
    pub = row.get("pubblicabile") == "true"
    gallery_src, og_image = gallery_path(entry.get("immagine", ""))
    desc = entry.get("descrizione", "")
    metadesc = f"{title}: {desc[:120]}…" if len(desc) > 120 else f"{title}. {desc}"
    if price and pub:
        price_txt = f"a partire da {fmt_eur(price)} €" if sku in PRICE_FROM_SKUS else f"da {fmt_eur(price)} €"
        metadesc = f"{title} {price_txt}. {entry.get('sottotitolo', '')}"

    html = TEMPLATE
    repl = {
        "%%LANG_TITLE%%": f"{title} | Abra Robotics",
        "%%METADESC%%": metadesc[:160],
        "%%FILENAME%%": filename,
        "%%COLLECTION_FILE%%": coll_file,
        "%%COLLECTION_NAME%%": coll_name,
        "%%BADGE%%": cat.replace("_", " · "),
        "%%TITLE%%": title,
        "%%SUBTITLE%%": entry.get("sottotitolo", ""),
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
        "%%BUY_AREA%%": buy_area(price if pub else None, pub and price is not None, sku),
        "%%PRODUCT_SCHEMA%%": product_schema(
            title, desc[:200], og_image, price if pub else None, filename, coll_file, coll_name
        ),
        "%%SITE_NAV%%": render_site_nav("../"),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    path.write_text(html, encoding="utf-8")
    return filename


def read_csv() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def update_csv_pages(rows: list[dict]) -> None:
    for row in rows:
        fn = slug_file(row["sku"])
        path = f"prodotti/{fn}"
        price = parse_price(row.get("prezzo_enduser_eur", ""))
        pub = row.get("pubblicabile") == "true"
        if pub and price and (PRODOTTI / fn).exists():
            row["pagina_sito"] = path
            row["stato_sito"] = "pubblicato"
        elif (PRODOTTI / fn).exists():
            row["pagina_sito"] = path
            row["stato_sito"] = "presente"
    fields = list(rows[0].keys())
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter=";")
        w.writeheader()
        w.writerows(rows)


def _stripe_pub_key() -> str:
    """Legge pk da .env o da stripe-config.js esistente (non sovrascrive live con test)."""
    import os
    import re
    from pathlib import Path

    env_pk = (os.environ.get("STRIPE_PUBLISHABLE_KEY") or "").strip()
    if env_pk:
        return env_pk
    cfg = PRODOTTI / "stripe-config.js"
    if cfg.is_file():
        m = re.search(r'STRIPE_PUBLISHABLE_KEY\s*=\s*"([^"]+)"', cfg.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return (
        "pk_test_51TfGsx4sActfFZskv4KaRe70MlFYfSXz7pziwpQdY832en8IfMIqALSs1efCtwiGntjHG0Xr1CLemyDZQUW7lgyP003xdWD4si"
    )


def regenerate_stripe_config(filenames: list[str]) -> None:
    cfg_path = PRODOTTI / "stripe-config.js"
    existing_links: dict[str, str] = {}
    if cfg_path.is_file():
        import re

        for m in re.finditer(r'"([^"]+\.html)":\s*"([^"]*)"', cfg_path.read_text(encoding="utf-8")):
            existing_links[m.group(1)] = m.group(2)
    lines = [
        "/* Stripe — Payment Link per ogni scheda prodotto.",
        "   Valore vuoto = bottone Acquista rimanda a richiesta preventivo finche non configuri Stripe. */",
        f'window.STRIPE_PUBLISHABLE_KEY = "{_stripe_pub_key()}";',
        "window.STRIPE_PAYMENT_LINKS = {",
    ]
    for fn in sorted(set(filenames)):
        if fn.endswith(".html") and not fn.startswith("_"):
            url = existing_links.get(fn, "")
            lines.append(f'  "{fn}": "{url}",')
    lines.append("};")
    (PRODOTTI / "stripe-config.js").write_text("\n".join(lines) + "\n", encoding="utf-8")


def regenerate_catalogo_html(rows: list[dict], manifest: dict) -> None:
    """Pagina catalogo pubblico con immagini, filtri e navbar completa."""
    pub = [r for r in rows if r["pubblicabile"] == "true" and parse_price(r.get("prezzo_enduser_eur", ""))]

    cards = []
    families: set[str] = set()
    for r in sorted(pub, key=lambda x: x["nome_prodotto"]):
        sku = r["sku"]
        entry = manifest_entry(sku, manifest, r)
        fn = slug_file(sku)
        price = parse_price(r["prezzo_enduser_eur"])
        img = entry.get("immagine", "images/g1-hero.png")
        titolo = entry.get("titolo", r["nome_prodotto"])
        cat_key = r["categoria"]
        cat_label = CAT_LABEL.get(cat_key, cat_key)
        family = product_family(sku, r["nome_prodotto"])
        families.add(family)
        cards.append(f"""        <article class="cat-card" data-cat="{cat_label}" data-family="{family}" data-sku="{sku}" data-name="{titolo.lower()}">
          <a href="prodotti/{fn}" class="cat-media"><img src="{img}" alt="{titolo}" loading="lazy" onerror="this.style.display='none';this.parentElement.classList.add('no-img');"></a>
          <div class="cat-body">
            <p class="cat-family">{family}</p>
            <h3><a href="prodotti/{fn}">{titolo}</a></h3>
            <p class="cat-price">{"A partire da " if sku in PRICE_FROM_SKUS else ""}{fmt_eur(price)} €</p>
            <a href="prodotti/{fn}" class="btn btn-secondary btn-sm">Scheda prodotto</a>
          </div>
        </article>""")
    family_opts = "".join(f'<option value="{f}">{f}</option>' for f in sorted(families))
    cat_opts = "".join(f'<option value="{v}">{v}</option>' for v in CAT_LABEL.values())

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catalogo Unitree — Tutti i prodotti e prezzi | Abra Robotics</title>
  <meta name="description" content="Catalogo completo Unitree con prezzi End-User pubblici: umanoidi, quadrupedi, mani, batterie e accessori. Distributore ufficiale Italia.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/catalogo-unitree.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Catalogo Unitree — Abra Robotics">
  <meta property="og:description" content="{len(pub)} prodotti Unitree con prezzi End-User pubblici in Italia.">
  <meta property="og:url" content="{SITE}/catalogo-unitree.html">
  <meta property="og:image" content="{SITE}/images/g1-hero.png">
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <style>
    .cat-hero {{ padding: calc(40px + 72px + 48px) 48px 40px; border-bottom: 1px solid var(--gray-200); }}
    .cat-hero h1 {{ font-size: clamp(2rem,4vw,3rem); margin: 12px 0; }}
    .cat-body-page {{ padding: 48px; }}
    .cat-group {{ margin-bottom: 56px; }}
    .cat-group h2 {{ font-size: 1.4rem; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--gray-200); }}
    .cat-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; }}
    .cat-card {{ background: rgba(255,255,255,0.75); backdrop-filter: blur(10px); border: 1px solid var(--gray-200); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; transition: transform .3s ease, box-shadow .3s ease; }}
    .cat-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.08); }}
    .cat-media {{ aspect-ratio: 1/1; display: block; background: linear-gradient(135deg, var(--gray-50), var(--gray-100)); border-bottom: 1px solid var(--gray-200); overflow: hidden; }}
    .cat-media img {{ width: 100%; height: 100%; object-fit: contain; padding: 16px; }}
    .cat-body {{ padding: 18px; display: flex; flex-direction: column; flex: 1; gap: 8px; }}
    .cat-card h3 {{ font-size: 0.95rem; margin: 0; }}
    .cat-card h3 a {{ color: var(--black); text-decoration: none; font-weight: 700; }}
    .cat-price {{ font-size: 1.1rem; font-weight: 900; margin: 0; }}
    .cat-family {{ font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gray-400); margin: 0; }}
    .cat-toolbar {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 28px; }}
    .cat-toolbar input, .cat-toolbar select {{
      padding: 10px 14px; border: 1px solid var(--gray-200); border-radius: 8px;
      font-family: inherit; background: var(--white);
    }}
    .cat-toolbar input {{ flex: 1; min-width: 200px; }}
    .cat-card.hidden {{ display: none !important; }}
    @media (max-width:768px) {{ .cat-hero, .cat-body-page {{ padding-left: 20px; padding-right: 20px; }} }}
  </style>
</head>
<body>
{SITE_NAV}
  <header class="cat-hero">
    <p class="label">Catalogo pubblico End-User</p>
    <h1>Tutti i prodotti Unitree</h1>
    <p style="color:var(--gray-600);max-width:640px;">Listino pubblico End-User — IVA esclusa, spedizione e dazio inclusi. {len(pub)} prodotti con scheda e prezzo trasparente.</p>
{PUBLIC_NOTICE}
  </header>
  <main class="cat-body-page">
    <div class="cat-toolbar">
      <input type="search" id="cat-search" placeholder="Cerca prodotto o SKU…" aria-label="Cerca">
      <select id="cat-filter" aria-label="Categoria"><option value="">Tutte le categorie</option>{cat_opts}</select>
      <select id="family-filter" aria-label="Famiglia"><option value="">Tutte le famiglie</option>{family_opts}</select>
    </div>
    <div class="cat-grid" id="cat-grid">
{chr(10).join(cards)}
    </div>
    <p id="cat-empty" style="display:none;color:var(--gray-500);margin-top:24px;">Nessun prodotto corrisponde ai filtri.</p>
  </main>
{SITE_FOOTER}
  <script>
    function filterCatalog() {{
      const q = document.getElementById('cat-search').value.toLowerCase();
      const cat = document.getElementById('cat-filter').value;
      const fam = document.getElementById('family-filter').value;
      let visible = 0;
      document.querySelectorAll('.cat-card').forEach(card => {{
        const ok = (!cat || card.dataset.cat === cat)
          && (!fam || card.dataset.family === fam)
          && (!q || card.dataset.name.includes(q) || card.dataset.sku.toLowerCase().includes(q));
        card.classList.toggle('hidden', !ok);
        if (ok) visible++;
      }});
      document.getElementById('cat-empty').style.display = visible ? 'none' : 'block';
    }}
    document.getElementById('cat-search').addEventListener('input', filterCatalog);
    document.getElementById('cat-filter').addEventListener('change', filterCatalog);
    document.getElementById('family-filter').addEventListener('change', filterCatalog);
  </script>
  <script src="scripts/image-runtime.js"></script>
  <script src="script.js"></script>
</body>
</html>"""
    (ROOT / "catalogo-unitree.html").write_text(html, encoding="utf-8")


def regenerate_listino_html() -> None:
    """Pagina listino tabella con thumbnail e navbar corretta."""
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Listino pubblico End-User Unitree | Abra Robotics</title>
  <meta name="description" content="Listino prezzi End-User Unitree distribuiti da Abra Robotics in Italia. Valori indicativi, IVA esclusa, spedizione e dazio inclusi.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/listino-unitree.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Listino End-User Unitree — Abra Robotics">
  <meta property="og:url" content="{SITE}/listino-unitree.html">
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <style>
    .listino-hero {{ padding: calc(40px + 72px + 60px) 48px 48px; border-bottom: 1px solid var(--gray-200); }}
    .listino-hero h1 {{ font-size: clamp(2rem, 4vw, 3rem); letter-spacing: -0.03em; margin: 12px 0 16px; }}
    .listino-hero p {{ color: var(--gray-600); max-width: 720px; line-height: 1.6; }}
    .listino-body {{ padding: 48px; }}
    .listino-toolbar {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }}
    .listino-toolbar input, .listino-toolbar select {{
      padding: 10px 14px; border: 1px solid var(--gray-200); border-radius: 8px;
      font-family: inherit; background: var(--white);
    }}
    .listino-toolbar input {{ flex: 1; min-width: 200px; }}
    .listino-table-wrap {{
      background: rgba(255,255,255,0.7); backdrop-filter: blur(12px);
      border: 1px solid var(--gray-200); border-radius: var(--radius); overflow-x: auto;
    }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 14px 16px; text-align: left; border-bottom: 1px solid var(--gray-100); vertical-align: middle; }}
    th {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--gray-500); }}
    .thumb-col {{ width: 56px; }}
    .listino-thumb {{ width: 48px; height: 48px; object-fit: contain; border-radius: 6px; background: var(--gray-50); }}
    .price-col {{ font-weight: 800; white-space: nowrap; }}
    .listino-note {{ margin-top: 24px; font-size: 0.85rem; color: var(--gray-500); max-width: 720px; line-height: 1.6; }}
    .prod-link {{ color: var(--black); font-weight: 600; text-decoration: none; }}
    .prod-link:hover {{ text-decoration: underline; }}
    @media (max-width: 768px) {{ .listino-hero, .listino-body {{ padding-left: 20px; padding-right: 20px; }} }}
  </style>
</head>
<body>
{SITE_NAV}
  <header class="listino-hero">
    <p class="label">Listino pubblico End-User</p>
    <h1>Prezzi End-User Unitree</h1>
    <p>Valori indicativi per il mercato italiano. IVA esclusa. Spedizione e dazio doganale (3,7%) inclusi. Ogni ordine richiede conferma con preventivo aggiornato.</p>
{PUBLIC_NOTICE}
  </header>

  <main class="listino-body">
    <div class="listino-toolbar">
      <input type="search" id="search" placeholder="Cerca prodotto…" aria-label="Cerca">
      <select id="cat-filter" aria-label="Categoria">
        <option value="">Tutte le categorie</option>
      </select>
    </div>

    <div class="listino-table-wrap">
      <table>
        <thead>
          <tr><th class="thumb-col"></th><th>Prodotto</th><th>Categoria</th><th>Prezzo End-User</th></tr>
        </thead>
        <tbody id="rows"><tr><td colspan="4">Caricamento…</td></tr></tbody>
      </table>
    </div>

    <p class="listino-note">I prezzi sono soggetti a variazione del cambio EUR/USD. Non include prezzi distributore (Gold). Per uso interno: <code>admin/listini.html</code> (non indicizzato). Per configurazioni EDU avanzate, <a href="index.html#cta-finale">richiedi un preventivo personalizzato</a>.</p>
  </main>
{SITE_FOOTER}
  <script>
    let items = [];
    const CAT_LABEL = {{ UMANOIDI: "Umanoidi & robot", MANI_BRACCI: "Mani & bracci", COMPONENTISTICA: "Componentistica" }};

    function fmt(n) {{
      return n.toLocaleString('it-IT', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }}

    function render() {{
      const q = document.getElementById('search').value.toLowerCase();
      const cat = document.getElementById('cat-filter').value;
      const filtered = items.filter(i => {{
        if (cat && i.cat !== cat) return false;
        if (q && !i.nome.toLowerCase().includes(q) && !i.sku.toLowerCase().includes(q)) return false;
        return true;
      }});
      document.getElementById('rows').innerHTML = filtered.length
        ? filtered.map(i => `<tr>
            <td class="thumb-col">${{i.img ? `<img class="listino-thumb" src="${{i.img}}" alt="" loading="lazy">` : ''}}</td>
            <td><a class="prod-link" href="prodotti/${{i.slug}}">${{i.nome}}</a></td>
            <td>${{i.catLabel}}</td>
            <td class="price-col">${{i.prezzoDa ? 'da ' : ''}}€ ${{fmt(i.prezzo)}}</td>
          </tr>`).join('')
        : '<tr><td colspan="4">Nessun risultato</td></tr>';
    }}

    fetch('listini/pubblico/end-user.json')
      .then(r => r.json())
      .then(json => {{
        const cats = new Set();
        items = Object.entries(json).map(([sku, v]) => {{
          const catKey = v.categoria || '';
          const catLabel = CAT_LABEL[catKey] || catKey || '—';
          cats.add(catLabel);
          return {{
            sku, nome: v.nome, prezzo: v.prezzo_eur, prezzoDa: !!v.prezzo_da, slug: v.slug || '',
            img: v.immagine || '', cat: catLabel, catLabel
          }};
        }}).sort((a, b) => a.nome.localeCompare(b.nome, 'it'));

        const sel = document.getElementById('cat-filter');
        [...cats].sort().forEach(c => {{
          const o = document.createElement('option');
          o.value = c; o.textContent = c;
          sel.appendChild(o);
        }});
        render();
      }});

    document.getElementById('search').addEventListener('input', render);
    document.getElementById('cat-filter').addEventListener('change', render);
  </script>
  <script src="script.js"></script>
</body>
</html>"""
    (ROOT / "listino-unitree.html").write_text(html, encoding="utf-8")


def patch_b2_price(rows: list[dict]) -> None:
    """unitree-b2.html -> prezzo B2 base; nuova pagina b2-lidar."""
    by_sku = {r["sku"]: r for r in rows}
    b2 = by_sku.get("B2")
    if not b2:
        return
    path = PRODOTTI / "unitree-b2.html"
    if not path.exists():
        return
    price = parse_price(b2["prezzo_enduser_eur"])
    if not price:
        return
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'(<span class="buy-box-amount">)[^<]*(</span>)',
        rf"\g<1>{fmt_eur(price)} €\g<2>",
        text,
        count=1,
    )
    text = re.sub(r'("price":\s*")[^"]*(")', rf'\g<1>{price:.2f}\g<2>', text, count=1)
    path.write_text(text, encoding="utf-8")
    print(f"  OK unitree-b2.html -> B2 base {fmt_eur(price)} EUR")


def main() -> None:
    manifest = load_manifest()
    rows = read_csv()
    created: list[str] = []
    all_files: list[str] = []

    print("Generazione schede prodotto (manifest + prezzi CSV)...")
    for row in rows:
        fn = slug_file(row["sku"])
        all_files.append(fn)
        if row["pubblicabile"] != "true":
            continue
        if not parse_price(row.get("prezzo_enduser_eur", "")):
            continue
        result = generate_page(row, manifest)
        if result:
            created.append(result)
            print(f"  OK {result} ({row['sku']})")

    patch_b2_price(rows)
    update_csv_pages(rows)
    regenerate_stripe_config(all_files)
    regenerate_catalogo_html(rows, manifest)
    regenerate_listino_html()

    subprocess.run([sys.executable, str(ROOT / "scripts" / "genera_prezzi.py")], check=True, cwd=str(ROOT))

    print(f"\nRigenerate {len(created)} schede compatte")
    print("Catalogo: catalogo-unitree.html")
    print("Listino: listino-unitree.html")
    print(f"Stripe: prodotti/stripe-config.js ({len(set(all_files))} slug)")


if __name__ == "__main__":
    main()
