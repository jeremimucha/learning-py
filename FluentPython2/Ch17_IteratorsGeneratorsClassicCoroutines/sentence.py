#!/usr/bin/env python3


# Iterator protocol - `iter()` built-in function operates as follows:
# 1. Checks whether the object implements `__iter__`, and calls that to obtain an iterator,
# 2. Else if `__getitem__` is implemented, `iter()` creates an iterator that fetches elements
#    by index, starting at 0.
# 3. Else python raises TypeError - "'<some-class>' object is not iterable"


import re
import reprlib

RE_WORD = re.compile(r'\w+')



# 1. Iterable Sentence relying on the fallback to `__getitem__`


class Sentence1:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.wrods)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)



# 2. Classic iterator design:
# - Iterable implements the `__iter__` method, and returns an Iterator.
# - Iterator implements `__next__` returning items from the sequence and `__iter__` returning self.

class Sentence2:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    
    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        return Sentence2Iterator(self.words)


class Sentence2Iterator:

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self


# 3. Iterable and iterator implementation using a generator.
# This is the most idiomatic version.

class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'

    # This is a generator function/method, returning a generator object,
    # which is an iterable. There's no need for implementing a separate
    # iterator class now, and all the related bookeeping is done for us.
    def __iter__(self):
        # for word in self.words:
        #     yield word

        # or
        yield from self.words



# 4. Lazy iteration - avoid building the entire sequence eagerly,
# instead iterate over the values as needed.

class SentenceLazy:

    def __init__(self, text):
        self.text = text

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'
    
    def __iter__(self):
        # for match in RE_WORD.finditer(self.text):
        #     yield match.group()

        # or - generator expression
        # return (match.group() for match in RE_WORD.finditer(self.text))

        # or - yield from
        yield from RE_WORD.finditer(self.text)


if __name__ == '__main__':
    pass
