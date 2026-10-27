# Tipografia · Riferimento A

## Scelta

**Una sola famiglia: Barlow**, in tre larghezze (normale, Semi Condensed, Condensed). Barlow nasce dalla segnaletica stradale pubblica: è un grotesk a basso contrasto con curve leggermente arrotondate, della stessa stirpe dei caratteri da targa e da cartello (DIN 1451, Highway Gothic). Ha cifre tabellari, molti pesi e una versione semicondensata che regge titoli lunghi in italiano senza andare a capo ogni tre parole.

Una famiglia sola, perché in questa direzione la gerarchia si fa con larghezza, peso e maiuscolo spaziato, come su una targa dati. Niente serif, niente monospaziato come voce: il dato tecnico si scrive in Barlow con cifre tabellari.

Il logotipo non usa Barlow: è disegnato a mano su asse e tratto costante (vedi `logo/` e `_src/glyphs.py`). Barlow gli sta accanto perché viene dalla stessa logica costruttiva.

| Famiglia | Pesi usati | Licenza | Costo | Dove |
|-|-|-|-|-|
| Barlow | 400, 500, 600, 700 | SIL Open Font License 1.1 | gratuito | testo, dati, tabelle, interfacce |
| Barlow Semi Condensed | 400, 500, 600, 700 | SIL OFL 1.1 | gratuito | titoli, etichette, riquadri di controllo |
| Barlow Condensed | 500, 600 | SIL OFL 1.1 | gratuito | tabelle strette, segnaletica, flight case |

File OFL in `assets/fonts/` con il testo della licenza (`OFL-Barlow.txt`). La licenza OFL consente l'incorporamento nei PDF del Company Brain e l'uso via `@font-face` sul sito. Fonte: Google Fonts, progetto di Jeremy Tribby.

### Alternativa commerciale

Se Abra volesse un carattere più rigoroso e più raro: **FF DIN Pro** di Albert Jan Pool (FontFont, oggi Monotype). Licenza desktop per singolo peso indicativamente 60 a 80 euro; famiglia di 5 pesi con licenze desktop, web e incorporamento in PDF nell'ordine di 600 a 1.000 euro (da verificare su monotype.com al momento dell'acquisto). Barlow resta l'alternativa gratuita e la scelta consigliata per un team di due persone.

## Gerarchia

### Schermo (sito, post, presentazioni)

| Livello | Famiglia e peso | Dimensione / interlinea | Spaziatura | Esempio |
|-|-|-|-|-|
| Titolo display | Semi Condensed 600 | 74 a 92 px / 1,0 | -1,2 % | "Misura nel tuo reparto cosa farà il robot, prima di investire." |
| Titolo di sezione | Semi Condensed 600 | 30 a 40 px / 1,08 | -0,5 % | "Decidi fase per fase, con un criterio scritto." |
| Titolo di blocco | Semi Condensed 600 | 19 a 22 px / 1,15 | 0 | "Targa adesiva sul dorso" |
| Testo introduttivo | Barlow 400 | 19 a 20 px / 1,5 | 0 | paragrafo sotto il titolo |
| Testo | Barlow 400 | 16 a 17 px / 1,55 | 0 | corpo di pagina |
| Dato | Barlow 500, cifre tabellari | come il testo | 0 | "1320 mm", "3.500 €" |
| Etichetta | Semi Condensed 500, maiuscolo | 11 a 13 px / 1,3 | +9 % | "SCHEDA DI PROVA · REV 0.3" |

### Carta (preventivo A4, manuale, biglietto)

| Livello | Famiglia e peso | Corpo / interlinea |
|-|-|-|
| Titolo di copertina | Semi Condensed 600 | 34 pt / 36 pt |
| Titolo di sezione | Semi Condensed 600 | 22 pt / 24 pt |
| Testo | Barlow 400 | 10 pt / 14 pt |
| Tabelle | Barlow 400 e 600 | 9 pt / 12,5 pt |
| Etichette e cartiglio | Semi Condensed 500 maiuscolo | 7 pt / 9 pt, +10 % |

## Regole

- Maiuscolo spaziato solo per le etichette brevi (massimo 6 parole). "Abra" non si scrive mai tutto maiuscolo: nelle etichette il nome compare come logotipo oppure in tondo.
- Cifre tabellari sempre attive nelle tabelle, nelle quote e nei prezzi (`font-feature-settings:"tnum"`).
- Unità di misura sempre con lo spazio: "1320 mm", "2 h", "98 %". Separatore delle migliaia con il punto, decimali con la virgola.
- Un titolo per pagina; nessun titolo in maiuscolo.
- Allineamento a sinistra, bandiera a destra. Mai giustificato.
- Misura della riga: da 45 a 70 caratteri per il testo continuo.

## CSS di base

```css
@font-face{font-family:"Barlow";src:url(fonts/Barlow-Regular.ttf) format("truetype");font-weight:400}
@font-face{font-family:"Barlow SC";src:url(fonts/BarlowSemiCondensed-SemiBold.ttf) format("truetype");font-weight:600}
h1{font:600 80px/1 "Barlow SC";letter-spacing:-.012em}
.et{font:500 12px/1.3 "Barlow SC";letter-spacing:.09em;text-transform:uppercase}
body{font:400 17px/1.55 "Barlow";font-feature-settings:"tnum" 1}
```

Il foglio completo è in `assets/a.css`. Per il sito conviene servire i file in WOFF2, scaricabili già convertiti da Google Fonts.
