# Русский — app per imparare il russo

App web personale (PWA) per studiare il russo, livello A1+. Funziona offline e si installa sul telefono come un'app.

## Come funziona
- **`knowledge.json`** — la base di conoscenza: vocaboli, frasi, alfabeto e regole. È la fonte unica di verità che alimenta tutti gli esercizi. Quando studio nuovo materiale, le voci vengono aggiunte qui.
- **`note.md`** — spiegazioni grammaticali discorsive (lettura, non esercizi).
- **`index.html`** — l'app: 4 modalità di esercizio.
  - 🃏 **Flashcard** — vocaboli/frasi RU↔IT con ripetizione dilazionata (sistema Leitner: ciò che sbagli torna più spesso).
  - 🔤 **Cirillico** — riconoscere lettere e leggere parole.
  - 📐 **Grammatica** — generi, pronomi, regole, con drill.
  - 💬 **Frasi & ascolto** — completa la frase + pronuncia (text-to-speech russo del dispositivo).
- I progressi si salvano in `localStorage` sul dispositivo.

## Provarla in locale
```bash
# dalla cartella del progetto
python -m http.server 8000
# poi apri http://localhost:8000
```
> Serve un server locale (non aprire il file con doppio click): l'app carica `knowledge.json` via fetch e registra il service worker, cose che richiedono `http://`.

## Pubblicarla (GitHub Pages)
1. Crea un repo su GitHub e fai push di questa cartella.
2. Settings → Pages → Source: branch `main`, cartella `/root`.
3. Apri l'URL pubblicato sul telefono → menu browser → **"Aggiungi a schermata Home"**.

## Aggiungere materiale
Mando il materiale di studio → le voci vengono inserite in `knowledge.json` (e le spiegazioni lunghe in `note.md`) → l'app pesca automaticamente i nuovi contenuti.
