# Sistema grafico · In squadra (v3)

Il sistema prende i suoi elementi dal disegno tecnico e dalla strumentazione di misura. Ognuno ha una funzione: dove non c'è niente da misurare, da dichiarare o da firmare, l'elemento non compare.

## Il marchio in uso

| File | Quando |
|-|-|
| `logo/orizzontale.svg` | versione principale: sito, documenti, firme, post |
| `logo/verticale.svg` | spazi stretti e alti: totem, colonne, copertine strette |
| `logo/simbolo.svg`, `simbolo-netto.svg` | legatura Ab da sola, dopo che il nome è già stato letto |
| `logo/monogramma.svg` | legatura bianca su piastra verde: avatar, adesivi, timbro di verifica |
| `logo/monogramma-grafite.svg` | stessa piastra in grafite, per fondi verdi |
| `logo/favicon.svg` | icona da 24 px in su |
| `logo/favicon-16.svg` | versione ottica disegnata pixel per pixel, sotto i 24 px |
| `logo/mono-positivo.svg`, `mono-negativo.svg` | stampa a un colore; il negativo è solo la forma bianca, il fondo lo dà il supporto |
| `*-bianco.svg` | su verde, grafite, verde profondo e fotografie scure |

- **Area di rispetto**: un quarto dell'altezza delle maiuscole su ogni lato, già inclusa nei file.
- **Dimensioni minime**: logotipo orizzontale 90 px o 22 mm di larghezza; simbolo 16 px o 5 mm di altezza. Sotto i 24 px si usa sempre `favicon-16.svg`.
- **Geometria fissa, non modificabile**: A intera con aste a pendenza 2 a 1 e traversa; piede destro della A sull'asta verticale della b; vuoto tra le due lettere a forma di squadra 2 a 1. È l'oggetto del deposito come marchio figurativo.
- **Non si fa**: separare la A dalla b, cambiare la pendenza, togliere la traversa, ricomporre il nome con un carattere, colorare parti del segno, affiancare il marchio a quello di un produttore di robot in un unico blocco.
- **Su robot, casse e attrezzature** il segno va in grafite su alluminio o in bianco su grafite; il verde pieno resta ai formati di comunicazione.

## Griglie

### Schermo
- **Sito, 1440 px**: 12 colonne, margini 64 px, canale 24 px. Unità verticale 8 px. Il titolo display occupa le colonne 1 a 7; la tavola tecnica (immagine con quote) le colonne 8 a 12.
- **Mobile, 390 px**: 4 colonne, margini 20 px, canale 16 px.
- **Post LinkedIn 1200 × 1500** e **reel 1080 × 1920**: margini 72 px; titolo in alto, tavola al centro, targa dati e logotipo in basso. Nel reel i contenuti chiave stanno nella fascia centrale 1080 × 1350 che Instagram mostra nella griglia del profilo.

### Carta
- **A4**: margini 15 mm, 12 colonne con canale 4 mm, linea di base 4 mm. Copertina con testata verde per il 40 % dell'altezza, cartiglio in piede su ogni pagina.
- **Biglietto 85 × 55 mm**: margine 4 mm; fronte in Pantone 348 C con il segno Ab fuori formato, retro bianco come targa dati; nessun testo sotto i 6 pt.

## Elementi grafici

| Elemento | Origine | Funzione | Dove |
|-|-|-|-|
| **Triangolo a terra** ▲ | simbolo di riferimento ISO 5459 | segna il punto da cui si misura: P0, il piano d'appoggio del robot, il punto d'incontro con il pubblico sullo stand (adesivo verde a pavimento) | documenti piccolo e grafite; stand e reel grande e verde |
| **Riquadro di controllo** | cornice a celle delle tolleranze geometriche ISO 1101 | contiene un fatto verificabile: grandezza, valore, fase o riferimento. La cella verde dice che il criterio è misurato | preventivi, hero, post, totem |
| **Quota** | linea di misura con tacche alle estremità | dà la dimensione reale di un robot, di un oggetto, di una durata | immagini di robot, schemi delle fasi, livree |
| **Campo verde** | piastra del monogramma | testata dei formati di comunicazione: copertina del preventivo, post, totem, fronte del biglietto | un campo per superficie, sempre a filo di un bordo |
| **Tratteggio di limite** | sezione nel disegno tecnico | marca i limiti dichiarati accanto al valore | schede, preventivi, hero |
| **Cartiglio** | blocco del titolo nelle tavole tecniche | documento, revisione, data, foglio, firma | ogni pagina di preventivo e manuale |
| **Targa dati** | targhe di macchina | elenco etichetta e valore con filetti; quadratino verde (misurato) o tratteggiato (limite) a destra | schede robot, verbali di consegna, flight case |
| **Linea d'asse** | linea mista tratto e punto del disegno tecnico | asse di simmetria nelle costruzioni e negli schemi | tavole di costruzione, livree |

