import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from glyphs import *

# margini laterali (sinistro, destro) per lettera, in unita. Lati dritti piu larghi, tondi piu stretti.
SB = {
    'A': (0, 0), 'b': (9, 6), 'a': (6, 9), 'r': (9, 1), 'R': (9, 2), 'o': (6, 6),
    'c': (6, 3), 't': (2, 3), 'i': (9, 9), 's': (5, 5),
}
KERN = {'Ab': -1, 'ra': 2, 'Ro': 0, 'ot': -1, 'tc': 0, 'ti': 0}


def glyph(ch, s, datum=False):
    if ch == 'A' and datum:
        return A_datum(s)
    return GLYPHS[ch](None, s)


def A_datum(s, W=None, bar=None):
    """A con il triangolo di riferimento: il controstampo superiore ripetuto in positivo sulla linea di base."""
    W = W or 84 + (s - 16) * 1.2
    bar = bar or 49 + (s - 16) * 0.3
    A, adv = g_A(None, s, width=W, bar=bar)
    polys = [A] if isinstance(A, Polygon) else list(A.geoms)
    hole = None
    for p in polys:
        if p.interiors:
            hole = Polygon(p.interiors[0])
    minx, miny, maxx, maxy = hole.bounds
    t = affinity.translate(hole, 0, -miny)
    return unary_union([A, t]), adv


def setword(word, s=16.0, kern=KERN, sb=SB, datum=False, track=0.0):
    x = 0.0
    geoms = []
    prev = None
    for ch in word:
        if ch == ' ':
            x += 26 + track
            prev = None
            continue
        g, adv = glyph(ch, s, datum and ch == 'A')
        l, r = sb[ch]
        if prev:
            x += kern.get(prev + ch, 0)
        x += l
        geoms.append(affinity.translate(g, x, 0))
        x += adv + r + track
        prev = ch
    return unary_union(geoms), x


def svg(paths, vb, bg='#fff', fg='#111'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" style="background:{bg}">' + ''.join(f'<path fill="{fg}" fill-rule="evenodd" d="{p}"/>' for p in paths) + '</svg>'


if __name__ == '__main__':
    out = []
    for word, s, d in [('Abra', 16, True), ('Abra Robotics', 16, True), ('Robotics', 12, False), ('Abra Robotics', 18, True), ('bracci robot rotti', 16, False)]:
        g, w = setword(word, s=s, datum=d)
        p = to_path(g, dx=10, dy=10)
        out.append(f'<div class="row">{svg([p], f"0 0 {w+20:.0f} 125")}</div>')
    html = '<html><body style="margin:20px;background:#ddd"><style>.row svg{height:200px;display:block;margin:10px 0}</style>' + ''.join(out) + '</body></html>'
    open(sys.argv[1], 'w').write(html)
