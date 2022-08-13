#!/usr/bin/env python3
import re
import sys


# .setdefault() - use to update values if you don't know if they key exists.

WORD_RE = re.compile(r'\w+')


def demo_setdefault(file):
    index = {}
    with open(file, encoding='utf-8') as fp:
        for line_no, line in enumerate(fp, 1):
            for match in WORD_RE.finditer(line):
                word = match.group()
                column_no = match.start() + 1
                location = (line_no, column_no)
                # Get value for `word` or set it to `[]` and return the reference.
                # We can update/insert default without searching twice.
                index.setdefault(word, []).append(location)

    # display in alphabetical order
    for word in sorted(index, key=str.upper):
        print(word, index[word])
