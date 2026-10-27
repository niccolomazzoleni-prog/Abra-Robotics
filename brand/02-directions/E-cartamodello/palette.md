# Palette: Cartamodello (v2)

I colori vengono dal tavolo del modellista: la tela grezza su cui si prova, la flanella grigia, la carta da modello e il **gesso da sarto blu**, che è il colore firma della direzione. Il giallo della v1 è eliminato (sintesi del round 1: il giallo e l'ocra erano in tutte e cinque le direzioni, e su flanella si leggeva come segnaletica stradale).

## Il colore firma: gesso da sarto

Il gesso da sarto blu è il segno che si fa sulla stoffa prima di tagliare: si vede bene, si cancella con la spazzola, nessuno lo scambia per un segnale di pericolo. Lo usiamo in due tinte, come il sarto usa il gesso chiaro sul panno scuro e quello scuro sulla tela chiara.

| Nome | Ruolo | HEX | RGB | CMYK (Generic CMYK, intento colorimetrico relativo) | Ritorno in RGB, scarto | Uso |
|-|-|-|-|-|-|-|
| **Gesso blu** | Colore firma: metro, filo del simbolo, fascia d'azione, segni su flanella | `#8FB0E0` | 143, 176, 224 | 40, 22, 1, 0 | `#8FABCD`, dE 7,3 (fuori gamut) | 7% |
| **Blu segno** | Il gesso su fondo chiaro: bordi "da approvare", etichette Esempio, segni a gesso, link | `#2F5D9E` | 47, 93, 158 | 86, 61, 3, 2 | `#2E5C96`, dE 4,5 | 3% |

Il Gesso blu esce dal gamut di quadricromia: per stampe di marchio e casse usare un **Pantone indicativo 2717 C o 658 C**, per la stampa digitale il valore CMYK sopra. Il Blu segno è vicino al **Pantone 7684 C**. I Pantone vanno confermati su mazzetta prima della prima stampa.

## Colori di base

| Nome | Ruolo | HEX | RGB | CMYK (Generic CMYK) | Ritorno, scarto | Uso |
|-|-|-|-|-|-|-|
| **Tela** | Fondo principale | `#ECE6D8` | 236, 230, 216 | 6, 6, 11, 0 | `#EBE7D8`, dE 0,4 | 52% |
| **Flanella** | Testo, marchio, fondi scuri | `#2F3337` | 47, 51, 55 | 81, 72, 63, 40 (nero ricco) | `#2C3336`, dE 1,0 | 28% |
| **Carta modello** | Schede e pezzi di carta | `#D9CBAA` | 217, 203, 170 | 13, 15, 31, 0 | `#D8CCAB`, dE 1,0 | 6% |
| **Gesso** | Pagine interne, testo su flanella | `#FAF8F3` | 250, 248, 243 | 2, 2, 4, 0 | `#F9F7F2`, dE 0,4 | 3% |
| **Grafite** | Testo secondario, solo su fondi chiari | `#62666A` | 98, 102, 106 | 65, 55, 47, 7 | `#60676B`, dE 1,0 | 1% |

Conversioni calcolate con Pillow ImageCms, profilo `Generic CMYK Profile.icc` di macOS, intento colorimetrico relativo; per la tipografia offset chiedere allo stampatore il profilo FOGRA39 e ricalcolare. La Flanella è un nero ricco a quattro colori: nel testo sotto 9 pt usare il solo nero 100% per evitare problemi di registro.

## Rapporti d'uso

- Il Gesso blu non è mai testo su fondo chiaro e non supera il 10% di una superficie. Compare dove c'è qualcosa da misurare (il metro), sul filo del simbolo e nella fascia "passo successivo".
- Il Blu segno è la linea sottile: il bordo di una fase da approvare, il segno a gesso sul pavimento, l'etichetta Esempio su tela e gesso.
- Su Carta modello il testo è sempre Flanella (Blu segno e Grafite lì scendono sotto AA per il testo piccolo).
- Su Flanella il testo è Gesso o Gesso blu; Grafite su Flanella è vietata (2,20:1).

## Contrasti WCAG 2.1 (formula della luminanza relativa)

| Testo | Fondo | Rapporto | Esito |
|-|-|-|-|
| Flanella `#2F3337` | Tela `#ECE6D8` | 10,23:1 | AAA |
| Flanella `#2F3337` | Gesso `#FAF8F3` | 11,99:1 | AAA |
| Flanella `#2F3337` | Carta modello `#D9CBAA` | 7,93:1 | AAA |
| Flanella `#2F3337` | Gesso blu `#8FB0E0` | 5,73:1 | AA |
| Gesso `#FAF8F3` | Flanella `#2F3337` | 11,99:1 | AAA |
| Tela `#ECE6D8` | Flanella `#2F3337` | 10,23:1 | AAA |
| Gesso blu `#8FB0E0` | Flanella `#2F3337` | 5,73:1 | AA |
| Carta modello `#D9CBAA` | Flanella `#2F3337` | 7,93:1 | AAA |
| Blu segno `#2F5D9E` | Tela `#ECE6D8` | 5,31:1 | AA |
| Blu segno `#2F5D9E` | Gesso `#FAF8F3` | 6,22:1 | AA |
| Gesso `#FAF8F3` | Blu segno `#2F5D9E` | 6,22:1 | AA |
| Grafite `#62666A` | Tela `#ECE6D8` | 4,65:1 | AA |
| Grafite `#62666A` | Gesso `#FAF8F3` | 5,45:1 | AA |
| Blu segno `#2F5D9E` | Carta modello `#D9CBAA` | 4,11:1 | Solo elementi grafici e testo grande |
| Grafite `#62666A` | Carta modello `#D9CBAA` | 3,60:1 | Solo elementi grafici e testo grande |
| Grafite `#62666A` | Flanella `#2F3337` | 2,20:1 | Vietato |
| Gesso blu `#8FB0E0` | Tela `#ECE6D8` | 1,79:1 | Vietato per testo e linee sottili |

Nelle applicazioni v2 tutte le coppie testo e fondo usate sono AA o superiori.

## Distanza dai vicini

- Dalle altre direzioni: A verde di misura e grigio alluminio; B rosso e ocra; C giallo evidenziatore e inchiostro; D colore di gelatina teatrale. Nessuna usa un blu polvere.
- Dal settore: il Gesso blu è chiaro e polveroso, lontano dal blu elettrico di Unitree e AgiBot, dal cobalto di Eagleprojects e dal blu Comau, che sono saturi e scuri. Il Blu segno compare solo come linea sottile, mai come campo pieno, per non avvicinarsi ai blu corporate.
