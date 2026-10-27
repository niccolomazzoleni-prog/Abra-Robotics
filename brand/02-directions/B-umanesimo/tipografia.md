# Tipografia v2. Territorio B, Montato a vista

Due famiglie OFL, **in locale e statiche** nella cartella `fonts/` con i file di licenza. Nessuna richiesta a Google Fonts: il sito, i mockup e i PDF del Company Brain usano gli stessi file. Prova eseguita: export PDF di `preventivo-cover.html` e `preventivo-interna.html` con la rete bloccata (`_strumenti/pdf.js`), font incorporati InstrumentSans-Regular, InstrumentSans-Bold, CrimsonPro-Regular, zero richieste esterne. I PDF sono in `applicazioni/`.

## Le famiglie

### Instrument Sans: la voce dei titoli e dei dati
- **Autori**: The Instrument Sans Project Authors (Instrument). **Licenza**: SIL OFL 1.1, costo zero, incorporabile nei PDF e ridistribuibile con `OFL-InstrumentSans.txt`.
- **File**: `InstrumentSans-Regular.ttf`, `InstrumentSans-Italic.ttf`, `InstrumentSans-Bold.ttf` (statici).
- **Ruolo**: titoli, interfaccia, etichette, tabelle, numeri con le unità di misura, "Robotics" del marchio esteso.
- **Perché**: un grotesk sobrio e un po' stretto, con la "a" a doppia pancia come il logotipo. Nei titoli grandi in peso Regular dà il tono di un documento d'impresa, e regge il confronto con i loghi di un'azienda meccanica in un verbale.

### Crimson Pro: la voce della lettura
- **Autori**: The Crimson Pro Project Authors (Jacques Le Bailly). **Licenza**: SIL OFL 1.1, costo zero, file `OFL-CrimsonPro.txt`.
- **File**: `CrimsonPro-Regular.ttf`, `CrimsonPro-Italic.ttf`, `CrimsonPro-Bold.ttf` (statici).
- **Ruolo**: testo d'apertura, testo corrente di manuali e preventivi, didascalie in corsivo.
- **Perché**: un serif da libro di impianto rinascimentale, la parte umanista del sistema. Resta nel testo che si legge con calma; i titoli sono in Instrument Sans.

Il monospaziato non fa parte del sistema.

## Gerarchia

| Livello | Carattere | Sito (px) | A4 (pt) | Interlinea | Note |
|-|-|-|-|-|-|
| Titolo d'apertura | Instrument Sans 400 | 62 | 29 | 1,03 | Tondo, nessuna parola in corsivo o a colore |
| Titolo di sezione | Instrument Sans 400 | 40 | 23 | 1,1 | |
| Testo d'apertura | Crimson Pro 400 | 21 | 12 | 1,42 | |
| Testo corrente | Crimson Pro 400 | 18 | 10 | 1,45 | Da 60 a 75 battute |
| Didascalia e segnaposto | Crimson Pro corsivo | 13 a 15 | 9 | 1,35 | Sempre in grafite |
| Etichetta | Instrument Sans 700 maiuscolo, +0,06 em | 12 | 7,5 | 1,2 | Preceduta dal trattino della serie |
| Dato in evidenza | Instrument Sans 700 | 26 | 14 | 1,1 | Numero e unità nello stesso corpo |
| Interfaccia, pulsanti | Instrument Sans 700 | 14 a 15 | 9 | 1,2 | Pulsanti rettangolari grafite |
| Bollino "Esempio" | Instrument Sans 700 maiuscolo | 10,5 | 7 | 1 | Su ocra |

## Regole

- Nessuna enfasi in corsivo colorato nei titoli. Il beneficio si dice con le parole.
- Allineamento a sinistra, niente testo giustificato.
- Unità di misura staccate dal numero con uno spazio: "2 kg", "130 cm".
- I simboli ≤ e ≥ non sono nel set di Instrument Sans: si scrive "entro", "almeno", "massimo". Il controllo del PDF offline lo verifica.
- Corpo minimo in stampa 6 pt (biglietto compreso).

## Implementazione

```css
@font-face{font-family:"Instrument Sans";src:url("fonts/InstrumentSans-Regular.ttf") format("truetype");font-weight:400}
@font-face{font-family:"Instrument Sans";src:url("fonts/InstrumentSans-Bold.ttf") format("truetype");font-weight:700}
@font-face{font-family:"Crimson Pro";src:url("fonts/CrimsonPro-Regular.ttf") format("truetype");font-weight:400}
@font-face{font-family:"Crimson Pro";src:url("fonts/CrimsonPro-Italic.ttf") format("truetype");font-style:italic}
```

Il file completo è `assets/b.css`. Per il sito conviene aggiungere le versioni WOFF2 generate dagli stessi TTF.
