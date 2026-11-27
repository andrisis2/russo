#!/usr/bin/env python3
"""Costruisce corso.json (il corso in 365 giorni) dai sorgenti in corso/.

I sorgenti sono file di testo, una settimana per file (corso/s01.txt …
corso/s52.txt), più corso/moduli.txt. Il formato è descritto in
corso/FORMATO.md.

Uso:
  python scripts/build_corso.py             costruisce corso.json e stampa il resoconto
  python scripts/build_corso.py --accenta   prima aggiunge nei sorgenti gli accenti
                                            mancanti (e le ё) dove il dizionario non
                                            lascia dubbi, poi costruisce
  python scripts/build_corso.py --copertura stampa anche le parole delle frasi non
                                            ancora introdotte dal corso

Controlli facoltativi, se disponibili:
  - pymorphy3 (pip install pymorphy3 pymorphy3-dicts-ru): parole russe sconosciute
    (probabili refusi) e lemmi per il controllo di copertura;
  - il dizionario di OpenRussian (CSV con le forme accentate, CC BY-SA 4.0:
    github.com/Badestrand/russian-dictionary), cartella indicata dalla variabile
    OPENRUSSIAN_DIR: accenti sbagliati o mancanti.
Senza questi strumenti il corso si costruisce lo stesso (solo senza quei controlli).
"""
import csv
import datetime
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'corso')
OUT = os.path.join(ROOT, 'corso.json')
KNOWLEDGE = os.path.join(ROOT, 'knowledge.json')

ACC = '́'                      # accento tonico (combinante)
VOCALI = 'аеёиоуыэюя'
CYR_WORD = re.compile(r"[А-Яа-яЁё́]+(?:-[А-Яа-яЁё́]+)*")

avvisi = []                         # (file, riga, messaggio)
def avviso(f, n, msg):
    avvisi.append((os.path.basename(f) if f else '', n, msg))


# ---------------------------------------------------------------------------
# Utilità sul russo
# ---------------------------------------------------------------------------
def nudo(s):
    """Senza accenti tonici."""
    return s.replace(ACC, '')

def chiave(s):
    """Chiave di confronto: minuscole, senza accenti, ё = е."""
    return nudo(s).lower().replace('ё', 'е').strip()

def n_vocali(w):
    return sum(1 for c in nudo(w).lower() if c in VOCALI)

_PRIMA = re.compile(r"([А-Яа-яЁё́]+) $")
def dopo_proclitico(testo, start):
    """Vero se la parola che comincia in «start» segue un monosillabo accentato
    (не́ был, за́ городом, на́ дом): in quel caso è atona e non va accentata."""
    m = _PRIMA.search(testo[max(0, start - 8):start])
    return bool(m) and ACC in m.group(1) and n_vocali(m.group(1)) == 1

