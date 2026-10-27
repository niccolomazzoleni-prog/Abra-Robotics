# Sistema grafico · Riferimento A

Il sistema prende i suoi elementi dal disegno tecnico e dalla strumentazione di misura. Ognuno ha una funzione: dove non c'è niente da misurare, da dichiarare o da firmare, l'elemento non compare.

## Il marchio in uso

| File | Quando |
|-|-|
| `logo/orizzontale.svg` | versione principale: sito, documenti, firme, post |
| `logo/verticale.svg` | spazi stretti e alti: totem, colonne, copertine strette |
| `logo/simbolo.svg`, `simbolo-netto.svg` | avatar, adesivi, timbri, dopo che il nome è già stato letto |
| `logo/monogramma.svg` | timbro di revisione e verifica sui documenti |
| `logo/favicon.svg` | scheda del browser, icona dell'app, 16 e 32 px |
| `logo/mono-positivo.svg`, `mono-negativo.svg` | stampa a un colore, incisione, serigrafia |
| `*-bianco.svg` | su grafite e su fotografie scure |

- **Area di rispetto**: pari all'altezza del triangolo di riferimento della A (circa 0,29 volte l'altezza delle maiuscole) su ogni lato. È già inclusa nei file.
- **Dimensioni minime**: logotipo orizzontale 90 px o 22 mm di larghezza; simbolo 16 px o 5 mm di altezza.
- **Non si fa**: colorare il triangolo, separarlo dalla A, cambiare la pendenza, ricomporre il nome con un altro carattere, affiancare il marchio a quello di un produttore di robot in un unico blocco.

## Griglie

### Schermo
- **Sito, 1440 px**: 12 colonne, margini 64 px, canale 24 px. Unità verticale 8 px. Il titolo display occupa le colonne 1 a 7; la tavola tecnica (immagine con quote) le colonne 8 a 12.
- **Mobile, 390 px**: 4 colonne, margini 20 px, canale 16 px.
- **Post LinkedIn 1200 × 1500** e **reel 1080 × 1920**: margini 72 px; titolo in alto, tavola al centro, targa dati e logotipo in basso. Nel reel i contenuti chiave stanno nella fascia centrale 1080 × 1350 che Instagram mostra nella griglia del profilo.

### Carta
- **A4**: margini 15 mm, 12 colonne con canale 4 mm, linea di base 4 mm. Scala millimetrata in testa alla copertina, cartiglio in piede su ogni pagina.
- **Biglietto 85 × 55 mm**: margine 5 mm; il bordo inferiore del fronte porta 80 mm di righello.

## Elementi grafici

| Elemento | Origine | Funzione | Dove |
|-|-|-|-|
| **Triangolo di riferimento** ▲ | simbolo di riferimento ISO 5459 | segna il punto da cui si parte: P0, il piano d'appoggio del robot, le decisioni di fase | ovunque, sempre piccolo e pieno |
| **Riquadro di controllo** | cornice a celle delle tolleranze geometriche ISO 1101 | contiene un fatto verificabile: grandezza, valore, fase o riferimento. La cella verde dice che il criterio è misurato | preventivi, hero, post, totem |
| **Quota** | linea di misura con tacche alle estremità | dà la dimensione reale di un robot, di un oggetto, di una durata | immagini di robot, schemi delle fasi, livree |
| **Scala millimetrata** | righello, strumenti di misura | firma del bordo: testa dei documenti e dei post, base delle fasi nel sito, fronte del biglietto | un solo bordo per superficie |
| **Cartiglio** | blocco del titolo nelle tavole tecniche | documento, revisione, data, foglio, firma | ogni pagina di preventivo e manuale |
| **Targa dati** | targhe di macchina | elenco etichetta e valore con filetti; quadratino verde (misurato) o giallo (limite) a destra | schede robot, verbali di consegna, flight case |
| **Linea d'asse** | linea mista tratto e punto del disegno tecnico | asse di simmetria nelle costruzioni e negli schemi | tavole di costruzione, livree |

Regole:
- Filetti da 1 px (separatori) e 1,5 px (cornici). Nessuno spessore intermedio.
- Angoli vivi. Nessun raggio di raccordo, tranne il favicon e gli schemi dei robot.
- Nessuna ombra, nessun gradiente, nessuna trasparenza decorativa. Le immagini dei robot stanno su una tavola bianco disegno con quote, come in un catalogo tecnico.
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

- **Campo millimetrato**: griglia a 1 mm e 10 mm in Linea su Bianco disegno, per i retri dei documenti, le buste e la carta da lettera. Una sola intensità, mai sotto il testo.
- **Campo di riferimenti**: triangoli di riferimento da 3 mm su passo 10 mm, grafite su alluminio, per nastri adesivi, carta da imballo e sfondo della cassa di trasporto.

Entrambi i pattern si generano in CSS con `repeating-linear-gradient` o in SVG con `<pattern>`; non servono file grafici.

## Linguaggio per diagrammi e dati

- **Le fasi sono una barra misurata.** Le larghezze sono proporzionali alla durata; la fase conclusa si campisce in grafite; ogni passaggio di fase è un triangolo di riferimento con la parola "Decidi".
- **Ogni numero ha un'unità e un'origine.** Accanto al valore si scrive se è misurato (verde), stimato (grafite) o un limite (giallo). Le valutazioni interne si marcano come tali.
- **Grafici**: barre e linee in grafite, una sola serie in evidenza in verde segnale; assi con tacche come una scala, nessuna griglia di fondo piena, etichette direttamente sui dati. Niente torte, niente 3D.
- **Mappe LiDAR e nuvole di punti**: in grafite su bianco disegno, come un rilievo stampato, con quote e scala grafica. Mai su fondo nero con punti luminosi.
- **Tabelle**: filetto da 1,5 px sotto l'intestazione e in chiusura, filetti da 1 px tra le righe, nessuna campitura alternata, numeri allineati a destra con cifre tabellari.
