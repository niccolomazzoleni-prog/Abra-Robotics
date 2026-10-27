# Motion: annotare in tempo reale

Il movimento imita il gesto di chi annota una figura: prima la cosa, poi il punto, poi il filo, poi la nota. L'ordine resta sempre questo e gli elementi entrano uno dopo l'altro.

## Principi

1. **Una cosa alla volta.** Ogni elemento entra quando il precedente si è fermato. Ritardo tipico fra due elementi: 150 a 300 ms.
2. **Il punto è l'unico elemento che rimbalza.** Scala da 0 a 1 in 450 ms con un leggero superamento (cubic-bezier .2, 1.4, .4, 1). Tutto il resto si muove in modo lineare o con accelerazione dolce.
3. **Il filo si traccia.** Il filo cresce dalla parte del punto verso la nota (scaleX con origine sul punto), 400 a 550 ms, curva .6, 0, .2, 1.
4. **Il testo si scrive.** Le note compaiono a scatti come se fossero battute (steps), oppure con dissolvenza breve di 300 ms e 4 px di salita. Niente parole che volano.
5. **Nessun effetto luminoso.** Niente bagliori, scie, particelle, parallasse profondo. Il movimento serve a leggere nell'ordine giusto.
6. **Rispetto per chi riduce il movimento**: con `prefers-reduced-motion` tutto compare già fermo.

## Il logo animato (`logo/animazione.html`)

| Tempo | Cosa succede |
|-|-|
| 0 a 0,9 s | La A senza traversa sale dal basso: per un istante è la vecchia "Λ" di Abra |
| 0,9 s | Compare il punto, dentro la lettera |
| 1,25 a 1,8 s | Il filo si traccia verso destra e completa la A |
| 1,75 a 2,75 s | "bra Robotics" si scrive da sinistra a destra |
| 2,9 s | Sotto compare la nota "Robotica applicata · Laboratorio Abra · rev 1.0" con il punto giallo |

Durata totale circa 3,4 secondi. Versione breve per le sigle dei video: solo simbolo, 1,8 secondi.

## Applicazioni

- **Sito**: i richiami della figura in hero compaiono in sequenza quando la figura entra nel viewport; il numero di revisione in testata si aggiorna senza animazione.
- **Video e reel**: i richiami in sovrimpressione seguono la stessa grammatica e restano fermi almeno 2 secondi per poter essere letti.
- **Presentazioni**: i grafici si costruiscono per serie (prima il simulato, poi il misurato, poi il criterio), come in una lezione.
- **Interfacce**: hover dei link con sottolineatura che si allunga da sinistra in 200 ms; i bottoni non si ingrandiscono.
