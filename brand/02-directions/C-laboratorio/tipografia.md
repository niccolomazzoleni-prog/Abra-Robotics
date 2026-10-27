# Tipografia: il carattere delle riviste scientifiche e la macchina da scrivere del laboratorio

Due famiglie, entrambe OFL e gratuite, incluse in `fonts/` in versione **statica** (v2): STIX Two Text Regular, SemiBold, Bold e Italic dalla release ufficiale stixfonts v2.13, DM Mono Regular e Medium. Woff2 per il web, ttf per l'incorporamento nei PDF del Company Brain, dove Chrome le incorpora come TrueType (il file variabile della v1 finiva nel PDF come font Type 3). Nessun CDN.

## STIX Two Text: la voce

- **Cos'è**: serif progettato per lo STI Pub, il consorzio degli editori scientifici e tecnici (American Institute of Physics, American Mathematical Society, Elsevier, IEEE e altri), per comporre articoli, formule e tabelle. Ha maiuscoletto vero, numeri allineati e in stile antico, frazioni, apici e pedici.
- **Perché**: è il carattere che il pubblico dei laboratori ha letto in centinaia di paper. Porta autorevolezza senza nostalgia, legge bene in corpo piccolo e in titolo, ed è lontano dal grotesk usato da tutti i concorrenti rilevati.
- **Pesi usati**: Regular 400, SemiBold 600 per i titoli, Italic 400 per le note, Bold 700 solo per il grassetto nel testo.
- **Licenza**: SIL Open Font License 1.1 con Reserved Font Name "STIX" (`fonts/OFL-STIXTwoText.txt`). Usiamo i file ufficiali senza modifiche, quindi il nome resta lecito. Uso commerciale, web e incorporamento nei PDF liberi. Costo zero.

## DM Mono: le etichette e i dati

- **Cos'è**: monospaziato morbido disegnato da Colophon. Ha cifre chiare e lo zero barrato, utile nei codici di revisione e nei numeri di serie.
- **Ruolo**: metadati, etichette, numeri di fase, unità di misura, revisioni, ore del registro, indirizzi. Mai per titoli o paragrafi.
- **Pesi usati**: 400 e 500.
- **Licenza**: SIL Open Font License 1.1 (`fonts/OFL-DMMono.txt`). Costo zero.

Font di ripiego nel CSS: Georgia per il serif, ui-monospace e Menlo per il mono.

## Gerarchia

| Livello | Famiglia, peso | Web (px / interlinea) | Stampa A4 (pt / interlinea) | Note |
|-|-|-|-|-|
| Display | STIX 600 | 76 a 98 / 1,02 | 30 / 1,06 | Tracking -0,017 em, sempre all'imperativo |
| Titolo 1 | STIX 600 | 40 / 1,1 | 19 / 1,1 | Numerato come una sezione: "3 Fasi e criteri" |
| Titolo 2 | STIX 600 | 26 / 1,2 | 13 / 1,25 | |
| Lead | STIX 400 | 21 a 29 / 1,45 | 11 / 1,5 | Massimo 70 caratteri per riga |
| Testo | STIX 400 | 17 a 18 / 1,55 | 9,6 / 1,5 | |
| Nota a margine | STIX corsivo 400, grafite | 14 a 15 / 1,4 | 8,2 / 1,42 | Con numero di richiamo in DM Mono 500 |
| Didascalia | STIX 400 grafite + "Fig. 1" in maiuscoletto | 13 / 1,35 | 8 a 9 / 1,35 | Ogni immagine ha la sua didascalia |
| Etichetta | DM Mono 400 maiuscolo, tracking 0,08 em | 11 a 14 | 6,8 a 7,5 | Sezioni, campi, intestazioni di colonna |
| Dato | DM Mono 400 o 500 | 12 a 24 | 8 a 11 | Importi, durate, codici, ore |

## Regole di composizione

- **Maiuscoletto** (`font-feature-settings: "smcp", "c2sc"`) per "Fig.", "Tab.", "Tav." e per le sigle lunghe in un testo corrente.
- **Richiami numerici** in apice con DM Mono 500 al 42% del corpo; la nota corrispondente sta nella colonna a margine, alla stessa altezza.
- **Numeri**: in tabella cifre allineate di STIX o DM Mono; nel testo corrente cifre allineate, con lo spazio fine prima delle unità (15 s, 2 kg, 132 cm).
- **Allineamento**: a sinistra, bandiera libera, nessuna giustificazione nei paragrafi brevi.
- **Niente tutto maiuscolo nel serif.** Il maiuscolo è solo delle etichette mono.
- **Il logotipo non è un font.** In v2 "abra" è disegnato da zero con cerchi e aste (vedi `sistema-grafico.md`, Costruzione del marchio): non deriva da STIX né da altri caratteri e non si ricompone da tastiera. "ROBOTICS" nel lockup è DM Mono Medium convertito in tracciati, con spaziatura 90 unità. Usare sempre i file SVG di `logo/`.

## Alternative valutate

- Computer Modern (CMU, licenza OFL) è più riconoscibile come "LaTeX" ma ha un solo peso utile in titolo e una resa debole a schermo.
- IBM Plex Mono e JetBrains Mono sono più comuni nella comunicazione tecnologica e avvicinano il territorio A.
- Un carattere commerciale equivalente di livello superiore per il titolo sarebbe Tiempos Headline (Klim Type Foundry), licenza desktop e web da circa 700 euro per due pesi: non serve, STIX copre il bisogno.
