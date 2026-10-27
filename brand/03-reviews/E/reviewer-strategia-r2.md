# Revisione strategica, direzione E, round 2

Revisore: strategia. Data: 28/10/2026.
Materiali aperti: changelog.md, round1-sintesi.md, presentazione.html, logo/test.png, PNG v2 di hero, preventivo copertina, totem, reel, post LinkedIn anonimo; titoli di tutte le applicazioni HTML. Colore firma (gesso da sarto blu) assunto come vincolo, non valutato.

## Voti per criterio

| Criterio | r1 | r2 | Motivazione r2 |
|-|-|-|-|
| 1. Coerenza con brief e brand platform | 7 | 7 | Metro sempre vero e regola "in gesso / cucito" chiara; la metafora del cartamodello resta però invisibile al cliente, come voluto, e il marchio non la porta. |
| 2. Vincoli di posizionamento | 7 | 7 | Traversa sempre visibile, nessuna "Λ"; il simbolo resta una A maiuscola isolata, il campo che la sintesi indica come il più affollato nei registri. |
| 3. Efficacia sui tre segmenti | 7 | 8 | Riga per i laboratori nell'hero, preventivo leggibile con fasi in scala, totem con pianta dello stand in scala vera: l'event manager vede dove sta il robot e dove sta il pubblico. |
| 4. Differenziazione dai competitor | 6 | 7 | Uscito dal giallo e dal tratteggio da cantiere; tela, gesso blu e metro sono uno spazio libero nel settore. |
| 5. Tenuta nel tempo e oltre Unitree | 7 | 7 | Il metro misura qualunque robot; il simbolo A con il filo è debole come asset a lungo termine. |
| 6. Chiarezza della promessa nei testi applicati | 8 | 8 | "Misura cosa farà il robot nel tuo reparto prima di comprarlo" è la headline più diretta delle cinque. |

**Voto complessivo: 7,3** (r1: 7,0)

## Problemi residui

1. **Il simbolo è ancora una A generica.** La traversa inclinata e il filo corto che esce a destra si vedono in grande; a 16 e 24 px il filo diventa un puntino e resta una A maiuscola in un quadrato scuro, uguale a molte altre nei registri e nelle schede del browser. La sintesi chiedeva un segno riconoscibile a 16 px in monocromia: il test mostra il contrario.
2. **La metafora non lascia traccia nel marchio né nel copy.** Tolti "imbastitura" e tratteggio (correttamente), il cartamodello sopravvive solo nella forma dei pannelli con l'angolo tagliato e nel metro. Il territorio wildcard rischia di diventare una variante di A (misura, righello, scheda limiti) con un'altra palette.
3. **Headline condivise**: il totem è identico a B, il reel coincide con B e C, la copertina del preventivo con C, il post LinkedIn con A e D (tabella in fondo).

## Feedback azionabili ancora necessari

1. `logo/simbolo.svg` e `logo/favicon-16.svg`: lavora sulla legatura "Ab" o sull'intera parola, come suggerito nella sintesi, oppure rendi il filo il tratto dominante a 16 px (due righe di pixel che attraversano tutta la lettera e ne escono a destra). Mostra il risultato accanto a una A generica in `logo/test.html`.
2. `sistema-grafico.md`: scegli un gesto del mestiere che il cliente veda senza spiegazione e usalo in tre punti fissi (copertina del preventivo, totem, livrea): per esempio la tacca a V sul bordo dei pannelli usata come segno di fase superata. Oggi l'angolo tagliato è l'unico residuo e si legge come decorazione.
3. `applicazioni/totem.html`: il titolo è identico a quello di B. Usa la pianta dello stand, che è il punto forte di E: "Segna sul pavimento dove lavora il G1 e noi lo portiamo con un tecnico, per una giornata" o una formula equivalente.
4. `applicazioni/reel-g1.html`: titolo da riscrivere per staccarsi da B e C (tabella), con il dettaglio misurabile che solo E mostra (durata del copione, numero di schede approvate).
5. `applicazioni/linkedin-anonimo.html`: "Tesi in azienda" come titolo di cartellino, più quadrupede con LiDAR e MuJoCo, resta il dettaglio che porta al cliente; tienilo solo nel testo.
6. `applicazioni/hero.html`: "circa 35 kg" è dato del produttore e non è marcato; va bene, ma indica la fonte ("dato del produttore") per coerenza con la regola dei limiti marcati "Esempio".

## Headline troppo simili tra direzioni (riguardano E)

| Applicazione | E | Simile a |
|-|-|-|
| Totem | "Noleggia il G1 per una giornata, con un tecnico Abra accanto." | B: identico; C: "...al tuo stand."; D: "...in sala." |
| Reel | "Fai parlare un umanoide del tuo marchio, con parole che approvi tu." | B: "Fai parlare il G1 del tuo marchio, con le frasi che approvi tu."; C: "...con parole approvate da te." |
| Preventivo, copertina | "Misura in sei fasi cosa farà il robot nel tuo reparto." | C: "...misura in sei fasi cosa farà il robot, prima di investire" |
| LinkedIn | "Fai partire una tesi sul robot dal primo giorno." | A: "Fai lavorare il tuo team sul robot dal primo giorno..."; D: "Fai lavorare il tesista sul robot dal primo giorno." |

Proposta di ripartizione: "Misura" resta a E (hero e preventivo), C passa a "Leggi" anche nel preventivo.
