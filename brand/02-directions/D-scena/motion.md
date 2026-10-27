# Motion v2: la gelatina, poi i portali

In teatro ogni cambiamento in scena è un cue: ha un numero, una durata e un ordine. Il movimento di Abra segue la stessa logica: ogni animazione è un cue che porta un elemento in scena e poi si ferma.

## Principi

1. **Prima il colore, poi l'interprete.** Nei formati di scena la campitura magenta sale come una gelatina inserita nel proiettore (una tendina dal basso, bordo netto), poi entrano il titolo o il robot.
2. **Uno alla volta.** I quattro portali del logotipo entrano in sequenza, a 0,15 s l'uno dall'altro, come interpreti che prendono posizione.
3. **Da a a b.** Sulla pianta dei movimenti il percorso si disegna dalla posizione "a" alla posizione "b"; le fasi si accendono in ordine, quelle da decidere restano vuote.
4. **Ritmo contato.** Durate in multipli di 0,05 s, pause visibili tra un cue e il successivo.
5. **Fermo finale.** Ogni animazione finisce su una composizione statica che regge da sola.
6. **Registro documento**: nel sito e nei PDF interattivi solo il percorso delle fasi che si disegna una volta; niente campiture in movimento.

## Tempi e curve

| Cue | Durata | Curva | Uso |
|-|-|-|-|
| Gelatina | 0,7 s | `cubic-bezier(.6,0,.2,1)` | Campitura magenta nei formati di scena |
| Entrata di un portale | 0,45 s | `cubic-bezier(.2,.8,.2,1)` | Lettere del logotipo, titoli, robot |
| Percorso da a a b | 0,8 s | `cubic-bezier(.45,0,.2,1)` | Pianta delle fasi, percorso del robot |
| Cambio scena | taglio netto | | Passaggio tra slide o tra piani video |

## Il logo animato

File: `logo/animazione.html` (CSS e SVG, nessuna libreria).
1. Cue 1, da 0,15 s: la gelatina magenta sale dal basso sul fondo Grafite.
2. Cue 2, da 0,9 s: entrano "a", "b", "r", "a", una ogni 0,15 s, salendo di 40 px.
3. Cue 3, a 1,8 s: compare il descrittore "ROBOTICS".
Durata totale 2,3 s. Con `prefers-reduced-motion` si vede subito il fermo finale.

## Applicazioni

- **Sito**: il percorso delle fasi P0 a P5 si disegna da sinistra al primo caricamento; nient'altro si muove.
- **Reel e video**: apertura sui dischi a e b nel pavimento vuoto (1 s), entrata del robot, titolo in Condensed con cue di entrata, chiusura sul logo animato.
- **Totem digitale**: ciclo di 12 s con tre cue: gelatina, titolo, "Chiedi una data" con il QR.

## Da evitare

Rimbalzi elastici, particelle, scie, glitch, rotazioni 3D, luci che pulsano, aloni, dissolvenze lunghe, testi che si scrivono lettera per lettera come un terminale.
