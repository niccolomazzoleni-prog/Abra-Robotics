# Revisione di produzione, direzione D, round 2

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/D/` alla v2 (`changelog.md` letto), compresa la nuova `applicazioni/scheda-laboratorio.html`. Artefatti in `brand/03-reviews/D/_prod/r2/`.

## Voti

| # | Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 18 SVG validi, nessun `<text>`, `<image>`, font esterno, metadato o `transform`; aggiunto `favicon.svg` e collegato dalle pagine. |
| 2 | Leggibilità piccola e monocromia | 8 | 8 | Il simbolo "ab" a portali regge a 16 px, il favicon magenta è netto; mono positivo e negativo corretti. Il descrittore "ROBOTICS" in Archivo Expanded è alto il 21% del lockup: 3,7 pt nelle intestazioni di preventivo interno e scheda laboratorio. |
| 3 | Contrasti | 7 | 9 | I 10 rapporti dichiarati coincidono con il mio ricalcolo. I casi segnalati dall'audit (testo chiaro sui punti magenta della presentazione, quote del totem) sono falsi positivi verificati sugli screenshot: fondo dato da elementi fratelli. |
| 4 | Stampabilità | 5 | 7 | Biglietto 6,14 pt minimo; PDF con Archivo statico in TrueType, zero Type 3. Restano corpi sotto 6 pt nei documenti A4 e il Magenta fuori gamut (dE 7,0), dichiarato con Pantone 226 C. |
| 5 | Licenze | 9 | 9 | Sei istanze statiche di Archivo con `OFL.txt`; nessun font di sistema nei PDF. |
| 6 | Completezza file | 8 | 9 | `favicon.svg` aggiunto, cartella di processo rimossa, scheda per i laboratori in più. |
| 7 | Presentazione senza errori | 9 | 9 | 13 pagine: zero errori, zero 404, zero richieste esterne; tolto "Il futuro in scena" dalla copertina. |

**Voto complessivo r2: 8,6** (r1: 7,7)

## Problemi residui

1. **Testo sotto 6 pt nei documenti A4.** `preventivo-cover.html` e `scheda-laboratorio.html`: piede a 7,5 px = 5,6 pt; `preventivo-interna.html` e `scheda-laboratorio.html`: intestazioni di tabella (`th`) a 7,8 px = 5,85 pt in maiuscolo espanso. Portarli a 8,5 px (6,4 pt).
2. **Descrittore "ROBOTICS" troppo piccolo nei documenti.** Lockup alto 24 px nell'interna e nella scheda: le maiuscole misurano 5 px, cioè 3,7 pt; in copertina 4,7 pt. Usare `logotipo.svg` senza descrittore sotto i 40 px di altezza, oppure ingrandire il descrittore nel lockup piccolo.
3. **Magenta in grandi campiture.** Totem, reel, flight case: il ritorno in quadricromia è `#CF2570`, più spento. Rendere vincolante il Pantone 226 C per totem e flight case e chiedere prova su forex e vinile; Rosa `#FBE3EE` torna con dE 5,0 (tinta delle colonne dei criteri, accettabile ma da verificare in ufficio).

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 18 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- `node brand/_tools/shot.js <file> brand/03-reviews/D/_prod/r2/<nome>.png 1440 900 1` su 13 pagine: "nessun errore".
- `node r2/strumenti/audit.js <cartella D> r2/audit-D.json .bv 12`.
- `node r2/strumenti/small-text.js 8 <preventivi e scheda>`: testi sotto 6 pt nelle pagine A4.
- `python3 r2/strumenti/color.py r2/strumenti/colors2.json` (`r2/colore.txt`).
- `node r2/strumenti/pdf2.js` con rete bloccata: preventivo copertina e interna, scheda laboratorio; font Archivo Regular, SemiBold, Bold, Italic, Expanded SemiBold, tutti `FontFile2`, zero Type 3.
- `node r2/strumenti/logoh.js` e `bbox.js`: altezza dei lockup nelle pagine, descrittore 43 su 208 unità.
- Piccolo formato: `r2/piccolo-3x-pixel.png`.
- Copy: zero em dash, en dash, doppi trattini o tilde; il post anonimo non contiene SACMI, Imola o ceramica. Il QR del totem non è stato decodificato (nessun lettore installato): verificarlo con un telefono prima della stampa.
- Screenshot guardati: `r2/foglio-applicazioni-1.png`, `r2/foglio-applicazioni-2.png`, `r2/piccolo-3x-pixel.png`.
