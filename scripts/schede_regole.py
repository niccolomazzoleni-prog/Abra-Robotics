#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regole condivise sulle schede prodotto (usate da genera_sitemap.py e seo_schede_prezzo.py).

- tipo_unitree(slug): robot / accessorio / mano / pinza / braccio / sensore, dai dati prodotto
  (listini/pubblico/catalogo-manifest.json: categoria UMANOIDI / COMPONENTISTICA / MANI_BRACCI).
- categoria_title(slug, en): la categoria scritta nel title ("robot umanoide", "quadruped robot", ...).
- motivo_esclusione(rel): perche' una pagina resta FUORI dalla sitemap (None = in sitemap).
  Le pagine escluse restano online e indicizzabili: niente noindex, canonical invariati;
  escono solo dalla sitemap per non disperdere il crawl su accessori e varianti quasi duplicate.

Regole sitemap (pattern, non liste a mano):
  1. pagine legali (privacy, cookie, note legali, politica resi);
  2. accessori e ricambi Unitree (categoria COMPONENTISTICA: batterie, caricatori, telecomandi,
     foot pad, schede di calcolo, kit...), tranne bracci robotici e sensori LiDAR autonomi;
  3. mani e pinze (end-effector, categoria MANI_BRACCI che non sono bracci);
  4. bracci Z1 con pinza/telecamera (-gripper, -d405, -d435i): resta il braccio base;
  5. robot in bundle ("con kit ...", "con telecomando ..."): resta il robot base;
  6. configurazioni a lettera ("Standard A", "Smart B", "Ultimate C", "Professional D"...): restano
     le schede madre del modello (senza lettera); se il modello non ne ha, resta solo la configurazione A;
  7. schede doppie (stesso nome prodotto, parentesi escluse): resta la prima in ordine alfabetico;
  8. AMR con modulo top (-hook, -shelf, -pallet, -lift): resta la base.
