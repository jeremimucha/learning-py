#!/usr/bin/env python3

from collections.abc import Generator   # Generator is used to type-annotate a classic-coroutine

# This function returns a generator that yields float values,
# accepts float values via .send() and does not return a useful value.
def averager() -> Generator[float,      float,      None]:
#                           YieldType,  SendType,   ReturnType
    total = 0.0
    count = 0
    average = 0.0
    # Infinite loop - generator will yield values, as long as
    # client code sends values:
    while True:
        # yield statement here suspends the coroutine,
        # yields a result to the client, and - later - gets a value sent by the caller
        # to the coroutine, starting another iteration
        term = yield average
        total += term
        count += 1
        average = total/count


if __name__ == '__main__':
    coro_avg = averager()
    # Prime the coroutine first, by calling `next()`
    print(next(coro_avg))
    print(coro_avg.send(10))
    print(coro_avg.send(30))
    print(coro_avg.send(5))
    # Explicit termination of a classic coroutine:
    # .close() raises `GeneratorExit` at the suspended `yield`,
    # if not handled in the coroutine function, the exception terminates it.
    # `GeneratorExit` is caught by the generator object that wraps the coroutine.
    coro_avg.close()
    # Multiple .close() calls have no effect.
    coro_avg.close()
    # Attempting to .send() again results in `StopIteration` being raised.
    coro_avg.send(5)
