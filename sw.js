// Service worker: l'app funziona anche offline.
// - Pagina (navigazioni), index.html, knowledge.json: prima la rete, così gli
//   aggiornamenti arrivano subito. Ma se la rete non risponde entro pochi
//   secondi (campo debole, Wi-Fi senza internet) si apre la copia in cache; la
//   risposta della rete, se poi arriva, aggiorna la cache per la volta dopo.
// - Font di Google: in una cache a parte che sopravvive agli aggiornamenti
//   dell'app (anche offline il testo resta in Inter invece di ripiegare sul
//   carattere di sistema). Senza copia e senza rete si rinuncia presto.
// - Il resto dello stesso sito (immagini…): prima la cache; ciò che arriva dalla
//   rete ci finisce dentro per la volta dopo.
// - Dizionario esteso (dizionario.txt, ~1,4 MB): si scarica la prima volta che
//   serve e resta in una cache a parte che sopravvive agli aggiornamenti
//   dell'app. Se si rigenera il file, cambiare il nome di CACHE_DIZ.
// - Vika e la ricerca online (altri siti) passano dritte: lì internet serve.
const CACHE = "russo-v58";
const CACHE_FONT = "russo-font";
const CACHE_DIZ = "russo-diz-1";

// Indispensabili per aprire l'app senza rete: se uno non si scarica,
// l'installazione fallisce e resta in uso il service worker di prima.
const ESSENZIALI = ["./", "./index.html", "./knowledge.json", "./manifest.json", "./icon.png"];
// Utili ma non indispensabili: un errore qui non blocca l'installazione.
const EXTRA = [
  "./splash.png", "./vika.png",
  "./splash-ios/splash-750x1334.jpg","./splash-ios/splash-828x1792.jpg",
  "./splash-ios/splash-1125x2436.jpg","./splash-ios/splash-1170x2532.jpg",
  "./splash-ios/splash-1179x2556.jpg","./splash-ios/splash-1242x2688.jpg",
  "./splash-ios/splash-1284x2778.jpg","./splash-ios/splash-1290x2796.jpg"
];

// Risorse sempre prese dalla rete se disponibile
const NETWORK_FIRST = ["knowledge.json", "index.html", "sw.js"];
const FONT_HOSTS = ["fonts.googleapis.com", "fonts.gstatic.com"];
// Quanto si aspetta la rete prima di ripiegare sulla copia in cache
const ATTESA_RETE = 2500;
// Dopo un'attesa andata a vuoto, per un po' si apre subito la cache (senza
// ripetere l'attesa per ogni file): la rete aggiorna comunque in sottofondo.
const PAUSA_RETE_LENTA = 30000;
let reteLentaFinoA = 0;

// cache:"reload" = scarica davvero dal server, non dalla cache HTTP del browser
const fresco = u => new Request(u, { cache: "reload" });

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c =>
    c.addAll(ESSENZIALI.map(fresco))
      .then(() => Promise.all(EXTRA.map(u => c.add(fresco(u)).catch(() => {}))))
  ).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE && k !== CACHE_FONT && k !== CACHE_DIZ).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});

// Risposta da tenere: ok e non dirottata altrove (una pagina di login del Wi-Fi
// non deve finire in cache al posto dei contenuti).
const daSalvare = r => r.ok && !r.redirected;
// Risposta da mostrare così com'è; altrimenti (errore del server, dirottamento)
// meglio la copia in cache, se c'è. Il rimando di una navigazione ("/russo" →
// "/russo/") lo segue il browser.
const usabile = r => r.type === "opaqueredirect" || (!r.redirected && r.status < 500);
const attesa = ms => new Promise(ok => setTimeout(ok, ms));

function primaLaRete(e){
  const req = e.request;
  // si scrive sotto la chiave senza query string (?fresh=… dopo "Aggiorna
  // app"), così resta sempre una sola copia per file
  const key = new URL(req.url); key.search = "";
  const dallaCache = () => caches.match(req, { ignoreSearch: true, ignoreVary: true })
    .then(r => r || (req.mode === "navigate" ? caches.match("./index.html", { ignoreVary: true }) : undefined));

  let salvataggio;
  const rete = fetch(req).then(r => {
    reteLentaFinoA = 0;
    if(daSalvare(r)){
      const copy = r.clone();
      salvataggio = caches.open(CACHE).then(c => c.put(key.toString(), copy));
    }
    return r;
  });
  // il service worker resta sveglio finché la copia nuova non è salvata,
  // anche se intanto la pagina ha già ricevuto quella in cache
  e.waitUntil(rete.then(() => salvataggio).catch(() => {}));

  return new Promise(resolve => {
    let fatto = false;
    const rispondi = r => { if(!fatto && r){ fatto = true; resolve(r); } return fatto; };
    const provaCache = () => dallaCache().then(rispondi, () => fatto);
    // senza copia in cache non c'è alternativa: si aspetta la rete
    const timer = setTimeout(() => {
      if(!fatto) reteLentaFinoA = Date.now() + PAUSA_RETE_LENTA;
      provaCache();
    }, Date.now() < reteLentaFinoA ? 0 : ATTESA_RETE);
    rete.then(r => {
      clearTimeout(timer);
      if(usabile(r)) return rispondi(r);
      return provaCache().then(ok => ok || rispondi(r));
    }, () => {
      // offline: la copia in cache, ignorando l'eventuale query string
      clearTimeout(timer);
      return provaCache().then(ok => ok || rispondi(Response.error()));
    });
  });
}

function font(e){
  const req = e.request;
  // gli indirizzi dei font non cambiano mai: basta la prima copia scaricata
  return caches.open(CACHE_FONT).then(c => c.match(req).then(hit => {
    if(hit) return hit;
    const rete = fetch(req).then(r => {
      if(r.ok || r.type === "opaque") return c.put(req, r.clone()).then(() => r, () => r);
      return r;
    });
    e.waitUntil(rete.catch(() => {}));
    // il foglio dei font blocca il disegno della pagina: se la rete è appesa
    // si rinuncia (testo nel carattere di sistema) e la copia arriverà dopo
    return Promise.race([rete, attesa(ATTESA_RETE).then(() => Response.error())]);
  }));
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if(req.method !== "GET") return;            // le chiamate a Vika (POST) passano dritte
  const url = new URL(req.url);
  const stessoSito = url.origin === self.location.origin;

  if(req.mode === "navigate" || (stessoSito && NETWORK_FIRST.some(f => url.pathname.endsWith(f)))){
    e.respondWith(primaLaRete(e));
    return;
  }

  if(FONT_HOSTS.includes(url.hostname)){
    e.respondWith(font(e));
    return;
  }

  if(stessoSito && url.pathname.endsWith("dizionario.txt")){
    e.respondWith(caches.open(CACHE_DIZ).then(c => c.match(req, { ignoreSearch: true }).then(hit => hit || fetch(req).then(r => {
      if(daSalvare(r)) e.waitUntil(c.put(req, r.clone()).catch(() => {}));
      return r;
    }))));
    return;
  }

  if(stessoSito){
    e.respondWith(caches.match(req, { ignoreSearch: true, ignoreVary: true }).then(hit => hit || fetch(req).then(r => {
      if(r.ok){ const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return r;
    })));
  }
});
