#!/usr/bin/env python3
"""Pagine prodotto dei marchi non Unitree (prezzo su richiesta) e sezione "Altri marchi" nelle pagine categoria.

Legge data/partner-robots.json (una voce per pagina, nessun prezzo) e usa come guscio la scheda
prodotti/unitree-as2-pro.html: head con consenso e tracciamento, menu, footer e script restano quelli del sito.
Scrive prodotti/<slug>.html e aggiorna il blocco <!-- PARTNER:inizio --> ... <!-- PARTNER:fine -->
in umanoidi.html, quadrupedi.html, cobot.html e amr.html. Idempotente.
Uso: python3 scripts/genera_pagine_partner.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://abrarobotics.com/"
SHELL = os.path.join(ROOT, "prodotti", "unitree-as2-pro.html")
CATEGORIE = {
    "umanoidi": ("Umanoidi", "umanoidi.html"),
    "quadrupedi": ("Quadrupedi", "quadrupedi.html"),
    "cobot": ("Cobot", "cobot.html"),
    "amr": ("AMR", "amr.html"),
    "servizio": ("AMR", "amr.html"),
}
CLAIM = {
    "umanoidi": "Umanoidi di altri produttori per ricerca, test e progetti pilota: scheda tecnica e preventivo su richiesta.",
    "quadrupedi": "Quadrupedi di altri produttori per ispezione, carichi pesanti, ambienti a rischio e didattica: preventivo su richiesta.",
    "cobot": "Cobot e celle di pallettizzazione di altri produttori: scheda tecnica e preventivo su richiesta.",
    "amr": "AMR, smistamento e robot di servizio di altri produttori: scheda tecnica e preventivo su richiesta.",
}
e = html.escape


def breve(v, k=""):
    """Valore da riquadro: la parte con il numero prima di virgola, punto e virgola o parentesi.
    Un numero senza unità vale solo per i gradi di libertà (es. "7" da "7, 12, 18 kg" no)."""
    if len(v) <= 22:
        return v
    for sep in (" (", ", ", "; "):
        c = v.split(sep)[0]
        if sep in v and len(c) <= 22 and any(ch.isdigit() for ch in c):
            if re.fullmatch(r"[\d.,]+", c.strip()) and not re.search(r"libert|dof", k, re.I):
                continue
            return c
    return v if len(v) <= 40 else None


def corte(specs, n):
    """Riquadri: prima i dati che un acquirente confronta (altezza, peso, carico...), in forma breve;
    la scheda tecnica completa resta sotto."""
    ordine = ["altezza", "peso", "carico", "portata", "velocit", "autonomia", "coppia", "sbraccio", "gradi di libert", "dof",
              "protezione", "ip", "ripetibilit", "pendenza", "batteria", "garanzia"]
    salta = ("produttore", "tipo", "connettiv", "collo", "dotazione", "software", "sensori", "terreno", "impieghi", "interfacce")
    righe = []
    for i, (k, v) in enumerate(specs):
        b = breve(v, k)
        if b and not any(w in k.lower() for w in salta):
            r = next((j for j, w in enumerate(ordine) if w in k.lower()), len(ordine))
            righe.append((r, i, k, b))
    scelte = [(k, b) for _, _, k, b in sorted(righe)[:n]]
    return scelte


def shell_parts():
    s = open(SHELL, encoding="utf-8").read()
    head_top = s[:s.index("  <title>")]
    pixel = s[s.index("  <!-- Meta Pixel Code -->"):s.index("</head>")]
    body_top = s[s.index("<body>"):s.index("  <section class=\"product-hero\">")]
    footer = s[s.index("  <footer class=\"footer\">"):]
    return head_top, pixel, body_top, footer


def ld(obj):
    return "  <script type=\"application/ld+json\">\n" + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>\n"


def pagina(p, parts):
    head_top, pixel, body_top, footer = parts
    nome = f"{p['brand']} {p['model']}"
    cat_nome, cat_href = CATEGORIE[p["category"]]
    url = f"{BASE}prodotti/{p['slug']}.html"
    img = f"{BASE}images/prodotti/partner/{p['image']}.webp"
    title = p["title"] if len(p["title"]) > 52 else p["title"] + " | Abra Robotics"
    head = head_top + "".join([
        f"  <title>{e(title)}</title>\n",
        f"  <meta name=\"description\" content=\"{e(p['meta_description'])}\">\n",
        "  <meta name=\"robots\" content=\"index, follow\">\n",
        f"  <link rel=\"canonical\" href=\"{url}\">\n",
        "  <meta property=\"og:type\" content=\"product\">\n",
        f"  <meta property=\"og:title\" content=\"{e(title)}\">\n",
        f"  <meta property=\"og:description\" content=\"{e(p['meta_description'])}\">\n",
        f"  <meta property=\"og:url\" content=\"{url}\">\n",
        f"  <meta property=\"og:image\" content=\"{img}\">\n",
        "  <meta property=\"og:site_name\" content=\"Abra Robotics\">\n",
        "  <meta property=\"og:locale\" content=\"it_IT\">\n",
        "  <meta name=\"twitter:card\" content=\"summary_large_image\">\n",
        f"  <meta name=\"twitter:title\" content=\"{e(title)}\">\n",
        f"  <meta name=\"twitter:description\" content=\"{e(p['meta_description'])}\">\n",
        f"  <meta name=\"twitter:image\" content=\"{img}\">\n",
        "  <link rel=\"stylesheet\" href=\"../style.css\">\n",
        "  <link rel=\"stylesheet\" href=\"product.css\">\n",
        ld({"@context": "https://schema.org/", "@type": "Product", "name": nome, "sku": p["slug"], "image": [img],
            "description": p["lead"], "itemCondition": "https://schema.org/NewCondition",
            "brand": {"@type": "Brand", "name": p["brand"]}, "mpn": p["slug"]}),
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": cat_nome, "item": BASE + cat_href},
            {"@type": "ListItem", "position": 3, "name": nome, "item": url}]}),
        ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in p["faq"]]}),
    ]) + pixel + "</head>\n"

    specs = p["specs"]
    key = "".join(f"            <div class=\"key-spec\"><span class=\"key-spec-value\">{e(v)}</span>"
                  f"<span class=\"key-spec-label\">{e(k)}</span></div>\n" for k, v in corte(specs, 6))
    hero = f"""  <section class="product-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
