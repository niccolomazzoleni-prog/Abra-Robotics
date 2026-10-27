# Tipografia · In squadra (v3)

## Scelta

Due famiglie gratuite con licenza SIL Open Font License 1.1, in file **statici** locali (`assets/fonts/`), incorporabili nei PDF del Company Brain. Nessuna CDN.

| Famiglia | Ruolo | Pesi | Licenza | Costo |
|-|-|-|-|-|
| **IBM Plex Sans Condensed** | titoli e frasi in grande | 600, 700 | SIL OFL 1.1, nome riservato "Plex" (`OFL-IBMPlex.txt`) | gratuito |
| **IBM Plex Sans** | testo corrente, tabelle, dati | 400, 500, 600 | SIL OFL 1.1 | gratuito |
| **B612** | etichette, cartigli, riquadri di controllo, quote, targhe | 400, 700 | SIL OFL 1.1 (`OFL-B612.txt`) | gratuito |

Perché così, dopo i round 1 e 2:
- **Titoli in Plex Sans Condensed.** B612 in grande risultava goffo (spaziature larghe, ritmo irregolare): è nato per gli schermi di cabina a corpi piccoli. Plex, disegnato da Mike Abbink per IBM come carattere per ingegneri, ha un grassetto condensato compatto e regolare che regge 60 a 90 px senza correzioni.
- **Testo in Plex Sans al posto di Barlow.** Barlow più il verde ricreava la coppia di MYBOTSHOP. Plex Sans ha cifre tabellari, ottima leggibilità nei documenti e nessun concorrente rilevato lo usa con il verde.
- **B612 dove nasce: piccolo.** Etichette, quote, cartigli e targhe sono le "letture di strumento" del sistema; B612 (Intactile Design e Airbus) le rende riconoscibili da vicino.

Il logotipo non usa nessuna delle tre famiglie: è disegnato su asse e tratto costante (`_src/glyphs.py`).

### Alternativa commerciale

Per i titoli: **Söhne Schmal** (Klim Type Foundry), licenza desktop e web per peso nell'ordine di 100 a 200 euro, da verificare su klim.co.nz. Plex resta la scelta consigliata, gratuita e già completa.

## Gerarchia

### Schermo

| Livello | Famiglia e peso | Dimensione / interlinea | Spaziatura |
|-|-|-|-|
| Titolo display | Plex Sans Condensed 600 | 60 a 90 px / 1,02 | -1 % |
| Titolo di sezione | Plex Sans Condensed 600 | 26 a 52 px / 1,08 | -1 % |
| Titolo di blocco | Plex Sans Condensed 600 | 19 a 21 px / 1,15 | 0 |
| Testo introduttivo | Plex Sans 400 | 19 px / 1,5 | 0 |
| Testo | Plex Sans 400 | 16 a 17 px / 1,55 | 0 |
| Dato | Plex Sans 500, cifre tabellari | come il testo | 0 |
| Etichetta, quota, cartiglio | B612 400 maiuscolo | 11 a 13 px / 1,3 | +6 % |

### Carta

| Livello | Famiglia e peso | Corpo / interlinea |
|-|-|-|
| Titolo di copertina | Plex Sans Condensed 600 | 30 pt / 31 pt |
| Titolo di sezione | Plex Sans Condensed 600 | 20 pt / 22 pt |
| Testo | Plex Sans 400 | 9,5 pt / 13,5 pt |
| Tabelle | Plex Sans 400 e 600 | 8,5 pt / 12 pt |
| Etichette e cartiglio | B612 400 maiuscolo | 6,5 a 7 pt, +6 % |
| Minimo assoluto | qualsiasi | 6 pt |

## Regole

- Titoli sempre in Plex Sans Condensed; B612 mai sopra i 20 px.
- Maiuscolo solo nelle etichette B612, frasi brevi. "Abra" non si scrive mai tutto maiuscolo: nelle etichette il nome compare come logotipo.
- Cifre tabellari attive nei dati. Unità con lo spazio: "1320 mm", "2 h".
- Allineamento a sinistra, mai giustificato; righe da 45 a 70 caratteri.

## CSS di base

```css
@font-face{font-family:"Plex C";src:url(fonts/IBMPlexSansCondensed-SemiBold.ttf) format("truetype");font-weight:600}
@font-face{font-family:"Plex";src:url(fonts/IBMPlexSans-Regular.ttf) format("truetype");font-weight:400}
@font-face{font-family:"B612";src:url(fonts/B612-Regular.ttf) format("truetype");font-weight:400}
h1{font:600 80px/1.02 "Plex C";letter-spacing:-.01em}
body{font:400 17px/1.55 "Plex";font-feature-settings:"tnum" 1}
.et{font:400 12px/1.3 "B612";letter-spacing:.06em;text-transform:uppercase}
```
