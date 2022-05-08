#!/usr/bin/env python3


subs = dict()
substitution_file = "postproc/subs.txt"
with open(substitution_file, 'r') as f:
    for l in f.readlines():
        l = l.strip()
        if l and not l.startswith('#'):
            k, v = l.split('\t')
            subs[k] = v


def post_proc(text):
    if not text:
        return ''
    
    # web adresses
    if "HTTP" in text or "WWW" in text:
        text = text.replace("pik", '.')
        text = text.replace(' ', '')
        return text.lower()
    
    for sub in subs:
        text = text.replace(sub, subs[sub])
    
    splitted = text.split(maxsplit=1)
    splitted[0] = splitted[0].capitalize()
    return ' '.join(splitted)
