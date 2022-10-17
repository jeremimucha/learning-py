#!/usr/bin/env python3

import asyncio


async def coro_add_one(number: int) -> int:
    return number + 1


def add_one(number: int) -> int:
    return number + 1


def drive_coro(coro):
    v = None
    try:
        coro.send(None)
    # Values "returned" from a coroutine are carried by the StopIteration exception
    # raised when the return statement in a coroutine is reached.
    # the return value is assigned to the `value` member of the exception.
    except StopIteration as e:
        v = e.value
    return v


if __name__ == '__main__':
    fn_result = add_one(1)
    coro_result = coro_add_one(1)

    print(f"Function result is {fn_result} and the type is {type(fn_result)}")
    print(f"Coroutine result is {coro_result} and the type is {type(coro_result)}")

    actual_coro_result = asyncio.run(coro_result)
    print(f"Actual coroutine result is {actual_coro_result} and the type is {type(actual_coro_result)}")

    # We could run the coroutines manually:
    driven1 = drive_coro(coro_add_one(1))
    driven2 = drive_coro(coro_add_one(42))
    print(f"Manually driven coro result: {driven1}, type: {type(driven1)}")
