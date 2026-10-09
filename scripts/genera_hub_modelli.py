#!/usr/bin/env python3
"""Pagine hub per famiglia di modello Unitree (IT + EN), generate dal listino pubblico.

Obiettivo SEO: essere la pagina di riferimento tra i venditori per le ricerche
"unitree <modello> prezzo/price/preis/kaufen", versioni (EDU, Air, Pro, W) e specifiche.
- Prezzi e versioni: listini/pubblico/end-user.json (unica fonte, prezzi End-User IVA esclusa).
- Specifiche: SOLO dati ufficiali Unitree (FAMILIES[*]["specs"]), con link alla fonte.
- Header, menu e footer copiati da umanoidi.html / en/umanoidi-en.html (stesso sito, stesso consenso cookie).
Idempotente. Uso: python3 scripts/genera_hub_modelli.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from genera_correlati import label  # noqa: E402

SITE = "https://abrarobotics.com"
CAL = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ22FrpPdyPVRihi4eXPQlljTcG2toa8XF2d8W-QX-L9cKMaXqozq_YsHym56LEdTs9WsnqlTHeF"

# Famiglie: prefissi del primo token del nome a listino (dopo "UNITREE").
FAMILIES = {
    "g1": {
        "name": "G1", "prefixes": ["G1", "G1-E"], "it_page": "g1.html", "en_page": "en/g1-en.html",
        "image": "images/prodotti/2026/famiglia-g1.png", "parent_it": "umanoidi.html", "parent_en": "en/umanoidi-en.html",
        "type_it": "Robot umanoide", "type_en": "Humanoid robot",
        "source": "https://www.unitree.com/g1/",
        "specs": [("Dimensioni in piedi", "Standing dimensions", "1320 × 450 × 200 mm"), ("Peso", "Weight", "circa 35 kg|about 35 kg"),
                  ("Gradi di libertà (G1)", "Degrees of freedom (G1)", "23"), ("Coppia max ginocchio", "Max knee torque", "90 N·m (G1), 120 N·m (EDU)"),
                  ("Carico braccio", "Arm payload", "circa 2 kg (G1), 3 kg (EDU)|about 2 kg (G1), 3 kg (EDU)"),
                  ("Batteria", "Battery", "9000 mAh"), ("Autonomia", "Battery life", "circa 2 ore|about 2 hours")],
        "choose_it": [("G1 Air", "per dimostrazioni, eventi e attività di comunicazione: è la versione con meno gradi di libertà e senza sviluppo secondario."),
                      ("G1 EDU (U1–U10)", "per ricerca e sviluppo: aggiunge sviluppo secondario (SDK), coppia al ginocchio di 120 N·m, carico braccio di 3 kg e, nelle versioni superiori, mani destre."),
                      ("G1-D", "se il compito è la manipolazione su banco o in reparto: busto dual-arm su piantana o base mobile, vedi la famiglia G1-D.")],
        "choose_en": [("G1 Air", "for demos, events and marketing: fewer degrees of freedom and no secondary development."),
                      ("G1 EDU (U1–U10)", "for research and development: secondary development (SDK), 120 N·m knee torque, 3 kg arm payload and, in higher versions, dexterous hands."),
                      ("G1-D", "for bench or shop-floor manipulation: dual-arm torso on a fixed stand or mobile base, see the G1-D family.")],
        "what_it": "Il G1 cammina, si rialza, esegue movimenti dimostrativi dall'app Unitree e, nelle versioni EDU, si programma via SDK per ricerca su locomozione, manipolazione e apprendimento.",
        "what_en": "The G1 walks, gets up, performs demo motions from the Unitree app and, in EDU versions, can be programmed via SDK for research on locomotion, manipulation and learning.",
    },
    "go2": {
        "name": "Go2", "prefixes": ["GO2", "GO2-W", "GO2-X"], "it_page": "go2.html", "en_page": "en/go2-en.html",
        "image": "images/prodotti/go2-edu-smart.webp", "parent_it": "quadrupedi.html", "parent_en": "en/quadrupedi-en.html",
        "type_it": "Cane robot quadrupede", "type_en": "Quadruped robot dog",
        "source": "https://www.unitree.com/go2/",
        "specs": [("Dimensioni in piedi", "Standing dimensions", "70 × 31 × 40 cm"), ("Peso", "Weight", "circa 15 kg|about 15 kg"),
                  ("Velocità max", "Max speed", "2,5 m/s (Air), 3,5 m/s (Pro), 3,7 m/s fino a ~5 m/s (EDU)|2.5 m/s (Air), 3.5 m/s (Pro), 3.7 m/s up to ~5 m/s (EDU)"),
                  ("Carico", "Payload", "≈7 kg (Air), ≈8 kg (Pro, EDU), max ~12 kg (EDU)"),
                  ("Batteria", "Battery", "8000 mAh"), ("Autonomia", "Battery life", "circa 1–2 ore|about 1–2 hours"),
                  ("LiDAR", "LiDAR", "4D LiDAR super grandangolare|Super-wide-angle 4D LiDAR")],
        "choose_it": [("Go2 Air", "per avvicinarsi ai quadrupedi e per eventi: è la versione d'ingresso."),
                      ("Go2 Pro", "più veloce e con più carico dell'Air, per uso dimostrativo avanzato."),
                      ("Go2 EDU", "per sviluppo e ricerca: sviluppo secondario, prestazioni più alte e configurazioni con LiDAR aggiuntivi."),
                      ("Go2-W", "versione con ruote alle zampe, per superfici lunghe e piane.")],
        "choose_en": [("Go2 Air", "entry-level version for getting started with quadrupeds and for events."),
                      ("Go2 Pro", "faster and with more payload than the Air, for advanced demos."),
                      ("Go2 EDU", "for development and research: secondary development, higher performance and configurations with extra LiDARs."),
                      ("Go2-W", "wheeled-leg version for long, flat surfaces.")],
        "what_it": "Il Go2 è un quadrupede compatto: cammina e corre su terreni vari, segue la persona, si controlla da app e telecomando; le versioni EDU si programmano per ricerca, ispezione e didattica.",
        "what_en": "The Go2 is a compact quadruped: it walks and runs on varied terrain, follows its user and is controlled via app and remote; EDU versions are programmable for research, inspection and education.",
    },
    "r1": {
        "name": "R1", "prefixes": ["R1"], "exclude": ["R1-A", "R1-D"], "it_page": "r1.html", "en_page": "en/r1-en.html",
        "image": "images/prodotti/2026/famiglia-r1.jpg", "parent_it": "umanoidi.html", "parent_en": "en/umanoidi-en.html",
        "type_it": "Robot umanoide", "type_en": "Humanoid robot",
        "source": "https://www.unitree.com/R1/",
        "specs": [("Dimensioni", "Dimensions", "1230 × 357 × 190 mm"), ("Peso", "Weight", "circa 27 kg (Air), circa 29 kg (R1, EDU)|about 27 kg (Air), about 29 kg (R1, EDU)"),
                  ("Gradi di libertà", "Degrees of freedom", "20 (Air), 26 (R1, EDU)"), ("Autonomia", "Battery life", "circa 1 ora|about 1 hour"),
                  ("Calcolo", "Computing", "processore 8 core|8-core processor"), ("Telecamere", "Cameras", "monoculare (Air), binoculare (R1, EDU)|monocular (Air), binocular (R1, EDU)")],
        "choose_it": [("R1 Air", "la versione più semplice: 20 gradi di libertà, senza vita e testa motorizzate."),
                      ("R1 / R1 Basic", "26 gradi di libertà con vita e testa mobili, telecamera binoculare."),
                      ("R1 EDU", "per sviluppo e didattica, con configurazioni di mani e calcolo aggiuntivo.")],
        "choose_en": [("R1 Air", "the simplest version: 20 degrees of freedom, no motorised waist or head."),
                      ("R1 / R1 Basic", "26 degrees of freedom with movable waist and head, binocular camera."),
                      ("R1 EDU", "for development and education, with hand and extra computing configurations.")],
        "what_it": "L'R1 è l'umanoide bipede più compatto e accessibile di Unitree: adatto a didattica, laboratori, dimostrazioni e sviluppo di base.",
        "what_en": "The R1 is Unitree's most compact and affordable biped humanoid: suited to education, labs, demos and entry-level development.",
    },
    "a2": {
        "name": "A2", "prefixes": ["A2", "A2-W"], "it_page": "a2.html", "en_page": "en/a2-en.html",
        "image": "images/prodotti/a2-pro.png", "parent_it": "quadrupedi.html", "parent_en": "en/quadrupedi-en.html",
        "type_it": "Quadrupede industriale", "type_en": "Industrial quadruped",
        "source": "https://www.unitree.com/A2/",
        "specs": [("Peso", "Weight", "circa 42 kg con batteria|about 42 kg with battery"),
                  ("Carico", "Payload", "circa 100 kg da fermo, circa 25 kg in camminata continua|about 100 kg standing, about 25 kg continuous walking"),
                  ("Velocità max", "Max speed", "0–3,7 m/s (fino a ~5 m/s)|0–3.7 m/s (up to ~5 m/s)"),
                  ("Autonomia", "Endurance", "oltre 5 ore senza carico (circa 20 km)|over 5 hours unloaded (about 20 km)"),
                  ("Protezione", "Protection", "IP56 (A2), IP56–IP67 (A2 Pro)"),
                  ("Sensori", "Sensors", "1 LiDAR + telecamera HD (A2), 2 LiDAR + telecamera HD (A2 Pro)|1 LiDAR + HD camera (A2), 2 LiDAR + HD camera (A2 Pro)")],
        "choose_it": [("A2 Standard", "quadrupede industriale per ispezione e trasporto leggero, IP56."),
                      ("A2 Pro", "due LiDAR e componenti principali IP67, per ambienti più gravosi."),
                      ("A2-W", "versione con ruote per percorsi lunghi su superfici regolari.")],
        "choose_en": [("A2 Standard", "industrial quadruped for inspection and light transport, IP56."),
                      ("A2 Pro", "two LiDARs and IP67 core components for harsher environments."),
                      ("A2-W", "wheeled version for long routes on regular surfaces.")],
        "what_it": "L'A2 è un quadrupede industriale per ispezioni, sorveglianza e trasporto in impianti, con lunga autonomia e protezione dagli agenti esterni.",
        "what_en": "The A2 is an industrial quadruped for inspection, surveillance and transport in plants, with long endurance and environmental protection.",
    },
    "b2": {
        "name": "B2", "prefixes": ["B2", "B2-W", "B2W"], "it_page": "b2.html", "en_page": "en/b2-en.html",
        "image": "prodotti/assets/variants/b2/img-02.jpg", "parent_it": "quadrupedi.html", "parent_en": "en/quadrupedi-en.html",
        "type_it": "Quadrupede industriale pesante", "type_en": "Heavy industrial quadruped",
        "source": "https://www.unitree.com/b2/",
        "specs": [("Peso", "Weight", "≈60 kg con batteria|≈60 kg with battery"),
                  ("Carico", "Payload", "≥120 kg da fermo, >40 kg in camminata|≥120 kg standing, >40 kg walking"),
                  ("Velocità max", "Max speed", "> 6 m/s"), ("Batteria", "Battery", "45 Ah (2250 Wh), 58 V"),
                  ("Autonomia", "Endurance", "oltre 5 ore senza carico, oltre 20 km|over 5 hours unloaded, over 20 km"),
                  ("Protezione", "Protection", "IP67")],
        "choose_it": [("B2", "quadrupede pesante su zampe per ispezione industriale, terreni difficili e carichi elevati."),
                      ("B2-W", "versione con ruote, più efficiente su lunghe distanze; disponibile anche come kit di conversione.")],
        "choose_en": [("B2", "heavy legged quadruped for industrial inspection, rough terrain and high payloads."),
                      ("B2-W", "wheeled version, more efficient over long distances; also available as a conversion kit.")],
        "what_it": "Il B2 è il quadrupede industriale più robusto di Unitree: ispezione di impianti, ambienti esterni e trasporto di carichi.",
        "what_en": "The B2 is Unitree's most rugged industrial quadruped: plant inspection, outdoor environments and payload transport.",
    },
    "z1": {
        "name": "Z1 e D1", "name_en": "Z1 and D1", "prefixes": ["Z1", "D1", "D1-T"], "it_page": "z1.html", "en_page": "en/z1-en.html",
        "image": "images/accessori/z1.jpg", "parent_it": "accessori.html", "parent_en": "en/accessori-en.html",
        "type_it": "Braccio robotico", "type_en": "Robot arm", "seo_it": "Unitree Z1 prezzo: bracci robotici Z1 e D1", "seo_en": "Unitree Z1 price: Z1 and D1 robot arms",
        "source": "https://www.unitree.com/z1/", "source2": "https://www.unitree.com/D1-T/",
        "specs": [("Z1: assi", "Z1: axes", "6"), ("Z1: peso", "Z1: weight", "4,3 kg (Air), 4,5 kg (Pro)|4.3 kg (Air), 4.5 kg (Pro)"),
                  ("Z1: carico", "Z1: payload", "2 kg (Air), ≥3 kg (Pro)"), ("Z1: sbraccio", "Z1: reach", "740 mm"),
                  ("Z1: ripetibilità", "Z1: repeatability", "~0,1 mm|~0.1 mm"),
                  ("D1: assi", "D1: axes", "6 + pinza|6 + gripper"), ("D1: carico", "D1: payload", "500 g"), ("D1: sbraccio", "D1: reach", "550 mm (670 mm con pinza)|550 mm (670 mm with gripper)")],
        "choose_it": [("Z1 Air", "braccio a 6 assi da 2 kg, anche da montare su quadrupede."),
                      ("Z1 Pro", "stesso sbraccio, carico di almeno 3 kg."),
                      ("D1 / D1-T", "braccio leggero da 500 g; il D1-T è il kit di teleoperazione con due bracci.")],
        "choose_en": [("Z1 Air", "6-axis arm with 2 kg payload, also mountable on a quadruped."),
                      ("Z1 Pro", "same reach, payload of at least 3 kg."),
                      ("D1 / D1-T", "lightweight 500 g payload arm; D1-T is the dual-arm teleoperation kit.")],
        "what_it": "Z1 e D1 sono i bracci robotici Unitree per manipolazione leggera, ricerca e montaggio su robot mobili.",
        "what_en": "Z1 and D1 are Unitree's robot arms for light manipulation, research and mounting on mobile robots.",
    },
    # Solo EN: le pagine italiane esistono gia' (as2.html, h2.html, g1-d.html).
    "as2": {
        "name": "AS2", "prefixes": ["AS2", "AS2-W", "AS2-X"], "it_page": "as2.html", "en_page": "en/as2-en.html", "en_only": True,
        "image": "images/prodotti/2026/as2.png", "parent_en": "en/quadrupedi-en.html",
        "type_en": "Quadruped robot", "source": "https://www.unitree.com/As2/",
        "specs": [("", "Weight", "|approx. 20 kg with battery"),
                  ("", "Max speed", "|0–3.0 m/s (Air), 0–3.7 m/s (Pro), 0–3.7 m/s up to ~5 m/s (X, EDU)"),
                  ("", "Walking payload", "|approx. 10 kg (Air), 13 kg (Pro), 15 kg (X, EDU)"),
                  ("", "Endurance", "|~2 h (Air), ~4 h (Pro, X, EDU) unloaded"), ("", "Protection", "|IP54 (Pro, X, EDU)"),
                  ("", "LiDAR", "|Unitree L2 (Pro, X), industrial 64–128-line LiDAR (EDU)")],
        "choose_en": [("AS2 Air", "entry version with HD camera, for demos and getting started."),
                      ("AS2 Pro / X", "Unitree L2 LiDAR, IP54 and about 4 h endurance."),
                      ("AS2 EDU", "for development: industrial LiDAR and secondary development."),
                      ("AS2-W", "wheeled version.")],
        "what_en": "The AS2 is Unitree's new-generation mid-size quadruped, between Go2 and A2, for research, inspection and demos.",
    },
    "h2": {
        "name": "H2", "prefixes": ["H2", "H2-D", "H2-A"], "it_page": "h2.html", "en_page": "en/h2-en.html", "en_only": True,
        "image": "images/prodotti/2026/famiglia-h2.png", "parent_en": "en/umanoidi-en.html",
        "type_en": "Full-size humanoid robot", "source": "https://www.unitree.com/H2/",
        "specs": [("", "Dimensions", "|1820 × 456 × 218 mm"), ("", "Weight", "|about 70 kg"), ("", "Degrees of freedom", "|31"),
                  ("", "Battery life", "|about 3 hours"), ("", "Max joint torque", "|360 N·m (leg), 120 N·m (arm)"),
                  ("", "Computing", "|Intel Core i5, optional Intel Core i7")],
        "choose_en": [("H2 Air", "full-size humanoid for demos and showrooms."),
                      ("H2 EDU", "for research and development with secondary development."),
                      ("H2-D / H2-A", "dual-arm torso versions for manipulation.")],
        "what_en": "The H2 is Unitree's full-size humanoid (about 1.8 m), for research, advanced demos and human-scale tasks.",
    },
    "g1-d": {
        "name": "G1-D", "prefixes": ["G1-D", "G1D"], "it_page": "g1-d.html", "en_page": "en/g1-d-en.html", "en_only": True,
        "image": "images/prodotti/2026/famiglia-g1-d.jpg", "parent_en": "en/umanoidi-en.html",
        "type_en": "Wheeled dual-arm humanoid", "source": "https://www.unitree.com/G1-D/",
        "specs": [("", "Type", "|wheeled dual-arm humanoid, differential drive, 360° in-place rotation"),
                  ("", "Degrees of freedom", "|17 (Standard), 19 (Ultimate), excl. end effector; 7 per arm"),
                  ("", "Single-arm payload", "|approx. 3 kg"), ("", "Height", "|1260–1680 mm (adjustable column)"),
                  ("", "Weight", "|approx. 90 kg incl. battery"), ("", "Base speed", "|1.5 m/s"),
                  ("", "Battery life", "|approx. 2 h (Standard), approx. 6 h (Ultimate)")],
        "choose_en": [("G1-D Standard", "fixed stand or base, 17 DOF, about 2 h battery."),
                      ("G1-D Flagship / Ultimate", "mobile base, 19 DOF, about 6 h battery.")],
        "what_en": "The G1-D is a dual-arm humanoid torso on a fixed stand or mobile base, built for manipulation tasks on benches and shop floors.",
    },
}


def family_of(name: str) -> str | None:
    first = name.upper().replace("UNITREE ", "").split()[0].rstrip("/") if name.strip() else ""
    best = None
    for key, f in FAMILIES.items():
        for p in f["prefixes"]:
            if first == p or (first.startswith(p) and not first[len(p):len(p) + 1].isalnum()):
                if any(first.startswith(x) for x in f.get("exclude", [])):
                    continue
                if best is None or len(p) > best[1]:
                    best = (key, len(p))
    return best[0] if best else None


def eur(x: float, en: bool) -> str:
    s = f"{x:,.0f}"
    return s if en else s.replace(",", ".")


def load() -> dict[str, dict]:
    items = json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8"))
    out: dict[str, dict] = {k: {"robots": [], "acc": []} for k in FAMILIES}
    for sku, v in items.items():
        slug = v.get("slug")
        p = ROOT / "prodotti" / (slug or "_")
        if not slug or not p.is_file() or 'http-equiv="refresh"' in p.read_text(encoding="utf-8"):
            continue
        fam = family_of(v.get("nome", ""))
        if not fam:
            continue
        row = {"sku": sku, "name": label(v["nome"]), "price": v.get("prezzo_eur"), "slug": slug}
        is_robot = v.get("categoria") == "UMANOIDI"
        if fam == "z1":  # bracci: i "robot" sono i bracci, non pinze/telecamere/motori
            n = v["nome"].upper()
            is_robot = bool(re.match(r"Z1 (AIR|PRO)\b|D1 ROBOTIC ARM|D1-T", n))
        out[fam]["robots" if is_robot else "acc"].append(row)
    for f in out.values():
        f["robots"].sort(key=lambda r: r["price"] or 0)
        f["acc"].sort(key=lambda r: r["price"] or 0)
    return out


def split(v: str, en: bool) -> str:
    if "|" in v:
        it, e = v.split("|", 1)
        return e if en else it
    return v


def template(en: bool) -> tuple[str, str, str, str]:
    """(head_prefix, style_block, body_chrome, footer) dalla pagina umanoidi della lingua."""
    s = (ROOT / ("en/umanoidi-en.html" if en else "umanoidi.html")).read_text(encoding="utf-8")
    head_prefix = s[: s.index("<title>")]
    # via i tag specifici della pagina template (canonical, hreflang, descrizione, social, JSON-LD)
    head_prefix = re.sub(r'\s*<link[^>]*(rel="canonical"|hreflang=)[^>]*>', "", head_prefix)
    head_prefix = re.sub(r'\s*<meta[^>]*(name="(description|robots|keywords)"|property="og:|name="twitter:)[^>]*>', "", head_prefix)
    head_prefix = re.sub(r'\s*<script type="application/ld\+json">[\s\S]*?</script>', "", head_prefix)
    style = re.search(r"<style>[\s\S]*?</style>", s).group(0)
    body = s[s.index("<body>"): s.index("<!-- HERO -->")]
    footer = s[s.index('<footer class="footer">'): s.index("</footer>") + len("</footer>")]
    return head_prefix, style, body, footer


HUB_CSS = """<style id="hub-modello-css">
.hm-table{width:100%;border-collapse:collapse;font-size:.95rem}
.hm-table th,.hm-table td{padding:10px 12px;border-bottom:1px solid var(--gray-200);text-align:left;vertical-align:top}
.hm-table th{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--gray-600)}
.hm-table td.p{white-space:nowrap;font-weight:700}
.hm-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.hm-specs{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:20px}
.hm-specs div{border:1px solid var(--gray-200);border-radius:var(--radius);padding:14px}
.hm-specs span{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--gray-600);margin-bottom:4px}
.hm-specs strong{font-size:1rem;line-height:1.35}
.hm-choose{display:grid;gap:12px;margin-top:20px}
.hm-choose p{margin:0;line-height:1.6}
.hm-acc{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:6px;list-style:none;padding:0;margin:20px 0 0}
.hm-acc a{display:flex;justify-content:space-between;gap:10px;padding:9px 12px;border:1px solid var(--gray-200);border-radius:8px;color:var(--black);text-decoration:none;font-size:.92rem}
.hm-acc a span{color:var(--gray-600);white-space:nowrap}
.hm-src a{color:var(--accent-text);overflow-wrap:anywhere}
.hm-faq details{border-bottom:1px solid var(--gray-200);padding:14px 0}
.hm-faq summary{font-weight:700;cursor:pointer}
.hm-faq p{margin:10px 0 0;line-height:1.6;color:var(--gray-600)}
.hm-fam{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.hm-fam a{padding:6px 12px;border:1px solid var(--gray-200);border-radius:999px;color:var(--black);text-decoration:none;font-size:.9rem}
</style>"""


def page(key: str, f: dict, data: dict, en: bool) -> str:
    pre = "../" if en else ""
    url_it = f"{SITE}/{f['it_page']}"
    url_en = f"{SITE}/{f['en_page']}"
    own = url_en if en else url_it
    name = f.get("name_en", f["name"]) if en else f["name"]
    robots, acc = data["robots"], data["acc"]
    prices = [r["price"] for r in robots if r["price"]] or [r["price"] for r in acc if r["price"]]
    low, high = (min(prices), max(prices)) if prices else (None, None)
    head_prefix, style, body, footer = template(en)

    def link(slug: str) -> str:
        if en:
            en_slug = slug.replace(".html", "-en.html")
            if (ROOT / "en/prodotti" / en_slug).is_file():
                return f"prodotti/{en_slug}"
            return f"../prodotti/{slug}"
        return f"prodotti/{slug}"

    if en:
        title = f.get("seo_en") or f"Unitree {name} price: versions and specs | Abra"
        h1 = f"Unitree {name}: price and versions in Europe"
        desc = (f"Unitree {name} price in Europe: all versions from € {eur(low, True)} excl. VAT, official specs and "
                f"which to choose. Sold in Italy by Abra Robotics.") if low else f"Unitree {name}: versions, official specs and quote from Abra Robotics."
        lead = f"{f['what_en']} Below: every {name} version we sell with its end-user price (excl. VAT), the official specifications and how to choose."
    else:
        title = f.get("seo_it") or f"Unitree {name} prezzo: versioni e specifiche | Abra"
        h1 = f"Unitree {name}: prezzi e versioni in Italia"
        desc = (f"Prezzo Unitree {name} in Italia: tutte le versioni da {eur(low, False)} € IVA esclusa, specifiche ufficiali "
                f"e quale scegliere. Filiera di distribuzione di Unitree Italia.") if low else f"Unitree {name}: versioni, specifiche ufficiali e preventivo da Abra Robotics."
        lead = f"{f['what_it']} Qui trovi tutte le versioni {name} a listino con prezzo End-User (IVA esclusa), le specifiche ufficiali e come scegliere."
    if len(title) > 60:
        title = title.replace(" | Abra", "")[:60].rsplit(" ", 1)[0]
    if len(desc) > 158:
        desc = desc[:157].rsplit(" ", 1)[0].rstrip(",.") + "."

    rows = robots or acc
    th = ("Version", "Price (excl. VAT)", "") if en else ("Versione", "Prezzo (IVA esclusa)", "")
    tr = "\n".join(
        f'<tr><td><a href="{link(r["slug"])}">{html.escape(r["name"])}</a></td>'
        f'<td class="p">{("from € " + eur(r["price"], True)) if en else ("da " + eur(r["price"], False) + " €")}</td>'
        f'<td><a href="{link(r["slug"])}">{"Details" if en else "Scheda"} →</a></td></tr>'
        for r in rows if r["price"])
    table = f'<div class="hm-wrap"><table class="hm-table"><thead><tr><th>{th[0]}</th><th>{th[1]}</th><th>{th[2]}</th></tr></thead><tbody>\n{tr}\n</tbody></table></div>'

    specs = "".join(f'<div><span>{html.escape(s[1] if en else s[0])}</span><strong>{html.escape(split(s[2], en))}</strong></div>'
                    for s in f["specs"] if (s[1] if en else s[0]))
    choose = "".join(f"<p><strong>{html.escape(a)}</strong>: {html.escape(b)}</p>" for a, b in f["choose_en" if en else "choose_it"])
    acc_html = ""
    if robots and acc:
        acc_html = (f'<section class="section" style="padding-top:0"><div class="container"><h2>{"Accessories for" if en else "Accessori per"} Unitree {html.escape(name)}</h2>'
                    '<ul class="hm-acc">' + "".join(
                        f'<li><a href="{link(a["slug"])}">{html.escape(a["name"])}<span>{("from € " + eur(a["price"], True)) if en else ("da " + eur(a["price"], False) + " €")}</span></a></li>'
                        for a in acc[:24] if a["price"]) + "</ul></div></section>")

    srcs = [f["source"]] + ([f["source2"]] if f.get("source2") else [])
    if en:
        faq = [
            (f"How much does the Unitree {name} cost?", f"End-user prices for the Unitree {name} start from € {eur(low, True)} excluding VAT and go up to € {eur(high, True)} depending on the version. Prices include shipping and duty to Italy; every order is confirmed with an updated quote." if low else f"Contact us for a quote on the Unitree {name}."),
            (f"Which Unitree {name} version should I choose?", " ".join(f"{a}: {b}" for a, b in f["choose_en"])),
            (f"What can the Unitree {name} do?", f["what_en"]),
            (f"Can I buy the Unitree {name} outside Italy?", "We mainly work in Italy, Switzerland and the Balkans; other EU countries on a project basis. Contact us for delivery and a quote for your country."),
            (f"Where do the {name} specifications come from?", "From Unitree's official product page, linked in the Sources section. Actual configuration depends on the version you order."),
        ]
    else:
        faq = [
            (f"Quanto costa l'Unitree {name}?", f"I prezzi End-User dell'Unitree {name} partono da {eur(low, False)} € IVA esclusa e arrivano a {eur(high, False)} € a seconda della versione. Spedizione e dazio in Italia sono inclusi; ogni ordine si conferma con un preventivo aggiornato." if low else f"Contattaci per un preventivo sull'Unitree {name}."),
            (f"Quale versione dell'Unitree {name} scegliere?", " ".join(f"{a}: {b}" for a, b in f["choose_it"])),
            (f"Cosa fa l'Unitree {name}?", f["what_it"]),
            (f"Si può finanziare l'acquisto dell'Unitree {name}?", "Spesso sì: verifichiamo gratuitamente se il progetto rientra in iperammortamento, Nuova Sabatini o bandi regionali prima del preventivo. Dettagli nella pagina Finanziamenti."),
            (f"Consegnate l'Unitree {name} anche fuori dall'Italia?", "Lavoriamo principalmente in Italia, Svizzera e Balcani; altri paesi UE su progetto. Contattaci per tempi e preventivo."),
        ]
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)

    fam_links = "".join(
        f'<a href="{(("../" + g["en_page"].split("/", 1)[1]) if False else (g["en_page"].split("/", 1)[1] if en else g["it_page"]))}">Unitree {html.escape(g.get("name_en", g["name"]) if en else g["name"])}</a>'
        for k2, g in FAMILIES.items() if k2 != key and (en or not g.get("en_only") or (ROOT / g["it_page"]).is_file()))

    ld_product = {"@context": "https://schema.org", "@type": "Product", "name": f"Unitree {name}", "brand": {"@type": "Brand", "name": "Unitree"},
                  "image": f"{SITE}/{f['image']}", "description": desc, "url": own}
    if low:
        ld_product["offers"] = {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": f"{low:.2f}", "highPrice": f"{high:.2f}",
                                "offerCount": len([r for r in rows if r["price"]]),
                                "seller": {"@type": "Organization", "name": "Abra Robotics", "url": SITE}}
    parent = f["parent_en"] if en else f["parent_it"]
    ld_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/{'en/index-en.html' if en else ''}"},
        {"@type": "ListItem", "position": 2, "name": parent.split("/")[-1].replace("-en.html", "").replace(".html", "").capitalize(), "item": f"{SITE}/{parent}"},
        {"@type": "ListItem", "position": 3, "name": f"Unitree {name}", "item": own}]}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld_product, ld_bc, ld_faq))

    hreflang = (f'<link rel="alternate" hreflang="it" href="{url_it}"/>\n<link rel="alternate" hreflang="en" href="{url_en}"/>\n'
                f'<link rel="alternate" hreflang="x-default" href="{url_it}"/>')
    lang_label = ("Italiano", url_it) if en else ("English", url_en)
    sources = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{u}</a></li>' for u in srcs)
    parent_rel = parent.split("/", 1)[1] if en else parent
    cta_assess = "assessment-en.html" if en else "assessment.html"
    T = (lambda e, i: e if en else i)

    head = f"""{head_prefix}<title>{html.escape(title)}</title>
{hreflang}
<meta content="{html.escape(desc)}" name="description"/>
<meta content="index, follow" name="robots"/>
<link href="{own}" rel="canonical"/>
<link href="{pre}favicon.ico" rel="icon" sizes="any"/>
<link href="{pre}images/favicon-32x32.png" rel="icon" type="image/png" sizes="32x32"/>
<link href="{pre}images/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="{pre}style.css" rel="stylesheet"/>
{style}
{HUB_CSS}
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Abra Robotics"/>
<meta property="og:title" content="{html.escape(title)}"/>
<meta property="og:description" content="{html.escape(desc)}"/>
<meta property="og:url" content="{own}"/>
<meta property="og:image" content="{SITE}/{f['image']}"/>
<meta property="og:locale" content="{T('en_GB', 'it_IT')}"/>
<meta name="twitter:card" content="summary_large_image"/>
{lds}
</head>
"""
    main = f"""<!-- HERO -->
<section class="collection-hero">
<div class="container">
<p class="label"><a href="{parent_rel}" style="color:inherit">{html.escape(T(f['type_en'], f.get('type_it', '')))}</a> · <a href="{lang_label[1]}" hreflang="{T('it', 'en')}" style="color:inherit">{lang_label[0]}</a></p>
<h1>{html.escape(h1)}</h1>
<p class="lead">{html.escape(lead)}</p>
<div class="hero-meta">
<div><strong>{len([r for r in rows if r['price']])}</strong><span>{T('Versions', 'Versioni a listino')}</span></div>
{('<div><strong>' + (T('from € ' + eur(low, True), 'da ' + eur(low, False) + ' €')) + '</strong><span>' + T('excl. VAT', 'IVA esclusa') + '</span></div>') if low else ''}
<div><strong>{T('Italy', 'Italia')}</strong><span>{T('Unitree Italy distribution chain', 'Filiera di distribuzione di Unitree Italia')}</span></div>
</div>
<div class="hm-fam">{fam_links}</div>
</div>
</section>
<section class="section" style="padding-top:24px"><div class="container">
<h2>{T(f'Unitree {name} versions and prices', f'Versioni e prezzi Unitree {name}')}</h2>
<p>{T('End-user prices excluding VAT, shipping and duty to Italy included. Each order is confirmed with an updated quote.', 'Prezzi End-User IVA esclusa, spedizione e dazio in Italia inclusi. Ogni ordine si conferma con un preventivo aggiornato.')}</p>
{table}
</div></section>
<section class="section" style="padding-top:0"><div class="container">
<h2>{T(f'Which Unitree {name} should I choose?', f'Quale Unitree {name} scegliere')}</h2>
<div class="hm-choose">{choose}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
<h2>{T(f'Unitree {name} official specifications', f'Specifiche ufficiali Unitree {name}')}</h2>
<div class="hm-specs">{specs}</div>
</div></section>
{acc_html}
<section class="section section-cta"><div class="container" style="text-align:center">
<h2>{T(f'Get a quote for the Unitree {name}', f"Preventivo per l'Unitree {name}")}</h2>
<p>{T('Tell us what you need it for: we suggest the right version, accessories and financing options.', 'Raccontaci a cosa ti serve: ti indichiamo versione, accessori e possibilità di finanziamento.')}</p>
<p style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:20px"><a class="btn btn-primary" href="{cta_assess}">{T('Find the right model', 'Trova il modello giusto')}</a><a class="btn btn-secondary" href="{CAL}" target="_blank" rel="noopener noreferrer">{T('Book a call', 'Prenota una chiamata')}</a></p>
</div></section>
<section class="section hm-faq" id="faq"><div class="container"><h2>{T('Frequently asked questions', 'Domande frequenti')}</h2>{faq_html}</div></section>
<section class="section hm-src" style="padding-top:0"><div class="container"><h2>{T('Sources', 'Fonti')}</h2><ul>{sources}<li><a href="{pre}listini/pubblico/end-user.json">{T('Abra Robotics public end-user price list', 'Listino pubblico End-User Abra Robotics')}</a></li></ul></div></section>
"""
    tail = f'\n<script defer src="{pre}script.js"></script>\n</body>\n</html>\n'
    return "<!-- generato da scripts/genera_hub_modelli.py -->\n" + head + body + main + footer + tail


def add_hreflang(it_page: str, en_page: str) -> None:
    """Pagine IT esistenti (as2, h2, g1-d): hreflang verso la nuova pagina EN."""
    p = ROOT / it_page
    s = p.read_text(encoding="utf-8")
    url_it, url_en = f"{SITE}/{it_page}", f"{SITE}/{en_page}"
    s = re.sub(r'\s*<link[^>]*hreflang="(it|en|x-default)"[^>]*>', "", s)
    links = (f'\n<link rel="alternate" hreflang="it" href="{url_it}"/>\n<link rel="alternate" hreflang="en" href="{url_en}"/>\n'
             f'<link rel="alternate" hreflang="x-default" href="{url_it}"/>')
    s = re.sub(r"(</title>)", r"\1" + links.replace("\\", "\\\\"), s, count=1)
    p.write_text(s, encoding="utf-8")


def link_row(page_path: str, en: bool, keys: list[str]) -> None:
    """Riga "Famiglie Unitree" dopo l'hero delle pagine categoria (tra marcatori, idempotente)."""
    p = ROOT / page_path
    s = p.read_text(encoding="utf-8")
    links = "".join(
        f'<a href="{(FAMILIES[k]["en_page"].split("/", 1)[1]) if en else FAMILIES[k]["it_page"]}">Unitree {html.escape(FAMILIES[k].get("name_en", FAMILIES[k]["name"]) if en else FAMILIES[k]["name"])}</a>'
        for k in keys)
    block = (f'<!-- HUB:MODELLI -->\n<section class="section" style="padding:8px 0 0"><div class="container">'
             f'<p class="label">{"Unitree families: prices and versions" if en else "Famiglie Unitree: prezzi e versioni"}</p>'
             f'<div class="hm-fam" style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div></section>\n<!-- /HUB:MODELLI -->')
    block = block.replace('<a href', '<a style="padding:6px 12px;border:1px solid var(--gray-200);border-radius:999px;color:var(--black);text-decoration:none;font-size:.9rem" href')
    if "<!-- HUB:MODELLI -->" in s:
        s = re.sub(r"<!-- HUB:MODELLI -->[\s\S]*?<!-- /HUB:MODELLI -->", lambda m: block, s)
    else:
        i = s.index('<section class="collection-hero">')
        j = s.index("</section>", i) + len("</section>")
        s = s[:j] + "\n" + block + s[j:]
    p.write_text(s, encoding="utf-8")


def main() -> None:
    data = load()
    written = []
    for key, f in FAMILIES.items():
        if not f.get("en_only"):
            (ROOT / f["it_page"]).write_text(page(key, f, data[key], en=False), encoding="utf-8")
            written.append(f["it_page"])
        (ROOT / f["en_page"]).write_text(page(key, f, data[key], en=True), encoding="utf-8")
        written.append(f["en_page"])
        if f.get("en_only"):
            add_hreflang(f["it_page"], f["en_page"])
    link_row("umanoidi.html", False, ["g1", "g1-d", "h2", "r1"])
    link_row("quadrupedi.html", False, ["go2", "as2", "a2", "b2"])
    link_row("accessori.html", False, ["z1"])
    link_row("en/umanoidi-en.html", True, ["g1", "g1-d", "h2", "r1"])
    link_row("en/quadrupedi-en.html", True, ["go2", "as2", "a2", "b2"])
    for k, f in FAMILIES.items():
        print(f"{k:5s} robot {len(data[k]['robots']):3d} accessori {len(data[k]['acc']):3d}")
    print("scritte:", " ".join(written))


if __name__ == "__main__":
    main()
