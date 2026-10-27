// Sei icone del territorio B, costruite con le tre forme del marchio: disco, asta, arco.
const fs=require('fs');const {circle,rect,band,lens,ring,f}=require('./geo.js');
const OUT=process.argv[2];
const INK='#24211E', R='#BB3B26', IV='#F3EEE3';
const svg=(title,body)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" role="img" aria-labelledby="t"><title id="t">${title}</title>${body}</svg>\n`;
const p=(d,fill,ev)=>`<path fill="${fill}"${ev?' fill-rule="evenodd"':''} d="${d}"/>`;
const ic={};
// 1. Prova sul banco: asta graduata e disco da misurare
ic['prova']=svg('Prova sul banco',
  p(rect(30,6,5,36)+rect(35,12,5,3)+rect(35,22,7,3)+rect(35,32,5,3),INK)+
  p(rect(4,39,30,3),INK)+
  p(circle(16,29,10),R));
// 2. Simulazione e digital twin: reale e virtuale sovrapposti, il giunto resta visibile
ic['simulazione']=svg('Simulazione e digital twin',
  p(circle(18,24,12)+lens(18,24,12,22,40),INK,true)+
  p(ring(30,24,12,8),R));
// 3. POC a fasi: tre dischi su un'asta, il terzo è la decisione
ic['fasi']=svg('POC a fasi',
  p(rect(3,35,42,3),INK)+p(circle(9,30,4),INK)+p(circle(21,28,6),INK)+p(circle(36,25,9),R));
// 4. Documentazione consegnata: foglio ad arco con righe e sigillo
ic['consegna']=svg('Documentazione consegnata',
  p(`M8 44V18A16 16 0 0 1 40 18V44Z`+`M13 41H35V18A11 11 0 0 0 13 18Z`,INK,true)+
  p(rect(17,22,14,3)+rect(17,28,14,3)+rect(17,34,9,3),INK)+
  p(circle(36,38,7),R)+p(circle(36,38,3),IV));
// 5. Formazione: libro aperto da due archi su un'asta
ic['formazione']=svg('Formazione',
  p('M22.5 13A22 9 0 0 0 3 10.5V37.5A22 9 0 0 1 22.5 40Z',INK)+
  p('M25.5 13A22 9 0 0 1 45 10.5V37.5A22 9 0 0 0 25.5 40Z',R));
// 6. Voce: l'umanoide che parla al pubblico
ic['voce']=svg('Umanoide che parla',
  p(circle(15,17,8),INK)+p(rect(9,27,12,17),INK)+
  p(band(25,18,10,6.5,55,-55),R)+p(band(25,18,18,14.5,55,-55),R));
for(const [k,v] of Object.entries(ic)) fs.writeFileSync(`${OUT}/${k}.svg`,v);
console.log(Object.keys(ic));
