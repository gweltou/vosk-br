#!/usr/bin/env python3

import subprocess
import sys
import argparse
import srt
import json
import datetime
from vosk import Model, KaldiRecognizer, SetLogLevel
from ostilhou.asr.post_processing import post_process_vosk



def SrtResult(rec, stream, words_per_line = 7, normalize=False):
        results = []

        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(rec.Result())
        results.append(rec.FinalResult())

        subs = []
        for res in results:
            jres = json.loads(res)
            if not "result" in jres:
                continue
            words = jres["result"]
            # We need to apply text post-processing here
            words = post_process_vosk(words, normalize)
            
            for j in range(0, len(words), words_per_line):
                line = words[j : j + words_per_line]
                s = srt.Subtitle(index=len(subs),
                        content=" ".join([l["word"] for l in line]),
                        start=datetime.timedelta(seconds=line[0]["start"]),
                        end=datetime.timedelta(seconds=line[-1]["end"]))
                subs.append(s)

        return srt.compose(subs)



if __name__ == "__main__":
    desc = f"Generate subtitles in srt format"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('filename')
    parser.add_argument("-m", "--model", default="model/vosk-model-br-0.7", help="Vosk model to use for decoding", metavar='MODEL_PATH')
    parser.add_argument("-n", "--normalize", help="Normalize numbers", action="store_true")
    args = parser.parse_args()

    SAMPLE_RATE = 16000

    SetLogLevel(-1)

    model = Model(args.model)
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)

    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                args.filename,
                                "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                                stdout=subprocess.PIPE).stdout as stream:

        print(SrtResult(rec, stream, normalize=args.normalize))
