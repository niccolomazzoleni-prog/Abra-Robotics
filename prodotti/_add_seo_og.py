#!/usr/bin/env python3
"""Inserisce i meta OpenGraph + Twitter Card nelle schede prodotto che ne sono prive.
Idempotente: salta le pagine che contengono gia' 'og:title'.
og:image viene dedotto dalla prima immagine prodotto (sotto assets/ o ../images/, escluso il logo).
"""
import glob, re, html, os

SITE = "https://niccolomazzoleni-prog.github.io/Abra-Robotics/"
PROD = SITE + "prodotti/"
DEFAULT_IMG = SITE + "images/hero-robots.png"

def abs_url(src):
    if src.startswith("../"):
        return SITE + src[3:]
    if src.startswith("assets/") or src.startswith("./assets/"):
        return PROD + src.lstrip("./")
    if src.startswith("http"):
        return src
    return PROD + src.lstrip("/")

def first_product_image(text):
    for m in re.finditer(r'src="([^"]+\.(?:png|jpg|jpeg|webp))"', text):
        src = m.group(1)
        if "logo" in src.lower():
            continue
        return abs_url(src)
    return DEFAULT_IMG

def grab(pattern, text, default=""):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default

changed = 0
for path in sorted(glob.glob("unitree-*.html")):
    text = open(path, encoding="utf-8").read()
    if "og:title" in text:
        continue
    title = html.escape(grab(r"<title>(.*?)</title>", text), quote=True)
    desc = html.escape(grab(r'<meta\s+name="description"\s+content="(.*?)"', text), quote=True)
    canon = grab(r'<link\s+rel="canonical"\s+href="(.*?)"', text, PROD + path)
    img = first_product_image(text)

    og = f'''
  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="product">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{img}">
  <meta property="og:site_name" content="Abra Robotics">
  <meta property="og:locale" content="it_IT">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{img}">'''

    # inserisci dopo il meta robots
    new = re.sub(r'(<meta\s+name="robots"[^>]*>)', r"\1" + og, text, count=1)
    if new == text:
        print(f"  ! robots meta non trovato in {path}, salto")
        continue
    open(path, "w", encoding="utf-8").write(new)
    changed += 1
    print(f"  OK {path}  (og:image -> {img.split('/')[-1]})")

print(f"\nSchede aggiornate: {changed}")
