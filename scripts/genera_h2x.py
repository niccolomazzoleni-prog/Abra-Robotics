#!/usr/bin/env python3
"""Scheda Unitree H2-X in tutte le lingue del sito, con le sei configurazioni e i prezzi.

- IT: prodotti/unitree-h2-x.html            (layout scheda prodotto, chrome da prodotti/unitree-g1-pro.html)
- EN: en/prodotti/unitree-h2-x-en.html      (layout scheda prodotto, chrome da en/prodotti/unitree-g1-edu-plus-en.html)
- DE FR NL DA SV NO FI ES PL CS: <codice>/unitree-h2-x.html (layout delle pagine lingua, chrome di genera_lingue.py)
Prezzo "da" = H2-X Air (voce H2-X in end-user.json); la tabella mostra tutte le configurazioni fino al Full Setup.
JSON-LD con offerta in preordine (PreOrder). Testi e configurazioni: scripts/h2x_testi.py.
Idempotente. Uso: python3 scripts/genera_h2x.py   (Python >= 3.12, come genera_lingue.py)
"""
from __future__ import annotations

import html
import json
import posixpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from g1_plus_testi import T as G1P  # noqa: E402  stringhe d'interfaccia IT/EN (pulsanti, form, vantaggi)
from h2x_testi import CONFIGS, LANGS, SOURCE_H2, SOURCE_VIDEO, T  # noqa: E402
from genera_hub_modelli import CAL, SITE  # noqa: E402
from genera_lingue import chrome, cta, head as lang_head, money  # noqa: E402

IMG = "images/official/unitree-h2-01.webp"
NAME = "Unitree H2-X"
SKU = "H2-X"
HREFLANG = {"no": "nb"}
LANG_NAMES = {"it": "Italiano", "en": "English"}
VALID_UNTIL = "2027-06-30"

H2X_CSS = """<style id="h2x-css">
.h2x-table td:first-child{white-space:nowrap}
.h2x-table tr:target td{background:var(--gray-50,#fafafa)}
.h2x-specs td:first-child{color:var(--gray-600);min-width:180px}
.h2x-notes{font-size:.85rem;color:var(--gray-600);margin-top:12px;line-height:1.5}
.h2x-price{display:inline-block;margin-top:14px;padding:10px 16px;border:1px solid var(--gray-200);border-radius:12px}
.h2x-price strong{font-size:1.15rem}
.h2x-media{margin-top:20px}.h2x-media img{width:100%;max-width:720px;height:auto;border-radius:12px;border:1px solid var(--gray-200);background:#fff}
.hm-langs{font-size:.85rem;margin:0 0 14px;color:var(--gray-600)}.hm-langs a{color:inherit}.hm-langs a[aria-current]{font-weight:700;color:var(--black)}
</style>"""


def page_path(code: str) -> str:
    if code == "it":
        return "prodotti/unitree-h2-x.html"
    if code == "en":
        return "en/prodotti/unitree-h2-x-en.html"
    return f"{code}/unitree-h2-x.html"


def rel(src_page: str, target: str) -> str:
    """Link relativo da una pagina (percorso dal root del sito) a un file del sito."""
    return posixpath.relpath(target, posixpath.dirname(src_page))


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def lang_data(code: str) -> dict:
    d = json.loads((ROOT / "data" / "lingue" / f"{code}.json").read_text(encoding="utf-8"))
    d["code"] = code
    return d


def lang_names() -> dict[str, str]:
    names = dict(LANG_NAMES)
    for code in LANGS:
        p = ROOT / "data" / "lingue" / f"{code}.json"
        if code not in names and p.is_file():
            names[code] = json.loads(p.read_text(encoding="utf-8"))["name"]
    return names


def prices(code: str) -> dict[str, str]:
    """Prezzo di ogni configurazione nel formato della lingua."""
    if code == "it":
        fmt = lambda x: f"{x:,.0f}".replace(",", ".") + " €"  # noqa: E731
    elif code == "en":
        fmt = lambda x: f"€{x:,.0f}"  # noqa: E731
    else:
        d = lang_data(code)
        fmt = lambda x: money(x, d)  # noqa: E731
    return {k: fmt(p) for k, _, p in CONFIGS}


def fill(s: str, P: dict[str, str]) -> str:
    for k, v in P.items():
        s = s.replace("{" + k + "}", v)
    return s


def alternates() -> str:
    rows = [(HREFLANG.get(c, c), f"{SITE}/{page_path(c)}") for c in LANGS]
    rows.append(("x-default", f"{SITE}/{page_path('it')}"))
    return "\n".join(f'<link rel="alternate" hreflang="{h}" href="{u}"/>' for h, u in rows)


