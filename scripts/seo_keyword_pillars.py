#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Optimize pillar pages for high-volume keywords + FAQ schema."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def set_title(html: str, title: str) -> str:
    return re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.I | re.S)


def set_meta_desc(html: str, desc: str) -> str:
    if re.search(r'name=["\']description["\']', html, re.I):
        return re.sub(
            r'<meta\s+(?:name=["\']description["\']\s+content=["\'][^"\']*["\']|content=["\'][^"\']*["\']\s+name=["\']description["\'])\s*/?>',
            f'<meta content="{desc}" name="description"/>',
            html,
            count=1,
            flags=re.I,
        )
    return re.sub(
        r"</title>",
        f'</title>\n<meta content="{desc}" name="description"/>',
        html,
        count=1,
        flags=re.I,
    )


def set_h1(html: str, h1: str) -> str:
    return re.sub(r"<h1([^>]*)>.*?</h1>", rf"<h1\1>{h1}</h1>", html, count=1, flags=re.I | re.S)


def set_lead(html: str, lead: str) -> str:
    return re.sub(
        r'(<p class="lead">).*?(</p>)',
        rf"\1{lead}\2",
        html,
        count=1,
        flags=re.I | re.S,
    )


FAQ_IT_UMANOIDI = [
    (
        "Cos'è un robot umanoide?",
        "Un robot umanoide è un robot bipede con forma antropomorfa, progettato per muoversi e interagire in ambienti pensati per le persone. In Italia Abra Robotics distribuisce la gamma Unitree G1 (Air, EDU, Comp) con listino e supporto locale.",
    ),
    (
        "Quanto costa un Unitree G1 in Italia?",
        "Il Unitree G1 Air parte da circa 22.800 € (IVA esclusa, listino End-User). Le versioni EDU e Comp variano in base a mani, computing Jetson e garanzia. Consulta le schede prodotto o richiedi un preventivo.",
    ),
    (
        "Quale robot umanoide Unitree scegliere?",
        "G1 Air per demo e comunicazione; G1 EDU (U1–U8) per università e R&D con mani e Orin NX; G1 Comp per performance atletiche. Un assessment Abra aiuta a mappare il caso d'uso in 5–9 settimane.",
    ),
    (
        "Abra Robotics è distributore ufficiale Unitree?",
        "Sì: Abra Robotics è supply chain ufficiale Unitree in Italia, con listino pubblico, ricambi, formazione e supporto tecnico.",
    ),
]

FAQ_EN_HUMANOID = [
    (
        "What is a humanoid robot?",
        "A humanoid robot is a bipedal, human-shaped robot designed for human environments. Abra Robotics distributes the Unitree G1 range in Italy with local pricing and support.",
    ),
    (
        "How much does a Unitree G1 cost in Italy?",
        "Unitree G1 Air starts around €22,800 (ex-VAT, End-User list). EDU and Comp variants depend on hands, Jetson compute and warranty. See product pages or request a quote.",
    ),
    (
        "Which Unitree humanoid should I choose?",
        "G1 Air for demos and marketing; G1 EDU for research labs; G1 Comp for athletic performance. Abra can run a short assessment against your use case.",
    ),
]

FAQ_IT_QUAD = [
    (
        "Cos'è un robot quadrupede?",
        "Un robot quadrupede (o robot cane) è una piattaforma mobile a quattro zampe per ispezione, security e logistica su terreni irregolari. Abra distribuisce Unitree Go2, A2 e B2 in Italia.",
    ),
    (
        "Quale Unitree Go2 scegliere?",
        "Go2 Pro per uso generale; Go2 EDU / EDU+ per università e sviluppo; Go2 Enterprise per scenari professionali. A2 e B2 coprono carichi e ambienti industriali più impegnativi.",
    ),
    (
        "A cosa serve un robot cane Unitree in azienda?",
        "Ispezione impianti, pattugliamento, rilievo 3D con LiDAR e POC di robotica mobile. Abra integra hardware, software e formazione sul campo.",
    ),
]

