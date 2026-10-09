#!/usr/bin/env python3
"""SEO schede prodotto Unitree per le ricerche "unitree <modello> prezzo / price".

Per ogni scheda Unitree italiana (prodotti/unitree-*.html) e inglese
(en/prodotti/unitree-*-en.html), redirect esclusi:
- title "<Nome> prezzo | Abra Robotics" / "<Name> price | Abra Robotics" (entro 60
  caratteri se possibile, mai duplicati: in caso di collisione resta il title attuale);
- meta description (e og) con il prezzo mostrato in pagina: "da X € IVA esclusa" /
  "from €X excl. VAT", 120-158 caratteri;
- breadcrumb visibile e BreadcrumbList: Home > categoria > Unitree <famiglia> > prodotto;
- Product JSON-LD: mpn = sku e politica resi (solo i fatti di politica-resi.html).
Cobot e AMR: solo title "prezzo/price". Idempotente.
Uso: python3 scripts/seo_schede_prezzo.py  (lanciato anche da regenerate_from_public.py)"""
from __future__ import annotations

import html as H
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_title_desc import seo_desc  # noqa: E402

SITE = "https://abrarobotics.com/"
MAX_TITLE = 60

# famiglia -> (etichetta, hub IT, hub EN, categoria del robot: "umanoidi"/"quadrupedi"/None)
FAMILIES = {
    "g1": ("Unitree G1", "g1.html", "en/g1-en.html", "umanoidi"),
    "g1-d": ("Unitree G1-D", "g1-d.html", "en/g1-d-en.html", "umanoidi"),
    "r1": ("Unitree R1", "r1.html", "en/r1-en.html", "umanoidi"),
    "r1-d": ("Unitree R1-D", "r1-d.html", "en/r1-d-en.html", "umanoidi"),
    "h2": ("Unitree H2", "h2.html", "en/h2-en.html", "umanoidi"),
    "go2": ("Unitree Go2", "go2.html", "en/go2-en.html", "quadrupedi"),
    "as2": ("Unitree AS2", "as2.html", "en/as2-en.html", "quadrupedi"),
    "a2": ("Unitree A2", "a2.html", "en/a2-en.html", "quadrupedi"),
    "b2": ("Unitree B2", "b2.html", "en/b2-en.html", "quadrupedi"),
    "z1": ("Unitree Z1 e D1", "z1.html", "en/z1-en.html", None),
}
FAMILY_LABEL_EN = {"z1": "Unitree Z1 & D1"}

# Politica resi (politica-resi.html): reso entro 14 giorni dal ricevimento, per posta,
# spese di spedizione del reso a carico del cliente, nessuna commissione.
RETURN_POLICY = {
    "@type": "MerchantReturnPolicy",
    "applicableCountry": "IT",
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 14,
    "returnMethod": "https://schema.org/ReturnByMail",
    "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
}

TAIL_IT = "Configurazione, consegna e supporto in Italia con Abra Robotics."
TAIL_EN = "Configuration, delivery and support from Abra Robotics, Italy."
TAIL_IT_SHORT = "Supporto in Italia con Abra Robotics."
TAIL_EN_SHORT = "Support from Abra Robotics, Italy."


def family_of(slug: str) -> str | None:
    s = slug.replace("-en.html", ".html")
    if re.match(r"unitree-g1-?d-", s) or s.startswith("unitree-g1d"):
        return "g1-d"
    if re.match(r"unitree-r1-a[57]-d-", s) or s in ("unitree-r1-d.html",) or s.startswith("unitree-r1a-d"):
        return "r1-d"
    for prefix, fam in (("unitree-g1", "g1"), ("unitree-r1", "r1"), ("unitree-h2", "h2"), ("unitree-go2", "go2"),
                        ("unitree-as2", "as2"), ("unitree-a2", "a2"), ("unitree-b2", "b2"), ("unitree-arm-z1", "z1"),
                        ("unitree-z1", "z1"), ("unitree-d1", "z1")):
        if s.startswith(prefix):
            return fam
    return None


def fmt_it(p: float) -> str:
    s = f"{p:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s[:-3] if s.endswith(",00") else s


def fmt_en(p: float) -> str:
    s = f"{p:,.2f}"
    return s[:-3] if s.endswith(".00") else s


def price_title(name: str, en: bool) -> str:
    word = "price" if en else "prezzo"
    for cand in (f"{name} {word} | Abra Robotics", f"{name} {word} | Abra"):
        if len(cand) <= MAX_TITLE:
            return cand
    return f"{name} {word}"


def ld_blocks(s: str):
    for m in re.finditer(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)', s):
        try:
            yield m, json.loads(m.group(2))
        except ValueError:
            yield m, None


def product_of(s: str):
    for m, j in ld_blocks(s):
        for x in (j if isinstance(j, list) else [j]) if j else []:
            if isinstance(x, dict) and x.get("@type") == "Product":
                return x
    return None