def lang_bar(code: str, label: str) -> str:
    names = lang_names()
    own = page_path(code)
    items = [f'<a href="{rel(own, page_path(c))}" hreflang="{HREFLANG.get(c, c)}"{" aria-current=\"page\"" if c == code else ""}>{esc(names[c])}</a>'
             for c in LANGS]
    return f'<nav class="hm-langs" aria-label="{esc(label)}">{" · ".join(items)}</nav>'


def section(h2: str, inner: str, anchor: str = "") -> str:
    a = f' id="{anchor}"' if anchor else ""
    return f'<section class="section hm-guide" style="padding-top:0"{a}><div class="container"><h2>{esc(h2)}</h2>{inner}</div></section>\n'


def configs_table(code: str, P: dict[str, str], price_col: str) -> str:
    t = T[code]
    rows = "".join(f'<tr id="h2x-{k}"><td><strong>{esc(n)}</strong></td><td>{esc(inc)}</td><td class="p">{esc(P[k])}</td></tr>'
                   for (k, n, _), inc in zip(CONFIGS, t["cfg"]))
    return (f'<p>{esc(t["cfg_intro"])}</p><div class="hm-wrap"><table class="hm-table h2x-table"><thead><tr>'
            f'<th>{esc(t["cols"][0])}</th><th>{esc(t["cols"][1])}</th><th>{esc(price_col)}</th></tr></thead><tbody>{rows}</tbody></table></div>'
            + '<div class="h2x-notes">' + "<br>".join(esc(n) for n in t["cfg_notes"]) + "</div>")


def specs_table(code: str) -> str:
    t = T[code]
    rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in t["specs"])
    return f'<p>{esc(t["specs_intro"])}</p><div class="hm-wrap"><table class="hm-table h2x-specs"><tbody>{rows}</tbody></table></div>'


def what_html(code: str) -> str:
    return "".join(f"<p>{esc(p)}</p>" for p in T[code]["what"])


def faq_html(code: str, P: dict[str, str]) -> str:
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(fill(a, P))}</p></details>" for q, a in T[code]["faq"])


def sources_html(code: str) -> str:
    v, h = T[code]["src"]
    return (f'<ul><li><a href="{SOURCE_VIDEO}" target="_blank" rel="noopener">{esc(v)}: {SOURCE_VIDEO}</a></li>'
            f'<li><a href="{SOURCE_H2}" target="_blank" rel="noopener">{esc(h)}: {SOURCE_H2}</a></li></ul>')


def json_ld(code: str, crumbs: list[tuple[str, str]], P: dict[str, str]) -> list[dict]:
    t = T[code]
    own = f"{SITE}/{page_path(code)}"
    low = CONFIGS[0][2]
    # Offerta "da": prezzo dell'H2-X Air, in preordine (la data di consegna si conferma in offerta)
    product = {"@context": "https://schema.org", "@type": "Product", "name": NAME, "sku": SKU, "mpn": SKU,
               "brand": {"@type": "Brand", "name": "Unitree"}, "image": [f"{SITE}/{IMG}"],
               "description": fill(t["desc"], P), "url": own, "category": "Business & Industrial > Robotics",
               "offers": {"@type": "Offer", "url": own, "priceCurrency": "EUR", "price": f"{low:.2f}",
                          "priceValidUntil": VALID_UNTIL, "availability": "https://schema.org/PreOrder",
                          "itemCondition": "https://schema.org/NewCondition",
                          "seller": {"@type": "Organization", "name": "Abra Robotics"}}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(crumbs + [(NAME, own)], 1)]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": fill(a, P)}} for q, a in t["faq"]]}
    return [product, bc, faq]


def ld_tags(lds: list[dict]) -> str:
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)


# ---------- IT / EN: scheda prodotto ----------

