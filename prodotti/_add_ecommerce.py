#!/usr/bin/env python3
"""Inietta nelle schede prodotto:
  - il box 'Richiedi informazioni' (form compatto) sopra la descrizione
  - gli script stripe-config.js + ecommerce.js prima di </body>
Genera inoltre stripe-config.js con una voce per ogni scheda (Payment Link da riempire).
Idempotente.
"""
import glob, re, html

pages = sorted(glob.glob("unitree-*.html"))

# 1) stripe-config.js (solo se non esiste gia')
import os
if not os.path.exists("stripe-config.js"):
    lines = [
        "/* Stripe — incolla qui i Payment Link creati nella dashboard Stripe.",
        "   Chiave = nome file della scheda. Valore = URL del Payment Link (https://buy.stripe.com/...).",
        "   Finche' il valore resta vuoto, il bottone 'Acquista' rimanda alla richiesta preventivo. */",
        'window.STRIPE_PUBLISHABLE_KEY = "";',
        "window.STRIPE_PAYMENT_LINKS = {",
    ]
    for p in pages:
        lines.append(f'  "{p}": "",')
    lines.append("};")
    open("stripe-config.js", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("Creato stripe-config.js con", len(pages), "voci")
else:
    print("stripe-config.js gia' presente, non sovrascrivo")

def form_box(product):
    p = html.escape(product, quote=True)
    return f'''<div class="quote-box">
            <p class="quote-box-title">Richiedi informazioni su questo prodotto</p>
            <form class="quote-form-top" data-product="{p}">
              <div class="quote-row">
                <input type="text" name="nome" placeholder="Nome e cognome" required>
                <input type="email" name="email" placeholder="Email" required>
              </div>
              <textarea name="messaggio" rows="2" placeholder="La tua richiesta..."></textarea>
              <button type="submit" class="btn btn-primary btn-sm">Invia richiesta</button>
              <span class="quote-form-feedback" aria-live="polite"></span>
            </form>
          </div>
          '''

changed = 0
for path in pages:
    text = open(path, encoding="utf-8").read()
    orig = text

    # a) form box sopra la prima <p class="product-desc">
    if "quote-form-top" not in text:
        m = re.search(r"<h1[^>]*class=\"product-title\"[^>]*>(.*?)</h1>", text, re.S)
        product = re.sub(r"\s+", " ", m.group(1)).strip() if m else "questo prodotto"
        text = re.sub(r'(\s*)<p class="product-desc">',
                      r"\1" + form_box(product) + '<p class="product-desc">',
                      text, count=1)

    # b) script includes prima di </body>
    inject = ""
    if "stripe-config.js" not in text:
        inject += '  <script src="stripe-config.js"></script>\n'
    if "ecommerce.js" not in text:
        inject += '  <script src="ecommerce.js"></script>\n'
    if inject:
        text = text.replace("</body>", inject + "</body>", 1)

    if text != orig:
        open(path, "w", encoding="utf-8").write(text)
        changed += 1
        print(f"  OK {path}")

print(f"\nSchede aggiornate: {changed}")
