#!/usr/bin/env python3
"""Pagina categoria quadrupedi (IT + EN): contenuti SEO generati qui, prezzi dal listino pubblico.

Fonte unica per:
- title / meta description / og:title / og:description
- hero (H1 + intro), tabella "prezzi e specifiche" per famiglia, "quale scegliere", guide
- FAQ visibili + FAQPage JSON-LD (stesso testo), ItemList JSON-LD
- prezzi sulle card prodotto (da listini/pubblico/end-user.json, IVA esclusa)

Specifiche: SOLO dati ufficiali unitree.com (go2, As2, A2, b2, go2-w, b2-w), verificati 2026-10.
Navbar, footer, form, script e consenso NON vengono toccati.
Idempotente (blocchi tra marcatori <!-- QUAD:... -->). Uso: python3 scripts/seo_quadrupedi.py
Nota: genera_hub_modelli.py gestisce il blocco <!-- HUB:MODELLI --> (lasciato intatto).
"""
from __future__ import annotations

import html as H
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRICES = json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8"))
SITE = "https://abrarobotics.com"


def p(key: str) -> float:
    return float(PRICES[key]["prezzo_eur"])


def eur_it(v: float) -> str:
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return (s[:-3] if s.endswith(",00") else s) + " €"


def eur_en(v: float) -> str:
    s = f"{v:,.2f}"
    return "€" + (s[:-3] if s.endswith(".00") else s)


def eur_card_it(v: float) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def strip_tags(s: str) -> str:
    return H.unescape(re.sub(r"<[^>]+>", "", s))


# --- Righe tabella: (famiglia, nome, chiavi listino, "da"?, hub, scheda, specifiche IT, specifiche EN) ---
# specifiche: peso, velocita', carico in camminata, autonomia senza carico, protezione, ideale per
ROWS = [
    ("go2", "Go2 Air", ["GO2-AIR"], "unitree-go2-air.html",
     ("~15 kg", "2,5 m/s", "≈7 kg", "1–2 h", "—", "Primo approccio, eventi"),
     ("~15 kg", "2.5 m/s", "≈7 kg", "1–2 h", "—", "Getting started, events")),
    ("go2", "Go2 Pro", ["GO2-PRO"], "unitree-go2-pro.html",
     ("~15 kg", "3,5 m/s", "≈8 kg", "1–2 h", "—", "Demo avanzate, marketing"),
     ("~15 kg", "3.5 m/s", "≈8 kg", "1–2 h", "—", "Advanced demos, marketing")),
    ("go2", "Go2 EDU (Standard → Ultimate)", ["GO2-EDU-STD", "GO2-EDU-SMART", "GO2-EDU-LASER", "GO2-EDU-ULT"], "unitree-go2-edu.html",
     ("~15 kg", "3,7 m/s (max ~5)", "≈8 kg (max ~12)", "2–4 h", "—", "Ricerca, didattica, SDK"),
     ("~15 kg", "3.7 m/s (max ~5)", "≈8 kg (max ~12)", "2–4 h", "—", "Research, education, SDK")),
    ("go2", "Go2-W (ruote)", ["GO2W-STD", "GO2W-U2", "GO2W-U3", "GO2W-U4", "GO2W-U5"], "unitree-go2w-u2.html",
     ("~18 kg", "2,5 m/s", "≈8 kg (max ~12)", "1,5–3 h", "—", "Percorsi lunghi su superfici piane"),
     ("~18 kg", "2.5 m/s", "≈8 kg (max ~12)", "1.5–3 h", "—", "Long routes on flat ground")),
    ("as2", "AS2 Air", ["AS2-AIR"], "unitree-as2-air.html",
     ("~20 kg", "3,0 m/s", "~10 kg", "~2 h", "non dichiarata", "Demo, POC a basso costo"),
     ("~20 kg", "3.0 m/s", "~10 kg", "~2 h", "not declared", "Demos, low-cost POC")),
    ("as2", "AS2-X", ["AS2-X"], "unitree-as2-x.html",
     ("~20 kg", "3,7 m/s (fino a ~5)", "~15 kg", "~4 h", "IP54", "Ispezione leggera, sviluppo"),
     ("~20 kg", "3.7 m/s (up to ~5)", "~15 kg", "~4 h", "IP54", "Light inspection, development")),
    ("as2", "AS2 EDU (U1–U4)", ["AS2-EDU", "AS2-EDU-SMART", "AS2-EDU-LASER", "AS2-EDU-ULT"], "unitree-as2-edu.html",
     ("~20 kg", "3,7 m/s (fino a ~5)", "~15 kg", "~4 h", "IP54", "Università, laboratori, ROS 2"),
     ("~20 kg", "3.7 m/s (up to ~5)", "~15 kg", "~4 h", "IP54", "Universities, labs, ROS 2")),
    ("as2", "AS2 Pro", ["AS2-PRO"], "unitree-as2-pro.html",
     ("~20 kg", "3,7 m/s", "~13 kg", "~4 h", "IP54", "Sorveglianza, ispezione indoor"),
     ("~20 kg", "3.7 m/s", "~13 kg", "~4 h", "IP54", "Surveillance, indoor inspection")),
    ("as2", "AS2-W (ruote)", ["AS2W-X", "AS2W-EDU-STD", "AS2W-EDU-SMART", "AS2W-EDU-PLUS", "AS2W-EDU-ULT"], "unitree-as2-w.html",
     ("—", "—", "—", "—", "—", "Versione con ruote dell'AS2"),
     ("—", "—", "—", "—", "—", "Wheeled AS2 version")),
    ("a2", "A2", ["A2-STD"], "unitree-a2.html",
     ("~42 kg", "3,7 m/s (fino a ~5)", "~25 kg", ">5 h (~20 km)", "IP56", "Ispezione impianti, trasporto"),
     ("~42 kg", "3.7 m/s (up to ~5)", "~25 kg", ">5 h (~20 km)", "IP56", "Plant inspection, transport")),
    ("a2", "A2 Pro", ["A2-PRO"], "unitree-a2-pro.html",
     ("~42 kg", "3,7 m/s (fino a ~5)", "~25 kg", ">5 h (~20 km)", "IP56–IP67", "Ambienti gravosi, 2 LiDAR"),
     ("~42 kg", "3.7 m/s (up to ~5)", "~25 kg", ">5 h (~20 km)", "IP56–IP67", "Harsh sites, 2 LiDARs")),
    ("a2", "A2-W (ruote)", ["A2W-STD", "A2W-PRO"], "unitree-a2w-std.html",
     ("—", "—", "—", "—", "—", "Lunghe distanze in impianto"),
     ("—", "—", "—", "—", "—", "Long distances on site")),
    ("b2", "B2", ["B2", "B2-LIDAR"], "unitree-b2.html",
     ("~60 kg", ">6 m/s*", ">40 kg", ">5 h (>20 km)", "IP67", "Outdoor, carichi pesanti"),
     ("~60 kg", ">6 m/s*", ">40 kg", ">5 h (>20 km)", "IP67", "Outdoor, heavy payloads")),
    ("b2", "B2-W (ruote)", ["B2W", "B2W-LIDAR"], "unitree-b2w.html",
     ("~85 kg", "15 km/h*", ">40 kg", "~30 km", "IP67", "Pattugliamento su grandi aree"),
     ("~85 kg", "15 km/h*", ">40 kg", "~30 km", "IP67", "Patrols over large areas")),
]

