"""Genera tutti gli SVG del marchio "Riferimento A" in ../logo/.
Uso: python build_logo.py   (richiede shapely)
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from glyphs import *
from proof import setword, SB, KERN

OUT = os.path.join(os.path.dirname(__file__), '..', 'logo')
GRAFITE = '#1A2125'
VERDE = '#00875A'
BIANCO = '#F6F8F8'
NERO = '#000000'


ANG = 63.43494882  # pendenza delle aste 2 a 1 (tan = 2)


def A_parts(s, gapk=0.45, apexk=-0.25, ang=ANG):
    """A di riferimento: aste a 60 gradi; il controstampo superiore e ripetuto in positivo
    sulla linea di base. La traversa si colloca in modo che tra la punta del triangolo e la
    traversa resti una luce pari a 0,6 volte il tratto."""
    import math
    W = 2 * (H + s * apexk) / math.tan(math.radians(ang))
    best = None
    for bar10 in range(300, 620, 2):
        bar = bar10 / 10
        A, adv = g_A(None, s, width=W, bar=bar, apex=s * apexk)
        polys = [A] if isinstance(A, Polygon) else list(A.geoms)
        hs = [Polygon(p.interiors[0]) for p in polys if p.interiors]
        if not hs:
            continue
        hole = hs[0]
        gap = (bar - 0.42 * s) - (hole.bounds[3] - hole.bounds[1])
        if best is None or abs(gap - gapk * s) < abs(best[0] - gapk * s):
            best = (gap, A, hole, adv)
    _, A, hole, adv = best
    t = affinity.translate(hole, 0, -hole.bounds[1])
    return A, t, adv


def word_parts(word, s=16.0):
    """come setword ma tiene separato il triangolo della prima A"""
    x = 0.0
    letters, tri = [], None
    prev = None
    for ch in word:
        if ch == ' ':
            x += 26
            prev = None
            continue
        if ch == 'A':
            g, t, adv = A_parts(s)
        else:
            g, adv = GLYPHS[ch](None, s)
            t = None
        l, r = SB[ch]
        if prev:
            x += KERN.get(prev + ch, 0)
        x += l
        letters.append(affinity.translate(g, x, 0))
        if t is not None and tri is None:
            tri = affinity.translate(t, x, 0)
        x += adv + r
        prev = ch
    # togliamo i margini laterali esterni: il marchio parte dal piede della A
    return unary_union(letters), tri, x - SB[word[-1]][1]


def P(geom, fill, dx, dy, flip_h, scale=1.0):
    d = to_path(geom, dx=dx, dy=dy, flip_h=flip_h, scale=scale, prec=2)
    return f'<path fill="{fill}" d="{d}"/>'


def write(name, w, h, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" role="img" aria-labelledby="t">'
           f'<title id="t">{title}</title>{body}</svg>\n')
    open(os.path.join(OUT, name), 'w').write(svg)


def main():
    os.makedirs(OUT, exist_ok=True)
    s = 16.0
    # zona di rispetto: altezza del triangolo di riferimento (circa un quarto dell'altezza delle maiuscole)
    letters, tri, wordw = word_parts('Abra Robotics', s)
    th = tri.bounds[3] - tri.bounds[1]
    pad = round(th, 1)
    clear = pad

    # orizzontale: logotipo monocromatico grafite
    W = wordw + 2 * clear
    Hh = H + 2 * clear
    letters_noT = letters.difference(tri.buffer(0.01)) if letters.intersects(tri) else letters
    body = P(letters, GRAFITE, clear, clear, H) + P(tri, GRAFITE, clear, clear, H)
    write('orizzontale.svg', round(W, 1), round(Hh, 1), body, 'Abra Robotics')

    # mono positivo e negativo (orizzontale)
    allg = unary_union([letters, tri])
    write('mono-positivo.svg', round(W, 1), round(Hh, 1), P(allg, NERO, clear, clear, H), 'Abra Robotics, monocromatico positivo')
    write('mono-negativo.svg', round(W, 1), round(Hh, 1),
          f'<rect id="fondo" width="100%" height="100%" fill="{GRAFITE}"/>' + P(allg, BIANCO, clear, clear, H),
          'Abra Robotics, monocromatico negativo (il rettangolo di fondo si elimina in uso)')

    # verticale: Abra sopra, Robotics sotto, allineati a sinistra, interlinea = 1,5 H
    l1, t1, w1 = word_parts('Abra', s)
    l2, _, w2 = word_parts('Robotics', s)
    # Robotics: compensiamo il margine sinistro della R per allineare l'asta al piede della A
    l2 = affinity.translate(l2, -SB['R'][0], 0)
    w2 -= SB['R'][0]
    lead = H * 1.42
    Wv = max(w1, w2) + 2 * clear
    Hv = H + lead + 2 * clear
    body = (P(l1, GRAFITE, clear, clear, H) + P(t1, GRAFITE, clear, clear, H)
            + P(l2, GRAFITE, clear, clear + lead, H))
    write('verticale.svg', round(Wv, 1), round(Hv, 1), body, 'Abra Robotics, versione verticale')
    write('verticale-bianco.svg', round(Wv, 1), round(Hv, 1), body.replace(GRAFITE, BIANCO), 'Abra Robotics, versione verticale in bianco per fondi scuri')
    write('orizzontale-bianco.svg', round(W, 1), round(Hh, 1), P(allg, BIANCO, clear, clear, H), 'Abra Robotics, in bianco per fondi scuri')

    # simbolo: A di riferimento, tratto piu pesante per le piccole dimensioni
    sA = 18.0
    A, T, adv = A_parts(sA)
    side = round(adv * 1.32, 1)
    ox = (side - adv) / 2
    oy = (side - H) / 2
    body = P(A, GRAFITE, ox, oy, H) + P(T, GRAFITE, ox, oy, H)
    write('simbolo.svg', side, side, body, 'Abra Robotics, simbolo')
    write('simbolo-bianco.svg', side, side, body.replace(GRAFITE, BIANCO), 'Abra Robotics, simbolo in bianco')
    # simbolo stretto senza margini, per comporre (adesivi, timbri)
    write('simbolo-netto.svg', round(adv, 2), H, P(unary_union([A, T]), GRAFITE, 0, 0, H), 'Abra Robotics, simbolo senza area di rispetto')

    # monogramma: la A di riferimento nel riquadro, come la lettera di riferimento nel disegno tecnico
    side = 160.0
    fr_t = 10.0
    frame = box(0, 0, side, side).difference(box(fr_t, fr_t, side - fr_t, side - fr_t))
    sc = 0.70
    A2 = affinity.scale(A, sc, sc, origin=(0, 0))
    T2 = affinity.scale(T, sc, sc, origin=(0, 0))
    aw = adv * sc
    ox = (side - aw) / 2
    oy = (side - H * sc) / 2 + 1.5
    A2 = affinity.translate(A2, ox, oy)
    T2 = affinity.translate(T2, ox, oy)
    body = P(frame, GRAFITE, 0, 0, side) + P(A2, GRAFITE, 0, 0, side) + P(T2, GRAFITE, 0, 0, side)
    write('monogramma.svg', side, side, body, 'Abra Robotics, monogramma')

    # favicon: piastra grafite e A in bianco disegno, su griglia 32
    g = 32.0
    sF = 25.0
    AF, TF, advF = A_parts(sF)
    scF = 19.0 / H
    AF = affinity.scale(AF, scF, scF, origin=(0, 0))
    TF = affinity.scale(TF, scF, scF, origin=(0, 0))
    ox = (g - advF * scF) / 2
    oy = 6.2
    AF = affinity.translate(AF, ox, oy)
    TF = affinity.translate(TF, ox, oy)
    body = (f'<rect width="32" height="32" rx="3" fill="{GRAFITE}"/>' + P(AF, BIANCO, 0, 0, g) + P(TF, BIANCO, 0, 0, g))
    write('favicon.svg', 32, 32, body, 'Abra Robotics')

    print('ok', round(W, 1), round(Hh, 1), 'clear', clear)


if __name__ == '__main__':
    main()
