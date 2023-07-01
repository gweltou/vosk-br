from typing import List, Iterator, Any, Tuple
import re
from .definitions import LETTERS, PUNCTUATION




def strip_punct(word: str) -> str:
    """ strip punctuation left and right of a word """

    while word and word[0] in PUNCTUATION:
        word = word[1:]
    while word and word[-1] in PUNCTUATION:
        word = word[:-1]
    return word



def filter_out(text: str, chars: str) -> str:
    """ Remove characters from a string """

    filtered_text = ""
    for l in text:
        if not l in chars: filtered_text += l
    return filtered_text



def capitalize(word: str) -> str:
    """ Capitalize a single word or the first word of a given sentence """
    # Should we capitalize the whole "C'H" character ? For now we don't.

    # Find first letter
    lowered = word.lower()
    i = 0
    while i < len(lowered) and lowered[i] not in LETTERS: i += 1
    if i >= len(word):
        return word
    
    capitalized = word[:i] + word[i].upper() + word[i+1:]
    return capitalized



_PATTERN_BETWEEN_PARENTHESIS = re.compile(r"\((.+?)\)")

def extract_parenthesis_content(txt: str) -> Tuple[str, str]:
    extracted = []
    remaining = txt
    match = re.search(_PATTERN_BETWEEN_PARENTHESIS, remaining)
    while match:
        extracted.append(match.group(1))
        start, end = match.span()
        remaining = remaining[:start] + remaining[end:]
        match = re.search(_PATTERN_BETWEEN_PARENTHESIS, remaining)
    return remaining, extracted



def pre_process(text: str) -> str:
    text = text.replace('‘', "'")
    text = text.replace('’', "'")
    text = text.replace('ʼ', "'")
    text = text.replace(',', ',')
    text = text.replace('˜', '') # Found instead of non-breakable spaces when parsing Ya! pdfs
    text = text.replace('Š', '') # Found instead of long dashes when parsing Ya! pdfs
    text = text.replace('ñ', 'ñ') # A sneaky n-tilde (found in Ya! webpages)
    text = text.replace('ň', 'ñ')
    text = text.replace('ù', 'ù') # Another sneaky one (found in Ya! webpages)
    return text



def fix_clitic(text: str) -> str:
    """ Do not use ! """
    
    text = text.replace("d' ", "d'")
    # text = text.replace("n' ", "n'")

    text = text.replace("n'eus ", "'n eus ")
    text = text.replace("n'int ", "n' int ")
    text = text.replace("n'eo ", "n' eo ")
    text = text.replace("n'hon ", "n' hon ")
    text = text.replace("n'ez ", "n' ez ")
    text = text.replace("n'em ", "n' em ")
    text = text.replace("n'am ", "n' am ")
    text = text.replace("n'en ", "n' en ")
    text = text.replace("n'o ", "n' o ")
    text = text.replace("n'on ", "n' on ")
    text = text.replace("n'he ", "n' he ")
    text = text.replace("n'edo ", "n' edo ")
    text = text.replace("n'emañ ", "n' emañ ")
    text = text.replace("n'anavezan ", "n' anavezan ")
    text = text.replace("n'ouzer ", "n' ouzer ")
    text = text.replace("n'ouzon ", "n' ouzon ")
    # n'oc'h
    # n'omp



def sentence_stats(sentence: str) -> dict:
    """ Get statistics about a string """
    
    letter = 0
    decimal = 0
    upper = 0
    punct = 0
    blank = 0
    other = 0
    
    for c in sentence:
        if c.lower() in LETTERS or c in "'-":
            letter += 1
            if c.isupper():
                upper += 1
        elif c.isdecimal():
            decimal += 1
        elif c.isspace():
            blank += 1
        elif c in PUNCTUATION:
            punct += 1
        else:
            other += 1
        
        sentence = filter_out(sentence, PUNCTUATION)
    
    return {"letter": letter, "decimal": decimal, "upper": upper, "punct": punct,
            "blank": blank, "other": other, "words": len(sentence.split())}