HUB = {"go2": ("go2.html", "Unitree Go2"), "as2": ("as2.html", "Unitree AS2"),
       "a2": ("a2.html", "Unitree A2"), "b2": ("b2.html", "Unitree B2")}

MIN = min(p(k) for r in ROWS for k in r[2])
MAX = max(p(k) for r in ROWS for k in r[2])


def rel(path: str, en: bool) -> str:
    """Link relativo; in EN usa la versione -en se esiste."""
    if not en:
        return path
    cand = path.replace(".html", "-en.html")
    if path in {k for k, _ in HUB.values()}:
        return cand  # en/go2-en.html ecc.
    if (ROOT / cand).exists():
        return "../" + cand
    return "../" + path


def table(en: bool) -> str:
    th = (["Model", "Price from (excl. VAT)", "Weight", "Max speed", "Walking payload", "Endurance (unloaded)", "Protection", "Best for"]
          if en else ["Modello", "Prezzo da (IVA escl.)", "Peso", "Velocità max", "Carico in camminata", "Autonomia (senza carico)", "Protezione", "Ideale per"])
    out = ['<div class="matrix-wrap"><table class="matrix q-table">',
           "<caption class=\"q-caption\">" + ("Unitree quadruped robots: list prices and official specs" if en else "Robot quadrupedi Unitree: prezzi a listino e specifiche ufficiali") + "</caption>",
           "<thead><tr>" + "".join(f'<th scope="col">{h}</th>' for h in th) + "</tr></thead><tbody>"]
    fam_prev = None
    for fam, name, keys, slug, s_it, s_en in ROWS:
        if fam != fam_prev:
            hub, label = HUB[fam]
            out.append(f'<tr class="q-fam"><td colspan="8"><a href="{rel(hub, en)}">{label}</a> — '
                       + ("all versions and prices →" if en else "tutte le versioni e i prezzi →") + "</td></tr>")
            fam_prev = fam
        lo = min(p(k) for k in keys)
        price = (eur_en(lo) if en else eur_it(lo))
        if len(keys) > 1:
            price = ("from " if en else "da ") + price
        s = s_en if en else s_it
        if en:
            name = name.replace("(ruote)", "(wheeled)")
        out.append(f'<tr><th scope="row"><a href="{rel("prodotti/" + slug, en)}">Unitree {name}</a></th>'
                   f'<td><strong>{price}</strong></td>' + "".join(f"<td>{H.escape(x)}</td>" for x in s) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def faq_html(faqs: list[tuple[str, str]], en: bool) -> str:
    items = "".join(f'<details class="seo-faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    h2 = "Quadruped robot FAQ" if en else "Domande frequenti sui robot quadrupedi"
    lab = "Frequently asked questions" if en else "Domande frequenti"
    return (f'<section class="section seo-faq" id="faq" aria-label="{lab}"><div class="container">'
            f'<h2>{h2}</h2>{items}</div></section>')


def faq_jsonld(faqs: list[tuple[str, str]]) -> str:
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs]}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>"


