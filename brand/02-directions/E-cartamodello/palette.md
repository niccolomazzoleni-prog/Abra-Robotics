# Palette: Cartamodello (v3)

Nella v3 la palette diventa più solida per chi deve portare un numero all'amministratore delegato: la **flanella** è il colore dominante, i fondi sono neutri (gesso e tela grigio chiaro, niente sabbia), il cartoncino da modello è grigio, i robot sono in grigio neutro. Il **gesso blu** resta il colore firma e ha ora un **Pantone vincolante**.

## Colori

| Nome | Ruolo | HEX | RGB | Pantone | CMYK (Generic CMYK, colorimetrico relativo) | Ritorno, scarto | Uso |
|-|-|-|-|-|-|-|-|
| **Flanella** | Dominante: testo, marchio, fasce e fondi pieni | `#2F3337` | 47, 51, 55 | indicativo 432 C | 81, 72, 63, 40 (nero ricco) | `#2C3336`, dE 1,0 | 40% |
| **Gesso** | Pagine e fondi chiari | `#F7F6F2` | 247, 246, 242 | carta naturale bianca | 2, 2, 3, 0 | `#F7F6F2`, dE 0,0 | 35% |
| **Tela** | Fondo secondario neutro | `#E9E7E1` | 233, 231, 225 | | 7, 6, 7, 0 | `#EAE8E2`, dE 0,4 | 10% |
| **Cartoncino** | Schede numerate con tacche | `#CFCCC3` | 207, 204, 195 | indicativo Cool Gray 2 C | 16, 13, 16, 0 | `#CDCCC4`, dE 1,4 | 7% |
| **Gesso blu** | Colore firma: metro, tacche, cartellini, fascia d'azione | `#8BB8E8` | 139, 184, 232 | **278 C, vincolante** | 41, 18, 1, 0 (solo stampa digitale) | `#8EB1D2`, dE 8,3 | 5% |
| **Blu segno** | Linee "da approvare", etichette Esempio, segni a gesso su chiaro | `#3D5A99` | 61, 90, 153 | **7684 C** | 83, 64, 4, 2 | `#395A94`, dE 3,6 | 2% |
| **Grafite** | Testo secondario, solo su gesso e tela | `#5E6266` | 94, 98, 102 | | 67, 56, 49, 9 | `#5C6367`, dE 1,1 | 1% |

### Regola di stampa del gesso blu (vincolante)

Il gesso blu è fuori dal gamut di quadricromia: in CMYK torna più grigio (dE 8,3). Su **marchio, totem, flight case, adesivi, cartellini e righello del biglietto** si stampa **solo in Pantone 278 C** (tinta piatta, o la corrispondente pellicola o vernice). La conversione CMYK è ammessa solo per documenti stampati in digitale, come i preventivi in ufficio. Prima della prima produzione serve una prova colore su forex e su carta naturale. Il valore HEX corrisponde al riferimento pubblicato per il 278 C; va confermato sulla mazzetta Pantone Formula Guide in vigore.

## Rapporti d'uso

- I documenti per l'azienda (preventivo, manuale) hanno una fascia di testa in flanella piena e pagine in gesso; le schede sono in cartoncino grigio.
- Il gesso blu compare solo dove c'è qualcosa da misurare o da segnare: metro, tacche, cartellini, fascia "passo successivo". Mai testo su fondo chiaro.
- Su cartoncino il testo è sempre flanella.
- Su flanella il testo è gesso o gesso blu; grafite su flanella è vietata.
- I robot sono in scala di grigi, in moltiplica sul cartoncino o sulla tela: escono grigio neutro, senza viraggio seppia.

## Contrasti WCAG 2.1

| Testo | Fondo | Rapporto | Esito |
|-|-|-|-|
| Flanella `#2F3337` | Gesso `#F7F6F2` | 11,77:1 | AAA |
| Flanella `#2F3337` | Tela `#E9E7E1` | 10,30:1 | AAA |
| Flanella `#2F3337` | Cartoncino `#CFCCC3` | 7,93:1 | AAA |
| Flanella `#2F3337` | Gesso blu `#8BB8E8` | 6,13:1 | AA |
| Gesso `#F7F6F2` | Flanella `#2F3337` | 11,77:1 | AAA |
| Gesso blu `#8BB8E8` | Flanella `#2F3337` | 6,13:1 | AA |
| Cartoncino `#CFCCC3` | Flanella `#2F3337` | 7,93:1 | AAA |
| Blu segno `#3D5A99` | Gesso `#F7F6F2` | 6,22:1 | AA |
| Blu segno `#3D5A99` | Tela `#E9E7E1` | 5,44:1 | AA |
| Gesso `#F7F6F2` | Blu segno `#3D5A99` | 6,22:1 | AA |
| Grafite `#5E6266` | Gesso `#F7F6F2` | 5,69:1 | AA |
| Grafite `#5E6266` | Tela `#E9E7E1` | 4,97:1 | AA |
| Blu segno `#3D5A99` | Cartoncino `#CFCCC3` | 4,19:1 | Solo elementi grafici e testo grande |
| Grafite `#5E6266` | Cartoncino `#CFCCC3` | 3,83:1 | Solo elementi grafici e testo grande |
| Grafite `#5E6266` | Flanella `#2F3337` | 2,07:1 | Vietato |
| Gesso blu `#8BB8E8` | Gesso `#F7F6F2` | 1,92:1 | Vietato per testo e linee sottili |

Tutte le coppie testo e fondo usate nelle applicazioni v3 sono AA o superiori, comprese le didascalie delle tavole, ora su tela o gesso.

## Distanza

- Dalle altre direzioni: A verde di misura con alluminio, C giallo evidenziatore con inchiostro. Nessuna usa blu.
- Dal settore: il 278 C è un blu chiaro e polveroso, lontano dal blu elettrico di Unitree e AgiBot, dal cobalto di Eagleprojects e dal blu Comau. Il 7684 C compare solo come linea sottile.
