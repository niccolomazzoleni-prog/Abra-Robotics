# Motion: annotare in tempo reale

Il movimento imita il gesto di chi annota una figura: prima la cosa, poi il punto, poi il filo, poi la nota. L'ordine resta sempre questo e gli elementi entrano uno dopo l'altro.

## Principi

1. **Una cosa alla volta.** Ogni elemento entra quando il precedente si è fermato. Ritardo tipico fra due elementi: 150 a 300 ms.
2. **Il punto è l'unico elemento che rimbalza.** Scala da 0 a 1 in 450 ms con un leggero superamento (cubic-bezier .2, 1.4, .4, 1). Tutto il resto si muove in modo lineare o con accelerazione dolce.
3. **Il filo si traccia.** Il filo cresce dalla parte del punto verso la nota (scaleX con origine sul punto), 400 a 550 ms, curva .6, 0, .2, 1.
4. **Il testo si scrive.** Le note compaiono a scatti come se fossero battute (steps), oppure con dissolvenza breve di 300 ms e 4 px di salita. Niente parole che volano.
5. **Nessun effetto luminoso.** Niente bagliori, scie, particelle, parallasse profondo. Il movimento serve a leggere nell'ordine giusto.
6. **Rispetto per chi riduce il movimento**: con `prefers-reduced-motion` tutto compare già fermo.

## Il logo animato (`logo/animazione.html`, v2)

| Tempo | Cosa succede |
|-|-|
| 0,25 s | L'asta della a cresce dal basso, poi compare il suo punto |
| 0,57 s | L'asta della b sale fino all'ascendente, poi il punto |
| 0,89 s | L'asta della r, il collo, il punto piccolo |
| 1,21 s | L'ultima a, asta e punto |
| 1,9 s | Compare "ROBOTICS" |
| 2,4 s | Sotto, la nota "Ogni lettera è un richiamo: prima il filo, poi il punto" |

Durata totale circa 2,9 secondi. Versione breve per le sigle: solo la a, 0,8 secondi. La vecchia "Λ" non compare più in nessuna fase.

## Applicazioni

- **Sito**: i richiami della figura in hero compaiono in sequenza quando la figura entra nel viewport; il numero di revisione in testata si aggiorna senza animazione.
- **Video e reel**: i richiami in sovrimpressione seguono la stessa grammatica e restano fermi almeno 2 secondi per poter essere letti.
- **Presentazioni**: i grafici si costruiscono per serie (prima il simulato, poi il misurato, poi il criterio), come in una lezione.
- **Interfacce**: hover dei link con sottolineatura che si allunga da sinistra in 200 ms; i bottoni non si ingrandiscono.
