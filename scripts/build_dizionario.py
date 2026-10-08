# -*- coding: utf-8 -*-
"""Genera dizionario.txt: il dizionario esteso russo -> italiano dell'app.

Fonte: WikDict (https://www.wikdict.com), dizionari bilingui ricavati da
Wiktionary; licenza CC BY-SA 3.0 (va citata: lo fa l'app sotto i risultati).
Si uniscono le due direzioni (ru-it e it-ru), così una parola russa ha anche le
traduzioni che compaiono solo dal lato italiano.

Formato del file (testo, una voce per riga, dalla più importante):
    russo<TAB>traduzioni italiane separate da virgola
Le righe che iniziano con # sono commenti.

Uso:
    python scripts/build_dizionario.py            # scarica i due database
    python scripts/build_dizionario.py CARTELLA   # usa ru-it.sqlite3 e it-ru.sqlite3 già scaricati
Idempotente: rilanciandolo riscrive il file.
"""
import collections, datetime, os, re, sqlite3, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "dizionario.txt")
URL = "https://download.wikdict.com/dictionaries/sqlite/2/{}.sqlite3"

ACCENTO = "\u0301"                  # accento tonico russo (ро́стбиф)
SPORCO = re.compile(r"[\[\]{}<>=|#_@*;]|https?:|\)\s*$|^\(|^\W")
MAX_TRAD = 6                             # traduzioni italiane per parola
# Il turpiloquio resta (se lo si cerca si trova), ma in fondo: non deve
# comparire tra i primi suggerimenti mentre si scrive.
VOLGARE = re.compile(r"^(пизд|хуй|хуё|хуе|хуя|бляд|бля\b|[её]б|залуп|муд[аио]|жоп|сук[аи]$|манд[аеуы]|дроч|гандон|пидо|говн|сра[тл]|ссать)", re.I)


def scarica(cartella):
    for nome in ("ru-it", "it-ru"):
        dest = os.path.join(cartella, nome + ".sqlite3")
        if not os.path.exists(dest):
            print("scarico", nome, "...")
            urllib.request.urlretrieve(URL.format(nome), dest)


def pulisci_ru(s):
    return re.sub(r"\s+", " ", s.replace(ACCENTO, "")).strip()


def pulisci_it(s):
    s = re.sub(r"</?u>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    # l'accento grafico sulle vocali interne è solo una guida alla pronuncia
    # (àlbero, fàccia): si toglie. Quello finale (città, perché) resta.
    s = re.sub(r"[àáèéìíòóù](?=[a-z])", lambda m: "aaeeiioou"["àáèéìíòóù".index(m.group())], s)
    return s


# articoli rimasti da soli al posto della traduzione (вода: «la»)
ARTICOLI = {"il", "lo", "la", "i", "gli", "le", "un", "uno", "una", "l'"}


def valida(ru, it):
    if not ru or not it or SPORCO.search(ru) or SPORCO.search(it):
        return False
    if it.lower() in ARTICOLI and ru not in ("ля", "ле"):
        return False
    if not re.search("[а-яё]", ru, re.I) or re.search("[a-z]", ru, re.I):
        return False
    return len(ru) <= 40 and len(it) <= 45


def main():
    cartella = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="wikdict-")
    scarica(cartella)

    trad = collections.OrderedDict()            # russo -> [italiano...]
    peso = collections.defaultdict(float)       # importanza, per l'ordine del file

    def aggiungi(ru, it, imp):
        ru, it = pulisci_ru(ru), pulisci_it(it)
        if not valida(ru, it):
            return
        lst = trad.setdefault(ru, [])
        if it.lower() not in (x.lower() for x in lst):
            lst.append(it)
        peso[ru] = max(peso[ru], imp or 0)

    q = ("select written_rep, trans_list, max_score, rel_importance from simple_translation "
         "order by rel_importance desc")
    db = sqlite3.connect(os.path.join(cartella, "ru-it.sqlite3"))
    for ru, lista, score, imp in db.execute(q):
        for it in lista.split(" | "):
            aggiungi(ru, it, imp)
    # Dal lato italiano le traduzioni col punteggio basso sono spesso del senso
    # sbagliato (inchinarsi → бабочка): a una parola russa che c'è già si
    # aggiungono solo quelle sicure, alle parole nuove quelle almeno discrete.
    # L'importanza è quella della parola italiana: pesa meno.
    russe = set(trad)
    db = sqlite3.connect(os.path.join(cartella, "it-ru.sqlite3"))
    for it, lista, score, imp in db.execute(q):
        for ru in lista.split(" | "):
            minimo = 10 if pulisci_ru(ru) in russe else 2
            if (score or 0) >= minimo:
                aggiungi(ru, it, (imp or 0) * 0.5)

    for ru in trad:
        if VOLGARE.search(ru):
            peso[ru] = -1
    voci = sorted(trad.items(), key=lambda kv: (-peso[kv[0]], kv[0]))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Dizionario esteso russo-italiano dell'app. Fonte: WikDict (www.wikdict.com), "
                "dai dati di Wiktionary, licenza CC BY-SA 3.0.\n")
        f.write("# Generato da scripts/build_dizionario.py il %s: %d parole.\n"
                % (datetime.date.today().isoformat(), len(voci)))
        for ru, its in voci:
            f.write(ru + "\t" + ", ".join(its[:MAX_TRAD]) + "\n")
    print("scritto", OUT, "-", len(voci), "parole,", os.path.getsize(OUT), "byte")


if __name__ == "__main__":
    main()
