# STATO DEL PROGETTO — Russo (per riprendere il lavoro)

> File di continuità: dice **a che punto siamo** e **come si va avanti**. Aggiornare a ogni blocco di lezioni.

## Coordinate progetto
- **Cartella locale:** `C:\Users\weare\Desktop\claude files\4Claude\Projects\russo`
- **Repo GitHub:** https://github.com/andrisis2/russo  (account: `andrisis2`)
- **App live (GitHub Pages):** https://andrisis2.github.io/russo/
- **Deploy:** `git push origin main` → Pages rigenera in ~1 min. L'autenticazione è già salvata (Git Credential Manager): **nessun token serve**.
- **Livello utente:** A1. **Ritmo concordato:** a blocchi (~5 lezioni). **Formato confermato:** riassunto + trascrizione + vocaboli/frasi/grammatica nell'app.

## Com'è fatta l'app
- `index.html` — PWA, legge `knowledge.json`. 4 modi: Flashcard, Cirillico, Grammatica, Frasi&ascolto (TTS ru-RU). SRS (Leitner) salvato in `localStorage`.
- `knowledge.json` — fonte unica: `meta`, `alfabeto[33]`, `voci[]`, `frasi[]`, `grammatica[]` (ogni regola ha `drill[]` di coppie domanda/risposta). Le voci dai video sono taggate `video-NN`.
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
- `knowledge.json` **versione 4** — **87 voci** (ultimo id `v087`), **23 frasi** (ultimo `f023`), **12 regole** quiz (ultimo `g012`).
- **Sezione `riferimento`** (chiave a parte): 8 schede di consultazione "Regole grammaticali" (`r001`–`r008`: sei casi, pronomi declinati, possessivi, verbi al presente, passato, aspetto, plurale, numeri). Generata da `scripts/add_riferimento.py` (idempotente). NON sono drill: solo display + tap-per-ascoltare. Resa in `index.html` da `runReference()`. **Service worker a `russo-v2`** (se modifichi `index.html` ricordati di bumpare la cache in `sw.js`, altrimenti i client di ritorno non vedono il nuovo file).
- Lezioni elaborate: **L01, L02, L03, 1000-parole, L04, L05**.
- Prossimi id da usare: voci `v088…`, frasi `f024…`, grammatica `g013…`.

## ➡️ PROSSIMA AZIONE
Elaborare **L.06** (02:08:55 → 02:33:58) e proseguire il blocco fino a ~L.10, poi aggiornare questo file.
