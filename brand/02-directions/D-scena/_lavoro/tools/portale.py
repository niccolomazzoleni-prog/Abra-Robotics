# Lettering v2 "abra" a portale: ogni occhiello è un arco scenico (tetto tondo, base piana)
# baseline y=100, occhio medio y=0, ascendente y=-ASC
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from geo import *
S=26; R=50; ASC=60; RI=23; BOT=76; GAP=11
def portale(cx):
    outer=U(disk(cx,50,R).intersection(rect(cx-R,-1,cx+R,50)), rect(cx-R,50,cx+R,100))
    counter=U(disk(cx,50,RI).intersection(rect(cx-RI,0,cx+RI,50)), rect(cx-RI,50,cx+RI,BOT))
    return outer.difference(counter)
def g_a(x): return U(portale(x+R), rect(x+2*R-S,0,x+2*R,100)), 2*R
def g_b(x): return U(portale(x+R), rect(x,-ASC,x+S,100)), 2*R
def g_r(x, arm=80, drop=50):
    cx=x+R
    ring=disk(cx,50,R).difference(disk(cx,50,RI))
    arc=ring.intersection(rect(x,-1,x+arm,drop))
    return U(rect(x,0,x+S,100),arc), arm
def abra(x0=0):
    x=x0; gs=[]
    for fn in (g_a,g_b,g_r,g_a):
        g,w=fn(x); gs.append(g); x+=w+GAP
    return U(*gs), x-GAP-x0
def monogramma():
    g,w=g_a(0); return g,w
