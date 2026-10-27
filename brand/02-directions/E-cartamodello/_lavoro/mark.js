// shared geometry for the Abra monogram. y-down, apex y=0, baseline y=H
function capsule(x0,y0,x1,y1,r){
  const dx=x1-x0,dy=y1-y0,L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L,nx=-uy*r,ny=ux*r;
  const f=v=>+v.toFixed(2);
  return `M${f(x0+nx)} ${f(y0+ny)} L${f(x1+nx)} ${f(y1+ny)} A${r} ${r} 0 0 0 ${f(x1-nx)} ${f(y1-ny)} L${f(x0-nx)} ${f(y0-ny)} A${r} ${r} 0 0 0 ${f(x0+nx)} ${f(y0+ny)} Z`;
}
function rectSeg(x0,y0,x1,y1,r){ // square ends
  const dx=x1-x0,dy=y1-y0,L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L,nx=-uy*r,ny=ux*r;const f=v=>+v.toFixed(2);
  return `M${f(x0+nx)} ${f(y0+ny)} L${f(x1+nx)} ${f(y1+ny)} L${f(x1-nx)} ${f(y1-ny)} L${f(x0-nx)} ${f(y0-ny)} Z`;
}
function mark(o={}){
 const H=660,W=o.W||600,st=o.st||150,top=o.top||70,ia=o.ia||470,cx=W/2;
 const by=o.by||400,t=o.t||64,gap=o.gap||34,ang=(o.ang||0)*Math.PI/180,ext=o.ext||null,cap=o.cap||'round';
 const tl=cx-top/2,tr=cx+top/2,iy=H-ia;
 const f=v=>+v.toFixed(2);
 const legs=`M0 ${H} L${f(tl)} 0 L${f(tr)} 0 L${W} ${H} L${f(W-st)} ${H} L${cx} ${f(iy)} L${st} ${H} Z`;
 // thread line: y = by + m*(x-cx), m = -tan(ang) (rising to the right)
 const m=-Math.tan(ang);
 const yl=x=>by+m*(x-cx);
 // intersection of thread with a leg edge line from (xa,ya) to (xb,yb)
 const inter=(xa,ya,xb,yb)=>{ // solve param
   // edge: x = xa + s*(xb-xa), y = ya + s*(yb-ya); need y = by + m*(x-cx)
   const s=(by+m*(xa-cx)-ya)/((yb-ya)-m*(xb-xa)); return xa+s*(xb-xa);};
 const oL=inter(0,H,tl,0), iL=inter(st,H,cx,iy), iR=inter(W-st,H,cx,iy), oR=inter(W,H,tr,0);
 const g=gap+(cap=='round'?t/2:0); // gap measured from edge to cap end
 const cosA=Math.cos(ang);
 const inLen=(iR-iL)-2*g/cosA*cosA; // horizontal span
 const a0=iL+g, a1=iR-g; const L=o.len||(a1-a0);
 const seg=cap=='round'?capsule:rectSeg;
 const r=t/2;
 const S=[[a0,a1],[oL-g-L,oL-g],[oR+g,oR+g+L]];
 if(o.n2){S.push([oL-g-L-o.n2-L,oL-g-L-o.n2]);S.push([oR+g+L+o.n2,oR+g+L+o.n2+L]);}
 let d=legs; let minx=0,maxx=W;
 for(const [x0,x1] of S){ d+=' '+seg(x0,yl(x0),x1,yl(x1),r); minx=Math.min(minx,x0-r); maxx=Math.max(maxx,x1+r);}
 return {d,minx,maxx,H,W,legs};
}
function svgOf(g,size,fg,pad=0.1,bg){
 const Wd=g.maxx-g.minx,S=Math.max(Wd,g.H)*(1+pad*2);
 return `<svg width="${size}" height="${size}" viewBox="${(g.minx-(S-Wd)/2).toFixed(1)} ${(-(S-g.H)/2).toFixed(1)} ${S.toFixed(1)} ${S.toFixed(1)}">${bg?`<rect x="-9999" y="-9999" width="99999" height="99999" fill="${bg}"/>`:''}<path d="${g.d}" fill="${fg}"/></svg>`;
}
