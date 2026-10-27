"""Costruzione geometrica del logotipo Abra, direzione A "Riferimento A".
Ogni lettera nasce da una linea d'asse (centerline) spessorata con tratto costante,
come i caratteri incisi sulle targhe dati (DIN 1451 come riferimento di metodo).
Unita: altezza delle maiuscole H = 100, asse y verso l'alto, linea di base y = 0.
"""
import math
from shapely.geometry import LineString, Polygon, box, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

H = 100.0      # altezza maiuscole e ascendenti
X = 70.0       # altezza della x
OV = 1.6       # overshoot ottico delle forme tonde


def arc(cx, cy, rx, ry, a0, a1, n=48):
    """punti su un arco ellittico da a0 ad a1 (gradi, verso antiorario se a1>a0)."""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return pts


def stroke(pts, w, closed=False):
    if closed:
        ring = LineString(pts + [pts[0]])
        return ring.buffer(w / 2, cap_style='flat', join_style='round', quad_segs=24)
    return LineString(pts).buffer(w / 2, cap_style='flat', join_style='mitre', mitre_limit=10, quad_segs=24)


def stadium_path(x0, x1, y0, y1, r):
    """centerline di un rettangolo arrotondato (raggio r) in senso antiorario, partendo dal lato destro in basso"""
    pts = []
    pts += arc(x1 - r, y0 + r, r, r, -90, 0)
    pts += arc(x1 - r, y1 - r, r, r, 0, 90)
    pts += arc(x0 + r, y1 - r, r, r, 90, 180)
    pts += arc(x0 + r, y0 + r, r, r, 180, 270)
    return pts


# lettere
# ogni funzione ritorna (geometria, avanzamento)

def g_A(w, s, width=72.0, bar=30.0, apex=None):
    """A maiuscola: apice tagliato in piano all'altezza H, traversa a quota bar (asse).
    Ritorna la geometria allineata con il piede sinistro a x=0 e l'avanzamento reale."""
    hw = width / 2
    top = H + (apex if apex is not None else s * 0.9)
    # le aste si prolungano sotto la linea di base con la stessa pendenza, poi si tagliano in piano
    k = 20.0 / top
    legs = LineString([(-hw * k, -20), (hw, top), (width + hw * k, -20)]).buffer(
        s / 2, cap_style='flat', join_style='mitre', mitre_limit=20)
    crossbar = box(-50, bar - s * 0.42, width + 50, bar + s * 0.42)
    cb = crossbar.intersection(legs.convex_hull)
    g = unary_union([legs, cb]).intersection(box(-100, 0, width + 100, H))
    minx, _, maxx, _ = g.bounds
    g = affinity.translate(g, -minx, 0)
    return g, maxx - minx


def g_b(w, s, bw=56.0, r=None):
    """b: asta + occhiello a stadio sulla destra"""
    r = r if r is not None else (bw - s) / 2 * 0.98
    stem = box(0, 0, s, H)
    x0, x1 = s / 2, bw - s / 2
    y0, y1 = s / 2 - OV, X - s / 2 + OV
    bowl = stroke(stadium_path(x0, x1, y0, y1, min(r, (x1 - x0) / 2, (y1 - y0) / 2)), s, closed=True)
    # occhiello: dalla parte dell'asta lo raddrizziamo
    g = unary_union([stem, bowl])
    g = g.intersection(box(0, -OV - 1, bw + 5, H))
    # niente sporgenze sotto l'asta: l'overshoot vale solo per la parte tonda
    g = g.difference(box(-1, -OV - 2, s + 0.5, 0))
    return g, bw


def g_a(w, s, bw=56.0):
    """a a un piano, speculare di b senza ascendente: occhiello + asta a destra"""
    g, adv = g_b(w, s, bw)
    g = g.intersection(box(-5, -10, bw + 10, X + OV))
    g = affinity.scale(g, xfact=-1, yfact=1, origin=(bw / 2, 0))
    return g, bw


def g_r(w, s, rw=36.0):
    """r: asta + spalla che finisce con taglio verticale"""
    stem = box(0, 0, s, X)
    r = (rw - s / 2)
    y_top = X - s / 2 + OV
    # spalla: arco da sinistra (sull'asta) verso destra in alto
    cx = s / 2 + r
    ry = r * 0.92
    pts = arc(cx, y_top - ry, r, ry, 180, 90)
    pts.append((rw + 2, y_top))
    sh = LineString(pts).buffer(s / 2, cap_style='flat', join_style='round', quad_segs=24)
    g = unary_union([stem, sh]).intersection(box(0, 0, rw, X + OV))
    return g, rw


