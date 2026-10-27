# Revisione di produzione, direzione C, round 3

Revisore: produzione e pre-press. Materiale: `brand/03-reviews/_anon/C/` alla v3 (`changelog.md` letto). Artefatti in `brand/03-reviews/C/_prod/r3/`.

## Voti

| # | Criterio | r1 | r2 | r3 | Motivazione r3 |
|-|-|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 9 | 9 | 15 SVG validi; nessun `<text>`, `<image>`, font esterno, metadato o `transform`. |
| 2 | Leggibilità piccola e monocromia | 6 | 7 | 8 | `favicon-16.svg` a pixel mostra la A con il punto 3 x 3; il simbolo pieno a 16 px si legge "A" con il punto. Il filo (1 a 6,4 rispetto al punto) sotto i 24 px è un pixel chiaro appena visibile. Descrittore "ROBOTICS" ora al 29% del lockup e omesso sotto i 30 px. |
| 3 | Contrasti | 7 | 9 | 9 | 11 rapporti dichiarati identici al mio ricalcolo; zero testi sotto AA nelle 12 pagine. |
| 4 | Stampabilità | 5 | 6 | 8 | Risolti tutti i punti di r2: niente ≤, ≥, →, Bold dichiarato anche in stampa, apici a 8 px. Biglietto 6,14 pt, filetti 0,47 pt; evidenziatore riproducibile in quadricromia (8 0 90 0 restituisce `#EEE842`). |
| 5 | Licenze | 8 | 7 | 9 | STIX Two Text e DM Mono statici con OFL; il PDF offline non contiene più font di sistema. |
| 6 | Completezza file | 9 | 9 | 9 | Tutti i deliverable, 9 documenti, 6 icone, favicon a 16 e 32 px. |
| 7 | Presentazione senza errori | 9 | 9 | 9 | 12 pagine: zero errori, zero 404, zero richieste esterne, nessun testo tagliato. |

**Voto complessivo r3: 8,7** (r1: 7,4; r2: 8,0)

## Problemi residui

1. **Pantone dell'evidenziatore da scegliere.** I due candidati dichiarati sono lontani dall'HEX: 395 C dista dE 9,2, 3965 C dE 10,8 (riferimenti sRGB comunemente pubblicati, da confermare su mazzetta). Entrambi sono più saturi di `#EEE842`. Retro del biglietto, avatar, adesivi e riquadro del totem cambiano a seconda della scelta: va fissato un solo Pantone e riallineato l'HEX dopo la prova.
2. **Filo del simbolo in piccolo.** Spessore 17 unità su 662: a 16 px è 0,4 px, sull'etichetta di inventario e sul biglietto va verificato che non scenda sotto 0,25 pt. Scrivere in `sistema-grafico.md` la dimensione minima del simbolo in mm per la stampa.
3. **Struttura della A.** Fuori dal mio ambito ma da segnalare: il changelog descrive una "A senza traversa con punto". Il punto e il filo fanno da traversa a ogni dimensione che ho provato, però l'orchestratore aveva vietato la A senza traversa; la conferma spetta al revisore del marchio.

## Controlli eseguiti (comandi)

- `xmllint -noout` su `logo/*.svg` e `icone/*.svg`: 15 file, 0 errori. Igiene con `grep -c` su `<text`, `<image`, font esterni, metadati, `transform=`, `viewBox`.
- `node brand/_tools/shot.js <file> brand/03-reviews/C/_prod/r3/<nome>.png 1440 900 1` su 12 pagine: "nessun errore".
- `node r3/strumenti/audit3.js <cartella C> r3/audit-C.json .card 12`. L'unico caso a 1,00:1 (testo ruotato sul totem) è un falso positivo, verificato sullo screenshot.
- `node r3/strumenti/small-text.js 8 <preventivi>`: nessun testo sotto 6 pt.
- `node r3/strumenti/platfonts.js <preventivi>`: nessun font di sistema per nodo (in r2 Georgia e Lucida Grande).
- `node r3/strumenti/pdf3.js` con rete bloccata: incorporati DMMono Regular e Medium, STIXTwoText Regular, SemiBold, Bold, Italic, tutti `FontFile2`, zero Type 3.
- `python3 r3/strumenti/color.py r3/strumenti/colors3.json` e confronto Pantone (`r3/strumenti/pantone3.out`).
- `node r3/strumenti/bbox.js` e `logoh.js`: descrittore 207 su 717 unità; lockup di copertina 34 px, cioè maiuscole a 7,4 pt in A4.
- Piccolo formato: `r3/piccolo-3x-pixel.png`.
- Copy: zero em dash, en dash, doppi trattini o tilde; il post anonimo non contiene SACMI, Imola o ceramica.
- Screenshot guardati: `r3/foglio-applicazioni-1.png`, `r3/foglio-applicazioni-2.png`, `r3/piccolo-3x-pixel.png`.
