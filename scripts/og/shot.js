const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1200,height:630}});p.on('pageerror',e=>console.log(e.message));
await p.goto('file:///home/claude/og/og.html');await p.waitForFunction(()=>document.title==='listo',null,{timeout:60000});await p.waitForTimeout(500);
await p.screenshot({path:'/home/claude/og/og-image.png'});await b.close()})();
