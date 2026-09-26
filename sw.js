// Service worker: l'app funziona anche offline.
// - Pagina (navigazioni), index.html, knowledge.json, sw.js: prima la rete, così
//   gli aggiornamenti arrivano subito; la cache serve solo quando si è offline.
// - Font di Google: salvati in cache al primo uso (anche offline il testo resta
//   in Inter invece di ripiegare sul carattere di sistema).
// - Il resto dello stesso sito (immagini…): prima la cache; ciò che arriva dalla
//   rete ci finisce dentro per la volta dopo.
const CACHE = "russo-v51";
const ASSETS = [
  "./", "./index.html", "./knowledge.json", "./manifest.json", "./icon.png", "./splash.png", "./vika.png",
  "./splash-ios/splash-750x1334.jpg","./splash-ios/splash-828x1792.jpg",
  "./splash-ios/splash-1125x2436.jpg","./splash-ios/splash-1170x2532.jpg",
  "./splash-ios/splash-1179x2556.jpg","./splash-ios/splash-1242x2688.jpg",
  "./splash-ios/splash-1284x2778.jpg","./splash-ios/splash-1290x2796.jpg"
];

// Risorse sempre prese dalla rete se disponibile
const NETWORK_FIRST = ["knowledge.json", "index.html", "sw.js"];
const FONT_HOSTS = ["fonts.googleapis.com", "fonts.gstatic.com"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if(req.method !== "GET") return;            // le chiamate a Vika (POST) passano dritte
  const url = new URL(req.url);
  const stessoSito = url.origin === self.location.origin;

  const isNetFirst = req.mode === "navigate" || (stessoSito && NETWORK_FIRST.some(f => url.pathname.endsWith(f)));
  if(isNetFirst){
    e.respondWith(
      fetch(req).then(r => {
        if(r.ok){
          const copy = r.clone();
          // si scrive sotto la chiave senza query string (?fresh=… dopo "Aggiorna
          // app"), così resta sempre una sola copia per file
          const key = new URL(req.url); key.search = '';
          caches.open(CACHE).then(c => c.put(key.toString(), copy));
        }
        return r;
      }).catch(() =>
        // offline: la copia in cache, ignorando l'eventuale query string
        caches.match(req, { ignoreSearch: true })
          .then(r => r || (req.mode === "navigate" ? caches.match("./index.html") : undefined))
          .then(r => r || Response.error())
      )
    );
    return;
  }

  if(FONT_HOSTS.includes(url.hostname)){
    // gli indirizzi dei font non cambiano mai: basta la prima copia scaricata
    e.respondWith(caches.open(CACHE).then(c => c.match(req).then(hit => hit || fetch(req).then(r => {
      if(r.ok || r.type === "opaque") c.put(req, r.clone());
      return r;
    }))));
    return;
  }

  if(stessoSito){
    e.respondWith(caches.match(req, { ignoreSearch: true }).then(hit => hit || fetch(req).then(r => {
      if(r.ok){ const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return r;
    })));
  }
});
