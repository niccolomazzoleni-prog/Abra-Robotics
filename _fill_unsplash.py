#!/usr/bin/env python3
"""Sostituisce i placeholder immagine (.img-ph) con foto Unsplash (free) a tema.
Prima passata: l'utente poi indica quali cambiare. G1D/R1D NON toccati (servono foto reali).
"""
import re

Q = "?w=1600&q=70&auto=format&fit=crop"
def url(pid): return f"https://images.unsplash.com/photo-{pid}{Q}"

# label esatta -> URL  (per i placeholder con label unica)
BY_LABEL = {
    "IMG: umanoide contesto università": url("1737644467636-6b0053476bb2"),
    "IMG: hero manifattura e logistica": url("1655393001768-d946c97d6fd1"),
    "IMG: quadrupedi in ispezione impianto": url("1592085198739-ffcad7f36b54"),
    "IMG: hero università e ricerca": url("1601132359864-c974e79890ac"),
    "IMG: laboratorio di ricerca robotica": url("1581093577421-f561a654a353"),
}
# assessment: 4 placeholder identici "IMG: placeholder" -> in ordine
ASSESS = [url("1563968743333-044cef800494"), url("1587293852726-70cdb56c2866"),
          url("1614935151651-0bea6508db6b"), url("1518152006812-edab29b069ac")]
# finanziamenti: 3 "IMG: placeholder finanziamenti" -> in ordine
FIN = [url("1637002722490-5f8ceed9774c"), url("1568561586426-10f4ce2dafc5"),
       url("1543967708-2418d2e7748c")]

PAT = re.compile(r'<div class="[^"]*img-ph[^"]*" style="([^"]*)">(IMG:[^<]*)</div>')

def fill(path, queues):
    text = open(path, encoding="utf-8").read()
    def repl(m):
        style, label = m.group(1), m.group(2).strip()
        if label in BY_LABEL:
            u = BY_LABEL[label]
        elif label in queues and queues[label]:
            u = queues[label].pop(0)
        else:
            return m.group(0)  # non toccare (es. G1D/R1D non sono img-ph comunque)
        st = style.rstrip().rstrip(";")
        return (f'<div style="{st}; background-image:url(\'{u}\'); '
                f'background-size:cover; background-position:center; border-radius:12px;"></div>')
    new, n = PAT.subn(repl, text)
    open(path, "w", encoding="utf-8").write(new)
    print(f"  {path}: {n} placeholder sostituiti")

fill("index.html", {})
fill("assessment.html", {"IMG: placeholder": list(ASSESS)})
fill("finanziamenti.html", {"IMG: placeholder finanziamenti": list(FIN)})
fill("manifattura-logistica.html", {})
fill("universita-ricerca.html", {})
print("Fatto. (G1D/R1D restano placeholder: servono foto prodotto reali)")
