# Motion · Riferimento A

## Principi

1. **Ogni animazione mostra una misura.** Si vede una grandezza che cambia: una quota che si traccia, una barra di fase che si riempie, un contatore che arriva al valore. Se non c'è niente da misurare, l'elemento entra senza animazione.
2. **Passo di 120 ms.** Tutte le durate sono multipli di 120 ms (120, 240, 360, 480, 720). Le sequenze hanno un ritmo regolare, come lo scatto di uno strumento.
3. **Una curva sola.** Entrate con `cubic-bezier(.2,0,0,1)` (partenza decisa, arresto morbido, come un carrello che si ferma sul fine corsa). Tracciati lineari per righelli e quote. Nessun rimbalzo, nessuna elasticità, nessun effetto di luce.
4. **Da sinistra a destra, dal basso in alto.** Le cose si costruiscono come si disegna una tavola: prima il piano di riferimento, poi l'oggetto, poi le quote.
5. **Il robot resta reale.** Nei video il robot si mostra in tempo reale, senza accelerazioni né rallentamenti spettacolari. Il tempo si legge su un contatore.
6. **Rispetta chi chiede meno movimento.** Con `prefers-reduced-motion` il marchio compare già costruito.

## Logo animato

File: `logo/animazione.html` (CSS e SVG, ciclo di 6 secondi).

| Tempo | Cosa succede |
|-|-|
| 0 a 0,6 s | si traccia il piano di riferimento, una linea sottile sotto il logotipo |
| 0,36 a 1,56 s | il logotipo si scopre da sinistra a destra, come uscisse da un plotter |
| 1,68 a 2,88 s | compare la quota verticale del vuoto della A |
| 2,04 a 3,12 s | il contorno del vuoto scende sulla linea di base |
| 3,24 s | il contorno diventa il triangolo pieno: il riferimento è fissato |
| 3,6 a 5,4 s | il marchio resta fermo con l'etichetta A sotto il triangolo |

Usi: apertura e chiusura dei video, schermata di avvio della presentazione, attesa nella pagina del preventivo online. Durata breve (1,8 s) per i reel: solo scoperta del logotipo e caduta del triangolo.

## Micro interazioni sul sito

| Elemento | Comportamento | Durata |
|-|-|-|
| Pulsante | il riquadro passa da contorno a pieno grafite | 120 ms |
| Link | sottolineatura che si traccia da sinistra | 240 ms, lineare |
| Barra delle fasi | ogni fase si campisce in sequenza allo scroll | 240 ms per fase |
| Dato numerico | contatore da 0 al valore con cifre tabellari | 720 ms |
| Quota su immagine | tacche, poi linea, poi valore | 120 + 240 + 120 ms |

## Video

- Titoli: entrano con la regola del passo, restano almeno 2,4 s, escono senza animazione.
- Sovrimpressioni: riquadro di controllo con valore e unità, posizionato su un angolo della griglia, mai sul robot.
- Transizioni: stacco netto. Nessuna dissolvenza incrociata, nessun effetto glitch.
- Chiusura: logo animato breve su alluminio, con l'indirizzo web in etichetta.
