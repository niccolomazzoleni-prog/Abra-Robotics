// node raster.js in.svg out.png w h  (rende l'SVG a piena finestra)
const {chromium}=require('/Users/niccolomazzoleni/Downloads/prisma-hero/node_modules/playwright');
const path=require('path');
(async()=>{const [,,i,o,w,h]=process.argv;const b=await chromium.launch({channel:'chrome'});
const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
await p.goto('file://'+path.resolve(i));await p.waitForTimeout(150);
await p.screenshot({path:o,omitBackground:true});await b.close();})();
