# Revisione strategica, direzione E, round 1

Revisore: strategia (partner esterno, non coinvolto nella creazione). Data: 27/10/2026.
Materiali aperti: presentazione.html, concept.md, voce.md, logo/test.png, tutti i PNG in applicazioni/ (hero, preventivo copertina e interna, LinkedIn nominativo e anonimo, reel, biglietto, totem, livrea).

## Voti per criterio

| Criterio | Voto | Motivazione |
|-|-|-|
| 1. Coerenza con brief e brand platform | 7 | La corrispondenza misure, imbastitura, prova, modello con P0 a P5 è precisa, e il cartamodello consegnato è una bella traduzione di "ti resta in mano"; ma il lettore non vede la sartoria, vede metro e tratteggi. |
| 2. Vincoli di posizionamento | 7 | Nessuna violazione di posizionamento; il simbolo ricade nel difetto che il brief chiede di correggere: a piccole dimensioni la A torna senza traverso. |
| 3. Efficacia sui tre segmenti | 7 | Manifattura da 8 (pagina delle fasi con il metro come calendario e margine dichiarato), eventi da 7 (totem con pianta dello stand), laboratorio da 6 (il pacchetto è nel post, assente dall'hero). |
| 4. Differenziazione dai competitor | 6 | Tela e metro sono liberi nel settore; giallo e grigio scuro richiamano la segnaletica e le macchine da cantiere, e Bricolage Grotesque condensato nero è un carattere molto usato oggi dalle startup. |
| 5. Tenuta nel tempo e oltre Unitree | 7 | Regola tratteggio/continuo semplice e indipendente dal robot; il riferimento sartoriale, se esplicitato, rischia di invecchiare in fretta o di sembrare moda. |
| 6. Chiarezza della promessa nei testi applicati | 8 | Hero all'imperativo con limiti accanto alle prestazioni; preventivo con "Paghi solo le fasi che approvi" e "Se ti fermi dopo una fase". |

**Voto complessivo: 7,0**

## I 3 problemi più gravi

1. **Il simbolo ripropone la A senza traverso.** Il traverso è un punto d'imbastitura che si vede solo nel controforma: nel logotipo diventa un trattino corto staccato, a 16 e 32 px sparisce e resta una "Λ". Il brief chiede esplicitamente un monogramma che sostituisca la "Λ" attuale; sul biglietto la A attraversata dal tratteggio giallo si legge come una strada con la segnaletica orizzontale.
2. **La metafora resta nel documento di concept.** Misure, imbastitura, prova e modello compaiono solo come etichette minute delle fasi; nelle applicazioni il cliente vede un righello giallo, cartellini e tratteggi. Il territorio wildcard doveva portare una tensione propria (il brief suggeriva la magia del nome contro la misura); qui la tensione è dichiarata e poi spenta.
3. **Codici visivi già occupati fuori dal settore.** Giallo #F2BF2C su flanella, nastro tratteggiato a terra, righello: sono i segni di cantiere, logistica e sicurezza. In un reparto il flight case con la banda gialla si confonde con le delimitazioni HSE del cliente.

## Feedback azionabili

1. `logo/simbolo.svg` e `logo/logotipo-abra.svg`: rendi il punto d'imbastitura continuo dentro il controforma (un punto lungo che tocca le due gambe) e tratteggiato solo fuori dalla lettera; nella favicon a 16 px il traverso deve essere pieno. Verifica in `logo/test.html` che a 16 px si legga una A con traverso.
2. `applicazioni/biglietto.html`: sul fronte riduci il tratteggio a un solo segmento che entra nella A; oggi la linea attraversa tutto il biglietto e richiama la segnaletica stradale.
3. `palette.md` e `applicazioni/livrea.html`: abbassa la saturazione del giallo metro verso un giallo da metro di stoffa (più caldo, meno segnaletico) e vieta le bande gialle continue su casse e robot.
4. `applicazioni/hero.html` e `applicazioni/preventivo-cover.html`: porta la parola del mestiere nel titolo di sezione almeno una volta ("Le misure del tuo reparto", "Il modello che ti resta"), oppure togli la metafora dalla presentazione; oggi chi legge le applicazioni non la ricostruisce.
5. `applicazioni/hero.html`: aggiungi una riga per i laboratori nella fascia delle quattro fasi o sotto la CTA (robot con SDK, ROS 2, simulatore e manuale per i tesisti), per soddisfare il criterio di successo "laboratorio".
6. `tipografia.md`: valuta un peso e una larghezza meno estremi di Bricolage per i titoli lunghi dei documenti (il preventivo a 700 condensato pesa come un cartellone) e mostra una pagina di manuale tecnico con testo corrente.
7. `applicazioni/reel-g1.html`: "come nasce una piastrella in questo stabilimento" porta il settore ceramico nel copy dell'evento e accosta il mockup al cliente reale; usa un prodotto di fantasia lontano dalla ceramica.
8. `applicazioni/linkedin-anonimo.html`: "Go2 con LiDAR per una tesi in azienda", "Manuale tecnico rev. 1.1", "85 ore di assistenza" e "Consegna di ottobre 2026" insieme rendono il cliente riconoscibile; togli revisione e ore di assistenza.
