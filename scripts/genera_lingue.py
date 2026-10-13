#!/usr/bin/env python3
"""Pagine Unitree nelle lingue europee (DE, FR, NL, DA, SV, NO, FI), generate dal listino pubblico.

Per ogni lingua in data/lingue/<codice>.json:
- /<codice>/index.html       pagina paese: modelli con prezzo "da", servizio, consegna e dazi per stato, incentivi per stato
- /<codice>/unitree-<fam>.html pagina modello: versioni e prezzi (listino), scelta, specifiche ufficiali, guida, FAQ
Prezzi e versioni: SOLO listini/pubblico/end-user.json (EUR, IVA esclusa). Testi: SOLO dal file della lingua.
Header/menu/footer dalla versione inglese (il supporto per queste lingue e' in inglese).
hreflang: ogni pagina modello e' collegata a IT, EN e alle altre lingue (anche le hub IT/EN, vedi genera_hub_modelli.py).
Idempotente. Uso: python3 scripts/genera_lingue.py [codice ...]
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from genera_hub_modelli import CAL, FAMILIES, HUB_CSS, SITE, load, template  # noqa: E402
from nomi_en import nome_en  # noqa: E402

DATA = ROOT / "data" / "lingue"
ORDER = ["de", "fr", "nl", "da", "sv", "no", "fi", "es", "pl", "cs", "uk"]
FAMILY_KEYS = ["go2", "as2", "a2", "b2", "g1", "g1-d", "h2", "r1", "r1-d", "z1"]
HREFLANG = {"no": "nb", "uk": "en-GB"}  # norvegese bokmal; uk = pagina paese inglese per il Regno Unito

UI_KEYS = ["home", "versions_prices", "table_version", "table_price", "table_link", "from", "excl_vat", "choose", "specs",
           "accessories", "delivery_short", "delivery_link", "quote_title", "quote_text", "btn_assess", "btn_call", "faq", "sources",
           "price_list_source", "versions_count", "families_label", "price_note", "support_badge", "faq_price_q", "faq_price_a",
           "faq_choose_q", "faq_what_q", "faq_delivery_q", "faq_delivery_a", "languages", "models_h2", "breadcrumb_family"]
FAM_KEYS = ["name", "type", "seo_title", "h1", "description", "lead", "choose", "specs", "guide", "faq"]


def langs() -> list[dict]:
    out = []
    for code in ORDER:
        p = DATA / f"{code}.json"
        if p.is_file():
            d = json.loads(p.read_text(encoding="utf-8"))
            d["code"] = code
            out.append(d)
    return out


def check(d: dict) -> list[str]:
    err = [f"ui.{k}" for k in UI_KEYS if k not in d.get("ui", {})]
    for k in ([] if d.get("landing_only") else FAMILY_KEYS):
        f = d.get("families", {}).get(k)
        if not f:
            err.append(f"families.{k}")
            continue
        err += [f"families.{k}.{x}" for x in FAM_KEYS if x not in f]
    for k in ("landing", "service", "delivery", "incentives", "markets", "price_format", "html_lang", "og_locale", "name"):
        if k not in d:
            err.append(k)
    return err


def money(x: float, d: dict) -> str:
    """Prezzo nel formato della lingua: price_format = {"thousands": ".", "pattern": "{n} €"}."""
    n = f"{x:,.0f}".replace(",", d["price_format"]["thousands"])
    return d["price_format"]["pattern"].replace("{n}", n)


def fam_url(code: str, key: str) -> str:
    return f"{SITE}/{code}/unitree-{key}.html"


def alternates(key: str | None, all_langs: list[dict]) -> str:
    """hreflang: pagina modello in tutte le lingue + IT/EN; per la pagina paese solo le pagine paese + EN."""
    rows = []
    if key:
        f = FAMILIES[key]
        if not f.get("en_only") and (ROOT / f["it_page"]).is_file():
            rows.append(("it", f"{SITE}/{f['it_page']}"))
        rows.append(("en", f"{SITE}/{f['en_page']}"))
        rows += [(HREFLANG.get(L["code"], L["code"]), fam_url(L["code"], key)) for L in all_langs if not L.get("landing_only")]
        rows.append(("x-default", f"{SITE}/{f['it_page']}" if rows[0][0] == "it" else f"{SITE}/{f['en_page']}"))  # come le hub IT/EN
    else:
        # pagine paese: gruppo tra loro (home IT/EN hanno contenuti diversi, non sono traduzioni)
        rows += [(HREFLANG.get(L["code"], L["code"]), f"{SITE}/{L['code']}/") for L in all_langs]
        rows.append(("x-default", f"{SITE}/en/index-en.html"))
    return "\n".join(f'<link rel="alternate" hreflang="{h}" href="{u}"/>' for h, u in rows)


def chrome(d: dict) -> tuple[str, str, str, str]:
    """Header/footer della versione inglese, con link relativi riportati a /en/ e lingua della pagina."""
    head_prefix, style, body, footer = template(True)

    def fix(s: str) -> str:
        return re.sub(r'((?:href|src)=")(?!https?:|mailto:|tel:|/|#|\.\./|data:)([^"]+)"', r'\1../en/\2"', s)

    head_prefix = re.sub(r'<html lang="[^"]*"', f'<html lang="{d["html_lang"]}"', head_prefix)
    return fix(head_prefix), style, fix(body), fix(footer)


def link_product(slug: str) -> str:
    en_slug = slug.replace(".html", "-en.html")
    if (ROOT / "en/prodotti" / en_slug).is_file():
        return f"../en/prodotti/{en_slug}"
    return f"../prodotti/{slug}"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def para(t: str) -> str:
    """Testo dei file lingua: HTML fidato limitato (a, strong, em) scritto da noi; tutto il resto gia' testo."""
    return t


