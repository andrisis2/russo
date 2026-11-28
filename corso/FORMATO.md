# Formato dei sorgenti del corso

Una settimana per file: `corso/s01.txt` … `corso/s52.txt`. Si costruisce con:

```
python scripts/build_corso.py            # crea corso.json e stampa avvisi
python scripts/build_corso.py --accenta  # aggiunge gli accenti certi nei sorgenti
```

Per i controlli su accenti e parole servono `pip install pymorphy3 pymorphy3-dicts-ru`
e il dizionario di OpenRussian (CSV, CC BY-SA 4.0) in una cartella indicata da
`OPENRUSSIAN_DIR` (vedi l'intestazione dello script). Senza, il corso si costruisce
lo stesso.

## Struttura

```
# Settimana 3 | Famiglia e descrizioni

## Giorno 15 | La famiglia
obiettivo: Una frase che dice cosa saprai fare alla fine.
breve: Un punto chiave (va nel riepilogo della settimana). Anche più righe «breve:».
vedi: cyr, dialogo:bar, lettura:anna, ref:r001, numeri, ore, prezzi, casi, moto

### Lezione
Testo in markdown: **grassetto**, *corsivo*, elenchi con «- », tabelle con «|»,
riquadri con «> », sottotitoli con «#### ». Una riga «---» divide le pagine.
Le parole russe nel testo si toccano per ascoltarle.

### Parole
ма́ма = mamma [f]
жить = vivere [v impf; живу́, живёшь]
по-ру́сски = in russo [avv]

### Frasi
Э́то моя́ ма́ма. = Questa è mia mamma. // nota facoltativa

### Esercizi
? Domanda {risposta giusta | sbagliata | sbagliata} = traduzione // spiegazione
? Я ___ в Москве́. {живу́ | живёт | живёшь} = Vivo a Mosca.
> Он (чита́ть) → чита́ет = Lui legge.
> Scrivi «gatto» → кот / ко́шка
~ Я живу́ в Москве́. = Vivo a Mosca.
@ Магази́н рабо́тает до восьми́. → Fino a quando è aperto? {fino alle 8 | fino alle 18 | tutto il giorno} = Il negozio è aperto fino alle otto.
```

- **Parole**: `russo = italiano [tipo; nota]`. Tipi: `m f n pl mf` (nomi),
  `v impf` / `v pf` (verbi), `agg avv pron num prep cong part inter espr nome`.
  L'accento si segna con l'acuto combinante (U+0301) sulla vocale: `молоко́`.
  Una parola si introduce **una volta sola** in tutto il corso (lo script avvisa).
- **Esercizi**: `?` scelta multipla (la prima opzione è quella giusta: l'app
  le mescola; `___` nella domanda viene riempito con la risposta), `>` risposta
  da scrivere (alternative separate da ` / `), `~` frase da ricomporre,
  `@` **ascolto**: la frase russa si sente ma non si legge (si vede dopo la
  risposta); dopo `→` la domanda in italiano (senza, «Che cosa hai sentito?»),
  tra graffe le risposte (la prima è quella giusta), dopo `=` la traduzione.
- Il **7° giorno** di ogni settimana è il ripasso: ha una `### Lettura | Titolo russo | Titolo italiano`
  (righe `russo = italiano`) e `### Domande` (righe `?`). Riepilogo e test si
  generano da soli; il 28°, 56°… giorno aggiungono il test del modulo, il 365°
  l'esame finale.

Gli id di parole, frasi ed esercizi nascono dal testo russo: cambiando una frase
cambia anche il suo id (e il suo ripasso riparte da zero).

## Controlli dello script

- **Accenti**: con il dizionario di OpenRussian lo script segnala gli accenti
  che mancano o che sembrano sbagliati; `--accenta` aggiunge quelli certi. Le
  parole giuste che il dizionario non conosce (nomi propri, forme rare, parole
  nuove come `гу́глить`) vanno in `corso/parole_ok.txt`.
- Dopo un monosillabo accentato la parola è atona e non si accenta
  (`не́ было`, `за́ городом`, `на́ уши`); i prefissi (`пере-`, `вы-`) non si
  accentano.
- Avvisa anche di: parole già introdotte in un altro giorno, opzioni ripetute,
  lettere latine dentro parole russe, giorni senza lezione o (al 7° giorno)
  senza lettura.

