#!/usr/bin/env python3

import subprocess
import argparse
from vosk import Model, KaldiRecognizer, SetLogLevel
from ostilhou.asr.post_processing import post_process_text


def format_output(result, normalize=False):
    sentence = eval(result)["text"]
    sentence = post_process_text(sentence, normalize)
    print(sentence)



if __name__ == "__main__":
    desc = f"Decode an audio file in any format, with the help of ffmpeg"
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
                                stdout=subprocess.PIPE) as process:

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                format_output(rec.Result(), normalize=args.normalize)
        format_output(rec.FinalResult(), normalize=args.normalize)
