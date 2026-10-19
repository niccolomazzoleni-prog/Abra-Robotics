#!/usr/bin/env python3
"""Articoli del blog nelle altre lingue: /en/blog/<slug>.html, /de/blog/<slug>.html, ...

Il testo lo scrive l'agente traduzioni (content-agent/traduci.sh) in un frammento HTML:
    <title>...</title>
    <meta name="description" content="..."/>
    <article class="article-wrap">...</article>
Questo script fa tutto il resto in modo deterministico:
  build <lingua> <slug> <frammento>  pagina completa partendo dall'articolo italiano (head, JSON-LD, hreflang,
                                     menu/footer inglesi, link verso le pagine della stessa lingua)
  sync <slug>                        hreflang reciproci tra l'articolo italiano e tutte le sue versioni
  check <lingua> <slug>              controlli prima della pubblicazione (uscita 1 se qualcosa non va)
  list                               articoli italiani e versioni esistenti
"""
from __future__ import annotations

import html as H
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from genera_hub_modelli import FAMILIES, template  # noqa: E402
from lingue_chrome import localize_chrome  # noqa: E402

SITE = "https://abrarobotics.com"
LANGS = ["en", "de", "fr", "es", "pl", "nl", "cs", "sv", "da", "no", "fi"]
HREFLANG = {"no": "nb"}
COMPETITORS = re.compile(r"meko|reichelt|quadruped\.de|eagle ?robots|mybotshop|generation ?robots|botland|funduino|robotshop|openelab|joybuy|scan\.co\.uk", re.I)
# frasi valide solo per l'Italia: nelle altre lingue non devono restare
ITALIA = re.compile(r"iperammortamento|sabatini|transizione 5\.0|credito d.imposta|spedizione e dazio|IVA esclusa|in italiano", re.I)


def lang_info(code: str) -> dict:
    if code == "en":
        return {"html_lang": "en", "og_locale": "en_GB", "name": "English", "home": "/en/index-en.html"}
    d = json.loads((ROOT / "data/lingue" / f"{code}.json").read_text(encoding="utf-8"))
    return {"html_lang": d["html_lang"], "og_locale": d["og_locale"], "name": d["name"], "home": f"/{code}/"}


def path_of(code: str, slug: str) -> Path:
    return ROOT / code / "blog" / f"{slug}.html"


def url_of(code: str | None, slug: str) -> str:
    return f"{SITE}/blog/{slug}.html" if code in (None, "it") else f"{SITE}/{code}/blog/{slug}.html"


def is_stub(p: Path) -> bool:
    return p.is_file() and 'http-equiv="refresh"' in p.read_text(encoding="utf-8", errors="ignore")[:5000]


def refresh_target(p: Path) -> str | None:
    m = re.search(r'http-equiv="refresh"[^>]*url=([^"]+)"', p.read_text(encoding="utf-8", errors="ignore"))
    return m.group(1) if m else None


def root_path(href: str, base: str = "/blog/") -> str:
    """href relativo all'articolo italiano -> percorso dalla radice del sito."""
    if href.startswith("/"):
        return href
    parts = [x for x in base.split("/") if x]
    for seg in href.split("/"):
        if seg == "..":
            parts = parts[:-1]
        elif seg not in ("", "."):
            parts.append(seg)
    return "/" + "/".join(parts)


IT_HUB = {f["it_page"]: k for k, f in FAMILIES.items()}


