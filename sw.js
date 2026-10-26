const C="zhivoymir-v274";
const FILES=["./","./index.html","./manifest.json","./icon-192.png","./icon-512.png"];
// мир по умолчанию (5.6 МБ) кладём в кэш заранее и без ошибки установки, если связь плохая — тогда карточка «Готовые миры» работает даже без сети
const BIG=["./presets/south-clean.json","./presets/maps/south-saltham.jpg"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(async c=>{await c.addAll(FILES);await Promise.all(BIG.map(u=>c.add(u).catch(()=>{})));}));self.skipWaiting();});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim();});
// сеть сначала, но если в кэше уже есть копия, а сеть молчит дольше 5 секунд — отдаём кэш (раньше на плохой связи всё зависало)
const net=(req,ms)=>new Promise((ok,no)=>{const t=ms?setTimeout(()=>no(new Error("timeout")),ms):0;fetch(req).then(r=>{clearTimeout(t);ok(r);},e=>{clearTimeout(t);no(e);});});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET"||u.origin!==location.origin)return;
  e.respondWith(caches.match(e.request).then(cached=>net(e.request,cached?5000:0).then(r=>{if(r.ok){const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));}return r;}).catch(()=>cached||Response.error())));});
