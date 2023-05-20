#!/usr/bin/env python3

import subprocess
import argparse
import static_ffmpeg
import os.path
from vosk import Model, KaldiRecognizer, SetLogLevel
from .ostilhou.asr.post_processing import post_process_text
from .ostilhou.text import tokenize, detokenize, load_translation_dict, translate



def format_output(result, normalize=False):
	sentence = eval(result)["text"]
	sentence = post_process_text(sentence, normalize)
	for td in translation_dicts:
		sentence = detokenize( translate(tokenize(sentence), td) )
	return sentence


def main_adskrivan() -> None:
	global translation_dicts

	DEFAULT_MODEL = os.path.join(
		os.path.dirname(os.path.realpath(__file__)),
		"models",
		"vosk-model-br-0.7"
	)
	
	# Use static_ffmpeg instead of ffmpeg
	static_ffmpeg.add_paths()

	desc = f"Decode an audio file in any format, with the help of ffmpeg"
	parser = argparse.ArgumentParser(description=desc)
	parser.add_argument('filename')
	parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
		help="Vosk model to use for decoding", metavar='MODEL_PATH')
	parser.add_argument("-n", "--normalize", action="store_true",
		help="Normalize numbers")
	parser.add_argument("-t", "--translate", nargs='+',
		help="Use additional translation dictionaries")
	args = parser.parse_args()

	SAMPLE_RATE = 16000
	SetLogLevel(-1)
	model = Model(args.model)
	rec = KaldiRecognizer(model, SAMPLE_RATE)
	rec.SetWords(True)

	translation_dicts = []
	if args.translate:
		translation_dicts = [ load_translation_dict(path) for path in args.translate ]


	with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
								args.filename,
								"-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
								stdout=subprocess.PIPE) as process:

		while True:
			data = process.stdout.read(4000)
			if len(data) == 0:
				break
			if rec.AcceptWaveform(data):
				print(format_output(rec.Result(), normalize=args.normalize))
		print(format_output(rec.FinalResult(), normalize=args.normalize))
	

if __name__ == "__main__":
	main_adskrivan()
