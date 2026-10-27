# Palette: Cartamodello

I colori vengono dal tavolo del modellista: la tela grezza su cui si prova, la flanella grigia, il giallo del metro da sarta, la carta da modello, il gesso. Nessun colore dipende dal robot fotografato.

## Primari

| Nome | Ruolo | HEX | RGB | CMYK indicativo | Uso |
|-|-|-|-|-|-|
| **Tela** | Fondo principale | `#ECE6D8` | 236, 230, 216 | 0, 3, 8, 7 | 55% |
| **Flanella** | Testo, marchio, fondi scuri (eventi, social, casse) | `#2F3337` | 47, 51, 55 | 15, 7, 0, 78 | 25% |
| **Giallo metro** | Il segnale: metro, filo, fascia d'azione | `#F2BF2C` | 242, 191, 44 | 0, 21, 82, 5 | 7% |

## Secondari

| Nome | Ruolo | HEX | RGB | CMYK indicativo | Uso |
|-|-|-|-|-|-|
| **Carta modello** | Pezzi di cartamodello, schede, riquadri dei limiti | `#D9CBAA` | 217, 203, 170 | 0, 6, 22, 15 | 8% |
| **Gesso** | Pagine interne dei documenti, testo su flanella, segni a gesso | `#FAF8F3` | 250, 248, 243 | 0, 1, 3, 2 | 3% |
| **Grafite** | Testo secondario, didascalie | `#62666A` | 98, 102, 106 | 8, 4, 0, 58 | 1,5% |
| **Blu gesso** | Seconda serie nei grafici, mai come colore di marca | `#48667F` | 72, 102, 127 | 43, 20, 0, 50 | 0,5% |

Per la stampa: tela e carta modello si ottengono anche stampando su carta naturale avoriata (tipo Fedrigoni Materica o Arena Natural) con il solo nero flanella e il giallo; il giallo in Pantone indicativo è vicino al 123 C, la flanella al 432 C. I valori Pantone vanno verificati con prova colore.

## Rapporti d'uso

- Il giallo non è mai testo su fondo chiaro e non supera il 10% di una superficie. È il metro, il filo e la fascia "passo successivo" (totem, cartellini).
- La flanella come fondo pieno vale per eventi, social, flight case, biglietto (fronte). Documenti, sito e preventivi restano su tela e gesso.
- La carta modello è sempre un "pezzo": un riquadro con tacche e margine tratteggiato, mai un fondo pagina intero.
- Il blu gesso entra solo nei grafici, come seconda serie accanto alla flanella.

## Contrasti WCAG 2.1 (calcolati con la formula di luminanza relativa)

| Testo | Fondo | Rapporto | Esito |
|-|-|-|-|
| Flanella `#2F3337` | Tela `#ECE6D8` | 10,23:1 | AAA |
| Flanella `#2F3337` | Gesso `#FAF8F3` | 11,99:1 | AAA |
| Flanella `#2F3337` | Carta modello `#D9CBAA` | 7,93:1 | AAA |
| Flanella `#2F3337` | Giallo metro `#F2BF2C` | 7,43:1 | AAA |
| Gesso `#FAF8F3` | Flanella `#2F3337` | 11,99:1 | AAA |
| Tela `#ECE6D8` | Flanella `#2F3337` | 10,23:1 | AAA |
| Giallo metro `#F2BF2C` | Flanella `#2F3337` | 7,43:1 | AAA |
| Carta modello `#D9CBAA` | Flanella `#2F3337` | 7,93:1 | AAA |
| Grafite `#62666A` | Tela `#ECE6D8` | 4,65:1 | AA |
| Grafite `#62666A` | Gesso `#FAF8F3` | 5,45:1 | AA |
| Grafite `#62666A` | Carta modello `#D9CBAA` | 3,60:1 | AA solo testo grande (da 18,7 px in grassetto) |
| Blu gesso `#48667F` | Tela `#ECE6D8` | 4,85:1 | AA |
| Blu gesso `#48667F` | Gesso `#FAF8F3` | 5,68:1 | AA |
| Gesso `#FAF8F3` | Blu gesso `#48667F` | 5,68:1 | AA |
| Giallo metro `#F2BF2C` | Tela `#ECE6D8` | 1,38:1 | Vietato per testo e per il marchio |

## Distanza dai vicini

Blu elettrico (Unitree, AgiBot), cobalto (Eagleprojects, Comau), viola (vecchio sito Abra), arancio e salmone (Apptronik, PAL, Generation Robots), rosso su antracite (ANYbotics), teal (Oversonic), verde (Reply, MYBOTSHOP) e grigio caldo con mono tecnico (Agility) restano fuori. Il giallo pieno non è usato da nessuno dei siti rilevati; lo abbiniamo alla flanella e alla tela, mai al nero, per non leggerlo come segnaletica di pericolo.
