# Fotografia e video: fotografare la prova

Un robot Abra si fotografa come si documenta una prova generale: con la luce del posto o con una luce di scena vera, con le persone che lavorano intorno, con il segno a terra sotto i piedi. La scena è sempre un luogo reale (laboratorio, reparto, stand, sala); il robot è un interprete al lavoro, mai una scultura isolata nel vuoto.

## Principi

1. **Luce vera, una sorgente leggibile.** In reparto la luce del reparto (neon, finestre a shed). Agli eventi un sagomatore o una luce frontale calda, a 3.200 K, che disegna una zona di palco con bordi netti. Si vede da dove arriva la luce.
2. **Scala.** Almeno uno scatto per servizio mostra il robot intero con una persona accanto e lo spazio intorno: l'altezza del G1 (132 cm) accanto a un adulto, il Go2 tra gli scaffali.
3. **Taglio.** Inquadrature frontali o a tre quarti, ad altezza del robot. Il taglio stretto si usa per le mani al lavoro e per i segni a terra, e deve lasciare capire dove siamo.
4. **Persone al lavoro.** Tecnici Abra, tesisti, operatori del cliente: mani, strumenti, laptop con il simulatore aperto, il tecnico in sala durante l'evento. Solo persone che hanno firmato la liberatoria.
5. **Il segno a terra.** Prima di ogni ripresa si posa la T di nastro color Luce dove sta il robot. È la firma di Abra nelle foto proprie.

## Inquadrature

| Nome | Descrizione | Uso |
|-|-|-|
| Platea | Campo largo frontale, robot al centro del palco o della postazione, persone in primo piano di spalle | Hero, totem, LinkedIn |
| Quinta | Tre quarti dal lato, il tecnico in primo piano sfocato, il robot a fuoco | Pagine di servizio, post |
| Pianta | Dall'alto, robot e segno a terra, cavi e strumenti visibili | Manuale, preventivo, sezione metodo |
| Mani | Dettaglio della presa o del pezzo, con il riferimento di misura (righello, bilancia, cronometro) | Prove, limiti dichiarati |
| Schermo | Il simulatore MuJoCo o il digital twin sullo schermo, con il robot vero sfocato dietro | Digital twin, laboratorio |

## Ambienti

Laboratorio Abra (quando avrà un indirizzo fisso), reparti italiani di packaging, ceramica e automotive, laboratori universitari, stand fieristici, sale congressi e luoghi storici per gli eventi. Sempre con i segni del lavoro: nastro a terra, cartelli di sicurezza, carrelli, flight case aperti.

## Post produzione: il trattamento tungsteno

- Bilanciamento caldo (3.200 a 3.600 K) e neri chiusi verso Buio `#211412`, mai neri puri.
- Saturazione ridotta del 20%. I LED blu del robot (visore del G1) si desaturano fino a diventare grigio caldo.
- Per le immagini dei produttori usate come segnaposto: conversione in bicromia con mappa Buio, `#7A4A32`, `#DEBE8C`, `#FAF0DE` (script in `_lavoro`, risultato in `applicazioni/img/*-tungsteno.png`). Il segnaposto è sempre dichiarato in didascalia.
- Il ritocco si limita a colore e pulizia: cieli sostituiti, riflessi aggiunti e scie di movimento sono esclusi.

## Video

- Riprese su treppiede o slider lento, durata dei piani 3 a 6 secondi, tagli a tempo di musica solo nei reel.
- Audio presa diretta quando il robot parla: si sente la sala.
- Ogni video di evento si apre con il palco vuoto e il segno a terra, poi entra il robot (la stessa sequenza del logo animato).
- Sottotitoli sempre, composti in Testo su fascia Velluto.

## Cosa evitare

Robot su fondo nero con luce radente, cielo stellato o pianeti, piste e scie di luce, bagliori intorno ai sensori, inquadrature dal basso eroiche, robot che balla o fa acrobazie, mani robotiche che toccano mani umane, il robot da solo su fondo grigio da catalogo, sguardo in macchina con occhi illuminati, persone prese da banche immagini.

## Shot list per la prima sessione (8 scatti)

1. **Consegna, platea.** Il Go2 sul suo segno a terra nel reparto del cliente (o in laboratorio per la versione anonima), il tecnico Abra e il tesista accanto, flight case aperto in primo piano.
2. **Pianta della consegna.** Dall'alto: Go2, segno a terra, laptop con la mappa LiDAR aperta, manuale rev 1.1 stampato.
3. **Schermo.** Simulatore MuJoCo sullo schermo, il Go2 vero sfocato dietro, nella stessa posa.
4. **Mani.** Il tecnico che configura lo SLAM dal laptop, mani e cavo Ethernet a fuoco.
5. **G1 in sala, platea.** Il G1 su una pedana con sagomatore caldo, tre persone di spalle che lo ascoltano, il tecnico Abra in quinta.
6. **G1, quinta.** Tre quarti dal lato del tecnico: il tablet con il copione approvato a fuoco, il G1 sfocato.
7. **Prova di presa, mani.** Mano del G1 con un pezzo del cliente sulla bilancia, cronometro in campo: lo scatto che accompagna i limiti dichiarati.
8. **Flight case.** Il case G1 · 01 chiuso sul carrello, livrea in vista, nel corridoio di servizio di una fiera.

## Prompt per immagini di mood (da non generare ora: crediti esauriti)

1. *Documentary photograph, Italian packaging factory floor, a small grey quadruped robot standing on a yellow floor-tape T mark, an engineer kneeling with a laptop showing a 3D map, fluorescent factory light, warm white balance, 35 mm lens at robot height, muted colours, no logos, realistic, no glow.*
2. *Wide shot of a conference hall in an Italian historic building, a 1.3 m humanoid robot on a low wooden stage lit by a single warm profile spotlight with hard edges, audience seen from behind, technician standing at the side holding a tablet, tungsten light 3200 K, deep red velvet seats, no blue light, no smoke.*
3. *Top-down photograph of a workbench: quadruped robot, printed technical manual with ring binding, laptop showing a physics simulation, roll of amber floor tape, cables, warm daylight, editorial still life, no logos.*
4. *Close-up of a humanoid robot hand holding a glass jar above a digital scale, a stopwatch beside it, laboratory with plain walls, warm side light from a window, shallow depth of field, factual mood.*
5. *Trade fair aisle at night before opening, a black aluminium flight case with an amber band on a trolley, work lights, empty stand behind, warm practical lighting, documentary style.*
6. *University robotics lab, two students and a researcher around a quadruped robot on the floor, one student pointing at a monitor with code, natural light, candid moment, no posing, warm colour grading.*
