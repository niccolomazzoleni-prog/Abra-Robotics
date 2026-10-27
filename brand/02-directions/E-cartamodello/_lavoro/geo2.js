// Geometria v2 del marchio Abra (direzione E). Coordinate y verso il basso, linea di base y=660, altezza maiuscola 0.
const H=660;
const f=v=>+v.toFixed(1);
function pathPoly(pts){return 'M'+pts.map(p=>f(p[0])+' '+f(p[1])).join(' L')+' Z';}
function capsule(x0,y0,x1,y1,r){const dx=x1-x0,dy=y1-y0,L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L,nx=-uy*r,ny=ux*r;
 return `M${f(x0+nx)} ${f(y0+ny)} L${f(x1+nx)} ${f(y1+ny)} A${r} ${r} 0 0 0 ${f(x1-nx)} ${f(y1-ny)} L${f(x0-nx)} ${f(y0-ny)} A${r} ${r} 0 0 0 ${f(x0+nx)} ${f(y0+ny)} Z`;}
function A2(o={}){
 const W=o.W||730, st=o.st||198, top=o.top||74, ia=o.ia||530, cx=W/2;
 const by=o.by||420, t=o.t||80, ang=(o.ang??9)*Math.PI/180, gap=o.gap??30, len=o.len??150, notch=o.notch??0;
 const tl=cx-top/2,tr=cx+top/2,iy=H-ia, m=-Math.tan(ang);
 const line=(x,off)=>by+off+m*(x-cx);
 // intersection of line y=by+off+m(x-cx) with segment (xa,ya)-(xb,yb)
 const X=(xa,ya,xb,yb,off)=>{const s=(by+off+m*(xa-cx)-ya)/((yb-ya)-m*(xb-xa));return [xa+s*(xb-xa),ya+s*(yb-ya)];};
 // legs outline with optional notch on left outer edge, centred on the bar line
 let left=[[0,H]];
 if(notch){const c=X(0,H,tl,0,0); const L=Math.hypot(tl,H), ux=tl/L, uy=-H/L; const hw=notch*0.62;
   left.push([c[0]-ux*hw,c[1]-uy*hw],[c[0]+notch*Math.cos(ang),c[1]-notch*Math.sin(ang)],[c[0]+ux*hw,c[1]+uy*hw]);}
 const legs=pathPoly([...left,[tl,0],[tr,0],[W,H],[W-st,H],[cx,iy],[st,H]]);
 // crossbar: quad between inner edges
 const a0=X(st,H,cx,iy,-t/2), a1=X(st,H,cx,iy,t/2), b0=X(W-st,H,cx,iy,-t/2), b1=X(W-st,H,cx,iy,t/2);
 const bar=pathPoly([[a0[0]-1,a0[1]],[b0[0]+1,b0[1]],[b1[0]+1,b1[1]],[a1[0]-1,a1[1]]]);
 // outer stitch on the right: near end follows the leg edge (the thread comes out from under the leg), far end rounded
 const r=t/2; let stitch='';
 if(len>0){
   const u0=X(W,H,tr,0,-t/2), u1=X(W,H,tr,0,t/2); // outer edge at bar top/bottom
   const dx=Math.cos(ang), dy=-Math.sin(ang);
   const p0=[u0[0]+gap*dx,u0[1]+gap*dy], p1=[u1[0]+gap*dx,u1[1]+gap*dy];
   const ex=Math.max(p0[0],p1[0])+len-r; const c=[ex,line(ex,0)];
   const nx=-dy*r, ny=dx*r; // normal (towards bar bottom)
   const top=[c[0]-nx,c[1]-ny], bot=[c[0]+nx,c[1]+ny];
   stitch=`M${f(p0[0])} ${f(p0[1])} L${f(top[0])} ${f(top[1])} A${r} ${r} 0 0 1 ${f(bot[0])} ${f(bot[1])} L${f(p1[0])} ${f(p1[1])} Z`;
 }
 const maxx=len>0?Math.max(p0x(),0):W;
 function p0x(){const u0=X(W,H,tr,0,-t/2);return u0[0]+gap*Math.cos(ang)+len;}
 return {legs,bar,stitch,W,minx:0,maxx:len>0?p0x()+r*0.2:W,miny:0,maxy:H};
}
// superellipse sampling
function se(cx,cy,a,b,n,t){const c=Math.cos(t),s=Math.sin(t);return [cx+a*Math.sign(c)*Math.pow(Math.abs(c),2/n), cy+b*Math.sign(s)*Math.pow(Math.abs(s),2/n)];}
function ring(cx,cy,ao,bo,ai,bi,n,ni,t0,t1,N=96){ // arc of ring from t0 to t1 (y down: t positive goes clockwise visually)
 const o=[],i=[];for(let k=0;k<=N;k++){const t=t0+(t1-t0)*k/N;o.push(se(cx,cy,ao,bo,n,t));}
 for(let k=N;k>=0;k-=1){const t=t0+(t1-t0)*k/N;i.push(se(cx,cy,ai,bi,ni,t));}
 return [...o,...i];}