def localize(href: str, code: str) -> str:
    """Link interno -> la pagina migliore nella lingua `code` (stessa lingua, poi inglese, poi originale)."""
    if re.match(r"^(https?:|mailto:|tel:|#|data:)", href):
        return href
    frag = ""
    if "#" in href:
        href, frag = href.split("#", 1)
        frag = "#" + frag
    p = root_path(href)
    name = p.lstrip("/")
    if name in ("", "index.html"):
        return lang_info(code)["home"] + frag
    if name in IT_HUB:
        k = IT_HUB[name]
        if code != "en" and (ROOT / code / f"unitree-{k}.html").is_file():
            return f"/{code}/unitree-{k}.html{frag}"
        return "/" + FAMILIES[k]["en_page"] + frag
    m = re.match(r"blog/([a-z0-9-]+)\.html$", name)
    if m:
        for c in (code, "en"):
            if path_of(c, m.group(1)).is_file():
                return f"/{c}/blog/{m.group(1)}.html{frag}"
        return p + frag
    if name == "blog.html":
        return lang_info(code)["home"]
    # listino e finanziamenti: nelle lingue c'e' la sezione della home con prezzi e incentivi del paese
    if code != "en" and name in ("listino-unitree.html", "finanziamenti.html"):
        return lang_info(code)["home"] + ("#models" if name.startswith("listino") else "#incentives")
    m = re.match(r"prodotti/([a-z0-9-]+)\.html$", name)
    if m:
        en = ROOT / "en/prodotti" / f"{m.group(1)}-en.html"
        return (f"/en/prodotti/{m.group(1)}-en.html" if en.is_file() and not is_stub(en) else p) + frag
    m = re.match(r"([a-z0-9-]+)\.html$", name)
    if m:
        en = ROOT / "en" / f"{m.group(1)}-en.html"
        if en.is_file():
            if is_stub(en):
                t = refresh_target(en)
                if t:
                    t = t.replace(SITE, "")
                    return (t if t.startswith(("/", "http")) else root_path(t, "/en/")) + frag
            else:
                return f"/en/{m.group(1)}-en.html{frag}"
    return p + frag


def fix_links(s: str, code: str, base: str = "/blog/") -> str:
    def rep(m):
        attr, href = m.group(1), m.group(2)
        if attr == "src" or re.search(r"\.(css|js|png|jpe?g|webp|svg|ico|gif|avif)$", href.split("?")[0]):
            return f'{attr}="{href if re.match(r"^(https?:|data:)", href) else root_path(href, base)}"'
        return f'{attr}="{localize(href, code)}"'
    return re.sub(r'\b(href|src)="([^"]+)"', rep, s)


def faq_of(article: str) -> list[tuple[str, str]]:
    # tre forme nei post: <section class="article-faq" ...>, <div class="faq-item">, oppure h3+p dopo l'ultimo h2 prima delle fonti
    sec = re.search(r'<section class="article-faq"[^>]*>([\s\S]*?)</section>', article)
    if sec:
        body = sec.group(1)
    elif 'class="faq-item"' in article:
        body = "".join(re.findall(r'<div class="faq-item">([\s\S]*?)</div>', article))
    else:
        blocks = re.findall(r"<h2[^>]*>[^<]*</h2>\s*((?:<h3[^>]*>[\s\S]*?</h3>\s*<p>[\s\S]*?</p>\s*){2,})(?=<h2|</div>|<div|<p|<section|</article)", article)
        if not blocks:
            return []
        body = blocks[-1]
    out = []
    for q, a in re.findall(r"<h3[^>]*>([\s\S]*?)</h3>\s*<p>([\s\S]*?)</p>", body):
        strip = lambda x: H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x))).strip()  # noqa: E731
        out.append((strip(q), strip(a)))
    return out


def alternates(slug: str) -> str:
    rows = [("it", url_of("it", slug))] + [(HREFLANG.get(c, c), url_of(c, slug)) for c in LANGS if path_of(c, slug).is_file()]
    rows.append(("x-default", url_of("it", slug)))
    return "\n".join(f'<link href="{u}" hreflang="{h}" rel="alternate"/>' for h, u in rows)


def set_alternates(s: str, slug: str) -> str:
    s = re.sub(r'\n?<link href="[^"]*" hreflang="[^"]*" rel="alternate"/>', "", s)
    s = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*"/>', "", s)
    return re.sub(r'(<link rel="canonical" href="[^"]*"/>)', lambda m: m.group(1) + "\n" + alternates(slug), s, count=1)


