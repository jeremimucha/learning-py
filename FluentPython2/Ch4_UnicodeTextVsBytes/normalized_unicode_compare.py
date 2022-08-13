#!/usr/bin/env python3

"""
Utility function for normalized Unicode string comparison.
"""

from unicodedata import normalize, combining
import string


def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)


def fold_equal(str1, str2):
    return (normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold)


def shave_marks(txt):
    """Remove all diacritic marks.
    1. Decompose all characters into base characters and combining marks,
    2. Filter out all conbining marks,
    3. Recompose all characters,
    """
    norm_txt = normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt
                     if not combining(c))
    return normalize('NFC', shaved)


def shave_marks_latin(txt):
    """Remove all diacritic marks from Latin base characters"""
    norm_txt = normalize('NFD', txt)
    latin_base = False
    preserve = []
    for c in norm_txt:
        if combining(c) and latin_base:
            continue    # ignore diacritic on Latin base char
        preserve.append(c)
        # if it isn't a combining char, it's a new base char
        if not combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(preserve)
    return normalize('NFC', shaved)


# Transform some western typographical symbols into ASCII
single_map = str.maketrans("""‚ƒ„ˆ‹‘’“”•–—˜›""",
                           """'f"^<''""---~>""")

multi_map = str.maketrans({
    '€': 'EUR',
    '…': '...',
    'Æ': 'AE',
    'æ': 'ae',
    'Œ': 'OE',
    'œ': 'oe',
    '™': '(TM)',
    '‰': '<per mille>',
    '†': '**',
    '‡': '***',
})
multi_map.update(single_map)

def dewinize(txt):
    """Replace Win1252 symbols with ASCII chars or sequences"""
    return txt.translate(multi_map)

def asciize(txt):
    no_marks = shave_marks_latin(dewinize(txt))
    no_marks = no_marks.replace('ß', 'ss')
    return normalize('NFKC', no_marks)
