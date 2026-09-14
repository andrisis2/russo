// Service worker minimale: tiene offline solo il guscio dell'app.
// I contenuti arrivano dall'API di GitHub e NON vanno messi in cache qui:
// se ne occupa l'app salvando l'ultima copia letta in localStorage.
const CACHE = 'articoli-v1';
const ASSETS = ['./', './index.html', './manifest.json', './icon.png', './icon-192.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // tutto ciò che non è dell'app (in primis api.github.com) passa diretto:
  // intercettarlo romperebbe autenticazione e salvataggi
  if (url.origin !== self.location.origin || e.request.method !== 'GET') return;

  // l'app si aggiorna da sola: prima la rete, la cache è la riserva
  e.respondWith(
    fetch(e.request)
      .then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return r;
      })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});