def lang_bar(d: dict, key: str | None, all_langs: list[dict]) -> str:
    items = []
    if key:
        f = FAMILIES[key]
        if (ROOT / f["it_page"]).is_file():
            items.append(f'<a href="../{f["it_page"]}" hreflang="it">Italiano</a>')
        items.append(f'<a href="../{f["en_page"]}" hreflang="en">English</a>')
        items += [f'<a href="../{L["code"]}/unitree-{key}.html" hreflang="{HREFLANG.get(L["code"], L["code"])}"'
                  f'{" aria-current=\"page\"" if L["code"] == d["code"] else ""}>{esc(L["name"])}</a>' for L in all_langs if not L.get("landing_only")]
    else:
        items.append('<a href="../" hreflang="it">Italiano</a>')
        items.append('<a href="../en/index-en.html" hreflang="en">English</a>')
        items += [f'<a href="../{L["code"]}/" hreflang="{HREFLANG.get(L["code"], L["code"])}"'
                  f'{" aria-current=\"page\"" if L["code"] == d["code"] else ""}>{esc(L["name"])}</a>' for L in all_langs]
    return f'<nav class="hm-langs" aria-label="{esc(d["ui"]["languages"])}">{" · ".join(items)}</nav>'


LANG_CSS = """<style id="lingue-css">
.hm-langs{font-size:.85rem;margin:0 0 14px;color:var(--gray-600)}.hm-langs a{color:inherit}.hm-langs a[aria-current]{font-weight:700;color:var(--black)}
.hm-badge{display:inline-block;padding:4px 10px;border:1px solid var(--gray-200);border-radius:999px;font-size:.85rem;margin-top:10px}
.hm-country{border:1px solid var(--gray-200);border-radius:12px;padding:16px 18px;margin:12px 0}.hm-country h3{margin:0 0 6px;font-size:1.05rem}
.hm-country ul{margin:6px 0 0 18px}.hm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.hm-grid a{display:block;border:1px solid var(--gray-200);border-radius:12px;padding:14px 16px;color:var(--black);text-decoration:none}
.hm-grid a span{display:block;color:var(--gray-600);font-size:.9rem;margin-top:4px}
</style>"""


