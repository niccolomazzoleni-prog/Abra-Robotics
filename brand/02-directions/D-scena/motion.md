# Motion: tre cue e un dimmer

In teatro ogni cambiamento in scena è un cue: ha un numero, una durata e un ordine. Il movimento di Abra segue la stessa logica: ogni animazione è un cue che porta un elemento in scena e poi si ferma.

## Principi

1. **Prima la luce, poi l'interprete.** In ogni sequenza il palco si accende prima che arrivi il contenuto: il trapezio Luce appare, poi entra il titolo o il robot.
2. **Il dimmer del tungsteno.** Quando una lampada a incandescenza sale con il dimmer passa dal rosso scuro al giallo caldo. Le campiture Luce entrano con questa stessa curva di colore (`#4A1A0C`, `#8E3A14`, `#D58C2F`, `#E9AE45`), senza alone e senza dissolvenze morbide sui bordi.
3. **Entrate dal basso o dalle quinte.** Gli elementi entrano come in scena: salgono da sotto il palco (la botola) o scorrono dalle quinte laterali, dentro una maschera con bordo netto.
4. **Ritmo contato.** Durate brevi e ripetibili, sempre multipli di 0,1 s; tra un cue e il successivo c'è una pausa visibile.
5. **Fermo finale.** Ogni animazione finisce su una composizione statica che regge da sola come immagine.

## Tempi e curve

| Cue | Durata | Curva | Uso |
|-|-|-|-|
| Luce (dimmer) | 0,9 s | `cubic-bezier(.45,0,.2,1)` | Accensione del palco, delle barre dei grafici |
| Entrata dalla botola | 0,8 s | `cubic-bezier(.2,.8,.2,1)` | Simbolo, titoli, robot |
| Apertura | 0,7 s | `cubic-bezier(.6,0,.2,1)` | Testo che si apre da sinistra come una quinta |
| Cambio scena | 0,4 s | taglio netto | Passaggio tra slide o tra piani video con un taglio netto |
| Pausa tra cue | 0,1 a 0,3 s | | |

## Il logo animato

File: `logo/animazione.html` (CSS e SVG, nessuna libreria).

1. Cue 1, 0,1 s: si accende il taglio di luce sul fondale.
2. Cue 1, 0,35 s: il pavimento della A sale con il dimmer, dal rosso al color Luce.
3. Cue 2, 0,75 s: la A sale dalla botola e si ferma sul palco acceso.
4. Cue 3, 1,35 s: "bra" si apre da sinistra come una quinta; a 1,9 s sale "Robotics".
Durata totale 2,5 s. Con `prefers-reduced-motion` la sequenza mostra direttamente il fermo finale.

## Applicazioni

- **Sito**: la hero accende il palco e la scaletta delle fasi al caricamento, una sola volta. Le barre dei grafici di misura salgono con il dimmer quando entrano nello schermo; la barra che supera il criterio passa in Luce per ultima.
- **Reel e video**: apertura con il palco vuoto e il segno a terra (1 s), entrata del robot, titolo in sovrimpressione con cue di apertura. Chiusura sul logo animato.
- **Presentazioni**: cambio di slide con taglio netto; dentro la slide al massimo due cue.
- **Totem digitale (se schermo)**: ciclo di 12 s con tre cue: palco acceso, titolo, "Chiedi una data".

## Da evitare

Rimbalzi elastici, particelle, scie, glitch, rotazioni 3D del logo, effetti di luce che pulsa, dissolvenze lunghe, testi che scrivono lettera per lettera come un terminale.
