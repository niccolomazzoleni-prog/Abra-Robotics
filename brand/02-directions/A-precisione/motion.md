# Motion · In squadra (v3)

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
| 0 a 0,6 s | si traccia la linea di base |
| 0,48 a 1,2 s | sale l'asta verticale della b, con la pancia |
| 1,2 a 2,16 s | la A intera si scopre da sinistra e appoggia il piede all'asta della b |
| 2,16 a 4,08 s | compare il segno verde dei 90 gradi nella squadra vuota tra la A e la b |
| 2,4 a 3,72 s | il resto del logotipo si scopre da sinistra, come da un plotter |
| 3,72 a 5,52 s | il marchio resta fermo, poi si spegne e il ciclo riparte |

Usi: apertura e chiusura dei video, avvio della presentazione, attesa nella pagina del preventivo online. Per i reel una versione breve di 1,8 s: asta, diagonale, logotipo.

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
- Chiusura: logo animato breve su verde di misura, con l'indirizzo web in etichetta.
