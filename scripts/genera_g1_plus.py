#!/usr/bin/env python3
"""Scheda Unitree G1+ (G1 Plus) in tutte le lingue del sito.

- IT: prodotti/unitree-g1-plus.html            (layout scheda prodotto, chrome da prodotti/unitree-g1-pro.html)
- EN: en/prodotti/unitree-g1-plus-en.html      (layout scheda prodotto, chrome da en/prodotti/unitree-g1-edu-plus-en.html)
- DE FR NL DA SV NO FI ES PL CS: <codice>/unitree-g1-plus.html (layout delle pagine lingua, chrome di genera_lingue.py)
Prezzo SEMPRE su richiesta: nessuna cifra, nessun "price"/"offers" nel JSON-LD (quindi fuori dal merchant feed).
Testi e dati: scripts/g1_plus_testi.py (solo dalla pagina ufficiale Unitree).
Idempotente. Uso: python3 scripts/genera_g1_plus.py   (Python >= 3.12, come genera_lingue.py)
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
from g1_plus_testi import LANGS, SOURCE, SOURCE_EN, T  # noqa: E402
from genera_hub_modelli import CAL, SITE  # noqa: E402
from genera_lingue import chrome, cta, head as lang_head  # noqa: E402

IMG = "images/prodotti/2026/unitree-g1-plus.webp"
IMG2 = "images/prodotti/2026/unitree-g1-plus-dettagli.webp"
NAME = "Unitree G1+ (G1 Plus)"
HREFLANG = {"no": "nb"}
LANG_NAMES = {"it": "Italiano", "en": "English"}

G1P_CSS = """<style id="g1-plus-css">
.g1p-upg{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-top:20px}
.g1p-upg div{border:1px solid var(--gray-200);border-radius:var(--radius,12px);padding:16px}
.g1p-upg b{display:block;font-size:.75rem;letter-spacing:.06em;color:var(--gray-600);margin-bottom:4px}
.g1p-upg h3{font-size:1.02rem;margin:0 0 6px}.g1p-upg p{margin:0;line-height:1.55;font-size:.93rem}
.g1p-table tr.sec th{background:var(--gray-50,#fafafa);color:var(--black);font-size:.8rem}
.g1p-table td:first-child{color:var(--gray-600);min-width:180px}
.g1p-notes{font-size:.85rem;color:var(--gray-600);margin-top:12px;line-height:1.5}
.g1p-media{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:20px}
.g1p-media img{width:100%;height:auto;border-radius:12px;border:1px solid var(--gray-200);background:#fff}
.g1p-price{display:inline-block;margin-top:14px;padding:10px 16px;border:1px solid var(--gray-200);border-radius:12px}
.g1p-price strong{font-size:1.15rem}
.g1p-note{font-size:.9rem;color:var(--gray-600)}
.hm-langs{font-size:.85rem;margin:0 0 14px;color:var(--gray-600)}.hm-langs a{color:inherit}.hm-langs a[aria-current]{font-weight:700;color:var(--black)}
</style>"""


def page_path(code: str) -> str:
    if code == "it":
        return "prodotti/unitree-g1-plus.html"
    if code == "en":
        return "en/prodotti/unitree-g1-plus-en.html"
    return f"{code}/unitree-g1-plus.html"


def rel(src_page: str, target: str) -> str:
    """Link relativo da una pagina (percorso dal root del sito) a un file del sito."""
    return posixpath.relpath(target, posixpath.dirname(src_page))


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def L(code: str, key: str):
    """Testo nella lingua, con ripiego sull'inglese per le chiavi d'interfaccia delle pagine IT/EN."""
    return T[code].get(key, T["en"].get(key))


def lang_names() -> dict[str, str]:
    names = dict(LANG_NAMES)
    for code in LANGS:
        p = ROOT / "data" / "lingue" / f"{code}.json"
        if code not in names and p.is_file():
            names[code] = json.loads(p.read_text(encoding="utf-8"))["name"]
    return names


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


def dec(x: str, code: str) -> str:
    return x if code == "en" else re.sub(r"(\d)\.(\d)", r"\1,\2", x)


def spec_rows(code: str) -> list[tuple]:
    t = T[code]
    s, v = t["s"], t["v"]
    ap = lambda x: v["approx"].format(x=dec(x, code))  # noqa: E731
    yes, none, price = v["yes"], "—", t["price"]
    jr = f'{v["waist"]} Z ±155° · {v["knee"]} 0–165° · {v["hip"]} P ±154°, R −30…+170°, Y ±158°'
    wr = dec("92.5", code)
    same = lambda k, x: (s[k], x, x)  # noqa: E731
    return [
        ("#", s["sec_mech"]),
        same("dim_stand", "1340 × 450 × 200 mm"),
        same("dim_fold", "690 × 450 × 300 mm"),
        (s["weight"], ap("35 kg"), ap("35 kg+")),
        (s["dof_total"], "25", "25–45"),
        same("dof_head", "2"), same("dof_leg", "6"),
        (s["dof_waist"], "1", v["waist_opt"]),
        same("dof_arm", "5"),
        (s["dof_hand"], none, v["hand_edu"]),
        same("bearing", v["bearing_v"]), same("motor", v["motor_v"]),
        (s["arm_load"], ap("3 kg"), ap("4 kg")),
        same("leg_len", dec("0.6 m", code)), same("arm_span", ap("0.45 m")),
        (s["joint_range"], jr, f'{jr} · {v["wrist"]} P ±{wr}°, Y ±{wr}°'),
        ("#", s["sec_elec"]),
        same("routing", yes), same("encoder", v["encoder_v"]), same("cooling", v["cooling_v"]),
        same("power", v["power_v"]), same("cpu", v["cpu_v"]), same("sensors", v["sensors_v"]),
        same("mics", yes), same("speakers", "2"), same("wifi", yes),
        ("#", s["sec_acc"]),
        (s["compute_module"], none, v["module_v"]),
        same("battery", "9000 mAh"), same("charger", "54 V 5 A"), same("remote", yes),
        ("#", s["sec_other"]),
        same("battery_life", ap("2 h")), same("ota", yes),
        (s["sdk"], none, yes),
        (s["warranty"], v["months"].format(n=8), v["months"].format(n=18)),
        same("price", price),
    ]


def specs_table(code: str) -> str:
    t = T[code]
    body = []
    for r in spec_rows(code):
        if r[0] == "#":
            body.append(f'<tr class="sec"><th colspan="3">{esc(r[1])}</th></tr>')
        else:
            body.append(f"<tr><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td></tr>")
    return (f'<div class="hm-wrap"><table class="hm-table g1p-table"><thead><tr><th>{esc(t["col"])}</th><th>G1+</th><th>G1+ EDU</th></tr></thead>'
            f'<tbody>\n' + "\n".join(body) + "\n</tbody></table></div>"
            + '<div class="g1p-notes">' + "<br>".join(esc(n) for n in t["notes"]) + "</div>")


def upgrades(code: str) -> str:
    t = T[code]
    cards = "".join(f'<div><b>{i:02d}</b><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for i, (a, b) in enumerate(t["upg"], 1))
    return f'<p>{esc(t["upg_intro"])}</p><div class="g1p-upg">{cards}</div>'


def faq_html(code: str) -> str:
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in T[code]["faq"])


def section(h2: str, inner: str, anchor: str = "") -> str:
    a = f' id="{anchor}"' if anchor else ""
    return f'<section class="section hm-guide" style="padding-top:0"{a}><div class="container"><h2>{esc(h2)}</h2>{inner}</div></section>\n'


def sources_html(code: str) -> str:
    t = T[code]
    srcs = [SOURCE] + ([SOURCE_EN] if code != "it" else [])
    return "<ul>" + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t["source_label"] if i == 0 else "Unitree G1+ (EN)")}: {u}</a></li>'
                            for i, u in enumerate(srcs)) + "</ul>"


def json_ld(code: str, crumbs: list[tuple[str, str]]) -> list[dict]:
    t = T[code]
    own = f"{SITE}/{page_path(code)}"
    # Nessun "offers": il prezzo e' su richiesta (niente prezzo nei risultati Google ne' nel merchant feed).
    product = {"@context": "https://schema.org", "@type": "Product", "name": NAME, "sku": "unitree-g1-plus", "mpn": "unitree-g1-plus",
               "brand": {"@type": "Brand", "name": "Unitree"}, "image": [f"{SITE}/{IMG}", f"{SITE}/{IMG2}"],
               "description": t["desc"], "url": own, "category": "Business & Industrial > Robotics"}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(crumbs + [(NAME, own)], 1)]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    return [product, bc, faq]


def ld_tags(lds: list[dict]) -> str:
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)


# ---------- IT / EN: scheda prodotto ----------

def product_page(code: str) -> str:
    en = code == "en"
    t = T[code]
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
    crumbs = ([("Home", f"{SITE}/en/index-en.html"), ("Humanoids", f"{SITE}/en/umanoidi-en.html"), ("Unitree G1", f"{SITE}/en/g1-en.html")] if en else
              [("Home", f"{SITE}/"), ("Umanoidi", f"{SITE}/umanoidi.html"), ("Unitree G1", f"{SITE}/g1.html")])
    meta = f"""<title>{esc(t['title'])}</title>
  <meta name="description" content="{esc(t['desc'])}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{own}">
{alternates()}
  <meta property="og:type" content="product">
  <meta property="og:title" content="{esc(t['title'])}">
  <meta property="og:description" content="{esc(t['desc'])}">
  <meta property="og:url" content="{own}">
  <meta property="og:image" content="{SITE}/{IMG}">
  <meta property="og:site_name" content="Abra Robotics">
  <meta property="og:locale" content="{'en_GB' if en else 'it_IT'}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(t['title'])}">
  <meta name="twitter:description" content="{esc(t['desc'])}">
  <meta name="twitter:image" content="{SITE}/{IMG}">"""
    head = head.replace("%%HEADMETA%%", meta, 1)
    head += ld_tags(json_ld(code, crumbs)) + "\n" + G1P_CSS + "\n"
    if "hub-modello-css" not in head:
        from genera_hub_modelli import HUB_CSS
        head += HUB_CSS + "\n"
    head += "</head>\n"
    body = tpl[tpl.index("<body>"): tpl.index('<section class="product-hero">')]
    footer = tpl[tpl.index('<footer class="footer">'):]

    home, hum, fam = (("../index-en.html", "../umanoidi-en.html", "../g1-en.html") if en else ("../index.html", "../umanoidi.html", "../g1.html"))
    edu_plus = "unitree-g1-edu-plus-en.html" if en else "unitree-g1-edu-plus.html"
    img, img2 = pre + IMG, pre + IMG2
    keys = "".join(f'<div class="key-spec"><span class="key-spec-value">{esc(v)}</span><span class="key-spec-label">{esc(k)}</span></div>' for k, v in t["key"])
    perks = "".join(f'<li><span class="bp-ico">✓</span> {esc(p)}</li>' for p in L(code, "perks"))
    f = L(code, "form")
    company = f'\n        <input type="text" name="azienda" placeholder="{esc(f["company"])}" required>'
    main = f"""<section class="product-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
<a href="{home}">Home</a>
<span class="breadcrumb-sep">›</span>
<a href="{hum}">{esc(L(code, 'umanoidi'))}</a>
<span class="breadcrumb-sep">›</span>
<a href="{fam}">Unitree G1</a>
<span class="breadcrumb-sep">›</span>
<span>Unitree G1+</span>
</nav>
      {lang_bar(code, 'Languages' if en else 'Lingue')}
      <div class="product-hero-grid">
        <div class="gallery">
          <div class="gallery-main">
            <img id="gallery-main-img" src="{img}" alt="{esc(t['img_alt'])}">
            <div class="gallery-nav">
              <button aria-label="{'Previous image' if en else 'Immagine precedente'}" class="gallery-btn" id="gallery-prev">←</button>
              <button aria-label="{'Next image' if en else 'Immagine successiva'}" class="gallery-btn" id="gallery-next">→</button>
            </div>
          </div>
          <div class="gallery-thumbs">
            <div class="gallery-thumb active" data-index="0"><img src="{img}" alt="{esc(t['img_alt'])}"></div>
            <div class="gallery-thumb" data-index="1"><img src="{img2}" alt="{esc(t['img2_alt'])}"></div>
          </div>
        </div>
        <div class="product-info">
          <p class="label">{esc(L(code, 'label'))}</p>
          <h1 class="product-title">{NAME}</h1>
          <p class="product-subtitle">{esc(t['subtitle'])}</p>
          <div class="key-specs-grid" style="grid-template-columns:repeat(2,1fr)">{keys}</div>
          <p class="product-desc">{esc(t['lead'])}</p>
          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price"><span class="buy-box-amount" style="font-size:1.5rem;">{esc(t['price'])}</span><span class="buy-box-sub">G1+ · G1+ EDU</span></div>
            </div>
            <ul class="buy-box-perks">
              {perks}
            </ul>
            <div class="buy-box-cta">
              <a href="#form" class="btn btn-primary">{esc(L(code, 'btn_quote'))}</a>
              <a href="{CAL}" class="btn btn-secondary" target="_blank" rel="noopener noreferrer">{esc(L(code, 'btn_call'))}</a>
            </div>
            <p class="buy-box-note">{esc(t['price_note'])}</p>
          </div>
          <p class="g1p-note">{t['not_edu_plus'].format(edu_plus=edu_plus)}</p>
        </div>
      </div>
    </div>
  </section>

{section(t['upg_h2'], upgrades(code), 'aggiornamenti')}{section(t['specs_h2'], '<p>' + esc(t['specs_intro']) + '</p>' + specs_table(code), 'specs')}{section(t['family_h2'], '<p>' + esc(t['family_text']) + f' <a href="{fam}">{esc(t["family_link"])} →</a></p>')}
<section class="section hm-faq" id="faq"><div class="container"><h2>{esc(L(code, 'faq_h2'))}</h2>{faq_html(code)}</div></section>
<section class="section hm-src" style="padding-top:0"><div class="container"><h2>{esc(L(code, 'sources_h2'))}</h2>{sources_html(code)}</div></section>

  <section id="form" class="section" style="scroll-margin-top:120px;">
    <div class="container" style="max-width:720px;">
      <div class="section-header" style="text-align:center;">
        <p class="label">{'Contact' if en else 'Contatti'}</p>
        <h2>{esc(L(code, 'form_h2'))}</h2>
        <p class="section-sub">{esc(L(code, 'form_sub'))}</p>
      </div>
      <form class="quote-form-top" data-product="Unitree G1+ (G1 Plus)" style="max-width:100%;">
        <input type="text" name="nome" placeholder="{esc(f['name'])}" required>{company}
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
    d = json.loads((ROOT / "data" / "lingue" / f"{code}.json").read_text(encoding="utf-8"))
    d["code"] = code
    u, t = d["ui"], T[code]
    own_rel = page_path(code)
    own = f"{SITE}/{own_rel}"
    g1_name = d["families"]["g1"]["name"]
    crumbs = [(u["home"], f"{SITE}/{code}/"), (f"Unitree {g1_name}", f"{SITE}/{code}/unitree-g1.html")]
    head = lang_head(d, t["title"], t["desc"], own, alternates(), IMG, json_ld(code, crumbs))
    head = head.replace("</head>", G1P_CSS + "\n</head>", 1)
    _, _, body, footer = chrome(d)
    keys = "".join(f"<div><strong>{esc(v)}</strong><span>{esc(k)}</span></div>" for k, v in t["key"])
    edu_plus = "../en/prodotti/unitree-g1-edu-plus-en.html"
    media = (f'<div class="g1p-media"><img src="../{IMG}" alt="{esc(t["img_alt"])}" loading="lazy" width="900" height="1177">'
             f'<img src="../{IMG2}" alt="{esc(t["img2_alt"])}" loading="lazy" width="1600" height="1077"></div>')
    cta_html = cta(d).replace('<section class="section section-cta">', '<section class="section section-cta" id="quote">', 1)
    main = f"""<!-- HERO -->
<section class="collection-hero">
<div class="container">
{lang_bar(code, u['languages'])}
<p class="label"><a href="./" style="color:inherit">{esc(u['home'])}</a> · <a href="unitree-g1.html" style="color:inherit">Unitree {esc(g1_name)}</a></p>
<h1>{NAME}</h1>
<p class="lead">{esc(t['lead'])}</p>
<div class="hero-meta">
{keys}
</div>
<p class="g1p-price"><strong>{esc(t['price'])}</strong> · G1+ / G1+ EDU</p>
<p>{esc(t['price_note'])} <a href="#quote">{esc(u['quote_title'])} →</a></p>
<p class="g1p-note">{t['not_edu_plus'].format(edu_plus=edu_plus)}</p>
</div>
</section>
{section(t['upg_h2'], upgrades(code) + media, 'upgrades')}{section(t['specs_h2'], '<p>' + esc(t['specs_intro']) + '</p>' + specs_table(code), 'specs')}{section(t['family_h2'], '<p>' + esc(t['family_text']) + f' <a href="unitree-g1.html">{esc(t["family_link"])} →</a></p>')}{cta_html}
<section class="section hm-faq" id="faq"><div class="container"><h2>{esc(u['faq'])}</h2>{faq_html(code)}</div></section>
<section class="section hm-src" style="padding-top:0"><div class="container"><h2>{esc(u['sources'])}</h2>{sources_html(code)}</div></section>
"""
    return ("<!-- generato da scripts/genera_g1_plus.py -->\n" + head + body + main + footer
            + '\n<script defer src="../script.js"></script>\n</body>\n</html>\n')


def main() -> None:
    for code in LANGS:
        out = ROOT / page_path(code)
        out.write_text(product_page(code) if code in ("it", "en") else lang_page(code), encoding="utf-8")
        print("scritta", page_path(code))


if __name__ == "__main__":
    main()
