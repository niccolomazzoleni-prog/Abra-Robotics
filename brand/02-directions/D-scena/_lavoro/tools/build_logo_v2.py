# Marchio v2: logotipo "abra" a portali disegnato a mano + descrittore ROBOTICS in tracciati
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from portale import *
from descrittore import text
OUT=os.path.join(os.path.dirname(__file__),'..','..','logo')
GRAF='#202124'; MAG='#D6006F'; CARTA='#FAFAF7'
EV=' fill-rule="evenodd"'
def p(d,c,ev=True): return f'<path fill="{c}"{EV if ev else ""} d="{d}"/>'
def svg(vb,body,t): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{t}">\n<title>{t}</title>\n{body}\n</svg>\n'
def save(n,s): open(os.path.join(OUT,n),'w').write(s); print('ok',n)
def fv(v): return ('%.1f'%v).rstrip('0').rstrip('.')
for f_ in os.listdir(OUT):
    if f_.endswith('.svg') and f_!='favicon.svg': os.remove(os.path.join(OUT,f_))
g,w=abra(); D=topath(g)
M=24
# logotipo
vbL=f"{-M} {-ASC-M} {fv(w+2*M)} {fv(100+ASC+2*M)}"
save('logotipo.svg',svg(vbL,p(D,GRAF),'abra'))
save('logotipo-negativo.svg',svg(vbL,p(D,CARTA),'abra'))
# orizzontale: descrittore alto quanto 0,34 dell'occhio medio, allineato alla base
size=44/0.73  # descrittore alto 0,44 dell occhio medio
rd,radv,cap=text('ROBOTICS',size=size,track=150,x0=w+44,y0=100)
tot=w+44+radv
vbH=f"{-M} {-ASC-M} {fv(tot+2*M)} {fv(100+ASC+2*M)}"
save('orizzontale.svg',svg(vbH,p(D,GRAF)+p(rd,MAG,False),'abra Robotics'))
save('orizzontale-negativo.svg',svg(vbH,p(D,CARTA)+p(rd,CARTA,False),'abra Robotics'))
save('mono-positivo.svg',svg(vbH,p(D,GRAF)+p(rd,GRAF,False),'abra Robotics'))
save('mono-negativo.svg',svg(vbH,p(D,CARTA)+p(rd,CARTA,False),'abra Robotics'))
# verticale: descrittore giustificato sotto la parola
_,adv0,_=text('ROBOTICS',size=size,track=0)
tr=(w-adv0)/7/size*1000
rd2,_,_=text('ROBOTICS',size=size,track=tr,x0=0,y0=100+30+cap)
vbV=f"{-M} {-ASC-M} {fv(w+2*M)} {fv(100+ASC+30+cap+2*M)}"
save('verticale.svg',svg(vbV,p(D,GRAF)+p(rd2,MAG,False),'abra Robotics'))
save('verticale-negativo.svg',svg(vbV,p(D,CARTA)+p(rd2,CARTA,False),'abra Robotics'))
# simbolo: legatura visiva "ab", due portali (da a a b)
ga,wa=g_a(0); gb,wb=g_b(wa+GAP); gab=U(ga,gb); wab=wa+GAP+wb; DAB=topath(gab)
vbS=f"{-M} {-ASC-M} {fv(wab+2*M)} {fv(100+ASC+2*M)}"
save('simbolo.svg',svg(vbS,p(DAB,GRAF),'ab, simbolo di Abra'))
save('simbolo-negativo.svg',svg(vbS,p(DAB,CARTA),'ab, simbolo di Abra'))
# monogramma su tessera magenta (avatar)
H=100+ASC; k=50/H; tx=50-wab*k/2; ty=50-H*k/2+ASC*k
save('monogramma.svg',svg("0 0 100 100",f'<rect width="100" height="100" fill="{MAG}"/>'+p(topath(gab,dx=tx,dy=ty,sx=k,sy=k),CARTA),'Abra, monogramma'))
