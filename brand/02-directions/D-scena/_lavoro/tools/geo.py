# Primitive geometriche per il lettering v2 (shapely), export in path SVG
from shapely.geometry import Point, Polygon, box, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
import math
def ring(cx,cy,ro,ri,res=96):
    return Point(cx,cy).buffer(ro,resolution=res).difference(Point(cx,cy).buffer(ri,resolution=res))
def disk(cx,cy,r,res=96): return Point(cx,cy).buffer(r,resolution=res)
def rect(x0,y0,x1,y1): return box(min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1))
def poly(*pts): return Polygon(pts)
def U(*g): return unary_union(g)
def f(v): return ('%.2f'%v).rstrip('0').rstrip('.')
def topath(g,dx=0,dy=0,sx=1,sy=1):
    polys=[g] if g.geom_type=='Polygon' else list(g.geoms)
    out=[]
    for p in polys:
        for r in [p.exterior]+list(p.interiors):
            c=list(r.coords)[:-1]
            out.append('M'+'L'.join(f"{f(x*sx+dx)} {f(y*sy+dy)}" for x,y in c)+'Z')
    return ''.join(out)