def visible_name(s: str) -> str | None:
    nav = re.search(r'<nav[^>]*class="breadcrumb"[^>]*>([\s\S]*?)</nav>', s) or re.search(r'<nav[^>]*breadcrumb[^>]*>([\s\S]*?)</nav>', s)
    if not nav:
        return None
    spans = re.findall(r"<span>([^<]+)</span>", nav.group(1))
    return H.unescape(spans[-1]).strip() if spans else None


def strip_price_sentences(desc: str, name: str) -> str:
    """Toglie le frasi di prezzo (anche quella generata qui) e la coda standard: resta la descrizione."""
    for tail in (TAIL_IT, TAIL_EN, TAIL_IT_SHORT, TAIL_EN_SHORT):
        desc = desc.replace(tail, " ")
    # niente spezzature dopo "excl." / "IVA" abbreviati: "excl. VAT." resta una frase sola
    parts = re.split(r"(?<=[.!?])(?<!excl\.)(?<!incl\.)\s+", desc.strip())
    keep = [p for p in parts if p and "€" not in p]
    out = " ".join(keep).strip()
    if out.lower().startswith(name.lower()):
        out = out[len(name):].lstrip(" :.—–-")
        out = out[:1].upper() + out[1:]
    return out


def new_desc(desc: str, name: str, price: float, en: bool) -> str:
    head = f"{name} price: from €{fmt_en(price)} excl. VAT." if en else f"{name}: prezzo da {fmt_it(price)} € IVA esclusa."
    rest = strip_price_sentences(desc, name)
    text = seo_desc((head + " " + rest).strip())
    if len(text) < 120 and "Abra Robotics" not in text:
        for tail in ((TAIL_EN, TAIL_EN_SHORT) if en else (TAIL_IT, TAIL_IT_SHORT)):
            if len(text) + 1 + len(tail) <= 158:
                return text + " " + tail
    return text


def set_meta(s: str, name: str, value: str) -> str:
    v = H.escape(value, quote=True)
    for rx in (rf'(<meta[^>]*name="{name}"[^>]*content=")[^"]*(")', rf'(<meta[^>]*content=")[^"]*("[^>]*name="{name}")',
               rf'(<meta[^>]*property="{name}"[^>]*content=")[^"]*(")', rf'(<meta[^>]*content=")[^"]*("[^>]*property="{name}")'):
        if re.search(rx, s):
            return re.sub(rx, lambda m: m.group(1) + v + m.group(2), s, count=1)
    return s


def rebuild_breadcrumb(s: str, rel: str, fam: str | None, en: bool, name: str) -> str:
    nav = re.search(r'(<nav[^>]*class="breadcrumb"[^>]*>|<nav[^>]*aria-label="Breadcrumb"[^>]*>)([\s\S]*?)(</nav>)', s)
    if not nav:
        return s
    links = [(h, H.unescape(t).strip()) for h, t in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', nav.group(2))]
    home = links[0] if links else ("../index-en.html" if en else "../index.html", "Home")
    fam_hubs = {v[2 if en else 1].split("/")[-1] for v in FAMILIES.values()}
    cats = [l for l in links[1:] if l[0].split("/")[-1] not in fam_hubs]
    cat = cats[0] if cats else None
    if fam and FAMILIES[fam][3] and (not cat or cat[0].split("/")[-1].replace("-en", "") in ("index.html", "catalogo-unitree.html", "catalogo.html")):
        c = FAMILIES[fam][3]
        cat = (f"../{c}-en.html" if en else f"../{c}.html", ("Humanoids" if c == "umanoidi" else "Quadrupeds") if en else c.capitalize())
    crumbs = [home] + ([cat] if cat else [])
    if fam:
        label = FAMILY_LABEL_EN.get(fam, FAMILIES[fam][0]) if en else FAMILIES[fam][0]
        hub = FAMILIES[fam][2] if en else FAMILIES[fam][1]
        crumbs.append(("../" + hub.split("/")[-1], label))
    sep = '<span class="breadcrumb-sep">›</span>'
    inner = "\n" + "\n".join(f'<a href="{h}">{H.escape(t, quote=False)}</a>\n{sep}' for h, t in crumbs) + f"\n<span>{H.escape(name, quote=False)}</span>\n"
    s = s[:nav.start(2)] + inner + s[nav.end(2):]
    # BreadcrumbList coerente con quello visibile (URL assoluti della stessa lingua)
    base = SITE + ("en/prodotti/" if en else "prodotti/")
    canon = (re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', s) or re.search(r'<link[^>]*href="([^"]+)"[^>]*rel="canonical"', s))
    canon = canon.group(1) if canon else SITE + rel

    def absu(h: str) -> str:
        if h.startswith("http"):
            return h
        u = base + h
        while "/../" in u:
            u = re.sub(r"[^/]+/\.\./", "", u, count=1)
        return u.replace(SITE + "index.html", SITE)

    items = [{"@type": "ListItem", "position": i + 1, "name": t, "item": absu(h)} for i, (h, t) in enumerate(crumbs)]
    items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "item": canon})
    bl = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    done = False
    for m, j in ld_blocks(s):
        if isinstance(j, dict) and j.get("@type") == "BreadcrumbList":
            s = s[:m.start(2)] + "\n" + json.dumps(bl, ensure_ascii=False, indent=2) + "\n" + s[m.end(2):]
            done = True
            break
    if not done:
        s = s.replace("</head>", '<script type="application/ld+json">\n' + json.dumps(bl, ensure_ascii=False, indent=2) + "\n</script>\n</head>", 1)
    return s


