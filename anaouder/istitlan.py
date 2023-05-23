#!/usr/bin/env python3

import subprocess
import sys
import argparse
import json
import datetime
import os.path

import static_ffmpeg
import srt
from vosk import Model, KaldiRecognizer, SetLogLevel

from anaouder.asr.post_processing import post_process_vosk
from anaouder.text import tokenize, detokenize, load_translation_dict, translate



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
			text = ' '.join([ w["word"] for w in line ])
			for td in translation_dicts:
				text = detokenize( translate(tokenize(text), td) )

			s = srt.Subtitle(index=len(subs),
					content=text,
					start=datetime.timedelta(seconds=line[0]["start"]),
					end=datetime.timedelta(seconds=line[-1]["end"]))
			subs.append(s)

	return srt.compose(subs)



def main_istitlan() -> None:
	""" istitlan cli entry point """

	global translation_dicts

	DEFAULT_MODEL = os.path.join(
		os.path.dirname(os.path.realpath(__file__)),
		"models",
		"vosk-model-br-0.7"
	)

	desc = f"Generate subtitles in srt format"
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('filename')
	parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
		help="Vosk model to use for decoding", metavar='MODEL_PATH')
	parser.add_argument("-n", "--normalize", action="store_true",
		help="Normalize numbers")
	parser.add_argument("-d", "--translate", nargs='+',
		help="Use additional translation dictionaries")
	parser.add_argument("-o", "--output", help="write to a file")
	args = parser.parse_args()
	
	# Use static_ffmpeg instead of ffmpeg
	static_ffmpeg.add_paths()

	SAMPLE_RATE = 16000
	SetLogLevel(-1)
	model = Model(args.model)
	rec = KaldiRecognizer(model, SAMPLE_RATE)
	rec.SetWords(True)

	translation_dicts = []
	if args.translate:
		translation_dicts = [ load_translation_dict(path) for path in args.translate ]

	fout = open(args.output, 'w') if args.output else sys.stdout

	with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
								args.filename,
								"-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
								stdout=subprocess.PIPE).stdout as stream:

		print(SrtResult(rec, stream, normalize=args.normalize), file=fout)
	
	if args.output:
		fout.close()


if __name__ == "__main__":
	main_istitlan()