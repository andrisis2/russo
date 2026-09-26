# Русский — app per imparare il russo

App web personale (PWA) per studiare il russo, livello A1+. Funziona offline e si installa sul telefono come un'app.

## Come funziona
- **`knowledge.json`** — la base di conoscenza: vocaboli, frasi, alfabeto e regole. È la fonte unica di verità che alimenta tutti gli esercizi. Quando studio nuovo materiale, le voci vengono aggiunte qui.
- **`note.md`** — spiegazioni grammaticali discorsive (lettura, non esercizi).
- **`index.html`** — l'app. In cima alla home il saluto in russo (tocca per ascoltarlo), la card del
  **Ripasso del giorno** con l'anello di avanzamento e la serie di giorni di fila, e **I miei esercizi**;
  sotto, due schede: **Pratica** e **Teoria** (si passa dall'una all'altra anche con uno swipe).

  **Pratica**
  - 📅 **Ripasso del giorno** — il mazzo quotidiano scelto dalla ripetizione dilazionata, con la serie di giorni di fila.
  - 🃏 **Flashcard** — vocaboli RU↔IT per livello o argomento (sistema Leitner: ciò che sbagli torna più spesso).
  - ✍️ **Scrittura** — l'unico esercizio in cui la parola russa va **prodotta**, non riconosciuta: dall'italiano o
    sotto **dettato**, con **tastiera cirillica a schermo** (niente layout russo da installare) e correzione
    lettera per lettera.
  - ✏️ **Coniugazione** — allenamento sulle forme verbali, con la stessa tastiera cirillica a schermo.
  - 💬 **Frasi & ascolto** — completa la frase + pronuncia (text-to-speech russo del dispositivo).
  - 🧠 **Memory** — abbinamento RU↔IT a tempo.
  - 📈 **Progressi** — quante parole sono imparate/in corso/da scoprire, precisione, mappa dello studio delle
    ultime 18 settimane, ripassi in arrivo nei prossimi 7 giorni e l'elenco delle **parole ostiche** (quelle che
    sbagli spesso) da allenare in un colpo solo.
  - 🎙️ **Conversa con Vika** — chiacchierata in russo con la tutor IA.

  **Teoria**
  - 📖 **Vocabolario** — dizionario con ricerca (prima le corrispondenze esatte) e argomenti; se una parola
    manca, la cerca online. ⚡ **Verbi** — coniugazioni complete, con ricerca e allenamento sul singolo verbo.
  - 🔤 **Cirillico** — alfabeto, pronuncia e quiz sulle lettere. 📚 **Regole grammaticali** — tabelle di
    consultazione con indice che segue la lettura.
  - 📐 **Grammatica** — regole in breve e quiz, anche su una regola sola. 🧩 **Frasi & grammatica** — frasi
    spiegate parola per parola, filtrabili per parola o regola.

- ⚙️ **Impostazioni** (in fondo alla home) — tema chiaro/scuro/auto, velocità della voce, quante carte al giorno,
  tastiera cirillica, e soprattutto **backup**: i progressi vivono solo sul dispositivo, quindi si possono
  esportare in un file JSON e reimportare altrove.
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