def product_page(code: str) -> str:
    en = code == "en"
    t, ui = T[code], G1P[code]
    P = prices(code)
    title, desc = fill(t["title"], P), fill(t["desc"], P)
    own_rel = page_path(code)
    own = f"{SITE}/{own_rel}"
    tpl = (ROOT / ("en/prodotti/unitree-g1-edu-plus-en.html" if en else "prodotti/unitree-g1-pro.html")).read_text(encoding="utf-8")
    head = tpl[: tpl.index("</head>")]
    head = re.sub(r"<title>[\s\S]*?</title>", "%%HEADMETA%%", head, count=1)
    head = re.sub(r'\s*<meta[^>]*(?:name="(?:description|robots|twitter:[^"]*)"|property="og:[^"]*")[^>]*>', "", head)
    head = re.sub(r'\s*<link[^>]*(?:rel="canonical"|hreflang=)[^>]*>', "", head)
    head = re.sub(r'\s*<script type="application/ld\+json">[\s\S]*?</script>', "", head)
    head = re.sub(r'\s*<style id="correlati-css">[\s\S]*?</style>', "", head)
    head = head.replace("<!-- Open Graph / Twitter -->", "")
    pre = rel(own_rel, "index.html").replace("index.html", "")  # "../" o "../../"
    crumbs = ([("Home", f"{SITE}/en/index-en.html"), ("Humanoids", f"{SITE}/en/umanoidi-en.html"), ("Unitree H2", f"{SITE}/en/h2-en.html")] if en else
              [("Home", f"{SITE}/"), ("Umanoidi", f"{SITE}/umanoidi.html"), ("Unitree H2", f"{SITE}/h2.html")])
    meta = f"""<title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{own}">
{alternates()}
  <meta property="og:type" content="product">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{own}">
  <meta property="og:image" content="{SITE}/{IMG}">
  <meta property="og:site_name" content="Abra Robotics">
  <meta property="og:locale" content="{'en_GB' if en else 'it_IT'}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{SITE}/{IMG}">"""
    head = head.replace("%%HEADMETA%%", meta, 1)
    head += ld_tags(json_ld(code, crumbs, P)) + "\n" + H2X_CSS + "\n"
    if "hub-modello-css" not in head:
        from genera_hub_modelli import HUB_CSS
        head += HUB_CSS + "\n"
    head += "</head>\n"
    body = tpl[tpl.index("<body>"): tpl.index('<section class="product-hero">')]
    footer = tpl[tpl.index('<footer class="footer">'):]

    home, hum, fam = (("../index-en.html", "../umanoidi-en.html", "../h2-en.html") if en else ("../index.html", "../umanoidi.html", "../h2.html"))
    img = pre + IMG
    keys = "".join(f'<div class="key-spec"><span class="key-spec-value">{esc(v)}</span><span class="key-spec-label">{esc(k)}</span></div>' for k, v in t["key"])
    perks = "".join(f'<li><span class="bp-ico">✓</span> {esc(p)}</li>' for p in ui["perks"])
    f = dict(ui["form"], msg=t["form_msg"])
    price_from = t["price_label"].replace("{p}", P["air"])
    main = f"""<section class="product-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
<a href="{home}">Home</a>
<span class="breadcrumb-sep">›</span>
<a href="{hum}">{esc(ui['umanoidi'])}</a>
<span class="breadcrumb-sep">›</span>
<a href="{fam}">Unitree H2</a>
<span class="breadcrumb-sep">›</span>
<span>{NAME}</span>
</nav>
      {lang_bar(code, 'Languages' if en else 'Lingue')}
      <div class="product-hero-grid">
        <div class="gallery">
          <div class="gallery-main">
            <img id="gallery-main-img" src="{img}" alt="{esc(t['img_alt'])}">
          </div>
          <div class="gallery-thumbs">
            <div class="gallery-thumb active" data-index="0"><img src="{img}" alt="{esc(t['img_alt'])}"></div>
          </div>
        </div>
        <div class="product-info">
          <p class="label">{esc(t['label'])}</p>
          <h1 class="product-title">{NAME}</h1>
          <p class="product-subtitle">{esc(t['subtitle'])}</p>
          <div class="key-specs-grid" style="grid-template-columns:repeat(2,1fr)">{keys}</div>
          <p class="product-desc">{esc(t['lead'])}</p>
          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price"><span class="buy-box-amount" style="font-size:1.5rem;">{esc(price_from)}</span><span class="buy-box-sub">H2-X Air → H2-X Full Setup ({esc(P['full'])})</span></div>
            </div>
            <ul class="buy-box-perks">
              {perks}
            </ul>
            <div class="buy-box-cta">
              <a href="#form" class="btn btn-primary">{esc(ui['btn_quote'])}</a>
              <a href="{CAL}" class="btn btn-secondary" target="_blank" rel="noopener noreferrer">{esc(ui['btn_call'])}</a>
            </div>
            <p class="buy-box-note">{esc(t['price_note'])}</p>
          </div>
        </div>
      </div>
    </div>
  </section>

{section(t['cfg_h2'], configs_table(code, P, t['price_col']), 'configurazioni')}{section(t['what_h2'], what_html(code), 'unitree-h2-x')}{section(t['specs_h2'], specs_table(code), 'specs')}{section(t['family_h2'], '<p>' + esc(t['family_text']) + f' <a href="{fam}">{esc(t["family_link"])} →</a></p>')}
<section class="section hm-faq" id="faq"><div class="container"><h2>{esc(ui['faq_h2'])}</h2>{faq_html(code, P)}</div></section>
<section class="section hm-src" style="padding-top:0"><div class="container"><h2>{esc(ui['sources_h2'])}</h2>{sources_html(code)}</div></section>

  <section id="form" class="section" style="scroll-margin-top:120px;">
    <div class="container" style="max-width:720px;">
      <div class="section-header" style="text-align:center;">
        <p class="label">{'Contact' if en else 'Contatti'}</p>
        <h2>{esc(t['form_h2'])}</h2>
        <p class="section-sub">{esc(t['form_sub'])}</p>
      </div>
      <form class="quote-form-top" data-product="{NAME}" style="max-width:100%;">
        <input type="text" name="nome" placeholder="{esc(f['name'])}" required>
        <input type="text" name="azienda" placeholder="{esc(f['company'])}" required>
        <input type="email" name="email" placeholder="{esc(f['email'])}" required>
        <input type="tel" name="telefono" placeholder="{esc(f['phone'])}" required>
        <textarea name="messaggio" required rows="3" placeholder="{esc(f['msg'])}"></textarea>
        <button type="submit" class="btn btn-primary">{esc(f['send'])}</button>
        <span class="quote-form-feedback" aria-live="polite"></span>
      </form>
    </div>
  </section>

"""
    return head + body + main + footer


