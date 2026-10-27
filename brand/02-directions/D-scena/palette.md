# Palette v2: una gelatina magenta e i neutri del palco

Il colore firma è una gelatina teatrale: il magenta che ogni tecnico luci usa per i controluce e le scene di festa. Non è usato dalle altre direzioni (A verde di misura, B rosso con ocra, C giallo evidenziatore, E gesso da sarto) né dai competitor rilevati (blu Unitree e AgiBot, teal Oversonic, azzurro SIR, salmone PAL). È un primario della stampa in quadricromia, quindi si riproduce bene su carta, vinile e forex, e porta il nome di Magenta, in Lombardia.

## Colori

CMYK calcolati con Pillow ImageCms dal profilo `Generic CMYK Profile.icc` di macOS, intento colorimetrico relativo. Ritorno = colore che si ottiene riconvertendo il CMYK in sRGB.

| Nome | Ruolo | HEX | RGB | CMYK calcolato | Ritorno | Pantone indicativo |
|-|-|-|-|-|-|-|
| **Magenta di scena** | Colore firma: arco scenico negli eventi, punti della pianta, pulsanti | `#D6006F` | 214, 0, 111 | 2, 96, 14, 4 | `#CF2570` | 226 C |
| **Grafite** | Testo dei documenti, fondo di scena | `#202124` | 32, 33, 36 | 80, 75, 65, 60 (TAC 280%) | `#1F2225` | 426 C |
| **Carta** | Pagina | `#FAFAF7` | 250, 250, 247 | 2, 1, 2, 0 | `#FAFAF7` | carta bianca naturale |
| **Cemento** | Fondi neutri, pavimenti, tavole | `#E7E6E1` | 231, 230, 225 | 7, 6, 7, 0 | `#E9E8E3` | Cool Gray 1 C |
| Rosa | Gelatina diluita: colonna dei criteri nelle tabelle | `#FBE3EE` | 251, 227, 238 | 4, 12, 1, 0 | `#EEDFE5` | 705 C |
| Quinta | Secondo piano su Grafite | `#3A3B40` | 58, 59, 64 | 79, 73, 61, 31 | `#373A3F` | 425 C |
| Fumo | Testo secondario su chiaro | `#5F6066` | 95, 96, 102 | 67, 58, 48, 9 | `#5C6067` | Cool Gray 10 C |
| Fumo chiaro | Testo secondario su Grafite | `#A9AAAF` | 169, 170, 175 | 31, 25, 19, 0 | `#A8ABB0` | Cool Gray 6 C |

Note di stampa:
- Il Magenta di scena è appena fuori gamma in quadricromia: il ritorno è un magenta meno saturo (`#CF2570`). Per totem, flight case e biglietti in tiratura si stampa in tinta piatta **Pantone 226 C**; per i preventivi stampati in ufficio la quadricromia basta.
- La Grafite in grandi campiture (totem su forex, flight case) si stampa con il CMYK sopra (TAC 280%, sotto il limite di 300% delle macchine offset comuni) oppure in Pantone 426 C. Chiedere sempre una prova colore per forex e vinile.

## Rapporti d'uso

| Registro | Grafite | Magenta | Carta e Cemento | Secondari |
|-|-|-|-|-|
| Documento (preventivo, post aziendali, scheda laboratorio, biglietto) | 15% (testo) | 2 a 4% | 78% | 4% |
| Scena (reel, totem, livrea, eventi) | 55% | 30% | 10% | 5% |
| Sito | 15% | 5% | 75% | 5% |

Regole:
- Nei documenti il magenta compare solo in punti (posizioni della pianta, etichette brevi, un filo): mai come fondo.
- Nella scena il magenta riempie l'arco scenico, una sola campitura per composizione.
- Nessuna sfumatura e nessun alone: il magenta è sempre pieno e con bordi netti.
- Le foto restano a colori naturali; il magenta non si applica sopra il robot.

## Contrasti WCAG (calcolati)

Formula WCAG 2.1. Soglie: AA testo normale 4,5; AA testo grande 3 (da 24 px, o 18,5 px in grassetto); AAA 7.

| Testo | Fondo | Rapporto | Esito |
|-|-|-|-|
| Grafite | Carta | 15,40 : 1 | AAA |
| Grafite | Cemento | 12,88 : 1 | AAA |
| Grafite | Rosa | 13,28 : 1 | AAA |
| Carta | Grafite | 15,40 : 1 | AAA |
| Carta | Quinta | 10,68 : 1 | AAA |
| Carta | Magenta | 4,91 : 1 | AA |
| Magenta | Carta | 4,91 : 1 | AA |
| Fumo | Carta | 5,99 : 1 | AA |
| Fumo | Cemento | 5,01 : 1 | AA |
| Fumo chiaro | Grafite | 6,94 : 1 | AA |
| Magenta | Cemento | 4,11 : 1 | Solo testo grande |
| Magenta | Grafite | 3,13 : 1 | Solo testo grande, mai nelle applicazioni |

Nelle applicazioni nessuna coppia testo e fondo scende sotto AA: il magenta come testo compare solo su Carta.

## Token CSS

```css
--magenta:#D6006F; --rosa:#FBE3EE; --grafite:#202124; --quinta:#3A3B40;
--carta:#FAFAF7; --cemento:#E7E6E1; --fumo:#5F6066; --fumo-chiaro:#A9AAAF;
```
