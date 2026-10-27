// Geometria v3 del marchio Abra (direzione E): logotipo "abra" minuscolo disegnato,
// simbolo "ab" in legatura: la a e la b condividono l'asta, che fa da linea di piega del cartamodello.
const H=660;
const f=v=>+v.toFixed(1);
function poly(pts){return 'M'+pts.map(p=>f(p[0])+' '+f(p[1])).join(' L')+' Z';}
function se(cx,cy,a,b,n,t){const c=Math.cos(t),s=Math.sin(t);return [cx+a*Math.sign(c)*Math.pow(Math.abs(c),2/n), cy+b*Math.sign(s)*Math.pow(Math.abs(s),2/n)];}
function ellipse(cx,cy,a,b,n,rev,N=180){const p=[];for(let k=0;k<N;k++){const t=(rev?-1:1)*2*Math.PI*k/N;p.push(se(cx,cy,a,b,n,t));}return poly(p);}
// arco di anello da t0 a t1; il terminale in t1 è tagliato orizzontale (stessa y fuori e dentro)
function arc(cx,cy,ao,bo,ai,bi,n,t0,t1,N=90,ni){ni=ni||n;
  const o=[];for(let k=0;k<=N;k++)o.push(se(cx,cy,ao,bo,n,t0+(t1-t0)*k/N));
  const ey=o[o.length-1][1];
  // t interno con la stessa y del terminale esterno, cercato vicino a t1
  let best=t1,bd=1e9;for(let k=0;k<=4000;k++){const t=t1+(t0-t1)*k/4000*0.6;const p=se(cx,cy,ai,bi,ni,t);const d=Math.abs(p[1]-ey);if(d<bd){bd=d;best=t;}}
  const i=[];for(let k=N;k>=0;k-=1)i.push(se(cx,cy,ai,bi,ni,t0+(best-t0)*k/N));
  const pts=[...o,...i]; return poly(t1<t0?pts.reverse():pts);
}
const M={xh:168, asc:-30, sw:138, n:2.3, ov:12};
// asta con tacca a V in cima (la tacca di piega)
function asta(x,top,{notch=true}={}){const sw=M.sw;
  if(!notch) return poly([[x,top],[x+sw,top],[x+sw,H],[x,H]]);
  const w=sw*0.56, d=62, m=x+sw/2;
  return poly([[x,top],[m-w/2,top],[m,top+d],[m+w/2,top],[x+sw,top],[x+sw,H],[x,H]]);}
// pancia della b attaccata a destra dell'asta (x = bordo sinistro dell'asta)
function bBowl(x){const sw=M.sw,th=96,bw=420; const cx=x+sw+bw/2-60, cy=(M.xh+H)/2, a=bw/2+60, b=(H-M.xh)/2+M.ov;
  return {d:ellipse(cx,cy,a,b,M.n,false)+' '+ellipse(cx+8,cy,a-sw*0.9,b-th,M.n*0.95,true), right:cx+a};}
// a a doppio occhio a sinistra dell'asta (x = bordo sinistro dell'asta)
function aLeft(x,o={}){const sw=M.sw;
  const ba=o.ba||172, bb=o.bb||150, bcx=x+sw*0.5-ba, bcy=H+M.ov-bb;
  const bowl=ellipse(bcx,bcy,ba,bb,M.n,false)+' '+ellipse(bcx+(o.cxo??-4),bcy+2,ba-(o.bth||104),bb-(o.btv||92),M.n*0.95,true);
  // arco: quarto di anello con il centro sull'asta, dal colmo (dentro l'asta) al terminale sinistro
  const acx=x+sw*0.5, acy=o.ay||380, aa=sw*0.5+(o.aw||300), ab=acy-(M.xh-M.ov);
  const arch=arc(acx,acy,aa,ab,aa-(o.ath||112),ab-(o.atv||104),M.n,Math.PI*1.5,Math.PI*(o.at||1.12));
  return {d:bowl+' '+arch, left:Math.min(bcx-ba, acx-aa)};
}
module.exports={H,M,poly,se,ellipse,arc,asta,bBowl,aLeft,f};
// r: asta corta + braccio (arco di anello con terminale verticale)
function rLetter(x,o={}){const sw=M.sw; const cx=x+sw+(o.cx||96), cy=(M.xh+H)/2, a=sw+(o.cx||96), b=(H-M.xh)/2+M.ov;
  const arm=arc(cx,cy,a,b,a-sw*0.95,b-(o.th||94),M.n,Math.PI*1.0,Math.PI*(o.rt||1.8));
  const st=poly([[x,M.xh],[x+sw,M.xh],[x+sw,H],[x,H]]);
  const ex=se(cx,cy,a,b,M.n,Math.PI*(o.rt||1.8))[0];
  return {d:st+' '+arm,right:ex};}
const A_OPT={ba:196,bb:148,bth:90,btv:80,ay:392,aw:300,ath:98,atv:96,at:1.1};
// a isolata: occhio, arco e asta corta (x = bordo sinistro dell'asta)
function aAlone(x){const r=aLeft(x,A_OPT);return {d:poly([[x,M.xh],[x+M.sw,M.xh],[x+M.sw,H],[x,H]])+' '+r.d,left:r.left,right:x+M.sw};}
// legatura ab: asta comune con tacca di piega
function ab(x,{notch=true}={}){const a=aLeft(x,A_OPT), b=bBowl(x);return {d:[asta(x,M.asc,{notch}),a.d,b.d].join(' '),left:a.left,right:b.right};}
module.exports.rLetter=rLetter;module.exports.aAlone=aAlone;module.exports.ab=ab;module.exports.A_OPT=A_OPT;
