"""Aggiunge i link hreflang it/en/x-default alle coppie di pagine IT/EN.

Coppie: pagina.html <-> en/pagina-en.html, prodotti/x.html <-> en/prodotti/x-en.html.
- Se la pagina IT omonima e' un rimando (meta refresh o canonical verso un'altra pagina, es.
  catalogo-amr.html -> amr.html), la coppia si fa con la pagina IT reale indicata dal canonical.
- Coppie con una pagina noindex o rimando (es. en/software-en.html, schede EN dismesse) vengono
  saltate: niente hreflang verso pagine che non vanno in indice.
- Gli hreflang delle altre lingue (de, fr, ... sulle pagine hub) restano: si aggiornano solo it/en/x-default.
Idempotente. Lanciato anche da regenerate_from_public.py.
Uso: python scripts/add_hreflang.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://abrarobotics.com/"
OLD = re.compile(r'\n?[ \t]*<link[^>]*hreflang=[^>]*>')
ANCHOR = re.compile(r'<link[^>]*rel="canonical"[^>]*>|</title>')


def head_of(t):
    return t.split("</head>", 1)[0]


def canonical(head):
    m = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', head) or re.search(r'<link[^>]*href="([^"]+)"[^>]*rel="canonical"', head)
    return m.group(1) if m else None


def status(rel):
    """'ok', 'rimando' (meta refresh o canonical altrove), 'noindex' o None se il file non esiste."""
    p = ROOT / rel
    if not p.is_file():
        return None
    head = head_of(p.read_text(encoding="utf-8"))
    if re.search(r'http-equiv=["\']refresh', head, re.I):
        return "rimando"
    c = canonical(head)
    if c and c not in (BASE + rel, BASE + rel.replace("index.html", "")):
        return "rimando"
    m = re.search(r'<meta[^>]*name="robots"[^>]*>', head, re.I)
    if m and "noindex" in m.group(0).lower():
        return "noindex"
    return "ok"


def real_it(it):
    """Pagina IT reale della coppia: quella omonima, o quella indicata dal canonical se l'omonima e' un rimando."""
    st = status(it)
    if st == "ok":
        return it
    if st == "rimando":
        c = canonical(head_of((ROOT / it).read_text(encoding="utf-8")))
        if c and c.startswith(BASE):
            target = c[len(BASE):] or "index.html"
            own_en = "en/" + target.replace(".html", "-en.html")
            if status(target) == "ok" and status(own_en) != "ok":  # se ha gia' la sua EN, resta quella
                return target
    return None


def tag(path, it, en):
    t = path.read_text(encoding="utf-8")
    head = head_of(t)
    old = []
    for m in OLD.finditer(head):
        lang = re.search(r'hreflang="([^"]+)"', m.group(0))
        href = re.search(r'href="([^"]+)"', m.group(0))
        if lang and href:
            old.append((lang.group(1), href.group(1)))
    others = []
    for lang, href in old:
        if lang not in ("it", "en", "x-default") and lang not in dict(others):
            others.append((lang, href))
    want = [("it", BASE + it), ("en", BASE + en)] + others + [("x-default", BASE + it)]
    if dict(old) == dict(want) and len({l for l, _ in old if l in ("it", "en", "x-default")}) == 3:
        return False  # stessi hreflang (ordine e doppioni a parte): niente da riscrivere
    rest = OLD.sub("", head)
    m = ANCHOR.search(rest)
    if not m:
        return False
    tags = "".join(f'\n<link rel="alternate" hreflang="{lang}" href="{href}"/>' for lang, href in want)
    new = rest[:m.end()] + tags + rest[m.end():] + t[len(head):]
    if new != t:
        path.write_text(new, encoding="utf-8", newline="")
        return True
    return False


def drop(path, href):
    """Toglie dalla pagina gli hreflang che puntano a href."""
    t = path.read_text(encoding="utf-8")
    head = head_of(t)
    rest = OLD.sub(lambda m: "" if f'href="{href}"' in m.group(0) else m.group(0), head)
    if rest == head:
        return False
    path.write_text(rest + t[len(head):], encoding="utf-8", newline="")
    return True


def main():
    changed = skipped = 0
    for en_path in sorted((ROOT / "en").rglob("*-en.html")):
        en = en_path.relative_to(ROOT).as_posix()
        it = en[3:].replace("-en.html", ".html")
        if not (ROOT / it).exists():
            continue
        it = real_it(it)
        if not it or status(en) != "ok":
            if it:  # la pagina IT reale non deve indicare come EN una pagina noindex o un rimando
                changed += drop(ROOT / it, BASE + en)
            skipped += 1
            continue
        it_url = "" if it == "index.html" else it
        changed += tag(ROOT / it, it_url, en) + tag(en_path, it_url, en)
    print("hreflang aggiornati:", changed, "· coppie saltate (noindex/rimando):", skipped)


if __name__ == "__main__":
    main()