def itemlist_jsonld(en: bool) -> str:
    page = f"{SITE}/en/quadrupedi-en.html" if en else f"{SITE}/quadrupedi.html"
    items = []
    for fam in ("go2", "as2", "a2", "b2"):
        keys = [k for r in ROWS if r[0] == fam for k in r[2]]
        hub, label = HUB[fam]
        url = f"{SITE}/en/{hub.replace('.html', '-en.html')}" if en else f"{SITE}/{hub}"
        items.append({"@type": "ListItem", "position": len(items) + 1, "item": {
            "@type": "Product", "name": label, "url": url, "brand": {"@type": "Brand", "name": "Unitree"},
            "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                       "lowPrice": f"{min(p(k) for k in keys):.2f}", "highPrice": f"{max(p(k) for k in keys):.2f}",
                       "offerCount": len(keys),
                       "seller": {"@type": "Organization", "name": "Abra Robotics", "url": SITE}}}})
    data = {"@context": "https://schema.org", "@type": "CollectionPage",
            "name": "Unitree quadruped robots: prices and models" if en else "Robot quadrupedi Unitree: prezzi e modelli",
            "url": page, "inLanguage": "en" if en else "it",
            "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": items}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/en/index-en.html" if en else f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Quadruped robots" if en else "Robot quadrupedi", "item": page}]}
    return ("<!-- itemlist-schema -->\n<script type=\"application/ld+json\">\n" + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n<script type=\"application/ld+json\">\n" + json.dumps(crumbs, ensure_ascii=False, indent=2) + "\n</script>\n")


CSS = """
    /* QUAD:CSS — tabella prezzi, quale scegliere, guide (scripts/seo_quadrupedi.py) */
    .q-table { min-width: 980px; }
    .q-table thead th { background: var(--black); color:#fff; font-size:0.7rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; padding:14px 16px; text-align:center; }
    .q-table thead th:first-child, .q-table tbody th { text-align:left; }
    .q-table tbody th { padding:12px 16px; font-size:0.9rem; border-bottom:1px solid var(--gray-100); white-space:nowrap; }
    .q-table tbody th a { color:var(--black); font-weight:700; text-decoration:none; }
    .q-table tbody th a:hover { text-decoration:underline; }
    .q-table tr.q-fam td { text-align:left; background:var(--gray-50, #fafafa); font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.06em; }
    .q-table tr.q-fam a { color:var(--black); }
    .q-table tbody td:nth-child(2), .q-table tbody td:nth-child(3) { white-space:nowrap; }
    .q-caption { caption-side: top; text-align:left; padding:12px 16px; font-size:0.85rem; color:var(--gray-600); }
    .q-note { font-size:0.82rem; color:var(--gray-600); margin-top:12px; }
    .q-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:20px; }
    .q-card { border:1px solid var(--gray-200); border-radius:var(--radius); padding:24px; background:var(--white); }
    .q-card h3 { margin:0 0 8px; font-size:1.1rem; }
    .q-card p { margin:0 0 10px; color:var(--gray-700); font-size:0.95rem; }
    .q-card a { color:var(--black); font-weight:700; }
    .q-links { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; padding:0; list-style:none; }
    .q-links a { display:block; padding:14px 18px; border:1px solid var(--gray-200); border-radius:var(--radius); color:var(--black); text-decoration:none; font-weight:700; }
    .q-links a span { display:block; font-weight:400; font-size:0.85rem; color:var(--gray-600); margin-top:4px; }
    .q-links a:hover { border-color:var(--gray-400); }
    @media (max-width: 900px) { .q-grid, .q-links { grid-template-columns:1fr; } }
    /* /QUAD:CSS */
"""

