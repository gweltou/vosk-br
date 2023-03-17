#!/usr/bin/env python3

import subprocess
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel
from postproc.postproc import *


SAMPLE_RATE = 16000

SetLogLevel(-1)

model = Model("model/bzg7-short")
rec = KaldiRecognizer(model, SAMPLE_RATE)


def pretty_print(result):
    print(post_proc(eval(result)["text"]))


with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                            sys.argv[1],
                            "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                            stdout=subprocess.PIPE) as process:

    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            pretty_print(rec.Result())
        else:
            pass
            #print(rec.PartialResult())

    pretty_print(rec.FinalResult())
