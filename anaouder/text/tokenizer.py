#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Programming pattern inspired by https://github.com/mideind/Tokenizer
"""


from typing import Iterator, Iterable, List, Any, Union, Set
import re

from .definitions import (
    is_noun, is_noun_f, is_noun_m, is_proper_noun,
    is_time, match_time,
    is_unit_number, match_unit_number,
    PUNCTUATION, LETTERS, SI_UNITS,
    OPENING_QUOTES, CLOSING_QUOTES,
)
from .utils import capitalize
from ..dicts import acronyms, corrected_tokens, standard_tokens



# Regular words

re_word = re.compile(r"['\-·" + LETTERS + r"]+", re.IGNORECASE)
match_word = lambda s: re_word.fullmatch(s)
is_word = lambda s: bool(match_word(s))

# Inclusive words (ex: arvester·ez)
# will always match as regular words
re_word_inclusive = re.compile(r"(['-" + LETTERS + r"]+)·([-" + LETTERS + r"]+)", re.IGNORECASE)
match_word_inclusive = lambda s: re_word_inclusive.fullmatch(s)
is_word_inclusive = lambda s: bool(match_word_inclusive(s))



# Percentage

# re_percent = re.compile(r"(\d+)%")
# match_percent = lambda s: re_percent.fullmatch(s)
# is_percent = lambda s: bool(match_percent(s))


# Ordinals

ORDINALS = {
    "1añ"  : "kentañ",
    "2vet" : "eilvet",
    "3de"  : "trede",
    "3vet" : "teirvet",
    "4e"   : "pevare",
    "4re"  : "pevare",
    "4vet" : "pedervet",
    "9vet" : "navet"
}

re_ordinal = re.compile(r"(\d+)vet")
match_ordinal = lambda s: re_ordinal.fullmatch(s)
is_ordinal = lambda s: s in ORDINALS or bool(match_ordinal(s))


ROMAN_ORDINALS = {
    "Iañ"  : "kentañ",
    "IIvet": "eilvet",
    "IIIde": "trede",
    "IIIe" : "trede",
    "IIIvet": "teirvet",
    "IVe"  : "pevare",
    "IVvet": "pedervet",
    "IXvet": "navet"
}

re_roman_ordinal = re.compile(r"([XVI]+)vet")
match_roman_ordinal = lambda s: re_roman_ordinal.fullmatch(s)
is_roman_ordinal = lambda s: s in ROMAN_ORDINALS or bool(match_roman_ordinal(s))

re_roman_number = re.compile(r"([XVI]+)")
match_roman_number = lambda s: re_roman_number.fullmatch(s)
is_roman_number = lambda s: bool(match_roman_number(s))



class Token:
    # Enum
    RAW = -1
    FIRST_IN_SENTENCE = 0
    END_SENTENCE = 1
    PUNCTUATION = 2
    WORD = 3
    NUMBER = 4
    ROMAN_NUMBER = 5
    NOUN = 6
    PROPER_NOUN = 7
    VERB = 8
    ACRONYM = 9
    ORDINAL = 10
    ROMAN_ORDINAL = 11
    TIME = 12
    UNIT = 13         # %, m, km2, kg...
    QUANTITY = 14     # a number and a unit (%, m, km2, kg, bloaz, den...)
    # PERCENT = 11
    UNKNOWN = 99

    descr = {
        RAW: "RAW",
        FIRST_IN_SENTENCE: "FIRST_IN_SENTENCE",
        END_SENTENCE: "END_SENTENCE",
        WORD: "WORD",
        NUMBER: "NUMBER",
        ROMAN_NUMBER: "ROMAN_NUMBER",
        PUNCTUATION: "PUNCTUATION",
        NOUN: "NOUN",
        PROPER_NOUN: "PROPER_NOUN",
        VERB: "VERB",
        ACRONYM: "ACRONYM",
        ORDINAL: "ORDINAL",
        ROMAN_ORDINAL: "ROMAN_ORDINAL",
        TIME: "TIME",
        UNIT: "UNIT",
        QUANTITY: "QUANTITY",
        # PERCENT: "PERCENT",
        UNKNOWN: "UNKNOWN",
    }

    def __init__(self, data: str, kind: int=RAW, *flags):
        self.data = data
        self.norm = []
        self.kind = kind
        self.flags: Set[Flag] = set(flags)
    
    def __repr__(self):
        return f"Token({repr(self.data)}, {self.descr[self.kind]})"


class Flag:
    FIRST_WORD = 1
    MASCULINE = 2
    FEMININE = 3
    INCLUSIVE = 4
    CAPITALIZED = 5
    CORRECTED = 6



def generate_raw_tokens(text_or_gen: Union[str, Iterable[str]]) -> Iterator[Token]:
    """ Generate raw tokens by splitting strings on whitespaces """
    
    if isinstance(text_or_gen, str):
        if not text_or_gen:
            return
        text_or_gen = [text_or_gen]
    
    for sentence in text_or_gen:
        for s in sentence.split():
            yield Token(s, Token.RAW)



def parse_punctuation(token_stream: Iterator[Token], **options: Any) -> Iterator[Token]:
    """ Parse a stream of raw tokens to find punctuation
    
        TODO:
            * words with a dot in the middle and more than 2 letters
                (ex: [...] fin miz Gouere.Laouen e oa [...])
            * rak,tost

    """

    # Normalize punctuation option
    norm_punct = options.pop('norm_punct', False)

    punct_stack = []

    for tok in token_stream:
        if tok.kind == Token.RAW:
            data = tok.data
            remainder = ""
            while data:
                tokens = []
                if re.search(r"\.\.+", data):
                    match = re.search(r"\.\.+", data)
                    if match.start() == 0:
                        # Ellipsis is at the beginning of the word
                        tokens.append(Token(match.group(), Token.PUNCTUATION))
                        data = data[match.end():]
                    else:
                        # Ellipsis in the middle or end of the word
                        left_part = data[:match.start()]
                        remainder = data[match.start():]
                        data = left_part
                elif data in PUNCTUATION:
                    # A single punctuation
                    tokens.append(Token(data, Token.PUNCTUATION))
                    # All data is consumed
                    data = remainder
                    remainder = ""
                elif re.match(r"([A-Z]\.)+", data):
                    # Single initial or group of initials (i.e: I.E.)
                    match = re.match(r"([A-Z]\.)+", data)
                    tokens.append(Token(data))
                    data = data[match.end():]
                    #data = remainder
                    #remainder = ""
                else:
                    # Parse left punctuation
                    while data and data[0] in PUNCTUATION:
                        tokens.append(Token(data[0], Token.PUNCTUATION))
                        data = data[1:]
                    # Parse right punctuation
                    deferred_tokens = []
                    while data and data[-1] in PUNCTUATION:
                        deferred_tokens.insert(0, Token(data[-1], Token.PUNCTUATION))
                        data = data[:-1]
                    if data:
                        # No more punctuation in word
                        tokens.append(Token(data, tok.kind))
                        # All data is consumed
                        data = remainder
                        remainder = ""
                    if deferred_tokens:
                        tokens.extend(deferred_tokens)

                
                for t in tokens:
                    if t.kind == Token.PUNCTUATION:
                        if norm_punct:
                            if t.data == '‚':   # dirty comma
                                t.norm.append(',')
                            if re.match(r"\.\.+", t.data):
                                t.norm.append('…')
                        
                        if t.data == '"':
                            if punct_stack and punct_stack[-1] == '"':
                                punct_stack.pop()
                            else:
                                # we use a single '"' char to represent every kind of quotation mark
                                # this prevents problems when mixing types of quotation marks
                                punct_stack.append('"')
                        elif t.data in OPENING_QUOTES:
                            punct_stack.append('"')
                        elif t.data in CLOSING_QUOTES:
                            if punct_stack and punct_stack[-1] == '"':
                                punct_stack.pop()
                        elif t.data == '(':
                            punct_stack.append('(')
                        elif t.data == ')':
                            if punct_stack and punct_stack[-1] == '(':
                                punct_stack.pop()

                    yield t
                    if not punct_stack and t.data in '.?!:;':
                        yield Token('', Token.END_SENTENCE)
        
        else:
            yield tok



def parse_regular_words(token_stream: Iterator[Token], **options: Any) -> Iterator[Token]:
    """ It should be called after `parse_punctuation`
    
        TODO:
            * Brezhoneg/Galleg
            * miz Gouere.Laouen e oa
    """

    # Arg options

    for tok in token_stream:
        if tok.kind == Token.RAW:
            if tok.data in acronyms:
                tok.kind = Token.ACRONYM
            elif is_word(tok.data):
                # Token is a simple and well formed word
                if is_proper_noun(tok.data):
                    tok.kind = Token.PROPER_NOUN
                else:
                    tok.kind = Token.WORD
                    if is_word_inclusive(tok.data):
                        tok.flags.add(Flag.INCLUSIVE)
            yield tok
        else:
            yield tok



def parse_numerals(token_stream: Iterator[Token]) -> Iterator[Token]:
    """ Look for various numeral forms: numbers, ordinals, units...
        It should be applied before `parse_regular_words` to accurately parse quantities

        TODO:
            * 1,20
            * €/miz
            * +40 %
            * d'ar Sul 10/10
            * ½
            * 02.98.00.00.00
            * 2003-2004
    """

    # prev_token = None
    num_concat = "" # buffer to contatenate numeral forms such as '12 000' -> '12000'
    for tok in token_stream:
        if tok.kind == Token.RAW:
            if tok.data.isdecimal():
                if not num_concat and len(tok.data) < 4:
                    num_concat += tok.data
                elif num_concat and len(tok.data) == 3:
                    num_concat += tok.data                    
                else:
                    # An full number
                    tok.kind = Token.NUMBER
            elif re.fullmatch(r"\d{1,3}(\.\d\d\d)+", tok.data):
                # A big number with dotted thousands (i.e: 12.000.000)
                tok.data = tok.data.replace('.', '')
                tok.kind = Token.NUMBER
            else:
                if is_roman_number(tok.data):
                    tok.kind = Token.ROMAN_NUMBER
                elif is_ordinal(tok.data):
                    tok.kind = Token.ORDINAL
                elif is_roman_ordinal(tok.data):
                    tok.kind = Token.ROMAN_ORDINAL
                elif is_time(tok.data):
                    # TODO: Check for token 'gm', 'g.m', 'GM'...
                    tok.kind = Token.TIME
                elif is_unit_number(tok.data):
                    # ex: "10m2"
                    number, unit = match_unit_number(tok.data).groups()
                    number = number.replace('.', '')
                    tok.kind = Token.QUANTITY
                    tok.data = f"{num_concat}{number}{unit}"
                    tok.number = num_concat + number
                    tok.unit = unit
                    if num_concat:
                        num_concat = ""
                elif tok.data in SI_UNITS:
                    if num_concat:
                        # ex: "10 s"
                        tok.kind = Token.QUANTITY
                        tok.number = num_concat
                        tok.unit = tok.data
                        tok.data = num_concat + tok.data
                        num_concat = ""
                    elif tok.data not in ('l', 'm', 't', 'g'):
                        tok.kind = Token.UNIT
                elif num_concat and is_noun(tok.data):
                    # ex: "32 bloaz"
                    tok.kind = Token.QUANTITY
                    tok.number = num_concat
                    tok.unit = tok.data
                    if is_word_inclusive(tok.data):
                        tok.flags.add(Flag.INCLUSIVE)
                    else:
                        if is_noun_f(tok.data):
                            tok.flags.add(Flag.FEMININE)
                        if is_noun_m(tok.data):
                            tok.flags.add(Flag.MASCULINE)
                    tok.data = f"{num_concat} {tok.data}"
                    num_concat = ""
                
                if num_concat:
                    yield Token(num_concat, Token.NUMBER)
                    num_concat = ""
        else:
            if num_concat:
                yield Token(num_concat, Token.NUMBER)
                num_concat = ""

        if not num_concat:
            yield tok
    
    if num_concat:
        yield(Token(num_concat, Token.NUMBER))



def correct_tokens(token_stream: Iterator[Token]) -> Iterator[Token]:
    """ Should be applied before `parse_regular_words` """

    def get_susbitution(word: str) -> List[str]:
        lowered = word.lower()
        
        if lowered in corrected_tokens:
            substitutes = corrected_tokens[lowered]
        elif lowered in standard_tokens:
            substitutes = standard_tokens[lowered]
        else:
            return []
        
        # Keep capitalization
        i = 0
        while lowered[i] not in LETTERS: i += 1
        if word[i].isupper():
            first = capitalize(substitutes[0])
            return [first] + substitutes[1:]
        else:
            return substitutes

        


    for tok in token_stream:
        if tok.kind == Token.RAW:
            lowered = tok.data.lower()
            substitutes = get_susbitution(tok.data)
            if substitutes:
                # We must keep the prepended apostrophe (there could be a substitution rule for it)
                yield from [ Token(s, Token.RAW, Flag.CORRECTED) for s in substitutes ]
            elif lowered.startswith("'") and lowered[1:] not in ('n', 'm', 'z'):
                # Remove prepended apostrophies
                # Check if there is a susbstitution rule for the remaining word
                substitutes = get_susbitution(tok.data[1:])
                if substitutes:
                    yield from [ Token(s, Token.RAW, Flag.CORRECTED) for s in substitutes ]
                else:
                    # Pass the word without the apostrophe
                    tok.data = tok.data[1:]
                    yield tok
            else:
                yield tok
        else:
            yield tok



def tokenize(text_or_gen: Union[str, Iterable[str]], **options: Any) -> Iterator[Token]:
    """
        TODO:
            * &
    """

    # Arg options
    autocorrect = options.pop('autocorrect', False)
    #standardize = options.pop('standardize', False)
    
    token_stream = generate_raw_tokens(text_or_gen)
    token_stream = parse_punctuation(token_stream, **options)
    if autocorrect:
        token_stream = correct_tokens(token_stream)
    token_stream = parse_numerals(token_stream)
    token_stream = parse_regular_words(token_stream, **options)
    # token_stream = parse_acronyms(token_stream)

    return token_stream



def detokenize(token_stream: Iterator[Token], **options: Any) -> str:
    
    # Parse options
    end_sentence = options.pop('end', '')
    # colored = options.pop("colored", False)

    parts: List[str] = []
    punct_stack = [] # Used to keep track of coupled punctuation (quotes and brackets)

    for tok in token_stream:
        data = tok.norm[0] if tok.norm else tok.data

        prefix = ''
        if tok.kind == Token.PUNCTUATION:
            if data in '!?:;':
                prefix = '\xa0' # Non-breakable space
            elif data == '"':
                if punct_stack and punct_stack[-1] == '"':
                    punct_stack.pop()
                    prefix = ''
                else:
                    punct_stack.append('"')
                    prefix = ' '
            elif data in OPENING_QUOTES:
                # we use a single '"' char to represent every kind of quotation mark
                # this prevents problems when mixing types of quotation marks
                punct_stack.append('"')
                prefix = ' '
            elif data in CLOSING_QUOTES:
                if punct_stack and punct_stack[-1] == '"':
                    punct_stack.pop()
                prefix = '\xa0' if data == '»' else ''
            elif data in '([':
                punct_stack.append(data)
                prefix = ' '
            elif data in ')':
                if punct_stack and punct_stack[-1] == '(':
                    punct_stack.pop()
                prefix = ''
            elif data in ']':
                if punct_stack and punct_stack[-1] == '[':
                    punct_stack.pop()
                prefix = ''
            elif data == '/…':
                prefix = ''
        
        elif tok.kind == Token.END_SENTENCE:
            prefix = end_sentence

        elif parts and parts[-1]:
            last_char = parts[-1][-1]
            if last_char == '«':
                prefix = '\xa0'
            elif punct_stack and last_char == punct_stack[-1]:
                prefix = ''
            elif punct_stack and last_char == '“':
                prefix = ''
            elif last_char not in '-/':
                prefix = ' '

        if parts:
            parts.append(prefix + data)
        else:
            # First word in sentence
            parts.append(data if data else '')
        if parts[-1] == '':
            parts.pop()
    
    if parts:
        ret = ''.join(parts)
        return ret
    return ''



def split_sentences(text_or_gen: Union[str, Iterable[str]], **options: Any) -> Iterator[str]:
    """ Split a line (or list of lines) according to its punctuation
        This function can be used independently

        Options:
            'end' : end the sentences with the given character 

    """

    end_sentence = options.pop("end", '\n')
    # preserve_newline = options.pop("preserve_newline", False)

    if isinstance(text_or_gen, str):
        if not text_or_gen:
            return
        text_or_gen = [text_or_gen]
    
    token_stream = generate_raw_tokens(text_or_gen)
    token_stream = parse_punctuation(token_stream)

    current_sentence = []
    for tok in token_stream:
        if tok.kind == Token.END_SENTENCE:
            yield detokenize(current_sentence, **options) + end_sentence
            current_sentence = []
        else:
            current_sentence.append(tok)
    if current_sentence:
        yield detokenize(current_sentence, **options) + end_sentence