# ---------------------------------------------------------------- IT
def it_content() -> dict:
    title = "Robot quadrupede Unitree: prezzi e modelli in Italia | Abra"
    desc = (f"Robot quadrupede (cane robot) Unitree: prezzi da {eur_it(MIN)} IVA esclusa, confronto Go2, AS2, A2 e B2 "
            "e quale scegliere per ricerca, ispezione e outdoor.")
    hero = f"""<section class="collection-hero">
<div class="container">
<p class="label">Robot quadrupedi · cane robot</p>
<h1>Robot quadrupede Unitree: modelli, prezzi e quale scegliere</h1>
<p class="lead">Un <strong>robot quadrupede</strong> (o <strong>cane robot</strong>) è un robot mobile a quattro zampe che cammina dove ruote e cingoli si fermano: scale, grigliati, terreni sconnessi. In Italia i quadrupedi Unitree costano da <strong>{eur_it(p("GO2-AIR"))}</strong> (Go2 Air) a oltre <strong>{eur_it(MAX // 10000 * 10000)}</strong> (B2-W con LiDAR), IVA esclusa, con spedizione e dazio inclusi. Abra Robotics è parte della filiera Unitree Italia: qui trovi i prezzi pubblici di <a href="go2.html">Go2</a>, <a href="as2.html">AS2</a>, <a href="a2.html">A2</a> e <a href="b2.html">B2</a>, le specifiche ufficiali e il modello giusto per ricerca, ispezione, sicurezza e outdoor.</p>
<div class="hero-meta">
<div><strong>4</strong><span>Famiglie: Go2, AS2, A2, B2</span></div>
<div><strong>da {eur_it(MIN)}</strong><span>IVA esclusa</span></div>
<div><strong>IP67</strong><span>Fino a (A2 Pro / B2)</span></div>
<div><strong>Italia</strong><span>Filiera Unitree Italia</span></div>
</div>
</div>
</section>"""
    body = f"""<!-- QUAD:CONTENUTI -->
<section class="section" id="prezzi" style="padding-top:40px;">
<div class="container">
<div class="section-header" style="text-align:left;max-width:100%;">
<p class="label">Confronto</p>
<h2>Prezzi robot quadrupede Unitree e specifiche a confronto</h2>
<p class="section-sub" style="margin-left:0;">Prezzi End-User a listino, IVA esclusa, spedizione e dazio in Italia inclusi; ogni ordine si conferma con un preventivo aggiornato. Specifiche dai dati ufficiali Unitree (<a href="https://www.unitree.com/go2/" rel="noopener" target="_blank">Go2</a>, <a href="https://www.unitree.com/As2/" rel="noopener" target="_blank">AS2</a>, <a href="https://www.unitree.com/A2/" rel="noopener" target="_blank">A2</a>, <a href="https://www.unitree.com/b2/" rel="noopener" target="_blank">B2</a>), misurate in laboratorio. Su mobile scorri la tabella in orizzontale.</p>
</div>
{table(False)}
<p class="q-note">* Velocità massima solo in configurazioni speciali; le unità di serie hanno un limite di velocità di sicurezza. «—» = dato non pubblicato da Unitree per quella versione: vedi la scheda. Listino completo con accessori: <a href="listino-unitree.html">listino prezzi Unitree</a>.</p>
</div>
</section>
<section class="section" id="quale-scegliere" style="padding-top:24px;">
<div class="container">
<div class="section-header" style="text-align:left;max-width:100%;">
<p class="label">Guida alla scelta</p>
<h2>Quale robot quadrupede scegliere</h2>
<p class="section-sub" style="margin-left:0;">La scelta dipende da ambiente, carico, autonomia e da quanto serve programmare il robot. Quattro casi tipici:</p>
</div>
<div class="q-grid">
<div class="q-card"><h3>Ricerca e didattica</h3><p>Per università, laboratori e ITS servono SDK aperto e ROS 2: <a href="go2.html">Go2 EDU</a> (da {eur_it(p("GO2-EDU-STD"))}) è la piattaforma più diffusa; <a href="as2.html">AS2 EDU</a> (da {eur_it(p("AS2-EDU"))}) aggiunge carico di ~15 kg, ~4 h di autonomia e IP54. Per iniziare con un budget ridotto: AS2 Air ({eur_it(p("AS2-AIR"))}).</p><p>Approfondisci: <a href="blog/unitree-go2-vs-go2-pro.html">Go2 vs Go2 Pro ed EDU</a> · <a href="universita-ricerca.html">Università e ricerca</a></p></div>
<div class="q-card"><h3>Ispezioni industriali</h3><p>Giri di ispezione in impianti, cabine e capannoni: <a href="as2.html">AS2 Pro / AS2-X</a> per ambienti indoor (IP54, ~4 h); <a href="a2.html">A2</a> (da {eur_it(p("A2-STD"))}) quando servono più carico (~25 kg), oltre 5 ore di autonomia e IP56; A2 Pro con due LiDAR e componenti IP67 per ambienti gravosi.</p><p>Approfondisci: <a href="blog/robot-quadrupede-ispezione-industriale.html">quadrupede per ispezione industriale</a></p></div>
<div class="q-card"><h3>Sicurezza e sorveglianza</h3><p>Pattugliamenti programmati e verifica di allarmi: AS2 Pro per aree coperte; <a href="a2.html">A2</a> e A2-W per perimetri lunghi; <a href="b2.html">B2-W</a> (con ruote, fino a ~30 km senza carico) per grandi aree esterne. Il quadrupede affianca, non sostituisce, il personale di vigilanza.</p></div>
<div class="q-card"><h3>Outdoor e carichi pesanti</h3><p>Cantieri, terreni sconnessi, pioggia e polvere: <a href="b2.html">B2</a> (da {eur_it(p("B2"))}) porta oltre 40 kg in camminata, è IP67 e sale scale fino a 40 cm in avanti. Per attività leggere all'aperto basta spesso un A2. Serve un braccio? Il <a href="z1.html">braccio Unitree Z1</a> si monta anche su quadrupede.</p></div>
</div>
<p class="q-note">Non solo Unitree: tra i quadrupedi industriali esistono anche Boston Dynamics Spot (<a href="https://bostondynamics.com/products/spot/" rel="noopener" target="_blank">bostondynamics.com</a>) e ANYbotics ANYmal (<a href="https://www.anybotics.com/" rel="noopener" target="_blank">anybotics.com</a>), con posizionamento e prezzi diversi: confrontali sulle fonti ufficiali. Abra fornisce la gamma Unitree.</p>
</div>
</section>
<section class="section" id="guide" style="padding-top:24px;">
<div class="container">
<div class="section-header" style="text-align:left;max-width:100%;">
<p class="label">Approfondimenti</p>
<h2>Guide sui cani robot</h2>
</div>
<ul class="q-links">
<li><a href="blog/cane-robot-prezzo.html">Cane robot: prezzi e modelli<span>Quanto costa un cane robot in Italia, versione per versione</span></a></li>
<li><a href="blog/robot-quadrupede-ispezione-industriale.html">Quadrupede per ispezione industriale<span>AS2, A2, B2 e Go2 a confronto sul campo</span></a></li>
<li><a href="blog/unitree-go2-vs-go2-pro.html">Unitree Go2 vs Go2 Pro ed EDU<span>Differenze e come scegliere la versione</span></a></li>
<li><a href="blog/unitree-as2-italia.html">Unitree AS2 in Italia<span>Modelli, prezzi e uso in ricerca</span></a></li>
</ul>
</div>
</section>
<!-- /QUAD:CONTENUTI -->"""
    faqs = [
        ("Cos'è un robot quadrupede?",
         "Un robot quadrupede, detto anche cane robot, è un robot mobile a quattro zampe che si muove su scale, terreni sconnessi e ostacoli dove robot a ruote o cingoli faticano. Si usa per ispezioni, sorveglianza, ricerca, didattica e trasporto di piccoli carichi."),
        ("Quanto costa un robot quadrupede Unitree?",
         f"A listino in Italia, IVA esclusa e con spedizione e dazio inclusi: Go2 Air {eur_it(p('GO2-AIR'))}, AS2 Air {eur_it(p('AS2-AIR'))}, Go2 EDU da {eur_it(p('GO2-EDU-STD'))}, A2 da {eur_it(p('A2-STD'))}, B2 da {eur_it(p('B2'))}; la configurazione più completa (B2-W con LiDAR) costa {eur_it(p('B2W-LIDAR'))}. Ogni ordine si conferma con un preventivo aggiornato."),
        ("Che differenza c'è tra Unitree Go2 e AS2?",
         "L'AS2 è il quadrupede Unitree di nuova generazione, più grande del Go2 (circa 20 kg contro 15 kg): porta fino a circa 15 kg in camminata, arriva a circa 4 ore di autonomia e le versioni Pro, X ed EDU sono IP54. Il Go2 resta la scelta più compatta ed economica."),
        ("Quale robot quadrupede scegliere per ispezioni industriali?",
         "Per ispezioni indoor bastano spesso AS2 Pro o AS2-X (IP54, circa 4 ore). Per impianti più estesi o ambienti gravosi serve un A2 (IP56, oltre 5 ore, circa 25 kg di carico) o un A2 Pro con componenti IP67. Il B2 è indicato per outdoor e carichi oltre 40 kg."),
        ("Un robot quadrupede può salire le scale?",
         "Sì, entro i limiti dichiarati da Unitree: l'AS2 sale gradini fino a 25 cm (20 cm la versione Air), l'A2 supera gradini fino a 30 cm e il B2 sale scale continue di 20–25 cm e gradini fino a 40 cm in avanti. Dati di laboratorio: le prestazioni reali dipendono dal terreno."),
        ("Si può montare un braccio robotico su un quadrupede Unitree?",
         "Sì: il braccio Unitree Z1, a 6 assi, è pensato anche per il montaggio su quadrupede, per aprire porte, azionare valvole o manipolare piccoli oggetti. Prezzi e versioni nella pagina dei bracci Z1 e D1."),
        ("Ci sono incentivi per acquistare un robot quadrupede?",
         "Dipende dal progetto e dall'azienda: verifichiamo caso per caso iperammortamento, Nuova Sabatini e bandi regionali, senza garantire l'ammissibilità. Trovi i dettagli nella pagina Finanziamenti."),
    ]
    faqs_visible = list(faqs)
    faqs_visible[5] = (faqs[5][0], faqs[5][1].replace("pagina dei bracci Z1 e D1", '<a href="z1.html">pagina dei bracci Z1 e D1</a>'))
    faqs_visible[6] = (faqs[6][0], faqs[6][1].replace("pagina Finanziamenti", '<a href="finanziamenti.html">pagina Finanziamenti</a>'))
    return dict(title=title, desc=desc, hero=hero, body=body, faqs=faqs, faqs_visible=faqs_visible)