Regole:
- Filetti da 1 px (separatori) e 1,5 px (cornici). Nessuno spessore intermedio.
- Angoli vivi. Nessun raggio di raccordo, tranne il favicon e gli schemi dei robot.
- Nessuna ombra, nessun gradiente. Unica tinta ammessa: il segno Ab in bianco al 16 % sul campo verde (fronte del biglietto). Le immagini dei robot stanno su una tavola bianco disegno o su alluminio, con quote.
- Robot e persone sempre in scala tra loro. Senza foto proprie il pubblico si indica con le linee di vista (altezza degli occhi, 1600 mm e 1100 mm) e con figure in pianta dello stand (spalle arrotondate e testa), mai con sagome da cartello. Il G1 segnaposto è l'immagine ufficiale in bianco e nero, dichiarata; il quadrupede dei post è uno schema vettoriale in pianta.
- La parola "Esempio" in un riquadro accompagna ogni numero, verbale o criterio inventato.

## Iconografia

Sei icone disegnate su griglia 24 × 24 px, tratto 1,5 px, terminali e giunzioni vive, file in `icone/`:

| File | Significato |
|-|-|
| `misura.svg` | quota con frecce e triangolo di riferimento: assessment, prove, misura |
| `simulazione.svg` | robot reale e il suo gemello tratteggiato: simulazione e digital twin |
| `codice.svg` | parentesi angolari in un riquadro: codice nel repository del cliente |
| `manuale.svg` | manuale con il triangolo di riferimento in copertina: documentazione |
| `assistenza.svg` | chiave fissa: assistenza e manutenzione |
| `copione.svg` | fumetto con testo e spunta: copione approvato per l'umanoide negli eventi |

Le icone accompagnano un testo, non lo sostituiscono. A 24 px si usano in grafite; a 48 px e oltre il tratto resta 1,5 px scalando il viewBox, per mantenere il segno sottile da strumento.

## Pattern

- **Campo di legature**: il segno Ab da 6 mm su passo 20 mm, bianco su verde di misura, per nastro adesivo, carta da imballo e interno dei flight case.
- **Campo di riferimenti**: triangoli da 3 mm su passo 10 mm, grafite su alluminio, per i retri dei documenti.

Entrambi i pattern si generano in CSS con `repeating-linear-gradient` o in SVG con `<pattern>`; non servono file grafici.

## Linguaggio per diagrammi e dati

- **Le fasi sono una barra misurata.** Le larghezze sono proporzionali alla durata; la fase conclusa si campisce in grafite; ogni passaggio di fase è un triangolo di riferimento con la parola "Decidi".
- **Ogni numero ha un'unità e un'origine.** Accanto al valore si scrive se è misurato (quadratino verde), stimato (grafite) o un limite (quadratino tratteggiato). Le valutazioni interne si marcano come tali.
- **Grafici**: barre e linee in grafite, una sola serie in evidenza in verde di misura; assi con tacche come una scala, nessuna griglia di fondo piena, etichette direttamente sui dati. Niente torte, niente 3D.
- **Mappe LiDAR e nuvole di punti**: in grafite su bianco disegno, come un rilievo stampato, con quote e scala grafica. Mai su fondo nero con punti luminosi.
- **Tabelle**: filetto da 1,5 px sotto l'intestazione e in chiusura, filetti da 1 px tra le righe, nessuna campitura alternata, numeri allineati a destra con cifre tabellari.

## Favicon a 16 px

A 16 px il segno vettoriale scalato perde la traversa. Per questo `favicon-16.svg` è disegnata pixel per pixel su griglia 16: A intera con aste di 2 px a gradini, vuoto della A di 2 × 2 px, traversa di 1 px, piede destro sull'asta della b di 2 px, vuoto a squadra tra A e b di almeno 1 px fino alla traversa (3 px in cima), pancia della b con vuoto di 2 × 4 px, piastra verde piena. Verificata anche su fondo scuro. Si usa per favicon e icone fino a 24 px; da 24 px in su `favicon.svg`.