def build(code: str, slug: str, frag_path: str) -> Path:
    src = (ROOT / "blog" / f"{slug}.html").read_text(encoding="utf-8")
    frag = Path(frag_path).read_text(encoding="utf-8")
    title = H.unescape(re.search(r"<title>([\s\S]*?)</title>", frag).group(1).strip())
    desc = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', frag).group(1).strip())
    art = re.search(r'<article class="article-wrap">[\s\S]*</article>', frag).group(0)
    L = lang_info(code)
    own = url_of(code, slug)

    head = src[: src.index("<body>")]
    head = re.sub(r'<html lang="[^"]*"', f'<html lang="{L["html_lang"]}"', src[: src.index("<head>")]) + head[head.index("<head>"):]
    head = re.sub(r"<title>[\s\S]*?</title>", f"<title>{H.escape(title, quote=False)}</title>", head, count=1)
    # description in entrambi gli ordini degli attributi
    head = re.sub(r'<meta (?:name="description" content="[^"]*"|content="[^"]*" name="description")\s*/?>', lambda m: f'<meta name="description" content="{H.escape(desc)}"/>', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*"/>', f'<link rel="canonical" href="{own}"/>', head, count=1)
    head = re.sub(r'<meta property="og:locale" content="[^"]*"/>', f'<meta property="og:locale" content="{L["og_locale"]}"/>', head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + H.escape(title) + '"', head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + H.escape(desc) + '"', head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*"', lambda m: m.group(1) + own + '"', head)

    # JSON-LD: articolo con titolo, descrizione, lingua e URL della versione; FAQ dalla traduzione
    def ld(m):
        try:
            j = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        items = j if isinstance(j, list) else [j]
        keep = []
        for x in items:
            t = x.get("@type") if isinstance(x, dict) else None
            if t in ("Article", "BlogPosting", "NewsArticle", "TechArticle"):
                x.update({"headline": title, "description": desc, "inLanguage": L["html_lang"], "url": own,
                          "mainEntityOfPage": {"@type": "WebPage", "@id": own}})
                keep.append(x)
            elif t == "FAQPage":
                faq = faq_of(art)
                if faq:
                    x["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
                    keep.append(x)
            elif t == "BreadcrumbList":
                continue  # il percorso italiano non vale per la versione tradotta
            else:
                keep.append(x)
        if not keep:
            return ""
        out = keep if isinstance(j, list) else keep[0]
        return m.group(1) + json.dumps(out, ensure_ascii=False, indent=2) + m.group(3)
    head = re.sub(r'(<script type="application/ld\+json">\s*)([\s\S]*?)(\s*</script>)', ld, head)
    head = fix_links(head, code)
    head = set_alternates(head, slug)

    # menu e footer: struttura del sito inglese, etichette tradotte da lingue_chrome
    _, _, en_body, en_footer = template(True)
    to_root = lambda s: re.sub(r'((?:href|src)=")(?!https?:|mailto:|tel:|/|#|data:)([^"]+)"', lambda m: m.group(1) + root_path(m.group(2), "/en/") + '"', s)  # noqa: E731
    body_top = to_root(en_body.replace("<body>", "", 1))
    footer = to_root(en_footer)
    art = fix_links(art, code)
    tail = src[src.index("</footer>") + len("</footer>"):]
    tail = re.sub(r'((?:href|src)=")(?!https?:|mailto:|tel:|/|#|data:)([^"]+)"', lambda m: m.group(1) + root_path(m.group(2)) + '"', tail)
    page = ("<!-- generato da scripts/blog_lingue.py da blog/" + slug + ".html -->\n" + head + "<body>\n" + body_top
            + "\n" + art + "\n" + footer + tail)
    page = localize_chrome(page, code)
    out = path_of(code, slug)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


def sync(slug: str) -> list[Path]:
    files = [ROOT / "blog" / f"{slug}.html"] + [path_of(c, slug) for c in LANGS if path_of(c, slug).is_file()]
    for f in files:
        s = f.read_text(encoding="utf-8")
        n = set_alternates(s, slug)
        if f.parent.parent != ROOT:  # traduzione: link agli altri articoli verso la migliore lingua esistente oggi
            code = f.parent.parent.name
            n = re.sub(r'href="/(?:[a-z]{2}/)?blog/([a-z0-9-]+)\.html(#[^"]*)?"',
                       lambda m: f'href="{localize(f"/blog/{m.group(1)}.html", code)}{m.group(2) or ""}"', n)
        if n != s:
            f.write_text(n, encoding="utf-8")
    return files


def check(code: str, slug: str) -> list[str]:
    from html.parser import HTMLParser
    f = path_of(code, slug)
    err = []
    if not f.is_file():
        return [f"manca {f}"]
    s = f.read_text(encoding="utf-8")
    try:
        HTMLParser().feed(s)
    except Exception as e:  # pragma: no cover
        err.append(f"HTML: {e}")
    for m in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', s):
        try:
            json.loads(m)
        except ValueError as e:
            err.append(f"JSON-LD: {e}")
    if f'<html lang="{lang_info(code)["html_lang"]}"' not in s:
        err.append("lang")
    if f'<link rel="canonical" href="{url_of(code, slug)}"/>' not in s:
        err.append("canonical")
    t = re.search(r"<title>([\s\S]*?)</title>", s)
    if not t or not (20 <= len(H.unescape(t.group(1))) <= 65):
        err.append(f"title {len(t.group(1)) if t else 0}")
    d = re.search(r'<meta name="description" content="([^"]*)"', s) or re.search(r'<meta content="([^"]*)" name="description"', s)
    if not d or not (70 <= len(H.unescape(d.group(1))) <= 165):
        err.append(f"description {len(d.group(1)) if d else 0}")
    for h in re.findall(r'(?:href|src)="(/[^"#?]*)', s):
        p = ROOT / h.lstrip("/")
        if h.endswith("/"):
            p = p / "index.html"
        if not p.exists():
            err.append(f"link rotto {h}")
    for h in re.findall(r'(?:href|src)="(?!https?:|mailto:|tel:|/|#|data:)([^"]+)"', s):
        err.append(f"link relativo rimasto {h}")
    text = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", s.split('<article class="article-wrap">', 1)[-1].split("<footer", 1)[0]))
    if COMPETITORS.search(text):
        err.append(f"concorrente: {COMPETITORS.search(text).group(0)}")
    if ITALIA.search(text):
        err.append(f"frase solo per l'Italia: {ITALIA.search(text).group(0)}")
    words = len(text.split())
    src_words = len(re.sub(r"<[^>]+>", " ", (ROOT / "blog" / f"{slug}.html").read_text(encoding="utf-8").split('<article class="article-wrap">', 1)[-1].split("<footer", 1)[0]).split())
    if words < 0.6 * src_words:
        err.append(f"testo troppo corto: {words} parole contro {src_words} dell'originale")
    return err


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "build":
        print(build(sys.argv[2], sys.argv[3], sys.argv[4]).relative_to(ROOT))
    elif cmd == "sync":
        for f in sync(sys.argv[2]):
            print(f.relative_to(ROOT))
    elif cmd == "check":
        e = check(sys.argv[2], sys.argv[3])
        print(json.dumps({"ok": not e, "errors": e}, ensure_ascii=False))
        sys.exit(1 if e else 0)
    else:
        for f in sorted((ROOT / "blog").glob("*.html")):
            if is_stub(f):
                continue
            have = [c for c in LANGS if path_of(c, f.stem).is_file()]
            print(f.stem, " ".join(have))


if __name__ == "__main__":
    main()
