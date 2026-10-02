"""Sezione "Sfoglia per categoria" della home (index.html) con prezzi "da" aggiornati.

I prezzi Unitree vengono dal listino pubblico; cobot e AMR dal prezzo minimo
mostrato nelle rispettive pagine catalogo. Il blocco è delimitato da
<!-- HOME:CATEGORIE --> ... <!-- /HOME:CATEGORIE --> e viene inserito subito
dopo l'hero al primo avvio.
Uso: python scripts/gen_home_categorie.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
LISTINO = json.loads((ROOT / "listini/pubblico/end-user.json").read_text(encoding="utf-8"))


def eur(v):
    return f"{v:,.0f}".replace(",", ".")


def unitree(pred):
    xs = [v["prezzo_eur"] for k, v in LISTINO.items() if pred(k, v) and not v.get("prezzo_da")]
    return min(xs), len(xs)


def da_catalogo(path):
    t = (ROOT / path).read_text(encoding="utf-8")
    prezzi = [float(x.replace(".", "").replace(",", ".")) for x in re.findall(r"(\d{1,3}(?:\.\d{3})+(?:,\d{2})?)\s?€", t)]
    return min(prezzi), len(set(re.findall(r'href="prodotti/([^"]+\.html)"', t)))


um = unitree(lambda k, v: v["categoria"] == "UMANOIDI" and re.match(r"^(G1|H2|R1)", k))
qu = unitree(lambda k, v: v["categoria"] == "UMANOIDI" and re.match(r"^(GO2|AS2|A2|B2)", k))
ac = unitree(lambda k, v: v["categoria"] in ("COMPONENTISTICA", "MANI_BRACCI"))
co = da_catalogo("catalogo-cobot.html")
am = da_catalogo("amr.html")

CATEGORIE = [
    ("Umanoidi", "Unitree G1, H2, R1 e versioni dual-arm", um, "umanoidi.html", "images/prodotti/2026/famiglia-g1.png"),
    ("Quadrupedi", "Unitree Go2, AS2, A2 e B2", qu, "quadrupedi.html", "images/prodotti/2026/as2.png"),
    ("Cobot", "Bracci collaborativi Fairino, con celle chiavi in mano", co, "catalogo-cobot.html", "images/manifattura/fairino-fr5.png"),
    ("AMR", "Robot mobili per logistica e intralogistica", am, "amr.html", "images/manifattura/amr/juno-plus.webp"),
    ("Accessori", "Mani, pinze, LiDAR, batterie e moduli di calcolo", ac, "accessori.html", "images/prodotti/2026/revo2-touch.png"),
]


def card(nome, sub, dati, href, img):
    prezzo, n = dati
    return (f'<a class="cat-card" href="{href}"><span class="cat-card-media"><img src="{img}" alt="{nome}" loading="lazy"></span>'
            f'<span class="cat-card-body"><span class="cat-card-name">{nome}</span><span class="cat-card-sub">{sub}</span>'
            f'<span class="cat-card-meta"><span>da <strong>{eur(prezzo)} €</strong></span><span>{n} prodotti</span></span>'
            f'<span class="cat-card-cta">Vedi prezzi →</span></span></a>')


STYLE = """<style id="home-cat-style">
.cat-section{padding-top:56px;padding-bottom:24px}
.cat-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:28px}
.cat-card{display:flex;flex-direction:column;border:1px solid var(--gray-200);border-radius:var(--radius);background:var(--white);color:var(--black);text-decoration:none;overflow:hidden;transition:border-color .2s,box-shadow .2s}
.cat-card:hover{border-color:var(--black);box-shadow:0 8px 24px rgba(0,0,0,.06)}
.cat-card-media{display:block;aspect-ratio:16/10;overflow:hidden;background:var(--gray-50)}
.cat-card-media img{display:block;width:100%;height:100%;object-fit:contain;padding:14px}
.cat-card-body{display:flex;flex-direction:column;gap:6px;padding:18px 20px 20px;flex:1}
.cat-card-name{font-size:22px;font-weight:700;letter-spacing:-.01em}
.cat-card-sub{color:var(--gray-600);font-size:15px;line-height:1.45}
.cat-card-meta{display:flex;justify-content:space-between;gap:12px;margin-top:auto;padding-top:12px;border-top:1px solid var(--gray-200);font-size:14px;color:var(--gray-600)}
.cat-card-meta strong{color:var(--black);font-size:17px}
.cat-card-cta{font-weight:600;font-size:15px;margin-top:4px}
.cat-card--listino{background:var(--black);color:var(--white);border-color:var(--black);justify-content:space-between;padding:24px}
.cat-card--listino:hover{box-shadow:0 8px 24px rgba(0,0,0,.18)}
.cat-card--listino .cat-card-name{font-size:24px}
.cat-card--listino p{color:rgba(255,255,255,.72);font-size:15px;line-height:1.5;margin:10px 0 0}
.cat-card--listino ul{list-style:none;padding:0;margin:16px 0;display:grid;gap:6px;font-size:14px;color:rgba(255,255,255,.85)}
.cat-card--listino li::before{content:"✓ ";color:#b37eff}
.cat-card--listino .cat-card-cta{background:var(--white);color:var(--black);border-radius:999px;padding:12px 18px;text-align:center}
@media (max-width:960px){.cat-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:600px){.cat-grid{grid-template-columns:1fr}.cat-card-media{aspect-ratio:16/9}}
</style>"""


def blocco():
    tot = len([1 for v in LISTINO.values() if not v.get("prezzo_da")]) + co[1] + am[1]
    listino = ('<a class="cat-card cat-card--listino" href="listino-unitree.html"><span>'
               '<span class="cat-card-name">Listino prezzi completo</span>'
               f'<p>Tutti i prezzi End-User in un\'unica pagina, IVA esclusa.</p>'
               '<ul><li>Spedizione e dazio inclusi</li><li>Consegna in 4–6 settimane</li><li>Garanzia e assistenza in Italia</li></ul>'
               '</span><span class="cat-card-cta">Apri il listino →</span></a>')
    return (STYLE + '<section class="section cat-section" id="categorie"><div class="container">'
            '<div class="section-header" style="text-align:left;max-width:100%;margin-bottom:0;">'
            '<p class="label">Prodotti e prezzi</p><h2>Sfoglia per categoria</h2>'
            f'<p class="section-sub" style="margin-left:0;">Prezzi pubblici IVA esclusa per oltre {tot // 10 * 10} prodotti. '
            'Scegli una categoria per confrontare modelli e configurazioni.</p></div>'
            '<div class="cat-grid">' + "".join(card(*c) for c in CATEGORIE) + listino + "</div></div></section>")


def main():
    t = PAGE.read_text(encoding="utf-8")
    contenuto = f"<!-- HOME:CATEGORIE -->\n{blocco()}\n<!-- /HOME:CATEGORIE -->"
    rx = re.compile(r"<!-- HOME:CATEGORIE -->.*?<!-- /HOME:CATEGORIE -->", re.S)
    if rx.search(t):
        t = rx.sub(lambda _: contenuto, t)
    else:
        i = t.index("</header>") + len("</header>")
        t = t[:i] + "\n" + contenuto + t[i:]
    # CTA secondaria dell'hero: porta ai prodotti con i prezzi
    t = t.replace('<a class="btn btn-secondary" href="#soluzioni">Esplora le soluzioni</a>',
                  '<a class="btn btn-secondary" href="#categorie">Vedi prodotti e prezzi</a>')
    PAGE.write_text(t, encoding="utf-8")
    print("home: categorie", [(c[0], eur(c[2][0]), c[2][1]) for c in CATEGORIE])


if __name__ == "__main__":
    main()