def head(d: dict, title: str, desc: str, own: str, alt: str, image: str, lds: list[dict]) -> str:
    head_prefix, style, _, _ = chrome(d)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f"""{head_prefix}<title>{esc(title)}</title>
{alt}
<meta content="{esc(desc)}" name="description"/>
<meta content="index, follow" name="robots"/>
<link href="{own}" rel="canonical"/>
<link href="../favicon.ico" rel="icon" sizes="any"/>
<link href="../images/favicon-32x32.png" rel="icon" type="image/png" sizes="32x32"/>
<link href="../images/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="../style.css" rel="stylesheet"/>
{style}
{HUB_CSS}
{LANG_CSS}
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Abra Robotics"/>
<meta property="og:title" content="{esc(title)}"/>
<meta property="og:description" content="{esc(desc)}"/>
<meta property="og:url" content="{own}"/>
<meta property="og:image" content="{SITE}/{image}"/>
<meta property="og:locale" content="{d['og_locale']}"/>
<meta name="twitter:card" content="summary_large_image"/>
{ld}
</head>
"""


def faq_ld(faq: list[tuple[str, str]]) -> dict:
    strip = lambda s: re.sub(r"<[^>]+>", "", s)  # noqa: E731
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]}


def cta(d: dict) -> str:
    u = d["ui"]
    return f"""<section class="section section-cta"><div class="container" style="text-align:center">
<h2>{esc(u['quote_title'])}</h2>
<p>{esc(u['quote_text'])}</p>
<p style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:20px"><a class="btn btn-primary" href="../en/assessment-en.html">{esc(u['btn_assess'])}</a><a class="btn btn-secondary" href="{CAL}" target="_blank" rel="noopener noreferrer">{esc(u['btn_call'])}</a></p>
</div></section>"""


def section(h2: str, inner: str, anchor: str = "") -> str:
    a = f' id="{anchor}"' if anchor else ""
    return f'<section class="section hm-guide" style="padding-top:0"{a}><div class="container"><h2>{esc(h2)}</h2>{inner}</div></section>\n'