def g_R(w, s, rw=62.0, bowl_bottom=46.0):
    stem = box(0, 0, s, H)
    yt = H - s / 2
    yb = bowl_bottom
    r = (yt - yb) / 2
    x_end = rw - s / 2 - r * 0.0
    pts = [(s / 2, yt), (rw - s / 2 - r, yt)]
    pts += arc(rw - s / 2 - r, (yt + yb) / 2, r, r, 90, -90)
    pts.append((s / 2, yb))
    bowl = LineString(pts).buffer(s / 2, cap_style='flat', join_style='mitre')
    # gamba: dal punto di attacco dell'occhiello alla base destra
    attach = (rw - s / 2 - r * 1.05, yb)
    leg = LineString([attach, (rw - s * 0.05, -30)]).buffer(s / 2, cap_style='flat')
    g = unary_union([stem, bowl, leg]).intersection(box(0, 0, rw + 2, H))
    return g, rw + 1


def g_o(w, s, ow=58.0):
    x0, x1 = s / 2, ow - s / 2
    y0, y1 = s / 2 - OV, X - s / 2 + OV
    r = (x1 - x0) / 2
    g = stroke(stadium_path(x0, x1, y0, y1, r), s, closed=True)
    return g, ow


def g_c(w, s, cw=52.0, open_h=None):
    x0, x1 = s / 2, cw - s / 2 + 3
    y0, y1 = s / 2 - OV, X - s / 2 + OV
    r = (cw - s) / 2
    pts = []
    pts += arc(x0 + r, y1 - r, r, r, 22, 180)
    pts += arc(x0 + r, y0 + r, r, r, 180, 338)
    g = LineString(pts).buffer(s / 2, cap_style='flat', join_style='round', quad_segs=24)
    # tagli orizzontali dei terminali
    cut = box(x0 + r + 2, y0 + r + 4, cw + 20, y1 - r - 4)
    g = g.difference(cut)
    return g, cw


def g_t(w, s, tw=36.0, cross=None):
    stem_x = s / 2 + 6
    top = 90.0
    r = 16.0
    pts = [(stem_x, top), (stem_x, s / 2 - OV + r)]
    pts += arc(stem_x + r, s / 2 - OV + r, r, r, 180, 270)
    pts.append((tw + 1, s / 2 - OV))
    st = LineString(pts).buffer(s / 2, cap_style='flat', join_style='round', quad_segs=24)
    cb = box(0, X - s, tw, X)
    g = unary_union([st, cb]).intersection(box(0, -OV - 1, tw, top))
    return g, tw


def g_i(w, s):
    stem = box(0, 0, s, X)
    dot = box(0, H - s, s, H)
    return unary_union([stem, dot]), s


def g_s(w, s, sw=50.0):
    """s geometrica: due anse tangenti in centro, terminali tagliati in orizzontale"""
    x0, x1 = s / 2, sw - s / 2
    yb, yt = s / 2 - OV, X - s / 2 + OV
    ym = (yb + yt) / 2
    ru = (yt - ym) / 2           # raggio verticale ansa alta
    rl = (ym - yb) / 2
    rxu = (x1 - x0) / 2 - 0.5
    rxl = (x1 - x0) / 2
    cx = (x0 + x1) / 2
    up = arc(cx, ym + ru, rxu, ru, 15, 270, 80)
    lo = arc(cx, ym - rl, rxl, rl, 90, -165, 80)
    g = LineString(up + lo[1:]).buffer(s / 2, cap_style='flat', join_style='round', quad_segs=24)
    return g, sw


GLYPHS = {'A': g_A, 'b': g_b, 'a': g_a, 'r': g_r, 'R': g_R, 'o': g_o, 'c': g_c, 't': g_t, 'i': g_i, 's': g_s}


def to_path(geom, dx=0.0, dy=0.0, scale=1.0, flip_h=None, prec=2):
    """converte poligoni shapely in path SVG (y verso il basso). flip_h: altezza per il ribaltamento."""
    if geom.is_empty:
        return ''
    polys = [geom] if isinstance(geom, Polygon) else [p for p in getattr(geom, 'geoms', []) if isinstance(p, Polygon)]
    out = []
    fh = H if flip_h is None else flip_h

    def ring(coords):
        cs = list(coords)[:-1]
        parts = []
        for i, (x, y) in enumerate(cs):
            X_ = round(dx + x * scale, prec)
            Y_ = round(dy + (fh - y) * scale, prec)
            parts.append(('M' if i == 0 else 'L') + f'{X_:g} {Y_:g}')
        return ''.join(parts) + 'Z'

    for p in polys:
        p = p.simplify(0.02)
        out.append(ring(p.exterior.coords))
        for h in p.interiors:
            out.append(ring(h.coords))
    return ''.join(out)
