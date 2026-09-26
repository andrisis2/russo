# Русский — app per imparare il russo

App web personale (PWA) per studiare il russo, livello A1+. Funziona offline e si installa sul telefono come un'app.

## Come funziona
- **`knowledge.json`** — la base di conoscenza: vocaboli, frasi, alfabeto e regole. È la fonte unica di verità che alimenta tutti gli esercizi. Quando studio nuovo materiale, le voci vengono aggiunte qui.
- **`note.md`** — spiegazioni grammaticali discorsive (lettura, non esercizi).
- **`index.html`** — l'app. In cima alla home il saluto in russo (tocca per ascoltarlo), la card del
  **Ripasso del giorno** con l'anello di avanzamento e la serie di giorni di fila, **I miei esercizi** e la
  🗺️ **Percorso A1** (12 tappe che si sbloccano una dopo l'altra, dall'alfabeto alle feste), il tuo **livello**
  (punti per ogni risposta, da Новичок a Легенда) e la fascia **«Oggi per te»**: ✨ Parola del giorno,
  proverbio del giorno e pillola di cultura. Di sera il Cremlino accende le finestre, d'inverno nevica. Sotto, due schede: **Pratica** e **Teoria** (si passa dall'una all'altra anche con uno swipe).

  **Pratica**
  - 📅 **Ripasso del giorno** — il mazzo quotidiano scelto dalla ripetizione dilazionata, con la serie di giorni di fila.
  - 🃏 **Flashcard** — vocaboli RU↔IT per livello o argomento (sistema Leitner: ciò che sbagli torna più spesso).
  - ✍️ **Scrittura** — l'unico esercizio in cui la parola russa va **prodotta**, non riconosciuta: dall'italiano o
    sotto **dettato**, con **tastiera cirillica a schermo** (niente layout russo da installare) e correzione
    lettera per lettera. C'è anche il **dettato di frasi intere** (con la voce lenta 🐢).
  - 🎤 **Pronuncia** — nelle flashcard, nelle frasi e nella parola del giorno: dici la parola e il telefono
    controlla (riconoscimento vocale del browser, nessuna chiave).
  - ✏️ **Coniugazione** — allenamento sulle forme verbali, con la stessa tastiera cirillica a schermo.
  - 💬 **Frasi & ascolto** — completa la frase + pronuncia (text-to-speech russo del dispositivo).
  - 🧩 **Componi la frase** — la frase in italiano, le parole russe mescolate: toccale nell'ordine giusto
    (frasi brevi, medie, lunghe o prese dai dialoghi).
  - 🔢 **Numeri e ore** — convertitore cifre → russo, tabella da ascoltare, dettato di numeri, «leggi il numero»,
    **che ore sono?** (orologio, con la forma colloquiale: половина четвёртого…) e **quanto costa?**
    (рубль / рубля / рублей), più le regole in breve.
  - 🧠 **Palestra di grammatica** — **casi al volo** (50 frasi: scegli la forma giusta del nome, con la
    spiegazione dopo la risposta) e **verbi di moto** (идти / ходить / ехать / ездить: teoria e 20 frasi).
  - ⚡ **Sfida lampo** — quante parole traduci in 60 secondi? Con record e risultato da condividere.
  - 🧠 **Memory** — abbinamento RU↔IT a tempo.
  - 📈 **Progressi** — quante parole sono imparate/in corso/da scoprire, precisione, mappa dello studio delle
    ultime 18 settimane, ripassi in arrivo nei prossimi 7 giorni e l'elenco delle **parole ostiche** (quelle che
    sbagli spesso) da allenare in un colpo solo. Più 15 **traguardi** da sbloccare (serie, parole imparate,
    dialoghi recitati, numeri, frasi composte, letture, percorso…) e il riepilogo della settimana.
  - 🎙️ **Conversa con Vika** — chiacchierata in russo con la tutor IA.

  **Teoria**
  - 🎭 **Dialoghi** — 16 scene di tutti i giorni (bar, ristorante, albergo, stazione, taxi, farmacia, medico,
    telefono…): si ascoltano a due voci con la traduzione, si **recitano** facendo una delle parti (anche a
    voce, col riconoscimento vocale del telefono) e c'è il quiz «Cosa rispondi?». Frasi chiave e note culturali.
  - 💬 **Frasario** — frasi pronte divise per situazione, con ricerca, pronuncia e ＋ per allenarle.
  - 📖 **Letture** — 10 racconti A1 (Mosca, il mercato, la dacia, Capodanno, le notti bianche…): tocchi una
    parola e vedi la traduzione, li ascolti frase per frase e rispondi alle domande di comprensione.
  - 🏛️ **Cultura e curiosità** — proverbi russi con il nostro equivalente, 16 «pillole» su tradizioni e
    usanze, **falsi amici** (магазин non è il magazzino!) e parole gemelle, con quiz.
  - 📖 **Vocabolario** — dizionario con ricerca (prima le corrispondenze esatte) e argomenti; se una parola
    manca, la cerca online. ⚡ **Verbi** — coniugazioni complete, con ricerca e allenamento sul singolo verbo.
  - 🔤 **Cirillico** — alfabeto, pronuncia e quiz sulle lettere. 📚 **Regole grammaticali** — tabelle di
    consultazione con indice che segue la lettura.
  - 📐 **Grammatica** — regole in breve e quiz, anche su una regola sola. 🧩 **Frasi & grammatica** — frasi
    spiegate parola per parola, filtrabili per parola o regola.

- 🔖 **I miei esercizi** — parole, frasi e verbi salvati, più la scheda **Errori**: ogni risposta sbagliata, in
  qualsiasi esercizio, finisce lì per essere riallenata.
- ⚙️ **Impostazioni** (in fondo alla home) — tema chiaro/scuro/auto, velocità della voce, quante carte al giorno,
  tastiera cirillica, **promemoria giornaliero** nel calendario del telefono e soprattutto **backup**: i progressi vivono solo sul dispositivo, quindi si possono
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