def family_page(d: dict, key: str, data: dict, all_langs: list[dict]) -> str:
    u, F, f = d["ui"], d["families"][key], FAMILIES[key]
    code = d["code"]
    own = fam_url(code, key)
    name = F["name"]
    robots, acc = data["robots"], data["acc"]
    rows = robots or acc
    prices = [r["price"] for r in rows if r["price"]]
    low, high = (min(prices), max(prices)) if prices else (None, None)
    fill = lambda s: s.replace("{name}", name).replace("{low}", money(low, d) if low else "").replace("{high}", money(high, d) if high else "")  # noqa: E731
    title, desc = fill(F["seo_title"]), fill(F["description"])

    tr = "\n".join(
        f'<tr><td><a href="{link_product(r["slug"])}">{esc(nome_en(r["name"]))}</a></td>'
        f'<td class="p">{esc(u["from"].replace("{p}", money(r["price"], d)))}</td>'
        f'<td><a href="{link_product(r["slug"])}">{esc(u["table_link"])} →</a></td></tr>'
        for r in rows if r["price"])
    table = (f'<div class="hm-wrap"><table class="hm-table"><thead><tr><th>{esc(u["table_version"])}</th><th>{esc(u["table_price"])}</th><th></th></tr></thead>'
             f'<tbody>\n{tr}\n</tbody></table></div>')
    choose = "".join(f"<p><strong>{esc(a)}</strong>: {para(b)}</p>" for a, b in F["choose"])
    specs = "".join(f'<div><span>{esc(a)}</span><strong>{esc(b)}</strong></div>' for a, b in F["specs"])
    guide = "".join(section(h, "".join(f"<p>{para(p)}</p>" for p in ps)) for h, ps in F["guide"])
    acc_html = ""
    if robots and acc:
        acc_html = section(fill(u["accessories"]), '<ul class="hm-acc">' + "".join(
            f'<li><a href="{link_product(a["slug"])}">{esc(nome_en(a["name"]))}<span>{esc(u["from"].replace("{p}", money(a["price"], d)))}</span></a></li>'
            for a in acc[:24] if a["price"]) + "</ul>")
    faq = []
    if low:
        faq.append((fill(u["faq_price_q"]), fill(u["faq_price_a"])))
    faq.append((fill(u["faq_choose_q"]), " ".join(f"{a}: {re.sub(r'<[^>]+>', '', b)}" for a, b in F["choose"])))
    faq += [(fill(q), fill(a)) for q, a in F["faq"]]
    faq.append((fill(u["faq_delivery_q"]), fill(u["faq_delivery_a"])))
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{para(a)}</p></details>" for q, a in faq)

    srcs = [f["source"]] + ([f["source2"]] if f.get("source2") else [])
    sources = "".join(f'<li><a href="{x}" target="_blank" rel="noopener">{x}</a></li>' for x in srcs)
    ld_product = {"@context": "https://schema.org", "@type": "Product", "name": f"Unitree {name}", "brand": {"@type": "Brand", "name": "Unitree"},
                  "image": f"{SITE}/{f['image']}", "description": desc, "url": own}
    if low:
        ld_product["offers"] = {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": f"{low:.2f}", "highPrice": f"{high:.2f}",
                                "offerCount": len(prices), "seller": {"@type": "Organization", "name": "Abra Robotics", "url": SITE}}
    ld_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": u["home"], "item": f"{SITE}/{code}/"},
        {"@type": "ListItem", "position": 2, "name": f"Unitree {name}", "item": own}]}
    _, _, body, footer = chrome(d)
    fam_links = "".join(f'<a href="unitree-{k}.html">Unitree {esc(d["families"][k]["name"])}</a>' for k in FAMILY_KEYS if k != key)
    main = f"""<!-- HERO -->
<section class="collection-hero">
<div class="container">
{lang_bar(d, key, all_langs)}
<p class="label"><a href="./" style="color:inherit">{esc(u['home'])}</a> · {esc(F['type'])}</p>
<h1>{esc(fill(F['h1']))}</h1>
<p class="lead">{para(fill(F['lead']))}</p>
<div class="hero-meta">
<div><strong>{len(prices)}</strong><span>{esc(u['versions_count'])}</span></div>
{('<div><strong>' + esc(u['from'].replace('{p}', money(low, d))) + '</strong><span>' + esc(u['excl_vat']) + '</span></div>') if low else ''}
<div><strong>EN</strong><span>{esc(u['support_badge'])}</span></div>
</div>
<div class="hm-fam">{fam_links}</div>
</div>
</section>
<section class="section" style="padding-top:24px"><div class="container">
<h2>{esc(fill(u['versions_prices']))}</h2>
<p>{para(u['price_note'])}</p>
{table}
</div></section>
{section(fill(u['choose']), '<div class="hm-choose">' + choose + '</div>')}
{section(fill(u['specs']), '<div class="hm-specs">' + specs + '</div>')}
{guide}{acc_html}{section(u['delivery_short'], '<p>' + para(fill(u['delivery_link'])) + '</p>')}
{cta(d)}
<section class="section hm-faq" id="faq"><div class="container"><h2>{esc(u['faq'])}</h2>{faq_html}</div></section>
<section class="section hm-src" style="padding-top:0"><div class="container"><h2>{esc(u['sources'])}</h2><ul>{sources}<li><a href="../listini/pubblico/end-user.json">{esc(u['price_list_source'])}</a></li></ul></div></section>
"""
    return ("<!-- generato da scripts/genera_lingue.py -->\n"
            + head(d, title, desc, own, alternates(key, all_langs), f["image"], [ld_product, ld_bc, faq_ld(faq)])
            + body + main + footer + '\n<script defer src="../script.js"></script>\n</body>\n</html>\n')


