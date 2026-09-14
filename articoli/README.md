# Articoli — l'app

PWA per scrivere articoli: sfoglia a tendine le cartelle del repo **privato**
`andrisis2/prep`, apre i file, li mostra in markdown e li lascia modificare.
Ogni salvataggio è un commit vero su GitHub, così Claude ritrova le modifiche.

- Live: https://andrisis2.github.io/russo/articoli/
- Contenuti: repo `andrisis2/prep` (privato) — **qui non c'è nessun testo degli articoli**

## Perché sta dentro il repo `russo`

Serve un sito su HTTPS per installare la PWA sul telefono, e Pages pubblica solo
da repo pubblici. `prep` è privato, quindi qui vive solo l'interfaccia — che non
contiene segreti — mentre i contenuti restano privati. Spostare questi file in un
repo dedicato è banale: basta copiarli e aggiornare l'URL.

## File

- `index.html` — tutta l'app (interfaccia + logica, nessuna dipendenza esterna)
- `manifest.json`, `sw.js` — installazione sul telefono e guscio offline
- `icon.png`, `icon-192.png` — icona

## Come parla con GitHub

API `contents` e `git/trees`, autenticata con un token personale che l'utente
incolla una volta nelle impostazioni dell'app. Il token sta **solo** nel
`localStorage` del suo telefono: non è nel codice e non passa da nessun server.

Il service worker tiene in cache solo il guscio e lascia passare tutto ciò che
va verso `api.github.com`: intercettarlo romperebbe autenticazione e salvataggi.
