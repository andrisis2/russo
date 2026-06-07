# 💕 La Torre — mini gioco-sorpresa

Un piccolo gioco da browser: l'avatar di lei sale una **torre** rispondendo a
**3 domande** (la vostra storia). In cima arriva sul **tetto della moschea**
dove vi siete conosciuti, c'è il tuo avatar, e i due si **baciano** 💖.

## Come si apre
- In locale: apri `torre/index.html` con un doppio clic (si apre nel browser).
- Online (dopo il push): `https://andrisis2.github.io/russo/torre/`
  (GitHub Pages si aggiorna ~1 minuto dopo `git push`).

## Cosa devi mettere tu (2 minuti)

### 1) Le foto degli avatar
Metti in questa cartella `torre/` due foto **quadrate**, chiamate esattamente:
- `lei.jpg` — la faccia di lei
- `lui.jpg` — la tua faccia

Diventano le "facce" dei due personaggi. Se non le metti, compaiono due
faccine disegnate al loro posto (il gioco funziona lo stesso).

### 2) Le domande e i nomi
Apri `index.html` e cerca in alto la sezione **"⚙️ PERSONALIZZA QUI"**.
Lì cambi, in chiaro:
- `NOME_LEI` e `NOME_LUI` (i vostri nomi sotto gli avatar)
- l'elenco `DOMANDE`: per ognuna scrivi la domanda, le 3 risposte e l'indice
  della risposta giusta (`ok`: 0 = prima, 1 = seconda, 2 = terza)
- `MSG_FINE_TITOLO` e `MSG_FINE_SOTTO`: il messaggio dopo il bacio

> Se mi incolli tu le domande vere, te le inserisco io al posto dei segnaposto.

## Note
- Funziona anche da telefono (a tutto schermo).
- Se sbaglia tutte le risposte di un piano, riparte semplicemente lo stesso
  piano: niente "game over" cattivo, è un regalo 😊
