const {chromium}=require('/Users/niccolomazzoleni/Downloads/prisma-hero/node_modules/playwright');const path=require('path');
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage();
for(const f of process.argv.slice(2)){await p.goto('file://'+path.resolve(f));await p.waitForTimeout(400);await p.pdf({path:f.replace('.html','.pdf').replace('applicazioni/','_lavoro/'),width:'794px',height:'1123px',printBackground:true});}
await b.close();})();
