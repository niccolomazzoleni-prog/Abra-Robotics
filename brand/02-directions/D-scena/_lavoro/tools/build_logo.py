# Genera gli SVG del marchio D "Prova generale" in ../../logo
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from textpath import text
from amark import A
OUT=os.path.join(os.path.dirname(__file__),'..','..','logo')
VEL='#3A1915'; LUCE='#E9AE45'; STUCCO='#F3ECDF'
CAP=687; XH=526
WD,WG=85,800
AP=dict(apex=24,t=27,c1=58,c2=71,floor=76,gap=5.2)
AW=650
def wordmark(x0=0, y0=0):
    """'Abra' con baseline y0, ritorna (d_scuro, d_luce, larghezza)"""
    a,fl=A(W=AW,H=CAP,x0=x0,y0=y0-CAP,**AP)
    d,adv=text('bra',WD,WG,1000,0,{'br':-4,'ra':-6},x0=x0+AW-6,y0=y0)
    return a+d, fl, AW-6+adv
def robotics(size, track, x0, y0):
    return text('ROBOTICS',125,600,size,track,x0=x0,y0=y0)
def svg(vb, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">\n<title>{title}</title>\n{body}\n</svg>\n'
EV=' fill-rule="evenodd"'
def p(d,c,rule=False): return '<path fill="'+c+'"'+(EV if rule else '')+' d="'+d+'"/>'
def save(n,s):
    open(os.path.join(OUT,n),'w').write(s); print('ok',n)

# orizzontale: "Abra" 85/800 con la A di scena + "Robotics" 85/450, stessa linea di base e stesso corpo
dk,fl,w=wordmark(0,0)
GAP=230
rd,radv=text('Robotics',WD,450,1000,0,x0=w+GAP,y0=0)
total=w+GAP+radv
M=70
def horiz(cd,cl):
    return p(dk,cd,True)+p(fl,cl)+p(rd,cd)
vbH=f"{-M} {-724-M} {total+2*M:.0f} {724+12+2*M}"
save('orizzontale.svg',svg(vbH,horiz(VEL,LUCE),'Abra Robotics'))
save('mono-positivo.svg',svg(vbH,horiz(VEL,VEL),'Abra Robotics'))
save('mono-negativo.svg',svg(vbH,horiz(STUCCO,STUCCO),'Abra Robotics'))
save('orizzontale-negativo.svg',svg(vbH,horiz(STUCCO,LUCE),'Abra Robotics'))
# verticale: Abra sopra Robotics, allineati a sinistra
LS=900
rd2,radv2=text('Robotics',WD,450,1000,0,x0=0,y0=LS)
W2=max(w,radv2)
vbV=f"{-M} {-724-M} {W2+2*M:.0f} {724+LS+12+2*M}"
save('verticale.svg',svg(vbV,p(dk,VEL,True)+p(fl,LUCE)+p(rd2,VEL),'Abra Robotics'))
save('verticale-negativo.svg',svg(vbV,p(dk,STUCCO,True)+p(fl,LUCE)+p(rd2,STUCCO),'Abra Robotics'))
# simbolo
a,f2=A(W=100*AW/CAP,H=100,**AP)
SW=100*AW/CAP
vbS=f"{-8:.2f} -8 {SW+16:.2f} 116"
save('simbolo.svg',svg(vbS,p(a,VEL,True)+p(f2,LUCE),'Abra, simbolo'))
# monogramma: simbolo su quadrato velluto, versione per piccoli formati (fughe allargate)
SMALL=dict(apex=26,t=28,c1=56,c2=68,floor=75,gap=8)
a3,f3=A(W=62*AW/CAP,H=62,x0=50-31*AW/CAP,y0=19,**SMALL)
save('monogramma.svg',svg("0 0 100 100",f'<rect width="100" height="100" fill="{VEL}"/>'+p(a3,STUCCO,True)+p(f3,LUCE),'Abra, monogramma'))
a4,f4=A(W=100*AW/CAP,H=100,**SMALL)
save('simbolo-piccolo.svg',svg(vbS,p(a4,VEL,True)+p(f4,LUCE),'Abra, simbolo per piccoli formati'))
