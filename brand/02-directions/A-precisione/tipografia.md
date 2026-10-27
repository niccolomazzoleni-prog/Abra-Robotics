# Tipografia · In squadra (v2)

## Scelta

Due voci, entrambe gratuite con licenza SIL Open Font License 1.1, in file statici locali (`assets/fonts/`), adatti all'incorporamento nei PDF del Company Brain.

| Famiglia | Ruolo | Pesi | Licenza | Costo |
|-|-|-|-|-|
| **B612** | titoli, nome sul biglietto, voce dei formati di comunicazione | 400, 700 | SIL OFL 1.1 (`OFL-B612.txt`) | gratuito |
| **Barlow**, Semi Condensed, Condensed | testo, dati con cifre tabellari, tabelle, etichette | 400, 500, 600, 700 | SIL OFL 1.1 (`OFL-Barlow.txt`) | gratuito |

**B612** è il carattere disegnato da Intactile Design con Airbus (e la scuola ENAC di Tolosa) per gli schermi della cabina di pilotaggio: forme aperte, aperture larghe, distinzione netta tra caratteri simili, pensato per essere letto in fretta su uno strumento. È la voce dello strumento di bordo: tecnica senza essere un grotesk da catalogo, e nessun concorrente rilevato la usa. In grassetto, con spaziatura stretta, dà alle headline un timbro proprio.

**Barlow** resta per testo e dati: discende dalla segnaletica stradale, ha cifre tabellari e larghezze semicondensate che servono a tabelle, cartigli e targhe. Non è più l'unica voce del sistema.

Il logotipo non usa nessuno dei due: è disegnato su asse e tratto costante (`_src/glyphs.py`), con la legatura Ab e i tagli a pendenza 2 a 1.

### Alternativa commerciale

Per le headline, al posto di B612: **FF DIN Round** o **FF DIN Pro** (Albert Jan Pool, Monotype), licenza desktop circa 60 a 80 euro per peso, famiglia con licenze web e PDF nell'ordine di 600 a 1.000 euro, da verificare su monotype.com. B612 resta la scelta consigliata: gratuita e più rara.

## Gerarchia

### Schermo

| Livello | Famiglia e peso | Dimensione / interlinea | Spaziatura |
|-|-|-|-|
| Titolo display | B612 700 | 62 a 76 px / 1,02 a 1,06 | -2,5 % |
| Titolo di sezione | B612 700 | 26 a 52 px / 1,06 a 1,12 | -2 % |
| Titolo di blocco | B612 700 | 19 a 21 px / 1,15 | -1 % |
| Testo introduttivo | Barlow 400 | 19 px / 1,5 | 0 |
| Testo | Barlow 400 | 16 a 17 px / 1,55 | 0 |
| Dato | Barlow 500, cifre tabellari | come il testo | 0 |
| Etichetta | Barlow Semi Condensed 500, maiuscolo | 11 a 13 px / 1,3 | +9 % |

### Carta

| Livello | Famiglia e peso | Corpo / interlinea |
|-|-|-|
| Titolo di copertina | B612 700 | 30 pt / 32 pt |
| Titolo di sezione | B612 700 | 20 pt / 22 pt |
| Testo | Barlow 400 | 10 pt / 14 pt |
| Tabelle | Barlow 400 e 600 | 9 pt / 12,5 pt |
| Etichette e cartiglio | Barlow Semi Condensed 500 maiuscolo | 7 pt / 9 pt, +10 % |
| Biglietto da visita | minimo assoluto | 6 pt |

## Regole

- B612 solo per titoli e frasi brevi; mai per tabelle o testo lungo.
- Maiuscolo spaziato solo per etichette brevi in Barlow Semi Condensed. "Abra" non si scrive mai tutto maiuscolo: nelle etichette il nome compare come logotipo.
- Cifre tabellari sempre attive nei dati (`font-feature-settings:"tnum"`). Unità con lo spazio: "1320 mm", "2 h".
- Allineamento a sinistra, mai giustificato; righe da 45 a 70 caratteri.
- Nessun testo sotto i 6 pt in stampa.

## CSS di base

```css
@font-face{font-family:"B612";src:url(fonts/B612-Bold.ttf) format("truetype");font-weight:700}
@font-face{font-family:"Barlow";src:url(fonts/Barlow-Regular.ttf) format("truetype");font-weight:400}
h1{font:700 70px/1.04 "B612";letter-spacing:-.025em}
body{font:400 17px/1.55 "Barlow";font-feature-settings:"tnum" 1}
.et{font:500 12px/1.3 "Barlow SC";letter-spacing:.09em;text-transform:uppercase}
```

Il foglio completo è in `assets/a.css`.
