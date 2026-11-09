const CACHE_NAME = 'm82-sovereign-core-202610231054';
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.map(k => { if(k!==CACHE_NAME) return caches.delete(k) }))).then(()=>self.clients.claim()));
});
