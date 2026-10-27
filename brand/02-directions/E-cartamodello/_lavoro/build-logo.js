const fs=require('fs'),path=require('path');
const L=__dirname, OUT=path.join(L,'..','logo');
eval(fs.readFileSync(path.join(L,'mark.js'),'utf8'));
const BRA=JSON.parse(fs.readFileSync(path.join(L,'bra.json')));
const ROB=JSON.parse(fs.readFileSync(path.join(L,process.env.ROB||'rob430.json')));
const H=660;
const P={W:730,st:198,top:74,ia:520,by:460,t:62,gap:24,ang:9,len:150};
const PF={W:720,st:200,top:80,ia:520,by:470,t:84,gap:30,ang:9,len:96}; // favicon cut
const COL={flan:'#2F3337',tela:'#ECE6D8',giallo:'#F2BF2C',gesso:'#FAF8F3'};
// transform glyph path d (y-up, units) into y-down translated absolute path by parsing commands
function tx(d,dx,dy=H,s=1){
  return d.replace(/([MLQCZHV])([^MLQCZHV]*)/g,(m,c,args)=>{
    if(c==='Z')return 'Z';
    const n=args.trim().split(/[ ,]+/).map(Number);const o=[];
    if(c==='H'){return 'H'+n.map(v=>+(dx+v*s).toFixed(1)).join(' ');}
    if(c==='V'){return 'V'+n.map(v=>+(dy-v*s).toFixed(1)).join(' ');}
    for(let i=0;i<n.length;i+=2)o.push(+(dx+n[i]*s).toFixed(1),+(dy-n[i+1]*s).toFixed(1));
    return c+o.join(' ');
  });
}
function runGlyphs(glyphs,x0,track,s=1,dy=H){let x=x0,d='';for(const c of glyphs){d+=tx(c.d,x,dy,s);x+=(c.adv+track)*s;}return {d,end:x-track*s};}
function wordAbra(){ // A with inner thread only + bra
  const g=mark(P); const s=g.d.split(' M'); const A=`${s[0]} M${s[1]}`;
  const r=runGlyphs(BRA,P.W+30,0);
  return {d:A+' '+r.d,end:r.end};
}
function svgFile(vb,body,title){return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb}" role="img" aria-labelledby="t"><title id="t">${title}</title>${body}</svg>\n`;}
const w=wordAbra();
// horizontal: Abra + space + Robotics (lighter), robotics at same cap height (scale so cap ~660)
const RS=0.56; const rob=runGlyphs(ROB,w.end+150,10,RS);
const hb={x:-10,w:rob.end+20};
const horiz=(fill)=>`<path fill="${fill}" d="${w.d}"/><path fill="${fill}" d="${rob.d}"/>`;
const vbH=`${hb.x} -50 ${hb.w} 790`;
fs.writeFileSync(path.join(OUT,'orizzontale.svg'),svgFile(vbH,horiz(COL.flan),'Abra Robotics'));
fs.writeFileSync(path.join(OUT,'mono-positivo.svg'),svgFile(vbH,horiz('#000000'),'Abra Robotics'));
fs.writeFileSync(path.join(OUT,'mono-negativo.svg'),svgFile(vbH,horiz('#FFFFFF'),'Abra Robotics'));
// symbol
const g=mark(P);
const sw=g.maxx-g.minx, S=Math.max(sw,H)+160;
const vbS=`${(g.minx-(S-sw)/2).toFixed(1)} ${(-(S-H)/2).toFixed(1)} ${S.toFixed(1)} ${S.toFixed(1)}`;
fs.writeFileSync(path.join(OUT,'simbolo.svg'),svgFile(vbS,`<path fill="${COL.flan}" d="${g.d}"/>`,'Abra, simbolo'));
// monogram for small sizes: favicon cut in a tela square tile? keep transparent, heavier
const f=mark(PF); const fw=f.maxx-f.minx, FS=Math.max(fw,H)+60;
const vbF=`${(f.minx-(FS-fw)/2).toFixed(1)} ${(-(FS-H)/2).toFixed(1)} ${FS.toFixed(1)} ${FS.toFixed(1)}`;
fs.writeFileSync(path.join(OUT,'monogramma.svg'),svgFile(vbF,`<path fill="${COL.flan}" d="${f.d}"/>`,'Abra, monogramma per piccole dimensioni'));
// vertical: Abra over Robotics; Robotics distributed across the ink width of Abra (set "to measure")
const vS=0.33; const wInk=w.end-12;
const natW=ROB.reduce((t,c)=>t+c.adv,0)*vS; const lastAdv=ROB[ROB.length-1].adv*vS;
const tr=(wInk-natW)/(ROB.length-1)/vS; // tracking in font units
const vRob=runGlyphs(ROB,0,tr,vS,0);
const vy=H+150+H*vS;
const vbody=(fill)=>`<path fill="${fill}" d="${w.d}"/><path fill="${fill}" transform="translate(6 ${vy.toFixed(1)})" d="${vRob.d}"/>`;
fs.writeFileSync(path.join(OUT,'verticale.svg'),svgFile(`-60 -60 ${(w.end+100).toFixed(1)} ${(vy+130).toFixed(1)}`,vbody(COL.flan),'Abra Robotics'));
// wordmark only
fs.writeFileSync(path.join(OUT,'logotipo-abra.svg'),svgFile(`-10 -50 ${w.end+20} 790`,`<path fill="${COL.flan}" d="${w.d}"/>`,'Abra'));
// two-tone symbol on dark (A gesso, thread giallo)
const parts=g.d.split(' M'); const legs=parts[0]; const thr='M'+parts.slice(1).join(' M');
fs.writeFileSync(path.join(OUT,'simbolo-bicolore.svg'),svgFile(vbS,`<rect x="${(g.minx-(S-sw)/2).toFixed(1)}" y="${(-(S-H)/2).toFixed(1)}" width="${S.toFixed(1)}" height="${S.toFixed(1)}" fill="${COL.flan}"/><path fill="${COL.gesso}" d="${legs}"/><path fill="${COL.giallo}" d="${thr}"/>`,'Abra, simbolo bicolore'));
fs.writeFileSync(path.join(L,'geom.json'),JSON.stringify({g,f,w,rob,legs,thr,vbS,vbF,vbH,P,PF}));
console.log('ok',vbH,vbS);
// pieces for animation
{
 const g2=mark(P); const s=g2.d.split(' M');
 const braPieces=[]; let x=P.W+30; for(const c of BRA){braPieces.push(tx(c.d,x,H,1)); x+=c.adv;}
 const robPieces=[]; let xr=w.end+150; for(const c of ROB){robPieces.push(tx(c.d,xr,H,0.56)); xr+=(c.adv+10)*0.56;}
 fs.writeFileSync(path.join(L,'anim.json'),JSON.stringify({legs:s[0],inner:'M'+s[1],outerL:'M'+s[2],outerR:'M'+s[3],bra:braPieces,rob:robPieces,vbH,P}));
}
