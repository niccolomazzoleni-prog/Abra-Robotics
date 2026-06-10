"""Generate AMR HTML: 6 featured on manifattura-logistica, full catalog on catalogo-amr."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = "images/manifattura/amr"

MIR250_SPECS = [("Payload", "250 kg"), ("Velocità max", "2,0 m/s"), ("Autonomia", "~13 h"), ("Protezione", "IP52")]
MIR250_ROWS = [("Dimensioni (L×P×H)", "800 × 580 × 300 mm"), ("Peso", "78 kg"), ("Navigazione", "SLAM laser 2D/3D"), ("Corridoio min.", "800 mm")]
MIR600_SPECS = [("Payload", "600 kg"), ("Velocità max", "2,0 m/s"), ("Autonomia", "~8 h"), ("Protezione", "IP52")]
MIR600_ROWS = [("Dimensioni (L×P×H)", "1.350 × 920 × 320 mm"), ("Peso", "238 kg"), ("Navigazione", "SLAM laser"), ("Corridoio min.", "1.400 mm")]
MIR1350_SPECS = [("Payload", "1.350 kg"), ("Velocità max", "1,2 m/s"), ("Autonomia", "~6–10 h"), ("Protezione", "IP52")]
MIR1350_ROWS = [("Dimensioni (L×P×H)", "1.350 × 920 × 320 mm"), ("Peso", "350 kg"), ("Navigazione", "SLAM laser"), ("Flotta", "MiR Fleet")]

# slug -> immagine corretta per quel modello; video solo sulla base MiR (luci animate ufficiali)
DEFAULT_ASSETS = {
    "juno-plus": {"file": "juno-plus.webp"},
    "juno-lift": {"file": "juno-lift.webp"},
    "l300": {"file": "youibot-l300-gallery.png"},
    "mir250-base": {"file": "mir250-base.png", "video": "mir250-hero.mp4"},
    "mir250-shelf": {"file": "mir250-shelf.png"},
    "mir250-hook": {"file": "mir250-hook.png"},
    "mir600-base": {"file": "mir600-base.png", "video": "mir600-hero.mp4"},
    "mir600-pallet": {"file": "mir600-hero.png"},
    "mir600-shelf": {"file": "mir600-hero.png"},
    "mir1350-base": {"file": "mir1350-hero.png", "video": "mir1350-hero.mp4"},
    "mir1350-pallet": {"file": "mir1350-hero.png"},
    "mir1200": {"file": "mir1200-palletjack.png"},
    "l1000": {"file": "youibot-l1000.png"},
    "mav-1500": {"file": "neura-mav-1500.webp"},
    "xp15": {"file": "ep-xp15.png"},
    "mav-lara": {"file": "neura-mav-1500-side.webp"},
}

CATALOG = [
    ("juno-plus", "leggeri", "Pesi leggeri · Piattaforma",
     "AutoXing Juno Plus", "AMR leggero · 200 kg · indoor/outdoor",
     "Piattaforma compatta per cassette e carrelli leggeri. SLAM, follow-me, oltre 8 ore di autonomia.",
     [("Payload", "200 kg"), ("Velocità max", "1,0 m/s"), ("Autonomia", "> 8 h"), ("Ambiente", "Indoor / outdoor")],
     [("Dimensioni", "900 × 600 × 1.240 mm"), ("Navigazione", "SLAM 2D"), ("Funzioni", "Follow-me"), ("Setup", "~1 h")],
     "Trasporto tote e semilavorati tra postazioni vicine.", 16999),
    ("juno-lift", "leggeri", "Pesi leggeri · Lift",
     "AutoXing Juno Lift", "AMR con lift · 200 kg",
     "Come Juno Plus con modulo lift integrato: carica e scarica fino a 200 kg senza operatore.",
     [("Payload", "200 kg"), ("Lift", "Integrato"), ("Autonomia", "10 h"), ("Ambiente", "Indoor / outdoor")],
     [("Dimensioni", "710 × 500 × 1.240 mm"), ("Navigazione", "SLAM 2D"), ("Funzioni", "Follow-me + lift"), ("Setup", "~1 h")],
     "Kanban automatico tra magazzino e linea con carrelli standard.", 19999),
    ("l300", "leggeri", "Pesi leggeri · Latent",
     "Youibot L300", "Latent AMR · 300 kg · lift 60 mm",
     "Va sotto carrelli e scaffali, solleva e trasporta in autonomia. Laser SLAM ±5 mm, YOUIFLEET, CE.",
     [("Payload", "300 kg"), ("Lift", "60 mm · 360°"), ("Autonomia", "8 h"), ("Precisione", "±5 mm")],
     [("Dimensioni", "800 × 619 × 330 mm"), ("Peso", "180 kg"), ("Velocità max", "1,5 m/s"), ("Navigazione", "Laser SLAM")],
     "Logistica interna in corridoi stretti, rifornimento bordo linea.", 24990),
    ("mir250-base", "mir", "MiR · Leggero-medio",
     "MiR250 Base", "Mobile Industrial Robots · 250 kg · IP52",
     "Piattaforma base senza top module. Massima flessibilità per integrazioni custom e moduli UR+.",
     MIR250_SPECS, MIR250_ROWS,
     "Trasporto materiali in manifattura con ecosistema MiR Fleet.", 44284),
    ("mir250-shelf", "mir", "MiR · Leggero-medio",
     "MiR250 Shelf Carrier", "Mobile Industrial Robots · 250 kg · IP52",
     "Portascarrelli integrato per shelf-to-person e trasporto carrelli tra reparti.",
     MIR250_SPECS, MIR250_ROWS,
     "Trasporto materiali in manifattura con integrazione MiR Fleet.", 53012),
    ("mir250-hook", "mir", "MiR · Leggero-medio",
     "MiR250 Hook", "Mobile Industrial Robots · 250 kg · IP52",
     "Gancio trainante per carrelli e traini manuali — automazione senza modificare i carrelli esistenti.",
     MIR250_SPECS, MIR250_ROWS,
     "Trasporto materiali in manifattura con ecosistema MiR Fleet.", 65428),
    ("mir600-base", "mir", "MiR · Medio",
     "MiR600 Base", "Mobile Industrial Robots · 600 kg · IP52",
     "Piattaforma 600 kg per pallet e carichi medi in logistica interna.",
     MIR600_SPECS, MIR600_ROWS,
     "Trasporto pallet e materiali tra produzione e magazzino.", 67324),
    ("mir600-pallet", "mir", "MiR · Medio",
     "MiR600 EU Pallet Lift", "Mobile Industrial Robots · 600 kg · IP52",
     "Sollevamento pallet EUR 800×1200 mm — sostituisce movimenti muletto su percorsi fissi.",
     MIR600_SPECS, MIR600_ROWS,
     "Trasporto pallet e materiali tra produzione e magazzino.", 72812),
    ("mir600-shelf", "mir", "MiR · Medio",
     "MiR600 Shelf Lift", "Mobile Industrial Robots · 600 kg · IP52",
     "Modulo shelf lift sottoscocca per scaffali e carrelli fino a 600 kg.",
     MIR600_SPECS, MIR600_ROWS,
     "Trasporto pallet e materiali tra produzione e magazzino.", 76216),
    ("mir1350-base", "mir", "MiR · Pesante",
     "MiR1350 Base", "Mobile Industrial Robots · 1.350 kg",
     "AMR più potente della gamma MiR per pallet completi e carichi industriali pesanti.",
     MIR1350_SPECS, MIR1350_ROWS,
     "Movimentazione pallet in magazzino ad alto volume.", 85040),
    ("mir1350-pallet", "mir", "MiR · Pesante",
     "MiR1350 EU Pallet Lift", "Pallet EUR · 1.250 kg effettivi",
     "Pick-up, trasporto e deposito autonomo di pallet euro fino a 1.250 kg con lift integrato.",
     [("Payload lift", "1.250 kg"), ("Velocità max", "1,2 m/s"), ("Autonomia", "~10,5 h"), ("Pallet", "EUR 800×1200")],
     [("Dimensioni base", "1.350 × 920 × 320 mm"), ("Peso robot", "350 kg"), ("Navigazione", "SLAM laser"), ("Flotta", "MiR Fleet")],
     "Stoccaggio e cross-docking pallet EUR senza operatore.", 92448),
    ("mir1200", "mir", "MiR · Muletto",
     "MiR1200 Pallet Jack EU", "Transpallet autonomo · 1.200 kg",
     "Pallet jack completamente autonomo per EUR pallet con flotta centralizzata MiR Fleet.",
     [("Payload", "1.200 kg"), ("Tipo", "Pallet jack"), ("Pallet", "EUR standard"), ("Flotta", "MiR Fleet")],
     [("Navigazione", "SLAM laser"), ("Integrazione", "WMS / ERP API"), ("Sicurezza", "ISO 3691-4"), ("Brand", "Teradyne / MiR")],
     "Cross-docking e stoccaggio pallet in hub logistici.", 137025),
    ("l1000", "latent", "Latent · Medio",
     "Youibot L1000-R", "Latent AMR · 1.000 kg",
     "Sollevamento sottoscocca 1 ton, laser SLAM ±5 mm. Deploy con Michelin, DHL, TSMC.",
     [("Payload", "1.000 kg"), ("Lift", "60 mm"), ("Autonomia", "8 h"), ("Precisione", "±5 mm")],
     [("Dimensioni", "1.060 × 838 × 300 mm"), ("Peso", "310 kg"), ("Velocità max", "1,5 m/s"), ("Software", "YOUIFLEET")],
     "Trasporto carrelli e pallet tra magazzino e produzione.", 50000),
    ("mav-1500", "latent", "Pesante · EU",
     "Neura Robotics MAV-1500", "AMR · 1.500 kg · PLd Cat.3",
     "Progettato in Germania: SLAM dinamico, lift 55 mm, ROS2 / OPC UA / VDA 5050.",
     [("Payload", "1.500 kg"), ("Lift", "0–55 mm"), ("Autonomia", "10 h"), ("Safety", "PLd Cat.3")],
     [("Dimensioni", "1.530 × 910 × 294 mm"), ("Peso", "400 kg"), ("Velocità max", "1,5 m/s"), ("IP", "IP44 (IP54 opt.)")],
     "Movimentazione carichi pesanti in automotive e metalmeccanica.", 44900),
    ("xp15", "muletti", "Muletto · AMR",
     "EP Equipment XP15", "Transpallet AMR · 1.500 kg",
     "Muletto elettrico autonomo con forche. LiDAR + camera, anche in modalità manuale.",
     [("Payload", "1.500 kg"), ("Forche", "1.150–1.500 mm"), ("Precisione", "±20 mm"), ("Batteria", "24V / 60Ah")],
     [("Dimensioni", "1.695 × 842 mm"), ("Peso", "335 kg"), ("Velocità max", "1,25 m/s"), ("Navigazione", "LiDAR 2D")],
     "Movimentazione pallet tra dock, magazzino e linea.", 25000),
    ("mav-lara", "mobile-cobot", "Mobile cobot",
     "Neura MAV-1500 + LARA 5", "Mobile manipulator · base 1.500 kg + cobot 5 kg",
     "Base MAV con cobot LARA 5: navigazione autonoma + manipolazione sul posto.",
     [("Base payload", "1.500 kg"), ("Cobot", "LARA 5 · 5 kg"), ("Reach cobot", "800 mm"), ("Ripetibilità", "±0,02 mm")],
     [("Navigazione", "SLAM + mapping dinamico"), ("Protocolli", "ROS2 · VDA 5050"), ("Safety", "PLd Cat.3"), ("Config.", "MAV + LARA 5")],
     "Machine tending mobile e kitting distribuito su più CNC.", 63800),
]

FEATURED_SLUGS = ("l300", "mir250-shelf", "mir600-pallet", "l1000", "xp15", "mav-1500")

GROUPS = {
    "leggeri": ("AMR leggeri · 200–300 kg", "Piattaforme compatte per tote, cassette e carrelli leggeri."),
    "mir": ("Gamma MiR (Teradyne)", "Mobile Industrial Robots — dalla piattaforma base ai pallet jack autonomi."),
    "latent": ("Latent lift · medio e pesante", "Sollevamento sottoscocca per carrelli e pallet fino a 1,5 t."),
    "muletti": ("Muletti autonomi", "Transpallet AMR per sostituire movimenti manuali con forche."),
    "mobile-cobot": ("Mobile manipulator", "AMR con braccio collaborativo integrato."),
}

AMR_MEDIA_CSS = """
    .robot-media.amr-media,
    .cat-media.amr-media {
      background: linear-gradient(145deg, #e8e8ec 0%, #d6d6dc 100%);
    }
    .robot-media.amr-media img,
    .robot-media.amr-media video,
    .cat-media.amr-media img,
    .cat-media.amr-media video {
      width: 100%; height: 100%; object-fit: contain; padding: 20px;
      filter: drop-shadow(0 12px 16px rgba(0,0,0,0.14));
      mix-blend-mode: multiply;
    }
    .robot-media.amr-media video,
    .cat-media.amr-media video { padding: 12px; mix-blend-mode: normal; }
    .cat-media.amr-media { aspect-ratio: 4/3; display: flex; align-items: center; justify-content: center; }
"""


def p(eur_net: float) -> str:
    abra = int(round(eur_net * 1.2))
    return f"da {f'{abra:,}'.replace(',', '.')},00 €"


def _norm_relpath(p: str | None) -> str | None:
    if not p:
        return None
    p = p.replace("\\", "/")
    for prefix in (f"{IMG}/", "images/manifattura/amr/"):
        if p.startswith(prefix):
            return p[len(prefix) :]
    return p.split("/")[-1]


def load_assets() -> dict:
    assets = {k: dict(v) for k, v in DEFAULT_ASSETS.items()}
    path = ROOT / "data" / "amr-images.json"
    if path.is_file():
        overrides = json.loads(path.read_text(encoding="utf-8"))
        for slug, o in overrides.items():
            if slug not in assets:
                continue
            if o.get("file"):
                assets[slug]["file"] = _norm_relpath(o["file"]) or assets[slug]["file"]
            if "video" in o:
                v = _norm_relpath(o.get("video"))
                if v:
                    assets[slug]["video"] = v
                else:
                    assets[slug].pop("video", None)
    return assets


_ASSETS: dict | None = None


def get_assets() -> dict:
    global _ASSETS
    if _ASSETS is None:
        _ASSETS = load_assets()
    return _ASSETS


def write_amr_catalog_json() -> None:
    items = []
    for row in CATALOG:
        slug, group, _, title, *_ = row
        a = get_assets()[slug]
        item = {
            "slug": slug,
            "title": title,
            "group": group,
            "file": f"{IMG}/{a['file']}",
        }
        if a.get("video"):
            item["video"] = f"{IMG}/{a['video']}"
        items.append(item)
    out = ROOT / "data" / "amr-catalog.json"
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote data/amr-catalog.json")


def by_slug(slug: str):
    return next(x for x in CATALOG if x[0] == slug)


def media_block(slug: str, title: str, tag: str = "") -> str:
    a = get_assets()[slug]
    primary = f"{IMG}/{a['file']}"
    video = a.get("video")
    if video:
        media = f'<video src="{IMG}/{video}" poster="{primary}" autoplay loop muted playsinline></video>'
    else:
        media = (
            f'<img src="{primary}" alt="{title}" loading="lazy" '
            f'onerror="this.closest(\'.robot-media\').classList.add(\'no-img\');">'
        )
    tag_html = f'<span class="robot-media-tag">{tag}</span>' if tag else ""
    return (
        f'<div class="robot-media amr-media">'
        f'{tag_html}{media}'
        f'<div class="robot-media-placeholder"><strong>{title.split()[0]}</strong><span>{title}</span></div></div>'
    )


def cat_media_block(slug: str, title: str) -> str:
    a = get_assets()[slug]
    primary = f"{IMG}/{a['file']}"
    video = a.get("video")
    if video:
        inner = f'<video src="{IMG}/{video}" poster="{primary}" autoplay loop muted playsinline></video>'
    else:
        inner = f'<img src="{primary}" alt="{title}" loading="lazy">'
    return f'<div class="cat-media amr-media">{inner}</div>'


def manifattura_card_v2(prod):
    slug, _, tag, title, subtitle, blurb, specs, rows, use_case, price = prod
    specs_html = "\n".join(
        f'              <div class="key-spec"><span class="key-spec-label">{k}</span><span class="key-spec-value">{v}</span></div>'
        for k, v in specs
    )
    rows_html = "\n".join(f"              <li><span>{k}</span><span>{v}</span></li>" for k, v in rows)
    return f"""
        <article class="robot-card" id="amr-{slug}">
          {media_block(slug, title, tag)}
          <div class="robot-body">
            <div><h3>{title}</h3><p class="robot-subtitle">{subtitle}</p></div>
            <p class="robot-blurb">{blurb}</p>
            <div class="key-specs">{specs_html}
            </div>
            <ul class="spec-rows">{rows_html}
            </ul>
            <div class="use-case-box">
              <span class="use-case-label">Caso d'uso chiave</span>
              <p class="use-case-text">{use_case}</p>
            </div>
            <div class="robot-card-cta">
              <span class="card-price">{p(price)}</span>
              <a href="prodotti/amr-{slug}.html" class="btn btn-primary btn-sm">Vedi scheda →</a>
            </div>
          </div>
        </article>"""


def catalogo_card(prod):
    slug, group, tag, title, subtitle, blurb, *_rest = prod
    price = prod[-1]
    return f"""
        <article class="cat-card" id="{slug}" data-group="{group}" data-name="{title.lower()}">
          {cat_media_block(slug, title)}
          <div class="cat-body">
            <p class="cat-family">{tag}</p>
            <h3>{title}</h3>
            <p class="cat-sub">{subtitle}</p>
            <p class="cat-blurb">{blurb}</p>
            <p class="cat-price">{p(price)}</p>
            <a href="prodotti/amr-{slug}.html" class="btn btn-primary btn-sm">Vedi scheda →</a>
          </div>
        </article>"""


featured_cards = "".join(manifattura_card_v2(by_slug(s)) for s in FEATURED_SLUGS)

MANIFATTURA_BODY = f"""
      <div class="vert-section-head">
        <p class="label">03 · AMR</p>
        <h2>I tuoi materiali arrivano in linea. Sempre, in orario, senza operatori logistici.</h2>
        <p>Gli AMR sostituiscono il trasporto manuale interno: tote, cassette, semilavorati, carrelli e pallet. Qui trovi <strong>6 modelli in evidenza</strong> — i più richiesti per latent lift, shelf MiR, pallet EUR e muletti. Il <a href="catalogo-amr.html">catalogo completo</a> include <strong>16 configurazioni</strong> MiR, Youibot, Neura, AutoXing ed EP Equipment. Prezzi indicativi — IVA esclusa.</p>
        <div class="amr-inclusion-box">
          <p><strong>Inclusi nel prezzo «da»:</strong> assessment iniziale, sopralluogo virtuale o fisico e prima analisi di fattibilità Abra.</p>
          <p><strong>Non inclusi</strong> (preventivo dedicato): digital twin, progettazione isola o cella, integrazione WMS/MES/ERP, software flotta, stazione di ricarica, commissioning in sito e top module aggiuntivi.</p>
        </div>
        <p class="price-note"><a href="catalogo-amr.html">Vedi tutte le 16 configurazioni AMR →</a></p>
      </div>

      <div class="robot-grid cols-3">
{featured_cards}
      </div>

      <div class="section-cta-row">
        <a href="catalogo-amr.html" class="btn btn-primary">Catalogo AMR completo (16 modelli)</a>
        <a href="#contact-form" class="btn btn-secondary">Richiedi preventivo</a>
      </div>
"""

catalog_sections = []
for gid, (heading, desc) in GROUPS.items():
    items = [catalogo_card(p) for p in CATALOG if p[1] == gid]
    catalog_sections.append(f"""
    <section class="cat-group" id="cat-{gid}">
      <h2>{heading}</h2>
      <p class="cat-group-desc">{desc}</p>
      <div class="cat-grid">{''.join(items)}
      </div>
    </section>""")


def inject_amr_css(html: str) -> str:
    if ".robot-media.amr-media video" in html:
        return html
    # replace old gallery CSS if present
    html = re.sub(r"\n    \.robot-media\.amr-media \.amr-media-stage[\s\S]*?\.cat-media\.amr-media \{ aspect-ratio: 4/3; \}\n", "\n", html)
    html = re.sub(r"\n    \.amr-gallery-thumbs[\s\S]*?\.thumb-video \{ position: relative; \}\n", "\n", html)
    return html.replace("</style>", AMR_MEDIA_CSS + "\n  </style>", 1)


def write_catalogo():
    body = "\n".join(catalog_sections)
    page = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catalogo AMR — 16 configurazioni | Abra Robotics</title>
  <meta name="description" content="Catalogo completo AMR: MiR, Youibot, Neura, AutoXing, EP Equipment. 16 configurazioni con prezzi indicativi IVA esclusa.">
  <link rel="canonical" href="https://abrarobotics.com/catalogo-amr.html">
  <link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <style>
    .cat-hero {{ padding: calc(40px + 72px + 48px) 48px 40px; border-bottom: 1px solid var(--gray-200); }}
    .cat-hero h1 {{ font-size: clamp(2rem,4vw,3rem); margin: 12px 0; }}
    .cat-body-page {{ padding: 48px; }}
    .cat-group {{ margin-bottom: 56px; }}
    .cat-group h2 {{ font-size: 1.35rem; margin: 0 0 8px; }}
    .cat-group-desc {{ color: var(--gray-600); margin: 0 0 24px; max-width: 720px; }}
    .cat-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }}
    .cat-card {{ background: rgba(255,255,255,0.75); backdrop-filter: blur(10px); border: 1px solid var(--gray-200); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; }}
    .cat-body {{ padding: 18px; display: flex; flex-direction: column; flex: 1; gap: 6px; }}
    .cat-card h3 {{ font-size: 0.95rem; margin: 0; font-weight: 700; }}
    .cat-sub {{ font-size: 0.78rem; color: var(--gray-500); margin: 0; }}
    .cat-blurb {{ font-size: 0.82rem; color: var(--gray-600); margin: 4px 0; flex: 1; line-height: 1.45; }}
    .cat-price {{ font-size: 1.1rem; font-weight: 900; margin: 4px 0 8px; }}
    .cat-family {{ font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--gray-400); margin: 0; }}
    .amr-note {{ background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 20px 24px; margin-bottom: 40px; font-size: 0.92rem; color: var(--gray-600); }}
    .cat-jump {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 32px; }}
    .cat-jump a {{ font-size: 0.85rem; padding: 8px 14px; border: 1px solid var(--gray-200); border-radius: 999px; text-decoration: none; color: var(--black); }}
    {AMR_MEDIA_CSS}
  </style>
</head>
<body>
  <div class="top-bar"><p>Catalogo AMR · IVA esclusa · <a href="manifattura-logistica.html#amr">Manifattura e Logistica</a></p></div>
  <nav class="navbar">
    <div class="container navbar-inner">
      <a href="index.html" class="logo"><img src="images/logo.png" alt="Abra Robotics" class="logo-img"></a>
      <div class="nav-links">
        <a href="manifattura-logistica.html#amr">AMR</a>
        <a href="catalogo-amr.html">Catalogo AMR</a>
        <a href="catalogo-unitree.html">Catalogo Unitree</a>
        <a href="index.html#cta-finale" class="btn btn-primary btn-sm">Prenota una chiamata</a>
      </div>
      <button class="menu-toggle" aria-label="Menu"><span></span><span></span></button>
    </div>
  </nav>
  <header class="cat-hero">
    <p class="label">Manifattura e logistica</p>
    <h1>Catalogo AMR completo</h1>
    <p style="color:var(--gray-600);max-width:680px;">16 configurazioni con foto prodotto corrette e video ufficiali MiR (luci in movimento sulle basi). Prezzi «da» — IVA esclusa.</p>
  </header>
  <main class="cat-body-page">
    <div class="amr-note">
      <p><strong>Inclusi nel prezzo «da»:</strong> assessment, sopralluogo e prima analisi di fattibilità Abra.</p>
      <p style="margin:0;"><strong>Non inclusi:</strong> digital twin, WMS/MES/ERP, software flotta, ricarica, commissioning.</p>
    </div>
    <nav class="cat-jump" aria-label="Categorie AMR">
      <a href="#cat-leggeri">Leggeri</a><a href="#cat-mir">MiR</a><a href="#cat-latent">Latent</a><a href="#cat-muletti">Muletti</a><a href="#cat-mobile-cobot">Mobile cobot</a>
    </nav>
{body}
    <p style="margin-top:48px;text-align:center;">
      <a href="manifattura-logistica.html#amr" class="btn btn-secondary">Modelli in evidenza</a>
      <a href="manifattura-logistica.html#contact-form" class="btn btn-primary" style="margin-left:12px;">Richiedi preventivo</a>
    </p>
  </main>
  <footer class="footer"><div class="container footer-inner"><p>© 2026 Abra Robotics</p></div></footer>
  <script src="script.js"></script>
</body>
</html>
"""
    (ROOT / "catalogo-amr.html").write_text(page, encoding="utf-8")
    print("Wrote catalogo-amr.html")


def patch_manifattura():
    path = ROOT / "manifattura-logistica.html"
    html = path.read_text(encoding="utf-8")
    html = inject_amr_css(html)
    amr_pos = html.index('id="amr"')
    start = html.index('<div class="vert-section-head">', amr_pos)
    end = html.index("<!-- SEZIONE 4 - COBOT -->")
    end = html.rindex("</div>", amr_pos, end)
    # keep container close: find last </div> before </section>
    section_end = html.index("</section>", end)
    container_close = html.rindex("</div>", end, section_end)
    html = html[:start] + MANIFATTURA_BODY.strip() + "\n\n" + html[container_close:]
    html = re.sub(r"\n  <script>\s*\(function \(\) \{[\s\S]*?data-amr-gallery[\s\S]*?\}\)\(\);\s*</script>", "", html)
    path.write_text(html, encoding="utf-8")
    print("Patched manifattura-logistica.html")


if __name__ == "__main__":
    write_amr_catalog_json()
    write_catalogo()
    patch_manifattura()
    import subprocess
    import sys

    prod = ROOT / "scripts" / "_gen_amr_products.py"
    subprocess.run([sys.executable, str(prod)], check=True)
