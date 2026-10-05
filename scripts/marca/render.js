const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1200,height:630}});
await p.goto('http://localhost:8765/brand/og.html');await p.waitForFunction(()=>document.title==='listo',null,{timeout:60000});
await p.screenshot({path:'og-image.png'});
const q=await b.newPage();
for(const s of [16,32,48,180,192,512]){await q.setViewportSize({width:s,height:s});
 await q.setContent(`<style>html,body{margin:0;background:transparent}</style><img src="http://localhost:8765/brand/favicon.svg" width="${s}" height="${s}">`);await q.waitForTimeout(150);
 await q.screenshot({path:`icon-${s}.png`,omitBackground:true});}
await b.close()})();
