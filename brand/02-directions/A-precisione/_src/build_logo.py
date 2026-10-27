"""Genera gli SVG del marchio v2 "In squadra" in ../logo/.
Uso: python build_logo.py   (richiede shapely)

Il segno e la legatura Ab v3: la A e intera (aste a pendenza 2 a 1 e traversa) e il suo piede destro
poggia sull'asta verticale della b; il vuoto tra la A e la b e una squadra.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from glyphs import *
from proof import SB, KERN

OUT = os.path.join(os.path.dirname(__file__), '..', 'logo')
GRAFITE = '#1A2125'
VERDE = '#00843D'
BIANCO = '#FFFFFF'
NERO = '#000000'
CLEAR = 25.0  # area di rispetto: un quarto dell'altezza delle maiuscole


def word(text, s=16.0, head=0.45):
    """compone una parola; se inizia con Ab usa la legatura"""
    x = 0.0
    geoms = []
    prev = None
    i = 0
    if text.startswith('Ab'):
        g, adv = g_Ab2(None, s, overlap=0.6)
        geoms.append(g)
        x = adv + SB['b'][1]
        prev = 'b'
        i = 2
    for ch in text[i:]:
        if ch == ' ':
            x += 26
            prev = None
            continue
        g, adv = GLYPHS[ch](None, s)
        l, r = SB[ch]
        if prev:
            x += KERN.get(prev + ch, 0)
        x += l
        geoms.append(affinity.translate(g, x, 0))
        x += adv + r
        prev = ch
    last = text[-1]
    return unary_union(geoms), x - SB[last][1]


def P(geom, fill, dx, dy, flip_h, scale=1.0):
    return f'<path fill="{fill}" d="{to_path(geom, dx=dx, dy=dy, flip_h=flip_h, scale=scale, prec=2)}"/>'


def write(name, w, h, body, title, extra=''):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}"{extra} role="img" aria-labelledby="t">'
           f'<title id="t">{title}</title>{body}</svg>\n')
    open(os.path.join(OUT, name), 'w').write(svg)


# favicon disegnata pixel per pixel su griglia 16: 1 = pixel bianco
FAV16 = [
    "................",
    "................",
    "....##...##.....",
    "....##...##.....",
    "...####..##.....",
    "...####..##.....",
    "...####..#####..",
    "..##..##.######.",
    "..##..##.##..##.",
    "..######.##..##.",
    ".##....####..##.",
    ".##....####..##.",
    ".##....#######..",
    ".##....######...",
    "................",
    "................",
]


def pixel_path(rows):
    parts = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            if row[x] == '#':
                x0 = x
                while x < len(row) and row[x] == '#':
                    x += 1
                parts.append(f'M{x0} {y}h{x - x0}v1h{x0 - x}z')
            else:
                x += 1
    return ''.join(parts)


def main():
    os.makedirs(OUT, exist_ok=True)
    s = 16.0
    letters, ww = word('Abra Robotics', s)
    c = CLEAR
    W, Hh = ww + 2 * c, H + 2 * c
    write('orizzontale.svg', round(W, 1), round(Hh, 1), P(letters, GRAFITE, c, c, H), 'Abra Robotics')
    write('orizzontale-bianco.svg', round(W, 1), round(Hh, 1), P(letters, BIANCO, c, c, H), 'Abra Robotics, in bianco per fondi scuri o verdi')
    write('mono-positivo.svg', round(W, 1), round(Hh, 1), P(letters, NERO, c, c, H), 'Abra Robotics, monocromatico positivo')
    write('mono-negativo.svg', round(W, 1), round(Hh, 1), P(letters, BIANCO, c, c, H), 'Abra Robotics, monocromatico negativo, solo forma bianca')

    # verticale: Abra sopra, Robotics sotto, allineati a sinistra
    l1, w1 = word('Abra', s)
    l2, w2 = word('Robotics', s)
    l2 = affinity.translate(l2, -SB['R'][0], 0)
    lead = H * 1.42
    Wv, Hv = max(w1, w2) + 2 * c, H + lead + 2 * c
    body = P(l1, GRAFITE, c, c, H) + P(l2, GRAFITE, c, c + lead, H)
    write('verticale.svg', round(Wv, 1), round(Hv, 1), body, 'Abra Robotics, versione verticale')
    write('verticale-bianco.svg', round(Wv, 1), round(Hv, 1), body.replace(GRAFITE, BIANCO), 'Abra Robotics, versione verticale in bianco')

    # simbolo: legatura Ab, tratto 18
    sA = 18.0
    Ab, adv = g_Ab2(None, sA, overlap=0.6)
    write('simbolo-netto.svg', round(adv, 2), H, P(Ab, GRAFITE, 0, 0, H), 'Abra Robotics, simbolo senza area di rispetto')
    side = round(max(adv, H) + 2 * c, 1)
    ox, oy = (side - adv) / 2, (side - H) / 2
    body = P(Ab, GRAFITE, ox, oy, H)
    write('simbolo.svg', side, side, body, 'Abra Robotics, simbolo')
    write('simbolo-bianco.svg', side, side, body.replace(GRAFITE, BIANCO), 'Abra Robotics, simbolo in bianco')

    # monogramma: piastra verde con la legatura in bianco (avatar, adesivo, timbro)
    side = 160.0
    sc = 0.62
    Ab2 = affinity.scale(Ab, sc, sc, origin=(0, 0))
    ox, oy = (side - adv * sc) / 2, (side - H * sc) / 2
    body = f'<rect width="{side:g}" height="{side:g}" fill="{VERDE}"/>' + P(Ab2, BIANCO, ox, oy, H * sc)
    write('monogramma.svg', side, side, body, 'Abra Robotics, monogramma su piastra verde')
    write('monogramma-grafite.svg', side, side, body.replace(VERDE, GRAFITE), 'Abra Robotics, monogramma su piastra grafite')

    # favicon vettoriale per 32 px e oltre
    g = 32.0
    scF = 20.0 / H
    AbF = affinity.scale(g_Ab2(None, 20.0, overlap=0.6)[0], scF, scF, origin=(0, 0))
    advF = g_Ab2(None, 20.0, overlap=0.6)[1] * scF
    body = f'<rect width="32" height="32" fill="{VERDE}"/>' + P(AbF, BIANCO, (g - advF) / 2, (g - 20) / 2, 20)
    write('favicon.svg', 32, 32, body, 'Abra Robotics')

    # favicon ottica 16 px, pixel per pixel
    body = f'<rect width="16" height="16" fill="{VERDE}"/><path fill="{BIANCO}" d="{pixel_path(FAV16)}"/>'
    write('favicon-16.svg', 16, 16, body, 'Abra Robotics, favicon 16 px', extra=' shape-rendering="crispEdges"')
    print('ok', round(W, 1), round(Hh, 1))


if __name__ == '__main__':
    main()
