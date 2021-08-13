#! /usr/bin/env python

import asyncio

# Async comprehensions are also supported.
# This includes using the following within list/dict/set/generator comprehensions:
# - `async for`
# - `await`



# ------------------------------------------------------------------------------------------------
# async for
# ------------------------------------------------------------------------------------------------

# async generator function
async def doubler(n):
    for i in range(n):
        yield i, i * 2
        await asyncio.sleep(0.1)


async def async_for_main():
    # list comp
    result = [x async for x in doubler(3)]
    print(result)
    # dict comp
    result = {x: y async for x, y in doubler(3)}
    print(result)
    # set comp
    result = {x async for x in doubler(3)}
    print(result)
# ------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------
# await
# ------------------------------------------------------------------------------------------------

async def f(x):
    await asyncio.sleep(0.1)
    return x + 100

async def factory(n):
    for x in range(n):
        await asyncio.sleep(0.1)
        # yield a tuple of the coro-function defined above and the value to apply it to
        yield f, x

async def await_main():
    # apply the coro to each value returned by the factory (async generator function)
    results = [await f(x) async for f, x in factory(3)]
    print(results)

# ------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    print("comprehension async for example:")
    asyncio.run(async_for_main())
    # output:
    # [(0, 0), (1, 2), (2, 4)]
    # {0: 0, 1: 2, 2: 4}
    # {(2, 4), (1, 2), (0, 0)}

    print("\ncomprehension await")
    asyncio.run(await_main())
    # output:
    # [100, 101, 102]
