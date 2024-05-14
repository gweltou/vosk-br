from typing import List
import os
import sys
import subprocess
import json

from vosk import KaldiRecognizer
from pydub import AudioSegment
from tqdm import tqdm
from math import ceil

from .models import load_model
from .post_processing import post_process_text, post_process_timecoded
from ..audio import get_audiofile_length



def transcribe_segment(segment: AudioSegment) -> str:
    """ Transcribe a short AudioSegment """
    model = load_model()
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    
    data = segment.raw_data
    text = []
    i = 0
    while i + 4000 < len(data):
        if recognizer.AcceptWaveform(data[i:i+4000]):
            text.append(json.loads(recognizer.Result())["text"])
        i += 4000
    recognizer.AcceptWaveform(data[i:])
    text.append(json.loads(recognizer.FinalResult())["text"])

    return text



def transcribe_segment_timecoded(segment: AudioSegment) -> List[dict]:
    """ Transcribe a short AudioSegment, keeping the timecodes

        The resulting transcription is a list of Vosk tokens
        Each Vosk token is a dictionary of the form:
            {'word': str, 'start': float, 'end': float, 'conf': float}
        'start' and 'end' keys are in seconds
        'conf' is a normalized confidence score
    """
    model = load_model()
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    
    data = segment.get_array_of_samples().tobytes()
    timecoded_text = []
    i = 0
    while i + 4000 < len(data):
        if recognizer.AcceptWaveform(data[i:i+4000]):
            result = json.loads(recognizer.Result())
            if "result" in result:
                timecoded_text.extend(result["result"])
        i += 4000
    recognizer.AcceptWaveform(data[i:])
    result = json.loads(recognizer.FinalResult())
    if "result" in result:
        timecoded_text.extend(result["result"])
    
    return timecoded_text



def transcribe_file(filepath: str, normalize=False) -> List[str]:
    def format_output(sentence, normalize=False):
        sentence = post_process_text(sentence, normalize)
        return sentence
    
    if not os.path.exists(filepath):
        print("Couldn't find {}".format(filepath), file=sys.stderr)

    model = load_model()
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    
    text = []

    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                filepath,
                                "-ar", "16000" , "-ac", "1", "-f", "s16le", "-"],
                                stdout=subprocess.PIPE) as process:

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                sentence = json.loads(recognizer.Result())["text"]
                result = format_output(sentence, normalize)
                if result:
                    text.append(result)
        sentence = json.loads(recognizer.FinalResult())["text"]
        result = format_output(sentence, normalize)
        if result:
            text.append(result)
    
    return text



def transcribe_file_timecoded(filepath: str, normalize=False) -> List[dict]:
    """ Return list of infered words with associated timecodes (vosk format)

        Parameters
            normalized (boolean): inverse-normalize sentences
        
        The resulting transcription is a list of Vosk tokens
        Each Vosk token is a dictionary of the form:
            {'word': str, 'start': float, 'end': float, 'conf': float}
        'start' and 'end' keys are in seconds
        'conf' is a normalized confidence score
    """

    def format_output(result) -> List[dict]:
        jres = json.loads(result)
        return jres.get("result", [])

    model = load_model()
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    
    total_duration = get_audiofile_length(filepath)
    progress_bar = tqdm(total=ceil(total_duration))
    i = 0
    cumul_frames = 0

    tokens = []
    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                filepath,
                                "-ar", "16000" , "-ac", "1", "-f", "s16le", "-"],
                                stdout=subprocess.PIPE) as process:
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                tokens.extend(format_output(recognizer.Result()))
            cumul_frames += len(data) // 2
            if i%10 == 0:
                progress_bar.update(cumul_frames / 16000)
                cumul_frames = 0
            i += 1
        tokens.extend(format_output(recognizer.FinalResult()))
    progress_bar.close()
    
    return tokens