# ---------------------------------------------------------------- EN
def en_content() -> dict:
    title = "Quadruped robot price: Unitree Go2, AS2, A2, B2 | Abra"
    desc = (f"Unitree quadruped robot prices in Italy from {eur_en(MIN)} excl. VAT: compare Go2, AS2, A2 and B2 "
            "specs and pick the right robot dog for research or inspection.")
    hero = f"""<section class="collection-hero">
<div class="container">
<p class="label">Quadruped robots · robot dogs</p>
<h1>Unitree quadruped robots: models, prices and how to choose</h1>
<p class="lead">A <strong>quadruped robot</strong> (or <strong>robot dog</strong>) is a four-legged mobile robot that walks where wheels and tracks stop: stairs, gratings, rough ground. In Italy, Unitree quadrupeds range from <strong>{eur_en(p("GO2-AIR"))}</strong> (Go2 Air) to over <strong>{eur_en(MAX // 10000 * 10000)}</strong> (B2-W with LiDAR), excluding VAT, with shipping and duty to Italy included. Abra Robotics is part of the Unitree Italy distribution chain: here are the public prices of <a href="go2-en.html">Go2</a>, <a href="as2-en.html">AS2</a>, <a href="a2-en.html">A2</a> and <a href="b2-en.html">B2</a>, official specs and the right model for research, inspection, security and outdoor work.</p>
<div class="hero-meta">
<div><strong>4</strong><span>Families: Go2, AS2, A2, B2</span></div>
<div><strong>from {eur_en(MIN)}</strong><span>Excl. VAT</span></div>
<div><strong>IP67</strong><span>Up to (A2 Pro / B2)</span></div>
<div><strong>Italy</strong><span>Unitree Italy distribution chain</span></div>
</div>
</div>
</section>"""
    body = f"""<!-- QUAD:CONTENUTI -->
<section class="section" id="prices" style="padding-top:40px;">
<div class="container">
<div class="section-header" style="text-align:left;max-width:100%;">
<p class="label">Comparison</p>
<h2>Unitree quadruped robot prices and specs compared</h2>
<p class="section-sub" style="margin-left:0;">End-user list prices, excluding VAT, shipping and duty to Italy included; every order is confirmed with an updated quote. Specs from official Unitree data (<a href="https://www.unitree.com/go2/" rel="noopener" target="_blank">Go2</a>, <a href="https://www.unitree.com/As2/" rel="noopener" target="_blank">AS2</a>, <a href="https://www.unitree.com/A2/" rel="noopener" target="_blank">A2</a>, <a href="https://www.unitree.com/b2/" rel="noopener" target="_blank">B2</a>), measured in lab conditions. On mobile, scroll the table horizontally.</p>
</div>
{table(True)}
<p class="q-note">* Top speed only in special configurations; production units have a safety speed limit. "—" = not published by Unitree for that version: see the product page. Full price list with accessories: <a href="listino-unitree-en.html">Unitree price list</a>.</p>
</div>
</section>
<section class="section" id="which-to-choose" style="padding-top:24px;">
<div class="container">
<div class="section-header" style="text-align:left;max-width:100%;">
<p class="label">Buying guide</p>
<h2>Which quadruped robot should you choose?</h2>
<p class="section-sub" style="margin-left:0;">It depends on environment, payload, endurance and how much you need to program the robot. Four typical cases:</p>
</div>
<div class="q-grid">
<div class="q-card"><h3>Research and education</h3><p>Universities and labs need an open SDK and ROS 2: <a href="go2-en.html">Go2 EDU</a> (from {eur_en(p("GO2-EDU-STD"))}) is the most widespread platform; <a href="as2-en.html">AS2 EDU</a> (from {eur_en(p("AS2-EDU"))}) adds ~15 kg payload, ~4 h endurance and IP54. On a tight budget: AS2 Air ({eur_en(p("AS2-AIR"))}).</p><p>See also: <a href="universita-ricerca-en.html">Universities and research</a></p></div>
<div class="q-card"><h3>Industrial inspection</h3><p>Inspection rounds in plants, substations and warehouses: <a href="as2-en.html">AS2 Pro / AS2-X</a> indoors (IP54, ~4 h); <a href="a2-en.html">A2</a> (from {eur_en(p("A2-STD"))}) when you need more payload (~25 kg), 5+ hours and IP56; A2 Pro with two LiDARs and IP67 core components for harsh sites.</p><p>Guide (Italian): <a href="../blog/robot-quadrupede-ispezione-industriale.html" hreflang="it">quadruped for industrial inspection</a></p></div>
<div class="q-card"><h3>Security and surveillance</h3><p>Scheduled patrols and alarm checks: AS2 Pro for covered areas; <a href="a2-en.html">A2</a> and A2-W for long perimeters; <a href="b2-en.html">B2-W</a> (wheeled, ~30 km unloaded) for large outdoor areas. A quadruped supports security staff rather than replacing them.</p></div>
<div class="q-card"><h3>Outdoor and heavy payloads</h3><p>Construction sites, rough terrain, rain and dust: <a href="b2-en.html">B2</a> (from {eur_en(p("B2"))}) carries over 40 kg while walking, is IP67 and climbs steps up to 40 cm forward. For lighter outdoor tasks an A2 is often enough. Need an arm? The <a href="z1-en.html">Unitree Z1 arm</a> can also be mounted on a quadruped.</p></div>
</div>
<p class="q-note">Beyond Unitree, industrial quadrupeds include Boston Dynamics Spot (<a href="https://bostondynamics.com/products/spot/" rel="noopener" target="_blank">bostondynamics.com</a>) and ANYbotics ANYmal (<a href="https://www.anybotics.com/" rel="noopener" target="_blank">anybotics.com</a>), with different positioning and pricing: compare them on their official sources. Abra supplies the Unitree range.</p>
</div>
</section>
<section class="section" id="guides" style="padding-top:24px;">
<div class="container">
<div class="section-header" style="text-align:left;max-width:100%;">
<p class="label">Further reading</p>
<h2>Robot dog guides (in Italian)</h2>
</div>
<ul class="q-links">
<li><a href="../blog/cane-robot-prezzo.html" hreflang="it">Robot dog prices and models<span>How much a robot dog costs in Italy, version by version</span></a></li>
<li><a href="../blog/robot-quadrupede-ispezione-industriale.html" hreflang="it">Quadruped for industrial inspection<span>AS2, A2, B2 and Go2 compared in the field</span></a></li>
<li><a href="../blog/unitree-go2-vs-go2-pro.html" hreflang="it">Unitree Go2 vs Go2 Pro and EDU<span>Differences and how to choose</span></a></li>
<li><a href="../blog/unitree-as2-italia.html" hreflang="it">Unitree AS2 in Italy<span>Models, prices and research use</span></a></li>
</ul>
</div>
</section>
<!-- /QUAD:CONTENUTI -->"""
    faqs = [
        ("What is a quadruped robot?",
         "A quadruped robot, also called a robot dog, is a four-legged mobile robot that handles stairs, rough ground and obstacles where wheeled or tracked robots struggle. It is used for inspection, surveillance, research, education and carrying small payloads."),
        ("How much does a Unitree quadruped robot cost?",
         f"List prices in Italy, excluding VAT, shipping and duty included: Go2 Air {eur_en(p('GO2-AIR'))}, AS2 Air {eur_en(p('AS2-AIR'))}, Go2 EDU from {eur_en(p('GO2-EDU-STD'))}, A2 from {eur_en(p('A2-STD'))}, B2 from {eur_en(p('B2'))}; the most complete configuration (B2-W with LiDAR) is {eur_en(p('B2W-LIDAR'))}. Every order is confirmed with an updated quote."),
        ("What is the difference between Unitree Go2 and AS2?",
         "The AS2 is Unitree's new-generation quadruped, larger than the Go2 (about 20 kg vs 15 kg): it carries up to about 15 kg while walking, reaches about 4 hours of endurance and the Pro, X and EDU versions are IP54. The Go2 remains the most compact and affordable option."),
        ("Which quadruped robot is best for industrial inspection?",
         "For indoor inspection, AS2 Pro or AS2-X (IP54, about 4 hours) are often enough. Larger plants or harsh environments call for an A2 (IP56, 5+ hours, about 25 kg payload) or an A2 Pro with IP67 core components. The B2 suits outdoor work and payloads above 40 kg."),
        ("Can a quadruped robot climb stairs?",
         "Yes, within Unitree's stated limits: the AS2 climbs steps up to 25 cm (20 cm for the Air), the A2 handles steps up to 30 cm and the B2 climbs continuous 20–25 cm stairs and steps up to 40 cm forward. Lab data: real performance depends on the terrain."),
        ("Can a robot arm be mounted on a Unitree quadruped?",
         "Yes: the 6-axis Unitree Z1 arm is also designed for mounting on a quadruped, to open doors, operate valves or handle small objects. Prices and versions on the Z1 and D1 arms page."),
        ("Do you ship Unitree quadrupeds outside Italy?",
         "We work mainly in Italy, Switzerland and the Balkans; other EU countries on a project basis. Contact us for lead times and a quote."),
    ]
    faqs_visible = list(faqs)
    faqs_visible[5] = (faqs[5][0], faqs[5][1].replace("Z1 and D1 arms page", '<a href="z1-en.html">Z1 and D1 arms page</a>'))
    return dict(title=title, desc=desc, hero=hero, body=body, faqs=faqs, faqs_visible=faqs_visible)


