# Revisione di produzione, direzione B, round 1

Revisore: produzione e pre-press. Data: 27/10/2026. Materiale: `brand/03-reviews/_anon/B/`.

## Voti

| # | Criterio | Voto | Motivazione |
|-|-|-|-|
| 1 | SVG validi e puliti | 8 | 10 SVG del logo e 6 icone validi; niente `<text>`, `<image>`, font esterni, metadati, `transform`; geometria ad archi esatti, file leggeri. |
| 2 | Leggibilità piccola e monocromia | 6 | A 16 px il simbolo si riduce a un disco rosso con un'asta: la "a" non si legge senza il favicon ottico. Nel logotipo orizzontale alto 20 px la parola "Robotics" in corsivo scende a circa 5 px ed è illeggibile. Mono positivo e negativo corretti. |
| 3 | Contrasti | 7 | I 18 rapporti dichiarati coincidono con il mio ricalcolo. In uso: Pietra `#D9D1C3` su Rosso Abra 3,68:1 per testo da 12 a 17 px (presentazione, reel). |
| 4 | Stampabilità | 5 | Biglietto con testo a 4,25 pt (etichette "Posta", "Telefono", "Sito") e 5,3 pt sul retro. Rosso Abra fuori dal gamut CMYK generico (dE 5,9), Rosso scuro dE 7,8; i CMYK dichiarati di Ocra, Rosso, Rosso scuro tornano a colori diversi (dE da 7 a 9). |
| 5 | Licenze | 6 | Newsreader e Hanken Grotesk sono OFL, ma la direzione non consegna i file: tutto viene da Google Fonts. Senza rete il PDF incorpora Georgia e Helvetica Neue, font di sistema Apple che non si possono ridistribuire dentro un preventivo. |
| 6 | Completezza file | 8 | Tutti i deliverable presenti; mancano i file dei font con la licenza, richiesti dal brief per incorporarli nei PDF del Company Brain. |
| 7 | Presentazione senza errori | 7 | Zero errori di console e zero 404 con rete attiva; ogni pagina fa da 3 a 5 richieste a fonts.googleapis.com e fonts.gstatic.com. Offline la presentazione cambia carattere. |

**Voto complessivo: 6,7**

## I 3 problemi più gravi

1. **Font solo da CDN.** `assets/b.css` riga 2 importa i font da `fonts.googleapis.com`. Ho esportato `preventivo-cover.html` in PDF con la rete bloccata: font incorporati `Georgia`, `Georgia-Italic`, `HelveticaNeue-Bold`, `HelveticaNeue-Medium` (vedi `_prod/preventivo-cover-offline.pdf` e `.png`). Il Company Brain gira su un VPS: se il fetch fallisce, il cliente riceve un preventivo in un altro carattere e con font proprietari incorporati.
2. **Simbolo e logotipo deboli in piccolo.** `_prod/piccolo-3x-pixel.png`: `simbolo.svg` a 16 px è un pallino rosso; l'arco ocra resta un filo di 2 px. In `orizzontale.svg` "Robotics" è circa un quarto dell'altezza di "abra": sotto i 120 px di larghezza del marchio non si legge (header del sito a 22 px, biglietto, flight case visti da lontano).
3. **Biglietto sotto i 6 pt e rosso da verificare.** `applicazioni/biglietto.html` (scala 8 px = 1 mm): `.contatti b` a 12 px = 4,25 pt. Il retro è un fondo pieno Rosso Abra: con CMYK 10 85 95 10 il ritorno è `#B64430`, più spento dell'HEX; su carta avorio non patinata peggiora.

## Feedback azionabili

1. Scaricare i TTF statici di Newsreader (400, 400 corsivo, 500) e Hanken Grotesk (400, 500, 600) in `B/fonts/` con `OFL.txt`; sostituire l'`@import` di `assets/b.css` con `@font-face` locali e togliere il `<link>` a Google Fonts da tutte le pagine. Ripetere l'export PDF offline e verificare che i nomi incorporati siano Newsreader e HankenGrotesk.
2. `logo/orizzontale.svg` e `verticale.svg`: portare "Robotics" almeno al 45% dell'altezza x di "abra", oppure prevedere un logotipo "abra" senza "Robotics" sotto i 160 px di larghezza e scriverlo come regola in `sistema-grafico.md`.
3. `logo/test.html`: aggiungere la prova del simbolo pieno (non solo favicon) a 16 px su fondo chiaro e la regola esplicita "sotto 32 px solo favicon ottico".
4. `applicazioni/biglietto.html`: `.contatti b` da 12 a 16 px (5,7 pt è ancora poco: meglio 17 px = 6 pt), `.retro small` da 15 a 17 px.
5. `palette.md`: indicare un Pantone per Rosso Abra e Ocra (tinta piatta per biglietto e retro), rifare i CMYK con un profilo dichiarato; segnalare che il Rosso scuro `#8E2B1B` esce dal gamut.
6. Presentazione e reel: Pietra su rosso (3,68:1) solo da 24 px in su; per le didascalie su rosso usare Carta `#FBF8F2` (5,26:1).
7. `applicazioni/linkedin-sacmi.html`: la versione nominativa cita "Imola"; va bene solo con il consenso scritto, ricordarlo nel cartellino "Bozza" già presente.

## Controlli eseguiti (comandi)

- Validità SVG: `xmllint -noout` su `logo/*.svg` e `icone/*.svg` (16 file, 0 errori).
- Igiene logo: `grep -c` su `<text`, `<image`, `font-family|@font-face|@import|url(http`, metadati da editor, `transform=`, `viewBox`.
- Apertura pagine: `node brand/_tools/shot.js <file> brand/03-reviews/B/_prod/<nome>.png 1440 900 1` su presentazione, test, animazione e 9 applicazioni: "nessun errore" (log in `_prod/strumenti/shot-log.txt`).
- Audit: `node _prod/strumenti/audit.js <cartella B> <out.json> .card 8`: contrasti effettivi su ogni nodo di testo, richieste esterne, font, copy, corpo e filetti del biglietto in pt. Dati in `_prod/audit-B.json`. Il "Noleggia il G1" a 1,00:1 sul totem è un falso positivo (fondo dato da un'immagine), verificato sullo screenshot.
- Colore: `python3 _prod/strumenti/color.py colors.json` (Pillow ImageCms, `Generic CMYK Profile.icc`, colorimetrico relativo).
- PDF offline: `node _prod/strumenti/pdf.js`, rete bloccata con `page.route`, lettura dei `/BaseFont` nel PDF.
- Piccolo formato: `_prod/strumenti/piccolo.html` resa 1x, ingrandita 3x: `_prod/piccolo-3x-pixel.png`.
- Copy: nessun em dash, en dash, doppio trattino o tilde nel testo visibile e nei `.md`; parole vietate solo nella lista "no" di `voce.md`; il post anonimo non contiene SACMI né Imola.
- Screenshot guardati: `_prod/foglio-applicazioni-1.png`, `_prod/foglio-applicazioni-2.png`, `_prod/preventivo-cover-offline.png`, `_prod/piccolo-3x-pixel.png`.