# ---------- altre lingue: pagina in stile pagine lingua ----------

def lang_page(code: str) -> str:
    d = lang_data(code)
    u, t = d["ui"], T[code]
    P = prices(code)
    own_rel = page_path(code)
    own = f"{SITE}/{own_rel}"
    h2_name = d["families"]["h2"]["name"]
    crumbs = [(u["home"], f"{SITE}/{code}/"), (f"Unitree {h2_name}", f"{SITE}/{code}/unitree-h2.html")]
    head = lang_head(d, fill(t["title"], P), fill(t["desc"], P), own, alternates(), IMG, json_ld(code, crumbs, P))
    head = head.replace("</head>", H2X_CSS + "\n</head>", 1)
    _, _, body, footer = chrome(d)
    keys = "".join(f"<div><strong>{esc(v)}</strong><span>{esc(k)}</span></div>" for k, v in t["key"])
    media = f'<div class="h2x-media"><img src="../{IMG}" alt="{esc(t["img_alt"])}" loading="lazy"></div>'
    cta_html = cta(d).replace('<section class="section section-cta">', '<section class="section section-cta" id="quote">', 1)
    price_from = f'{u["from"].replace("{p}", P["air"])} {u["excl_vat"]}'
    main = f"""<!-- HERO -->
<section class="collection-hero">
<div class="container">
{lang_bar(code, u['languages'])}
<p class="label"><a href="./" style="color:inherit">{esc(u['home'])}</a> · <a href="unitree-h2.html" style="color:inherit">Unitree {esc(h2_name)}</a></p>
<h1>{NAME}</h1>
<p class="lead">{esc(t['lead'])}</p>
<div class="hero-meta">
{keys}
</div>
<p class="h2x-price"><strong>{esc(price_from)}</strong> · H2-X Air → H2-X Full Setup ({esc(P['full'])})</p>
<p>{esc(t['price_note'])} <a href="#quote">{esc(u['quote_title'])} →</a></p>
</div>
</section>
{section(t['cfg_h2'], configs_table(code, P, u['table_price']), 'configurations')}{section(t['what_h2'], what_html(code) + media, 'unitree-h2-x')}{section(t['specs_h2'], specs_table(code), 'specs')}{section(t['family_h2'], '<p>' + esc(t['family_text']) + f' <a href="unitree-h2.html">{esc(t["family_link"])} →</a></p>')}{cta_html}
<section class="section hm-faq" id="faq"><div class="container"><h2>{esc(u['faq'])}</h2>{faq_html(code, P)}</div></section>
<section class="section hm-src" style="padding-top:0"><div class="container"><h2>{esc(u['sources'])}</h2>{sources_html(code)}</div></section>
"""
    return ("<!-- generato da scripts/genera_h2x.py -->\n" + head + body + main + footer
            + '\n<script defer src="../script.js"></script>\n</body>\n</html>\n')


def main() -> None:
    for code in LANGS:
        out = ROOT / page_path(code)
        out.write_text(product_page(code) if code in ("it", "en") else lang_page(code), encoding="utf-8")
        print("scritta", page_path(code))


if __name__ == "__main__":
    main()
