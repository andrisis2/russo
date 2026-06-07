// Service worker minimale: cache offline dell'app e dei dati
const CACHE = "russo-v19";
const ASSETS = [
  "./", "./index.html", "./knowledge.json", "./manifest.json", "./icon.png", "./splash.png", "./vika.png",
  "./splash-ios/splash-750x1334.jpg","./splash-ios/splash-828x1792.jpg",
  "./splash-ios/splash-1125x2436.jpg","./splash-ios/splash-1170x2532.jpg",
  "./splash-ios/splash-1179x2556.jpg","./splash-ios/splash-1242x2688.jpg",
  "./splash-ios/splash-1284x2778.jpg","./splash-ios/splash-1290x2796.jpg"
];

// Risorse sempre prese dalla rete se disponibile
const NETWORK_FIRST = ["knowledge.json", "index.html", "sw.js"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  const isNetFirst = NETWORK_FIRST.some(f => url.pathname.endsWith(f));
  if(isNetFirst){
    e.respondWith(
      fetch(e.request).then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return r;
      }).catch(() => caches.match(e.request))
    );
  } else {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
  }
});
