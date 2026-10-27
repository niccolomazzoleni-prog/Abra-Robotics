// Geometria del segno Abra (territorio B). Coordinate SVG, y verso il basso.
const f=v=>+v.toFixed(2);
const pol=(cx,cy,r,a)=>[cx+r*Math.cos(a*Math.PI/180),cy-r*Math.sin(a*Math.PI/180)];
function circle(cx,cy,r){return `M${f(cx-r)} ${f(cy)}A${r} ${r} 0 1 1 ${f(cx+r)} ${f(cy)}A${r} ${r} 0 1 1 ${f(cx-r)} ${f(cy)}Z`}
function rect(x,y,w,h){return `M${f(x)} ${f(y)}H${f(x+w)}V${f(y+h)}H${f(x)}Z`}
// banda d'arco da a0 a a1 (gradi matematici, a0>a1, senso orario sullo schermo)
function band(cx,cy,ro,ri,a0,a1){
  const [x0,y0]=pol(cx,cy,ro,a0),[x1,y1]=pol(cx,cy,ro,a1),[x2,y2]=pol(cx,cy,ri,a1),[x3,y3]=pol(cx,cy,ri,a0);
  const L=Math.abs(a0-a1)>180?1:0;
  return `M${f(x0)} ${f(y0)}A${ro} ${ro} 0 ${L} 1 ${f(x1)} ${f(y1)}L${f(x2)} ${f(y2)}A${ri} ${ri} 0 ${L} 0 ${f(x3)} ${f(y3)}Z`;
}
// intersezione disco con striscia verticale [s0,s1]
function lens(cx,cy,r,s0,s1){
  const a=Math.max(s0,cx-r), b=Math.min(s1,cx+r);
  const h=x=>Math.sqrt(Math.max(0,r*r-(x-cx)**2));
  const ha=h(a),hb=h(b);
  // da (a,cy-ha) arco superiore fino a (b,cy-hb), giù, arco inferiore fino a (a,cy+ha)
  let d=`M${f(a)} ${f(cy-ha)}A${r} ${r} 0 0 1 ${f(b)} ${f(cy-hb)}`;
  d+= hb>0.01?`L${f(b)} ${f(cy+hb)}`:'';
  d+=`A${r} ${r} 0 0 1 ${f(a)} ${f(cy+ha)}Z`;
  return d;
}
if(typeof module!=='undefined')module.exports={circle,rect,band,lens,pol,f};
function circleR(cx,cy,r){return `M${f(cx-r)} ${f(cy)}A${r} ${r} 0 1 0 ${f(cx+r)} ${f(cy)}A${r} ${r} 0 1 0 ${f(cx-r)} ${f(cy)}Z`}
function ring(cx,cy,ro,ri){return circle(cx,cy,ro)+circleR(cx,cy,ri)}
if(typeof module!=='undefined')Object.assign(module.exports,{circleR,ring});
