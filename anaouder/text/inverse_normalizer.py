import os
from typing import List
from .definitions import is_noun



token_value = {
    "mann" : 0, "zero" : 0,
    "un" : 1, "ur" : 1, "ul" : 1, "unan" : 1,
    "daou" : 2, "zaou" : 2, "div" : 2,
    "tri" : 3, "teir" : 3,
    "pevar" : 4, "peder" : 4,
    "pemp" : 5, "bemp" : 5,
    "c'hwec'h" : 6,
    "seizh" : 7,
    "eizh" : 8,
    "nav" : 9,
    "dek" : 10,
    "unnek" : 11,
    "daouzek" : 12,
    "trizek" : 13,
    "pevarzek" : 14,
    "pemzek" : 15,
    "c'hwezek" : 16,
    "seitek" : 17,
    "triwec'h" : 18,
    "naontek" : 19,
    "ugent" : 20,
    "tregont" : 30,
    "kant" : 100, "c'hant" : 100,
    "mil" : 1000, "vil" : 1000,
    "milion" : 1_000_000, "vilion" : 1_000_000,
    "miliard" : 1_000_000_000, "viliard" : 1_000_000_000,
    "hanter" : 0.5,
    "ha" : '+', "hag" : '+', "warn" : '+'
}


# A star character represents any noun
numtok_chain = {
	'[': ['zero', 'unan', 'un', 'ul', 'ur', 'daou', 'zaou', 'div', 'tri', 'teir', 'pevar', 'peder', 'pemp', "bemp", "c'hwec'h", 'seizh', 'eizh', 'nav', 'dek', 'unnek', 'daouzek', 'trizek', 'pevarzek', 'pemzek', "c'hwezek", 'seitek', "triwec'h", 'naontek', 'ugent', 'tregont', 'kant', 'mil', 'hanter'],
	'zero': [']'],
	'unan': [']', 'warn', 'ha', 'hag'],
	'ur': ["c'hant", 'mil', 'milion', 'miliard', '*'],
    'un': [']', 'warn', 'ha', 'hag', '*'],
    'ul': [']', 'warn', 'ha', 'hag', '*'],
	'daou': [']', 'warn', 'ha', 'ugent', 'hag', "c'hant", 'vil', 'vilion', 'viliard', '*'],
    'zaou': [']', 'warn', 'ha', 'ugent', 'hag', "c'hant", 'vil', 'vilion', 'viliard', '*'],
    'div': [']', 'warn', 'ha', 'hag', '*'],
	'tri': [']', 'warn', 'ha', 'hag', 'ugent', "c'hant", 'mil', 'milion', '*'],
    'teir': [']', 'warn', 'ha', 'hag', '*'],
	'pevar': [']', 'warn', 'ha', 'hag', 'ugent', "c'hant", 'mil', 'milion', '*'],
    'peder': [']', 'warn', 'ha', 'hag', '*'],
	'pemp': [']', 'warn', 'ha', 'hag', 'kant', 'mil', 'milion', '*'],
    'bemp': [']', 'warn', 'ha', 'hag', 'kant', 'mil', 'milion', '*'],
	"c'hwec'h": [']', 'warn', 'ha', 'hag', 'kant', 'mil', 'milion', '*'],
	'seizh': [']', 'warn', 'ha', 'hag', 'kant', 'mil', 'milion', '*'],
	'eizh': [']', 'warn', 'ha', 'hag', 'kant', 'mil', 'milion', '*'],
	'nav': [']', 'warn', 'ha', 'hag', "c'hant", 'mil', 'milion', '*'],
	'dek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'unnek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'daouzek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'trizek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'pevarzek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'pemzek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	"c'hwezek": [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'seitek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	"triwec'h": [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'naontek': [']', 'ha', 'kant', 'mil', 'milion', '*'],
	'ugent': [']', 'mil', 'milion', 'mil', 'milion', '*'],
	'tregont': [']', 'mil', 'milion', 'mil', 'milion', '*'],
	'kant': [']', 'unan', 'un', 'ul', 'ur', 'daou', 'tri', 'pevar', 'pemp', "c'hwec'h", 'seizh', 'eizh', 'nav', 'dek', 'unnek', 'daouzek', 'trizek', 'pevarzek', 'pemzek', "c'hwezek", 'seitek', "triwec'h", 'naontek', 'ugent', 'tregont', 'hanter', 'mil', 'milion', '*'],
	"c'hant": [']', 'unan', 'un', 'ul', 'ur', 'daou', 'tri', 'pevar', 'pemp', "c'hwec'h", 'seizh', 'eizh', 'nav', 'dek', 'unnek', 'daouzek', 'trizek', 'pevarzek', 'pemzek', "c'hwezek", 'seitek', "triwec'h", 'naontek', 'ugent', 'tregont', 'hanter', 'mil', 'milion', '*'],
	'mil': [']', 'unan', 'un', 'ul', 'ur', 'daou', 'tri', 'pevar', 'pemp', "c'hwec'h", 'seizh', 'eizh', 'nav', 'dek', 'unnek', 'daouzek', 'trizek', 'pevarzek', 'pemzek', "c'hwezek", 'seitek', "triwec'h", 'naontek', 'ugent', 'tregont', 'hanter', 'kant', '*'],
	'vil': [']', 'unan', 'un', 'ul', 'ur', 'daou', 'tri', 'pevar', 'pemp', "c'hwec'h", 'seizh', 'eizh', 'nav', 'dek', 'unnek', 'daouzek', 'trizek', 'pevarzek', 'pemzek', "c'hwezek", 'seitek', "triwec'h", 'naontek', 'ugent', 'tregont', 'hanter', 'kant', '*'],
	'milion': [']', '*'], 'vilion': [']', '*'],
	'miliard': [']', '*'], 'viliard': [']', '*'],
	'ha': ['tregont', 'daou', 'tri', 'pevar'],
	'hag': ['hanter'],
	'hanter': ['kant'],
	'warn': ['ugent'],
}



def solve_num_tokens(numerical_tokens: List[float]) -> float:
    # Token 0.5 ("hanter") takes precedence and is applied to next closest token
    while 0.5 in numerical_tokens:
        i = numerical_tokens.index(0.5)
        if i < len(numerical_tokens) - 1:
            numerical_tokens = numerical_tokens[:i] + [0.5*numerical_tokens[i+1]] + numerical_tokens[i+2:]
        else:
            break

    # Find highest value token
    i_max, val_max = -1, -1
    i_token_add, token_add = -1, False
    for i, val in enumerate(numerical_tokens):
        if val == '+':
            token_add = True
            i_token_add = i
        elif val > val_max:
            val_max = val
            i_max = i
    
    if token_add and val_max < 100:
        # Invert two parts of token_list around '+' symbol and solve
        inverted = numerical_tokens[i_token_add+1:] + numerical_tokens[:i_token_add]
        return solve_num_tokens(inverted)
    else:
        # solve recursively
        if len(numerical_tokens) == 0:
            return 0
        elif len(numerical_tokens) == 1:
            return numerical_tokens[0]
        else:
            left_part = solve_num_tokens(numerical_tokens[:i_max])
            if left_part == 0:
                left_part = 1
            right_part = solve_num_tokens(numerical_tokens[i_max+1:])
            return left_part * val_max + right_part



def inverse_normalize_sentence(sentence: str, min_num=5) -> str:
    """ Translate spelled numbers to more readable numbers
        This is a simple function expected on plain sentences with no punctuation
        The sentence is simply split on whitespaces

        Parameter
        ---------
            min_num (int):
                numbers below `min_num` won't be normalized
    """

    def flush_number():
        nonlocal num_tokens
        nonlocal noun
        num = solve_num_tokens( [token_value[t] for t in num_tokens] )
        if num >= min_num:
            translated.append(str(int(num)))
        else:
            translated.extend(num_tokens)
        if noun:
            translated.append(noun)
            noun = None
        num_tokens = []

    
    starters = numtok_chain['[']
    sentence = sentence.replace("-ugent", " ugent")
    sentence = sentence.replace("-kant", " kant")
    tokens = sentence.split()
    num_tokens = []
    in_chain = False
    noun = None
    translated = []
    for idx, tok in enumerate(tokens):
        if not in_chain and tok in starters:
            # Beginning of a numerical chain of words
            in_chain = True
            num_tokens = [tok]
        
        elif in_chain:
            prev = num_tokens[-1]
            if tok in numtok_chain[prev]:
                # Follow the chain of words describing a number
                num_tokens.append(tok)
            
            elif tok in starters:
                # Check for ill-formed numerical sequences,
                if ']' not in numtok_chain[prev]:
                    # treat as 2 numerical sequence in that case
                    # rewind and flush the first part
                    i = len(num_tokens)-1
                    while i >= 0 and num_tokens[i] not in ("ha", "hag"):
                        i -= 1
                    next_num_tokens = num_tokens[i+1:]
                    conj = num_tokens[i]
                    num_tokens = num_tokens[:i]
                    flush_number()
                    translated.append(conj)
                    num_tokens = next_num_tokens + [tok]
                else:
                    flush_number()
                    num_tokens = [tok]
            
            elif  '*' in numtok_chain[prev] and is_noun(tok) or tok in ('%',):
                if noun:
                    # There could be an ambiguity if another noun has already been found
                    # ex: "tri kazh ha daou besk"
                    # In that case...
                    i = len(num_tokens)-1
                    while i >= 0 and num_tokens[i] not in ("ha", "hag"):
                        i -= 1
                    next_num_tokens = num_tokens[i+1:]
                    conj = num_tokens[i]
                    num_tokens = num_tokens[:i]
                    flush_number()
                    translated.append(conj)
                    num_tokens = next_num_tokens
                    noun = tok
                elif len(tokens) > idx+1 and tokens[idx+1] in ('ha', 'hag', 'warn'):
                    noun = tok
                else:
                    # final noun
                    noun = tok
                    flush_number()
                    in_chain = False
            
            else:
                flush_number()
                translated.append(tok)
                in_chain = False

        else:
            translated.append(tok)
    
    if in_chain:
        flush_number()

    return ' '.join(translated)



def inverse_normalize_vosk(tokens: List[dict], min_num=5) -> List[dict]:
    """ Translate spelled numbers to more readable numbers
        Same functionality as the function `inverse_normalise_sentence` but
        works with vosk token (embedding timecodes and confidence values)

        Parameter
        ---------
            min_num (int):
                numbers below `min_num` won't be normalized
    """

    def flush_number():
        nonlocal num_tokens
        nonlocal noun
        num = solve_num_tokens( [token_value[t["word"]] for t in num_tokens] )
        if num >= min_num:
            # Create a new token for this number
            t_start = num_tokens[0]["start"]
            t_end = num_tokens[-1]["end"]
            word = str(int(num))
            vosk_token = {"word": word, "start": t_start, "end": t_end, "conf": 1.0}
            translated.append(vosk_token)
        else:
            translated.extend(num_tokens)
        if noun:
            if noun["start"] < translated[-1]["end"]:
                # Order of tokens has been changed, correct timecodes
                dur = noun["end"] - noun["start"]
                translated[-1]["end"] -= dur
                noun["start"] = translated[-1]["end"]
                noun["end"] = noun["start"] + dur
            translated.append(noun)
            noun = None
        num_tokens = []
    

    # Start by splitting numerical words containing hyphens
    parsed_tokens = []
    for tok in tokens:
        word = tok["word"]
        if word.endswith("-ugent") or word == "hanter-kant":
            w1, w2 = word.split('-')
            t_start = tok["start"]
            t_end = tok["end"]
            dur = (t_end - t_start) / 2
            t1 = {"word": w1, "start": t_start, "end": t_start+dur, "conf": tok["conf"]}
            t2 = {"word": w2, "start": t_start+dur, "end": t_end, "conf": tok["conf"]}
            parsed_tokens.append(t1)
            parsed_tokens.append(t2)
        else:
            parsed_tokens.append(tok)
    tokens = parsed_tokens


    starters = numtok_chain['[']
    num_tokens = []
    translated = []
    in_chain = False
    noun = None
    for idx, tok in enumerate(tokens):
        if not in_chain and tok["word"] in starters:
            # Beginning of a chain of words describing a number
            in_chain = True
            num_tokens = [tok]

        elif in_chain:
            prev = num_tokens[-1]["word"]
            if tok["word"] in numtok_chain[prev]:
                # Follow the chain of words describing a number
                num_tokens.append(tok)
            
            elif tok["word"] in starters:
                # Could be the beginning of a new chain
                # Check for ill-formed numerical sequences
                if ']' not in numtok_chain[prev]:
                    # treat as 2 numerical sequence in that case
                    # rewind and flush the first part
                    i = len(num_tokens)-1
                    while i >= 0 and num_tokens[i]["word"] not in ("ha", "hag"):
                        i -= 1
                    next_num_tokens = num_tokens[i+1:]
                    conj = num_tokens[i]
                    num_tokens = num_tokens[:i]
                    flush_number()
                    translated.append(conj)
                    num_tokens = next_num_tokens + [tok]
                else:
                    flush_number()
                    num_tokens = [tok]
            
            elif  '*' in numtok_chain[prev] and is_noun(tok["word"]) or tok["word"] in ('%',):
                if noun:
                    # There could be an ambiguity if another noun has already been found
                    # ex: "tri kazh ha daou besk"
                    # In that case, flush the first part
                    i = len(num_tokens)-1
                    while i >= 0 and num_tokens[i]["word"] not in ("ha", "hag"):
                        i -= 1
                    next_num_tokens = num_tokens[i+1:]
                    conj = num_tokens[i]
                    num_tokens = num_tokens[:i]
                    flush_number()
                    translated.append(conj)
                    num_tokens = next_num_tokens
                    noun = tok
                elif len(tokens) > idx+1 and tokens[idx+1]["word"] in ('ha', 'hag', 'warn'):
                    noun = tok
                else:
                    # final noun
                    noun = tok
                    flush_number()
                    in_chain = False
            
            else:
                flush_number()
                translated.append(tok)
                in_chain = False

        else:
            translated.append(tok)
    
    if in_chain:
        flush_number()

    return translated