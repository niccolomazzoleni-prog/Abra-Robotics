# Revisione di produzione, direzione A, round 3

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/A/` alla v3 (`changelog.md` letto). Artefatti in `brand/03-reviews/A/_prod/r3/`.

## Voti

| # | Criterio | r1 | r2 | r3 | Motivazione r3 |
|-|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 9 | 19 SVG validi; nessun `<text>`, `<image>`, font esterno, metadato o `transform`; mono negativo senza fondo. |
| 2 | Leggibilità piccola e monocromia | 8 | 9 | 9 | La legatura con la A intera si legge "Ab" a 16 e 32 px, su chiaro e su scuro; `favicon-16.svg` disegnato a pixel è il segno più leggibile delle tre direzioni rimaste. |
| 3 | Contrasti | 7 | 9 | 9 | 16 rapporti dichiarati identici al mio ricalcolo; zero testi sotto AA nelle 12 pagine. |
| 4 | Stampabilità | 6 | 8 | 7 | Biglietto a 6,14 pt minimo, preventivi senza testo sotto 6 pt, Pantone 348 C reso obbligatorio. Nuovo difetto: il G1 a tratto è un PNG di 824 x 2140 px stampato a 1320 mm sul totem, cioè circa 41 ppi. |
| 5 | Licenze | 9 | 9 | 8 | IBM Plex (OFL, Reserved Font Name "Plex", usato senza modifiche) e B612 statici con licenza. Il G1 a tratto è ricalcato da un'immagine ufficiale Unitree: va trattato come segnaposto, non come asset del sistema. |
| 6 | Completezza file | 9 | 9 | 9 | Tutti i deliverable, 9 documenti, 6 icone, favicon a 16 e 32 px. |
| 7 | Presentazione senza errori | 9 | 9 | 9 | 12 pagine: zero errori di console, zero 404, zero richieste esterne, nessun testo tagliato. |

**Voto complessivo r3: 8,6** (r1: 8,0; r2: 8,9)

## Problemi residui

1. **G1 a tratto in raster.** `assets/img/g1-tratto.png` (824 x 2140 px) è usato in `hero.html`, `reel-g1.html` e `totem.html`. Sul totem il G1 è disegnato in scala 1:1 (1320 mm): la risoluzione effettiva è circa 41 ppi, contro i 100 a 150 ppi minimi per il forex visto da vicino. Il tratto è un elemento del sistema e va consegnato vettoriale (SVG a tracciati, spessore minimo 0,5 pt alla scala di stampa).
2. **Origine del tratto.** Il disegno ricalca la foto ufficiale Unitree. `REGOLE.md` ammette quelle immagini solo come segnaposto dichiarato: le didascalie lo dicono, il changelog lo presenta come elemento distintivo. Prima dell'uso pubblico va ridisegnato da una foto propria del G1 nel laboratorio.
3. **Verde a schermo e Pantone 348 C.** Il riferimento sRGB comunemente pubblicato per il 348 C (`#00843D`) dista dE 11,7 da `#008351`: il 348 C è più giallo. `palette.md` lo dichiara ("da riallineare dopo la prima prova colore"); va fatto prima di consegnare il sistema, altrimenti sito e stampa avranno due verdi.

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 19 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`, `<rect`.
- `node brand/_tools/shot.js <file> brand/03-reviews/A/_prod/r3/<nome>.png 1440 900 1` su 12 pagine: "nessun errore" (`r3/strumenti/shot-log.txt`).
- `node r3/strumenti/audit3.js <cartella A> r3/audit-A.json .card 6`: contrasto su ogni nodo di testo, font, richieste esterne, caratteri vietati, testo tagliato, corpo e filetti del biglietto in pt.
- `node r3/strumenti/small-text.js 8 <preventivi>`: nessun testo sotto 6 pt nelle pagine A4.
- `python3 r3/strumenti/color.py r3/strumenti/colors3.json` (`r3/strumenti/colors3.out`) e confronto con i riferimenti sRGB dei Pantone dichiarati (`r3/strumenti/pantone3.out`; valori di riferimento comunemente pubblicati, da confermare su mazzetta).
- `node r3/strumenti/pdf3.js`: export dei due preventivi con rete bloccata; incorporati IBMPlexSans, IBMPlexSans Medium e SemiBold, IBMPlexSansCond SemiBold, B612 Regular e Bold, tutti `FontFile2`, zero Type 3. `r3/strumenti/platfonts.js`: nessun font di sistema.
- Dimensioni delle immagini con Pillow su `assets/img/*.png`.
- Piccolo formato: `r3/piccolo-3x-pixel.png`.
- Copy: zero em dash, en dash, doppi trattini o tilde nel testo visibile e nei `.md`; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `r3/foglio-applicazioni-1.png`, `r3/foglio-applicazioni-2.png`, `r3/piccolo-3x-pixel.png`.
