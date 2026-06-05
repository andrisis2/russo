# -*- coding: utf-8 -*-
"""Aggiunge/aggiorna la sezione 'riferimento' (Regole grammaticali) in knowledge.json.
Idempotente: rilanciandolo riscrive la sezione con questi contenuti.
"""
import json, io, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(HERE, "knowledge.json")

riferimento = [
    {
        "id": "r001",
        "categoria": "I sei casi",
        "icona": "\U0001F5C2️",
        "sottotitolo": "A cosa serve ogni caso e che domanda risponde",
        "blocchi": [
            {"tipo": "testo", "testo": "Il russo declina sostantivi, aggettivi e pronomi in <b>6 casi</b>. Il caso indica la funzione della parola nella frase (chi fa, di chi, a chi...). Non c'è l'articolo."},
            {"tipo": "tabella",
             "intestazioni": ["Caso", "Domanda", "A cosa serve", "Esempio"],
             "righe": [
                 ["Nominativo", "кто? что?", "soggetto", "Это дом."],
                 ["Genitivo", "кого? чего?", "possesso «di», dopo нет / много", "нет времени"],
                 ["Dativo", "кому? чему?", "destinatario «a/per»", "Я звоню маме."],
                 ["Accusativo", "кого? что?", "oggetto diretto", "Я читаю книгу."],
                 ["Strumentale", "кем? чем?", "mezzo «con», professione", "Я пишу ручкой."],
                 ["Prepositivo", "о ком? где?", "luogo (в/на), argomento (о)", "в Москве"],
             ]},
            {"tipo": "nota", "testo": "Al livello A1 conta soprattutto riconoscere il <b>nominativo</b> (soggetto) e l'<b>accusativo</b> (oggetto). Gli altri arrivano poco a poco."},
        ],
    },
    {
        "id": "r002",
        "categoria": "Pronomi personali",
        "icona": "\U0001F464",
        "sottotitolo": "I pronomi soggetto declinati in tutti i casi",
        "blocchi": [
            {"tipo": "testo", "testo": "I pronomi personali cambiano forma in ogni caso. Riga = pronome, colonna = caso. Tocca una forma per ascoltarla."},
            {"tipo": "tabella",
             "intestazioni": ["", "Nom", "Gen", "Dat", "Acc", "Strum", "Prep"],
             "righe": [
                 ["io", "я", "меня", "мне", "меня", "мной", "обо мне"],
                 ["tu", "ты", "тебя", "тебе", "тебя", "тобой", "о тебе"],
                 ["lui / esso", "он / оно", "его", "ему", "его", "им", "о нём"],
                 ["lei", "она", "её", "ей", "её", "ей", "о ней"],
                 ["noi", "мы", "нас", "нам", "нас", "нами", "о нас"],
                 ["voi / Lei", "вы", "вас", "вам", "вас", "вами", "о вас"],
                 ["loro", "они", "их", "им", "их", "ими", "о них"],
             ]},
            {"tipo": "nota", "testo": "Dopo una <b>preposizione</b> i pronomi di 3ª persona prendono una <b>н-</b>: у <b>него</b>, к <b>нему</b>, с <b>ним</b>, о <b>нём</b>. Senza preposizione restano его / ему / им."},
            {"tipo": "nota", "testo": "<b>Вы</b> = «voi» ma anche «Lei» di cortesia (con la maiuscola nello scritto)."},
        ],
    },
    {
        "id": "r003",
        "categoria": "Aggettivi possessivi",
        "icona": "\U0001F511",
        "sottotitolo": "mio, tuo, nostro... concordano col sostantivo",
        "blocchi": [
            {"tipo": "testo", "testo": "Il possessivo concorda in <b>genere e numero</b> con la cosa posseduta (non con chi possiede, come in italiano)."},
            {"tipo": "tabella",
             "intestazioni": ["", "maschile", "femminile", "neutro", "plurale"],
             "righe": [
                 ["mio", "мой", "моя", "моё", "мои"],
                 ["tuo", "твой", "твоя", "твоё", "твои"],
                 ["nostro", "наш", "наша", "наше", "наши"],
                 ["vostro", "ваш", "ваша", "ваше", "ваши"],
             ]},
            {"tipo": "nota", "testo": "«suo» e «loro» sono <b>invariabili</b>: его (di lui), её (di lei), их (loro). Es. его мама, её дом, их книги."},
        ],
    },
    {
        "id": "r004",
        "categoria": "Verbi essenziali — presente",
        "icona": "\U0001F3C3",
        "sottotitolo": "La coniugazione al presente dei verbi più usati",
        "blocchi": [
            {"tipo": "testo", "testo": "Il presente ha 6 forme. Esistono due coniugazioni: la <b>1ª</b> (vocale -е-: знаю, знаешь) e la <b>2ª</b> (vocale -и-: говорю, говоришь). Tocca una forma per ascoltarla. (* = irregolare)"},
            {"tipo": "tabella",
             "intestazioni": ["Verbo", "я", "ты", "он / она", "мы", "вы", "они"],
             "righe": [
                 ["знать — sapere", "знаю", "знаешь", "знает", "знаем", "знаете", "знают"],
                 ["думать — pensare", "думаю", "думаешь", "думает", "думаем", "думаете", "думают"],
                 ["делать — fare", "делаю", "делаешь", "делает", "делаем", "делаете", "делают"],
                 ["работать — lavorare", "работаю", "работаешь", "работает", "работаем", "работаете", "работают"],
                 ["читать — leggere", "читаю", "читаешь", "читает", "читаем", "читаете", "читают"],
                 ["понимать — capire", "понимаю", "понимаешь", "понимает", "понимаем", "понимаете", "понимают"],
                 ["говорить — parlare", "говорю", "говоришь", "говорит", "говорим", "говорите", "говорят"],
                 ["любить — amare", "люблю", "любишь", "любит", "любим", "любите", "любят"],
                 ["жить — vivere", "живу", "живёшь", "живёт", "живём", "живёте", "живут"],
                 ["идти — andare (a piedi)", "иду", "идёшь", "идёт", "идём", "идёте", "идут"],
                 ["хотеть* — volere", "хочу", "хочешь", "хочет", "хотим", "хотите", "хотят"],
                 ["мочь* — potere", "могу", "можешь", "может", "можем", "можете", "могут"],
                 ["есть* — mangiare", "ем", "ешь", "ест", "едим", "едите", "едят"],
                 ["пить* — bere", "пью", "пьёшь", "пьёт", "пьём", "пьёте", "пьют"],
             ]},
            {"tipo": "nota", "testo": "<b>быть</b> (essere) <b>non si usa al presente</b>: «Io sono Andrea» = Я Андрей. Al futuro: я буду, ты будешь, он будет, мы будем, вы будете, они будут."},
        ],
    },
    {
        "id": "r005",
        "categoria": "Il passato",
        "icona": "⏪",
        "sottotitolo": "Si forma dal genere, non dalla persona",
        "blocchi": [
            {"tipo": "testo", "testo": "Il passato russo è facile: si toglie -ть dall'infinito e si aggiunge una desinenza che dipende dal <b>genere</b> di chi parla (non dalla persona)."},
            {"tipo": "tabella",
             "intestazioni": ["Chi", "Desinenza", "делать (fare)", "быть (essere)"],
             "righe": [
                 ["lui (m.)", "-л", "делал", "был"],
                 ["lei (f.)", "-ла", "делала", "была"],
                 ["esso (n.)", "-ло", "делало", "было"],
                 ["loro (pl.)", "-ли", "делали", "были"],
             ]},
            {"tipo": "nota", "testo": "Quindi una donna dice Я делал<b>а</b>, un uomo Я делал. Vale per я, ты e он/она a seconda di chi sono."},
        ],
    },
    {
        "id": "r006",
        "categoria": "Aspetto del verbo",
        "icona": "\U0001F501",
        "sottotitolo": "Imperfettivo (processo) vs perfettivo (risultato)",
        "blocchi": [
            {"tipo": "testo", "testo": "Quasi ogni verbo russo esiste in <b>coppia</b>. L'<b>imperfettivo</b> indica il processo o l'abitudine; il <b>perfettivo</b> indica un'azione conclusa, con un risultato."},
            {"tipo": "tabella",
             "intestazioni": ["Imperfettivo", "Perfettivo", "Significato"],
             "righe": [
                 ["делать", "сделать", "fare"],
                 ["читать", "прочитать", "leggere"],
                 ["писать", "написать", "scrivere"],
                 ["видеть", "увидеть", "vedere"],
             ]},
            {"tipo": "nota", "testo": "Regola d'oro A1: il <b>presente</b> si fa solo dall'imperfettivo. Il perfettivo coniugato «al presente» ha in realtà valore di <b>futuro</b> (я прочитаю = «leggerò / avrò letto»)."},
        ],
    },
    {
        "id": "r007",
        "categoria": "Plurale dei sostantivi",
        "icona": "\U0001F4DA",
        "sottotitolo": "Come passare da uno a tanti",
        "blocchi": [
            {"tipo": "tabella",
             "intestazioni": ["Genere", "Singolare", "Plurale", "Desinenza"],
             "righe": [
                 ["maschile", "стол", "столы", "-ы"],
                 ["femminile", "книга", "книги", "-и"],
                 ["femminile -я", "неделя", "недели", "-и"],
                 ["neutro -о", "окно", "окна", "-а"],
                 ["neutro -е", "море", "моря", "-я"],
             ]},
            {"tipo": "nota", "testo": "<b>Regola ortografica</b>: dopo г к х ж ш щ ч si scrive sempre <b>-и</b>, mai -ы. Es. книга → книги, мальчик → мальчики."},
            {"tipo": "nota", "testo": "Alcuni plurali irregolari da imparare a memoria: дом → дома́, друг → друзья́, человек → лю́ди, ребёнок → де́ти."},
        ],
    },
    {
        "id": "r008",
        "categoria": "Numeri 0–10",
        "icona": "\U0001F522",
        "sottotitolo": "I numeri di base",
        "blocchi": [
            {"tipo": "tabella",
             "intestazioni": ["Cifra", "Russo", "Pronuncia"],
             "righe": [
                 ["0", "ноль", "nol'"],
                 ["1", "один", "adín"],
                 ["2", "два", "dva"],
                 ["3", "три", "tri"],
                 ["4", "четыре", "chetýre"],
                 ["5", "пять", "pjat'"],
                 ["6", "шесть", "shest'"],
                 ["7", "семь", "sem'"],
                 ["8", "восемь", "vósem'"],
                 ["9", "девять", "dévjat'"],
                 ["10", "десять", "désjat'"],
             ]},
            {"tipo": "nota", "testo": "Dopo один il sostantivo è singolare (один дом); dopo 2–4 va al genitivo singolare (два дома́); da 5 in su al genitivo plurale (пять домо́в)."},
        ],
    },
]

with io.open(PATH, "r", encoding="utf-8") as f:
    d = json.load(f)

d["riferimento"] = riferimento
d["meta"]["versione"] = 4
note = d["meta"].get("note", "")
if "riferimento" not in note:
    d["meta"]["note"] = note + " Sezione 'riferimento' = schede di consultazione (Regole grammaticali)."

with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("OK: riferimento sezioni =", len(riferimento), "| versione =", d["meta"]["versione"])
