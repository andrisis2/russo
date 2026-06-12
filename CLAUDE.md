# Progetto Russo — istruzioni per Claude

App PWA per imparare il russo, alimentata dai video di "Russo Facile con Yula".

## 🌳 Git: parti SEMPRE da origin/main quando crei un branch
**Il `main` locale può essere disallineato da `origin/main`** (è già successo: storie del tutto scollegate, senza antenato comune, perché l'ambiente remoto a volte clona un `main` vecchio/orfano). `origin/main` è l'UNICA fonte di verità (da lì pubblica GitHub Pages). Quindi:
- **Prima di creare un branch** fai sempre: `git fetch origin` e poi `git checkout -B <nuovo-branch> origin/main` (NON `git checkout -b <branch>` dal main locale).
- **Non fidarti del `main` locale** senza prima un `git fetch`. Per controllare l'allineamento: `git merge-base main origin/main` (se è vuoto, le storie sono scollegate → ricrea il branch da `origin/main`).
- Se devi lavorare su `main`: `git fetch origin && git checkout main && git reset --hard origin/main`.
- Imposta `git config pull.ff only` per evitare il prompt "Need to specify how to reconcile divergent branches".

## ⚙️ Workflow merge (preferenza dell'utente)
Quando l'utente chiede una modifica, dopo aver finito (commit + push + apertura PR) **fai tu il merge della PR senza chiedere conferma**: porta la PR da draft a "ready" e fai squash-merge su `main`. **Non chiedere "vuoi che faccia il merge?"** — è già autorizzato in modo permanente. Comunica solo l'esito (PR mergiata + link). Se invece qualcosa è ambiguo o rischioso nel *contenuto* della modifica, chiedi pure prima di procedere; l'auto-merge riguarda solo il passaggio finale di integrazione.

## ⚠️ PRIMA DI TUTTO
**Leggi `STATO.md`**: dice a che punto siamo col video e come proseguire la trascrizione. È la fonte di verità sull'avanzamento.

## Dove vive tutto (è TUTTO su GitHub)
- **Repo:** https://github.com/andrisis2/russo (account `andrisis2`)
- **App live (GitHub Pages):** https://andrisis2.github.io/russo/
- **Deploy:** ogni modifica si pubblica con `git push origin main` (auth già salvata via Git Credential Manager: niente token). Pages rigenera in ~1 min.

## Struttura
- `index.html` — l'app (PWA, 4 modi: flashcard, cirillico, grammatica, frasi+TTS; SRS in localStorage)
- `knowledge.json` — fonte unica dei contenuti (alfabeto, voci, frasi, grammatica con drill)
- `note.md` — spiegazioni grammaticali discorsive
- `lezioni/` — un riassunto `lezione-XX.md` per lezione + trascrizioni `*_transcript.txt` + il VTT del corso
- `scripts/extract_lesson.py` — taglia/pulisce una porzione del VTT per timestamp

## Pipeline "video → app" (per trascrivere il prossimo pezzo)
1. `python scripts/extract_lesson.py "lezioni/corso-completo.it-orig.vtt" <START hh:mm:ss> <END hh:mm:ss> "lezioni/LXX_transcript.txt"`
2. Leggi la trascrizione col tool Read (UTF-8 ok; la console PowerShell la mostra come mojibake, è normale).
3. Ricostruisci il cirillico CORRETTO: l'ASR è italiano e storpia le parole russe.
4. Scrivi `lezioni/lezione-XX.md` (riassunto) + aggiungi voci/frasi/grammatica a `knowledge.json` (continua la numerazione id, aggiorna `meta.versione`).
5. `git add -A; git commit; git push origin main`, poi verifica `https://andrisis2.github.io/russo/knowledge.json`.

## Trappole tecniche
- **Il tool Bash NON ha rete (HTTP 000); usa PowerShell** per yt-dlp / curl / git push.
- **Messaggi di commit: niente virgolette doppie** (in PowerShell 5.1 spezzano l'argomento `-m`).
- yt-dlp si invoca con `python -m yt_dlp`.
