from typing import List
import os
import sys
import subprocess
import json

from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment

from .post_processing import apply_post_process_dict_text, post_process_text, post_process_timecoded
from ..text.inverse_normalizer import inverse_normalize_timecoded



_vosk_loaded = False
MODEL_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', '..', '..', 'models'))
DEFAULT_MODEL = os.path.join(MODEL_DIR, "current")



def load_vosk(path: str = DEFAULT_MODEL) -> None:
    global _vosk_loaded
    global model

    SetLogLevel(-1)
    model_path = os.path.normpath(path or DEFAULT_MODEL)
    print("Loading vosk model", model_path, file=sys.stderr)
    model = Model(model_path)
    _vosk_loaded = True



def transcribe_segment(segment: AudioSegment) -> str:
    """ Transcribe a short AudioSegment """
    if not _vosk_loaded:
        load_vosk()
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
    if not _vosk_loaded:
        load_vosk()
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

    if not _vosk_loaded:
        load_vosk()
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

    def format_output(result, normalize=False) -> List[dict]:
        jres = json.loads(result)
        if not "result" in jres:
            return []
        words = jres["result"]
        words = post_process_timecoded(words, normalize)
        return words

    if not _vosk_loaded:
        load_vosk()
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)

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
                tokens.extend(format_output(recognizer.Result(), normalize))
        tokens.extend(format_output(recognizer.FinalResult(), normalize))
    
    return tokens