#! /usr/bin/env python3

import sys
import os.path
import datetime
from math import floor, ceil
import argparse
import subprocess

import static_ffmpeg
import json
import srt
from vosk import KaldiRecognizer
from pydub import AudioSegment

from anaouder.asr.models import load_model, DEFAULT_MODEL
from anaouder.asr.recognizer import transcribe_file_timecoded, transcribe_segment_timecoded
from anaouder.asr.post_processing import post_process_text, post_process_timecoded
from anaouder.audio import split_to_segments, convert_to_wav
from anaouder.utils import write_eaf
from anaouder.version import VERSION



def _split_vosk_tokens(tokens, min_silence=0.5):
    subsegments = []
    current_segment = [tokens[0]]
    for tok in tokens[1:]:
        if tok['start'] - current_segment[-1]['end'] > min_silence:
            # We shall split here
            subsegments.append(current_segment)
            current_segment = []
        current_segment.append(tok)
    subsegments.append(current_segment)
    return subsegments


def split_vosk_tokens(tokens, max_length=15):
    """ Split sequences of Vosk tokens on silences """
    token_segments = [tokens]
    silence_length = 1.0

    while True:
        n_long_segments = 0
        parsed = []
        for segment in token_segments:
            dur = segment[-1]['end'] - segment[0]['start']
            if dur > max_length:
                # Split this segment deeper
                sub = _split_vosk_tokens(segment, silence_length)
                parsed.extend(sub)
                n_long_segments += 1
            else:
                parsed.append(segment)
        token_segments = parsed
        silence_length -= 0.1
        if n_long_segments == 0 or silence_length < 0.3:
            break
    
    return token_segments


