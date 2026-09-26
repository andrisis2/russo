# STATO DEL PROGETTO — Russo (per riprendere il lavoro)

> File di continuità: dice **a che punto siamo** e **come si va avanti**. Aggiornare a ogni blocco di lezioni.

## Coordinate progetto
- **Cartella locale:** `C:\Users\weare\Desktop\claude files\4Claude\Projects\russo`
- **Repo GitHub:** https://github.com/andrisis2/russo  (account: `andrisis2`)
- **App live (GitHub Pages):** https://andrisis2.github.io/russo/
- **Deploy:** `git push origin main` → Pages rigenera in ~1 min. L'autenticazione è già salvata (Git Credential Manager): **nessun token serve**.
- **Livello utente:** A1. **Ritmo concordato:** a blocchi (~5 lezioni). **Formato confermato:** riassunto + trascrizione + vocaboli/frasi/grammatica nell'app.

## Com'è fatta l'app
- `index.html` — PWA, legge `knowledge.json`. Home: saluto in russo (tocca per ascoltarlo), card **Ripasso del giorno** con anello di avanzamento e serie (`makeDailyHero`/`dailyProgress`), **I miei esercizi**, poi due schede: **Pratica** (Flashcard, Scrittura, Coniugazione, **Frasi** = hub `runFrasiHub` con Completa e ascolta / Componi / Dettato di frasi, Numeri e ore, Palestra di grammatica con anche le regole in breve e il loro quiz, **Giochi** = hub `runGiochi` con Sfida lampo e Memory, Progressi, Vika) e **Teoria** (Vocabolario, Verbi, Dialoghi, Frasario, **Letture e cultura** = `runCultura` con racconti, proverbi, pillole, parole trappola, Cirillico, Regole grammaticali con il rimando alle regole in breve, Frasi&grammatica). 8 tessere per scheda. Le vecchie modalità (`phrase`, `compose`, `memory`, `lampo`, `letture`, `gram`) funzionano ancora con `start()` ma non hanno più una tessera. In alto: saluto + **chip del livello** (`makeLivelloChip`), Ripasso del giorno, **Percorso A1** (`makePercorsoCard`), I miei esercizi, poi la fascia **«Oggi per te»** (`makeOggi`): Parola del giorno (`makeWotd`/`parolaDelGiorno`, fissata per la giornata), Proverbio del giorno e Pillola di cultura (scelti in base al giorno, `giornoN`). Le sezioni in `NUOVE_SEZIONI` hanno l'etichetta «Nuovo» finché non si aprono. SRS (Leitner) salvato in `localStorage`.
- **Navigazione**: `navigateTo(fn)` spinge ogni schermata nella storia (anche i sotto-menu: livelli, tempi, quiz), il tasto Indietro torna al livello precedente e ritrova il punto a cui si era scorso (`_scrollAt`). `header(titolo, {narrow})` apre una schermata interna col titolo nella barra; ciò che va chiuso uscendo (microfono di Vika, timer, tasti) si registra con `onLeave(fn)`.
- **Grafica**: tutti i colori sono token CSS in `:root` (tema scuro = stessi token ridefiniti, niente eccezioni per componente); icone SVG in uno sprite in cima al `<body>`, usate con `ic('nome')`. Mura del Cremlino nella barra: alte con le torri in home (`body.is-home`), striscia sottile nelle altre pagine.
- **Tastiera cirillica a schermo** (`makeCyrKeyboard`): in Scrittura e Coniugazione (si spegne dalle Impostazioni).
- **Scrittura** (`runScrittura`): dall'italiano o sotto dettato, tastiera cirillica a schermo (`KBD_ROWS`), confronto indulgente (`normWrite`: niente maiuscole/accenti, ё=е).
- **Dialoghi** (`runDialoghi` → `runDialogo`): 16 scene in `knowledge.json` → `dialoghi` (generate da `scripts/add_dialoghi.py`, idempotente). Ascolto a due voci (`speakAs`: seconda voce russa se c'è, altrimenti tono più alto), traduzione nascondibile, frasi chiave, nota culturale; **Recita** (`runRecita`: l'altro parla, tu dici le tue battute, con `SpeechRecognition` se disponibile e confronto parola per parola `confrontaDetto`) e quiz **Cosa rispondi?** (`runDlgQuiz`). Le tue battute si salvano negli esercizi (scheda Frasi).
- **Numeri e ore** (`runNumeri`): `numRu(n, fem)` scrive i numeri in lettere fino a 999 999 999, `pluralRu(n, [1, 2-4, 5+])`, `oraRu`/`oraColloquiale` per l'ora, `clockSVG`. Esercizi: dettato (`runNumDettato`), leggi il numero, che ore sono, quanto costa (rubli). L'intervallo di numeri è in `settings().numRange`.
- **Frasario** (`runFrasario`/`runFrasarioCat`): le frasi di `frasi[]` raggruppate per tag in `FRASARIO_CAT`, più le frasi chiave dei dialoghi. **Componi la frase** (`runComponi`): frasi da `frasi[]` o dai dialoghi, per lunghezza; anche da una categoria del frasario o dalle frasi salvate negli esercizi.
- **Percorso A1** (`runPercorso` → `runTappa`): 12 tappe in `knowledge.json` → `percorso`, ognuna con passi `{t, titolo, …}` che lanciano gli esercizi esistenti (`lanciaPasso`: flash per tag, frasi, componi, recita/dlgquiz di un dialogo, lettura, numeri con intervallo, ore, prezzi, casi, moto, quiz alfabeto). `avviaPasso` imposta `_passoAttivo`; `finish()` chiama `passoCompletato(pct)` (soglia 60%, 0 per flashcard e recita) e mostra `passoBox`. Tappa successiva sbloccata quando la precedente è completa. Stato in `russo_extra_v1.percorso`.
- **Letture** (`runLetture`/`runLettura`): 10 racconti (`letture[]`, `glossarioLetture` per le parole frequenti); tocco su una parola → popup con traduzione (glossario → dizionario → forme dei verbi → nome proprio) e ＋ esercizi; ascolto frase per frase; domande di comprensione (`runLetturaQuiz`).
- **Cultura e curiosità** (`runCultura`): proverbio del giorno (condivisibile), `runProverbi` + quiz, «Russia in pillole» (`cultura[]`, `runPillola`), falsi amici e parole gemelle (`runParoleTrappola`, `runQuizTrappola`).
- **Palestra di grammatica** (`runPalestra`): «Casi al volo» (`casi[]` + `casiNomi` con le 6 forme singolari: i distrattori sono le altre forme dello stesso nome; `runCasi(caso)`) e verbi di moto (`verbiMoto`: teoria + `runMotoQuiz`).
- **Sfida lampo** (`runLampo`): 60 secondi di parole RU→IT, record in `russo_extra_v1.lampo`. **Dettato di frasi** (`runDettatoFrasi`) nel menu di Scrittura.
- **Spiega e Salva ovunque** (26/09/2026): ogni parola o frase proposta ha la barra `azioniTesto(ru, it, opts)` (Spiega · Salva · Pronuncia) oppure, negli elenchi, la lente `lensBtn` e il ＋ `saveMini`; righe «parola — traduzione» con `kwRow`. «Spiega» apre un pannello dal basso (`sheetApri`, con pila e «indietro»): `pagFrase` smonta la frase parola per parola, `pagParola` mostra la scheda della parola (analisi, declinazione/coniugazione, esempi da `frasiConParola`). L'analisi (`analizzaParola`) usa `indiceForme()`: indice di ~15.000 forme costruito al primo uso da preposizioni (`PREP_INFO`), pronomi (`PRONOUN_DECL`, `ADJLIKE_PRON`), numerali (`NUMERALI`), parole-funzione (`PAROLE_FUNZIONE`), coniugazioni di `verbi[]`, declinazioni generate di nomi e aggettivi di `voci[]`, glossario dei racconti; il caso si sceglie guardando la parola prima (preposizione o numero). Se la frase è in `frasiGrammar` si usano le note scritte a mano. Salvataggi senza doppioni: `salvaFrase`/`salvaParola` (per testo; ai verbi si aggiunge anche il drill di coniugazione). Il pannello si chiude cambiando schermata (`leaveScreen`).
- **Punti e livelli**: `recordActivity()` dà 10 punti per risposta giusta e 2 per sbagliata (`addXP`), più bonus (ripasso completato 50, dialogo recitato 40, lettura 40, passo 30, tappa 100, record lampo 20). `LIVELLI_XP` (Новичок → Легенда); `toast()` per il cambio di livello. Totale in `russo_extra_v1.xp`, per giorno in `russo_activity_v1[data].xp`.
- **Errori** (`russo_errori_v1`, max 150): `grade()` e i quiz con `Q.err` salvano le risposte sbagliate; scheda «Errori» negli Esercizi e ripasso `runErrori`.
- **Pronuncia** (`makeMicBtn`): riconoscimento vocale del browser in Flashcard, Frasi & ascolto, Parola del giorno. **Condividi** (`condividiCard`): immagine JPEG 1080×1350 via Web Share (o download).
- **Cremlino vivo** (`aggiornaCremlino`): di sera (19–6) finestre accese, stelle e luna; da dicembre a febbraio neve sui tetti e fiocchi (`body.sera`, `body.inverno`).
- **Promemoria** (Impostazioni → `scaricaPromemoria`): file `.ics` con evento giornaliero ricorrente e avviso.
- **Progressi** (`runProgressi`): livello e riepilogo settimana (`makeLivelloCard`), **traguardi** (`traguardi()`, 20 badge), stato del dizionario, mappa attività 18 settimane (chiave `russo_activity_v1`, alimentata da `grade()`), previsione ripassi a 7 giorni, parole ostiche.
- **Impostazioni** (`runImpostazioni`, chiave `russo_settings_v1`): tema auto/chiaro/scuro (`data-theme` sull'`<html>`), velocità TTS, carte al giorno, tastiera cirillica, **export/import JSON dei progressi** e azzeramento.
- Chiavi in `localStorage`: `russo_srs_v1`, `russo_daily_v1`, `russo_esercizi_v1`, `russo_user_voci`, `russo_activity_v1`, `russo_settings_v1`, `russo_memory_best_v1`, `russo_extra_v1` (punti, dialoghi, numeri, frasi composte, parola del giorno, percorso, letture, pillole, record lampo), `russo_errori_v1`, `russo_sezioni_viste`, `vika_*`.
- `knowledge.json` — fonte unica: `meta`, `alfabeto[33]`, `voci[]`, `frasi[]`, `grammatica[]` (ogni regola ha `drill[]` di coppie domanda/risposta), `frasiGrammar[]`, `riferimento[]`, `verbi[]`, `dialoghi[]` (`{id, icona, titolo, titoloRu, scena, livello, ruoli:{A,B}, battute:[{s,ru,it}], parole:[{ru,it}], nota}`; il ruolo «Вы» è quello di chi studia). Le voci dai video sono taggate `video-NN`.
- `note.md` — spiegazioni discorsive. `lezioni/` — un `.md` di riassunto per lezione + trascrizioni `*_transcript.txt`. `scripts/extract_lesson.py` — estrae/pulisce una porzione del VTT.

## Pipeline video → app (come trascrivere il prossimo pezzo)
1. VTT già scaricato: `lezioni/corso-completo.it-orig.vtt` (sottotitoli italiani auto-generati).
   - Per ri-scaricarlo: `python -m yt_dlp --skip-download --write-auto-subs --sub-langs it-orig --sub-format vtt -o "lezioni/corso-completo.%(ext)s" "https://youtu.be/hXWiEWwLy98"`
2. Taglia la lezione: `python scripts/extract_lesson.py "lezioni/corso-completo.it-orig.vtt" <START hh:mm:ss> <END hh:mm:ss> "lezioni/LXX_transcript.txt"`
3. **Leggi** la trascrizione (tool Read, non PowerShell: il file è UTF-8 corretto, la console PS lo mostra come mojibake).
4. **Ricostruisci il cirillico corretto**: l'ASR è italiano e storpia le parole russe → scrivo io le forme giuste in base al contesto.
5. Scrivi `lezioni/lezione-XX.md` (riassunto) e aggiungi voci/frasi/grammatica a `knowledge.json` (continua la numerazione id), aggiorna `meta.versione` e `meta.fonti`.
6. `git add -A; git commit; git push origin main`. Poi verifica `https://andrisis2.github.io/russo/knowledge.json`.

### Note tecniche / trappole
- **PowerShell ha rete, il tool Bash NO** (restituisce HTTP 000): usare PowerShell per yt-dlp/curl/git push.
- **Messaggi di commit:** niente virgolette doppie dentro il messaggio (in PS 5.1 spezzano l'argomento). I warning LF→CRLF sono innocui.
- yt-dlp installato via `python -m pip install yt-dlp` → si invoca `python -m yt_dlp`.

## VIDEO SORGENTE
- **Titolo:** *Russo Facile: Corso di Russo Completo per Principianti* — canale **Russo Facile con Yula**
- **YouTube id:** `hXWiEWwLy98`  ·  **Durata:** 523 min (~8h43)  ·  **Lingua:** it-orig (spiega in italiano), nessun sottotitolo manuale.

## STATO AVANZAMENTO (capitoli del video)
Legenda: ✅ fatto · ⬜ da fare · ⏪ **PROSSIMO**

| Inizio | Capitolo | Stato |
|---|---|---|
| 00:00:00 | Benvenuto – Come imparare il russo | ⬜ (introduttivo, saltato) |
| 00:04:14 | Lezione 01 | ✅ |
| 00:28:01 | L.02 | ✅ |
| 00:36:07 | L.03 | ✅ |
| 00:49:17 | 1000 parole russe | ✅ |
| 01:00:33 | L.04 | ✅ |
| 01:27:46 | L.05 | ✅ |
| 02:08:55 | **L.06** | ⏪ PROSSIMO |
| 02:33:58 | L.07 | ⬜ |
| 02:52:18 | Verbi russi (помнить, смотреть, верить, стоять/стоить, слышать, лежать, молчать, видеть, ненавидеть, сидеть) | ⬜ |
| 03:16:06 | L.08 | ⬜ |
| 03:38:27 | I verbi difficili | ⬜ |
| 03:49:08 | L.09 | ⬜ |
| 04:10:23 | L.10 | ⬜ |
| 04:28:28 | L.11 | ⬜ |
| 04:32:14 | L.12 | ⬜ |
| 05:01:11 | L.13 | ⬜ |
| 05:24:06 | L.14 | ⬜ |
| 05:40:41 | L.15 | ⬜ |
| 05:59:48 | L.16 | ⬜ |
| 06:38:07 | L.17 | ⬜ |
| 06:42:54 | L.18 | ⬜ |
| 06:58:35 | L.19 | ⬜ |
| 07:16:07 | L.20 "La mia città" | ⬜ |
| 07:29:07 | L.21 | ⬜ |
| 07:38:13 | L.22 | ⬜ |
| 07:54:06 | L.23 "Mi si è scaricata la batteria" | ⬜ |
| 08:13:08 | L.24 | ⬜ |
| 08:42:44 | Corso completato! Salutiamoci | ⬜ (chiusura) |

## CONTENUTI GIÀ NELL'APP (per non duplicare id)
- `knowledge.json` **versione 23** — **1631 voci** (ultimo id `v1631`), **190 frasi** (ultimo `f195`), **12 regole** quiz (ultimo `g012`), 120 `frasiGrammar` (id 100–219), 18 schede `riferimento` (`r018`), 216 `verbi` (`verb216`), **16 dialoghi** (id testuali: `bar`, `ristorante`… `museo`). Dal secondo blocco (`scripts/add_contenuti_2.py`, idempotente): 10 `letture`, 38 `proverbi`, 16 schede `cultura`, 24 `falsiAmici`, 48 `paroleGemelle`, 50 `casi` (+ `casiNomi`), 20 frasi in `verbiMoto`, 12 tappe / 52 passi in `percorso`.
- **Sezione `riferimento`** (chiave a parte): 8 schede di consultazione "Regole grammaticali" (`r001`–`r008`: sei casi, pronomi declinati, possessivi, verbi al presente, passato, aspetto, plurale, numeri). Generata da `scripts/add_riferimento.py` (idempotente). NON sono drill: solo display + tap-per-ascoltare. Resa in `index.html` da `runReference()`. **Service worker: cache attuale `russo-v53`** (se modifichi `index.html` ricordati di bumpare la cache in `sw.js`, altrimenti i client di ritorno non vedono il nuovo file).
- **Tema grafico**: chiaro di default, scuro automatico o forzato (token in `:root` di `index.html`, `theme_color` bianco in `manifest.json`). Card bianche con ombre morbide, icone SVG su quadrati a gradiente, rosso Cremlino + blu come accenti, oro per serie e record.
- Lezioni elaborate: **L01, L02, L03, 1000-parole, L04, L05**.
- Prossimi id da usare: voci `v1632…`, frasi `f196…`, grammatica `g013…`, frasiGrammar `220…`, riferimento `r019…`, verbi `verb217…`.

## ➡️ PROSSIMA AZIONE
**Le lezioni di Yula sono in pausa per scelta dell'utente (26/09/2026)**: non riprendere la trascrizione del video se non la chiede di nuovo. La tabella qui sopra resta come promemoria (L.06 sarebbe la prossima).
Si lavora invece su contenuti e sezioni nuove dell'app (es. altri dialoghi in `scripts/add_dialoghi.py`, più frasi per il frasario, nuovi esercizi).
