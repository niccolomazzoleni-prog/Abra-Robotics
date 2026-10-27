# Palette: carta, inchiostro, matita, evidenziatore

I colori sono quelli di un tavolo di laboratorio: la carta del quaderno, l'inchiostro della stampa, la grafite delle note a matita e il giallo dell'evidenziatore che segna il dato che conta. I codici già occupati dai concorrenti (blu elettrico Unitree, cobalto Eagleprojects, cianotipia Comau, arancio da e-commerce, viola da estetica AI) restano fuori.

## Primari

| Nome | HEX | RGB | CMYK indicativo | Ruolo |
|-|-|-|-|-|
| Carta | `#F5F2EA` | 245, 242, 234 | 0, 1, 4, 4 (in stampa: carta naturale non patinata, senza inchiostro) | Fondo di sito, post, documenti a schermo |
| Inchiostro | `#1F1D1A` | 31, 29, 26 | 0, 6, 16, 88 (in offset: nero ricco 40, 40, 40, 100) | Testo, marchio, richiami, fondi scuri |
| Evidenziatore | `#E9EC55` | 233, 236, 85 | 1, 0, 64, 7 (in stampa: tinta piatta, da verificare su mazzetta; mai fluorescente) | Il dato misurato, il retro del biglietto, adesivi, avatar |

## Secondari e funzionali

| Nome | HEX | RGB | CMYK indicativo | Ruolo |
|-|-|-|-|-|
| Grafite | `#625E57` | 98, 94, 87 | 0, 4, 11, 62 | Note a margine, didascalie, metadati |
| Grafite chiara | `#A9A397` | 169, 163, 151 | 0, 4, 11, 34 | Numeri di riga, testo secondario su inchiostro |
| Rigatura | `#DCD6C8` | 220, 214, 200 | 0, 3, 9, 14 | Quadretti, filetti di tabella, bordi. Mai per il testo |
| Verde registro | `#3E6A4E` | 62, 106, 78 | 42, 0, 26, 58 | Solo stati: criterio superato, voce consegnata. Mai decorativo |
| Bianco | `#FFFFFF` | 255, 255, 255 | carta bianca | Cartellini degli adesivi, codici QR |

## Rapporti d'uso

| Colore | Quota indicativa | Note |
|-|-|-|
| Carta | 70% | Il fondo è sempre la pagina. Le superfici scure sono l'eccezione (reel, slide di apertura, flight case) |
| Inchiostro | 20% | Testo e marchio; come fondo massimo una superficie su cinque |
| Grafite e rigatura | 6% | Tutto ciò che è nota, filetto, griglia |
| Evidenziatore | 3% | Una sola evidenziazione per pagina o per schermata. Fa eccezione il giallo pieno di avatar, adesivi e retro del biglietto |
| Verde registro | 1% | Solo segni di stato (spunta, "superato") |

Regola dell'evidenziatore: si evidenzia una misura o un beneficio misurabile, mai un aggettivo. Su fondo inchiostro l'evidenziatore diventa colore del testo, perché la fascia gialla coprirebbe le aste delle lettere.

Regola del punto: il punto di richiamo è inchiostro su carta; su fotografie e superfici scure diventa giallo con anello d'inchiostro, così si vede su qualunque materiale.

## Contrasti WCAG 2.1 (calcolati)

Calcolo con luminanza relativa sRGB, formula (L1 + 0,05) / (L2 + 0,05).

| Testo | Fondo | Rapporto | Esito |
|-|-|-|-|
| Inchiostro | Carta | 15,03 : 1 | AAA |
| Inchiostro | Bianco | 16,81 : 1 | AAA |
| Inchiostro | Evidenziatore | 13,29 : 1 | AAA |
| Inchiostro | Rigatura | 11,61 : 1 | AAA |
| Carta | Inchiostro | 15,03 : 1 | AAA |
| Evidenziatore | Inchiostro | 13,29 : 1 | AAA |
| Grafite | Carta | 5,76 : 1 | AA (AAA solo sopra i 18,66 px in grassetto o 24 px) |
| Grafite | Bianco | 6,45 : 1 | AA |
| Grafite | Evidenziatore | 5,09 : 1 | AA |
| Grafite chiara | Inchiostro | 6,70 : 1 | AA |
| Verde registro | Carta | 5,56 : 1 | AA |
| Carta | Verde registro | 5,56 : 1 | AA |
| Evidenziatore | Carta | 1,13 : 1 | Non ammesso per testo né per segni sottili |
| Rigatura | Carta | 1,29 : 1 | Solo elementi decorativi non informativi |

Conseguenze pratiche: la grafite è il colore minimo per qualunque testo su carta; la grafite chiara si usa per testo solo su inchiostro (su carta solo per numeri di riga decorativi, ripetuti altrove); l'evidenziatore su carta è sempre una fascia sotto un testo in inchiostro, mai un colore di testo.

## Token CSS

```css
:root {
  --carta: #F5F2EA; --inchiostro: #1F1D1A; --grafite: #625E57; --grafite-chiara: #A9A397;
  --rigatura: #DCD6C8; --evidenziatore: #E9EC55; --verde-registro: #3E6A4E;
}
```

Il file completo è `abra-c.css`.
