# Sistema grafico: la grammatica della regia

Cinque elementi, tutti presi dal lavoro di palcoscenico e tutti riproducibili in HTML e CSS dal team. Lo spettacolo viene dalla scala (titoli enormi, robot in piedi sul palco), dal taglio (campiture con bordi netti, immagini tagliate dal formato) e dal ritmo (la scaletta delle fasi).

## 1. Il marchio e le sue regole

- **Simbolo**: la A di scena. Gambe come quinte, traverso come architrave, trapezio color Luce come palcoscenico acceso. Costruzione nel file `_lavoro/tools/amark.py` (parametri: apice 24% della larghezza, gamba 27%, traverso tra 58% e 71% dell'altezza, palco dal 76% con fuga del 5,2%).
- **Logotipo**: "Abra" in Archivo 85/800 con la A di scena; "Robotics" in Archivo 85/450 sulla stessa linea di base. Tracciati in `logo/`.
- **Versioni**: `orizzontale`, `orizzontale-negativo`, `verticale`, `verticale-negativo`, `mono-positivo`, `mono-negativo`, `simbolo`, `simbolo-negativo`, `simbolo-piccolo` (fughe allargate per 16 a 24 px), `monogramma` (quadrato Velluto per avatar e favicon), `favicon-16.png` disegnata a pixel.
- **Area di rispetto**: l'altezza del traverso della A su ogni lato.
- **Dimensioni minime**: logotipo orizzontale 22 mm in stampa e 96 px a schermo; simbolo 6 mm e 16 px (sotto i 24 px si usa `simbolo-piccolo`).
- **Il palco nella A è sempre Luce** nella versione a colori, oppure dello stesso colore della lettera nelle versioni monocromatiche. Mai in un terzo colore.
- **Unitree e gli altri produttori** si citano a testo ("piattaforme Unitree e di altri produttori"), mai in un lockup.

## 2. Griglie

| Formato | Margini | Colonne | Note |
|-|-|-|-|
| Web 1440 | 64 px | 12 colonne, 24 px di spazio | Il palco occupa sempre l'ultima fascia del primo schermo (da 160 a 200 px) |
| A4 preventivo | 52 a 56 px (circa 14 mm) | 6 colonne | La copertina divide la pagina: metà superiore su Carta, metà inferiore in scena |
| Social 1080 e 1200 | 72 a 80 px | 6 colonne | Nei reel tutto il testo importante sta tra 300 e 1640 px di altezza, fuori dalle interfacce di Instagram |
| Totem 80 x 200 cm | 6,4 cm | 4 colonne | Il palco parte a 130 cm da terra: le informazioni stanno ad altezza d'occhi di chi passa |

## 3. Gli elementi

### Il palco
Trapezio color Luce in fondo alla composizione, con i lati inclinati come le gambe della A (rientro in alto tra il 6% e il 9% per lato). È il posto delle informazioni che contano: la scaletta delle fasi, ciò che resta al cliente, la chiamata all'azione. In CSS: `.palco` con `clip-path:polygon(...)` in `sistema.css`.

### Il taglio di luce sul fondale
Un trapezio Quinta su Velluto che parte stretto dall'alto e si allarga verso il palco: la luce di un sagomatore sul fondale. Una sola sorgente per composizione, bordi netti. Si usa solo su Velluto.

### Il segno a terra
La T di nastro con cui in teatro si segna il posto dell'attore e in reparto il posto di una macchina. Nei layout indica dove sta il robot (o dove starà); come icona apre le etichette. Nella realtà è un nastro da pavimento color Luce da 50 mm: Abra lo mette sotto ogni robot in laboratorio, allo stand e nel reparto, così ogni foto propria porta il segno della marca anche senza logo.

### La scaletta
La sequenza P0 a P5 composta come una scaletta di regia: numero grande in Titolo di scena, nome della fase, una riga in corsivo con ciò che il cliente ha in mano alla fine ("Esci con i numeri per decidere"). È l'elemento ritmico del sistema e compare in hero, copertina e pagina delle fasi.

### Il copione e le didascalie
Le battute dei format eventi si compongono come un copione: nome del personaggio in Etichetta, battuta in Testo, indicazioni di regia in corsivo tra parentesi. Le stesse parentesi in corsivo portano i limiti dichiarati nei documenti tecnici.

## 4. Iconografia

Sei icone in `icone/`, griglia 48 x 48, tratto 3 px Velluto a terminazioni quadrate, e un piccolo palco color Luce sotto ogni soggetto: ogni servizio "va in scena".

| File | Servizio |
|-|-|
| `misura.svg` | Assessment e misura |
| `simulazione.svg` | Digital twin e simulazione (l'oggetto vero e la sua copia tratteggiata) |
| `fasi.svg` | POC a fasi (gradini che arrivano al segno a terra) |
| `codice.svg` | Codice consegnato nel repository del cliente |
| `formazione.svg` | Manuale e formazione |
| `evento.svg` | Noleggio per eventi (sagomatore, fascio e fumetto) |

Regole: a 24 px il palco resta; a 16 px si toglie. Su Velluto il tratto diventa Stucco e il palco resta Luce.

## 5. Pattern

**Pianta di palco**: una griglia di segni a T piccoli (8 px) ogni 80 px, Quinta su Velluto. Serve come fondo per slide di sezione e per le pagine interne del sito, al posto dei pattern tecnologici. Uso massimo: un fondo per pagina.

## 6. Diagrammi e dati

I dati si leggono come una prova: c'è sempre un criterio e c'è sempre la misura.
- **Barre e colonne**: barre piene Velluto su Carta, oppure Luce su Velluto, piatte e senza effetti tridimensionali.
- **Il criterio di accettazione** è una linea orizzontale Velluto da 2 px con un segno a T all'estremità e l'etichetta "Criterio" in Etichetta. La barra che lo supera passa in Luce: la misura "accende il palco".
- **Tempi e fasi**: diagramma di Gantt a blocchi pieni per le fasi decise, tratteggiati per quelle da decidere (vedi `applicazioni/preventivo-interna.html`).
- **Esempi**: ogni grafico con dati di prova porta l'etichetta "Esempio" in Rame.
- **Colori dei dati**, in ordine: Velluto, Luce, Fumo, Paglia. Mai più di quattro serie.
