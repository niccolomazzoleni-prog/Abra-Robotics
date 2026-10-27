const {chromium}=require('/Users/niccolomazzoleni/Downloads/prisma-hero/node_modules/playwright');
const fs=require('fs');const D='/Users/niccolomazzoleni/Abra-Robotics-brand/brand/02-directions/B-umanesimo/applicazioni/';
(async()=>{const b=await chromium.launch({channel:'chrome'});
for(const n of ['preventivo-cover','preventivo-interna']){const p=await b.newPage();const ext=[];
 await p.route(u=>!u.href.startsWith('file:'),r=>{ext.push(r.request().url());r.abort()});
 await p.goto('file://'+D+n+'.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
 const out=D+n+'.pdf';await p.pdf({path:out,format:'A4',printBackground:true,preferCSSPageSize:true});
 const pdf=fs.readFileSync(out,'latin1');const names=[...new Set((pdf.match(/\/BaseFont\s*\/[A-Za-z0-9+\-_]+/g)||[]).map(s=>s.split('/').pop()))];
 console.log(n,'pagine',(pdf.match(/\/Type\s*\/Page[^s]/g)||[]).length,'font',names.join(', '),'richieste esterne',ext.length);await p.close();}
await b.close();})();
