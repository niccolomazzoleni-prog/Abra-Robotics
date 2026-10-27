# Converte testo Archivo (istanza variabile) in path SVG, con tracking e kerning manuale
import sys, functools
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
VF='/Users/niccolomazzoleni/Abra-Robotics-brand/brand/02-directions/D-scena/font/Archivo-VF.ttf'
@functools.lru_cache(None)
def inst(wdth,wght):
    f=TTFont(VF); return instantiateVariableFont(f,{'wdth':wdth,'wght':wght},inplace=False)
def metrics(wdth,wght):
    f=inst(wdth,wght); os2=f['OS/2']; return dict(upm=f['head'].unitsPerEm,cap=os2.sCapHeight,x=os2.sxHeight)
def text(s,wdth,wght,size=100,track=0,kern=None,x0=0,y0=0):
    """ritorna (d, advance) con baseline a y0; size = em in unità SVG; track in em/1000"""
    f=inst(wdth,wght); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; x=x0; parts=[]
    kern=kern or {}
    for i,ch in enumerate(s):
        gn=cmap[ord(ch)]; g=gs[gn]
        pen=SVGPathPen(gs, lambda v: ('%.2f'%v).rstrip('0').rstrip('.'))
        tp=TransformPen(pen,(sc,0,0,-sc,x,y0)); g.draw(tp)
        parts.append(pen.getCommands())
        x+=g.width*sc + track*size/1000
        if i+1<len(s): x+=kern.get(ch+s[i+1],0)*size/1000
    return ''.join(parts), x-x0
def bounds(s,wdth,wght,size=100):
    f=inst(wdth,wght); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    out=[]
    for ch in s:
        bp=BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp); out.append((ch,bp.bounds,gs[cmap[ord(ch)]].width))
    return out
if __name__=='__main__':
    print(metrics(100,800)); print(bounds('Abra',100,800))
