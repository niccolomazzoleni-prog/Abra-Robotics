# A-scena in unità assolute. Baseline y=H (coordinate SVG verso il basso), apice y=0. Origine x=0.
def f(v): return ('%.2f'%v).rstrip('0').rstrip('.')
def A(W=100,H=100,apex=26,t=24,c1=60,c2=73,floor=77.5,gap=4.5,x0=0,y0=0):
    """parametri apex,t,c1,c2,floor,gap in percentuale della box (apex,t,gap su W; c1,c2,floor su H)"""
    sx=W/100; sy=H/100
    ol0=50-apex/2; s=(ol0-0)/100.0
    xol=lambda y: ol0-s*y
    xil=lambda y: xol(y)+t
    xir=lambda y: 100-xil(y)
    xor=lambda y: 100-xol(y)
    ya=((ol0+t)-50)/s
    P=lambda x,y: f"{f(x0+x*sx)} {f(y0+y*sy)}"
    outer=f"M{P(ol0,0)}L{P(100-ol0,0)}L{P(100,100)}L{P(xir(100),100)}L{P(xir(c2),c2)}L{P(xil(c2),c2)}L{P(xil(100),100)}L{P(0,100)}Z"
    counter=f"M{P(50,ya)}L{P(xir(c1),c1)}L{P(xil(c1),c1)}Z"
    g=gap
    fl=f"M{P(xil(floor)+g,floor)}L{P(xir(floor)-g,floor)}L{P(xir(100)-g,100)}L{P(xil(100)+g,100)}Z"
    return outer+counter, fl
