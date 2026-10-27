// Genera i file del marchio v2 in ../logo. Uso: node build-logo-v2.js
const fs=require('fs'),path=require('path');
const {A2,letters,H}=require('./geo2.js');
const OUT=path.join(__dirname,'..','logo');
const C={flan:'#2F3337',gesso:'#FAF8F3',tela:'#ECE6D8',chalk:'#8FB0E0',segno:'#2F5D9E'};
const f=v=>+v.toFixed(1);
const P={by:400,t:86,len:150};
const ROB=JSON.parse(fs.readFileSync(path.join(__dirname,'rob-v2.json')));
function tx(d,dx,dy,s){return d.replace(/([MLQCZHV])([^MLQCZHV]*)/g,(m,c,a)=>{if(c==='Z')return'Z';const n=a.trim().split(/[ ,]+/).map(Number);
 if(c==='H')return 'H'+n.map(v=>f(dx+v*s)).join(' ');if(c==='V')return 'V'+n.map(v=>f(dy-v*s)).join(' ');const o=[];for(let i=0;i<n.length;i+=2)o.push(f(dx+n[i]*s),f(dy-n[i+1]*s));return c+o.join(' ');});}
function shift(d,dx,dy=0){return d.replace(/(-?[\d.]+) (-?[\d.]+)/g,(m,a,b)=>`${f(+a+dx)} ${f(+b+dy)}`);}
function svg(vb,body,title){return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.map(f).join(' ')}" role="img" aria-labelledby="t"><title id="t">${title}</title>${body}</svg>\n`;}
// simbolo
const g=A2(P);
const pad=40, sw=g.maxx, S=Math.max(sw,H)+2*pad;
const vbS=[(sw-S)/2, (H-S)/2, S, S];
const symMono=(fill)=>`<path fill="${fill}" d="${g.legs} ${g.bar} ${g.stitch}"/>`;
const symTwo=(a,b)=>`<path fill="${a}" d="${g.legs} ${g.bar}"/><path fill="${b}" d="${g.stitch}"/>`;
fs.writeFileSync(path.join(OUT,'simbolo.svg'),svg(vbS,symMono(C.flan),'Abra, simbolo'));
fs.writeFileSync(path.join(OUT,'simbolo-bicolore.svg'),svg(vbS,symTwo(C.flan,C.segno),'Abra, simbolo bicolore'));
fs.writeFileSync(path.join(OUT,'simbolo-negativo.svg'),svg(vbS,symTwo(C.gesso,C.chalk),'Abra, simbolo in negativo'));
// monogramma per piccole dimensioni: aste e traversa piu spesse, filo piu corto
const gm=A2({by:396,t:104,st:224,top:96,ia:500,len:120,gap:40});
const Sm=Math.max(gm.maxx,H)+24;
fs.writeFileSync(path.join(OUT,'monogramma.svg'),svg([(gm.maxx-Sm)/2,(H-Sm)/2,Sm,Sm],`<path fill="${C.flan}" d="${gm.legs} ${gm.bar} ${gm.stitch}"/>`,'Abra, monogramma da 24 a 64 px'));
// logotipo Abra: A con traversa, senza filo esterno, + b r a disegnate
const ga=A2({...P,len:0});
const L=letters({rt:1.75});
let x=ga.W+30, word=`${ga.legs} ${ga.bar}`;
const gaps={b:44,r:52,a:0};
for(const c of ['b','r','a']){word+=' '+shift(L[c].d,x);x+=L[c].adv+gaps[c];}
const wEnd=x; // right edge of a
const top=-44;
fs.writeFileSync(path.join(OUT,'logotipo-abra.svg'),svg([-24,top-24,wEnd+48,H-top+48],`<path fill="${C.flan}" d="${word}"/>`,'Abra'));
// Robotics, composto normale
function robotics(x0,base,s){let xx=x0,d='';for(const c of ROB){d+=tx(c.d,xx,base,s);xx+=(c.adv+4)*s;}return {d,end:xx};}
const RS=0.6; const rh=robotics(wEnd+150,H,RS);
const vbH=[-24,top-24,rh.end+48,H-top+48];
const horiz=(fill)=>`<path fill="${fill}" d="${word}"/><path fill="${fill}" d="${rh.d}"/>`;
fs.writeFileSync(path.join(OUT,'orizzontale.svg'),svg(vbH,horiz(C.flan),'Abra Robotics'));
fs.writeFileSync(path.join(OUT,'mono-positivo.svg'),svg(vbH,horiz('#000000'),'Abra Robotics'));
fs.writeFileSync(path.join(OUT,'mono-negativo.svg'),svg(vbH,horiz('#FFFFFF'),'Abra Robotics'));
// verticale: simbolo sopra, Abra, Robotics allineato a sinistra sotto
const rv=robotics(6,H+120+H*0.3,0.3);
const vH=H+120+H*0.3;
fs.writeFileSync(path.join(OUT,'verticale.svg'),svg([-24,top-24,Math.max(wEnd,rv.end)+48,vH-top+60],`<path fill="${C.flan}" d="${word}"/><path fill="${C.flan}" d="${rv.d}"/>`,'Abra Robotics'));
fs.writeFileSync(path.join(__dirname,'geom-v2.json'),JSON.stringify({g,gm,ga,word,rh,vbS,vbH,wEnd,P}));
console.log('ok',vbS.map(f),vbH.map(f));
