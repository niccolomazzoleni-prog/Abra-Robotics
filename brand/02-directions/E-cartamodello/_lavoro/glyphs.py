import sys,json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import RecordingPen
wght,wdth=float(sys.argv[1]),float(sys.argv[2]); text=sys.argv[3]
f=TTFont(sys.argv[4] if len(sys.argv)>4 else '/Users/niccolomazzoleni/Abra-Robotics-brand/brand/02-directions/E-cartamodello/fonts/BricolageGrotesque-VF.ttf')
inst=instantiateVariableFont(f,{'wght':wght,'wdth':wdth,'opsz':96})
gs=inst.getGlyphSet(); cmap=inst.getBestCmap()
out=[]
for ch in text:
    g=cmap[ord(ch)]; p=SVGPathPen(gs); gs[g].draw(p); r=RecordingPen(); gs[g].draw(r)
    out.append({'ch':ch,'glyph':g,'adv':gs[g].width,'d':p.getCommands(),'rec':r.value})
print(json.dumps(out))