# ---------------------------------------------------------------- patch
def set_meta(t: str, c: dict) -> str:
    t = re.sub(r"<title>.*?</title>", f"<title>{c['title']}</title>", t, count=1, flags=re.S)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{c["desc"]}" name="description"/>', t, count=1)
    t = re.sub(r'<meta property="og:title" content="[^"]*"/>', f'<meta property="og:title" content="{c["title"]}"/>', t, count=1)
    t = re.sub(r'<meta property="og:description" content="[^"]*"/>', f'<meta property="og:description" content="{c["desc"]}"/>', t, count=1)
    return t


FROM_SLUGS = {"unitree-as2-edu.html"}  # card AS2 EDU = U1–U4


def patch_cards(t: str, en: bool) -> str:
    def fix(m: re.Match) -> str:
        a = m.group(0)
        hm = re.search(r'href="(?:\.\./)?prodotti/([^"]+?)(?:-en)?\.html">(?:Vedi|View)', a)
        if not hm:
            return a
        slug = hm.group(1) + ".html"
        row = next((v for v in PRICES.values() if v.get("slug") == slug), None)
        if row is None:
            return a
        v, lst = float(row["prezzo_eur"]), row.get("prezzo_listino_eur")
        fmt = eur_en if en else eur_card_it
        # schede che raggruppano piu' configurazioni: prezzo "da"
        da = ("from " if en else "da ") if row.get("prezzo_da") or slug in FROM_SLUGS else ""
        inner = (f'<s style="font-size:0.72em;font-weight:600;color:#a3a3a3;margin-right:6px;" title="{"List price" if en else "Prezzo di listino"}">{fmt(float(lst))}</s>' if lst and float(lst) > v else "") + da + fmt(v)
        return re.sub(r'(<span style="font-size:1\.05rem;font-weight:900;letter-spacing:-0\.02em;">).*?(</span>\s*<a class="btn)',
                      lambda mm: mm.group(1) + inner + mm.group(2), a, count=1, flags=re.S)
    t = re.sub(r'<article class="robot-card".*?</article>', fix, t, flags=re.S)
    # AS2: immagine corretta (prima era la foto dell'A2 Pro)
    t = re.sub(r'(alt="Unitree AS2[^"]*"[^>]*?src=")(?:\.\./)?images/prodotti/a2-pro\.png"',
               lambda m: m.group(1) + ("../" if en else "") + 'images/prodotti/2026/as2.png"', t)
    return t


