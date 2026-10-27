const {chromium}=require('/Users/niccolomazzoleni/Downloads/prisma-hero/node_modules/playwright');const path=require('path');
(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage();
for(const f of process.argv.slice(2)){await p.goto('file://'+path.resolve(f));await p.waitForTimeout(400);await p.pdf({path:'/private/tmp/claude-501/-Users-niccolomazzoleni/3226bfba-c34c-47b6-b699-a19f144472ec/scratchpad/'+require('path').basename(f).replace('.html','.pdf'),width:'794px',height:'1123px',printBackground:true});}
await b.close();})();