function full(cx,cy,a,b,n,rev,N=160){const p=[];for(let k=0;k<N;k++){const t=(rev?-1:1)*2*Math.PI*k/N;p.push(se(cx,cy,a,b,n,t));}return pathPoly(p);}
// lettere disegnate: b, r, a (b e a sono lo stesso pezzo specchiato)
function letters(o={}){
 const xh=o.xh||168, asc=o.asc||-44, sw=o.sw||156, bw=o.bw||530, th=o.th||112, n=o.n||2.2, ov=12;
 const out={};
 // b at x0=0
 const bcx=bw/2+20, bcy=(xh+H)/2, bao=bw/2-20+0, bbo=(H-xh)/2+ov;
 const ai=bao-sw*0.98, bi=bbo-th; const icx=bcx+ (sw*0.02);
 const bstem=pathPoly([[0,asc],[sw,asc],[sw,H],[0,H]]);
 const bowl=full(bcx,bcy,bao,bbo,n,false);
 const counter=full(icx,bcy,ai,bi,n*0.95,true);
 // ink trap / tacca at junctions
 const trap=(x,y,dir)=>pathPoly([[x,y-dir*0],[x+38,y+dir*58],[x-2,y+dir*92]]);
 out.b={d:[bstem,bowl,counter].join(' '),adv:bcx+bao};
 // a: mirror of b without ascender
 const aw=out.b.adv; const mir=d=>d.replace(/M(-?[\d.]+) (-?[\d.]+)|L(-?[\d.]+) (-?[\d.]+)/g,(m0,a1,b1,c1,d1)=>a1!==undefined?`M${f(aw-+a1)} ${b1}`:`L${f(aw-+c1)} ${d1}`);
 const astem=mir(pathPoly([[0,xh],[sw,xh],[sw,H],[0,H]]));
 out.a={d:[astem,mir(bowl),mir(counter)].join(' '),adv:aw};
 // r: stem + upper arc of the bowl ring, terminal cut
 const rstem=pathPoly([[0,xh],[sw,xh],[sw,H],[0,H]]);
 // r arm: outer arc from the stem to t1, inner arc ends at the same x (vertical terminal)
 const t1=Math.PI*(o.rt||1.6);
 const ex=se(bcx,bcy,bao,bbo,n,t1)[0];
 let lo=Math.PI*1.5, hi=Math.PI*1.99; for(let k=0;k<60;k++){const mid=(lo+hi)/2; if(se(bcx,bcy,ai,bi,n*0.95,mid)[0]<ex) lo=mid; else hi=mid;}
 const t2=Math.min(lo,Math.PI*1.99);
 const oarc=[],iarc=[]; const N=80;
 for(let k=0;k<=N;k++){oarc.push(se(bcx,bcy,bao,bbo,n,Math.PI+(t1-Math.PI)*k/N));}
 for(let k=N;k>=0;k-=1){iarc.push(se(bcx,bcy,ai,bi,n*0.95,Math.PI+(t2-Math.PI)*k/N));}
 const arm=pathPoly([...oarc,[ex,se(bcx,bcy,ai,bi,n*0.95,t2)[1]],...iarc]);
 out.r={d:rstem+' '+arm,adv:ex};
 return out;
}
if(typeof module!=='undefined')module.exports={A2,letters,capsule,pathPoly,H};
