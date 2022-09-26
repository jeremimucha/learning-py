#!/usr/bin/env python3

import asyncio
from domainlib import probe, multi_probe


# Use of `async` and `await` in comprehensions.
# Since python 3.7 it is possible to use the async and await keywords in all
# comprehensions, making them async comprehensions.

 
names = 'python.org rust-lang.org golang.org no-lang.invalid'.split()
# Using `async for` in a generator expression makes it an async generator expression.
# It can be defined anywhere in a python module, but can only be consumed in a coroutine.
gen_found = (name async for name, found in multi_probe(names) if found)
print(gen_found)


async def show_gen_found():
    async for name in gen_found:
        print(name, end=' ')
    print()
    
async def show_list_comp():
    snames = sorted(names)
    found = (name async for name, found in multi_probe(snames) if found)
    # Use an async-for list comprehension
    result = [n async for n in found]
    for name in result:
        print(name, end=' ')
    print()

async def show_await_comp():
    snames = sorted(names)
    # Use `await` in a comprehension:
    result = [await probe(name) for name in snames]
    print(result)
    # The above is similar to using `asyncio.gather()`, however, .gather()
    # gives us more control over exception handling, thanks to its optional
    # `return_exceptions` argument. By default it's `False`, but it's recommended
    # to use `True` for most use cases.
    coros = [probe(name) for name in snames]
    result = await asyncio.gather(*coros, return_exceptions=True)
    print(result)


async def main():
    await show_gen_found()
    await show_list_comp()
    await show_await_comp()


if __name__ == '__main__':
    asyncio.run(main())