FAQ_EN_QUAD = [
    (
        "What is a quadruped robot?",
        "A quadruped robot (robot dog) is a four-legged mobile platform for inspection, security and rough-terrain logistics. Abra distributes Unitree Go2, A2 and B2 in Italy.",
    ),
    (
        "Which Unitree Go2 should I buy?",
        "Go2 Pro for general use; Go2 EDU / EDU+ for labs; Enterprise for professional deployments. A2/B2 cover heavier industrial payloads.",
    ),
]

FAQ_IT_COBOT = [
    (
        "Cos'è un robot collaborativo (cobot)?",
        "Un cobot è un robot industriale progettato per lavorare a fianco dell'operatore senza recinzioni fisse, con limiti di forza e velocità secondo ISO/TS 15066. Abra distribuisce i cobot Fairino FR Series.",
    ),
    (
        "Quale cobot industriale scegliere?",
        "FR5 e FR10 coprono la maggior parte di pick & place e machine tending PMI; FR20/FR30 per payload maggiori e palletizzazione. Valutiamo ROI tipico 12–24 mesi.",
    ),
]


def faq_section_html(faqs: list[tuple[str, str]], lang: str = "it") -> str:
    title = "Domande frequenti" if lang == "it" else "Frequently asked questions"
    items = []
    for q, a in faqs:
        items.append(
            f'<details class="seo-faq-item"><summary>{q}</summary>'
            f"<p>{a}</p></details>"
        )
    return (
        f'\n<section class="section seo-faq" id="faq" aria-label="{title}">'
        f'<div class="container">'
        f"<h2>{title}</h2>"
        f'{"".join(items)}'
        f"</div></section>\n"
    )


def faq_schema(faqs: list[tuple[str, str]]) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def inject_before_footer(html: str, block: str) -> str:
    if 'id="faq"' in html or "seo-faq" in html:
        return html
    m = re.search(r"<footer\b", html, re.I)
    if not m:
        m = re.search(r"</body>", html, re.I)
    if not m:
        return html + block
    return html[: m.start()] + block + html[m.start() :]


def inject_schema(html: str, schema: str) -> str:
    if '"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html:
        return html
    return html.replace("</head>", schema + "</head>", 1)


def collection_schema(name: str, url: str, items: list[tuple[str, str]]) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": name,
        "url": url,
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(items),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": n,
                    "url": u,
                }
                for i, (n, u) in enumerate(items)
            ],
        },
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def replace_or_append_itemlist(html: str, schema: str) -> str:
    if "itemlist-schema" in html or '"@type": "CollectionPage"' in html:
        html = re.sub(
            r"<!-- itemlist-schema -->\s*<script type=\"application/ld\+json\">.*?</script>",
            "<!-- itemlist-schema -->\n" + schema,
            html,
            count=1,
            flags=re.I | re.S,
        )
        if "itemlist-schema" in html and schema.strip() in html:
            return html
        html = re.sub(
            r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "CollectionPage".*?</script>',
            schema,
            html,
            count=1,
            flags=re.I | re.S,
        )
        return html
    return inject_schema(html, "<!-- itemlist-schema -->\n" + schema)


def optimize_file(path: Path, **opts) -> None:
    html = path.read_text(encoding="utf-8")
    if "title" in opts:
        html = set_title(html, opts["title"])
    if "desc" in opts:
        html = set_meta_desc(html, opts["desc"])
    if "h1" in opts:
        html = set_h1(html, opts["h1"])
    if "lead" in opts:
        html = set_lead(html, opts["lead"])
    if "faqs" in opts:
        lang = opts.get("lang", "it")
        html = inject_before_footer(html, faq_section_html(opts["faqs"], lang))
        html = inject_schema(html, faq_schema(opts["faqs"]))
    if "collection" in opts:
        name, url, items = opts["collection"]
        html = replace_or_append_itemlist(html, collection_schema(name, url, items))
    path.write_text(html, encoding="utf-8")
    print("updated", path.relative_to(ROOT))


