# -*- coding: utf-8 -*-
"""Costruisce il blocco prezzo+preventivo e lo schema JSON-LD per le schede.
Usa _prezzi.PREZZI come fonte unica."""
from _prezzi import PREZZI, euro, schema_price

SITE = "https://niccolomazzoleni-prog.github.io/Abra-Robotics"

_PERKS = '''            <ul class="buy-box-perks">
              <li><span class="bp-ico">✓</span> Spedizione e dazio doganale inclusi</li>
              <li><span class="bp-ico">✓</span> Parte della filiera di distribuzione di Unitree Italia · garanzia inclusa</li>
              <li><span class="bp-ico">✓</span> Consegna stimata 4–6 settimane</li>
            </ul>'''
_NOTE = '<p class="buy-box-note">Prezzo indicativo, soggetto a variazioni cambio EUR/USD — preventivo aggiornato su richiesta.</p>'

def buy_area(file):
    p = PREZZI[file]
    stato = p["stato"]
    if stato == "coming-soon":
        return f'''          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price">
                <span class="buy-box-amount" style="font-size:1.6rem;">Disponibile a breve</span>
              </div>
              <span class="buy-box-stock"><span class="dot" style="background:var(--orange);box-shadow:0 0 0 3px rgba(255,107,0,0.16);"></span> In arrivo</span>
            </div>
{_PERKS}
            <div class="buy-box-cta">
              <a class="btn btn-primary buy-btn is-disabled" aria-disabled="true">Coming soon</a>
              <a href="#form" class="btn btn-secondary">Richiedi informazioni</a>
            </div>
          </div>'''
    if stato == "preventivo":
        return f'''          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price">
                <span class="buy-box-amount" style="font-size:1.6rem;">Prezzo su richiesta</span>
              </div>
              <span class="buy-box-stock"><span class="dot"></span> Disponibile</span>
            </div>
{_PERKS}
            <div class="buy-box-cta">
              <a href="#form" class="btn btn-primary">Richiedi preventivo</a>
              <a href="#specs" class="btn btn-secondary">Specifiche tecniche</a>
            </div>
          </div>'''
    # stato == "acquista"
    return f'''          <div class="buy-box">
            <div class="buy-box-head">
              <div class="buy-box-price">
                <span class="buy-box-amount">{euro(p["cent"])}</span>
                <span class="buy-box-sub">Prezzo chiavi in mano</span>
              </div>
              <span class="buy-box-stock"><span class="dot"></span> Disponibile</span>
            </div>
{_PERKS}
            <div class="buy-box-cta">
              <a href="#form" class="btn btn-primary">Richiedi preventivo</a>
            </div>
            {_NOTE}
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
