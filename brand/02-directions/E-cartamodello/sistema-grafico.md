# Sistema grafico: Cartamodello

Sei strumenti del modellista diventano il linguaggio di Abra. Ognuno ha un significato fisso: chi monta un post o un preventivo sa quale usare senza chiedere a un designer.

## 1. Gli elementi

| Elemento | Forma | Significato | Dove |
|-|-|-|-|
| **Il punto di imbastitura** | Linea tratteggiata a capi tondi, tratto 3 px (schermo) o 0,5 mm (stampa), ritmo 14 su 8 | **In prova**: fase non ancora accettata, valore da misurare, dato di esempio | Timeline, bottoni secondari, bordi dei riquadri "Esempio" |
| **La cucitura** | La stessa linea, continua | **Misurato e firmato** | Fase accettata, intestazioni di tabella, separatori |
| **Il metro** | Nastro giallo con tacche al centimetro e numeri ogni 10 | **Una misura vera**: altezza del robot, durata in settimane, millimetri del biglietto | Accanto ai robot, come linea del tempo, sul bordo del biglietto |
| **Il pezzo di carta** | Riquadro carta modello con un angolo tagliato, tacche triangolari sui lati, margine tratteggiato interno | **Un oggetto definito**: una fase, una scheda misure, un limite | Copertina preventivo, hero, post, totem |
| **Il margine dichiarato** | Riquadro con un secondo bordo tratteggiato all'interno | **Il limite**: cosa il robot non fa | Box "Margine dichiarato" nei preventivi e nelle schede |
| **Il segno a gesso** | Una croce bianca a due tratti | **Un punto preciso nello spazio**: dove poggia il piede, dove sta il robot nello stand | Foto, piante, post |
| **Il cartellino** | Etichetta con foro e angoli smussati | **Un'informazione attaccata a un oggetto**: revisione, data della prova generale, numero di cassa | Casse, schede, annotazioni |

Il filo del simbolo è lo stesso punto di imbastitura: quando attraversa un pezzo di carta passa **sotto**, e si vede solo negli spazi (copertina del preventivo, fronte del biglietto, logo animato).

## 2. Griglia

- **Modulo**: 8 px a schermo, 4 mm in stampa.
- **Sito (1440 px)**: margini 64 px, 12 colonne, canale 24 px. Il titolo occupa 7 colonne, il pezzo di carta con il robot 5.
- **A4 (preventivo, manuale)**: margini 15 mm laterali, 14 mm in alto, 12 colonne da 10,9 mm, canale 4 mm. Le tabelle stanno su 12 colonne; il riquadro dei limiti chiude sempre la pagina.
- **Post 1200 x 1500**: margini 72 px, 3 colonne per gli elenchi; il pezzo di carta occupa la fascia centrale a tutta larghezza.
- **Verticali 1080 x 1920**: area sicura da 150 px in alto e in basso.

## 3. Iconografia

Sei icone in `icone/`, griglia 24 px, tratto 1,75 px, capi e giunti tondi, nessun riempimento. Le parti "in prova" sono tratteggiate.

| File | Concetto | Disegno |
|-|-|-|
| `misure.svg` | Assessment, sopralluogo | Metro avvolgibile con nastro e tacche |
| `simulazione.svg` | Digital twin | Cubo e la sua copia tratteggiata, il gemello |
| `prova.svg` | POC sul robot vero | Pezzo con tacca e segno a gesso |
| `modello.svg` | Codice e documentazione consegnati | Foglio con angolo piegato, tacca e righe imbastite |
| `assistenza.svg` | Assistenza e formazione | Cartellino appeso con filo |
| `noleggio.svg` | Noleggio a giornata | Calendario con il giorno segnato a gesso |

## 4. Pattern

Il **tavolo da taglio**: una griglia sottile a 2 cm (o 50 cm in pianta) in flanella al 10% sotto i pezzi di carta. È l'unico pattern ammesso. Texture di tessuto e fotografie di stoffa restano escluse.

## 5. Diagrammi e dati

- **Le fasi sono pezzi**, numerati P0 a P5, con il nome del mestiere sopra quello tecnico (Le misure, L'imbastitura, La prova, Il modello).
- **Il tempo è un metro**: una tacca per settimana, le fasi sono barre tratteggiate finché non sono firmate, poi diventano piene.
- **Ogni grafico mostra il margine**: la banda di tolleranza o il limite dichiarato è un riquadro tratteggiato attorno al valore, mai una nota a piè di pagina.
- **Colori nei grafici**: flanella per il valore misurato, blu gesso per il confronto, giallo solo per evidenziare un punto. Mai più di tre serie.
- **Mappe LiDAR e digital twin** si stampano come cartamodelli: linee flanella su carta modello, quote a mano, nessun effetto di profondità o luminosità.
- **Esempio**: ogni numero inventato porta l'etichetta "Esempio" con bordo tratteggiato. Il tratteggio dice già che il dato è in prova.

## 6. Regole di composizione

1. Un solo pezzo di carta protagonista per pagina.
2. Il robot non è mai al centro esatto: sta su un pezzo di carta, con il metro accanto.
3. Le foto dei robot si usano in scala di grigi, in moltiplica sulla carta, così ogni produttore ha lo stesso trattamento.
4. Il giallo compare al massimo in due punti per composizione.
5. Il logo sta in alto a sinistra o centrato sul fronte di un oggetto; mai accanto al logo di un produttore.

## 7. File di sistema

- `assets/sistema.css`: colori, classi tipografiche, etichetta "Esempio", metro lineare.
- `assets/metro.js`: genera il metro SVG da attributi `data-metro` (orizzontale o verticale, centimetri o settimane).
- `logo/`: tutte le versioni del marchio, `favicon-16.svg` disegnato sulla griglia di 16 pixel.
