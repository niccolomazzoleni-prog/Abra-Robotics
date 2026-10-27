const fs=require('fs'),path=require('path');const {A2,letters,H}=require('./geo2.js');
const f=v=>+v.toFixed(1);
const P={by:400,t:86,len:150};
const g=A2(P); const L=letters({rt:1.75});
function shift(d,dx){return d.replace(/(-?[\d.]+) (-?[\d.]+)/g,(m,a,b)=>`${f(+a+dx)} ${b}`);}
// layout: symbol A with tail, then b r a after the tail
let x=g.W+30; const gaps={b:44,r:52,a:0}; let bra='';
['b','r','a'].forEach((c,i)=>{bra+=`<path class="l l${i}" d="${shift(L[c].d,x)}"/>`;x+=L[c].adv+gaps[c];});
const vb=`-30 -80 ${f(x+60)} 800`;
const html=`<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Abra Robotics, logo animato (direzione Cartamodello, v2)</title>
<link rel="icon" href="favicon-16.svg">
<style>
  :root{--tela:#ECE6D8;--flanella:#2F3337;--gessoblu:#8FB0E0;--segno:#2F5D9E}
  @font-face{font-family:"Abra Bricolage";src:url(../fonts/BricolageGrotesque-Testo.ttf);font-weight:400}
  @font-face{font-family:"Abra Bricolage";src:url(../fonts/BricolageGrotesque-Etichetta.ttf);font-weight:600;font-stretch:75%}
  html,body{margin:0;height:100%;background:var(--tela)}
  body{display:grid;place-items:center;font-family:"Abra Bricolage",system-ui,sans-serif;color:var(--flanella)}
  .scena{width:min(1000px,86vw)}
  svg{width:100%;height:auto;display:block;overflow:visible}
  /* 1. le gambe della A si tagliano dal basso, come un pezzo di carta */
  .gambe{clip-path:inset(100% 0 0 0);animation:taglio .7s cubic-bezier(.2,.7,.2,1) .1s forwards}
  @keyframes taglio{to{clip-path:inset(0 0 0 0)}}
  /* 2. la traversa si cuce da sinistra a destra: e sempre piena, mai tratteggiata */
  .traversa{clip-path:inset(0 100% 0 0);animation:cuci .55s cubic-bezier(.45,0,.2,1) .8s forwards}
  @keyframes cuci{to{clip-path:inset(0 0 0 0)}}
  /* 3. il filo esce dalla gamba destra, in gesso blu */
  .filo{fill:var(--segno);clip-path:inset(0 100% 0 0);animation:cuci .4s cubic-bezier(.2,.7,.2,1) 1.3s forwards, entra .35s ease-in 2.1s forwards}
  @keyframes entra{from{clip-path:inset(0 0 0 0)}to{clip-path:inset(0 0 0 100%)}}
  /* 4. b, r, a salgono una alla volta */
  .l{transform:translateY(60px);opacity:0;animation:sale .5s cubic-bezier(.2,.7,.2,1) forwards}
  .l0{animation-delay:2.2s}.l1{animation-delay:2.3s}.l2{animation-delay:2.4s}
  @keyframes sale{to{transform:none;opacity:1}}
  button{margin-top:40px;font:600 13px/1 "Abra Bricolage";font-stretch:75%;letter-spacing:.09em;text-transform:uppercase;background:none;border:1.5px solid var(--flanella);color:var(--flanella);padding:10px 14px 9px;cursor:pointer}
  p{font-size:14px;color:#62666A;max-width:640px;line-height:1.5}
  @media (prefers-reduced-motion:reduce){.gambe,.traversa,.l{animation:none!important;clip-path:none;opacity:1;transform:none}.filo{display:none}}
</style>
</head>
<body>
<div class="scena">
  <svg id="logo" viewBox="${vb}" role="img" aria-label="Abra">
    <g fill="#2F3337">
      <path class="gambe" d="${g.legs}"/>
      <path class="traversa" d="${g.bar}"/>
      <path class="filo" d="${g.stitch}"/>
      ${bra}
    </g>
  </svg>
  <button type="button" id="ripeti">Ripeti</button>
  <p>La A si taglia come un pezzo di carta, la traversa si cuce da sinistra a destra e il filo esce dalla gamba destra in gesso blu; poi il filo rientra e arrivano le lettere b, r, a. Durata 2,9 secondi. Con la riduzione del movimento attiva il logo appare fermo.</p>
</div>
<script>
document.getElementById('ripeti').addEventListener('click',()=>{const s=document.getElementById('logo');const c=s.cloneNode(true);s.replaceWith(c);});
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(__dirname,'..','logo','animazione.html'),html);console.log('ok');