def main() -> None:
    g1_items = [
        ("Unitree G1 Air", "https://abrarobotics.com/prodotti/unitree-g1.html"),
        ("Unitree G1 EDU Standard", "https://abrarobotics.com/prodotti/unitree-g1-edu-standard.html"),
        ("Unitree G1 EDU Plus", "https://abrarobotics.com/prodotti/unitree-g1-edu-plus.html"),
        ("Unitree G1 Comp", "https://abrarobotics.com/prodotti/unitree-g1-comp.html"),
        ("Unitree H2", "https://abrarobotics.com/prodotti/unitree-h2.html"),
        ("Unitree R1 EDU", "https://abrarobotics.com/prodotti/unitree-r1-edu.html"),
    ]
    quad_items = [
        ("Unitree Go2 Pro", "https://abrarobotics.com/prodotti/unitree-go2-pro.html"),
        ("Unitree Go2 EDU", "https://abrarobotics.com/prodotti/unitree-go2-edu.html"),
        ("Unitree Go2 EDU+", "https://abrarobotics.com/prodotti/unitree-go2-edu-plus.html"),
        ("Unitree Go2 Enterprise", "https://abrarobotics.com/prodotti/unitree-go2-enterprise-u2.html"),
        ("Unitree A2", "https://abrarobotics.com/prodotti/unitree-a2.html"),
        ("Unitree A2 Pro", "https://abrarobotics.com/prodotti/unitree-a2-pro.html"),
        ("Unitree B2", "https://abrarobotics.com/prodotti/unitree-b2.html"),
    ]

    optimize_file(
        ROOT / "umanoidi.html",
        title="Robot umanoide Unitree G1 in Italia | Abra Robotics",
        desc="Robot umanoide Unitree G1: gamma completa in Italia (Air, EDU, Comp). Prezzi, specifiche e supporto Abra Robotics — distributore ufficiale.",
        h1="Robot umanoide Unitree G1 — gamma completa",
        lead="Cerchi un robot umanoide per azienda, università o demo? Qui trovi tutta la famiglia Unitree G1 distribuita in Italia da Abra Robotics: dal G1 Air alle configurazioni EDU e Comp, con scheda tecnica e prezzi per ciascun modello.",
        faqs=FAQ_IT_UMANOIDI,
        lang="it",
        collection=(
            "Robot umanoidi Unitree in Italia",
            "https://abrarobotics.com/umanoidi.html",
            g1_items,
        ),
    )

    optimize_file(
        ROOT / "en" / "umanoidi-en.html",
        title="Humanoid robot Unitree G1 in Italy | Abra Robotics",
        desc="Unitree G1 humanoid robot full range in Italy: Air, EDU and Comp. Specs, pricing and local support from Abra Robotics.",
        h1="Unitree G1 humanoid robot — full range",
        lead="Looking for a humanoid robot for business, research or demos? Explore the full Unitree G1 family distributed in Italy by Abra Robotics — Air, EDU and Comp — with dedicated product pages.",
        faqs=FAQ_EN_HUMANOID,
        lang="en",
    )

    optimize_file(
        ROOT / "quadrupedi.html",
        title="Robot quadrupede Unitree Go2, A2, B2 | Abra Robotics",
        desc="Robot quadrupede Unitree in Italia: Go2, A2 e B2 per ispezione e industria. Specifiche, prezzi e supporto Abra Robotics.",
        h1="Robot quadrupede Unitree — Go2, A2 e B2",
        lead="Dal Unitree Go2 per education e ispezione leggera al B2 industriale IP67: la gamma completa di robot quadrupedi (robot cane) Unitree, con scheda tecnica dedicata per ogni modello.",
        faqs=FAQ_IT_QUAD,
        lang="it",
        collection=(
            "Robot quadrupedi Unitree",
            "https://abrarobotics.com/quadrupedi.html",
            quad_items,
        ),
    )

    optimize_file(
        ROOT / "en" / "quadrupedi-en.html",
        title="Quadruped robot Unitree Go2, A2, B2 | Abra Robotics",
        desc="Unitree quadruped robots in Italy: Go2, A2 and B2 for inspection and industry. Specs, pricing and Abra Robotics support.",
        h1="Unitree quadruped robots — Go2, A2 and B2",
        lead="From the agile Unitree Go2 for education and light inspection to the industrial B2 IP67: the full Unitree robot dog range with a dedicated product page for each model.",
        faqs=FAQ_EN_QUAD,
        lang="en",
    )

    # G1 product page — strengthen Unitree G1 keyword
    g1 = ROOT / "prodotti" / "unitree-g1.html"
    html = g1.read_text(encoding="utf-8")
    html = set_title(html, "Unitree G1 — robot umanoide Air | Abra Robotics")
    html = set_meta_desc(
        html,
        "Unitree G1 Air: robot umanoide 23 DoF, 2 m/s, LiDAR MID-360 e RealSense. Prezzo e scheda tecnica — Abra Robotics Italia.",
    )
    # enrich product blurb if short intro exists
    if 'id="faq"' not in html:
        faqs = [
            (
                "Il Unitree G1 è un robot umanoide completo?",
                "Sì: il G1 Air è un bipede con 23 gradi di libertà, percezione 3D e piattaforma espandibile verso le varianti EDU con mani e Jetson Orin NX.",
            ),
            (
                "Differenza tra G1 Air e G1 EDU?",
                "G1 Air è orientato a demo e comunicazione; G1 EDU aggiunge computing, mani dexterous e garanzia estesa per ricerca e sviluppo.",
            ),
        ]
        html = inject_before_footer(html, faq_section_html(faqs, "it"))
        html = inject_schema(html, faq_schema(faqs))
    g1.write_text(html, encoding="utf-8")
    print("updated prodotti/unitree-g1.html")

    g1en = ROOT / "en" / "prodotti" / "unitree-g1-en.html"
    if g1en.exists():
        html = g1en.read_text(encoding="utf-8")
        html = set_title(html, "Unitree G1 — humanoid robot Air | Abra Robotics EN")
        html = set_meta_desc(
            html,
            "Unitree G1 Air humanoid robot: 23 DoF, 2 m/s, MID-360 LiDAR and RealSense. Specs and pricing — Abra Robotics Italy.",
        )
        g1en.write_text(html, encoding="utf-8")
        print("updated en/prodotti/unitree-g1-en.html")

    # Cobot hub
    cobot = ROOT / "catalogo-cobot.html"
    html = cobot.read_text(encoding="utf-8")
    html = set_title(html, "Robot collaborativo cobot Fairino | Abra Robotics")
    html = set_meta_desc(
        html,
        "Robot collaborativo e cobot industriale Fairino FR3–FR30 in Italia. Catalogo, prezzi indicativi e integrazione Abra Robotics.",
    )
    html = set_h1(html, "Robot collaborativo Fairino — catalogo cobot")
    html = inject_before_footer(html, faq_section_html(FAQ_IT_COBOT, "it"))
    html = inject_schema(html, faq_schema(FAQ_IT_COBOT))
    cobot.write_text(html, encoding="utf-8")
    print("updated catalogo-cobot.html")

    manif = ROOT / "manifattura-logistica.html"
    html = manif.read_text(encoding="utf-8")
    html = set_title(html, "Robot collaborativo e automazione industriale | Abra")
    html = set_meta_desc(
        html,
        "Robot collaborativo, cobot Fairino, AMR e quadrupedi Unitree per manifattura e logistica. Automazione industriale con Abra Robotics.",
    )
    manif.write_text(html, encoding="utf-8")
    print("updated manifattura-logistica.html")

    # Minimal FAQ styles (reuse existing container)
    css = ROOT / "style.css"
    css_text = css.read_text(encoding="utf-8")
    if ".seo-faq" not in css_text:
        css_text += """

/* SEO FAQ blocks on pillar pages */
.seo-faq { padding-top: 48px; padding-bottom: 48px; }
.seo-faq h2 { margin-bottom: 20px; letter-spacing: -0.02em; }
.seo-faq-item {
  border-top: 1px solid rgba(0,0,0,0.08);
  padding: 14px 0;
}
.seo-faq-item:last-child { border-bottom: 1px solid rgba(0,0,0,0.08); }
.seo-faq-item summary {
  cursor: pointer;
  font-weight: 700;
  font-size: 1.05rem;
  list-style: none;
}
.seo-faq-item summary::-webkit-details-marker { display: none; }
.seo-faq-item p {
  margin: 10px 0 0;
  max-width: 72ch;
  color: var(--gray-600, #525252);
  line-height: 1.55;
}
"""
        css.write_text(css_text, encoding="utf-8")
        print("updated style.css FAQ styles")


if __name__ == "__main__":
    main()
