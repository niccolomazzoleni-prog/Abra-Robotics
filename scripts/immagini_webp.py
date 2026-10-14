#!/usr/bin/env python3
"""Immagini piu' leggere: per ogni JPG/PNG usato dal sito crea accanto una versione .webp
ridimensionata (lato lungo max 1600 px, miniature max 800 px) e aggiorna i riferimenti:
<img src>, srcset delle pagine e i dati che i generatori e scripts/image-runtime.js leggono
(data/product-images.json, listini/pubblico/end-user.json, listini/pubblico/catalogo-manifest.json).
Gli originali restano (meta og:image, JSON-LD e link esterni continuano a funzionare).
Una versione .webp si usa solo se pesa almeno il 15% in meno dell'originale. Idempotente.
Uso: python3 scripts/immagini_webp.py [--prova]
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKIP = {".claude", ".git", "node_modules", "admin", "editor", "offerte-ai", "listini", "stripe", "apps-script"}
DATA = [ROOT / "data/product-images.json", ROOT / "listini/pubblico/end-user.json", ROOT / "listini/pubblico/catalogo-manifest.json"]
IMG_RE = re.compile(r"\.(png|jpe?g)$", re.I)


def pages() -> list[Path]:
    return [p for p in ROOT.rglob("*.html") if not (set(p.relative_to(ROOT).parts) & SKIP) and not p.name.startswith("_template")]


def local(base: Path, src: str) -> Path | None:
    src = src.split("?")[0].split("#")[0]
    if not src or re.match(r"^(https?:|data:|//)", src) or not IMG_RE.search(src):
        return None
    p = (ROOT / src.lstrip("/")) if src.startswith("/") else (base / src)
    p = Path(os.path.normpath(p))
    return p if p.is_file() and ROOT in p.parents else None


def webp_for(p: Path, cache: dict, prova: bool) -> Path | None:
    """Crea (se serve) la .webp accanto all'originale; None se non conviene."""
    if p in cache:
        return cache[p]
    w = p.with_suffix(".webp")
    if not w.exists() or w.stat().st_mtime < p.stat().st_mtime:
        if prova:
            cache[p] = w
            return w
        from PIL import Image  # solo quando serve convertire (in CI le .webp esistenti bastano)
        im = Image.open(p)
        im.load()
        alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        im = im.convert("RGBA" if alpha else "RGB")
        lato = 800 if "thumb" in p.as_posix() else 1600
        if max(im.size) > lato:
            im.thumbnail((lato, lato), Image.LANCZOS)
        im.save(w, "WEBP", quality=80, method=6)
    ok = prova or w.stat().st_size <= 0.85 * p.stat().st_size
    if not ok:
        w.unlink(missing_ok=True)
    cache[p] = w if ok else None
    return cache[p]


def main() -> None:
    prova = "--prova" in sys.argv
    cache: dict[Path, Path | None] = {}
    prima = dopo = 0
    cambiate = 0
    attr = re.compile(r'(<(?:img|source)\b[^>]*?\b(?:src|srcset|data-src)=")([^"]+)(")', re.I)
    for f in pages():
        s = f.read_text(encoding="utf-8")

        def one(src: str) -> str:
            p = local(f.parent, src.strip())
            if not p:
                return src
            w = webp_for(p, cache, prova)
            return IMG_RE.sub(".webp", src) if w else src

        def rep(m):
            v = m.group(2)
            if "," in v or re.search(r"\s\d+[wx]", v):  # srcset
                v = ", ".join(" ".join([one(part.split()[0])] + part.split()[1:]) for part in v.split(",") if part.strip())
            else:
                v = one(v)
            return m.group(1) + v + m.group(3)

        n = attr.sub(rep, s)
        if n != s:
            cambiate += 1
            if not prova:
                f.write_text(n, encoding="utf-8")
    # dati letti da generatori e image-runtime.js: percorsi dalla radice del sito
    def walk(x):
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        if isinstance(x, list):
            return [walk(v) for v in x]
        if isinstance(x, str) and IMG_RE.search(x) and not x.startswith("http"):
            p = local(ROOT, x)
            if p and webp_for(p, cache, prova):
                return IMG_RE.sub(".webp", x)
        return x
    for d in DATA:
        if not d.is_file():
            continue
        j = json.loads(d.read_text(encoding="utf-8"))
        n = walk(j)
        if n != j and not prova:
            d.write_text(json.dumps(n, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for p, w in cache.items():
        if w and w.exists():
            prima += p.stat().st_size
            dopo += w.stat().st_size
    print(f"pagine aggiornate: {cambiate}, immagini convertite: {sum(1 for w in cache.values() if w)}, "
          f"peso {prima / 1e6:.1f} MB -> {dopo / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