<a href="../index.html">Home</a>
<span class="breadcrumb-sep">›</span>
<a href="../{cat_href}">{e(cat_nome)}</a>
<span class="breadcrumb-sep">›</span>
<span>{e(nome)}</span>
</nav>
      <div class="product-hero-grid">
        <div class="gallery">
          <div class="gallery-main">
            <img id="gallery-main-img" src="../images/prodotti/partner/{p['image']}.webp" alt="{e(p['image_alt'])}">
          </div>
        </div>
        <div class="product-info">
          <p class="label">{e(cat_nome.upper())} · {e(p['brand'].upper())}</p>
          <h1 class="product-title">{e(p['h1'])}</h1>
          <div class="key-specs-grid">
{key}          </div>
          <p class="product-desc">{e(p['lead'])}</p>
          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price"><span class="buy-box-amount" style="font-size:1.5rem;">Prezzo su richiesta</span></div>
            </div>
            <ul class="buy-box-perks">
              <li><span class="bp-ico">✓</span> Preventivo in 24 ore lavorative</li>
              <li><span class="bp-ico">✓</span> Consegna e configurazione in Italia</li>
              <li><span class="bp-ico">✓</span> Formazione e assistenza tecnica in italiano</li>
            </ul>
            <div class="buy-box-cta"><a href="#form" class="btn btn-primary">Richiedi prezzo e disponibilità</a></div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
    righe ="".join(f"<li><span>{e(k)}</span><span>{e(v)}</span></li>\n" for k, v in specs)
    spec_html = f"""  <section id="specs" class="section section-dark specs-section">
    <div class="container">
      <div class="section-header" style="text-align:left;max-width:100%;margin-bottom:32px;">
        <p class="label label-light">Scheda tecnica</p>
        <h2>Specifiche {e(nome)}</h2>
      </div>
      <div class="specs-accordion faq-list" style="max-width:100%;">
        <div class="faq-item open">
          <button class="faq-question" type="button"><span>Dettagli prodotto</span><span class="faq-icon">+</span></button>
          <div class="faq-answer"><ul class="spec-table">{righe}</ul></div>
        </div>
"""
    if p.get("versions"):
        v = "".join(f"<li><span>{e(x['name'])}</span><span>{e(x.get('note', ''))}</span></li>\n" for x in p["versions"])
        spec_html += f"""        <div class="faq-item">
          <button class="faq-question" type="button"><span>Versioni disponibili</span><span class="faq-icon">+</span></button>
          <div class="faq-answer"><ul class="spec-table">{v}</ul></div>
        </div>
"""
    spec_html += "      </div>\n    </div>\n  </section>\n"

    usi = "".join(f"""        <div class="faq-item">
          <button class="faq-question" type="button"><span>{e(u['title'])}</span><span class="faq-icon">+</span></button>
          <div class="faq-answer"><p>{e(u['text'])}</p></div>
        </div>
""" for u in p.get("use_cases", []))
    highlights = ""
    if p.get("highlights"):
        highlights = "".join(f"<li>{e(h)}</li>" for h in p["highlights"])
        highlights = f"<ul class=\"partner-points\">{highlights}</ul>"
    usi_html = f"""  <section id="applicazioni" class="section">
    <div class="container">
      <div class="section-header" style="text-align:left;max-width:100%;margin-bottom:24px;">
        <p class="label">Applicazioni</p>
        <h2>A cosa serve {e(nome)}</h2>
        {highlights}
      </div>
      <div class="faq-list" style="max-width:100%;">
{usi}      </div>
      <p class="section-sub" style="margin-top:20px;">{e(p.get('compare', ''))}</p>
    </div>
  </section>
"""
    faq = "".join(f"""        <div class="faq-item">
          <button class="faq-question" type="button"><span>{e(f['q'])}</span><span class="faq-icon">+</span></button>
          <div class="faq-answer"><p>{e(f['a'])}</p></div>
        </div>
""" for f in p["faq"])
    faq_html = f"""  <section id="faq" class="section section-dark">
    <div class="container" style="max-width:860px;">
      <div class="section-header" style="text-align:left;max-width:100%;margin-bottom:24px;">
        <p class="label label-light">Domande frequenti</p>
        <h2>{e(nome)}: domande frequenti</h2>
      </div>
      <div class="faq-list" style="max-width:100%;">
{faq}      </div>
    </div>
  </section>
"""
    form = f"""  <section id="form" class="section">
    <div class="container" style="max-width:720px;">
      <div class="section-header" style="text-align:center;">
        <p class="label">Contatti</p>
        <h2>Richiedi prezzo e disponibilità di {e(nome)}</h2>
        <p class="section-sub">Rispondiamo entro 24 ore lavorative con prezzo, tempi di consegna in Italia e configurazione consigliata.</p>
      </div>
      <form class="quote-form-top" data-product="{e(nome)}" style="max-width:100%;">
        <input type="text" name="nome" placeholder="Nome e cognome" required>
        <input type="email" name="email" placeholder="Email" required>
        <input type="tel" name="telefono" placeholder="Telefono" required>
        <textarea name="messaggio" required="" rows="3" placeholder="La tua richiesta su {e(nome)}…"></textarea>
        <button type="submit" class="btn btn-primary">Invia richiesta</button>
        <span class="quote-form-feedback" aria-live="polite"></span>
      </form>
    </div>
  </section>

"""
    style = "<style>.partner-points{margin:12px 0 0;padding-left:20px;display:grid;gap:6px;line-height:1.5}</style>\n"
    return head + body_top.replace("<body>", "<body>\n" + style, 1) + hero + "\n" + spec_html + "\n" + usi_html + "\n" + faq_html + "\n" + form + footer


