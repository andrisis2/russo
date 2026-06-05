#!/usr/bin/env python3
"""Estrae e ripulisce una porzione (per intervallo di tempo) da una trascrizione VTT
auto-generata di YouTube. Rimuove i tag inline e i duplicati 'rolling'.

Uso:
  python extract_lesson.py <file.vtt> <start hh:mm:ss> <end hh:mm:ss> <out.txt>
"""
import re, sys

def to_sec(t):
    t = t.strip()
    parts = [float(p) for p in t.replace(',', '.').split(':')]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return h * 3600 + m * 60 + s

def main():
    vtt, start, end, out = sys.argv[1], to_sec(sys.argv[2]), to_sec(sys.argv[3]), sys.argv[4]
    with open(vtt, encoding='utf-8') as f:
        raw = f.read()

    # blocchi separati da riga vuota; ogni cue inizia con "hh:mm:ss.mmm --> hh:mm:ss.mmm"
    time_re = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})')
    tag_re = re.compile(r'<[^>]+>')

    lines = []
    cur_start = None
    for block in raw.split('\n'):
        m = time_re.search(block)
        if m:
            cur_start = to_sec(m.group(1))
            continue
        if cur_start is None:
            continue
        if not (start <= cur_start < end):
            continue
        text = tag_re.sub('', block).strip()
        if not text or text.upper().startswith(('WEBVTT', 'KIND:', 'LANGUAGE:')):
            continue
        # dedup: salta se uguale all'ultima riga aggiunta o se è prefisso/uguale (rolling)
        if lines and (text == lines[-1] or text == lines[-1][:len(text)]):
            continue
        if lines and lines[-1].endswith(text):
            continue
        lines.append(text)

    # ricompone in testo continuo, evitando ripetizioni di coda
    clean = []
    for ln in lines:
        if clean and ln.startswith(clean[-1]):
            clean[-1] = ln  # estensione della stessa riga rolling
        else:
            clean.append(ln)

    with open(out, 'w', encoding='utf-8') as f:
        f.write(' '.join(clean))
    print(f"OK: {len(clean)} segmenti -> {out} ({sum(len(c) for c in clean)} caratteri)")

if __name__ == '__main__':
    main()
