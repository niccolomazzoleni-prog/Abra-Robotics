const {chromium}=require('/Users/niccolomazzoleni/Downloads/prisma-hero/node_modules/playwright');const path=require('path');
(async()=>{const [,,i,o,w,h,...ts]=process.argv;const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:+w,height:+h}});
const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+path.resolve(i));let last=0;for(const t of ts){await p.waitForTimeout(+t-last);last=+t;await p.screenshot({path:o.replace('.png','-'+t+'.png')});}
await b.close();console.log(errs.join('\n')||'nessun errore');})();
