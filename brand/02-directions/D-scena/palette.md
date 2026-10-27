# Palette: i colori del teatro all'italiana, in chiave industriale

Il riferimento è la sala di un teatro all'italiana vista con gli occhi di un tecnico luci: il velluto delle poltrone, la luce di tungsteno sul palcoscenico, lo stucco dei palchi. Tre colori fanno il marchio; gli altri servono il testo e i dati. Nessun colore è una sfumatura: ogni campitura è piena e ha bordi netti, come una luce tagliata dalle lame di un sagomatore.

## Colori primari

| Nome | Ruolo | HEX | RGB | CMYK indicativo (patinata) |
|-|-|-|-|-|
| **Velluto** | Fondo di scena, testo su carta, marchio | `#3A1915` | 58, 25, 21 | 35, 85, 80, 60 |
| **Luce** | Il palco acceso, accento unico, pavimento della A | `#E9AE45` | 233, 174, 69 | 5, 35, 85, 0 |
| **Stucco** | Fondo dei documenti, testo su velluto | `#F3ECDF` | 243, 236, 223 | 3, 5, 12, 0 |

## Colori secondari

| Nome | Ruolo | HEX | RGB | CMYK indicativo |
|-|-|-|-|-|
| Carta | Pagina del preventivo e del manuale | `#FBF8F2` | 251, 248, 242 | 1, 2, 5, 0 |
| Buio | Sala a luci spente: flight case, video, fondi molto grandi | `#211412` | 33, 20, 18 | 50, 75, 70, 80 |
| Quinta | Taglio di luce sul fondale velluto (solo come campitura) | `#4A221C` | 74, 34, 28 | 35, 85, 80, 50 |
| Paglia | Luce diffusa: colonna dei criteri, evidenziazioni | `#F4D79E` | 244, 215, 158 | 3, 15, 45, 0 |
| Fumo | Testo secondario su chiaro | `#6F645B` | 111, 100, 91 | 40, 45, 50, 40 |
| Fumo chiaro | Testo secondario su velluto, didascalie | `#B5A99C` | 181, 169, 156 | 25, 28, 35, 5 |
| Rame | Solo stati e avvisi (etichetta "Esempio", errori) | `#A4472B` | 164, 71, 43 | 20, 80, 90, 15 |

I valori CMYK sono indicativi e vanno verificati con una prova colore sulla carta scelta. Velluto in stampa va costruito ricco (mai con il solo nero) per non diventare marrone spento.

## Rapporti d'uso

| Contesto | Velluto | Luce | Stucco / Carta | Secondari |
|-|-|-|-|-|
| Scena (social, totem, video, hero) | 55% | 25% | 15% | 5% |
| Documento (preventivo, manuale, mail) | 20% | 5% | 70% | 5% |
| Media su tutto il sistema | 40% | 15% | 40% | 5% |

Regole:
- **La Luce sta in basso.** È il pavimento del palco: occupa il terzo inferiore delle composizioni, oppure il pavimento della A. Non diventa un fondo pieno a tutta pagina, tranne che sul retro di un formato piccolo.
- **Un solo colore caldo acceso per composizione.** Rame non convive con grandi campiture Luce.
- **Campiture piene.** Il passaggio dalla Quinta al Velluto è sempre un bordo netto.
- **Le foto entrano nella palette** con il trattamento tungsteno (vedi `foto-video.md`).

## Contrasti WCAG (calcolati)

Formula WCAG 2.1 sulla luminanza relativa. Soglie: AA testo normale 4,5; AA testo grande 3; AAA testo normale 7.

| Testo | Fondo | Rapporto | Esito |
|-|-|-|-|
| Velluto | Stucco | 13,44 : 1 | AAA |
| Velluto | Carta | 14,90 : 1 | AAA |
| Velluto | Luce | 7,98 : 1 | AAA |
| Velluto | Paglia | 11,33 : 1 | AAA |
| Buio | Luce | 9,04 : 1 | AAA |
| Stucco | Velluto | 13,44 : 1 | AAA |
| Luce | Velluto | 7,98 : 1 | AAA |
| Luce | Buio | 9,04 : 1 | AAA |
| Paglia | Velluto | 11,33 : 1 | AAA |
| Fumo chiaro | Velluto | 6,86 : 1 | AA |
| Fumo | Stucco | 4,90 : 1 | AA |
| Fumo | Carta | 5,43 : 1 | AA |
| Rame | Carta | 5,64 : 1 | AA |
| Rame | Stucco | 5,09 : 1 | AA |
| Stucco | Rame | 5,09 : 1 | AA |
| Luce | Stucco | 1,69 : 1 | Vietato per il testo |
| Luce | Carta | 1,87 : 1 | Vietato per il testo |

La Luce su fondi chiari si usa solo come campitura (il pavimento del palco, il pavimento della A, le barre dei grafici), mai per scrivere.

## Token CSS

Tutti i mockup leggono i colori da `sistema.css`:

```css
--velluto:#3A1915; --buio:#211412; --luce:#E9AE45; --paglia:#F4D79E;
--stucco:#F3ECDF; --carta:#FBF8F2; --fumo:#6F645B; --fumo-chiaro:#B5A99C;
--rame:#A4472B; --quinta:#4A221C;
```