def fix_card_specs_it(t: str) -> str:
    """Specifiche Go2 sulle card allineate a unitree.com/go2 (velocita' Pro 3,5 m/s, EDU 3,7 m/s; LiDAR 4D L1)."""
    def go2(m: re.Match) -> str:
        a = m.group(0)
        a = a.replace('<span class="key-spec-value">1,7 m/s</span>', '<span class="key-spec-value">3,5 m/s</span>')
        a = a.replace('<span class="key-spec-value">2 m/s</span>', '<span class="key-spec-value">3,7 m/s</span>')
        a = a.replace("<li><span>LiDAR</span><span>3D L1</span></li>", "<li><span>LiDAR</span><span>4D L1</span></li>")
        a = a.replace("<li><span>LiDAR</span><span>4D L2</span></li>", "<li><span>LiDAR</span><span>4D L1</span></li>")
        a = a.replace("<li><span>LiDAR onboard</span><span>4D L2</span></li>", "<li><span>LiDAR onboard</span><span>4D L1</span></li>")
        return a
    t = re.sub(r'<article class="robot-card" data-family="go2">.*?</article>', go2, t, flags=re.S)
    t = t.replace("<li><span>LiDAR</span><span>32 canali</span></li>", "<li><span>LiDAR</span><span>3D</span></li>")
    return t


