# Testo in tracciati da un TTF statico (solo per il descrittore "ROBOTICS")
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
FD=os.path.join(os.path.dirname(__file__),'..','..','font')
def text(s,font='ArchivoExpanded-SemiBold.ttf',size=100,track=0,x0=0,y0=0):
    f=TTFont(os.path.join(FD,font)); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; x=x0; out=[]
    for i,ch in enumerate(s):
        g=gs[cmap[ord(ch)]]
        pen=SVGPathPen(gs,lambda v:('%.2f'%v).rstrip('0').rstrip('.'))
        g.draw(TransformPen(pen,(sc,0,0,-sc,x,y0))); out.append(pen.getCommands())
        x+=g.width*sc+(track*size/1000 if i<len(s)-1 else 0)
    return ''.join(out), x-x0, f['OS/2'].sCapHeight*sc
