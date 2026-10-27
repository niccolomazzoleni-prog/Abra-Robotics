# Revisione di produzione, direzione C, round 1

Revisore: produzione e pre-press. Data: 27/10/2026. Materiale: `brand/03-reviews/_anon/C/`.

## Voti

| # | Criterio | Voto | Motivazione |
|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 8 SVG del logo e 6 icone validi; niente `<text>`, `<image>`, font esterni, metadati; un `transform` residuo in `verticale.svg`. Il simbolo è il contorno della A di STIX Two (curve quadratiche TrueType), ritoccato con punto e filo. |
| 2 | Leggibilità piccola e monocromia | 6 | A 16 px il punto e il filo, cioè l'idea del segno, spariscono dentro la traversa: resta una A graziata qualsiasi. Il favicon giallo regge come macchia di colore. Mono positivo e negativo corretti. |
| 3 | Contrasti | 7 | I 14 rapporti dichiarati coincidono con il mio ricalcolo. In uso: Grafite chiara su Carta 2,24:1 per i numeri 01 a 04 dell'hero (10 px) e 2,40:1 per le etichette dell'asse del grafico nel preventivo (8 px). |
| 4 | Stampabilità | 5 | L'Evidenziatore `#E9EC55`, colore portante, esce dal gamut CMYK (dE 12,4); i CMYK dichiarati di Inchiostro, Grafite e Verde registro tornano lontani dagli HEX (dE 12,4, 7,4, 12,5). Biglietto con testo a 4,0 pt e filetto a 0,24 pt, sotto 0,25. |
| 5 | Licenze | 8 | STIX Two Text e DM Mono locali con i rispettivi OFL. Il simbolo derivato da un glifo OFL è lecito, ma STIX ha nomi di font riservati e il segno resta poco distintivo per una registrazione. |
| 6 | Completezza file | 9 | Tutti i deliverable presenti, con font locali in woff2 e ttf. |
| 7 | Presentazione senza errori | 9 | Presentazione, test, animazione e 9 applicazioni: zero errori, zero 404, zero richieste esterne. |

**Voto complessivo: 7,4**

## I 3 problemi più gravi

1. **Il colore firma non si stampa in quadricromia.** `#E9EC55` con profilo Generic CMYK torna con dE 12,4; il CMYK dichiarato (1 0 64 7) produce `#EDE376`, un giallo paglia (dE 17,5). Retro del biglietto, avatar, adesivi, etichette di inventario e totem dipendono da quel colore: senza tinta piatta il marchio cambia faccia a ogni stampatore.
2. **Il segno perde l'idea in piccolo.** `_prod/piccolo-3x-pixel.png`: a 16 e 32 px il "richiamo" (cerchio raggio 64 su 738 unità, filo spesso 40) diventa 1 px o meno. Favicon, avatar e adesivo sul Go2 mostrano quindi una A di STIX.
3. **Biglietto fuori soglia e PDF con font Type 3.** `applicazioni/biglietto.html` (12 px = 1 mm): "Appunti dell'incontro" a 17 px = 4,0 pt, `abrarobotics.com` sul retro 5,2 pt, filetto `.piede` 1,5 px = 0,24 pt. Il preventivo esportato in PDF incorpora STIX come 31 font Type 3 (il variabile non viene incorporato come TrueType): testo meno ricercabile e preflight di tipografia a rischio.

## Feedback azionabili

1. `palette.md`: scegliere una tinta piatta Pantone per l'Evidenziatore (verificare su mazzetta coated e uncoated) e dichiarare una variante CMYK di ripiego con il suo HEX di schermo coerente; rifare i CMYK di Inchiostro, Grafite e Verde registro con un profilo dichiarato (le formule attuali sono conversioni a solo nero e danno colori diversi).
2. `logo/`: disegnare `simbolo-16.svg` e `simbolo-32.svg` ottici, con punto di raggio almeno 2 px e filo di 2 px a 16 px, e usarli in `favicon.svg` e nell'avatar.
3. `applicazioni/biglietto.html`: `.appunto .etichetta` e `.fronte .piede` da 17 a 26 px (6,1 pt); `.retro .t .mono` da 22 a 26 px; filetto `.piede` da 1,5 a 2 px (0,31 pt).
4. Font per PDF: aggiungere in `fonts/` le istanze statiche di STIX Two Text (Regular, Italic, SemiBold) e dichiararle in `abra-c.css` per la stampa (`@media print`), così Chrome le incorpora come TrueType.
5. `applicazioni/hero.html` e `preventivo-interna.html`: i numeri di riga e le etichette dell'asse sono informativi; passarli a Grafite `#625E57` (5,76:1) oppure dichiararli decorativi e ripetere l'informazione altrove.
6. `applicazioni/linkedin-sacmi.html`: il piede dice "Caso pubblicato con il consenso scritto di SACMI", che oggi non esiste; scrivere "Bozza: pubblicare solo con il consenso scritto".
7. `concept.md` e `tipografia.md`: dichiarare che il simbolo deriva da STIX Two Text (OFL 1.1, Reserved Font Name "STIX") e chiedere un parere sulla registrabilità del marchio prima della scelta.

## Controlli eseguiti (comandi)

- Validità SVG: `xmllint -noout` su `logo/*.svg` e `icone/*.svg` (14 file, 0 errori).
- Igiene logo: `grep -c` su `<text`, `<image`, font esterni, metadati da editor, `transform=`, `viewBox`; lettura di `simbolo.svg` (comandi `Q` da contorno TrueType).
- Apertura pagine: `node brand/_tools/shot.js <file> brand/03-reviews/C/_prod/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- Audit: `node _prod/strumenti/audit.js <cartella C> <out.json> .card 12` (contrasti effettivi, font, richieste esterne, copy, corpo e filetti del biglietto). Dati in `_prod/audit-C.json`. Il "G1 · 132 cm" a 1,00:1 sul totem è un falso positivo (testo ruotato accanto al filetto).
- Colore: `python3 _prod/strumenti/color.py colors.json` (Pillow ImageCms, `Generic CMYK Profile.icc`).
- PDF: `node _prod/strumenti/pdf.js` con rete bloccata; nel PDF 31 `/Subtype /Type3` e 1 `/Type0` (DM Mono).
- Piccolo formato: `_prod/piccolo-3x-pixel.png`.
- Copy: nessun em dash, en dash, doppio trattino o tilde nel testo visibile e nei `.md`; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `_prod/foglio-applicazioni-1.png`, `_prod/foglio-applicazioni-2.png`, `_prod/piccolo-3x-pixel.png`.
