// Costruisce gli SVG del marchio Abra, territorio B. node build.js <cartella logo>
const fs=require('fs');const path=require('path');
const {wordmark3}=require('./mark.js');
const {circle,rect,band,lens,ring,f}=require('./geo.js');
const OUT=process.argv[2];
const P={iv:'#F3EEE3',ink:'#24211E',r:'#BB3B26',o:'#E2A93B',v:'#2B6F67',w:'#FFFFFF'};
const PAR={w:52,tb:56,ab:50,br_:38,ra:12};
const W=wordmark3(PAR);
const T=JSON.parse(fs.readFileSync(path.join(__dirname,'paths.json')));

// trasla e scala un path assoluto (comandi M L H V A Z C Q) di opentype/geo
function tx(d,s,dx,dy){
  return d.replace(/([MLHVACQZ])([^MLHVACQZ]*)/gi,(m,c,args)=>{
    const n=(args.match(/-?\d*\.?\d+(?:e-?\d+)?/g)||[]).map(Number);
    const C=c.toUpperCase(); let o=[];
    if(C==='H') o=n.map(v=>f(v*s+dx));
    else if(C==='V') o=n.map(v=>f(v*s+dy));
    else if(C==='A'){for(let i=0;i<n.length;i+=7)o.push(f(n[i]*s),f(n[i+1]*s),n[i+2],n[i+3],n[i+4],f(n[i+5]*s+dx),f(n[i+6]*s+dy));}
    else o=n.map((v,i)=>f(i%2?v*s+dy:v*s+dx));
    return C+o.join(' ');
  });
}
// parti della a: con finestra come foro (evenodd su pancia e asta)
function aParts(p,col){ // col: {hook,bowl,stem} oppure stringa unica
  const c=typeof col==='string'?{hook:col,bowl:col,stem:col}:col;
  if(c.hook===c.bowl&&c.bowl===c.stem)
    return `<path fill="${c.hook}" d="${p.hook}"/><path fill="${c.bowl}" fill-rule="evenodd" d="${p.bowl}${p.stem}"/>`;
  return `<path fill="${c.hook}" d="${p.hook}"/><path fill="${c.bowl}" fill-rule="evenodd" d="${p.bowl}${p.win}"/><path fill="${c.stem}" fill-rule="evenodd" d="${p.stem}${p.win}"/>`;
}
function wm(first,rest){ // first: colori della prima a; rest: colore di b, r, seconda a
  let g='',i=0;
  for(const p of W.parts){
    if(p.k==='a'){g+=aParts(p,i++===0?first:rest);}
    else g+=`<path fill="${rest}" d="${p.ink}"/>`;
  }
  return g;
}
const XH=W.xh, BASE=400; // x-height top 160
// "Robotics" corsivo: x-height del font = 426/1000 em. Lo scaliamo a 0.5 della x-height del logotipo.
const rob=T.robotics_it; const s=0.166; // cap-height di Robotics = 0.5 della x-height di abra
function robotics(x,base,fill,scale=s){return `<path fill="${fill}" d="${tx(rob.d,scale,x-rob.bb.x1*scale,base)}"/>`;}
const robW=(rob.bb.x2-rob.bb.x1)*s;

const svg=(vb,body,title='Abra Robotics')=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.map(f).join(' ')}" role="img" aria-labelledby="t"><title id="t">${title}</title>${body}</svg>\n`;
const pad=40;
const colA={hook:P.o,bowl:P.r,stem:P.ink};
const colAneg={hook:P.o,bowl:P.r,stem:P.iv};

// ORIZZONTALE: abra + Robotics
const gapR=54, totW=W.w+gapR+robW;
const yTop=W.top-pad, H=W.base-W.top+2*pad;
const hor=(first,rest,rc)=>wm(first,rest)+robotics(W.w+gapR,BASE,rc);
fs.writeFileSync(`${OUT}/orizzontale.svg`,svg([-pad,yTop,totW+2*pad,H],hor(colA,P.ink,P.ink)));
fs.writeFileSync(`${OUT}/orizzontale-negativo.svg`,svg([-pad,yTop,totW+2*pad,H],hor(colAneg,P.iv,P.iv)));
// LOGOTIPO solo
fs.writeFileSync(`${OUT}/logotipo.svg`,svg([-pad,yTop,W.w+2*pad,H],wm(colA,P.ink),'Abra'));
// MONO
fs.writeFileSync(`${OUT}/mono-positivo.svg`,svg([-pad,yTop,totW+2*pad,H],hor(P.ink,P.ink,P.ink)));
fs.writeFileSync(`${OUT}/mono-negativo.svg`,svg([-pad,yTop,totW+2*pad,H],hor(P.w,P.w,P.w)));
// VERTICALE: abra sopra, Robotics sotto allineato a sinistra con il bordo della pancia
const robWfull=(rob.bb.x2-rob.bb.x1); const s2=(W.w-6)/robWfull; const vBase=BASE+92+670*s2/1000*1000;
const vbody=wm(colA,P.ink)+robotics(3,vBase,P.ink,s2);
const vW=W.w;
fs.writeFileSync(`${OUT}/verticale.svg`,svg([-pad,yTop,vW+2*pad,vBase+pad+50*s2/0.25-yTop],vbody));
// SIMBOLO: prima a
const A=W.parts[0];
const ax0=-8, ax1=Math.max(...[A.stem].map(()=>0))+0; // calcolato sotto
// bordi del simbolo dal disegno: pancia da 0 a 2r, asta fino a sR
const r=75+2, sR=r+75-24+52;
const sy0=160, sy1=404;
const sp=36;
fs.writeFileSync(`${OUT}/simbolo.svg`,svg([-sp,sy0-sp,sR+2*sp,sy1-sy0+2*sp],aParts(A,colA),'Abra, simbolo'));
// MONOGRAMMA: simbolo su tessera rossa, per avatar, favicon e adesivi
const side=360, cx=(sR)/2, cy=(sy0+sy1)/2;
const mx=cx-side/2, my=cy-side/2;
fs.writeFileSync(`${OUT}/monogramma.svg`,svg([mx,my,side,side],`<rect x="${f(mx)}" y="${f(my)}" width="${side}" height="${side}" fill="${P.r}"/>`+aParts(A,{hook:P.o,bowl:P.iv,stem:P.ink}),'Abra, monogramma'));
fs.writeFileSync(`${__dirname}/_dati.json`,JSON.stringify({W:{w:W.w,top:W.top,base:W.base},s,robW,sR,sy0,sy1},null,1));
console.log('ok',W.w,robW,sR);
