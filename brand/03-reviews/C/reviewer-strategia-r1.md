# Revisione strategica, direzione C, round 1

Revisore: strategia (partner esterno, non coinvolto nella creazione). Data: 27/10/2026.
Materiali aperti: presentazione.html, concept.md, voce.md, logo/test.png, tutti i PNG in applicazioni/ (hero, preventivo copertina e interna, LinkedIn nominativo e anonimo, reel, biglietto, totem, livrea).

## Voti per criterio

| Criterio | Voto | Motivazione |
|-|-|-|
| 1. Coerenza con brief e brand platform | 8 | Il richiamo con la nota è la forma più diretta di "un fatto verificabile per ogni promessa"; limiti, date e revisioni stanno nella stessa pagina come chiede il nucleo della voce. |
| 2. Vincoli di posizionamento | 8 | Nessun vincolo violato; la nota "se un cobot o una base su ruote fa lo stesso lavoro con meno rischio, lo scriviamo" porta nel preventivo la prova delle raccomandazioni indipendenti. |
| 3. Efficacia sui tre segmenti | 7 | Laboratorio da 9, manifattura da 8 (la pagina delle fasi con simulato e misurato e barre d'incertezza è la migliore delle prove viste), eventi da 6: totem chiaro, registro accademico. |
| 4. Differenziazione dai competitor | 7 | Serif scientifico e carta sono uno spazio libero; il giallo evidenziatore acido è però un tic diffuso nel web di prodotto e il marchio ha poca proprietà formale. |
| 5. Tenuta nel tempo e oltre Unitree | 8 | Il richiamo funziona su qualunque oggetto, grafico o robot; il sistema migliora man mano che Abra produce note e protocolli. |
| 6. Chiarezza della promessa nei testi applicati | 8 | Hero all'imperativo con "prima di investire" evidenziato e la riga "cosa ti resta"; la copertina del preventivo ha una sintesi leggibile in 10 secondi. |

**Voto complessivo: 7,7**

## I 3 problemi più gravi

1. **Il marchio è un carattere tipografico con un dettaglio.** "Abra Robotics" è STIX Two composto; l'unica firma è il punto con il filo nella A, che sotto i 20 px diventa una traversa lunga (lo dice la stessa direzione). Il risultato si confonde con una casa editrice o uno studio legale e protegge poco il nome.
2. **Il giallo evidenziatore porta il registro sbagliato in due punti.** Sul web e nei titoli è efficace; su etichette, richiami adesivi e flight case diventa il giallo dei cartelli di pericolo e si confonde con la segnaletica HSE del cliente. Nei social, insieme a numeri di riga e didascalie, rallenta la lettura (ammesso in autocritica).
3. **Il post anonimo resta riconoscibile.** "Questa settimana consegniamo a un gruppo industriale italiano un Go2 per una tesi in azienda", con manuale rev 1.1 e repository condiviso con due tecnici: chi conosce il settore risale al cliente.

## Feedback azionabili

1. `logo/`: lavora su un logotipo proprietario partendo da STIX Two (spaziatura, legature b r, terminale della s, peso della R) e documenta le modifiche in `sistema-grafico.md`; oggi solo la A è disegnata.
2. `logo/favicon.svg`: disegna una favicon ottica in cui il punto resta visibile a 16 px (punto staccato dal filo, filo più corto), così la storia del richiamo arriva anche nella scheda del browser e sull'adesivo da 40 mm.
3. `applicazioni/livrea.html` e `palette.md`: per tutto ciò che sta su un robot o in un reparto usa la carta come fondo e il giallo solo nel punto del richiamo; vieta le campiture gialle piene sulle attrezzature per non sovrapporsi alla segnaletica di sicurezza.
4. `applicazioni/linkedin-sacmi-anonimo.html`: togli "questa settimana", "rev 1.1" e "due tecnici del cliente"; tieni la figura annotata, che è la parte forte del post.
5. `applicazioni/totem.html`: il totem funziona; aggiungi una nota a margine di una riga con il limite principale della giornata (batteria circa 2 ore, cambio previsto) marcata "Esempio", così anche l'event manager vede la franchezza sui limiti che distingue il sistema.
6. `applicazioni/reel-g1.html`: ottimo il dialogo con la risposta "non è nella mia base di conoscenza"; alleggerisci i timestamp a secondi (14:32) e porta la fonte in un solo richiamo per rendere la copertina leggibile in scorrimento.
7. `voce.md`: aggiungi le headline per l'evento in inglese e una frase di registro per i social brevi (massimo 20 parole, una nota sola), per evitare che ogni post diventi una pagina di paper.
8. `presentazione.html`, sezione 06: "dal preventivo da 40.000 euro" va indicato come importo di esempio.
