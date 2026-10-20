// «Запекает» дополнения в пресеты через само приложение (так же, как кнопка «＋ Добавить в мир»).
// Запуск из корня репозитория:
//   python3 -m http.server 8815 &
//   ADDS=presets/addons/south-xxx.json NODE_PATH=$(npm root -g) node tools/bake.js
// ADDS — список через запятую. Перезаписывает presets/south.json.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..');const PORT=process.env.PORT||8815;
(async()=>{const b=await chromium.launch();
for(const f of ['presets/south.json']){
 const ctx=await b.newContext();const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('dialog',d=>{errs.push('dialog:'+d.message());d.accept();});
 await p.goto(`http://localhost:${PORT}/?b=`+Date.now());await p.waitForTimeout(3000);
 const out=await p.evaluate(async([f,ADDS])=>{S.worlds=[];S.chars=[];S.scenes=[];
   const src=await (await fetch(f,{cache:'no-store'})).text();const orig=JSON.parse(src);
   await importFile(new Blob([src]));const w=S.worlds[0];
   for(const a of ADDS)await importFile(await (await fetch(a,{cache:'no-store'})).blob(),w.id);
   const o=Object.assign({},orig,{worlds:[w],chars:charsOf(w.id),scenes:S.scenes.filter(x=>x.worldId===w.id)});
   return JSON.stringify(o,null,1);},[f,(process.env.ADDS||'').split(',').filter(Boolean)]);
 fs.writeFileSync(path.join(ROOT,f),out);console.log(f,out.length,errs);await ctx.close();}
await b.close();})();
