#!/usr/bin/env python3
"""Aggiunge Email (obbligatoria) + Telefono (opzionale) al form principale (#contact-form)
su tutte le pagine, prima del campo Ruolo. Idempotente (salta se id='email' già presente)."""
import glob, re

# inserisce il blocco prima del gruppo "Ruolo", riusando l'indentazione di quel gruppo
PAT = re.compile(r'(?P<ws>[ \t]*)<div class="form-group">(?=\s*<label for="ruolo">)')

def block(ws):
    return (
        ws + '<div class="form-row">\n' +
        ws + '  <div class="form-group"><label for="email">Email</label>'
             '<input type="email" id="email" name="email" placeholder="nome@azienda.it" required></div>\n' +
        ws + '  <div class="form-group"><label for="telefono">Telefono (opzionale)</label>'
             '<input type="tel" id="telefono" name="telefono" placeholder="+39 ..."></div>\n' +
        ws + '</div>\n'
    )

n_files = 0
for f in glob.glob('*.html') + glob.glob('prodotti/*.html'):
    t = open(f, encoding='utf-8').read()
    if 'id="contact-form"' not in t or 'id="email"' in t:
        continue
    new, c = PAT.subn(lambda m: block(m.group('ws')) + m.group(0), t, count=1)
    if c:
        open(f, 'w', encoding='utf-8').write(new)
        n_files += 1
        print('  OK', f)
print(f'\nFile aggiornati: {n_files}')