def fix_card_specs_en(t: str) -> str:
    def go2(m: re.Match) -> str:
        a = m.group(0)
        a = a.replace('<span class="key-spec-value">1.7 m/s</span>', '<span class="key-spec-value">3.5 m/s</span>')
        a = a.replace('<span class="key-spec-value">2 m/s</span>', '<span class="key-spec-value">3.7 m/s</span>')
        a = re.sub(r"<li><span>LiDAR</span><span>(?:3D L1|4D L2)</span></li>", "<li><span>LiDAR</span><span>4D L1</span></li>", a)
        return a
    t = re.sub(r'<article class="robot-card" data-family="go2">.*?</article>', go2, t, flags=re.S)
    t = t.replace("<li><span>LiDAR</span><span>32 channels</span></li>", "<li><span>LiDAR</span><span>3D</span></li>")
    return t


def patch(path: Path, c: dict, en: bool) -> None:
    t = path.read_text(encoding="utf-8")
    t = set_meta(t, c)
    # CSS nel blocco <style> della pagina
    if "QUAD:CSS" in t:
        t = re.sub(r"\n    /\* QUAD:CSS.*?/\* /QUAD:CSS \*/\n", lambda m: CSS, t, count=1, flags=re.S)
    else:
        t = t.replace("  </style>", CSS + "  </style>", 1)
    # FAQPage JSON-LD in <head>
    t = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
               lambda m: faq_jsonld(c["faqs"]), t, count=1, flags=re.S)
    # hero
    t = re.sub(r'<section class="collection-hero">.*?</section>', lambda m: c["hero"], t, count=1, flags=re.S)
    # vecchia tabella "section-dark" (dati non allineati): sostituita dalla tabella prezzi
    t = re.sub(r'<section class="section section-dark">\s*<div class="container">\s*<div class="section-header"[^>]*>\s*<p class="label label-light">(?:Confronto|Comparison)</p>.*?</section>\n?',
               "", t, count=1, flags=re.S)
    # contenuti nuovi dopo HUB:MODELLI
    if "<!-- QUAD:CONTENUTI -->" in t:
        t = re.sub(r"<!-- QUAD:CONTENUTI -->.*?<!-- /QUAD:CONTENUTI -->", lambda m: c["body"], t, count=1, flags=re.S)
    else:
        t = t.replace("<!-- /HUB:MODELLI -->", "<!-- /HUB:MODELLI -->\n" + c["body"], 1)
    # titolo sezione catalogo card
    if "QUAD:CATALOGO" not in t:
        h = ("<!-- QUAD:CATALOGO --><h2 style=\"margin-bottom:20px;\">All Unitree quadruped versions</h2>" if en
             else "<!-- QUAD:CATALOGO --><h2 style=\"margin-bottom:20px;\">Tutte le versioni dei quadrupedi Unitree</h2>")
        anchor = '<div class="robot-grid">' if en else '<div aria-label="Filtra per famiglia" class="coll-filters">'
        t = t.replace(anchor, h + "\n" + anchor, 1)
    t = patch_cards(t, en)
    t = fix_card_specs_en(t) if en else fix_card_specs_it(t)
    # FAQ visibili
    t = re.sub(r'<section class="section seo-faq" id="faq".*?</section>', lambda m: faq_html(c["faqs_visible"], en), t, count=1, flags=re.S)
    # ItemList + Breadcrumb JSON-LD
    t = re.sub(r'<!-- itemlist-schema -->\s*<script type="application/ld\+json">.*?</script>\s*(?:<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "BreadcrumbList".*?</script>\s*)?',
               lambda m: itemlist_jsonld(en) + "\n", t, count=1, flags=re.S)
    path.write_text(t, encoding="utf-8")
    print("aggiornato", path.relative_to(ROOT))


def main() -> None:
    patch(ROOT / "quadrupedi.html", it_content(), en=False)
    patch(ROOT / "en" / "quadrupedi-en.html", en_content(), en=True)


if __name__ == "__main__":
    main()
