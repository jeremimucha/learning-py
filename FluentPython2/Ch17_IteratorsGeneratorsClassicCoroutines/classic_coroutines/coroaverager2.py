#!/usr/bin/env python3

from collections.abc import Generator
from typing import Union, NamedTuple


class Result(NamedTuple):
    count: int      # type: ignore
    average: float

class Sentinel:
    def __repr__(self) -> str:
        return f'<Sentinel>'

STOP = Sentinel()

SendType = Union[float, Sentinel]


def averager(verbose: bool = False) -> Generator[None, SendType, Result]:
    total = 0.0
    count = 0.0
    average = 0.0
    while True:
        # This coroutine doesn't yield data, it only receives it via the .send() channel.
        # Such usage of yield only makes sense for coroutines that consume data.
        term = yield
        if verbose:
            print('received: ', term)
        # If we get an instance of the `Sentinel` class we stop accumulating
        if isinstance(term, Sentinel):
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


def compute():
    # `yield from` handles the `StopIteration` thrown by returning from the delegated-to coroutine.
    res = yield from averager(True)
    print('computed: ', res)
    # Returning the value from this coroutine results in another `StopIteration` being raised.
    return res


if __name__ == '__main__':
    coro_avg = averager(True)
    # It's necessary to prime the coroutine first
    print(next(coro_avg))
    coro_avg.send(10)
    coro_avg.send(30)
    coro_avg.send(5)

    # Explicit termination:
    # for this coroutine .close() will not actually return enything,
    # since GeneratorExit will raise at the point of the yield expression,
    # so the return is never reached
    # coro_avg.close()

    # Instead use the designed-in termination channel - pass in a Sentinel instance.
    # `return` in a coroutine results in `StopIteration` being raised, with the
    # return value being assigned to the `.value` member of the `StopIteration` instance.
    # We can get the value explicitly:
    try:
        coro_avg.send(STOP)
    except StopIteration as exc:
        result = exc.value

    print(result)

    # Alternatively a delegating generator could get the result value directly,
    # by using the `yield from` syntax - see `compute()` above.
    comp = compute()
    # Sending `None` as the first value primes the coroutine,
    # equivalent to calling next().
    for v in [None, 10, 20, 30, STOP]:
        try:
            comp.send(v)
        except StopIteration as exc:
            result = exc.value
    
    print(result)