La versione EN di una scheda segue sempre la decisione della scheda IT.
"""
from __future__ import annotations

import html as H
import json
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "listini" / "pubblico" / "catalogo-manifest.json"

# famiglia Unitree (prefisso dello slug) -> categoria del robot
ROBOT_CAT = (
    ("unitree-g1", "umanoide"), ("unitree-r1", "umanoide"), ("unitree-h2", "umanoide"),
    ("unitree-go2", "quadrupede"), ("unitree-as2", "quadrupede"), ("unitree-a2", "quadrupede"),
    ("unitree-b2", "quadrupede"),
)
CAT_WORDS = {  # tipo/categoria -> (IT, EN)
    "umanoide": ("robot umanoide", "humanoid robot"),
    "quadrupede": ("robot quadrupede", "quadruped robot"),
    "braccio": ("braccio robotico", "robotic arm"),
    "mano": ("mano robotica", "robotic hand"),
    "pinza": ("pinza robotica", "robotic gripper"),
    "sensore": ("sensore LiDAR", "LiDAR sensor"),
    "accessorio": ("accessorio", "accessory"),
}

LEGALI = re.compile(r"^(?:en/)?(?:privacy-policy|cookie-policy|note-legali|politica-resi)(?:-en)?\.html$")
SCHEDA = re.compile(r"^(?:en/)?prodotti/([^/]+?)(?:-en)?\.html$")
LETTERA = re.compile(r"^(?P<modello>.+?)\s+(?:standard|smart|ultimate|professional)\s+[a-n]\b", re.I)
BUNDLE = re.compile(r"\bcon (?:kit|telecomando)\b", re.I)
BRACCIO_VARIANTE = re.compile(r"-(?:gripper|d405|d435i)\.html$")
AMR_MODULO_TOP = re.compile(r"^amr-.+-(?:hook|shelf|pallet|lift)\.html$")


def _norm(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\s*\([^)]*\)", "", name)).strip().lower()


@lru_cache(maxsize=1)
def _manifest() -> dict:
    out = {}
    if MANIFEST.is_file():
        for v in json.loads(MANIFEST.read_text(encoding="utf-8")).values():
            if isinstance(v, dict) and v.get("slug"):
                out.setdefault(v["slug"], (v.get("titolo") or "", v.get("categoria") or ""))
    return out


@lru_cache(maxsize=None)
def _pagina(slug: str) -> tuple[str, bool]:
    """(nome visibile nel breadcrumb, pagina reale) della scheda IT; reale = non redirect, canonical su se stessa."""
    p = ROOT / "prodotti" / slug
    if not p.is_file():
        return "", False
    s = p.read_text(encoding="utf-8", errors="replace")
    head = s.split("</head>", 1)[0]
    c = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', head) or re.search(r'<link[^>]*href="([^"]+)"[^>]*rel="canonical"', head)
    reale = 'http-equiv="refresh"' not in head and (not c or c.group(1).endswith("/prodotti/" + slug))
    nav = re.search(r'<nav[^>]*breadcrumb[^>]*>([\s\S]*?)</nav>', s)
    spans = re.findall(r"<span>([^<]+)</span>", nav.group(1)) if nav else []
    return (H.unescape(spans[-1]).strip() if spans else ""), reale


def nome(slug: str) -> str:
    """Nome prodotto della scheda IT (manifest, altrimenti breadcrumb), sempre con "Unitree" davanti."""
    n = _manifest().get(slug, ("", ""))[0] or _pagina(slug)[0]
    if slug.startswith("unitree-") and n and "unitree" not in n.lower():
        n = "Unitree " + n
    return n


def robot_cat(slug: str) -> str | None:
    for prefix, cat in ROBOT_CAT:
        if slug.startswith(prefix):
            return cat
    return None


def tipo_unitree(slug: str) -> str:
    """robot / accessorio / mano / pinza / braccio / sensore per una scheda IT unitree-*.html."""
    n = nome(slug)
    cat = _manifest().get(slug, ("", ""))[1]
    if re.match(r"unitree-(?:arm-|d1-)", slug) or re.search(r"robotic arm|braccio robotico", n, re.I):
        return "pinza" if re.search(r"gripper|pinza", n, re.I) and not slug.startswith("unitree-arm-") else "braccio"
    if cat == "MANI_BRACCI":
        return "pinza" if re.search(r"gripper|pinza|dex1", n + slug, re.I) else "mano"
    if cat == "COMPONENTISTICA":
        if not robot_cat(slug) and re.search(r"lidar", n, re.I) and not re.search(r"\bkit\b", n, re.I):
            return "sensore"
        return "accessorio"
    if cat == "UMANOIDI" or robot_cat(slug):
        return "robot"
    return "accessorio"


def categoria_title(slug: str, en: bool) -> str | None:
    """Categoria per il title della scheda Unitree (IT o EN), dai dati prodotto."""
    t = tipo_unitree(slug)
    key = robot_cat(slug) if t == "robot" else t
    if not key:
        return None
    return CAT_WORDS[key][1 if en else 0]


@lru_cache(maxsize=1)
def _robot_index() -> dict:
    """Schede robot Unitree IT reali: slug -> (nome normalizzato, modello se configurazione a lettera)."""
    idx = {}
    for p in sorted((ROOT / "prodotti").glob("unitree-*.html")):
        slug = p.name
        if not _pagina(slug)[1] or tipo_unitree(slug) != "robot":
            continue
        n = nome(slug)
        m = LETTERA.match(n)
        idx[slug] = (_norm(n), _norm(m.group("modello")) if m else None)
    return idx


def _motivo_robot(slug: str) -> str | None:
    n = nome(slug)
    if BUNDLE.search(n):
        return "robot in bundle (con kit/telecomando)"
    idx = _robot_index()
    if slug not in idx:
        return None
    norm, modello = idx[slug]
    if modello:
        madre = any(
            mod is None and (nn == modello or nn.startswith(modello + " "))
            for s, (nn, mod) in idx.items() if s != slug
        )
        lettera = LETTERA.match(n).group(0)[-1].upper()
        if madre or lettera != "A":
            return "configurazioni a lettera (A-N)"
    # schede doppie: stesso nome (parentesi escluse) -> resta la prima in ordine alfabetico
    for s, (nn, _mod) in idx.items():
        if s < slug and nn == norm and not BUNDLE.search(nome(s)):
            return "schede doppie (stesso nome)"
    return None


def motivo_esclusione(rel: str) -> str | None:
    """Motivo per cui la pagina (path relativo, es. 'prodotti/x.html') resta fuori dalla sitemap."""
    if LEGALI.match(rel):
        return "pagine legali"
    m = SCHEDA.match(rel)
    if not m:
        return None
    slug = m.group(1) + ".html"  # la scheda EN segue la decisione della scheda IT
    if AMR_MODULO_TOP.match(slug):
        return "AMR con modulo top (hook/shelf/pallet/lift)"
    if not slug.startswith("unitree-"):
        return None
    t = tipo_unitree(slug)
    if t == "accessorio":
        return "accessori e ricambi Unitree"
    if t in ("mano", "pinza"):
        return "mani e pinze (end-effector)"
    if t == "braccio" and BRACCIO_VARIANTE.search(slug):
        return "bracci con pinza/telecamera"
    if t == "robot":
        return _motivo_robot(slug)
    return None
