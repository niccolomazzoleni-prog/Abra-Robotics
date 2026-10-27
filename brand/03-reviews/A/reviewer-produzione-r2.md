# Revisione di produzione, direzione A, round 2

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/A/` alla v2 (`changelog.md` letto). Artefatti in `brand/03-reviews/A/_prod/r2/`.

## Voti

| # | Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 19 SVG validi; nessun `<text>`, `<image>`, font esterno, metadato o `transform`; `mono-negativo.svg` ora è solo la forma in `#FFFFFF`, senza rettangolo. |
| 2 | Leggibilità piccola e monocromia | 8 | 9 | La legatura Ab regge a 16 e 32 px; `favicon-16.svg` disegnato sulla griglia è il più netto del round. Il monogramma a 16 px lascia la legatura troppo piccola nella piastra, ma la regola "sotto 24 px solo favicon-16" copre il caso. |
| 3 | Contrasti | 7 | 9 | 15 rapporti dichiarati, tutti identici al mio ricalcolo; coppie vietate dichiarate. Nelle 12 pagine nessun testo sotto AA. |
| 4 | Stampabilità | 6 | 8 | Biglietto: testo minimo 6,14 pt sul retro, 8,98 pt sul fronte, nessun filetto sotto 0,25 pt. Verde di misura in gamut (ritorno dE 1,5); CMYK dichiarati coerenti con gli HEX (dE da 1,0 a 1,5). |
| 5 | Licenze | 9 | 9 | B612 e Barlow statici in locale con i due OFL; PDF offline con soli font della direzione. |
| 6 | Completezza file | 9 | 9 | Tutti i deliverable, più `favicon-16.svg` e `monogramma-grafite.svg`. |
| 7 | Presentazione senza errori | 9 | 9 | 12 pagine: zero errori di console, zero 404, zero richieste esterne, nessun testo tagliato. |

**Voto complessivo r2: 8,9** (r1: 8,0)

## Problemi residui

1. **Campi pieni di verde in quadricromia.** Il verde ora copre fronte del biglietto, testata del preventivo, totem e reel. In gamut con il profilo generico, ma su carta uso mano il 85 13 82 14 si spegne: per biglietto e totem va chiesta una prova colore oppure il Pantone 348 C indicato. Da scrivere come regola in `palette.md`, oggi è solo "indicativo".
2. **Corpi sotto 6 pt nelle tavole a scala.** `logo/test.html` ha annotazioni a 5,5 px ("ASTA COMUNE"), `applicazioni/livrea.html` testo a 7 px nella targa con scala dichiarata (1 mm = 3 px, quindi 2,3 mm, circa 6,6 pt reali: accettabile). Solo la prima è da correggere, è una pagina di presentazione.
3. **Monogramma a 16 px.** `logo/monogramma.svg` a 16 px riduce la legatura a 8 px dentro la piastra verde; tenere la regola e usare `favicon-16.svg` anche come avatar sotto i 48 px.

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 19 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`, `<rect`.
- `node brand/_tools/shot.js <file> brand/03-reviews/A/_prod/r2/<nome>.png 1440 900 1` su 12 pagine: "nessun errore" (`r2/strumenti/shot-log.txt`).
- `node r2/strumenti/audit.js <cartella A> r2/audit-A.json .card 6`: contrasto su ogni nodo di testo, font, richieste esterne, caratteri vietati, testo tagliato, corpo e filetti del biglietto in pt.
- `python3 r2/strumenti/color.py r2/strumenti/colors2.json`: ricalcolo WCAG e gamut con `Generic CMYK Profile.icc`, intento colorimetrico relativo (`r2/colore.txt`).
- `node r2/strumenti/pdf2.js`: export A4 di `preventivo-cover` e `preventivo-interna` con rete bloccata; font incorporati: Barlow, Barlow Semi Condensed, B612, tutti `FontFile2`, zero Type 3, zero richieste bloccate.
- Piccolo formato: `r2/strumenti/piccolo.html` resa 1x e ingrandita 3x senza interpolazione (`r2/piccolo-3x-pixel.png`).
- Copy: zero em dash, en dash, doppi trattini o tilde nel testo visibile e nei `.md`; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `r2/foglio-applicazioni-1.png`, `r2/foglio-applicazioni-2.png`, `r2/piccolo-3x-pixel.png`.
