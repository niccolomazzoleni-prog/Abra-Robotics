# Revisione di produzione, direzione A, round 1

Revisore: produzione e pre-press. Data: 27/10/2026. Materiale: `brand/03-reviews/_anon/A/`.

## Voti

| # | Criterio | Voto | Motivazione |
|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 11 SVG del logo e 6 icone validi; niente `<text>`, `<image>`, font esterni, metadati o `transform`; `mono-negativo.svg` contiene un rettangolo di fondo grafite, quindi non è un file a un colore. |
| 2 | Leggibilità piccola e monocromia | 8 | Il simbolo regge a 16 px, il favicon a riquadro è il più netto delle cinque direzioni; il triangolino sotto la traversa a 16 px diventa un punto di 1 o 2 pixel e si perde; il monogramma a 16 px ha la cornice di 1 px che sfarfalla. |
| 3 | Contrasti | 7 | Tutti i 14 rapporti dichiarati in `palette.md` coincidono con il mio ricalcolo. Nelle applicazioni compaiono però coppie fuori norma: Grigio quota su Grafite 2,81:1 e Acciaio su Grafite 80 4,09:1. |
| 4 | Stampabilità | 6 | Biglietto con testo a 4,7 pt (etichette TEL, MAIL) e numeri del righello a 5,2 pt, sotto la soglia di 6 pt. Filetti minimi 0,47 pt, corretti. Verde su scuro `#3DBB82` fuori gamut (dE 7,8) ma dichiarato solo schermo. |
| 5 | Licenze | 9 | Barlow in TTF locali con `OFL-Barlow.txt`; il PDF esportato offline incorpora Barlow vero (4 sottoinsiemi). |
| 6 | Completezza file | 9 | Tutti i deliverable di `direttore-creativo.md` presenti, compresi post anonimo, favicon, 6 icone, animazione, PNG. |
| 7 | Presentazione senza errori | 9 | `presentazione.html`, `logo/test.html`, `logo/animazione.html` e 9 applicazioni: zero errori di console, zero 404, zero richieste esterne. |

**Voto complessivo: 8,0**

## I 3 problemi più gravi

1. **Testo sotto i 6 pt nel biglietto.** `applicazioni/biglietto.html` (scala 6 px = 1 mm): `.retro .dati span` a 10 px = 4,7 pt; numeri del righello sul fronte 5,2 pt. In offset su carta da 400 g le etichette in maiuscoletto spaziato a 4,7 pt si impastano.
2. **Coppie di contrasto usate e non dichiarate.** Grigio quota `#5C676D` su Grafite `#1A2125` = 2,81:1 in `hero.html` ("Piano di riferimento A", 10 px), `reel-g1.html` (didascalia segnaposto 15 px) e `totem.html` ("Piano del padiglione"). Acciaio `#8A959B` su Grafite 80 `#2C353A` = 4,09:1 nei tempi del reel (17 px, sotto AA).
3. **CMYK indicativi incoerenti con gli HEX per i colori di segnale.** Con il profilo Generic CMYK di macOS, il CMYK dichiarato del Giallo limite (5 8 85 0) torna a `#F1DB4D`, scarto dE 8,3; il Verde segnale dE 4,1; la Grafite dichiarata 80 65 55 75 torna più scura (dE 4,2). Per un sistema che usa il colore come segnale di stato, la tinta stampata deve essere quella giusta.

## Feedback azionabili

1. `applicazioni/biglietto.html`: portare `.retro .dati span` da 10 px a 13 px (6,1 pt) e i numeri del righello a 13 px; se il righello non regge, tenere solo le tacche e i numeri a 0, 50, 80.
2. `assets/a.css` e applicazioni: vietare Grigio quota su fondi scuri; usare Acciaio `#8A959B` (5,32:1 su Grafite) per tutte le didascalie su scuro. Su Grafite 80 usare Alluminio `#E3E7E9`.
3. `palette.md`: aggiungere alla tabella dei contrasti le coppie su Grafite 80 (Acciaio 4,09, Alluminio) con esito, e la riga "Grigio quota su Grafite: 2,81, vietato".
4. `palette.md`: indicare un riferimento Pantone per Verde segnale e Giallo limite (oppure RAL vero per il vinile) e rifare i CMYK con un profilo dichiarato (FOGRA39 per patinata, FOGRA29 per uso mano).
5. `logo/mono-negativo.svg`: togliere il `<rect>` di fondo; il negativo deve essere solo la forma in `#FFFFFF`, il fondo lo mette il supporto.
6. `logo/monogramma.svg`: a 16 px la cornice (spessore 10 su 160, cioè 1 px) cade tra due pixel; preparare una versione ottica a 16 px con cornice di 2 px oppure usare sempre `favicon.svg` sotto i 24 px e scriverlo in `sistema-grafico.md`.
7. Livrea: `applicazioni/livrea.html` contiene testo a 5,6 px nella targa ("AR GO2 0007 · SW 1.1"); dichiarare in pagina la scala e la misura reale in mm della targa, così si verifica il corpo in stampa.

## Controlli eseguiti (comandi)

- Validità SVG: `xmllint -noout` su ogni file di `logo/` e `icone/` (17 file, 0 errori).
- Igiene logo: `grep -c` su `<text`, `<image`, `font-family|@font-face|@import|url(http`, `inkscape|sodipodi|illustrator|<metadata`, `transform=`, `viewBox` per ogni SVG di `logo/`.
- Apertura pagine: `node brand/_tools/shot.js <file> brand/03-reviews/A/_prod/<nome>.png 1440 900 1` su presentazione, test, animazione e tutte le applicazioni (log in `_prod/strumenti/shot-log.txt`).
- Audit approfondito: `node _prod/strumenti/audit.js <cartella A> <out.json> .card 6` (Playwright con Chrome di sistema): contrasto calcolato su ogni nodo di testo contro il fondo effettivo, font caricati, richieste esterne, caratteri vietati nel testo visibile e negli attributi alt, aria-label, title, testo tagliato, corpo minimo e filetti minimi del biglietto in pt. Dati grezzi in `_prod/audit-A.json`. I casi con rapporto 1,00 sulle quote (`.qx b`) sono falsi positivi: l'etichetta sta fuori dal filetto che le fa da antenato.
- Colore: `python3 _prod/strumenti/color.py colors.json` (Pillow ImageCms, profilo `Generic CMYK Profile.icc`, intento colorimetrico relativo): ricalcolo WCAG delle coppie dichiarate, giro sRGB, CMYK, sRGB con dE76, conversione dei CMYK dichiarati.
- Piccolo formato: `_prod/strumenti/piccolo.html` resa a 1x con shot.js, ingrandita 3x senza interpolazione: `_prod/piccolo-3x-pixel.png`.
- PDF: `node _prod/strumenti/pdf.js` esporta `preventivo-cover.html` in A4 con la rete bloccata e conta i font incorporati: `_prod/preventivo-cover-offline.pdf`.
- Copy: nessun em dash, en dash, doppio trattino o tilde nel testo visibile delle 12 pagine né nei file `.md`; le parole vietate compaiono solo nella lista "no" di `voce.md`. Il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `_prod/foglio-applicazioni-1.png`, `_prod/foglio-applicazioni-2.png`, `_prod/piccolo-3x-pixel.png`.
