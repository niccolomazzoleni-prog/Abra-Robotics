#!/usr/bin/env python3
"""Applica uno sconto del 6% a tutti i prezzi delle schede prodotto.
Aggiorna sia il prezzo visibile (.buy-box-amount, formato IT) sia il prezzo
nello schema JSON-LD ("price", formato numerico).

ATTENZIONE: eseguire UNA sola volta (ri-eseguendolo scontereste di nuovo).
"""
import glob, re

FACTOR = 0.94  # -6%

def it_fmt(v):
    s = f"{v:,.2f}"                       # 73,276.98 (formato US)
    return s.replace(",", "X").replace(".", ",").replace("X", ".")  # -> 73.276,98

def parse_it(s):
    return float(s.replace(".", "").replace(",", "."))

changed = 0
for path in sorted(glob.glob("unitree-*.html")):
    text = open(path, encoding="utf-8").read()
    orig = text
    log = []

    # 1) prezzo visibile .buy-box-amount  (es. 77.954,23 €)
    def repl_visible(m):
        old = m.group(2)
        new = it_fmt(round(parse_it(old) * FACTOR, 2))
        log.append(f"display {old} -> {new}")
        return m.group(1) + new + m.group(3)
    text = re.sub(r'(<span class="buy-box-amount">)([\d.]+,\d{2})( ?€</span>)',
                  repl_visible, text)

    # 2) prezzo schema JSON-LD ("price": "77954.23")
    def repl_schema(m):
        old = float(m.group(2))
        new = round(old * FACTOR, 2)
        log.append(f"schema {m.group(2)} -> {new:.2f}")
        return f'{m.group(1)}{new:.2f}{m.group(3)}'
    text = re.sub(r'("price":\s*")(\d+\.\d{1,2})(")', repl_schema, text)

    if text != orig:
        open(path, "w", encoding="utf-8").write(text)
        changed += 1
        print(f"OK {path}: " + " | ".join(log))

print(f"\nSchede aggiornate: {changed}")
