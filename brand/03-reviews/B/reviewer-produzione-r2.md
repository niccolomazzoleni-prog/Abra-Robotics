# Revisione di produzione, direzione B, round 2

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/B/` alla v2 (`changelog.md` letto). Artefatti in `brand/03-reviews/B/_prod/r2/`.

## Voti

| # | Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 17 SVG validi; nessun `<text>`, `<image>`, font esterno, metadato o `transform`; marchio a un colore, file leggeri. |
| 2 | Leggibilità piccola e monocromia | 6 | 8 | La "a" con il giunto si legge a 16 px; `favicon.svg` e `favicon-32.svg` sono versioni ottiche vere. "Robotics" ora è al 40% dell'altezza del lockup e si legge anche a 20 px. |
| 3 | Contrasti | 7 | 8 | I 13 rapporti dichiarati coincidono con il mio ricalcolo. Resta una coppia usata e non dichiarata: Grigio `#5E6264` su Grigio Lettera `#DADCD6` = 4,46:1, appena sotto AA, nelle didascalie della presentazione (12 px) e nella didascalia di `biglietto.html` (14 px). |
| 4 | Stampabilità | 5 | 7 | Biglietto a 6,02 pt minimo (fronte) e 6,73 pt (retro), filetti 1,06 pt. Rosso Abra fuori gamut (dE 5,1), ora dichiarato con Pantone indicativo e regola di tinta piatta; gli altri CMYK tornano entro dE 1,6. |
| 5 | Licenze | 6 | 9 | Instrument Sans e Crimson Pro statici in `fonts/` con gli OFL; nessuna richiesta a Google Fonts. Il PDF offline incorpora solo InstrumentSans e CrimsonPro. |
| 6 | Completezza file | 8 | 9 | Font consegnati, `simbolo-negativo.svg` e `favicon-32.svg` aggiunti, PDF del preventivo inclusi. |
| 7 | Presentazione senza errori | 7 | 9 | 12 pagine: zero errori, zero 404, zero richieste esterne (r1: da 3 a 5 per pagina). |

**Voto complessivo r2: 8,4** (r1: 6,7)

## Problemi residui

1. **Biglietto al limite dei 6 pt.** `applicazioni/biglietto.html`: le etichette "Posta", "Telefono" a 17 px su scala 8 px = 1 mm danno 6,02 pt in maiuscolo; in offset tiene, in stampa digitale su carta non patinata 350 g è al limite. Portarle a 18 o 19 px (6,4 a 6,7 pt).
2. **Rosso Abra in quadricromia.** Retro del biglietto, coperchio del flight case, pannello del totem e del reel sono campiture rosse: con il CMYK 7 86 89 13 il ritorno è `#B64133`. La regola "tinta piatta" va resa vincolante per biglietti e totem, e il Pantone scelto su mazzetta prima della prima tiratura.
3. **Grigio su Grigio Lettera.** 4,46:1; aggiungere la coppia in `palette.md` come "solo da 18,7 px in grassetto o 24 px" oppure scurire il Grigio a `#5A5E60` (4,8:1 circa) e ricalcolare.

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 17 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- `node brand/_tools/shot.js <file> brand/03-reviews/B/_prod/r2/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- `node r2/strumenti/audit.js <cartella B> r2/audit-B.json .card 8` (contrasti effettivi, font, richieste esterne, copy, corpo e filetti del biglietto).
- `python3 r2/strumenti/color.py r2/strumenti/colors2.json` con `Generic CMYK Profile.icc` (`r2/colore.txt`).
- `node r2/strumenti/pdf2.js`: export dei due preventivi con rete bloccata; font incorporati InstrumentSans Regular e Bold, CrimsonPro Regular, tutti `FontFile2`, zero Type 3.
- Misura del lockup: `r2/strumenti/bbox.js` sulla geometria di `orizzontale.svg` ("Robotics" alto 163 su 406 unità).
- Piccolo formato: `r2/piccolo-3x-pixel.png`.
- Copy: zero em dash, en dash, doppi trattini o tilde; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `r2/foglio-applicazioni-1.png`, `r2/foglio-applicazioni-2.png`, `r2/preventivo-cover-offline.png`.
