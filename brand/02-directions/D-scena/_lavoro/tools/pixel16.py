# Favicon "ab" disegnata a pixel su griglia 16 x 16: PNG 16 e 32 e favicon.svg a rettangoli
from PIL import Image
import os
OUT=os.path.join(os.path.dirname(__file__),'..','..','logo')
G='''................
................
................
........XX......
........XX......
........XX......
..XXXXX.XXXXX...
.XXXXXX.XXXXXX..
.XX..XX.XX..XX..
.XX..XX.XX..XX..
.XX..XX.XX..XX..
.XX..XX.XX..XX..
.XXXXXX.XXXXXX..
.XXXXXX.XXXXXX..
................
................'''.split()
MAG=(214,0,111,255); CAR=(250,250,247,255)
im=Image.new('RGBA',(16,16),MAG)
rects=[]
for y,row in enumerate(G):
    for x,c in enumerate(row):
        if c=='X': im.putpixel((x,y),CAR); rects.append(f'<rect x="{x}" y="{y}" width="1" height="1"/>')
im.save(os.path.join(OUT,'favicon-16.png'))
im.resize((32,32),Image.NEAREST).save(os.path.join(OUT,'favicon-32.png'))
im.resize((96,96),Image.NEAREST).save(os.path.join(OUT,'favicon-16-x6.png'))
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges" role="img" aria-label="Abra, favicon">\n<title>Abra, favicon</title>\n<rect width="16" height="16" fill="#D6006F"/>\n<g fill="#FAFAF7">'+''.join(rects)+'</g>\n</svg>\n'
open(os.path.join(OUT,'favicon.svg'),'w').write(svg)
