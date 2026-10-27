// Genera il marchio v3 in ../logo. Uso: node build-logo-v3.js
const fs=require('fs'),path=require('path');
const g=require('./geo3.js');const {H,M}=g;
const OUT=path.join(__dirname,'..','logo');
const C={flan:'#2F3337',gesso:'#F7F6F2',chalk:'#8BB8E8',segno:'#3D5A99'};
const f=v=>+v.toFixed(1);
const sh=(d,dx,dy=0)=>d.replace(/(-?[\d.]+) (-?[\d.]+)/g,(m,p,q)=>`${f(+p+dx)} ${f(+q+dy)}`);
function svg(vb,body,title){return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.map(f).join(' ')}" role="img" aria-labelledby="t"><title id="t">${title}</title>${body}</svg>\n`;}
// simbolo: legatura ab
const L=g.ab(0); const top=M.asc, bot=H+M.ov;
const sw=L.right-L.left, sh_=bot-top, pad=40, S=Math.max(sw,sh_)+2*pad;
const vbS=[L.left-(S-sw)/2, top-(S-sh_)/2, S, S];
fs.writeFileSync(path.join(OUT,'simbolo.svg'),svg(vbS,`<path fill="${C.flan}" d="${L.d}"/>`,'Abra, simbolo ab'));
fs.writeFileSync(path.join(OUT,'simbolo-negativo.svg'),svg(vbS,`<path fill="${C.gesso}" d="${L.d}"/>`,'Abra, simbolo ab in negativo'));
// bicolore: tessera in gesso blu con tacca a V sul bordo alto allineata alla piega
const T=S, tx=vbS[0], ty=vbS[1], mid=M.sw/2;
const tile=`M${f(tx)} ${f(ty)} H${f(mid-34)} L${f(mid)} ${f(ty+44)} L${f(mid+34)} ${f(ty)} H${f(tx+T)} V${f(ty+T)} H${f(tx)} Z`;
fs.writeFileSync(path.join(OUT,'simbolo-bicolore.svg'),svg(vbS,`<path fill="${C.chalk}" d="${tile}"/><path fill="${C.flan}" d="${L.d}"/>`,'Abra, simbolo ab su tessera in gesso blu'));
fs.writeFileSync(path.join(OUT,'monogramma.svg'),svg([L.left-12,top-(sw+24-sh_)/2,sw+24,sw+24],`<path fill="${C.flan}" d="${L.d}"/>`,'Abra, monogramma da 24 a 64 px'));
// logotipo abra
let x=L.right+26; const r=g.rLetter(x); x=r.right+50;
const a2=g.aAlone(0); const dx=x-a2.left;
const word=[L.d,r.d,sh(a2.d,dx)].join(' '); const wEnd=a2.right+dx;
const vbW=[L.left-24, top-24, wEnd-L.left+48, bot-top+48];
fs.writeFileSync(path.join(OUT,'logotipo-abra.svg'),svg(vbW,`<path fill="${C.flan}" d="${word}"/>`,'abra'));
// robotics: Bricolage 600, altezza x allineata a quella di abra
const ROB=JSON.parse(fs.readFileSync(path.join(__dirname,'rob-v3.json')));
function tx_(d,dx,dy,s){return d.replace(/([MLQCZHV])([^MLQCZHV]*)/g,(m,c,a)=>{if(c==='Z')return'Z';const n=a.trim().split(/[ ,]+/).map(Number);
 if(c==='H')return 'H'+n.map(v=>f(dx+v*s)).join(' ');if(c==='V')return 'V'+n.map(v=>f(dy-v*s)).join(' ');const o=[];for(let i=0;i<n.length;i+=2)o.push(f(dx+n[i]*s),f(dy-n[i+1]*s));return c+o.join(' ');});}
function rob(x0,base,s){let xx=x0,d='';for(const c of ROB){d+=tx_(c.d,xx,base,s);xx+=(c.adv+6)*s;}return {d,end:xx};}
const xs=(H-M.xh)/524; // scala per altezza x uguale
const rh=rob(wEnd+150,H,xs);
const vbH=[L.left-24, top-24, rh.end-L.left+48, bot-top+48];
const horiz=(fill)=>`<path fill="${fill}" d="${word}"/><path fill="${fill}" d="${rh.d}"/>`;
fs.writeFileSync(path.join(OUT,'orizzontale.svg'),svg(vbH,horiz(C.flan),'abra robotics'));
fs.writeFileSync(path.join(OUT,'mono-positivo.svg'),svg(vbH,horiz('#000000'),'abra robotics'));
fs.writeFileSync(path.join(OUT,'mono-negativo.svg'),svg(vbH,horiz('#FFFFFF'),'abra robotics'));
// verticale: abra sopra, robotics sotto allineato a sinistra, a 0,5 dell'altezza x
const vs=xs*0.42, rv=rob(L.left,bot+130+(H-M.xh)*0.42, vs);
fs.writeFileSync(path.join(OUT,'verticale.svg'),svg([L.left-24,top-24,Math.max(wEnd,rv.end)-L.left+48,bot+130+(H-M.xh)*0.42+60-top+24],`<path fill="${C.flan}" d="${word}"/><path fill="${C.flan}" d="${rv.d}"/>`,'abra robotics'));
fs.writeFileSync(path.join(__dirname,'geom-v3.json'),JSON.stringify({L,word,vbS,vbW,vbH,wEnd,tile,top,bot}));
console.log('ok',vbS.map(f),vbH.map(f));