def hash36(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    out, digits = '', '0123456789abcdefghijklmnopqrstuvwxyz'
    while True:
        h, r = divmod(h, 36)
        out = digits[r] + out
        if not h:
            return out

def norm_frase(s):
    s = chiave(s)
    s = re.sub(r'[^а-яa-z0-9\s-]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


# ---------------------------------------------------------------------------
# Traslitterazione "a orecchio" con l'accento (privét, harašó, minjá):
# o atona → a, e/я atone → i, consonanti finali sorde, assimilazioni.
# Stesso schema delle voci dell'app: č š ž šč c(ц) h(х) y(ы) j(й) ʹ(ь).
# ---------------------------------------------------------------------------
SONORE = {'б': 'п', 'в': 'ф', 'г': 'к', 'д': 'т', 'ж': 'ш', 'з': 'с'}
SORDE = {v: k for k, v in SONORE.items()}
SORDE_TUTTE = set('пфктшсхцчщ')
LAT = {'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ж': 'ž', 'з': 'z', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
       'н': 'n', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'č', 'ш': 'š',
       'щ': 'šč'}
ACUTO = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'y': 'ý'}
CLITICI = {'в', 'во', 'на', 'по', 'о', 'об', 'обо', 'до', 'за', 'из', 'к', 'ко', 'с', 'со', 'у', 'от', 'без',
           'для', 'не', 'ни', 'же', 'ли', 'бы', 'и', 'а', 'но', 'под', 'над', 'при', 'про', 'через'}
NON_GENITIVO = {'много', 'немного', 'дорого', 'недорого', 'строго', 'убого', 'полого'}
# grafia "come si pronuncia" per i casi più comuni (l'accento resta dov'è)
PRONUNCIA = [
    (r'^что', 'што'), (r'^(коне́?)чн', r'\1шн'), (r'^(ску́?)чн', r'\1шн'),
    (r'^(здра́?)вств', r'\1ств'), (r'(чу́?)вств', r'\1ств'), (r'^(со́?)лнц', r'\1нц'),
    (r'(се́?)рдц', r'\1рц'), (r'(пра́?)здни', r'\1зни'), (r'(ле́?)стниц', r'\1сниц'),
    (r'сч', 'щ'), (r'зч', 'щ'), (r'мужчи', 'мущи'), (r'([её]́?)гк', r'\1хк'), (r'(я́?)гк', r'\1хк'),
    (r'(е́?)гч', r'\1хч'), (r'стн', 'сн'), (r'здн', 'зн'), (r'[тд]ц', 'ц'), (r'ть?ся$', 'ца'),
    (r'^сего(́?)дн', r'сиво\1дн'),
]

GENITIVI_BREVI = {'его', 'него', 'кого', 'чего', 'того', 'сего'}

def _translit_parola(w, clitico_atono, seguente=None):
    orig = w
    w = w.lower()
    # genitivo -ого/-его (его, моего, нового…): la г si pronuncia v
    base = nudo(w)
    if base in GENITIVI_BREVI or (len(base) > 4 and re.search(r'[ое]го$', base) and base not in NON_GENITIVO
                                  and base[-4] not in VOCALI):
        w = re.sub(r'г(о́?)$', r'в\1', w)
    for a, b in PRONUNCIA:
        w = re.sub(a, b, w)
    # lettere con l'indicazione dell'accento
    lett = []
    for ch in w:
        if ch == ACC:
            if lett:
                lett[-1][1] = True
            continue
        lett.append([ch, False])
    vocali_idx = [i for i, (c, _) in enumerate(lett) if c in VOCALI]
    ha_accento = any(s for _, s in lett) or any(c == 'ё' for c, _ in lett)
    if clitico_atono:
        ha_accento = True          # parola atona: l'accento è su un'altra parola
        if nudo(w) == 'не':
            return 'ni'
    elif not ha_accento:
        if len(vocali_idx) == 1:
            lett[vocali_idx[0]][1] = True
            ha_accento = True
    else:
        for c in lett:
            if c[0] == 'ё':
                c[1] = True
    # consonanti: sonore/sorde da destra a sinistra
    suoni = [c for c, _ in lett]
    proclitica = len(suoni) == 1 and suoni[0] not in VOCALI      # в, к, с: si legano alla parola dopo
    for i in range(len(suoni) - 1, -1, -1):
        c = suoni[i]
        j = i + 1
        while j < len(suoni) and suoni[j] == 'ь':
            j += 1
        dopo = suoni[j] if j < len(suoni) else None
        if proclitica:
            if seguente is None or seguente in VOCALI or seguente in 'лмнрйв':
                continue
            dopo = seguente
        if c in SONORE:
            if dopo is None or dopo in SORDE_TUTTE:
                suoni[i] = SONORE[c]
        elif c in SORDE and dopo in SONORE and dopo != 'в':
            suoni[i] = SORDE[c]
    out = []
    n = len(lett)
    for i, (c0, tonica) in enumerate(lett):
        c = suoni[i]
        prev = lett[i - 1][0] if i else None
        nxt = lett[i + 1][0] if i + 1 < n else None
        iniziale = prev is None or prev in VOCALI or prev in 'ьъ'
        dura = prev in ('ж', 'ш', 'ч', 'щ', 'ц')
        finale = i == n - 1
        if c in VOCALI:
            atona = ha_accento and not tonica
            if c == 'а':
                v = 'a'
            elif c == 'о':
                v = 'a' if atona else 'o'
            elif c == 'у':
                v = 'u'
            elif c == 'ы':
                v = 'y'
            elif c == 'и':
                v = ('j' if prev is not None and prev in 'ьъ' else '') + 'i'
            elif c == 'э':
                v = 'e'
            elif c == 'е':
                if atona and not finale:
                    v = ('j' if iniziale else '') + 'i'
                else:
                    v = ('j' if iniziale else '') + 'e'
            elif c == 'ё':
                v = ('' if dura else 'j') + 'o'
            elif c == 'ю':
                v = ('' if dura else 'j') + 'u'
            else:  # я
                if atona and not finale and not iniziale:
                    v = 'i'
                elif atona and not finale and iniziale and prev is None:
                    v = 'ji'
                else:
                    v = 'ja'
            if tonica and not (n_vocali(orig) == 1 and '-' not in orig):
                v = v[:-1] + ACUTO[v[-1]]
            out.append(v)
        elif c == 'ь':
            if nxt is None or nxt not in VOCALI:
                out.append('ʹ')
        elif c == 'ъ':
            pass
        else:
            out.append(LAT.get(c, c))
    s = ''.join(out)
    if orig[:1].isupper():
        s = s[:1].upper() + s[1:]
    return s

def translit(testo):
    parti = []
    toks = re.split(r'(\s+)', testo)
    for k, tok in enumerate(toks):
        if not tok.strip():
            parti.append(tok)
            continue
        m = re.match(r'^([^А-Яа-яЁё]*)(.*?)([^А-Яа-яЁё́]*)$', tok)
        pre, core, post = m.groups()
        if not core:
            parti.append(tok)
            continue
        # prima lettera della parola dopo (per в, к, с che si legano a lei)
        seg = None
        for t in toks[k + 1:]:
            mm = re.search(r'[А-Яа-яЁё]', t)
            if mm:
                seg = mm.group(0).lower()
                break
        pezzi = core.split('-')
        segnati = any(ACC in p or 'ё' in p.lower() for p in pezzi)
        tr = []
        for p in pezzi:
            atono = (segnati and ACC not in p and 'ё' not in p.lower()) or (len(pezzi) == 1 and chiave(p) in CLITICI and len(testo.split()) > 1)
            tr.append(_translit_parola(p, atono, seg))
        parti.append(pre + '-'.join(tr) + post)
    return ''.join(parti)


# ---------------------------------------------------------------------------
# Dizionari facoltativi
# ---------------------------------------------------------------------------
def carica_openrussian():
    d = os.environ.get('OPENRUSSIAN_DIR')
    if not d or not os.path.isdir(d):
        return None
    idx = defaultdict(set)
    def aggiungi(forma):
        for v in re.split(r'[,;/]', forma or ''):
            v = v.strip().strip('*').strip()
            if not v or ' ' in v or not re.search('[а-яё]', v.lower()):
                continue
            v = v.replace("'", ACC).lower()
            v = v.replace('ё' + ACC, 'ё')
            if n_vocali(v) <= 1:
                v = nudo(v)
            if not re.fullmatch(r"[а-яё́-]+", v):
                continue
            idx[chiave(v)].add(v)
    for nome in ('nouns.csv', 'verbs.csv', 'adjectives.csv', 'others.csv'):
        p = os.path.join(d, nome)
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as fh:
            r = csv.reader(fh, delimiter='\t')
            intest = next(r)
            salta = {intest.index(c) for c in ('bare', 'translations_en', 'translations_de', 'gender', 'partner',
                                                'animate', 'indeclinable', 'sg_only', 'pl_only', 'aspect') if c in intest}
            for riga in r:
                for i, cella in enumerate(riga):
                    if i in salta:
                        continue
                    aggiungi(cella)
    return idx

def carica_morph():
    try:
        import pymorphy3
        return pymorphy3.MorphAnalyzer()
    except Exception:
        return None


# parole giuste che i dizionari non conoscono (corso/parole_ok.txt, una per riga)
# e accenti giusti che il dizionario non riporta (сре́ду «mercoledì», аэропорту́ «in aeroporto»)
PAROLE_OK, ACCENTI_OK = set(), set()
_pok = os.path.join(SRC, 'parole_ok.txt')
if os.path.exists(_pok):
    with open(_pok, encoding='utf-8') as _fh:
        for _r in _fh.read().split('\n'):
            _r = _r.split('#')[0].strip()
            if not _r:
                continue
            for _w in _r.split():
                PAROLE_OK.add(chiave(_w))
                if ACC in _w:
                    ACCENTI_OK.add(_w.lower())


def varianti_accento(idx, tok):
    """Forme accentate note per una parola (senza distinguere ё/е)."""
    if idx is None:
        return None
    return idx.get(chiave(tok))

def con_maiuscola(modello, forma):
    out, i = [], 0
    for ch in forma:
        if ch == ACC:
            out.append(ch)
            continue
        m = modello[i] if i < len(modello) else ch
        out.append(ch.upper() if m.isupper() else ch)
        i += 1
    return ''.join(out)

def accenta_token(idx, tok):
    """Restituisce (forma corretta o None, stato): 'ok', 'aggiunto', 'ambiguo', 'sbagliato', 'ignota'."""
    if n_vocali(tok) <= 1 and 'ё' not in tok.lower():
        return None, 'ok'
    var = varianti_accento(idx, tok)
    if not var:
        return None, 'ignota'
    low = tok.lower()
    if low in ACCENTI_OK:
        return None, 'ok'
    ha = ACC in low or 'ё' in low
    # le forme del dizionario senza accento non dicono nulla
    var = {v for v in var if ACC in v or 'ё' in v}
    if not var:
        return None, 'ok'
    if ha:
        if low in var:
            return None, 'ok'
        # stessa posizione dell'accento ma ё scritta come е
        if any(v.replace('ё', 'е') == low.replace('ё', 'е') and 'ё' in v for v in var):
            v = next(v for v in var if v.replace('ё', 'е') == low.replace('ё', 'е'))
            return con_maiuscola(tok, v), 'aggiunto'
        # ё nella parola: l'accento è già lì
        if 'ё' in low and ACC not in low:
            return None, 'ok'
        return None, 'sbagliato'
    # senza accento: si aggiunge solo se il dizionario ha una forma sola
    if len(var) == 1:
        v = next(iter(var))
        if nudo(v) != low and nudo(v).replace('ё', 'е') != low:
            return None, 'ok'
        if nudo(v) == low and ACC not in v:
            return None, 'ok'
        return con_maiuscola(tok, v), 'aggiunto'
    return None, 'ambiguo'


# ---------------------------------------------------------------------------
# Lettura dei sorgenti
# ---------------------------------------------------------------------------
TIPI = {
    'm': 'sostantivo (m.)', 'f': 'sostantivo (f.)', 'n': 'sostantivo (n.)', 'pl': 'sostantivo (pl.)',
    'mf': 'sostantivo (m./f.)', 'v': 'verbo', 'agg': 'aggettivo', 'avv': 'avverbio', 'pron': 'pronome',
    'num': 'numero', 'prep': 'preposizione', 'cong': 'congiunzione', 'part': 'particella',
    'inter': 'interiezione', 'espr': 'espressione', 'nome': 'nome proprio',
}
SEZIONI = ('Lezione', 'Parole', 'Frasi', 'Esercizi', 'Lettura', 'Domande')

RE_SETT = re.compile(r'^# Settimana (\d+) \| (.+)$')
RE_GIORNO = re.compile(r'^## Giorno (\d+) \| (.+)$')
RE_SEZ = re.compile(r'^### (\w+)(?: \| (.+?) \| (.+))?\s*$')
RE_PAROLA = re.compile(r'^(?P<ru>.+?)\s+=\s+(?P<it>.+?)(?:\s+\[(?P<g>[^\]]*)\])?\s*$')
RE_FRASE = re.compile(r'^(?P<ru>.+?)\s+=\s+(?P<it>.+?)(?:\s+//\s*(?P<n>.*))?\s*$')
RE_SCELTA = re.compile(r'^\?\s*(?P<q>.*?)\s*\{(?P<o>[^}]+)\}\s*(?:=\s*(?P<it>.*?))?\s*(?:\s//\s*(?P<n>.*))?\s*$')
RE_SCRIVI = re.compile(r'^>\s*(?P<q>.*?)\s*→\s*(?P<a>[^=]+?)\s*(?:=\s*(?P<it>.*?))?\s*(?:\s//\s*(?P<n>.*))?\s*$')
RE_COMPONI = re.compile(r'^~\s*(?P<ru>.+?)\s+=\s+(?P<it>.+?)(?:\s+//\s*(?P<n>.*))?\s*$')


def leggi_moduli():
    moduli = []
    with open(os.path.join(SRC, 'moduli.txt'), encoding='utf-8') as fh:
        for riga in fh:
            riga = riga.strip()
            if not riga or riga.startswith('#'):
                continue
            n, tit, liv, ico, desc = [x.strip() for x in riga.split('|', 4)]
            moduli.append({'n': int(n), 'titolo': tit, 'livello': liv, 'icona': ico, 'desc': desc})
    return moduli


def parse_esercizio(riga, f, n):
    m = RE_SCELTA.match(riga)
    if riga.startswith('?') and m:
        opts = [o.strip() for o in m.group('o').split('|')]
        opts = [o for o in opts if o]
        if len(opts) < 2:
            avviso(f, n, 'scelta multipla con meno di 2 opzioni')
            return None
        if len(set(o.lower() for o in opts)) != len(opts):
            avviso(f, n, 'opzioni ripetute')
        e = {'t': 's', 'q': m.group('q').strip(), 'ok': opts[0], 'opts': opts[1:]}
        if m.group('it'):
            e['it'] = m.group('it').strip()
        if m.group('n'):
            e['nota'] = m.group('n').strip()
        return e
    m = RE_SCRIVI.match(riga)
    if riga.startswith('>') and m:
        risp = [a.strip() for a in m.group('a').split(' / ') if a.strip()]
        e = {'t': 'w', 'q': m.group('q').strip(), 'ok': risp}
        if m.group('it'):
            e['it'] = m.group('it').strip()
        if m.group('n'):
            e['nota'] = m.group('n').strip()
        return e
    m = RE_COMPONI.match(riga)
    if riga.startswith('~') and m:
        e = {'t': 'c', 'ru': m.group('ru').strip(), 'it': m.group('it').strip()}
        if m.group('n'):
            e['nota'] = m.group('n').strip()
        return e
    avviso(f, n, f'esercizio non riconosciuto: {riga[:60]}')
    return None


def leggi_settimana(path):
    sett, giorno, sez = None, None, None
    giorni = []
    with open(path, encoding='utf-8') as fh:
        righe = fh.read().split('\n')
    for n, raw in enumerate(righe, 1):
        riga = raw.rstrip()
        m = RE_SETT.match(riga)
        if m:
            parti = [x.strip() for x in m.group(2).split('|')]
            sett = {'n': int(m.group(1)), 'titolo': parti[-1], 'file': path}
            continue
        m = RE_GIORNO.match(riga)
        if m:
            giorno = {'g': int(m.group(1)), 'titolo': m.group(2).strip(), 'breve': [], 'vedi': [],
                      'lezione': [], 'parole': [], 'frasi': [], 'esercizi': [], 'lettura': None,
                      'domande': [], '_file': path, '_riga': n}
            giorni.append(giorno)
            sez = None
            continue
        if giorno is None:
            continue
        if re.match(r'^vedi:', riga.strip()):
            giorno['vedi'] += [x.strip() for x in riga.split(':', 1)[1].split(',') if x.strip()]
            continue
        m = RE_SEZ.match(riga)
        if m and m.group(1) in SEZIONI:
            sez = m.group(1)
            if sez == 'Lettura':
                giorno['lettura'] = {'titoloRu': (m.group(2) or '').strip(), 'titolo': (m.group(3) or '').strip(),
                                     'frasi': []}
            continue
        if sez is None:
            if not riga.strip():
                continue
            k, _, v = riga.partition(':')
            k = k.strip().lower()
            if k in ('obiettivo', 'breve', 'vedi', 'icona'):
                v = v.strip()
                if k == 'breve':
                    giorno['breve'].append(v)
                elif k == 'vedi':
                    giorno['vedi'] += [x.strip() for x in v.split(',') if x.strip()]
                else:
                    giorno[k] = v
            else:
                avviso(path, n, f'riga fuori sezione: {riga[:60]}')
            continue
        if sez == 'Lezione':
            giorno['lezione'].append(riga)
            continue
        s = riga.strip()
        if not s or s.startswith('//'):
            continue
        if sez == 'Parole':
            m = RE_PAROLA.match(s)
            if not m:
                avviso(path, n, f'parola non riconosciuta: {s[:60]}')
                continue
            g = (m.group('g') or '').strip()
            tipo, _, nota = g.partition(';')
            tipo = tipo.strip()
            asp = ''
            if tipo.startswith('v'):
                bits = tipo.split()
                tipo = 'v'
                asp = bits[1] if len(bits) > 1 else ''
            if tipo and tipo not in TIPI:
                avviso(path, n, f'tipo sconosciuto [{tipo}]')
            p = {'ru': m.group('ru').strip(), 'it': m.group('it').strip(), 't': tipo}
            if asp:
                p['asp'] = asp
            if nota.strip():
                p['nota'] = nota.strip()
            p['_riga'] = n
            giorno['parole'].append(p)
        elif sez in ('Frasi', 'Lettura'):
            m = RE_FRASE.match(s)
            if not m:
                avviso(path, n, f'frase senza traduzione: {s[:60]}')
                continue
            fr = {'ru': m.group('ru').strip(), 'it': m.group('it').strip()}
            if m.group('n'):
                fr['nota'] = m.group('n').strip()
            if sez == 'Frasi':
                giorno['frasi'].append(fr)
            else:
                giorno['lettura']['frasi'].append(fr)
        elif sez in ('Esercizi', 'Domande'):
            e = parse_esercizio(s, path, n)
            if e:
                (giorno['esercizi'] if sez == 'Esercizi' else giorno['domande']).append(e)
    return sett, giorni


# ---------------------------------------------------------------------------
# Accenti nei sorgenti (--accenta)
# ---------------------------------------------------------------------------
def accenta_sorgenti(idx, files):
    if idx is None:
        print('!! --accenta: dizionario OpenRussian non trovato (OPENRUSSIAN_DIR)')
        return
    tot_agg, ambigui = 0, defaultdict(list)
    for path in files:
        with open(path, encoding='utf-8') as fh:
            righe = fh.read().split('\n')
        cambiato = False
        sez = None
        for i, riga in enumerate(righe):
            if riga.startswith('### '):
                sez = riga[4:].split('|')[0].strip()
                continue
            if riga.startswith('## ') or riga.startswith('# '):
                sez = None
                continue
            if sez is None:
                # intestazione del giorno: si accentano «obiettivo:» e «breve:»
                if not re.match(r'^(obiettivo|breve):', riga):
                    continue
                ru, sep, resto = riga, '', ''
            # nelle parole e nelle frasi si accenta solo la parte russa (prima di " = ")
            elif sez in ('Parole', 'Frasi', 'Lettura'):
                if ' = ' not in riga:
                    continue
                ru, sep, resto = riga.partition(' = ')
            elif sez is not None:
                ru, sep, resto = riga, '', ''
            def sost(m):
                nonlocal tot_agg
                tok = m.group(0)
                start = m.start()
                # frammenti di desinenza (-ешь, -ый) e pezzi di parola in grassetto (аэропорт**у́**)
                if start > 0 and ru[start - 1] in '-–*':
                    return tok
                if m.end() < len(ru) and ru[m.end()] in '*-':
                    return tok
                # dopo un monosillabo accentato la parola è atona (не́ был, за́ городом)
                if dopo_proclitico(ru, start):
                    return tok
                forma, stato = accenta_token(idx, tok)
                if stato == 'aggiunto' and forma:
                    tot_agg += 1
                    return forma
                if stato == 'ambiguo':
                    ambigui[chiave(tok)].append(f'{os.path.basename(path)}:{i + 1}')
                return tok
            nuovo = CYR_WORD.sub(sost, ru)
            if nuovo != ru:
                righe[i] = nuovo + sep + resto
                cambiato = True
        if cambiato:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(righe))
    print(f'Accenti aggiunti: {tot_agg}')
    if ambigui:
        print(f'Parole con più accenti possibili (da segnare a mano se servono): {len(ambigui)}')
        for k, dove in sorted(ambigui.items(), key=lambda x: -len(x[1]))[:80]:
            var = ' / '.join(sorted(varianti_accento(idx, k) or []))
            print(f'   {k:<16} {var:<40} {", ".join(dove[:4])}{" …" if len(dove) > 4 else ""}')


