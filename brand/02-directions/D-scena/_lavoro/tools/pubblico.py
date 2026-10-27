# Sagome del pubblico (testa e spalle) in SVG, disegnate con primitive: nessuna foto di persone
import random
def persona(x,base,s,col):
    hw,hh=24*s,30*s; sw,sh=78*s,118*s
    top=base-sh
    head=f'<ellipse cx="{x:.1f}" cy="{top-hh*0.85:.1f}" rx="{hw:.1f}" ry="{hh:.1f}" fill="{col}"/>'
    neck=f'<rect x="{x-10*s:.1f}" y="{top-hh*0.3:.1f}" width="{20*s:.1f}" height="{hh*0.5:.1f}" fill="{col}"/>'
    body=(f'<path d="M{x-sw:.1f} {base:.1f}V{top+36*s:.1f}Q{x-sw:.1f} {top:.1f} {x-sw+42*s:.1f} {top:.1f}'
          f'H{x+sw-42*s:.1f}Q{x+sw:.1f} {top:.1f} {x+sw:.1f} {top+36*s:.1f}V{base:.1f}Z" fill="{col}"/>')
    return head+neck+body
def folla(width,height,rows,seed=3):
    random.seed(seed); out=[]
    for y,s,col,n in rows:
        for j in range(n):
            x=(j+0.5+random.uniform(-0.22,0.22))*width/n
            out.append(persona(x,y,s*random.uniform(0.92,1.06),col))
    return f'<svg viewBox="0 0 {width} {height}" preserveAspectRatio="none" aria-hidden="true">'+''.join(out)+'</svg>'
