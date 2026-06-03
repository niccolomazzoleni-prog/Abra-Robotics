#!/usr/bin/env python3
"""Compila i dati legali reali nelle pagine del sito."""
import glob

# applicato a TUTTE le pagine root (footer P.IVA)
REPL_ALL = {
    'P.IVA [DA COMPLETARE]': 'P.IVA 04800170278',
}
# solo pagine legali (identità titolare) — ordine importante (stringa lunga prima)
REPL_LEGAL = {
    '[DA COMPLETARE: Nome Cognome del titolare]': 'Niccolò Mazzoleni',
    '[DA COMPLETARE: indirizzo], Pordenone (PN), Italia': 'Viale Trieste 105, 30026 Portogruaro (VE), Italia',
    '[DA COMPLETARE: indirizzo], Pordenone (PN)': 'Viale Trieste 105, 30026 Portogruaro (VE)',
    '[DA COMPLETARE: P.IVA]': '04800170278',
    'PEC: gio@abrarobotics.com': 'PEC: abrarobotics@pek.it',
    'Abra Robotics [DA COMPLETARE: ragione sociale]': 'Abra Robotics di Niccolò Mazzoleni (P.IVA 04800170278)',
}

def apply(path, mapping):
    t = open(path, encoding='utf-8').read(); n = 0
    for a, b in mapping.items():
        if a in t:
            n += t.count(a); t = t.replace(a, b)
    if n:
        open(path, 'w', encoding='utf-8').write(t)
    return n

tot = 0
for f in glob.glob('*.html'):
    tot += apply(f, REPL_ALL)
for f in ['privacy-policy.html', 'note-legali.html', 'condizioni-di-vendita.html', 'cookie-policy.html']:
    tot += apply(f, REPL_LEGAL)
print('Sostituzioni applicate:', tot)
