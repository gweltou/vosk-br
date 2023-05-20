from typing import List
import os
import subprocess
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from .post_processing import apply_post_process_dict_text, post_process_text, post_process_vosk
from ..text.inverse_normalizer import inverse_normalize_vosk



_vosk_loaded = False
MODEL_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', '..', '..', 'models'))
DEFAULT_MODEL = os.path.join(MODEL_DIR, "current")



def load_vosk(path: str = DEFAULT_MODEL) -> None:
    global recognizer
    global _vosk_loaded

    SetLogLevel(-1)
    model_path = os.path.normpath(path)
    # print("Loading model", model_path)
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    _vosk_loaded = True



def transcribe_file(filepath: str, normalize=False) -> List[str]:

    def format_output(result, normalize=False):
        sentence = eval(result)["text"]
        sentence = post_process_text(sentence, normalize)
        return sentence

    if not _vosk_loaded:
        load_vosk()
    
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
                result = format_output(recognizer.Result(), normalize)
                if result:
                    text.append(result)
        result = format_output(recognizer.FinalResult(), normalize)
        if result:
            text.append(result)
    
    return text



def transcribe_file_timecode(filepath: str, normalize=False) -> List[str]:
    """ Return list of infered words with associated timecodes (vosk format)

        Parameters
            normalized (boolean): inverse-normalize sentences
    """

    def format_output(result, normalize=False) -> List[dict]:
        jres = json.loads(result)
        if not "result" in jres:
            return []
        words = jres["result"]
        words = post_process_vosk(words, normalize)
        return words

    if not _vosk_loaded:
        load_vosk()

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