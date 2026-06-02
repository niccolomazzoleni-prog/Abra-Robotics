# -*- coding: utf-8 -*-
"""Costruisce il blocco prezzo+checkout e lo schema JSON-LD per le schede.
Usa _prezzi.PREZZI come fonte unica."""
from _prezzi import PREZZI, euro, schema_price

SITE = "https://niccolomazzoleni-prog.github.io/Abra-Robotics"

def buy_area(file):
    p = PREZZI[file]
    stato = p["stato"]
    if stato == "coming-soon":
        return '''          <div class="product-cta-group">
            <a class="btn btn-primary buy-btn is-disabled" aria-disabled="true">Coming soon</a>
            <a href="#form" class="btn btn-secondary">Richiedi informazioni</a>
          </div>'''
    if stato == "preventivo":
        return '''          <div class="product-cta-group">
            <a href="#form" class="btn btn-primary">Richiedi preventivo</a>
            <a href="#specs" class="btn btn-secondary">Specifiche tecniche</a>
          </div>'''
    # stato == "acquista"
    link = p["link"] or "#form"
    pending = "" if p["link"] else ' data-buy-pending="1"'
    return f'''          <div class="product-price">
            <span class="product-price-value">{euro(p["cent"])}</span>
          </div>
          <p class="product-price-note"><span class="ppn-ico">✓</span> Spedizione e dazio doganale inclusi</p>
          <p class="product-price-disclaimer">Prezzo indicativo, soggetto a variazioni cambio EUR/USD — preventivo aggiornato su richiesta.</p>
          <div class="product-cta-group">
            <a href="{link}" class="btn btn-primary buy-btn"{pending}>Acquista</a>
            <a href="#form" class="btn btn-secondary">Richiedi preventivo</a>
          </div>'''

def schema(file, name, desc, img_rel):
    p = PREZZI[file]
    canon = f"{SITE}/prodotti/{file}"
    img = img_rel if img_rel.startswith("http") else f"{SITE}/prodotti/{img_rel}"
    nm = name.replace('"', '\\"')
    ds = desc.replace('"', '\\"')
    offer = ""
    if p["stato"] == "acquista":
        offer = f''',
  "offers": {{
    "@type": "Offer",
    "priceCurrency": "EUR",
    "price": "{schema_price(p["cent"])}",
    "availability": "https://schema.org/InStock",
    "url": "{canon}"
  }}'''
    return f'''  <script type="application/ld+json">
  {{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{nm}",
  "image": ["{img}"],
  "description": "{ds}",
  "brand": {{"@type": "Brand", "name": "Unitree"}}{offer}
  }}
  </script>'''