def landing_page(d: dict, data: dict, all_langs: list[dict]) -> str:
    u, L = d["ui"], d["landing"]
    code = d["code"]
    own = f"{SITE}/{code}/"
    cards = []
    for k in FAMILY_KEYS:
        rows = data[k]["robots"] or data[k]["acc"]
        prices = [r["price"] for r in rows if r["price"]]
        low = min(prices) if prices else None
        price = esc(u["from"].replace("{p}", money(low, d))) + " " + esc(u["excl_vat"]) if low else ""
        href = f'../{FAMILIES[k]["en_page"]}' if d.get("landing_only") else f"unitree-{k}.html"
        F = d.get("families", {}).get(k) or {"name": FAMILIES[k].get("name_en", FAMILIES[k]["name"]), "type": FAMILIES[k]["type_en"]}
        cards.append(f'<a href="{href}"><strong>Unitree {esc(F["name"])}</strong><span>{esc(F["type"])}</span><span>{price}</span></a>')
    grid = section(u["models_h2"], '<div class="hm-grid">' + "".join(cards) + "</div>", "models")
    sections = "".join(section(s["h2"], "".join(f"<p>{para(p)}</p>" for p in s["paragraphs"])) for s in L["sections"])
    S = d["service"]
    service = section(S["h2"], "".join(f"<p>{para(p)}</p>" for p in S["paragraphs"]), "service")
    D = d["delivery"]
    deliv = "".join(
        f'<div class="hm-country"><h3>{esc(c["name"])}</h3>' + "".join(f"<p>{para(p)}</p>" for p in c["paragraphs"])
        + ("<ul>" + "".join(f'<li><a href="{esc(s)}" target="_blank" rel="noopener">{esc(s)}</a></li>' for s in c.get("sources", [])) + "</ul>" if c.get("sources") else "")
        + "</div>" for c in D["countries"])
    delivery = section(D["h2"], "".join(f"<p>{para(p)}</p>" for p in D["intro"]) + deliv, "delivery")
    I = d["incentives"]
    inc = "".join(
        f'<div class="hm-country"><h3>{esc(c["name"])}</h3><ul>' + "".join(
            f'<li><strong>{esc(i["name"])}</strong>: {para(i["text"])} <a href="{esc(i["url"])}" target="_blank" rel="noopener">{esc(I.get("link_label", "↗"))}</a></li>'
            for i in c["items"]) + "</ul></div>" for c in I["countries"])
    incentives = section(I["h2"], "".join(f"<p>{para(p)}</p>" for p in I["intro"]) + inc + f'<p><em>{para(I["disclaimer"])}</em></p>', "incentives")
    faq = [(q, a) for q, a in L.get("faq", [])]
    faq_html = ("<section class=\"section hm-faq\" id=\"faq\"><div class=\"container\"><h2>" + esc(u["faq"]) + "</h2>"
                + "".join(f"<details><summary>{esc(q)}</summary><p>{para(a)}</p></details>" for q, a in faq) + "</div></section>") if faq else ""
    ld_org = {"@context": "https://schema.org", "@type": "Organization", "name": "Abra Robotics", "url": SITE,
              "areaServed": [m["country"] for m in d["markets"]], "knowsLanguage": ["en", "it"]}
    _, _, body, footer = chrome(d)
    main = f"""<!-- HERO -->
<section class="collection-hero">
<div class="container">
{lang_bar(d, None, all_langs)}
<p class="label">{esc(u['families_label'])}</p>
<h1>{esc(L['h1'])}</h1>
<p class="lead">{para(L['lead'])}</p>
<span class="hm-badge">{esc(u['support_badge'])}</span>
</div>
</section>
{grid}{sections}{service}{delivery}{incentives}{cta(d)}
{faq_html}
"""
    lds = [ld_org] + ([faq_ld(faq)] if faq else [])
    return ("<!-- generato da scripts/genera_lingue.py -->\n"
            + head(d, L["title"], L["description"], own, alternates(None, all_langs), "images/prodotti/2026/famiglia-g1.png", lds)
            + body + main + footer + '\n<script defer src="../script.js"></script>\n</body>\n</html>\n')


def main() -> None:
    all_langs = langs()
    only = set(sys.argv[1:])
    data = load()
    bad = False
    for d in all_langs:
        if only and d["code"] not in only:
            continue
        err = check(d)
        if err:
            print(f"{d['code']}: campi mancanti: {', '.join(err)}")
            bad = True
            continue
        out = ROOT / d["code"]
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(landing_page(d, data, all_langs), encoding="utf-8")
        if d.get("landing_only"):
            print(f"{d['code']}: 1 pagina paese (modelli: hub inglesi)")
            continue
        for k in FAMILY_KEYS:
            (out / f"unitree-{k}.html").write_text(family_page(d, k, data[k], all_langs), encoding="utf-8")
        print(f"{d['code']}: 1 pagina paese + {len(FAMILY_KEYS)} pagine modello")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
