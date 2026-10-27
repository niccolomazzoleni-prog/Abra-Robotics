# Sistema grafico: Cartamodello (v2)

Gli strumenti del modellista diventano il linguaggio di Abra. La metafora sta nella logica del sistema; nei testi per i clienti si usano parole del settore (sopralluogo, simulazione, prova, consegna).

## 1. La regola del gesso e della cucitura

| Stato | Come si disegna | Esempio |
|-|-|-|
| **Da approvare, ancora da misurare** | In **gesso**: bordo sottile Blu segno `#2F5D9E` (2 px a schermo, 0,35 mm in stampa) su fondo chiaro, oppure Gesso blu su flanella | Fasi di un preventivo non ancora firmate, etichetta "Esempio" |
| **Misurato e firmato** | **Cucito**: Flanella piena o linea Flanella da 2 px | Fase accettata, totali, intestazioni di tabella |

Il gesso si cancella, la cucitura resta. Nella v1 la distinzione era tratteggio contro linea continua; il tratteggio si leggeva come mezzeria stradale o nastro da cantiere ed è stato eliminato da tutto il sistema, compreso il marchio.

## 2. Gli elementi

| Elemento | Forma | Quando si usa |
|-|-|-|
| **Il metro** | Nastro Gesso blu con tacche Flanella al centimetro (o alla settimana) e cifre ogni 10 | **Solo dove misura qualcosa di vero**, con la scala allineata all'oggetto: altezza del G1 (0 ai piedi, 130 alla testa), settimane del preventivo, millimetri del biglietto. Mai come cornice |
| **La scheda** | Pezzo di Carta modello con un angolo tagliato e una tacca sul lato | Il robot misurato, il percorso del preventivo, i limiti |
| **Il richiamo** | Linea Flanella da 1,5 px con un punto sull'oggetto misurato | Dal punto del robot alla sua misura |
| **Il segno a gesso** | Croce in Blu segno a due tratti | Dove poggiano i piedi, dove sta il robot nello stand |
| **Il rombo di decisione** | Rombo Flanella sul metro alla fine di ogni fase | "Qui decidi se proseguire" |
| **Il cartellino** | Etichetta Gesso blu con foro | Informazioni attaccate a un oggetto: data della prova generale, numero di cassa |
| **I limiti dichiarati** | Riquadro Carta modello con bordo interno Flanella | "Cosa il robot non farà", nella stessa pagina delle prestazioni |

Il filo del simbolo (la coda in Gesso blu che esce dalla gamba destra della A) non si usa come decorazione: compare solo nel marchio.

## 3. Marchio a piccole dimensioni

- **Sotto 24 px** solo `logo/favicon-16.svg` (disegnato sulla griglia di 16 pixel) o `favicon-16-mono.svg`.
- Da 24 a 64 px `logo/monogramma.svg` (aste e traversa più spesse, filo più corto).
- Sopra i 64 px `logo/simbolo.svg` o le versioni bicolore e negativo.
- La traversa della A è sempre piena e visibile, a ogni dimensione.

## 4. Griglia

- Modulo 8 px a schermo, 4 mm in stampa.
- Sito (1440 px): margini 64 px, 12 colonne, canale 24 px; titolo su 7 colonne, scheda del robot su 5.
- A4: margini 15 mm, 12 colonne da 10,9 mm, canale 4 mm; il percorso del preventivo usa una settimana = 24 px (6,35 mm).
- Post 1200 x 1500: margini 72 px, elenchi su 3 colonne. Verticali 1080 x 1920: area sicura di 150 px in alto e 120 in basso.

## 5. Iconografia

Sei icone in `icone/`, griglia 24 px, tratto 1,75 px, capi e giunti tondi, nessun riempimento, nessun tratteggio.

| File | Concetto |
|-|-|
| `misure.svg` | Sopralluogo e assessment: metro avvolgibile |
| `simulazione.svg` | Simulazione e modello digitale: il cubo e il suo gemello |
| `prova.svg` | Prova sul robot vero: scheda con tacca e segno a gesso |
| `modello.svg` | Codice e documentazione consegnati: foglio con angolo piegato |
| `assistenza.svg` | Assistenza e formazione: cartellino con filo |
| `noleggio.svg` | Noleggio a giornata: calendario con il giorno segnato |

## 6. Diagrammi e dati

- Le fasi si disegnano in scala sul metro delle settimane; i bordi Blu segno diventano pieni Flanella quando la fase è firmata.
- Ogni grafico porta il limite dichiarato nello stesso riquadro del valore.
- Serie: Flanella per il valore misurato, Blu segno per il confronto; il Gesso blu evidenzia un solo punto.
- Mappe LiDAR e modelli digitali si stampano in Flanella su Carta modello, con le quote; nessun effetto di luce.
- Ogni dato inventato porta l'etichetta "Esempio".

## 7. Regole di composizione

1. Una sola scheda protagonista per pagina.
2. Le foto dei robot sono in scala di grigi, in moltiplica sulla carta: robot di produttori diversi hanno lo stesso trattamento.
3. Il Gesso blu compare al massimo in due punti per composizione.
4. Il logo non sta mai accanto al logo di un produttore.
5. Negli eventi il pubblico è disegnato a sagome Flanella, mai con foto di persone.

## 8. File di sistema

- `assets/sistema.css`: colori, sei tagli tipografici statici, etichetta "Esempio", regola gesso e cucitura.
- `assets/metro.js`: disegna il metro da attributi `data-metro`; la tacca dello zero sta a 2 px dall'inizio dell'elemento, quindi il metro si allinea all'oggetto con un calcolo semplice (vedi i commenti in `applicazioni/hero.html`).
- `logo/`: tutte le versioni del marchio; i sorgenti di generazione sono in `_lavoro/` (`geo2.js`, `build-logo-v2.js`).
