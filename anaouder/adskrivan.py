#!/usr/bin/env python3

import subprocess
import argparse
import sys
import os.path
import datetime

import static_ffmpeg
import json
import srt
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

from anaouder.asr.recognizer import (
	transcribe_file, transcribe_segment, transcribe_segment_timecoded, load_vosk
	)
from anaouder.asr.post_processing import post_process_text, post_process_timecoded
from anaouder.text import tokenize, detokenize, load_translation_dict, translate
from anaouder.audio import split_to_segments



def format_output(sentence, normalize=False, keep_fillers=False):
	sentence = post_process_text(sentence, normalize, keep_fillers)
	for td in translation_dicts:
		sentence = detokenize( translate(tokenize(sentence), td) )
	return sentence



def export_to_eaf(segments, sentences, audiofile, type="wav"):
    """ Export to eaf (Elan) file """

    record_id = os.path.splitext(os.path.abspath(audiofile))[0]
    print(f"{record_id=}")
    audio_filename = os.path.extsep.join((record_id, 'wav'))
    if type == "mp3":
        mp3_file = os.path.extsep.join((record_id, 'mp3'))
        if not os.path.exists(mp3_file):
            convert_to_mp3(audio_filename, mp3_file)
        audio_filename = mp3_file

    text_filename = os.path.extsep.join((record_id, 'txt'))
    eaf_filename = os.path.extsep.join((record_id, 'eaf'))

    doc = minidom.Document()

    root = doc.createElement('ANNOTATION_DOCUMENT')
    root.setAttribute('AUTHOR', 'anaouder (Gweltaz DG)')
    root.setAttribute('DATE', datetime.datetime.now(pytz.timezone('Europe/Paris')).isoformat(timespec='seconds'))
    root.setAttribute('FORMAT', '3.0')
    root.setAttribute('VERSION', '3.0')
    root.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.setAttribute('xsi:noNamespaceSchemaLocation', 'http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
    doc.appendChild(root)

    header = doc.createElement('HEADER')
    header.setAttribute('MEDIA_FILE', '')
    header.setAttribute('TIME_UNITS', 'milliseconds')
    root.appendChild(header)

    media_descriptor = doc.createElement('MEDIA_DESCRIPTOR')
    media_descriptor.setAttribute('MEDIA_URL', 'file://' + os.path.abspath(audio_filename))
    if type == "mp3":
        media_descriptor.setAttribute('MIME_TYPE', 'audio/mpeg')
    else:
        media_descriptor.setAttribute('MIME_TYPE', 'audio/x-wav')
    media_descriptor.setAttribute('RELATIVE_MEDIA_URL', './' + os.path.basename(audio_filename))
    header.appendChild(media_descriptor)

    time_order = doc.createElement('TIME_ORDER')
    last_t = 0
    for i, (s, e) in enumerate(segments):
        if s < last_t:
            s = last_t
        last_t = s
        time_slot = doc.createElement('TIME_SLOT')
        time_slot.setAttribute('TIME_SLOT_ID', f'ts{2*i+1}')
        time_slot.setAttribute('TIME_VALUE', str(s))
        time_order.appendChild(time_slot)
        time_slot = doc.createElement('TIME_SLOT')
        time_slot.setAttribute('TIME_SLOT_ID', f'ts{2*i+2}')
        time_slot.setAttribute('TIME_VALUE', str(e))
        time_order.appendChild(time_slot)
    root.appendChild(time_order)

    tier_trans = doc.createElement('TIER')
    tier_trans.setAttribute('LINGUISTIC_TYPE_REF', 'transcript')
    tier_trans.setAttribute('TIER_ID', 'Transcription')

    for i, (sentence, _) in enumerate(sentences):
        annotation = doc.createElement('ANNOTATION')
        alignable_annotation = doc.createElement('ALIGNABLE_ANNOTATION')
        alignable_annotation.setAttribute('ANNOTATION_ID', f'a{i+1}')
        alignable_annotation.setAttribute('TIME_SLOT_REF1', f'ts{2*i+1}')
        alignable_annotation.setAttribute('TIME_SLOT_REF2', f'ts{2*i+2}')
        annotation_value = doc.createElement('ANNOTATION_VALUE')
        #text = doc.createTextNode(get_cleaned_sentence(sentence, rm_bl=True, keep_dash=True, keep_punct=True)[0])
        text = doc.createTextNode(sentence.replace('*', ''))
        annotation_value.appendChild(text)
        alignable_annotation.appendChild(annotation_value)
        annotation.appendChild(alignable_annotation)
        tier_trans.appendChild(annotation)
    root.appendChild(tier_trans)

    linguistic_type = doc.createElement('LINGUISTIC_TYPE')
    linguistic_type.setAttribute('GRAPHIC_REFERENCES', 'false')
    linguistic_type.setAttribute('LINGUISTIC_TYPE_ID', 'transcript')
    linguistic_type.setAttribute('TIME_ALIGNABLE', 'true')
    root.appendChild(linguistic_type)

    language = doc.createElement('LANGUAGE')
    language.setAttribute("LANG_ID", "bre")
    language.setAttribute("LANG_LABEL", "Breton (bre)")
    root.appendChild(language)

    constraint_list = [
        ("Time_Subdivision", "Time subdivision of parent annotation's time interval, no time gaps allowed within this interval"),
        ("Symbolic_Subdivision", "Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered"),
        ("Symbolic_Association", "1-1 association with a parent annotation"),
        ("Included_In", "Time alignable annotations within the parent annotation's time interval, gaps are allowed")
    ]
    for stereotype, description in constraint_list:
        constraint = doc.createElement('CONSTRAINT')
        constraint.setAttribute('DESCRIPTION', description)
        constraint.setAttribute('STEREOTYPE', stereotype)
        root.appendChild(constraint)

    xml_str = doc.toprettyxml(indent ="\t", encoding="UTF-8")

    with open(eaf_filename, "w") as f:
        f.write(xml_str.decode("utf-8"))



def main_adskrivan() -> None:
	""" adskrivan cli entry point """

	global translation_dicts

	DEFAULT_MODEL = os.path.join(
		os.path.dirname(os.path.realpath(__file__)),
		"models",
		"vosk-model-br-0.8"
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
	parser.add_argument("--translate", nargs='+', metavar="TRANSLATION_DICT",
		help="Use additional translation dictionaries")
	parser.add_argument("--keep-fillers", action="store_true",
		help="Keep verbal fillers ('euh', 'beñ', 'alors', 'kwa'...)")
	parser.add_argument("-t", "--type", choices=["txt", "srt", "eaf", "split"],
		help="file output type")
	parser.add_argument("-o", "--output", help="write to a file")
	parser.add_argument("--segment-min-length",
		help="Try not to go under this length when segmenting audio file",
		type=int, default=2)
	parser.add_argument("--segment-max-length",
		help="Try not to go above this length when segmenting audio file",
		type=int, default=15)
	args = parser.parse_args()
	print(args)

	translation_dicts = []
	if args.translate:
		translation_dicts = [ load_translation_dict(path) for path in args.translate ]

	fout = open(args.output, 'w') if args.output else sys.stdout

	if not args.type:
		if args.output:
			# No explicit type was given to we'll try to infer it from output file extension
			ext = os.path.splitext(args.output)[1][1:]
			if ext.lower() in ("srt", "split", "eaf"):
				args.type = ext.lower()
			else:
				args.type = "txt"	# Default type
		else:
			args.type = "txt"

	if args.type == "txt":
		SetLogLevel(-1)
		model = Model(args.model)
		rec = KaldiRecognizer(model, 16000)
		rec.SetWords(True)

		with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
								args.filename,
								"-ar", "16000" , "-ac", "1", "-f", "s16le", "-"],
								stdout=subprocess.PIPE).stdout as stream:
			while True:
				data = stream.read(4000)
				if len(data) == 0:
					break
				if rec.AcceptWaveform(data):
					sentence = json.loads(rec.Result())["text"]
					print(
						format_output(
							sentence,
							normalize=args.normalize,
							keep_fillers=args.keep_fillers),
						file=fout)
			sentence = json.loads(rec.FinalResult())["text"]
			print(
				format_output(
					sentence,
					normalize=args.normalize,
					keep_fillers=args.keep_fillers),
				file=fout)


	elif args.type in ("srt", "split", "eaf"):
		if args.model:
			load_vosk(args.model)

		song = AudioSegment.from_file(args.filename)
		song = song.set_channels(1)
		if song.frame_rate != 16000:
			song = song.set_frame_rate(16000)
		if song.sample_width != 2:
			song = song.set_sample_width(2)
		
		# Audio need to be segmented first
		print("Segmenting audio file...")
		segments = split_to_segments(
			song,
			max_length=args.segment_max_length,
			min_length=args.segment_min_length)
		segments = [[0, len(song)]]
		print(f"{len(segments)} segment{'s' if len(segments)>1 else ''} found")

		t_min, t_max = 0, segments[-1][1]
		sentences = [
			# transcribe_segment_timecoded(seg[max(t_min, seg[0]-200):min(t_max, seg[1]+200)])
			transcribe_segment_timecoded(song[max(t_min, seg[0]-200):min(t_max, seg[1]+200)])
			for seg in segments
		]
		# sentences = []
		# for start, end in segments:
		# 	sentences.append(transcribe_segment_timecoded(song[start:end]))
		
		# We need to apply text post-processing here
		sentences = [
			post_process_timecoded(sent, args.normalize, args.keep_fillers)
			for sent in sentences
		]

		# Remove empty sentences and associated segments
		new_segments = []
		new_sentences = []
		for i, sentence in enumerate(sentences):
			if not sentence:
				continue
			new_sentences.append(sentence)
			new_segments.append(segments[i])
		segments = new_segments
		sentences = new_sentences


		if args.type == 'split':
			for start, end in segments:
				print(f"{start} {end}", file=fout)
			
			textfile_header = \
			"{source: }\n{source-audio: }\n{author: }\n{licence: }\n{tags: }\n\n\n\n"
			
			if args.output:
				basename = os.path.splitext(args.output)[0]
			else:
				basename = os.path.splitext(args.filename)[0]
			text_filename = os.path.extsep.join([basename, 'txt'])
			
			with open(text_filename, 'w') as fw:
				fw.write(textfile_header)  # Text file split_header
				for s in sentences:
					sentence = ' '.join([token['word'] for token in s])
					fw.write(sentence + '\n')
		
		elif args.type == 'srt':
			words_per_line = 7
			subs = []
			for i, sentence in enumerate(sentences):
				if sentence:
					print("sent", sentence[0]["start"], sentence[-1]["end"])
					print("seg", segments[i][0]/1000, segments[i][1]/1000)
				else:
					print("none")
				for j in range(0, len(sentence), words_per_line):
					line = sentence[j : j + words_per_line]
					text = ' '.join([ w["word"] for w in line ])
					for td in translation_dicts:
						text = detokenize( translate(tokenize(text), td) )

					s = srt.Subtitle(index=len(subs),
							content=text,
							start=datetime.timedelta(seconds=line[0]["start"] + segments[i][0]/1000),
							end=datetime.timedelta(seconds=line[-1]["end"] + segments[i][0]/1000))
					subs.append(s)

			print(srt.compose(subs), file=fout)
		
		elif args.type == 'eaf':
			export_to_eaf(segments, sentences, args.filename)

			
		
	if args.output:
		fout.close()
	

if __name__ == "__main__":
	main_adskrivan()
