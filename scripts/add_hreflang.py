"""Aggiunge i link hreflang it/en/x-default alle coppie di pagine IT/EN.

Coppie: pagina.html <-> en/pagina-en.html, prodotti/x.html <-> en/prodotti/x-en.html.
Idempotente: rigenera i tag a ogni esecuzione. Lanciato anche da regenerate_from_public.py.
Uso: python scripts/add_hreflang.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://abrarobotics.com/"
OLD = re.compile(r'\n?[ \t]*<link[^>]*hreflang=[^>]*>')
ANCHOR = re.compile(r'<link[^>]*rel="canonical"[^>]*>|</title>')


def tag(path, it, en):
    t = path.read_text(encoding="utf-8")
    m = ANCHOR.search(OLD.sub("", t))
    if not m:
        return False
    t = OLD.sub("", t)
    tags = (f'\n<link rel="alternate" hreflang="it" href="{BASE}{it}"/>'
            f'\n<link rel="alternate" hreflang="en" href="{BASE}{en}"/>'
            f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{it}"/>')
    new = t[:m.end()] + tags + t[m.end():]
    if new != path.read_text(encoding="utf-8"):
        path.write_text(new, encoding="utf-8", newline="")
        return True
    return False


def main():
    changed = 0
    for en_path in sorted((ROOT / "en").rglob("*-en.html")):
        en = en_path.relative_to(ROOT).as_posix()
        it = en[3:].replace("-en.html", ".html")
        it_path = ROOT / it
        if not it_path.exists():
            continue
        it_url = "" if it == "index.html" else it
        changed += tag(it_path, it_url, en) + tag(en_path, it_url, en)
    print("hreflang aggiornati:", changed)


if __name__ == "__main__":
    main()
