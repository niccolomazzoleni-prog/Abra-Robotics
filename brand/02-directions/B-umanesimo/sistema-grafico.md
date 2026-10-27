# Sistema grafico. Territorio B, Misura d'uomo

## Il principio: le tre forme montate a vista

Tutto il sistema nasce dai tre pezzi del simbolo.

| Forma | Nel simbolo | Nel sistema |
|-|-|-|
| **Disco** | La pancia rossa della a | Campitura principale, sfondo del robot, segno delle fasi nei diagrammi, punto delle etichette |
| **Arco** | La spalla ocra | Cornice superiore, sagoma del totem e della targhetta, voce dell'umanoide (archi concentrici) |
| **Asta** | Il tratto verticale inchiostro | Bordo, pavimento su cui poggia il robot, filetto, fase finale nei diagrammi |

Regole di montaggio:
1. **Il giunto si vede.** Dove il disco incontra l'asta resta una finestra del colore di fondo. È la firma del sistema e va mantenuta anche nelle composizioni grandi.
2. **Una sola composizione per superficie.** Le forme si scalano dal simbolo (la geometria è nel generatore `_strumenti/scene.js`: un fattore di scala e una posizione; `_strumenti/build.js` rigenera i file del logo), ruotano solo di 90 gradi, possono uscire dal formato su uno o due lati.
3. **Un solo grande rosso.** In ogni composizione il disco rosso è il pezzo più grande; arco e asta lo accompagnano.
4. **Il robot sta sulla linea di base.** Quando c'è un robot, poggia sulla base della a o sull'asta orizzontale. È la misura d'uomo: il robot è messo in scala con la lettera e con le persone.
5. **Nessun ornamento aggiunto.** Niente ombre, gradienti, texture o particelle: colore pieno e carta.

## Griglie

**Sito (1440 px)**: 12 colonne, margini laterali 64 px, intervallo 24 px. Il testo occupa le colonne da 1 a 6; la composizione delle forme le colonne da 8 a 12 e può uscire dal bordo destro. Barra di navigazione alta 92 px. Fascia dei segmenti (aziende, laboratori, eventi) a tre colonne in basso.

**Documenti A4**: margini 56 px a 96 dpi (circa 15 mm) ai lati, 44 px in alto nelle pagine interne. Due griglie: copertina con campo colore nei primi 57% della pagina e testo sotto; pagine interne a una colonna di testo da 600 px con tabelle a cinque colonne. Intestazione corrente con simbolo, numero d'offerta e pagina.

**Social**: 1200 x 1500 per LinkedIn (scena in alto per il 57%, testo sotto), 1080 x 1920 per reel e storie, con il titolo nei primi 600 px e i contenuti chiave dentro l'area centrale 1080 x 1350 che Instagram mostra nella griglia.

**Stampa e allestimento**: totem e targhette con sagoma ad arco (raggio uguale a metà larghezza). Il totem è la a montata in grande: l'arco ocra segue il bordo superiore, l'asta inchiostro scende sul lato destro.

## Elementi grafici

- **Etichetta con disco**: Hanken 600 preceduta da un disco del colore della serie. Sostituisce gli occhielli tutto maiuscolo.
- **Cartellino**: riquadro carta con un dato e una frase in corsivo, come la didascalia di un museo ("130 cm, all'altezza del petto di un adulto"). Si appoggia sulle foto e sulle composizioni.
- **Linea di misura**: filetto inchiostro verticale con due tacche, accanto al robot. Una sola per immagine.
- **Riquadro dei limiti**: fondo ocra chiara, disco rosso, testo Newsreader. Compare nella stessa pagina delle prestazioni.
- **Bollino "Esempio"**: pillola inchiostro con testo avorio maiuscolo. Obbligatorio su ogni dato, criterio, prezzo o citazione di esempio.
- **Pulsanti**: pillola rossa con testo carta e un piccolo disco ocra in coda; secondario con filetto inchiostro.

## Iconografia

Sei icone in `icone/`, griglia 48 x 48, costruite solo con dischi, archi e aste, due colori (inchiostro più rosso), nessun contorno sottile.

| File | Significato |
|-|-|
| `prova.svg` | Prova sul banco: asta graduata e disco da misurare |
| `simulazione.svg` | Simulazione e digital twin: reale e virtuale sovrapposti, con il giunto visibile |
| `fasi.svg` | POC a fasi: dischi crescenti su un'asta, l'ultimo rosso è la decisione |
| `consegna.svg` | Documentazione consegnata: foglio ad arco con sigillo |
| `formazione.svg` | Formazione e tesisti: libro aperto |
| `voce.svg` | Umanoide che parla al pubblico: figura e archi della voce |

Dimensioni d'uso: 24, 32, 48 px. Sotto i 24 px si usa solo il colore inchiostro.

## Pattern

Il pattern è una griglia di tessere quadrate in cui le tre forme ruotano di 90 gradi da una tessera all'altra, sempre con il giunto aperto (lo si vede in `presentazione.html`). Si usa per interni di scatole e flight case, carta da pacchi, sfondo delle storie Instagram di servizio. Mai dietro a un testo.

## Diagrammi e dati

Il territorio evita l'estetica da cruscotto: i numeri stanno dentro le frasi e nelle tabelle, i diagrammi sono pochi e fatti con le forme del marchio.
- **Fasi**: una linea orizzontale con dischi che crescono da P0 a P4 e un'asta per P5. Colore inchiostro per le fasi d'ufficio, ocra per la simulazione, rosso per il robot vero. Sopra, in corsivo, dove avviene la fase.
- **Confronti**: tabella a righe con filetti pietra, numeri in Hanken tabellare allineati a destra, unità sempre presenti.
- **Una cifra in evidenza**: Newsreader 400 grande, unità in Hanken, una frase in corsivo che la porta in termini umani.
- **Mappe LiDAR e nuvole di punti**: stampate in inchiostro su carta avorio, come una tavola di rilievo, con la scala in metri e il nord. Mai luminose su fondo scuro.
