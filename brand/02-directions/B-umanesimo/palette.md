# Palette v2. Territorio B, Montato a vista

Colore firma esclusivo della direzione: **Rosso Abra con ocra**, nella tradizione delle macchine da ufficio italiane del Novecento. Il resto della palette è neutro e freddo come il grigio delle stesse macchine, così il rosso resta un segnale e non diventa decorazione. In v2 sono stati tolti verderame, avorio caldo e inchiostro bruno (vedi `changelog.md`).

## Colori

| Nome | HEX | RGB | CMYK da profilo | Ruolo |
|-|-|-|-|-|
| **Rosso Abra** | `#B83A2B` | 184, 58, 43 | 7 / 86 / 89 / 13 | Marchio, un solo pannello pieno per pagina, filetti di serie |
| **Ocra** | `#E2A93B` | 226, 169, 59 | 2 / 30 / 91 / 5 | Bollino "Esempio", fascia dei contatti sul totem, segno della serie laboratori |
| Ocra chiara | `#F2E0B0` | 242, 224, 176 | 5 / 9 / 32 / 0 | Riquadro dei limiti dichiarati |
| **Grafite** | `#232527` | 35, 37, 39 | 80 / 74 / 66 / 55 | Testo, pulsanti, filetti. Neutra, senza dominante bruna |
| Grigio | `#5E6264` | 94, 98, 100 | 67 / 56 / 51 / 9 | Testo secondario, etichette di tabella |
| **Grigio Lettera** | `#DADCD6` | 218, 220, 214 | 12 / 8 / 10 / 0 | Pannelli, sfondo delle foto dei robot |
| Carta | `#F6F4EF` | 246, 244, 239 | 3 / 3 / 4 / 0 | Fondo e giunti tra i pannelli |
| Bianco | `#FFFFFF` | 255, 255, 255 | 0 / 0 / 0 / 0 | Pannelli di testo, documenti |

I CMYK sono calcolati con il profilo `Generic CMYK Profile` di macOS, intento colorimetrico relativo; il ritorno a sRGB resta entro dE 2,3 per tutti i colori tranne il Rosso Abra (dE 5,1), che esce dal gamut della quadricromia.

**Stampa del Rosso Abra.** Per biglietti, retro dei biglietti, flight case e totem si usa una tinta piatta. Riferimento Pantone indicativo nella famiglia dei rossi aranciati (per esempio PANTONE 7621 C o 1795 C), da scegliere sulla mazzetta reale confrontata con una prova colore; in quadricromia si accetta il 7 / 86 / 89 / 13, leggermente più spento. **Ocra**: in gamut, riferimento indicativo PANTONE 7409 C, da verificare. Il rosso scuro della v1 è stato eliminato perché fuori gamut (dE 7,8).

## Rapporti d'uso

| Colore | Quota indicativa | Regola |
|-|-|-|
| Bianco e carta | 55% | Fondo e pannelli di testo |
| Grigio Lettera | 18% | Pannelli di dati e di immagine |
| Grafite e grigio | 14% | Testo e strumenti |
| Rosso Abra | 10% | Massimo un pannello pieno per pagina; nei documenti contrattuali solo marchio e filetti |
| Ocra e ocra chiara | 3% | Solo per esempi, limiti e contatti |

**Pagina industriale** (preventivo interno, verbali, manuali): il rosso compare solo nel marchio, nell'etichetta e nel filetto della fase in corso. Esempio in `applicazioni/preventivo-interna.png`.

**Serie dei materiali**: proposte e preventivi con pannello rosso in copertina; eventi con fascia rossa e fascia ocra; manuali e consegne con copertina Grigio Lettera e filetto ocra.

## Contrasti WCAG 2.1 calcolati

Soglie: 4,5 testo normale (AA), 3 testo grande da 24 px o 19 px grassetto, 7 AAA.

| Testo | Fondo | Rapporto | Esito | Uso |
|-|-|-|-|-|
| Grafite | Bianco | 15,38 | AAA | Tutto il testo |
| Grafite | Carta | 13,99 | AAA | Tutto il testo |
| Grafite | Grigio Lettera | 11,12 | AAA | Testo sui pannelli grigi |
| Grafite | Ocra | 7,30 | AAA | Bollino "Esempio", fascia contatti |
| Grafite | Ocra chiara | 11,77 | AAA | Riquadro dei limiti |
| Grigio | Bianco | 6,16 | AA | Didascalie, etichette |
| Grigio | Carta | 5,61 | AA | Didascalie |
| Grigio | Ocra chiara | 4,72 | AA | Note nei limiti |
| Rosso Abra | Bianco | 5,71 | AA | Marchio, etichette rosse |
| Rosso Abra | Carta | 5,19 | AA | Marchio |
| Bianco | Rosso Abra | 5,71 | AA | Testo sul pannello rosso |
| Carta | Rosso Abra | 5,19 | AA | Titoli sul pannello rosso |
| Carta | Grafite | 13,99 | AAA | Pulsanti |
| Ocra chiara | Rosso Abra | 4,37 | AA grande | Solo testo da 24 px in su |
| Rosso Abra | Grigio Lettera | 4,13 | AA grande | Solo testo da 24 px in su |

**Coppie vietate per il testo**: Grigio su Grigio Lettera (4,46), ocra su carta (1,92), grafite su rosso (2,69), ocra su rosso (2,71). Nelle applicazioni v2 nessun testo usa queste coppie.