def main_adskrivan(*args, **kwargs) -> None:
    """ adskrivan cli entry point """

    desc = f"Decode an audio file in any format, with the help of ffmpeg"
    parser = argparse.ArgumentParser(description=desc, prog="adskrivan")
    parser.add_argument('filename')
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL,
        help="Vosk model to use for decoding", metavar='MODEL_PATH')
    parser.add_argument("-n", "--normalize", action="store_true",
        help="Normalize numbers")
    parser.add_argument("--keep-fillers", action="store_true",
        help="Keep verbal fillers ('euh', 'beñ', 'alors', 'kwa'...)")
    parser.add_argument("-t", "--type", choices=["txt", "srt", "eaf", "seg"],
        help="file output type")
    parser.add_argument("-o", "--output", help="write to a file")
    parser.add_argument("--autosplit", action="store_true",
        help="Automatically split audio at silences (used with 'srt', 'eaf' or 'seg' type only)")
    parser.add_argument("--segment-min-length",
        help="Will try not to go under this length when segmenting audio files (seconds)",
        type=float, default=2)
    parser.add_argument("--segment-max-length",
        help="Will try not to go above this length when segmenting audio files (seconds)",
        type=float, default=8)
    parser.add_argument("--max_words_per_line", type=int, default=7,
        help="Number of words per line for subtitle files")
    parser.add_argument("--set-ffmpeg-path", type=str,
        help="Set ffmpeg path (will not use static_ffmpeg in that case)")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")

    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()
    
    if not os.path.exists(args.filename):
        print("Couldn't find file '{}'".format(args.filename))
        sys.exit(1)
        
    
    # Use static_ffmpeg instead of ffmpeg
    ffmpeg_path = "ffmpeg"
    if args.set_ffmpeg_path:
        ffmpeg_path = args.set_ffmpeg_path
    else:
        static_ffmpeg.add_paths()
    

    if args.type == "seg":
        if args.output:
            args.output = args.output.replace(' ', '_')
        else:
            args.output = args.filename.replace(' ', '_')
            ext = os.path.splitext(args.output)[1]
            args.output = args.output.replace(ext, ".seg")
    
    fout = open(args.output, 'w') if args.output else sys.stdout

    if not args.type:
        if args.output:
            # No explicit type was given to we'll try to infer it from output file extension
            ext = os.path.splitext(args.output)[1][1:]
            if ext.lower() in ("srt", "seg", "eaf"):
                args.type = ext.lower()
            else:
                args.type = "txt"	# Default type
        else:
            args.type = "txt"

    model = load_model(args.model)

    if args.type == "txt":
        # No need of timecodes

        if args.output:
            # Whole file decoding
            # Different segmentation algorithm than online decoding
            # Shows a progress bar
            print("Transcribing audio file...", flush=True)
            tokens = transcribe_file_timecoded(args.filename)
            token_segments = split_vosk_tokens(tokens, max_length=args.segment_max_length)
            token_segments = [
                post_process_timecoded(seg, args.normalize, args.keep_fillers)
                for seg in token_segments
            ]
            sentences = [ ' '.join([token['word'] for token in seg]) for seg in token_segments ]

            fout.write('\n'.join(sentences))
        else:
            # Online decoding
            # Print decoded sentences one-by-one
            rec = KaldiRecognizer(model, 16000)
            rec.SetWords(True)
        
            with subprocess.Popen([ffmpeg_path, "-loglevel", "quiet", "-i",
                                    args.filename,
                                    "-ar", "16000" , "-ac", "1", "-f", "s16le", "-"],
                                    stdout=subprocess.PIPE).stdout as stream:
                while True:
                    data = stream.read(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        sentence = json.loads(rec.Result())["text"]
                        sentence = post_process_text(sentence, normalize=args.normalize, keep_fillers=args.keep_fillers)
                        if sentence: print(sentence, file=fout)

                sentence = json.loads(rec.FinalResult())["text"]
                sentence = post_process_text(sentence, normalize=args.normalize, keep_fillers=args.keep_fillers)
                if sentence: print(sentence, file=fout)


    elif args.type in ("srt", "seg", "eaf"):
        # Transcribe with timecodes
        
        if args.autosplit:
            song = AudioSegment.from_file(args.filename)
            song = song.set_channels(1)
            if song.frame_rate != 16000:
                song = song.set_frame_rate(16000)
            if song.sample_width != 2:
                song = song.set_sample_width(2)
            
            # Audio need to be segmented first
            print("Segmenting audio file...", end=' ', flush=True)
            segments = split_to_segments(
                song,
                max_length=args.segment_max_length,
                min_length=args.segment_min_length)
            print(f"{len(segments)} segment{'s' if len(segments)>1 else ''} found")

            t_min, t_max = 0, segments[-1][1]
            sentences = []
            for seg in segments:
                tr = transcribe_segment_timecoded(song[max(t_min, seg[0]-200):min(t_max, seg[1]+200)])
                sentences.append(tr)
            
        else:
            print("Transcribing audio file...", flush=True)
            tokens = transcribe_file_timecoded(args.filename)
            sentences = split_vosk_tokens(tokens, max_length=args.segment_max_length)
            segments = [ [floor(sent[0]['start']*1000), ceil(sent[-1]['end']*1000)]
                               for sent in sentences ]

        # Remove empty sentences
        new_sentences = [s for s in sentences if s]
        new_segments = [segments[i] for i, s in enumerate(sentences) if s]
        segments = new_segments
        sentences = new_sentences

        # Apply text post-processing
        if args.type == "seg":
            args.keep_fillers = True
        sentences = [
            post_process_timecoded(sent, args.normalize, args.keep_fillers)
            for sent in sentences
        ]


        if args.type == 'seg':
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
            
            wav_filename = os.path.extsep.join([basename, 'wav'])
            print(args.filename, wav_filename)
            convert_to_wav(args.filename, wav_filename)
        
        
        elif args.type == 'srt':
            words_per_line = args.max_words_per_line
            if words_per_line == 0: words_per_line = 999
            subs = []
            for i, sentence in enumerate(sentences):
                for j in range(0, len(sentence), words_per_line):
                    line = sentence[j : j + words_per_line]
                    text = ' '.join([ w["word"] for w in line ])

                    if args.autosplit:
                        offset = segments[i][0]/1000
                        s = srt.Subtitle(index=len(subs),
                                content=text,
                                start=datetime.timedelta(seconds=line[0]["start"]+offset),
                                end=datetime.timedelta(seconds=line[-1]["end"]+offset))
                    else:
                        s = srt.Subtitle(index=len(subs),
                                content=text,
                                start=datetime.timedelta(seconds=line[0]["start"]),
                                end=datetime.timedelta(seconds=line[-1]["end"]))
                    subs.append(s)
            
            # Write to a srt file with the same name as input file by default
            if not args.output:
                srt_path = os.path.splitext(args.filename)[0] + ".srt"
                fout = open(srt_path, 'w')

            print(srt.compose(subs), file=fout)
        
        
        elif args.type == 'eaf':
            text_sentences = []
            for sentence in sentences:
                sentence = ' '.join([ t['word'] for t in sentence ])
                text_sentences.append(sentence)
            ext = os.path.splitext(args.output)[1][1:].lower()
            if ext not in ('mp3', 'wav'):
                data = write_eaf(segments, text_sentences, args.filename, type="mp3")
            else:
                data = write_eaf(segments, text_sentences, args.filename)

            print(data, file=fout)
            if args.output:
                print("EAF file written to", os.path.abspath(args.output))

  
    if args.output:
        fout.close()
    

if __name__ == "__main__":
    main_adskrivan()