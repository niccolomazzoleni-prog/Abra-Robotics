"""Rigenera l'hub per famiglie di umanoidi.html dal listino pubblico.

Gestisce tre blocchi delimitati da commenti marker (li inserisce al primo avvio):
  <!-- HUB:FAMIGLIE -->        schede famiglia sotto l'hero
  <!-- HUB:G1-ALTRE -->        configurazioni G1 non presenti nelle schede ricche
  <!-- HUB:ALTRE-FAMIGLIE -->  sezioni G1-D, H2, H2-A/H2-D, R1, R1-A
Uso: python scripts/gen_umanoidi_hub.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "umanoidi.html"
LISTINO = json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8"))

# Famiglie in ordine di presentazione. `serie`: (titolo, regex sullo SKU)
FAMIGLIE = [
    dict(id="g1", nome="Unitree G1", tag="Bipede compatto",
         claim="L'umanoide più diffuso per ricerca, didattica ed eventi: 23–43 gradi di libertà, mani Dex3 o BrainCo.",
         img="images/prodotti/2026/famiglia-g1.png", pagina=None,
         match=r"^G1-", serie=[]),
    dict(id="g1-d", nome="Unitree G1-D", tag="Dual-arm su piantana o base mobile",
         claim="Busto G1 a due braccia da 7 DoF su colonna di sollevamento: Standard su piantana, Ultimate su base mobile.",
         img="images/prodotti/2026/famiglia-g1-d.jpg", pagina="g1-d.html",
         match=r"^G1D-", serie=[("Standard · piantana", r"^G1D-STD-"), ("Ultimate · base mobile", r"^G1D-ULT-")]),
    dict(id="h2", nome="Unitree H2", tag="Full-size bipede",
         claim="Umanoide a grandezza naturale per R&D avanzata: dalla versione Air alle configurazioni EDU Smart e PLUS con mani dexterous.",
         img="images/prodotti/2026/famiglia-h2.png", pagina="h2.html",
         match=r"^H2(-AIR|-EDU|-PLUS)", serie=[("H2 Air ed EDU", r"^H2-(AIR|EDU)$"), ("H2 EDU Smart", r"^H2-EDU-SMART-"),
                                              ("H2 PLUS", r"^H2-PLUS")]),
    dict(id="h2-ad", nome="Unitree H2-A / H2-D", tag="Busto H2 dual-arm",
         claim="La parte superiore di H2 per manipolazione: H2-A come busto (34 kg), H2-D su base mobile con colonna 1,2–1,7 m e ~7 kg per braccio.",
         img="images/prodotti/2026/famiglia-h2-ad.png", pagina="h2.html",
         match=r"^H2-(A-|D)", serie=[("H2-A Standard · busto", r"^H2-A-STD-"), ("H2-D Standard · base mobile", r"^H2-D(-STD-|$)"),
                                     ("H2-D Ultimate · base mobile", r"^H2-D-ULT-")]),
    dict(id="r1", nome="Unitree R1", tag="Bipede entry-level",
         claim="Il bipede più accessibile: 1,21 m, circa 29 kg, 26 gradi di libertà. Versioni EDU con mani Dex3 o BrainCo.",
         img="images/prodotti/2026/famiglia-r1.jpg", pagina=None,
         match=r"^R1-(AIR|BASIC|U\d|EDU|D$)", serie=[]),
    dict(id="r1-a", nome="Unitree R1-A", tag="Busto R1 dual-arm",
         claim="Busto R1 con braccia A5 o A7 (11–13 kg) per banchi di lavoro e didattica; le versioni -D sono su chassis mobile.",
         img="images/prodotti/2026/famiglia-r1-a.png", pagina="r1-d.html",
         match=r"^R1-A[57]", serie=[("R1-A5", r"^R1-A5-(STD|SMART)"), ("R1-A5-D · base mobile", r"^R1-A5-D-"),
                                    ("R1-A7", r"^R1-A7-(STD|SMART)"), ("R1-A7-D · base mobile", r"^R1-A7-D-")]),
]


def eur(v, dec=True):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s if dec else s[:-3]


def prodotti(fam):
    out = [(k, v) for k, v in LISTINO.items()
           if v.get("categoria") == "UMANOIDI" and re.match(fam["match"], k) and not v.get("prezzo_da")]
    return sorted(out, key=lambda kv: kv[1]["prezzo_eur"])


def voce(k, v):
    listino = v.get("prezzo_listino_eur")
    barrato = (f'<s class="fam-map" title="Prezzo di listino">{eur(listino)} €</s>'
               if listino and listino > v["prezzo_eur"] else "")
    return (f'<a class="fam-item" href="prodotti/{v["slug"]}">'
            f'<span class="fam-item-name">{html.escape(v["nome"])}</span>'
            f'<span class="fam-item-price">{barrato}<strong>{eur(v["prezzo_eur"])} €</strong></span></a>')


def elenco(items):
    return '<div class="fam-list">' + "".join(voce(k, v) for k, v in items) + "</div>"


def scheda(fam):
    items = prodotti(fam)
    da = eur(items[0][1]["prezzo_eur"], dec=False)
    link = (f'<a class="fam-card-link" href="{fam["pagina"]}">Pagina famiglia</a>' if fam["pagina"] else "")
    return (f'<article class="fam-card"><a class="fam-card-media" href="#fam-{fam["id"]}">'
            f'<img src="{fam["img"]}" alt="{html.escape(fam["nome"])}, robot umanoide" loading="lazy"></a>'
            f'<div class="fam-card-body"><p class="fam-card-tag">{fam["tag"]}</p><h3>{fam["nome"]}</h3>'
            f'<p class="fam-card-claim">{fam["claim"]}</p>'
            f'<p class="fam-card-meta"><span>da <strong>{da} €</strong></span><span>{len(items)} configurazioni</span></p>'
            f'<div class="fam-card-actions"><a class="btn btn-primary" href="#fam-{fam["id"]}">Vedi configurazioni</a>{link}</div>'
            f"</div></article>")


def sezione(fam):
    items = prodotti(fam)
    corpo = ""
    if fam["serie"]:
        usati = set()
        for titolo, rx in fam["serie"]:
            gruppo = [(k, v) for k, v in items if re.match(rx, k)]
            usati.update(k for k, _ in gruppo)
            if gruppo:
                corpo += f'<h3 class="fam-serie">{titolo} <span>{len(gruppo)}</span></h3>' + elenco(gruppo)
        resto = [(k, v) for k, v in items if k not in usati]
        if resto:
            corpo += '<h3 class="fam-serie">Altre versioni</h3>' + elenco(resto)
    else:
        corpo = elenco(items)
    link = (f'<a class="btn btn-secondary" href="{fam["pagina"]}">Pagina famiglia {fam["nome"].replace("Unitree ", "")}</a>'
            if fam["pagina"] else "")
    return (f'<section class="section fam-section" id="fam-{fam["id"]}"><div class="container">'
            f'<div class="fam-head"><div><p class="label">{fam["tag"]}</p><h2>{fam["nome"]}</h2>'
            f'<p class="fam-head-claim">{fam["claim"]}</p></div>'
            f'<div class="fam-head-side"><img src="{fam["img"]}" alt="{html.escape(fam["nome"])}" loading="lazy">{link}</div></div>'
            f"{corpo}"
            f'<p class="fam-back"><a href="#famiglie">↑ Torna alle famiglie</a></p></div></section>')


STYLE = """<style id="hub-style">
.fam-nav{padding:8px 0 40px}
.fam-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.fam-card{display:flex;flex-direction:column;border:1px solid var(--gray-200);border-radius:var(--radius);background:var(--white);overflow:hidden;transition:border-color .2s,box-shadow .2s}
.fam-card:hover{border-color:var(--gray-400);box-shadow:0 8px 24px rgba(0,0,0,.06)}
.fam-card-media{display:block;aspect-ratio:4/3;overflow:hidden;background:var(--gray-50)}
.fam-card-media img{display:block;width:100%;height:100%;object-fit:contain;padding:16px}
.fam-card-body{display:flex;flex-direction:column;gap:10px;padding:20px;flex:1}
.fam-card-tag{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-text);margin:0}
.fam-card h3{margin:0;font-size:22px}
.fam-card-claim{margin:0;color:var(--gray-600);line-height:1.55;font-size:15px}
.fam-card-meta{display:flex;justify-content:space-between;gap:12px;margin:auto 0 0;padding-top:12px;border-top:1px solid var(--gray-200);font-size:14px;color:var(--gray-600)}
.fam-card-meta strong{color:var(--black);font-size:16px}
.fam-card-actions{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.fam-card-link{font-weight:600;color:var(--black);text-decoration:underline;text-underline-offset:3px}
.fam-section{border-top:1px solid var(--gray-200)}
.fam-head{display:grid;grid-template-columns:1fr 280px;gap:32px;align-items:center;margin-bottom:24px}
.fam-head h2{margin:4px 0 8px}
.fam-head-claim{color:var(--gray-600);line-height:1.6;max-width:680px;margin:0}
.fam-head-side{display:flex;flex-direction:column;gap:12px;align-items:stretch}
.fam-head-side img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:contain;background:var(--gray-50);border-radius:var(--radius-sm);padding:12px}
.fam-serie{font-size:15px;font-weight:700;margin:28px 0 12px;display:flex;align-items:center;gap:8px}
.fam-serie span{font-size:12px;font-weight:600;color:var(--gray-600);background:var(--gray-100);border-radius:999px;padding:2px 8px}
.fam-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.fam-item{display:flex;flex-direction:column;gap:6px;padding:14px 16px;border:1px solid var(--gray-200);border-radius:var(--radius-sm);background:var(--white);color:var(--black);text-decoration:none;transition:border-color .15s,background .15s}
.fam-item:hover{border-color:var(--black);background:var(--gray-50)}
.fam-item-name{font-weight:600;font-size:15px;line-height:1.35}
.fam-item-price{display:flex;align-items:baseline;gap:8px;font-size:14px}
.fam-item-price strong{font-size:16px}
.fam-map{color:var(--gray-400);font-size:13px}
.fam-back{margin:24px 0 0;font-size:14px}
.fam-back a{color:var(--gray-600)}
@media (max-width:960px){.fam-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.fam-head{grid-template-columns:1fr}.fam-head-side{max-width:360px}}
@media (max-width:600px){.fam-grid{grid-template-columns:1fr}}
</style>"""


def sostituisci(t, nome, contenuto, ancora_prima=None, ancora_dopo=None):
    """Sostituisce il blocco <!-- HUB:nome --> ... <!-- /HUB:nome -->, oppure lo inserisce all'ancora."""
    blocco = f"<!-- HUB:{nome} -->\n{contenuto}\n<!-- /HUB:{nome} -->"
    rx = re.compile(rf"<!-- HUB:{re.escape(nome)} -->.*?<!-- /HUB:{re.escape(nome)} -->", re.S)
    if rx.search(t):
        return rx.sub(lambda _: blocco, t)
    if ancora_prima:
        i = t.index(ancora_prima)
        return t[:i] + blocco + "\n" + t[i:]
    i = t.index(ancora_dopo) + len(ancora_dopo)
    return t[:i] + "\n" + blocco + t[i:]