def fix_product_ld(s: str) -> str:
    for m, j in ld_blocks(s):
        if not isinstance(j, dict) or j.get("@type") != "Product":
            continue
        changed = False
        if j.get("sku") and not j.get("mpn"):
            j["mpn"] = j["sku"]; changed = True
        img = j.get("image")
        if isinstance(img, str) and not img.startswith("http"):
            j["image"] = SITE + img.lstrip("./"); changed = True
        off = j.get("offers")
        if isinstance(off, dict) and off.get("price") and off.get("hasMerchantReturnPolicy") != RETURN_POLICY:
            off["hasMerchantReturnPolicy"] = RETURN_POLICY; changed = True
        if changed:
            s = s[:m.start(2)] + "\n" + json.dumps(j, ensure_ascii=False, indent=2) + "\n" + s[m.end(2):]
        break
    return s


def page_price(s: str, prod: dict | None, en: bool) -> float | None:
    off = (prod or {}).get("offers")
    try:
        p = float(off.get("price")) if isinstance(off, dict) and off.get("price") else 0.0
    except (TypeError, ValueError):
        p = 0.0
    if p <= 0:
        return None
    body = s.split("</head>", 1)[-1]
    ints = f"{int(p):,}"
    return p if (ints.replace(",", ".") in body or ints in body) else None


def main() -> None:
    pages = []
    for f in sorted((ROOT / "prodotti").glob("*.html")) + sorted((ROOT / "en" / "prodotti").glob("*-en.html")):
        if f.name.startswith("_"):
            continue
        s = f.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in s:
            continue
        pages.append((f, s))
    plan = {}
    for f, s in pages:
        en = f.parent.name == "prodotti" and f.parent.parent.name == "en"
        name = visible_name(s)
        if not name or not (f.name.startswith("unitree-") or f.name.startswith("cobot-") or f.name.startswith("amr-")):
            continue
        if f.name.startswith("unitree-") and "unitree" not in name.lower():
            name = "Unitree " + name
        canon = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', s) or re.search(r'<link[^>]*href="([^"]+)"[^>]*rel="canonical"', s)
        if canon and not canon.group(1).endswith("/" + f.name):
            continue  # duplicato con canonical verso un'altra scheda: resta com'e'
        plan[f] = (en, name, price_title(name, en))
    # mai title duplicati: chi collide mantiene il title attuale
    seen = {}
    for f, (en, name, t) in plan.items():
        seen.setdefault(t, []).append(f)
    stats = {"title": 0, "desc": 0, "breadcrumb": 0, "ld": 0, "collisioni": 0}
    for f, s in pages:
        if f not in plan:
            continue
        o = s
        en, name, t = plan[f]
        rel = f.relative_to(ROOT).as_posix()
        if len(seen[t]) == 1:
            m = re.search(r"<title>([\s\S]*?)</title>", s)
            if m and H.unescape(m.group(1)).strip() != t:
                s = s.replace(m.group(0), f"<title>{H.escape(t, quote=False)}</title>", 1)
                s = set_meta(s, "og:title", t)
                stats["title"] += 1
        else:
            stats["collisioni"] += 1
        prod = product_of(s)
        p = page_price(s, prod, en)
        dm = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', s) or re.search(r'<meta[^>]*content="([^"]*)"[^>]*name="description"', s)
        if p and dm:
            nd = new_desc(H.unescape(dm.group(1)), name, p, en)
            if nd != H.unescape(dm.group(1)):
                s = set_meta(set_meta(s, "description", nd), "og:description", nd)
                stats["desc"] += 1
        if f.name.startswith("unitree-"):
            b = rebuild_breadcrumb(s, rel, family_of(f.name), en, name)
            if b != s:
                s = b; stats["breadcrumb"] += 1
            l = fix_product_ld(s)
            if l != s:
                s = l; stats["ld"] += 1
        if s != o:
            f.write_text(s, encoding="utf-8")
    print("schede prezzo:", stats)


if __name__ == "__main__":
    main()
