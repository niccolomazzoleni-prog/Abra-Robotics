"""Genera ../logo/animazione.html: la legatura Ab si costruisce sulla squadra, poi compare il resto del logotipo."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_logo import word, CLEAR, H, to_path, g_Ab, SB
from glyphs import affinity, unary_union, box

D = os.path.join(os.path.dirname(__file__), '..', 'logo')
s = 16.0
letters, ww = word('Abra Robotics', s)
Ab, adv = g_Ab(None, s)
rest = letters.difference(box(-1, -5, adv + 0.5, H + 5))
c = CLEAR
VW, VH = ww + 2 * c, H + 2 * c
stem_poly = Ab.intersection(box(adv - 56, -5, adv + 1, H + 5))   # asta comune e pancia della b
diag_poly = Ab.difference(box(adv - 56, -5, adv + 1, H + 5))     # diagonale e traversa
P = lambda g: to_path(g, dx=c, dy=c, flip_h=H)
base = c + H
sx = c + adv - 56  # bordo sinistro dell'asta comune

html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>In squadra · logo animato</title>
<link rel="icon" href="favicon.svg">
<link rel="stylesheet" href="../assets/a.css">
<style>
  body{{min-height:100vh;display:grid;place-items:center;background:var(--alluminio)}}
  .palco{{width:min(1100px,92vw)}}
  svg{{width:100%;height:auto;overflow:visible}}
  .meta{{display:flex;justify-content:space-between;color:var(--quota);margin-top:40px}}
  /* ciclo di 6 s; tempi in multipli di 120 ms */
  .base{{stroke:var(--quota);stroke-width:1;stroke-dasharray:900;stroke-dashoffset:900;animation:base 6s cubic-bezier(.2,0,0,1) infinite}}
  #cs{{animation:sale 6s cubic-bezier(.2,0,0,1) infinite}}
  #cd{{animation:diag 6s cubic-bezier(.2,0,0,1) infinite}}
  #cr{{animation:resto 6s cubic-bezier(.4,0,.2,1) infinite}}
  .ang{{fill:none;stroke:var(--verde);stroke-width:1.4;opacity:0;animation:ang 6s steps(1,end) infinite}}
  .lab{{font:500 9px var(--f-etichetta);letter-spacing:.08em;fill:var(--verde);opacity:0;animation:ang 6s steps(1,end) infinite}}
  .tutto{{animation:esce 6s linear infinite}}
  @keyframes base{{0%{{stroke-dashoffset:900;opacity:1}}10%{{stroke-dashoffset:0}}70%{{opacity:1}}76%,100%{{stroke-dashoffset:0;opacity:0}}}}
  @keyframes sale{{0%,8%{{height:0;y:{base:.2f}px}}20%,100%{{height:{H+10:.0f}px;y:{c-5:.2f}px}}}}
  @keyframes diag{{0%,20%{{width:0}}36%,100%{{width:{adv:.0f}px}}}}
  @keyframes ang{{0%,36%{{opacity:0}}36.01%,68%{{opacity:1}}68.01%,100%{{opacity:0}}}}
  @keyframes resto{{0%,40%{{width:0}}62%,100%{{width:{VW:.0f}px}}}}
  @keyframes esce{{0%,92%{{opacity:1}}98%,100%{{opacity:0}}}}
  @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}#cs{{height:{H+10:.0f}px;y:{c-5:.2f}px}}#cd{{width:{adv:.0f}px}}#cr{{width:{VW:.0f}px}}.base,.ang,.lab{{display:none}}}}
</style>
</head>
<body>
<div class="palco">
  <svg viewBox="0 0 {VW:.1f} {VH:.1f}" role="img" aria-label="Abra Robotics, logo animato">
    <defs>
      <clipPath id="ks"><rect id="cs" x="{sx-1:.2f}" y="{base:.2f}" width="{56+s+2:.0f}" height="0"/></clipPath>
      <clipPath id="kd"><rect id="cd" x="{c:.2f}" y="0" width="0" height="{VH:.0f}"/></clipPath>
      <clipPath id="kr"><rect id="cr" x="{c+adv:.2f}" y="0" width="0" height="{VH:.0f}"/></clipPath>
    </defs>
    <line class="base" x1="8" y1="{base:.2f}" x2="{VW-8:.1f}" y2="{base:.2f}"/>
    <g class="tutto" fill="#1A2125">
      <path clip-path="url(#ks)" d="{P(stem_poly)}"/>
      <path clip-path="url(#kd)" d="{P(diag_poly)}"/>
      <path clip-path="url(#kr)" d="{P(rest)}"/>
    </g>
    <path class="ang" d="M{sx-9:.2f} {base:.2f}v-9h9"/>
    <text class="lab" x="{sx-34:.2f}" y="{base-13:.2f}">90°</text>
  </svg>
  <div class="meta et"><span>In squadra · logo animato, CSS e SVG</span><span class="num">ciclo 6,0 s · passo 120 ms</span></div>
</div>
</body>
</html>
'''
open(os.path.join(D, 'animazione.html'), 'w').write(html)
print('ok')
