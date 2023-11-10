from typing import Iterator, Any

from .tokenizer import Token, tokenize, detokenize, split_sentences
from .normalizer import normalize, normalize_sentence
from .inverse_normalizer import inverse_normalize_sentence, inverse_normalize_timecoded
from .utils import (
    strip_punct, filter_out, capitalize, pre_process,
    extract_parenthesis_content, sentence_stats,
)
from .definitions import PUNCTUATION
from ..utils import read_file_drop_comments



def load_translation_dict(path: str) -> dict:
    translation_dict = dict()
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if '\t' in line:
                key, val = line.split('\t')
                translation_dict[key] = val
            else:
                translation_dict[line] = ""
    return translation_dict



def reverse_translation_dict(path: str, newpath: str) -> None:
    reversed = dict()
    for line in read_file_drop_comments(path):
        line = pre_process(line)
        if '\t' in line:
            key, val = line.split('\t')
            if ' ' in key or ' ' in val:
                print("no spaces allowed in translation dictionaries")
                continue
            if val in reversed:
                reversed[val] += ", {}".format(key)
            else:
                reversed[val] = key
    with open(newpath, 'w') as f:
        for k in sorted(reversed):
            f.write(f"{k}\t{reversed[k]}\n")



def correct_sentence(sentence: str) -> str:
    return detokenize(tokenize(sentence, autocorrect=True))



def translate(token_stream: Iterator[Token], tra_dict: dict, **options: Any) -> Iterator[Token]:
    """ Substitute tokens according to a given dictionary
        
        Keys with uppercase letters will be case-sentitive
        Keys with lowercase letters only will be case-insensitive
        Translate will operate according to the first match in the dictionary

        Key/value pairs of the translation dictionary can contain
        the '*' character to match any character
        Ex: "*a" : "*añ"    -> will change suffixes of words ending with 'a'
    """

    for tok in token_stream:
        for key, val in tra_dict.items():
            if key.startswith('*'):
                if key.endswith('*'):
                    # Match chars in the middle of words
                    expr = key.strip('*')
                    if expr in tok.data:
                        tok.data.replace(expr, val.strip('*'))
                else:
                    # Match at the end
                    expr = key.lstrip('*')
                    if tok.data.endswith(expr):
                        tok.data = tok.data[:-len(expr)] + val.lstrip('*')
            elif key.endswith('*'):
                # Match at the beginning
                expr = key.rstrip('*')
                if tok.data.startswith(expr):
                    tok.data = val.rstrip('*') + tok.data[len(expr):]
            elif key.islower():
                if key == tok.data.lower():
                    if tok.data.istitle():
                        tok.data = val.capitalize()
                    elif tok.data.isupper():
                        tok.data = val.upper()
                    else:
                        tok.data = val
                    break
            else:
                if key == tok.data:
                    tok.data = tra_dict[tok.data]
                    break
        yield tok
