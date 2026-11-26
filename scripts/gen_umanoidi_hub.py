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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from miniature import HEIGHT, WIDTH, thumb_src  # noqa: E402
from h2x_testi import CONFIGS as H2X_CONFIGS  # noqa: E402
PAGE = ROOT / "umanoidi.html"
LISTINO = json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8"))

# Famiglie in ordine di presentazione. `serie`: (titolo, regex sullo SKU)
FAMIGLIE = [
    dict(id="g1", nome="Unitree G1", tag="Bipede compatto",
         claim="L'umanoide più diffuso per ricerca, didattica ed eventi: 23–43 gradi di libertà, mani Dex3 o BrainCo.",
         img="images/official/unitree-g1-01.webp", pagina=None,
         match=r"^G1-", serie=[]),
    dict(id="g1-d", nome="Unitree G1-D", tag="Dual-arm su piantana o base mobile",
         claim="Busto G1 a due braccia da 7 DoF su colonna di sollevamento: Standard su piantana, Ultimate su base mobile.",
         img="images/official/unitree-g1-d-mobile.webp", pagina="g1-d.html",
         match=r"^G1D-", serie=[("Standard · piantana", r"^G1D-STD-"), ("Ultimate · base mobile", r"^G1D-ULT-")]),
    dict(id="h2", nome="Unitree H2", tag="Full-size bipede",
         claim="Umanoide a grandezza naturale per R&D avanzata: dalla versione Air alle configurazioni EDU Smart e PLUS con mani dexterous.",
         img="images/official/unitree-h2-01.webp", pagina="h2.html",
         match=r"^H2(-AIR|-EDU|-PLUS)", serie=[("H2 Air ed EDU", r"^H2-(AIR|EDU)$"), ("H2 EDU Smart", r"^H2-EDU-SMART-"),
                                              ("H2 PLUS", r"^H2-PLUS")]),
    dict(id="h2-x", nome="Unitree H2-X", tag="Nuovo · sicurezza e soccorso",
         claim="Robot diverso dall'H2: circa 170 cm, 31 gradi di libertà, due batterie sostituibili a caldo e circa 8 ore di autonomia da fermo e circa 4 in camminata continua. In preordine, da Air a EDU con mani dexterous.",
         img="images/prodotti/2026/unitree-h2-x.webp", pagina="prodotti/unitree-h2-x.html",
         match=r"^H2-X", serie=[("H2-X Air ed EDU", r"^H2-X-(AIR|EDU)$"), ("H2-X EDU con mani", r"^H2-X-EDU-.")]),
    dict(id="h2-ad", nome="Unitree H2-A / H2-D", tag="Busto H2 dual-arm",
         claim="La parte superiore di H2 per manipolazione: H2-A come busto (34 kg), H2-D su base mobile con colonna 1,2–1,7 m e ~7 kg per braccio.",
         img="images/prodotti/2026/famiglia-h2-ad.png", pagina="h2.html",
         match=r"^H2-(A-|D)", serie=[("H2-A Standard · busto", r"^H2-A-STD-"), ("H2-D Standard · base mobile", r"^H2-D(-STD-|$)"),
                                     ("H2-D Ultimate · base mobile", r"^H2-D-ULT-")]),
    dict(id="r1", nome="Unitree R1", tag="Bipede entry-level",
         claim="Il bipede più accessibile: 1,21 m, circa 29 kg, 26 gradi di libertà. Versioni EDU con mani Dex3 o BrainCo.",
         img="images/official/unitree-r1-01.webp", pagina=None,
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


def h2x():
    """Le 15 versioni H2-X della scheda (una sola pagina prodotto): prezzo Abra e listino barrato."""
    base = LISTINO["H2-X"]
    return [(("H2-X-AIR" if k == "air" else "H2-X-EDU" if k == "edu" else f"H2-X-EDU-{k.upper()}"),
             dict(base, nome=n, prezzo_eur=float(p), prezzo_listino_eur=float(m)))
            for k, n, p, m in H2X_CONFIGS]


def prodotti(fam):
    if fam["id"] == "h2-x":
        return h2x()
    out = [(k, v) for k, v in LISTINO.items()
           if v.get("categoria") == "UMANOIDI" and re.match(fam["match"], k) and not v.get("prezzo_da") and (v.get("prezzo_eur") or v.get("prezzo_su_richiesta"))]
    # voci "su richiesta" (prezzo_su_richiesta, es. G1-PLUS) in fondo: il "da" della famiglia resta il prezzo piu' basso
    return sorted(out, key=lambda kv: (not kv[1].get("prezzo_eur"), kv[1].get("prezzo_eur") or 0))


# modelli nuovi: badge sulla scheda e richiamo nella famiglia
NOVITA = [(r"^H2-X-AIR$", "Novità")]


def novita(k):
    return next((lab for rx, lab in NOVITA if re.match(rx, k)), None)


CAP = 8  # schede visibili per elenco; le altre stanno in un <details> (link comunque presenti nell'HTML)


def voce(k, v):
    """Riga compatta: miniatura, nome, prezzo (listino barrato se c'e')."""
    nome = html.escape(v["nome"])
    # la foto G1 "in corsa" ha scie semitrasparenti che sullo sfondo chiaro diventano macchie grigie
    img = thumb_src((v.get("immagine") or "").replace("unitree-g1-02.webp", "unitree-g1-01.webp"), "")
    media = (f'<img src="{html.escape(img)}" alt="{nome}" width="{WIDTH}" height="{HEIGHT}" loading="lazy" decoding="async">'
             if img else "")
    if not v.get("prezzo_eur"):
        prezzo = '<strong>Su richiesta</strong>'
    else:
        listino = v.get("prezzo_listino_eur")
        barrato = (f'<s class="fam-map" title="Prezzo di listino">{eur(listino, False)} €</s>'
                   if listino and listino > v["prezzo_eur"] else "")
        prezzo = f'{barrato}<strong>{eur(v["prezzo_eur"])} €</strong>'
    badge = f'<span class="fam-badge">{novita(k)}</span>' if novita(k) else ""
    return (f'<a class="fam-row" href="prodotti/{v['slug']}"><span class="fam-row-media">{media}</span>'
            f'<span class="fam-row-name">{nome}{badge}</span><span class="fam-row-price">{prezzo}</span></a>')


def elenco(items, titolo="Tutte le versioni", aperto=False):
    """Serie di versioni in un riquadro espandibile: riepilogo con numero e fascia di prezzo."""
    prezzi = [v["prezzo_eur"] for _, v in items if v.get("prezzo_eur")]
    fascia = (f"da {eur(min(prezzi), False)} €" + (f" a {eur(max(prezzi), False)} €" if max(prezzi) > min(prezzi) else "")
              if prezzi else "prezzo su richiesta")
    return (f'<details class="fam-box"{" open" if aperto else ""}><summary><span class="fam-box-t">{titolo}</span>'
            f'<span class="fam-box-n">{len(items)} {"versione" if len(items) == 1 else "versioni"}</span>'
            f'<span class="fam-box-p">{fascia}</span></summary>'
            '<div class="fam-rows">' + "".join(voce(k, v) for k, v in items) + "</div></details>")


def scheda(fam):
    items = prodotti(fam)
    da = eur(items[0][1]["prezzo_eur"], dec=False)
    nuovi = [(k, v) for k, v in items if novita(k)]
    nuovo = (f'<a class="fam-card-new" href="prodotti/{nuovi[0][1]['slug']}">{novita(nuovi[0][0])}: '
             f'{html.escape(nuovi[0][1]["nome"].split(" (")[0])}</a>') if nuovi else ""
    return (f'<article class="fam-card"><a class="fam-card-media" href="#fam-{fam["id"]}">'
            f'<img src="{fam["img"]}" alt="{html.escape(fam["nome"])}, robot umanoide" loading="lazy"></a>'
            f'<div class="fam-card-body"><p class="fam-card-tag">{fam["tag"]}</p>'
            f'<h3><a href="#fam-{fam["id"]}">{fam["nome"]}</a></h3>{nuovo}'
            f'<p class="fam-card-meta"><span>{len(items)} configurazioni</span><strong>da {da} €</strong></p>'
            f"</div></article>")


def barra(t):
    """Barra fissa per saltare tra le famiglie (resta visibile scorrendo)."""
    voci = [(f"#fam-{f['id']}", f["nome"].replace("Unitree ", ""), any(novita(k) for k, _ in prodotti(f))) for f in FAMIGLIE]
    if 'id="fam-altri-marchi"' in t:
        voci.append(("#fam-altri-marchi", "Altri marchi", False))
    return ('<nav class="fam-jump" aria-label="Famiglie di umanoidi"><div class="container">'
            + "".join(f'<a href="{h}">{n}{"<span>Nuovo</span>" if nv else ""}</a>' for h, n, nv in voci)
            + '<a class="fam-jump-all" href="listino-unitree.html">Listino completo</a></div></nav>')


def sezione(fam):
    items = prodotti(fam)
    corpo = ""
    if fam["serie"]:
        usati = set()
        for titolo, rx in fam["serie"]:
            gruppo = [(k, v) for k, v in items if re.match(rx, k)]
            usati.update(k for k, _ in gruppo)
            if gruppo:
                corpo += elenco(gruppo, titolo, aperto=not corpo)
        resto = [(k, v) for k, v in items if k not in usati]
        if resto:
            corpo += elenco(resto, "Altre versioni")
    else:
        corpo = elenco(items, aperto=True)
    etichetta = "Scheda" if (fam["pagina"] or "").startswith("prodotti/") else "Pagina famiglia"
    link = (f'<a class="btn btn-secondary" href="{fam["pagina"]}">{etichetta} {fam["nome"].replace("Unitree ", "")}</a>'
            if fam["pagina"] else "")
    return (f'<section class="section fam-section" id="fam-{fam["id"]}"><div class="container">'
            f'<div class="fam-head"><div><p class="label">{fam["tag"]}</p><h2>{fam["nome"]}</h2>'
            f'<p class="fam-head-claim">{fam["claim"]}</p></div>'
            f'<div class="fam-head-side"><img src="{fam["img"]}" alt="{html.escape(fam["nome"])}" loading="lazy">{link}</div></div>'
            f'<div class="fam-boxes">{corpo}</div><p class="fam-back"><a href="#famiglie">↑ Torna alle famiglie</a></p></div></section>')


STYLE = """<style id="hub-style">
.fam-jump{position:sticky;top:113px;z-index:40;background:rgba(255,255,255,.96);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--gray-200)}
.fam-jump .container{display:flex;gap:6px;overflow-x:auto;padding-top:10px;padding-bottom:10px;scrollbar-width:none}
.fam-jump .container::-webkit-scrollbar{display:none}
.fam-jump a{flex:none;display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border:1px solid var(--gray-200);border-radius:999px;font-size:14px;font-weight:500;color:var(--black);text-decoration:none;white-space:nowrap}
.fam-jump a:hover,.fam-jump a.on{border-color:var(--black);background:var(--black);color:var(--white)}
.fam-jump a span,.fam-badge{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;background:#ff5a1f;color:#fff;border-radius:999px;padding:2px 7px}
.fam-jump .fam-jump-all{margin-left:auto;border-color:transparent;text-decoration:underline;text-underline-offset:3px}
.fam-section,#famiglie,#g1-grid{scroll-margin-top:170px}
.fam-nav{padding:32px 0 40px}
.fam-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.fam-card{display:grid;grid-template-columns:120px 1fr;border:1px solid var(--gray-200);border-radius:var(--radius);background:var(--white);overflow:hidden;transition:border-color .2s,box-shadow .2s}
.fam-card:hover{border-color:var(--gray-400);box-shadow:0 8px 24px rgba(0,0,0,.06)}
.fam-card-media{display:block;overflow:hidden;background:var(--gray-50)}
.fam-card-media img{display:block;width:100%;height:100%;min-height:130px;object-fit:contain;padding:10px;box-sizing:border-box}
.fam-card-body{display:flex;flex-direction:column;gap:6px;padding:14px 16px}
.fam-card-tag{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-text);margin:0}
.fam-card h3{margin:0;font-size:19px}
.fam-card h3 a{color:inherit;text-decoration:none}
.fam-card-new{align-self:flex-start;font-size:13px;font-weight:600;color:#c2410c;text-decoration:none}
.fam-card-new:hover{text-decoration:underline}
.fam-card-claim{margin:0;color:var(--gray-600);line-height:1.55;font-size:15px}
.fam-card-meta{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin:auto 0 0;padding-top:8px;border-top:1px solid var(--gray-200);font-size:14px;color:var(--gray-600)}
.fam-card-meta strong{color:var(--black);font-size:16px;white-space:nowrap}
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
.fam-list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.fam-item{position:relative;display:flex;flex-direction:column;box-sizing:border-box;border:1px solid var(--gray-200);border-radius:16px;background:var(--white);color:var(--black);text-decoration:none;overflow:hidden;transition:border-color .15s,box-shadow .15s,transform .15s}
.fam-item:hover,.fam-item:focus-visible{border-color:var(--black);box-shadow:0 8px 24px rgba(0,0,0,.07);transform:translateY(-2px)}
.fam-item-media{display:block;position:relative;overflow:hidden;aspect-ratio:4/3;background:var(--gray-50);border-bottom:1px solid var(--gray-100)}
.fam-item-media img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:contain;padding:12px;box-sizing:border-box}
.fam-item-body{display:flex;flex-direction:column;gap:6px;padding:12px 14px 14px;flex:1}
.fam-item-name{font-weight:500;font-size:15px;line-height:1.3}
.fam-item-price{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-top:auto;font-size:14px}
.fam-item-price strong{font-size:16px}
.fam-map{color:#6b6b6b;font-size:13px}
.fam-item .fam-badge{position:absolute;top:10px;left:10px;z-index:1}
#g1-grid .robot-grid.compatta>.robot-card:nth-child(n+7){display:none}
.g1-tutti{display:block;margin:18px auto 0}
.fam-more{margin-top:14px}
.fam-more summary{cursor:pointer;display:inline-block;padding:10px 18px;border:1px solid var(--gray-200);border-radius:999px;font-size:14px;font-weight:500;color:var(--black);list-style:none}
.fam-more summary::-webkit-details-marker{display:none}
.fam-more summary:hover{border-color:var(--black)}
.fam-more[open] summary{margin-bottom:14px}
.fam-boxes{display:flex;flex-direction:column;gap:10px}
.fam-box{border:1px solid var(--gray-200);border-radius:14px;background:var(--white);overflow:hidden}
.fam-box[open]{border-color:var(--gray-400)}
.fam-box summary{display:grid;grid-template-columns:1fr auto auto 20px;gap:16px;align-items:center;padding:14px 18px;cursor:pointer;list-style:none;font-size:15px}
.fam-box summary::-webkit-details-marker{display:none}
.fam-box summary::after{content:"+";font-size:20px;line-height:1;color:var(--gray-600);text-align:center}
.fam-box[open] summary::after{content:"−"}
.fam-box summary:hover{background:var(--gray-50)}
.fam-box-t{font-weight:700}
.fam-box-n{font-size:13px;color:var(--gray-600)}
.fam-box-p{font-size:14px;font-weight:600;white-space:nowrap}
.fam-rows{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid var(--gray-200)}
.fam-row{display:grid;grid-template-columns:52px 1fr auto;gap:12px;align-items:center;padding:8px 18px;border-bottom:1px solid var(--gray-100);color:var(--black);text-decoration:none}
.fam-row:nth-child(odd){border-right:1px solid var(--gray-100)}
.fam-row:hover{background:var(--gray-50)}
.fam-row-media{width:52px;height:40px;background:var(--gray-50);border-radius:6px;overflow:hidden}
.fam-row-media img{width:100%;height:100%;object-fit:contain;display:block}
.fam-row-name{font-size:14px;line-height:1.3;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.fam-row-price{display:flex;flex-direction:column;align-items:flex-end;font-size:14px;white-space:nowrap}
.fam-row-price .fam-map{font-size:12px}
.fam-back{margin:24px 0 0;font-size:14px}
.fam-back a{color:var(--gray-600)}
@media (max-width:960px){.fam-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.fam-head{grid-template-columns:1fr}.fam-head-side{max-width:360px}.fam-list{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (min-width:1101px){.fam-grid{grid-template-columns:repeat(4,minmax(0,1fr))}.fam-card{grid-template-columns:96px 1fr}.fam-card-meta{flex-direction:column;gap:2px}}
@media (max-width:960px){.fam-jump{top:104px}}
@media (max-width:760px){.fam-rows{grid-template-columns:1fr}.fam-row:nth-child(odd){border-right:0}.fam-box summary{grid-template-columns:1fr auto 20px;gap:10px}.fam-box-n{display:none}}
@media (max-width:600px){.fam-grid{grid-template-columns:1fr}.fam-card{grid-template-columns:96px 1fr}.fam-card-meta{flex-direction:column;gap:2px}.fam-list{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.fam-item-body{padding:10px 12px 12px}.fam-item-name{font-size:14px}.fam-item-price{font-size:14px}.fam-item-price strong{font-size:15px}.fam-map{font-size:14px}}
</style>"""


SCRIPT = """<script>
document.addEventListener('DOMContentLoaded',function(){
  var g=document.querySelector('#g1-grid .robot-grid');
  if(g&&g.children.length>6){
    g.classList.add('compatta');
    var b=document.createElement('button');b.type='button';b.className='btn btn-secondary g1-tutti';
    b.textContent='Mostra tutti i '+g.children.length+' modelli G1';
    b.onclick=function(){g.classList.remove('compatta');b.remove();};
    g.after(b);
    var f=document.querySelector('#g1-grid .coll-filters');
    if(f)f.addEventListener('click',function(){g.classList.remove('compatta');b.remove();});
  }
  var link=[].slice.call(document.querySelectorAll('.fam-jump a[href^="#"]'));
  if(!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;
    link.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id);});});},{rootMargin:'-40% 0px -55% 0px'});
  link.forEach(function(a){var s=document.querySelector(a.getAttribute('href'));if(s)io.observe(s);});
});
</script>"""


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
    minimo = min(v["prezzo_eur"] for f in FAMIGLIE for _, v in prodotti(f) if v.get("prezzo_eur"))

    # stile della pagina
    t = sostituisci(t, "STILE", STYLE, ancora_prima="</head>")
    # dati strutturati: elenco di tutte le configurazioni (ItemList) per Google e assistenti AI
    voci, visti = [], set()
    for f in FAMIGLIE:  # una voce per URL (le versioni H2-X stanno tutte nella stessa scheda)
        for k, v in prodotti(f):
            if v["slug"] not in visti:
                visti.add(v["slug"])
                voci.append((k, v))
    lista = {"@context": "https://schema.org", "@type": "ItemList", "name": "Robot umanoidi Unitree in Italia: configurazioni e prezzi",
             "numberOfItems": len(voci),
             # solo elenco (posizione, nome, URL): offerta, immagine, spedizione e resi stanno nel Product di ogni scheda;
             # annidare qui 168 Product senza image/description li faceva segnare come schede commerciante non valide
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": v["nome"],
                                  "url": f"https://abrarobotics.com/prodotti/{v['slug']}"}
                                 for i, (k, v) in enumerate(voci)]}
    t = sostituisci(t, "JSONLD", '<script type="application/ld+json">' + json.dumps(lista, ensure_ascii=False) + "</script>",
                    ancora_prima="</head>")

    # hero: titolo, sottotitolo e numeri
    # "robot umanoidi in vendita in Italia" (piano SEO Italia, IT-7): titolo, H1 e prime righe con prezzo,
    # consegna e assistenza; prezzo di partenza = R1 Air (umanoide completo), i busti dual-arm a parte
    r1_air = next(v["prezzo_eur"] for f in FAMIGLIE for k, v in prodotti(f) if k == "R1-AIR")
    titolo = "Robot umanoidi in vendita in Italia: Unitree G1, H2, R1"
    desc = (f"Robot umanoidi Unitree in vendita in Italia da {eur(round(r1_air), False)} € IVA esclusa: G1, H2, R1 e dual-arm, "
            "listino pubblico, consegna in 60 giorni e assistenza in Italia.")
    t = re.sub(r"<title>[^<]*</title>", f"<title>{titolo}</title>", t, count=1)
    t = re.sub(r'(<meta[^>]*property="og:title"[^>]*content=")[^"]*(")', lambda m: m.group(1) + titolo + m.group(2), t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" property="og:title")', lambda m: m.group(1) + titolo + m.group(2), t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" name="description")', lambda m: m.group(1) + desc + m.group(2), t, count=1)
    t = re.sub(r'(<meta content=")[^"]*(" property="og:description")', lambda m: m.group(1) + desc + m.group(2), t, count=1)
    t = re.sub(r'(<meta[^>]*property="og:description"[^>]*content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), t, count=1)
    t = re.sub(r"<h1>Robot umanoidi (?:Unitree in Italia|in vendita in Italia)[^<]*</h1>",
               "<h1>Robot umanoidi in vendita in Italia: Unitree G1, H2, R1 e dual-arm</h1>", t)
    t = re.sub(r'<p class="lead">(Gamma umanoide Unitree completa:|Sei famiglie di umanoidi|Robot umanoidi Unitree in vendita).*?</p>',
               lambda m: f'<p class="lead">Robot umanoidi Unitree in vendita in Italia da {eur(round(r1_air), False)} € IVA esclusa (R1 Air), '
               f'con spedizione e dazio inclusi; i busti dual-arm partono da {eur(round(minimo), False)} €. Consegna in 60 giorni dalla '
               "conferma d'ordine (G1 EDU U2 in pronta consegna), garanzia e assistenza in Italia. Sette famiglie, dai bipedi "
               "compatti ai busti dual-arm su base mobile.</p>", t, flags=re.S)
    meta = (f'<div class="hero-meta">\n<div><strong>{len(FAMIGLIE)}</strong><span>Famiglie di umanoidi</span></div>\n'
            f'<div><strong>{tot}</strong><span>Configurazioni</span></div>\n'

            f'<div><strong>Italia</strong><span>Filiera di distribuzione di <a href="catalogo-unitree.html">Unitree Italia</a></span></div>\n</div>')
    t = re.sub(r'<div class="hero-meta">.*?</div>\s*</div>', meta, t, count=1, flags=re.S)
    t = re.sub(r'\s*<div class="tldr"[^>]*>\s*<strong>Famiglie esposte:</strong>.*?</div>', "", t, count=1, flags=re.S)

    # schede famiglia sotto l'hero
    nav = (barra(t) + '<section class="section fam-nav" id="famiglie"><div class="container">'
           '<div class="section-header" style="text-align:left;max-width:100%;"><p class="label">Scegli la famiglia</p>'
           '<h2>Quale umanoide ti serve?</h2></div>'
           '<div class="fam-grid">' + "".join(scheda(f) for f in FAMIGLIE) + "</div></div></section>" + SCRIPT)
    t = sostituisci(t, "FAMIGLIE", nav, ancora_prima="<!-- GRID -->")

    # sezione G1: intestazione sopra le schede ricche + configurazioni non presenti
    g1 = FAMIGLIE[0]
    t = t.replace('<section class="section" id="g1-grid" style="padding-top:24px;">',
                  '<section class="section fam-section" id="fam-g1"><div class="container"><div class="fam-head"><div>'
                  f'<p class="label">{g1["tag"]}</p><h2>{g1["nome"]}</h2><p class="fam-head-claim">{g1["claim"]}</p>'
                  '</div></div></div></section>\n<section class="section" id="g1-grid" style="padding-top:0;">', 1)
    griglia = t[t.index('id="g1-grid"'):t.index("<!-- HUB:G1-ALTRE -->") if "<!-- HUB:G1-ALTRE -->" in t else None]
    griglia = griglia[:griglia.index("</section>")]
    altre = [(k, v) for k, v in prodotti(g1) if f'prodotti/{v['slug']}' not in griglia]
    blocco_g1 = ('<section class="section fam-section" style="padding-top:0;border-top:0"><div class="container">'
                 f'{elenco(altre, "Altre configurazioni G1")}'
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
    # il blocco partner (genera_pagine_partner.py) sta dentro ALTRE-FAMIGLIE: va conservato
    partner = re.search(r"<!-- PARTNER:inizio -->.*?<!-- PARTNER:fine -->", t, re.S)
    if partner:
        altre_fam += partner.group(0)
    if "<!-- HUB:ALTRE-FAMIGLIE -->" in t:
        t = sostituisci(t, "ALTRE-FAMIGLIE", altre_fam)
    else:
        t = t[:fine_matrix] + "\n<!-- HUB:ALTRE-FAMIGLIE -->\n" + altre_fam + "\n<!-- /HUB:ALTRE-FAMIGLIE -->" + t[fine_matrix:]

    t = t.replace("<h2>Non sai quale G1 scegliere?</h2>", "<h2>Non sai quale umanoide scegliere?</h2>")
    PAGE.write_text(t, encoding="utf-8")
    print(f"umanoidi.html: {len(FAMIGLIE)} famiglie, {tot} configurazioni, G1 extra: {len(altre)}")


if __name__ == "__main__":
    main()
