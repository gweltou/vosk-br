#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave


substitution_file = "postproc/subs.txt"
subs = dict()
with open(substitution_file, 'r') as f:
    for l in f.readlines():
        l = l.strip()
        if l and not l.startswith('#'):
            k, v = l.split('\t')
            subs[k] = v


def post_proc(text):
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


SetLogLevel(1)

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

if len(sys.argv) >= 3:
    model = Model(sys.argv[2])
else:
    model = Model("model/bzg3")
    
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

while True:
    data = wf.readframes(4000)   # skip header
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        r = eval(rec.Result())
        print(post_proc(r["text"]))

#print(rec.FinalResult())