# ---------------------------------------------------------------------------
# Controlli
# ---------------------------------------------------------------------------
def controlla_testo(idx, morph, testo, f, n, dove, mancanti):
    testo = testo.replace('**', '').replace('*', '')
    # refusi: lettere latine dentro parole russe (пожаluйста) o viceversa
    for w in re.findall(r"[A-Za-zÀ-ÿА-Яа-яЁё\u0301]+", testo):
        if re.search('[А-Яа-яЁё]', w) and re.search('[A-Za-zÀ-ÿ]', w):
            avviso(f, n, f'{dove}: lettere latine e cirilliche mescolate in «{w}»')
    for m in CYR_WORD.finditer(testo):
        tok = m.group(0)
        if m.start() > 0 and testo[m.start() - 1] in '-–':
            continue
        # prefissi e pezzi di parola (пере-, вы-)
        if m.end() < len(testo) and testo[m.end()] == '-':
            continue
        # lettere e sillabe isolate nelle spiegazioni (з, ги, -ешь…)
        if dove == 'lezione' and len(nudo(tok)) <= 2:
            continue
        # dopo un monosillabo accentato la parola è atona (не́ был, за́ городом)
        if dopo_proclitico(testo, m.start()):
            continue
        intero_noto = '-' in tok and ((morph is not None and morph.word_is_known(nudo(tok).lower()))
                                      or (idx is not None and chiave(tok) in idx) or chiave(tok) in PAROLE_OK)
        # nelle spiegazioni, radice-desinenza (говор-я́т, пиш-у́т) sono pezzi, non parole
        if dove == 'lezione' and '-' in tok and not intero_noto:
            continue
        # parola composta riconosciuta per intero (по-мо́ему): i pezzi non si controllano
        if intero_noto and chiave(tok) in PAROLE_OK:
            continue
        for parte in tok.split('-'):
            if not parte:
                continue
            if morph is not None and not intero_noto:
                b = nudo(parte).lower()
                if not morph.word_is_known(b) and not (idx and chiave(b) in idx) and not parte[:1].isupper() \
                        and chiave(b) not in PAROLE_OK:
                    avviso(f, n, f'{dove}: parola sconosciuta «{parte}»')
            if idx is not None:
                forma, stato = accenta_token(idx, parte)
                if stato == 'sbagliato':
                    var = ' / '.join(sorted(varianti_accento(idx, parte)))
                    avviso(f, n, f'{dove}: accento di «{parte}»? il dizionario dice {var}')
                elif stato == 'aggiunto':
                    mancanti.append((f, n, parte, forma))


