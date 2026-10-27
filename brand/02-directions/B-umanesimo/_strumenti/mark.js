// Generatore delle geometrie del marchio Abra, territorio B.
const {circle,rect,band,lens,ring}=require('./geo.js');

// SIMBOLO: la "a montata". x-height H, baseline 400, bordo destro dell'asta a x=300.
function symbol(o={}){
  const {H=240,w=58,Ro=96,a0=150,br=75,ov=24,os=4}=o;
  const base=400, top=base-H, sR=300, sL=sR-w;
  const hcx=sR-Ro, hcy=top+Ro;
  const r=br+os/2, bcx=sL+ov-br, bcy=base-br+os/2; // pancia con overshoot sotto la base
  return {
    hook: band(hcx,hcy,Ro,Ro-w,a0,0),
    bowl: circle(bcx,bcy,r),
    stem: rect(sL,hcy,w,base-hcy),
    win:  lens(bcx,bcy,r,sL,sR),
    box: {x0:bcx-r, x1:sR, y0:top, y1:base+os}
  };
}

// LOGOTIPO "abra"
function wordmark(o={}){
  const {H=240,w=48,asc=1.38,ov=22,Ro=98,br=79,Rs=98,ka=38,kb=30,kr=16,os=4,a0=148,rEnd=40}=o;
  const base=400, top=base-H, ascY=base-H*asc;
  let ink='', win='';
  function letA(x){
    const r=br+os/2, bcx=x+r, bcy=base-br+os/2, sL=x+2*r-ov, sR=sL+w;
    ink+=circle(bcx,bcy,r);
    win+=lens(bcx,bcy,r,sL,sR);
    ink+=band(sR-Ro,top+Ro,Ro,Ro-w,a0,0);
    ink+=rect(sL,top+Ro,w,base-top-Ro);
    return sR;
  }
  let x=0, e=letA(x);
  x=e+ka; const bR=H/2+os/2, bcy=base-H/2+os/2;
  ink+=rect(x,ascY,w,base-ascY);
  const bcx=x+w-ov+bR;
  ink+=circle(bcx,bcy,bR);
  win+=lens(bcx,bcy,bR,x,x+w);
  e=bcx+bR;
  x=e+kb;
  ink+=rect(x,top,w,H);
  ink+=band(x+Rs,top+Rs,Rs,Rs-w,180,rEnd);
  e=x+Rs*(1+Math.cos(rEnd*Math.PI/180));
  x=e+kr;
  e=letA(x);
  return {ink,win,w:e,top:ascY,base:base+os,xh:top};
}
module.exports={symbol,wordmark};
// LOGOTIPO a anelli: mode 'clean' | 'gap' | 'xor'
function wordmark2(o={}){
  const {H=240,w=40,t=44,asc=1.36,Ro=98,br=80,Rs=96,ka=42,kb=30,kr=14,os=4,a0=150,rEnd=40,ov=0,gap=10,mode='clean'}=o;
  const base=400, top=base-H, ascY=base-H*asc;
  let ink='', win='', xor='';
  function letA(x){
    const r=br+os/2, bcx=x+r, bcy=base-br+os/2, sL=x+2*r-t*0.5-ov, sR=sL+w;
    const rg=ring(bcx,bcy,r,r-t*0.92);
    if(mode==='xor'){xor+=rg+rect(sL,top+Ro,w,base-top-Ro);}
    else {ink+=rg; ink+=rect(sL,top+Ro,w,base-top-Ro); if(mode==='gap') win+=rect(sL-gap,bcy-r-1,gap,2*r+2);}
    ink+=band(sR-Ro,top+Ro,Ro,Ro-w,a0,0);
    return sR;
  }
  let x=0, e=letA(x);
  x=e+ka; const bR=H/2+os/2, bcy=base-H/2+os/2;
  const bcx=x+w*0.5+bR-ov;
  if(mode==='xor'){xor+=rect(x,ascY,w,base-ascY)+ring(bcx,bcy,bR,bR-t);}
  else {ink+=rect(x,ascY,w,base-ascY); ink+=ring(bcx,bcy,bR,bR-t); if(mode==='gap') win+=rect(x+w,bcy-bR-1,gap,2*bR+2);}
  e=bcx+bR;
  x=e+kb;
  ink+=rect(x,top,w,H);
  ink+=band(x+Rs,top+Rs,Rs,Rs-w,180,rEnd);
  if(mode==='gap') win+=rect(x+w,top+Rs-1,gap,Rs*0.0+2);
  e=x+Rs*(1+Math.cos(rEnd*Math.PI/180));
  x=e+kr;
  e=letA(x);
  return {ink,win,xor,w:e,top:ascY,base:base+os,xh:top};
}
module.exports.wordmark2=wordmark2;
// LOGOTIPO 3: la prima a è il simbolo; b e r costruite con le stesse misure.
function wordmark3(o={}){
  const {H=240,w=54,Ro=96,a0=150,br=75,ov=24,os=4,asc=1.36,tb=58,Rs=96,rEnd=38,ab=46,br_=34,ra=8}=o;
  const base=400, top=base-H, ascY=base-H*asc;
  const parts=[];
  function letA(x){ // x = bordo sinistro della pancia
    const r=br+os/2, bcx=x+r, bcy=base-br+os/2, sL=bcx+br-ov, sR=sL+w;
    const hcx=sR-Ro, hcy=top+Ro;
    parts.push({k:'a',hook:band(hcx,hcy,Ro,Ro-w,a0,0),bowl:circle(bcx,bcy,r),stem:rect(sL,hcy,w,base-hcy),win:lens(bcx,bcy,r,sL,sR)});
    return sR;
  }
  let e=letA(0);
  let x=e+ab; const bR=H/2+os/2, bcy=base-H/2+os/2, bcx=x+bR;
  parts.push({k:'b',ink:rect(x,ascY,w,base-ascY)+ring(bcx,bcy,bR,bR-tb)});
  e=bcx+bR;
  x=e+br_;
  parts.push({k:'r',ink:rect(x,top,w,H)+band(x+Rs,top+Rs,Rs,Rs-w,180,rEnd)});
  e=x+Rs*(1+Math.cos(rEnd*Math.PI/180));
  // la seconda a parte dalla pancia, che può infilarsi sotto la spalla della r
  x=e+ra;
  e=letA(x);
  return {parts,w:e,top:ascY,base:base+os,xh:top};
}
module.exports.wordmark3=wordmark3;
