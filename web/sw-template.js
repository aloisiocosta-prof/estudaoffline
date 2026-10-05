const CACHE = 'estudaoffline-__VERSION__';
const FILES = __FILES__;
const scope = new URL(self.registration.scope);
self.addEventListener('install', event => event.waitUntil((async () => {
  const cache = await caches.open(CACHE);
  // Fail the installation if any required asset cannot be fetched.
  await cache.addAll(FILES.map(f => new URL(f, scope).href));
  await self.skipWaiting();
})()));
self.addEventListener('activate', event => event.waitUntil((async () => {
  // Keep older assets for still-open tabs. Browser cache eviction remains possible.
  await self.clients.claim();
})()));
self.addEventListener('message', event => {
  if (event.data === 'OFFLINE_STATUS') event.source?.postMessage({type:'OFFLINE_READY', version:CACHE});
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== scope.origin || !url.pathname.startsWith(scope.pathname)) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    if (event.request.mode === 'navigate') {
      try { return await fetch(event.request); }
      catch { return await cache.match(new URL('index.html', scope).href) || Response.error(); }
    }
    const cached = await cache.match(event.request);
    return cached || fetch(event.request);
  })());
});