def card(p):
    nome = f"{p['brand']} {p['model']}"
    ks = "".join(f"<div class=\"key-spec\"><span class=\"key-spec-label\">{e(k)}</span><span class=\"key-spec-value\">{e(v)}</span></div>\n"
                 for k, v in corte(p["specs"], 4))
    return f"""<article class="robot-card" data-family="altri-marchi">
<div class="robot-media">
<span class="robot-media-tag">{e(p['brand'])}</span>
<img alt="{e(p['image_alt'])}" loading="lazy" onerror="this.parentElement.classList.add('no-img');" src="images/prodotti/partner/{p['image']}.webp"/>
<div class="robot-media-placeholder"><strong>{e(nome)}</strong></div>
</div>
<div class="robot-body">
<div>
<h3>{e(nome)}</h3>
<p class="robot-subtitle">{e(p['card_subtitle'] if p.get('card_subtitle') else p['highlights'][0] if p.get('highlights') else '')}</p>
</div>
<div class="key-specs">
{ks}</div>
<div class="robot-card-cta" style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
<span style="font-size:0.95rem;font-weight:700;">Prezzo su richiesta</span>
<a class="btn btn-primary btn-sm" href="prodotti/{p['slug']}.html">Vedi scheda →</a>
</div>
</div>
</article>
"""


