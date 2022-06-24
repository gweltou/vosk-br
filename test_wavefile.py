#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
from postproc.postproc import *


SetLogLevel(0)


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
    model = Model("model/bzg5")
    
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

while True:
    data = wf.readframes(4000)   # skip header
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        r = eval(rec.Result())
        print(post_proc(r["text"]))

print(post_proc(eval(rec.FinalResult())["text"]))
