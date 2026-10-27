# Revisione strategica, direzione C, round 2

Revisore: strategia. Data: 28/10/2026.
Materiali aperti: changelog.md, round1-sintesi.md, presentazione.html, logo/test.png, PNG v2 di hero, preventivo copertina, totem, reel, post LinkedIn anonimo; titoli di tutte le applicazioni HTML. Colore firma (giallo evidenziatore con inchiostro) assunto come vincolo, non valutato.

## Voti per criterio

| Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|
| 1. Coerenza con brief e brand platform | 8 | 8 | Evidenziatore solo sui dati e richiami solo su componenti nominati: il sistema ora pratica la regola "un fatto per ogni promessa". |
| 2. Vincoli di posizionamento | 8 | 8 | Nessuna violazione; nominativo marcato come bozza. |
| 3. Efficacia sui tre segmenti | 7 | 8 | Hero con la riga per università e laboratori; totem con il limite di batteria dichiarato; reel leggibile in un secondo. |
| 4. Differenziazione dai competitor | 7 | 7 | Il nuovo logotipo è proprietario, ma il suo linguaggio (cerchi pieni e aste) è lontano dal registro scientifico del resto del sistema e vicino alle soluzioni di B e D. |
| 5. Tenuta nel tempo e oltre Unitree | 8 | 8 | Il richiamo e la colonna delle note restano indipendenti dal robot; il giallo su carta bianca non entra più in conflitto con la segnaletica. |
| 6. Chiarezza della promessa nei testi applicati | 8 | 8 | "Leggi i numeri del robot sul tuo caso prima di firmare l'ordine" passa il test; la nota numerata nel titolo aiuta. |

**Voto complessivo: 7,8** (r1: 7,7)

## Problemi residui

1. **Il marchio parla un'altra lingua rispetto al sistema.** "abra" fatto di dischi pieni e aste, con "ROBOTICS" in mono, è un segno geometrico da studio di design; il sistema intorno è serif scientifico, note, figure. L'idea "ogni lettera è un richiamo" si capisce solo leggendo la didascalia: a colpo d'occhio sono pallini, non annotazioni. A 16 px la favicon è un disco e una barra, leggibile come "a" generica e molto vicina alla favicon di B.
2. **Convergenza con B e D.** Tre direzioni su cinque presentano ora un "abra" minuscolo costruito su occhielli geometrici. Il criterio dell'orchestratore sulla distanza tra direzioni torna a rischio sul marchio, l'elemento che il cliente ricorda.
3. **Il post anonimo resta riconoscibile per chi conosce il settore.** Go2 EDU con LiDAR 4D, tesi in un'azienda manifatturiera, MuJoCo e "quaderno di consegna" insieme bastano; il titolo "un robot che conosce già il tuo stabilimento" rafforza il legame con un cliente preciso.

## Feedback azionabili ancora necessari

1. `logo/`: riporta nel logotipo un elemento del richiamo che si legga come tale, per esempio un filo sottile che unisce i punti o un solo punto staccato dall'asta come nella v1; oggi il punto coincide con l'occhiello e il gesto dell'annotazione sparisce. Verifica il risultato a 24 px.
2. `logo/favicon-16.svg`: aggiungi un segno che la distingua dalla "a" di B (per esempio il filo che esce dal disco verso destra su una riga di pixel), e mostrale affiancate in `logo/test.html`.
3. `applicazioni/linkedin-sacmi-anonimo.html`: togli "4D" e il modello EDU, e generalizza il titolo ("Dai al tuo tesista un robot pronto con mappa, simulatore e codice").
4. `applicazioni/reel-g1.html`: il titolo coincide con B ed E (tabella). Usa il verbo del territorio, che è "leggere" o "citare la fonte": per esempio "Fai rispondere il G1 al tuo pubblico citando le tue schede prodotto".
5. `applicazioni/totem.html`: il titolo è quasi identico a B ed E; porta nel titolo il dettaglio che solo C mostra, la risposta con la fonte approvata.
6. `applicazioni/preventivo-cover.html`: "misura in sei fasi cosa farà il robot" coincide con la copertina di E; lascia "Misura" a E e usa "Leggi" anche qui, coerente con l'hero.

## Headline troppo simili tra direzioni (riguardano C)

| Applicazione | C | Simile a |
|-|-|-|
| Hero | "Leggi i numeri del robot sul tuo caso prima di firmare l'ordine." | B: "...prima di firmare l'ordine." (stessa chiusura) |
| Preventivo, copertina | "Prelievo dei cartoni a fine linea: misura in sei fasi cosa farà il robot, prima di investire" | E: "Misura in sei fasi cosa farà il robot nel tuo reparto." |
| Reel | "Fai parlare il G1 del tuo marchio, con parole approvate da te." | B: "...con le frasi che approvi tu."; E: "...con parole che approvi tu." |
| Totem | "Noleggia il G1 per una giornata, con un tecnico Abra al tuo stand." | B ed E: "...con un tecnico Abra accanto."; D: "...in sala." |
