// Marchio Abra v2, territorio B. node build2.js <cartella logo>
const fs=require('fs');const path=require('path');
const {wm}=require('./mark2.js');const {f}=require('./geo.js');
const OUT=process.argv[2];
const C={carta:'#F6F4EF',grafite:'#232527',rosso:'#B83A2B',bianco:'#FFFFFF'};
const PAR={g:16,w:46,t:50,ka:48,kb:36,kr:12};
const W=wm(PAR);
const T=JSON.parse(fs.readFileSync(path.join(__dirname,'txt.json')));
function tx(d,s,dx,dy){
  return d.replace(/([MLHVACQZ])([^MLHVACQZ]*)/gi,(m,c,args)=>{
    const n=(args.match(/-?\d*\.?\d+(?:e-?\d+)?/g)||[]).map(Number);const C=c.toUpperCase();let o=[];
    if(C==='H')o=n.map(v=>f(v*s+dx));else if(C==='V')o=n.map(v=>f(v*s+dy));
    else o=n.map((v,i)=>f(i%2?v*s+dy:v*s+dx));
    return C+o.join(' ');});
}
const partD=p=>Object.entries(p).filter(([k])=>k!=='k').map(([,d])=>d).join('');
const abra=col=>`<path fill="${col}" d="${W.parts.map(partD).join('')}"/>`;
const A=W.parts[0];
const svg=(vb,body,title)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.map(f).join(' ')}" role="img" aria-labelledby="t"><title id="t">${title}</title>${body}</svg>\n`;
const pad=36, BASE=400;
// "Robotics" Instrument Sans Regular, altezza x = 0.46 di quella di abra
const R=T.rob_b, s=(240*0.46)/R.xh, rw=R.adv*s, gap=78;
const robotics=(x,col,sc=s)=>`<path fill="${col}" d="${tx(R.d,sc,x,BASE)}"/>`;
const y0=W.top-pad, H=W.base-W.top+2*pad, totW=W.w+gap+rw;
const hor=(a,r)=>abra(a)+robotics(W.w+gap,r);
fs.writeFileSync(`${OUT}/orizzontale.svg`,svg([-pad,y0,totW+2*pad,H],hor(C.rosso,C.grafite),'Abra Robotics'));
fs.writeFileSync(`${OUT}/orizzontale-negativo.svg`,svg([-pad,y0,totW+2*pad,H],hor(C.carta,C.carta),'Abra Robotics, negativo'));
fs.writeFileSync(`${OUT}/mono-positivo.svg`,svg([-pad,y0,totW+2*pad,H],hor(C.grafite,C.grafite),'Abra Robotics, mono positivo'));
fs.writeFileSync(`${OUT}/mono-negativo.svg`,svg([-pad,y0,totW+2*pad,H],hor(C.bianco,C.bianco),'Abra Robotics, mono negativo'));
fs.writeFileSync(`${OUT}/logotipo.svg`,svg([-pad,y0,W.w+2*pad,H],abra(C.rosso),'Abra'));
// verticale: ROBOTICS maiuscolo spaziato sotto, largo quanto abra
const RC=T.rob_caps_b, s2=W.w/RC.adv, capH=RC.cap*s2, vb2=BASE+70+capH;
fs.writeFileSync(`${OUT}/verticale.svg`,svg([-pad,y0,W.w+2*pad,vb2+pad-y0],abra(C.rosso)+`<path fill="${C.grafite}" d="${tx(RC.d,s2,0,vb2)}"/>`,'Abra Robotics, verticale'));
// simbolo: la a con il giunto
const ax0=0, ax1=2*(80+1.5)+16+46; // pancia + giunto + asta
const sy0=160, sy1=403;
const aD=partD(A);
fs.writeFileSync(`${OUT}/simbolo.svg`,svg([ax0-28,sy0-28,ax1-ax0+56,sy1-sy0+56],`<path fill="${C.rosso}" d="${aD}"/>`,'Abra, simbolo'));
fs.writeFileSync(`${OUT}/simbolo-negativo.svg`,svg([ax0-28,sy0-28,ax1-ax0+56,sy1-sy0+56],`<path fill="${C.carta}" d="${aD}"/>`,'Abra, simbolo negativo'));
// monogramma: tessera rossa con la a in carta
const side=360, cx=(ax0+ax1)/2, cy=(sy0+sy1)/2;
fs.writeFileSync(`${OUT}/monogramma.svg`,svg([cx-side/2,cy-side/2,side,side],`<rect x="${f(cx-side/2)}" y="${f(cy-side/2)}" width="${side}" height="${side}" fill="${C.rosso}"/><path fill="${C.carta}" d="${aD}"/>`,'Abra, monogramma'));
fs.writeFileSync(path.join(__dirname,'dati.json'),JSON.stringify({W:{w:W.w,top:W.top,base:W.base},s,rw,gap,ax1,PAR}));
console.log('ok',W.w,rw,ax1);
