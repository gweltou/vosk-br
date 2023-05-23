import os
from typing import List
from ..text.inverse_normalizer import inverse_normalize_sentence, inverse_normalize_vosk
from ..text.definitions import is_noun
from ..utils import read_file_drop_comments



def post_process_text(sentence: str, normalize=False) -> str:
    sentence = apply_post_process_dict_text(sentence, _postproc_dict)
    
    # Add hyphens for "-se" and "-mañ"
    sentence = sentence.split()
    parsed = []
    idx = 1
    while idx < len(sentence):
        if sentence[idx] in ("se", "mañ") and is_noun(sentence[idx-1]):
            parsed.append('-'.join(sentence[idx-1:idx+1]))
            idx += 1
        else:
            parsed.append(sentence[idx-1])
        idx += 1
    if idx == len(sentence):
        parsed.append(sentence[idx-1])
    sentence = ' '.join(parsed)

    if normalize:
        sentence = apply_post_process_dict_text(sentence, _inorm_units_dict)
        sentence = inverse_normalize_sentence(sentence)
    return sentence



def post_process_vosk(tokens: List[dict], normalize=False) -> List[dict]:
    tokens = apply_post_process_dict_vosk(tokens, _postproc_dict)

    # Add hyphens for "-se" and "-mañ"
    parsed = []
    idx = 1
    while idx < len(tokens):
        if tokens[idx]["word"] in ("se", "mañ") and is_noun(tokens[idx-1]["word"]):
            word = tokens[idx-1]["word"] + '-' + tokens[idx]["word"]
            new_token = {
                        "word": word,
                        "start": tokens[idx-1]["start"],
                        "end": tokens[idx]["end"],
                        "conf": tokens[idx-1]["conf"]
                        }
            parsed.append(new_token)
            idx += 1
        else:
            parsed.append(tokens[idx-1])
        idx += 1
    if idx == len(tokens):
        parsed.append(tokens[idx-1])
    tokens = parsed

    if normalize:
        tokens = apply_post_process_dict_vosk(tokens, _inorm_units_dict)
        tokens = inverse_normalize_vosk(tokens)
    return tokens



def load_postproc_dict(filepath: str) -> List[dict]:
    """ Load the post processing dictionary from a tsv file
        Keys are treated uncased
    """

    trigrams = dict()
    bigrams = dict()
    monograms = dict()
    for l in read_file_drop_comments(filepath):
        k, v = l.split('\t')
        k = tuple([t.lower() for t in k.split()])
        v = tuple(v.split())
        if len(k) == 1:
            monograms[k] = v
        elif len(k) == 2:
            bigrams[k] = v
        elif len(k) == 3:
            trigrams[k] = v
        else:
            print("ERROR (postproc_dict): number of tokens should be between 1 and 3")
            print(k)
    
    return [monograms, bigrams, trigrams]

_postproc_dict_path = os.path.join(os.path.split(__file__)[0], "postproc_sub.tsv")
_postproc_dict = load_postproc_dict(_postproc_dict_path)

_inorm_units_dict_path = os.path.join(os.path.split(__file__)[0], "inorm_units.tsv")
_inorm_units_dict = load_postproc_dict(_inorm_units_dict_path)



def apply_post_process_dict_text(sentence: str, ngram_dicts: List[dict]=_postproc_dict) -> str:

    def check_ngram(n: int):
        ngram = tuple( [ t.lower() for t in tokens[idx:idx+n] ] )
        sub = ngram_dicts[n-1].get(ngram, None)
        if sub:
            for t in sub:
                translated.append(t)
            return True
        return False
    
    tokens = sentence.split()
    translated = []
    tlen = len(tokens)
    idx = 0
    while idx < tlen:
        if idx <= tlen-3 and check_ngram(3):
            idx += 3
            continue
        if idx <= tlen-2 and check_ngram(2):
            idx += 2
            continue
        if idx <= tlen-1 and check_ngram(1):
            pass
        else:
            translated.append(tokens[idx])
        idx += 1

    return ' '.join(translated)



def apply_post_process_dict_vosk(tokens: List[dict], ngram_dicts: List[dict]=_postproc_dict) -> List[dict]:

    def check_ngram(n: int):
        ngram = tuple( [ t["word"].lower() for t in tokens[idx:idx+n] ] )
        sub = ngram_dicts[n-1].get(ngram, None)
        if sub:
            t_start = tokens[idx]["start"]
            t_dur = tokens[idx+n-1]["end"] - t_start
            t_dur = t_dur / len(sub)
            conf = tokens[idx]["conf"]
            for t in sub:
                token = {"word": t, "start": t_start, "end": t_start + t_dur, "conf": conf}
                translated.append(token)
                t_start += t_dur
            return True
        return False
    
    translated = []
    tlen = len(tokens)
    idx = 0
    while idx < tlen:
        if idx <= tlen-3 and check_ngram(3):
            idx += 3
            continue
        if idx <= tlen-2 and check_ngram(2):
            idx += 2
            continue
        if idx <= tlen-1 and check_ngram(1):
            pass
        else:
            translated.append(tokens[idx])
        idx += 1

    return translated
