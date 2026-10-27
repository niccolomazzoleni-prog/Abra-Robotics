"""Genera ../logo/animazione.html con i tracciati del logotipo."""
import os, re
D = os.path.join(os.path.dirname(__file__), '..', 'logo')
svg = open(os.path.join(D, 'orizzontale.svg')).read()
paths = re.findall(r'<path fill="#1A2125" d="([^"]+)"', svg)
letters, tri = paths[0], paths[1]
import sys
sys.path.insert(0, os.path.dirname(__file__))
from build_logo import A_parts, H
from shapely.geometry import Polygon
vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
VW, VH = float(vb.group(1)), float(vb.group(2))
c = (VH - H) / 2
A, T, adv = A_parts(16.0)
polys = [A] if isinstance(A, Polygon) else list(A.geoms)
hole = [Polygon(p.interiors[0]) for p in polys if p.interiors][0]
pts = [(c + x, c + H - y) for x, y in list(hole.exterior.coords)[:-1]]
ys = [p[1] for p in pts]
top, bot = min(ys), max(ys)
shift = (c + H) - bot
counter_pts = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
cx = sum(p[0] for p in pts) / 3

html = r'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Riferimento A · logo animato</title>
<link rel="icon" href="favicon.svg">
<link rel="stylesheet" href="../assets/a.css">
<style>
  body{min-height:100vh;display:grid;place-items:center;background:var(--alluminio)}
  .palco{width:min(1100px,92vw)}
  svg{width:100%;height:auto;overflow:visible}
  .meta{display:flex;justify-content:space-between;color:var(--quota);margin-top:40px}
  /* ciclo di 6 s; tempi in multipli di 120 ms */
  .base{stroke:var(--quota);stroke-width:1;stroke-dasharray:900;stroke-dashoffset:900;animation:base 6s cubic-bezier(.2,0,0,1) infinite}
  .tacca{stroke:var(--quota);stroke-width:1;opacity:0;animation:tacca 6s linear infinite}
  .lettere{animation:compari 6s linear infinite}
  #wipe{animation:wipe 6s cubic-bezier(.4,0,.2,1) infinite}
  .copia{fill:none;stroke:var(--grafite);stroke-width:1.2;opacity:0;animation:copia 6s cubic-bezier(.2,0,0,1) infinite}
  .rif{fill:var(--grafite);opacity:0;animation:rif 6s steps(1,end) infinite}
  .quota-v line{stroke:var(--quota);stroke-width:1}
  .quota-v{opacity:0;animation:qv 6s linear infinite}
  .quota-v text,.lab{font:500 9px var(--f-etichetta);letter-spacing:.08em;fill:var(--quota)}
  .lab{opacity:0;animation:lab 6s linear infinite}
  @keyframes base{0%{stroke-dashoffset:900;opacity:1}10%{stroke-dashoffset:0}62%{opacity:1}70%,100%{stroke-dashoffset:0;opacity:0}}
  @keyframes tacca{0%,8%{opacity:0}10%,62%{opacity:1}70%,100%{opacity:0}}
  @keyframes wipe{0%,6%{width:0}26%,92%{width:900px}100%{width:900px}}
  @keyframes compari{0%,92%{opacity:1}98%,100%{opacity:0}}
  @keyframes qv{0%,28%{opacity:0}32%,48%{opacity:1}52%,100%{opacity:0}}
  @keyframes copia{0%,34%{opacity:0;transform:translateY(0)}38%{opacity:1;transform:translateY(0)}52%{opacity:1;transform:translateY(54.32px)}56%,100%{opacity:0;transform:translateY(54.32px)}}
  @keyframes rif{0%,54%{opacity:0}54.01%,92%{opacity:1}98%,100%{opacity:0}}
  @keyframes lab{0%,58%{opacity:0}62%,90%{opacity:1}96%,100%{opacity:0}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}.rif{opacity:1}.base,.tacca,.quota-v,.lab,.copia{display:none}}
</style>
</head>
<body>
<div class="palco">
  <svg viewBox="0 0 VW VH" role="img" aria-label="Abra Robotics, logo animato">
    <defs><clipPath id="c"><rect id="wipe" x="0" y="0" width="0" height="170"/></clipPath></defs>
    <line class="base" x1="20" y1="BASEY" x2="X2" y2="BASEY"/>
    
    <g class="lettere" clip-path="url(#c)"><path fill="#1A2125" d="LETTERS"/></g>
    <g class="quota-v">
      <line x1="12" y1="QTOP" x2="12" y2="QBOT"/><line x1="7" y1="QTOP" x2="17" y2="QTOP"/><line x1="7" y1="QBOT" x2="17" y2="QBOT"/>
      <text x="4" y="QMID" text-anchor="end">QLAB</text>
    </g>
    <polygon class="copia" points="COUNTER"/>
    <path class="rif" d="TRI"/>
    <text class="lab" x="CX" y="LABY" text-anchor="middle">A</text>
  </svg>
  <div class="meta et"><span>Riferimento A · logo animato, CSS e SVG</span><span class="num">ciclo 6,0 s · passo 120 ms</span></div>
</div>
</body>
</html>
'''
base = c + H
html = (html.replace('LETTERS', letters).replace('TRI', tri).replace('VW', f'{VW:g}').replace('VH', f'{VH:g}')
        .replace('COUNTER', counter_pts).replace('54.32', f'{shift:.2f}').replace('BASEY', f'{base:.2f}')
        .replace('QTOP', f'{top:.2f}').replace('QBOT', f'{bot:.2f}').replace('QMID', f'{(top+bot)/2+3:.2f}')
        .replace('QLAB', f'{bot-top:.1f}'.replace('.', ',')).replace('CX', f'{cx:.2f}').replace('LABY', f'{base+20:.2f}')
        .replace('X2', f'{VW-20:g}'))
open(os.path.join(D, 'animazione.html'), 'w').write(html)
print('ok')
