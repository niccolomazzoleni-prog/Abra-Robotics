# Autocritica: Cartamodello

## 1. La metafora può sembrare moda o artigianato, lontana dalla fabbrica

**Rischio**: un direttore R&D di una azienda di macchine automatiche vede "sartoria" e pensa a un fornitore di immagine, non a un partner tecnico. In più "sartoriale" è un luogo comune del marketing B2B italiano.

**Cosa ho fatto**: della sartoria ho tenuto solo gli strumenti di misura (metro, gesso, tacche, imbastitura), che sono gli stessi dell'officina; nessun tessuto, manichino o forbice nelle immagini. Le parole del mestiere compaiono solo come etichette accanto al nome tecnico della fase (P2 · L'imbastitura, digital twin e simulazione) e "sartoriale" è vietata in `voce.md`. Il preventivo resta un documento tecnico con tabella, criteri e costi: la metafora sta nella forma dei pezzi, non nel testo. Va verificato con il test dei 5 secondi su hero e copertina del preventivo.

## 2. Il giallo può leggersi come segnaletica di sicurezza, e la palette chiara come poco tecnologica

**Rischio**: giallo e grigio scuro ricordano il nastro di pericolo; la tela avorio può sembrare un'estetica editoriale più che robotica, e avvicinarsi ai territori caldi (B) o di carta (C).

**Cosa ho fatto**: il giallo non si abbina mai al nero e mai a strisce diagonali, resta sotto il 10% della superficie e ha sempre la forma di un metro o di un filo con le tacche. La flanella è grigio blu, non nero. La carta compare solo come "pezzo" con angolo tagliato e tacche, mai come fondo pagina con annotazioni a mano: è questo che la separa dal quaderno di laboratorio. Resta un punto da controllare quando i quattro territori saranno affiancati.

## 3. La A è semplice e il logotipo nasce da un carattere disponibile a tutti

**Rischio**: a 16 px il filo si riduce a tre puntini e la lettera può sembrare una A qualunque; "bra" e "Robotics" derivano da Bricolage Grotesque, che chiunque può scaricare.

**Cosa ho fatto**: la A è disegnata da zero (apice stretto, gambe da 198 unità, filo a 9 gradi con spazio di 24 unità dalle gambe) e non esiste in nessun font. Per le dimensioni piccole ci sono due versioni dedicate: `monogramma.svg` con filo e gambe ingrossati e `favicon-16.svg` disegnato sulla griglia di 16 pixel, su fondo flanella, dove il filo giallo resta leggibile (verificato ingrandito x8 in `logo/test.png`). Il logotipo è convertito in tracciati e spaziato a mano, quindi resta proprietario anche se il carattere di base è libero; il valore distintivo sta nella A e nella regola tratteggio e linea continua che attraversa tutto il sistema. Da fare in una v2: ridisegnare a mano anche "b", "r", "a" per allinearne i terminali all'apice della A, e una ricerca di anteriorità del segno.

## Limiti dei mockup

- I robot sono cutout ufficiali Unitree (segnaposto dichiarato), a bassa risoluzione per il G1: nella hero si vede la differenza con una foto propria. Le prime foto da produrre sono gli scatti 1 e 2 della shot list.
- Codice QR, telefono e numeri dei preventivi sono segnaposto o "Esempio".
