import os
import typing


# Proper nouns dictionary
# with phonemes when name has a foreign or particular pronunciations

proper_nouns = dict()
_proper_nouns_phon_path = __file__.replace("__init__.py", "proper_nouns_phon.tsv")

with open(_proper_nouns_phon_path, 'r') as f:
    for l in f.readlines():
        l = l.strip()
        if l.startswith('#') or not l: continue
        w, *pron = l.split(maxsplit=1)
        pron = pron if pron else []
        
        if w in proper_nouns and pron:
            proper_nouns[w].append(pron[0])
        else:
            proper_nouns[w] = pron



# Noun dictionary
# Things that you can count

nouns_f = set()
_nouns_f_path = __file__.replace("__init__.py", "noun_f.tsv")

with open(_nouns_f_path, 'r') as f:
    for l in f.readlines():
        l = l.strip()
        if l.startswith('#') or not l: continue
        nouns_f.add(l)


nouns_m = set()
_nouns_m_path = __file__.replace("__init__.py", "noun_m.tsv")

with open(_nouns_m_path, 'r') as f:
    for l in f.readlines():
        l = l.strip()
        if l.startswith('#') or not l: continue
        nouns_m.add(l)



# Acronyms dictionary

_acronyms_path = __file__.replace("__init__.py", "acronyms.tsv")

def get_acronyms_dict():
    """
        Acronyms are stored in UPPERCASE in dictionary
        Values are lists of strings for all possible pronunciation of an acronym
    """
    acronyms = dict()
    # for l in "BCDFGHIJKLMPQRSTUVWXZ":
    #     acronyms[l] = [acr2f[l]]
    
    if os.path.exists(_acronyms_path):
        with open(_acronyms_path, 'r') as f:
            for l in f.readlines():
                l = l.strip()
                if l.startswith('#') or not l: continue
                acr, pron = l.split(maxsplit=1)
                if acr in acronyms:
                    acronyms[acr].append(pron)
                else:
                    acronyms[acr] = [pron]
    else:
        print("Acronym dictionary not found... creating file")
        open(_acronyms_path, 'a').close()
    return acronyms

acronyms = get_acronyms_dict()



# Common word mistakes

corrected_tokens = dict()
_corrected_tokens_path = __file__.replace("__init__.py", "corrected_tokens.tsv")

with open(_corrected_tokens_path, 'r') as f:
    for l in f.readlines():
        l = l.strip()
        if l.startswith('#') or not l: continue
        k, v = l.split('\t')
        v = v.split()
        corrected_tokens[k] = v


# Standardization tokens

standard_tokens = dict()
_standard_tokens_path = __file__.replace("__init__.py", "standard_tokens.tsv")

with open(_standard_tokens_path, 'r') as f:
    for l in f.readlines():
        l = l.strip()
        if l.startswith('#') or not l: continue
        k, v = l.split('\t')
        v = v.split()
        standard_tokens[k] = v