def ultima_sezione_fam(s):
    """Fine dell'ultima sezione fam-section (conta le <section> annidate)."""
    i = s.rindex("class=\"section fam-section\"")
    i = s.rindex("<section", 0, i)
    depth, j = 0, i
    for m in re.finditer(r"<section\b|</section>", s[i:]):
        depth += 1 if m.group(0) == "<section" else -1
        if depth == 0:
            return i + m.end()
    raise ValueError("sezione non chiusa")


def main():
    data = json.load(open(os.path.join(ROOT, "data", "partner-robots.json"), encoding="utf-8"))
    parts = shell_parts()
    for p in data:
        open(os.path.join(ROOT, "prodotti", p["slug"] + ".html"), "w", encoding="utf-8", newline="").write(pagina(p, parts))
    per_pagina = {}
    for p in data:
        per_pagina.setdefault(CATEGORIE[p["category"]][1], []).append(p)
    for pag, prodotti in per_pagina.items():
        path = os.path.join(ROOT, pag)
        s = open(path, encoding="utf-8").read()
        s = re.sub(r"<!-- PARTNER:inizio -->.*?<!-- PARTNER:fine -->", "", s, flags=re.S)
        cat = next(k for k, v in CATEGORIE.items() if v[1] == pag and k in CLAIM)
        blocco = (f"<!-- PARTNER:inizio --><section class=\"section fam-section\" data-hub=\"1\" id=\"fam-altri-marchi\"><div class=\"container\">"
                  f"<div class=\"fam-head\"><div><h2>Altri marchi</h2><p class=\"fam-head-claim\">{e(CLAIM[cat])}</p></div></div>"
                  f"<div class=\"fam-body\"><div class=\"robot-grid\">{''.join(card(p) for p in prodotti)}</div></div></div></section><!-- PARTNER:fine -->")
        k = ultima_sezione_fam(s)
        s = s[:k] + blocco + s[k:]
        open(path, "w", encoding="utf-8", newline="").write(s)
    print(len(data), "pagine;", ", ".join(f"{k}: {len(v)}" for k, v in per_pagina.items()))


if __name__ == "__main__":
    main()