def main():
    t = PAGE.read_text(encoding="utf-8")
    tot = sum(len(prodotti(f)) for f in FAMIGLIE)
    minimo = min(prodotti(f)[0][1]["prezzo_eur"] for f in FAMIGLIE)

    # stile della pagina
    t = sostituisci(t, "STILE", STYLE, ancora_prima="</head>")
    # dati strutturati: elenco di tutte le configurazioni (ItemList) per Google e assistenti AI
    voci = [(k, v) for f in FAMIGLIE for k, v in prodotti(f)]
    lista = {"@context": "https://schema.org", "@type": "ItemList", "name": "Robot umanoidi Unitree in Italia — configurazioni e prezzi",
             "numberOfItems": len(voci),
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"https://abrarobotics.com/prodotti/{v['slug']}",
                                  "item": {"@type": "Product", "name": v["nome"], "brand": {"@type": "Brand", "name": "Unitree"},
                                           "url": f"https://abrarobotics.com/prodotti/{v['slug']}",
                                           "offers": {"@type": "Offer", "price": f"{v['prezzo_eur']:.2f}", "priceCurrency": "EUR",
                                                      "availability": "https://schema.org/InStock"}}}
                                 for i, (k, v) in enumerate(voci)]}
    t = sostituisci(t, "JSONLD", '<script type="application/ld+json">' + json.dumps(lista, ensure_ascii=False) + "</script>",
                    ancora_prima="</head>")

    # hero: titolo, sottotitolo e numeri
    t = re.sub(r"<h1>Robot umanoidi Unitree in Italia[^<]*</h1>",
               "<h1>Robot umanoidi Unitree in Italia — G1, H2, R1 e versioni dual-arm</h1>", t)
    t = re.sub(r'<p class="lead">Gamma umanoide Unitree completa:.*?</p>',
               '<p class="lead">Sei famiglie di umanoidi Unitree, dai bipedi compatti ai busti dual-arm su base mobile. '
               'Scegli la famiglia per vedere tutte le configurazioni con prezzi End-User, IVA esclusa.</p>', t, flags=re.S)
    meta = (f'<div class="hero-meta">\n<div><strong>6</strong><span>Famiglie di umanoidi</span></div>\n'
            f'<div><strong>{tot}</strong><span>Configurazioni</span></div>\n'
            f'<div><strong>da {eur(minimo, dec=False)} €</strong><span>IVA esclusa</span></div>\n'
            f'<div><strong>Italia</strong><span>Filiera Unitree Italia</span></div>\n</div>')
    t = re.sub(r'<div class="hero-meta">.*?</div>\s*</div>', meta, t, count=1, flags=re.S)
    t = re.sub(r'\s*<div class="tldr"[^>]*>\s*<strong>Famiglie esposte:</strong>.*?</div>', "", t, count=1, flags=re.S)

    # schede famiglia sotto l'hero
    nav = ('<section class="section fam-nav" id="famiglie"><div class="container">'
           '<div class="section-header" style="text-align:left;max-width:100%;"><p class="label">Scegli la famiglia</p>'
           '<h2>Quale umanoide ti serve?</h2></div>'
           '<div class="fam-grid">' + "".join(scheda(f) for f in FAMIGLIE) + "</div></div></section>")
    t = sostituisci(t, "FAMIGLIE", nav, ancora_prima="<!-- GRID -->")

    # sezione G1: intestazione sopra le schede ricche + configurazioni non presenti
    g1 = FAMIGLIE[0]
    t = t.replace('<section class="section" id="g1-grid" style="padding-top:24px;">',
                  '<section class="section fam-section" id="fam-g1"><div class="container"><div class="fam-head"><div>'
                  f'<p class="label">{g1["tag"]}</p><h2>{g1["nome"]}</h2><p class="fam-head-claim">{g1["claim"]}</p>'
                  '</div></div></div></section>\n<section class="section" id="g1-grid" style="padding-top:0;">', 1)
    griglia = t[t.index('id="g1-grid"'):t.index("<!-- HUB:G1-ALTRE -->") if "<!-- HUB:G1-ALTRE -->" in t else None]
    griglia = griglia[:griglia.index("</section>")]
    altre = [(k, v) for k, v in prodotti(g1) if f'prodotti/{v["slug"]}' not in griglia]
    blocco_g1 = ('<section class="section fam-section" style="padding-top:0;border-top:0"><div class="container">'
                 f'<h3 class="fam-serie">Altre configurazioni G1 <span>{len(altre)}</span></h3>{elenco(altre)}'
                 '<p class="fam-back"><a href="#famiglie">↑ Torna alle famiglie</a></p></div></section>')
    fine_griglia = t.index("</section>", t.index('id="g1-grid"')) + len("</section>")
    if "<!-- HUB:G1-ALTRE -->" in t:
        t = sostituisci(t, "G1-ALTRE", blocco_g1)
    else:
        t = t[:fine_griglia] + "\n<!-- HUB:G1-ALTRE -->\n" + blocco_g1 + "\n<!-- /HUB:G1-ALTRE -->" + t[fine_griglia:]

    # altre famiglie dopo il confronto G1
    t = t.replace("<h2>Tutta la gamma G1 a confronto</h2>", "<h2>G1: i modelli principali a confronto</h2>")
    altre_fam = "\n".join(sezione(f) for f in FAMIGLIE[1:])
    fine_matrix = t.index("</section>", t.index('class="matrix"')) + len("</section>")
    if "<!-- HUB:ALTRE-FAMIGLIE -->" in t:
        t = sostituisci(t, "ALTRE-FAMIGLIE", altre_fam)
    else:
        t = t[:fine_matrix] + "\n<!-- HUB:ALTRE-FAMIGLIE -->\n" + altre_fam + "\n<!-- /HUB:ALTRE-FAMIGLIE -->" + t[fine_matrix:]

    t = t.replace("<h2>Non sai quale G1 scegliere?</h2>", "<h2>Non sai quale umanoide scegliere?</h2>")
    PAGE.write_text(t, encoding="utf-8")
    print(f"umanoidi.html: 6 famiglie, {tot} configurazioni, G1 extra: {len(altre)}")


if __name__ == "__main__":
    main()
