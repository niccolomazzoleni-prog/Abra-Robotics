const fs=require('fs'),path=require('path');const g=require('./geo3.js');const {H,M}=g;
const f=v=>+v.toFixed(1);const sh=(d,dx)=>d.replace(/(-?[\d.]+) (-?[\d.]+)/g,(m,p,q)=>`${f(+p+dx)} ${q}`);
const a=g.aLeft(0,g.A_OPT), b=g.bBowl(0), st=g.asta(0,M.asc);
let x=b.right+26; const r=g.rLetter(x); x=r.right+50; const a2=g.aAlone(0); const dx=x-a2.left; const end=a2.right+dx;
const vb=`${f(a.left-30)} ${M.asc-60} ${f(end-a.left+60)} ${H-M.asc+120}`;
const html=`<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Abra Robotics, logo animato (direzione Cartamodello, v3)</title>
<link rel="icon" href="favicon-16.svg">
<style>
  @font-face{font-family:"Abra Bricolage";src:url(../fonts/BricolageGrotesque-Testo.ttf);font-weight:400}
  @font-face{font-family:"Abra Bricolage";src:url(../fonts/BricolageGrotesque-Etichetta.ttf);font-weight:600;font-stretch:75%}
  html,body{margin:0;height:100%;background:#F7F6F2}
  body{display:grid;place-items:center;font-family:"Abra Bricolage",system-ui,sans-serif;color:#2F3337}
  .scena{width:min(900px,86vw)}
  svg{width:100%;height:auto;display:block;overflow:visible}
  /* 1. l'asta si taglia dal basso: è la linea di piega */
  .asta{clip-path:inset(100% 0 0 0);animation:taglio .6s cubic-bezier(.2,.7,.2,1) .1s forwards}
  @keyframes taglio{to{clip-path:inset(0 0 0 0)}}
  /* 2. la tacca a V si incide in cima all'asta */
  .tacca{fill:#8BB8E8;opacity:0;animation:appare .3s ease .7s forwards}
  /* 3. la b e la a si aprono dalla piega, come un pezzo tagliato in doppio */
  .b{clip-path:inset(0 100% 0 0);animation:apri .6s cubic-bezier(.2,.7,.2,1) 1s forwards}
  .a{clip-path:inset(0 0 0 100%);animation:apri .6s cubic-bezier(.2,.7,.2,1) 1s forwards}
  @keyframes apri{to{clip-path:inset(0 0 0 0)}}
  @keyframes appare{to{opacity:1}}
  /* 4. r e a salgono */
  .l{transform:translateY(60px);opacity:0;animation:sale .5s cubic-bezier(.2,.7,.2,1) forwards}
  .l0{animation-delay:1.7s}.l1{animation-delay:1.8s}
  @keyframes sale{to{transform:none;opacity:1}}
  button{margin-top:40px;font:600 13px/1 "Abra Bricolage";font-stretch:75%;letter-spacing:.09em;text-transform:uppercase;background:none;border:1.5px solid #2F3337;color:#2F3337;padding:10px 14px 9px;cursor:pointer}
  p{font-size:14px;color:#5E6266;max-width:640px;line-height:1.5}
  @media (prefers-reduced-motion:reduce){.asta,.b,.a,.l,.tacca{animation:none!important;clip-path:none;opacity:1;transform:none}.tacca{display:none}}
</style>
</head>
<body>
<div class="scena">
  <svg id="logo" viewBox="${vb}" role="img" aria-label="abra">
    <g fill="#2F3337">
      <path class="tacca" d="M${f(M.sw/2-60)} ${M.asc-6} L${f(M.sw/2)} ${M.asc+70} L${f(M.sw/2+60)} ${M.asc-6} Z"/>
      <path class="asta" d="${st}"/>
      <path class="b" d="${b.d}"/>
      <path class="a" d="${a.d}"/>
      <path class="l l0" d="${r.d}"/>
      <path class="l l1" d="${sh(a2.d,dx)}"/>
    </g>
  </svg>
  <button type="button" id="ripeti">Ripeti</button>
  <p>L'asta comune si taglia dal basso ed è la linea di piega; in cima compare la tacca in gesso blu; la b e la a si aprono dalla piega come un pezzo tagliato in doppio; poi arrivano r e a. Durata 2,3 secondi. Con la riduzione del movimento il logotipo appare fermo.</p>
</div>
<script>
document.getElementById('ripeti').addEventListener('click',()=>{const s=document.getElementById('logo');const c=s.cloneNode(true);s.replaceWith(c);});
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(__dirname,'..','logo','animazione.html'),html);console.log('ok');
