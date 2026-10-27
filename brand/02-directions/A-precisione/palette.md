# Palette · In squadra (v2)

Colore firma esclusivo della direzione: **verde di misura RAL 6024 con grigio alluminio**. Il verde viene dalla norma sulle macchine (IEC 60204-1: verde per lo stato normale) e in Abra ha due ruoli: nelle schede segna il criterio misurato e superato, nei formati di comunicazione è il campo pieno che si riconosce da lontano (copertina del preventivo, testata del post, totem, biglietto, monogramma). Nessun giallo, nessun ocra, nessun blu, nessun rosso. Il limite dichiarato non ha un colore: è un tratteggio grafite.

## Colori

CMYK ricalcolati con il profilo Generic CMYK di macOS, intento colorimetrico relativo; per la stampa vera vanno rifatti dal tipografo con FOGRA39 (patinata) o FOGRA29 (uso mano). I Pantone sono indicativi, da verificare sulla mazzetta.

### Primari

| Nome | HEX | RGB | CMYK (profilo) | Riferimento | Uso |
|-|-|-|-|-|-|
| Verde di misura | `#008351` | 0, 131, 81 | 85 13 82 14 | RAL 6024 per vinili e vernici; Pantone 348 C indicativo | colore firma: campi pieni, monogramma, celle "misurato", pulsante principale |
| Alluminio | `#E3E7E9` | 227, 231, 233 | 9 5 4 0 | Pantone Cool Gray 1 C indicativo | fondo base di sito, post, pannelli |
| Grafite | `#1A2125` | 26, 33, 37 | 83 71 61 62 | Pantone Black 7 C indicativo | testo, logotipo, flight case |

### Secondari

| Nome | HEX | RGB | CMYK (profilo) | Uso |
|-|-|-|-|-|
| Verde profondo | `#0F3A2C` | 15, 58, 44 | 84 37 71 59 | fondo scuro dei formati social ed eventi, al posto del nero |
| Bianco disegno | `#F6F8F8` | 246, 248, 248 | 3 2 2 0 | fondo dei documenti, delle tavole e delle targhe |
| Grigio quota | `#5C676D` | 92, 103, 109 | 68 52 45 8 | etichette e quote, **solo su fondi chiari** |
| Acciaio | `#8A959B` | 138, 149, 155 | 46 32 27 1 | etichette su grafite, sagome grafiche, angolari |
| Linea | `#B4BDC2` | 180, 189, 194 | 27 17 14 0 | filetti e sagome, mai testo |

Tutti i colori rientrano nella gamma CMYK con scarto di ritorno dE76 tra 0 e 2. Tolto dalla v1: il verde chiaro `#3DBB82`, fuori gamma (dE 7,8).

### Il limite dichiarato

Tratteggio a 135 gradi, linee grafite da 1 px (0,25 mm in stampa) su passo 4 o 5 px, dentro un riquadro con filetto da 1,5 px. Si usa come quadratino accanto al valore o come cella del riquadro di controllo. In CSS: `repeating-linear-gradient(135deg, #1A2125 0 1px, transparent 1px 5px)`.

## Rapporti d'uso

| Colore | Quota | Note |
|-|-|-|
| Alluminio e Bianco disegno | 50 % | i fondi |
| Verde di misura | 22 % | campi pieni nei formati di comunicazione, segnali nei documenti |
| Grafite e Verde profondo | 20 % | testo, testate scure, eventi |
| Neutri di servizio | 8 % | quote, etichette, filetti, sagome |

Regole:
- Il logotipo è sempre monocromatico: grafite su chiaro, bianco su verde, grafite o verde profondo.
- Su verde il testo è bianco puro `#FFFFFF` (4,81 : 1); mai grafite su verde (3,39 : 1).
- Il verde nelle schede tecniche compare solo dove c'è una misura fatta; nei campi pieni non porta significato di stato.
- Le fotografie e i segnaposto robot vanno in bianco e nero o desaturati.

## Contrasti WCAG 2.2

Calcolati con la luminanza relativa WCAG 2.2 (1.4.3) e ricontrollati con lo strumento del revisore di produzione. Soglie: AA 4,5 : 1 per il testo normale, 3 : 1 per il testo grande; AAA 7 : 1.

| Testo | Fondo | Rapporto | Esito | Uso |
|-|-|-|-|-|
| Grafite `#1A2125` | Alluminio `#E3E7E9` | 13,10 : 1 | AAA | testo e titoli |
| Grafite `#1A2125` | Bianco disegno `#F6F8F8` | 15,29 : 1 | AAA | documenti |
| Grigio quota `#5C676D` | Alluminio `#E3E7E9` | 4,67 : 1 | AA | etichette |
| Grigio quota `#5C676D` | Bianco disegno `#F6F8F8` | 5,45 : 1 | AA | etichette nei documenti |
| Bianco `#FFFFFF` | Verde di misura `#008351` | 4,81 : 1 | AA | testo su campo verde |
| Verde di misura `#008351` | Bianco disegno `#F6F8F8` | 4,51 : 1 | AA | testo verde nei documenti |
| Verde di misura `#008351` | Alluminio `#E3E7E9` | 3,87 : 1 | AA solo testo grande | etichette da 18,7 px in grassetto o 24 px in su |
| Bianco `#FFFFFF` | Verde profondo `#0F3A2C` | 12,64 : 1 | AAA | testo su fondo scuro |
| Alluminio `#E3E7E9` | Verde profondo `#0F3A2C` | 10,15 : 1 | AAA | testo secondario su scuro |
| Bianco disegno `#F6F8F8` | Grafite `#1A2125` | 15,29 : 1 | AAA | testo su grafite |
| Alluminio `#E3E7E9` | Grafite `#1A2125` | 13,10 : 1 | AAA | date prenotate nel calendario |
| Acciaio `#8A959B` | Grafite `#1A2125` | 5,32 : 1 | AA | etichette su grafite |
| Grigio quota `#5C676D` | Grafite `#1A2125` | 2,81 : 1 | **vietato** | nessun uso |
| Grafite `#1A2125` | Verde di misura `#008351` | 3,39 : 1 | **vietato per il testo** | nessun uso |
| Acciaio `#8A959B` | Bianco disegno `#F6F8F8` | 2,87 : 1 | non per testo | solo grafica |
| Linea `#B4BDC2` | Bianco disegno `#F6F8F8` | 1,79 : 1 | non per testo | solo filetti |

Tolta dalla v1 la Grafite 80 `#2C353A` (Acciaio su Grafite 80 dava 4,09 : 1, sotto AA).

## Proteggibilità

La combinazione verde e grigio non è registrabile come marchio di colore e non va trattata come asset esclusivo in senso legale. La riconoscibilità poggia sul segno Ab e sul suo uso ricorrente su piastra verde (monogramma, adesivo sui robot, testate), che si può depositare come marchio figurativo secondario se diventa costante.

## Variabili CSS

```css
:root{
  --verde:#008351; --verde-profondo:#0F3A2C;
  --grafite:#1A2125; --alluminio:#E3E7E9; --bianco:#F6F8F8;
  --quota:#5C676D; --acciaio:#8A959B; --linea:#B4BDC2;
}
```
