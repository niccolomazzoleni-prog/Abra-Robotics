# Revisione art director, round 1: direzione A

File aperti: `logo/*.svg` (simbolo, orizzontale, monogramma), `logo/test.png`, tutti i PNG in `applicazioni/`, `palette.md`, `tipografia.md`, `concept.md`, `autocritica.md`.

## Voti

| Criterio | Voto | Motivazione |
|-|-|-|
| 1. Qualità del marchio | 7 | A solida e ben costruita (pendenza 2:1, tratto 16/100), il triangolo di riferimento regge a 16 px; il gesso di base resta una A con un triangolo dentro, che a distanza può leggersi come tenda o segnale stradale. |
| 2. Originalità | 6 | Il triangolo di riferimento ISO è un'idea propria; il linguaggio complessivo (grigio freddo, grotesk da segnaletica, cartigli) è quello di molti cataloghi di costruttori di macchine e sfiora Agility. |
| 3. Tipografia | 6 | Logotipo disegnato con cura e coerente con Barlow; Barlow in tre larghezze è corretta e producibile, ma è una scelta da default industriale e non dà una voce riconoscibile. |
| 4. Colore | 6 | Disciplina esemplare (verde misurato, giallo limite con significato); la base alluminio e grafite però è anonima, a colpo d'occhio non si distingue da un fornitore di automazione qualsiasi. |
| 5. Coerenza del sistema | 8 | Il sistema più coerente del round: riquadro di controllo, cartiglio, triangolo, righello e codice colore tornano identici su hero, preventivo, post, livrea. |
| 6. Qualità delle applicazioni | 7 | Preventivo interna di livello alto (criteri in riquadro di controllo, limiti e responsabilità accanto ai costi); reel e post invece sono impaginati come schede, senza un'immagine che resti in mente. |
| 7. Assenza di AI slop | 7 | Poco slop; restano alcune formule e un paio di elementi autoreferenziali (vedi sotto). |

**Voto complessivo: 6,7**

## Slop e problemi di copy trovati

- `applicazioni/biglietto.png`, fronte: "Robotica applicata. Prima la prova, poi l'investimento." La coppia "prima X, poi Y" è una struttura simmetrica da slogan con chiusura breve.
- `applicazioni/preventivo-cover.png`: la tavola "Costruzione del simbolo" sulla copertina di un'offerta a un cliente. Al direttore R&D serve il suo progetto in copertina; la costruzione del logo è materiale da manuale di marca.
- `applicazioni/hero.png`: quattro icone lineari stock (codice, cubo, documento, chiave inglese) sotto i pulsanti. Sono le uniche icone generiche del sistema e lo abbassano.
- `applicazioni/linkedin-sacmi-anonimo.png`: la versione anonima conserva data 29.10.2026, "Go2 EDU con LiDAR", "Tesi in azienda" e "Manuale tecnico rev 1.1": chi conosce il settore risale al cliente. Il brief chiede nessun dettaglio che lo renda riconoscibile.

## I 3 problemi più gravi

1. **Memorabilità bassa fuori dal documento.** Il sistema vince sulla carta e perde sui social e negli eventi: reel e totem sono tabelle ben fatte, senza un'immagine o un gesto che il pubblico ricordi.
2. **Vicinanza al linguaggio dei costruttori di macchine e di Agility.** Grigio, grotesk da segnaletica, filetti sottili e maiuscolo spaziato: tolto il triangolo, la pagina potrebbe essere di un integratore qualunque.
3. **Il segno vive di spiegazione.** Senza la didascalia ISO 5459 il triangolo è un dettaglio decorativo; a 16 px sparisce e resta una A generica.

## Feedback azionabili

1. `logo/simbolo.svg`: provare una variante con il triangolo pieno staccato di più dalla base delle aste (luce almeno 0,6 volte il tratto) e leggermente più grande del vuoto superiore, così a 16 e 32 px il triangolo resta visibile come elemento distinto e la lettura "tenda" si riduce.
2. `applicazioni/preventivo-cover.png`: togliere la tavola di costruzione del simbolo e mettere al suo posto lo schema della postazione del cliente (vista in pianta con quote e triangolo di riferimento A sul punto di misura). Il segno diventa strumento del progetto.
3. `applicazioni/hero.png`: sostituire le quattro icone stock con le icone proprie in `icone/` oppure con piccoli riquadri di controllo testuali; oggi contraddicono il resto del sistema.
4. `applicazioni/biglietto.png`: riscrivere la frase del fronte all'imperativo con beneficio, per esempio "Misura il robot nel tuo reparto prima di investire."; eliminare la coppia "prima la prova, poi".
5. `applicazioni/reel-g1.png` e `totem.png`: dare agli eventi un'immagine forte, per esempio il G1 fotografato in scala 1:1 accanto alla quota verticale a tutta altezza, con il triangolo di riferimento a terra come segno sul pavimento dello stand. La regola resta la stessa, cambia la scala.
6. `palette.md`: introdurre un terzo neutro più caldo o un fondo più profondo per i formati social, così la direzione si separa dal grigio dei cataloghi industriali senza perdere il codice dei segnali.
7. `applicazioni/linkedin-sacmi-anonimo.png`: togliere data esatta, revisione del manuale e "tesi in azienda", oppure generalizzarli ("ottobre 2026", "manuale tecnico").
8. `tipografia.md`: valutare per i titoli display una seconda voce più caratterizzata (anche solo Barlow Condensed 700 con spaziatura stretta, o un grotesk OFL meno diffuso) per dare un timbro proprio alle headline.

## Somiglianze con altre direzioni

- **A ed E**: entrambe usano il righello millimetrato sul biglietto da visita e la quota verticale accanto al robot nell'hero. Il motivo "metro" va assegnato a una sola delle due.
- **A e C**: stesso registro documentale (revisioni, cartigli, riquadri "Esempio", schede di prova) e stessa headline dell'hero ("Misura nel tuo reparto cosa farà il robot, prima di investire."). La differenza oggi sta quasi solo nel serif di C.
- **A e D**: entrambi i simboli sono una A piena con una figura pesante appoggiata alla linea di base fra le aste (triangolo in A, trapezio in D). A colpo d'occhio le due A si confondono.
