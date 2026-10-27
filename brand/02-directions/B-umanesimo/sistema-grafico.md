# Sistema grafico v2. Territorio B, Montato a vista

## Il principio: le pagine sono montate a vista

Nel marchio la pancia della a è staccata dall'asta e il giunto resta aperto: si vede come è fatta la lettera. Il sistema applica la stessa regola alle pagine. Ogni superficie è montata con **pannelli rettangolari** (bianco, Grigio Lettera, un solo rosso) separati da un **giunto** costante di carta: 12 px sullo schermo, 10 px sull'A4, 6 mm sul totem. Il giunto è l'unico elemento grafico ricorrente; dischi, archi e forme decorative della v1 sono stati eliminati.

Regole di montaggio:
1. **Un pannello, un contenuto.** Testo, immagine, dati, contatti stanno in pannelli diversi. Il lettore vede la struttura prima di leggere.
2. **Un solo pannello rosso per superficie**, dedicato al messaggio principale o al segmento prioritario (la manifattura nell'hero).
3. **Il robot sta su un pannello Grigio Lettera**, appoggiato a una fascia di pavimento, con il cartellino dati accanto.
4. **Nessun ornamento**: niente ombre, gradienti, forme geometriche di riempimento, texture. Il rosso e l'ocra sono campiture piene o filetti.
5. **Dati veri o marcati "Esempio"**: ogni numero di prova, limite o prezzo non confermato porta il bollino ocra.

## Griglie

- **Sito (1440 px)**: margine e giunto 12 px; barra di navigazione bianca alta 76 px; corpo a due colonne (testo 860 px, immagine il resto); fascia dei tre segmenti alta 150 px.
- **Documenti A4**: giunto 10 px. Copertina in cinque fasce: intestazione, pannello rosso del titolo, due pannelli "cosa sapete prima" e "cosa vi resta", pannello grigio con i dati del progetto e la sequenza delle fasi, piè di pagina. Pagine interne su fondo bianco, a una colonna, tabella a cinque colonne con il filetto verticale della fase.
- **Social**: LinkedIn 1200 x 1500 e reel 1080 x 1920 con le stesse fasce (intestazione, immagine, banda rossa, testo). I contenuti chiave del reel stanno nell'area centrale 1080 x 1350.
- **Allestimento**: totem 90 x 220 cm in tre pannelli (rosso, bianco, ocra) con giunto di 6 mm.

## Elementi

| Elemento | Descrizione | Dove |
|-|-|-|
| Giunto | Fessura di carta tra i pannelli | Ovunque |
| Etichetta | Instrument Sans 700 maiuscolo, preceduta da un trattino 18 x 3 px del colore della serie | Sopra i titoli |
| Cartellino dati | Pannello bianco con filetto rosso in alto, coppie etichetta e valore | Accanto a ogni robot |
| Sequenza delle fasi | Sei blocchi P0 a P5 con filetto superiore; la fase in corso in rosso | Copertina e pagina delle fasi |
| Riquadro dei limiti | Ocra chiara, nella stessa pagina delle prestazioni | Preventivi, schede |
| Bollino "Esempio" | Ocra con testo grafite maiuscolo | Ogni dato non confermato |
| Riga delle firme | Campi con filetto per chiudere una fase | Pagina delle fasi |
| Pulsante | Rettangolo grafite, testo carta; secondario con filetto | Sito |

## Il marchio nel sistema

- Marchio esteso orizzontale nell'intestazione di ogni superficie; sotto i 160 px di larghezza solo il logotipo "abra".
- Simbolo (la a con il giunto) per intestazioni correnti, adesivi, avatar.
- Sotto i 32 px solo la favicon disegnata pixel per pixel (`logo/favicon.svg` a 16 px, `logo/favicon-32.svg` a 32 px).
- Su rosso e su grafite si usa la versione negativa in carta o bianco.
- Il logotipo non si ricompone mai con un font: si usano i file SVG (rigenerabili con `_strumenti/build2.js`).

## Iconografia

Sei icone in `icone/`, griglia 48 x 48, tratto 3 px con terminali squadrati, grafite più un dettaglio rosso.

| File | Significato |
|-|-|
| `prova.svg` | Prova sul banco: il pezzo misurato accanto all'asta graduata |
| `simulazione.svg` | Simulazione e digital twin: modello reale e modello simulato sovrapposti |
| `fasi.svg` | POC a fasi: barre crescenti, l'ultima rossa è la decisione |
| `consegna.svg` | Codice e manuale consegnati |
| `formazione.svg` | Formazione dei tecnici e dei tesisti |
| `voce.svg` | Copione approvato per l'umanoide |

Uso a 24, 32, 48 px.

## Scene con persone

Per eventi e fiere le persone compaiono come **sagome piatte** in grigi (generatore `_strumenti/sagome.js`), senza volto, come nei rendering architettonici: il pubblico in primo piano, il tecnico Abra accanto al robot. Le scale sono reali (robot G1 130 cm, persone da 165 a 178 cm). Non si usano foto di persone prese online.

## Diagrammi e dati

- **Fasi**: blocchi in fila, mai frecce decorative.
- **Confronti**: tabelle con filetti grigi, numeri in Instrument Sans allineati, unità sempre presenti.
- **Dimensioni del robot**: cartellino con altezza, massa, carico, autonomia; nei disegni di montaggio quote in millimetri come in un disegno tecnico.
- **Mappe LiDAR**: stampate in grafite su bianco, con scala in metri e nord.
