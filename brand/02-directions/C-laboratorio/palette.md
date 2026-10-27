# Palette: carta, inchiostro, matita, evidenziatore

I colori sono quelli di un tavolo di laboratorio: la carta del quaderno, l'inchiostro della stampa, la grafite delle note a matita e il giallo dell'evidenziatore che segna il dato che conta. Il giallo evidenziatore con l'inchiostro è il colore firma esclusivo della direzione C (indicazione dell'orchestratore, round 1); gialli caldi e ocra sono esclusi. I codici già occupati dai concorrenti (blu elettrico Unitree, cobalto Eagleprojects, cianotipia Comau, arancio da e-commerce, viola da estetica AI) restano fuori.

## Primari

| Nome | HEX | RGB | CMYK indicativo | Ruolo |
|-|-|-|-|-|
| Carta | `#F5F2EA` | 245, 242, 234 | 3, 3, 6, 0 (in stampa: carta naturale non patinata, senza inchiostro) | Fondo di sito, post, documenti a schermo |
| Inchiostro | `#1F1D1A` | 31, 29, 26 | 72, 71, 71, 67 (ritorno a schermo #20201E, dE 1,8) | Testo, marchio, richiami, fondi scuri |
| Evidenziatore | `#EEE842` | 238, 232, 66 | 8, 0, 90, 0 (in gamut: l'HEX è il ritorno a schermo di questa quadricromia). Tinta piatta indicativa Pantone 395 C o 3965 C, da scegliere su mazzetta coated e uncoated; mai fluorescente | Il numero o il criterio misurato, il retro del biglietto, avatar e favicon |

CMYK ricalcolati in v2 con il profilo Generic CMYK di macOS (intento colorimetrico relativo, Pillow ImageCms); tra parentesi il ritorno a schermo quando lo scarto supera 1,5. Tutti i valori sono indicativi: con lo stampatore si usa il suo profilo (per esempio Fogra 39).

## Secondari e funzionali

| Nome | HEX | RGB | CMYK indicativo | Ruolo |
|-|-|-|-|-|
| Grafite | `#625E57` | 98, 94, 87 | 63, 58, 61, 13 | Note a margine, didascalie, metadati |
| Grafite chiara | `#A9A397` | 169, 163, 151 | 32, 29, 34, 0 | Testo secondario solo su inchiostro; su carta solo elementi non testuali |
| Rigatura | `#DCD6C8` | 220, 214, 200 | 12, 11, 16, 0 | Quadretti, filetti di tabella, bordi. Mai per il testo |
| Verde registro | `#3E6A4E` | 62, 106, 78 | 76, 33, 73, 21 | Solo stati: criterio superato, voce consegnata. Mai decorativo |
| Bianco | `#FFFFFF` | 255, 255, 255 | carta bianca | Cartellini degli adesivi, codici QR |

## Rapporti d'uso

| Colore | Quota indicativa | Note |
|-|-|-|
| Carta | 70% | Il fondo è sempre la pagina. Le superfici scure sono l'eccezione (reel, slide di apertura, flight case) |
| Inchiostro | 20% | Testo e marchio; come fondo massimo una superficie su cinque |
| Grafite e rigatura | 6% | Tutto ciò che è nota, filetto, griglia |
| Evidenziatore | 3% | Una sola evidenziazione per pagina o per schermata. Fa eccezione il giallo pieno di avatar, adesivi e retro del biglietto |
| Verde registro | 1% | Solo segni di stato (spunta, "superato") |

Regola dell'evidenziatore (v2): si evidenzia solo un numero o un criterio misurato ("3 settimane", "≤ 15 s", "70%", "circa 2 ore"), mai un titolo, mai un aggettivo, mai una frase di beneficio. Al massimo una evidenziazione per applicazione. Su fondo inchiostro non si evidenzia.

Regola delle attrezzature (v2): su robot, flight case ed etichette il fondo è carta bianca e il giallo compare solo nel punto del richiamo. Le campiture gialle piene restano a schermo (avatar, favicon) e al retro del biglietto, così il giallo e nero non si confonde con la segnaletica di sicurezza dei reparti.

Regola del punto: il punto di richiamo è inchiostro su carta; su fotografie diventa giallo con anello d'inchiostro, e cade sempre sul componente nominato.

## Contrasti WCAG 2.1 (calcolati)

Calcolo con luminanza relativa sRGB, formula (L1 + 0,05) / (L2 + 0,05).

| Testo | Fondo | Rapporto | Esito |
|-|-|-|-|
| Inchiostro | Carta | 15,03 : 1 | AAA |
| Inchiostro | Bianco | 16,81 : 1 | AAA |
| Inchiostro | Evidenziatore | 13,02 : 1 | AAA |
| Inchiostro | Rigatura | 11,61 : 1 | AAA |
| Carta | Inchiostro | 15,03 : 1 | AAA |
| Evidenziatore | Inchiostro | 13,02 : 1 | AAA (solo per segni, non per testo: su inchiostro non si evidenzia) |
| Grafite | Carta | 5,76 : 1 | AA (AAA solo sopra i 18,66 px in grassetto o 24 px) |
| Grafite | Bianco | 6,45 : 1 | AA |
| Grafite | Evidenziatore | 4,99 : 1 | AA |
| Grafite chiara | Inchiostro | 6,70 : 1 | AA |
| Verde registro | Carta | 5,56 : 1 | AA |
| Carta | Verde registro | 5,56 : 1 | AA |
| Evidenziatore | Carta | 1,15 : 1 | Non ammesso per testo né per segni sottili |
| Rigatura | Carta | 1,29 : 1 | Solo elementi decorativi non informativi |

Conseguenze pratiche: la grafite è il colore minimo per qualunque testo su carta, compresi numeri di riga ed etichette degli assi (corretto in v2); la grafite chiara si usa per testo solo su inchiostro; l'evidenziatore su carta è sempre una fascia sotto un testo in inchiostro, mai un colore di testo.

## Token CSS

```css
:root {
  --carta: #F5F2EA; --inchiostro: #1F1D1A; --grafite: #625E57; --grafite-chiara: #A9A397;
  --rigatura: #DCD6C8; --evidenziatore: #EEE842; --verde-registro: #3E6A4E;
}
```

Il file completo è `abra-c.css`.