def main():
    args = sys.argv[1:]
    files = sorted(os.path.join(SRC, x) for x in os.listdir(SRC) if re.fullmatch(r's\d\d\.txt', x))
    idx = carica_openrussian()
    morph = carica_morph()
    if '--accenta' in args:
        accenta_sorgenti(idx, files)

    moduli = leggi_moduli()
    with open(KNOWLEDGE, encoding='utf-8') as fh:
        kn = json.load(fh)
    voci_esistenti = {}
    for v in kn.get('voci', []):
        voci_esistenti.setdefault(chiave(v['ru']), v['id'])

    settimane, giorni = [], []
    for path in files:
        s, gg = leggi_settimana(path)
        if not s:
            avviso(path, 0, 'manca la riga «# Settimana N | …»')
            continue
        s['modulo'] = (s['n'] - 1) // 4 + 1
        settimane.append(s)
        for g in gg:
            g['s'] = s['n']
            atteso = range((s['n'] - 1) * 7 + 1, s['n'] * 7 + 1 + (1 if s['n'] == 52 else 0))
            if g['g'] not in atteso:
                avviso(path, g['_riga'], f'il giorno {g["g"]} non appartiene alla settimana {s["n"]}')
        giorni += gg

    giorni.sort(key=lambda g: g['g'])
    visti = {}
    for g in giorni:
        if g['g'] in visti:
            avviso(g['_file'], g['_riga'], f'giorno {g["g"]} ripetuto')
        visti[g['g']] = g

    # ---- parole: id, doppioni, traslitterazione ----
    prima_volta = {}
    oggi = datetime.date.today().isoformat()
    mancanti = []
    n_parole = n_frasi = n_es = 0
    for g in giorni:
        f = g['_file']
        modulo = (g['s'] - 1) // 4 + 1
        g['tipo'] = 'esame' if g['g'] == 365 else ('ripasso' if g['g'] % 7 == 0 else 'lezione')
        if g['tipo'] == 'ripasso' and g['g'] % 28 == 0:
            g['tipo'] = 'test'
        parole = []
        for p in g['parole']:
            k = chiave(p['ru'])
            if k in prima_volta:
                avviso(f, p['_riga'], f'«{p["ru"]}» è già stata introdotta il giorno {prima_volta[k]}')
            else:
                prima_volta[k] = g['g']
            pid = voci_esistenti.get(k) or ('c:' + k)
            controlla_testo(idx, morph, p['ru'], f, p['_riga'], 'parola', mancanti)
            if idx is not None and n_vocali(p['ru']) > 1 and ACC not in p['ru'] and 'ё' not in p['ru'].lower() \
                    and ' ' not in p['ru'] and '-' not in p['ru']:
                avviso(f, p['_riga'], f'parola senza accento: «{p["ru"]}»')
            q = OrderedDict([('id', pid), ('ru', p['ru']), ('it', p['it'])])
            if p.get('t'):
                q['t'] = p['t']
            if p.get('asp'):
                q['asp'] = p['asp']
            if p.get('nota'):
                q['nota'] = p['nota']
            q['tr'] = translit(p['ru'])
            parole.append(q)
        g['parole'] = parole
        n_parole += len(parole)

        frasi = []
        for fr in g['frasi']:
            controlla_testo(idx, morph, fr['ru'], f, g['_riga'], 'frase', mancanti)
            q = OrderedDict([('id', 'cf' + hash36(norm_frase(fr['ru']))), ('ru', fr['ru']), ('it', fr['it'])])
            if fr.get('nota'):
                q['nota'] = fr['nota']
            frasi.append(q)
        g['frasi'] = frasi
        n_frasi += len(frasi)

        for e in g['esercizi'] + g['domande']:
            # le opzioni sbagliate spesso sono sbagliate apposta (ребёнки): non si controllano
            testo = e.get('q', '') + ' ' + (e.get('ok') if isinstance(e.get('ok'), str) else ' '.join(e.get('ok', []))) + ' ' + e.get('ru', '')
            controlla_testo(idx, morph, testo, f, g['_riga'], 'esercizio', mancanti)
            base = e.get('q', '') + '|' + (e['ok'] if isinstance(e.get('ok'), str) else '/'.join(e.get('ok', []))) + '|' + e.get('ru', '')
            e['id'] = 'ce' + hash36(base)
        n_es += len(g['esercizi'])
        if g['lettura']:
            for fr in g['lettura']['frasi']:
                controlla_testo(idx, morph, fr['ru'], f, g['_riga'], 'lettura', mancanti)
            g['lettura']['domande'] = g['domande']
        if g['tipo'] == 'lezione' and g['g'] != 365:
            if not g['lezione'] or not ''.join(g['lezione']).strip():
                avviso(f, g['_riga'], f'giorno {g["g"]}: manca la lezione')
            if not g['parole'] and not g['esercizi']:
                avviso(f, g['_riga'], f'giorno {g["g"]}: né parole né esercizi')
        if g['tipo'] in ('ripasso', 'test') and not g['lettura']:
            avviso(f, g['_riga'], f'giorno {g["g"]}: giorno di ripasso senza lettura')
        controlla_testo(idx, morph, '\n'.join(g['lezione'] + g['breve'] + [g.get('obiettivo', '')]), f, g['_riga'], 'lezione', mancanti)

    # ---- uscita ----
    out_giorni = []
    for g in giorni:
        o = OrderedDict()
        o['g'] = g['g']
        o['s'] = g['s']
        o['tipo'] = g['tipo']
        o['titolo'] = g['titolo']
        for k in ('obiettivo', 'icona'):
            if g.get(k):
                o[k] = g[k]
        if g['breve']:
            o['breve'] = g['breve']
        lez = '\n'.join(g['lezione']).strip('\n')
        if lez:
            o['lezione'] = lez
        if g['parole']:
            o['parole'] = g['parole']
        if g['frasi']:
            o['frasi'] = g['frasi']
        if g['esercizi']:
            o['esercizi'] = g['esercizi']
        if g['lettura']:
            o['lettura'] = g['lettura']
        if g['vedi']:
            o['vedi'] = g['vedi']
        out_giorni.append(o)

    corso = OrderedDict()
    corso['versione'] = 1
    corso['aggiornato'] = oggi
    corso['moduli'] = moduli
    corso['settimane'] = [{'n': s['n'], 'modulo': s['modulo'], 'titolo': s['titolo']} for s in settimane]
    corso['giorni'] = out_giorni
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(corso, fh, ensure_ascii=False, separators=(',', ':'))

    # ---- resoconto ----
    print(f'corso.json: {len(out_giorni)} giorni in {len(settimane)} settimane · {n_parole} parole · '
          f'{n_frasi} frasi · {n_es} esercizi · {os.path.getsize(OUT) // 1024} KB')
    mancano = [g for g in range(1, 366) if g not in visti]
    if mancano:
        print(f'Giorni ancora da scrivere: {len(mancano)} (dal {mancano[0]})')
    if idx is None:
        print('(controllo degli accenti saltato: OPENRUSSIAN_DIR non impostata)')
    if morph is None:
        print('(controllo delle parole saltato: pymorphy3 non installato)')
    if mancanti:
        print(f'Accenti mancanti che il dizionario conosce: {len(mancanti)} (python scripts/build_corso.py --accenta)')
        for f, n, parte, forma in mancanti[:12]:
            print(f'   {os.path.basename(f)}:{n}  {parte} → {forma}')
    if avvisi:
        print(f'\nAvvisi ({len(avvisi)}):')
        for f, n, msg in avvisi:
            print(f'  {f}:{n}  {msg}')

    if '--copertura' in args and morph is not None:
        copertura(giorni, morph)


# Parole delle frasi non ancora introdotte (per tenere le frasi comprensibili)
FUNZIONALI = set('я ты он она оно мы вы они это и а но не да нет в на с к у о по за из от до как что кто где '
                 'когда так тоже очень вот там здесь тут уже ещё же ли бы или'.split())

def copertura(giorni, morph):
    noti = set(FUNZIONALI)
    print('\nCopertura (lemmi nuovi nelle frasi, per giorno):')
    for g in giorni:
        for p in g['parole']:
            for w in re.findall(r'[а-яё]+', chiave(p['ru'])):
                noti.add(morph.parse(w)[0].normal_form.replace('ё', 'е'))
                noti.add(w)
        ignoti = set()
        testi = [fr['ru'] for fr in g['frasi']] + ([fr['ru'] for fr in g['lettura']['frasi']] if g['lettura'] else [])
        for t in testi:
            for w in re.findall(r'[а-яё]+', chiave(t)):
                if w in noti:
                    continue
                lem = morph.parse(w)[0].normal_form.replace('ё', 'е')
                if lem not in noti:
                    ignoti.add(lem)
        if ignoti:
            print(f'  giorno {g["g"]:>3}: {", ".join(sorted(ignoti))}')


if __name__ == '__main__':
    main()
