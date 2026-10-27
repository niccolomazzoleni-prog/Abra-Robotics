// Logotipo v2: "abra" con i giunti a vista (pance e spalle staccate dalle aste)
const {circle,rect,band,ring}=require('./geo.js');
function wm(o={}){
  const {H=240,w=50,t=54,g=14,asc=1.38,Ro=100,a0=140,rb=80,rr=null,Rs=100,rEnd=38,rJoint=false,bJoint=false,ka=46,kb=34,kr=10,os=3,ti=0.9}=o;
  const base=400, top=base-H, ascY=base-H*asc;
  const parts=[]; // ogni parte: {k, d}
  function A(x){ // x = bordo sinistro della pancia
    const r=rb+os/2, bcx=x+r, bcy=base-rb+os/2;
    const sL=bcx+r+g, sR=sL+w, hcx=sR-Ro, hcy=top+Ro;
    parts.push({k:'a',bowl:ring(bcx,bcy,r,r-t*ti),stem:rect(sL,hcy,w,base-hcy),hook:band(hcx,hcy,Ro,Ro-t*0.96,a0,0)});
    return sR;
  }
  let e=A(0);
  let x=e+ka; const bR=H/2+os;
  const bcx=bJoint? x+w+g+bR : x+bR, bcy=base-H/2;
  parts.push({k:'b',stem:rect(x,ascY,w,base-ascY),bowl:ring(bcx,bcy,bR,bR-t)});
  e=bcx+bR;
  x=e+kb;
  let rd;
  if(rJoint){ const cx=x+w+g+Rs*0.62; rd=band(cx,top+Rs,Rs,Rs-t*0.92,180,rEnd); 
    // spalla staccata: parte dalla metà alta, con il centro spostato a destra
  } else rd=band(x+Rs,top+Rs,Rs,Rs-w,180,rEnd);
  parts.push({k:'r',stem:rect(x,top,w,H),sh:rd});
  const rx=rJoint? x+w+g+Rs*0.62 : x+Rs;
  e=rx+Rs*Math.cos(rEnd*Math.PI/180);
  x=e+kr;
  e=A(x);
  return {parts,w:e,top:ascY,base:base+os,xh:top};
}
module.exports={wm};
