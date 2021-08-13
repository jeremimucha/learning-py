#! /usr/bin/env python

import asyncio
import re

# Async iterators need to be defined when non-blocking iteration is desired.
# They're used with `async for`.

RE_WORD = re.compile(r"\w+")


# ------------------------------------------------------------------------------------------------
# Example of explicitly defining the async-iterator protocol.
# This requires defining __aiter__ as a regular function - which returns an async iterator instance,
# and an iterator class, which defined async __anext__ - coroutine which does the acutal iteration.

class Sentence:

    def __init__(self, text):
        self.text = text

    # Enables async-iteration
    # - note that this is defined using regular `def`, not `async-def`,
    # as it's just a factory method that produces the async-iterator.
    def __aiter__(self):
        return SentenceIterator(self.text)


# The async-iterator class itself.
class SentenceIterator:

    def __init__(self, text):
        self.matches = RE_WORD.finditer(text)

    # Standard practice - an iterator is iterable
    def __aiter__(self):
        return self

    # async-defining __anext__ enables non-blocking iteration,
    # this is a coroutine.
    async def __anext__(self):
        try:
            match = next(self.matches)
        except StopIteration:
            # Async-iterators throw StopAsyncIteration on sequence-end.
            raise StopAsyncIteration
        else:
            await asyncio.sleep(0.5)    # simulate long running computation
            return match.group()


async def do_longrunning_computation(word):
    await asyncio.sleep(0.1)
    print(word)


async def main():
    words = Sentence("This is an example sentence.")
    # Do an asynchronous operation, while performing asynchronous iteration...
    async for value in words:
        await do_longrunning_computation(value)
# ------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------
# Using generators instead of explicitly defining the iterator class.
#
# Much like with regular iterators it's possible to use generators,
# instead of explicitly defining an iterator, to greatly simplyfy
# the process of defining the iteration.

class AnotherSentence:

    def __init__(self, text):
        self.text = text

    # Enables async-iteration
    # uses an async generator expression, to avoid explicitly defining an iterator class
    # This time we use `async def` to make the method an async generator function
    async def __aiter__(self):
        for match in RE_WORD.finditer(self.text):
            await asyncio.sleep(0.5) # simulate long running computation
            yield match.group()


async def main_2():
    words = AnotherSentence("A different example sentence.")
    async for value in words:
        await do_longrunning_computation(value)
# ------------------------------------------------------------------------------------------------

        
if __name__ == '__main__':
    print("Performing async-iteration:")
    asyncio.run(main())

    print("\nSame thing using an async generator function:")
    asyncio.run(main_2())
