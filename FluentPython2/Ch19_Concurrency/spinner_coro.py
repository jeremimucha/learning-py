#!/usr/bin/env python3


# Main ways of running a coroutine:
# * asyncio.run(coro())
#   Called from a regular function to drive a coroutine object that usually
#   is the entry point for all the asynchronous code in the program.
#   Blocks until the body of `coro()` returns, the value of `run()` is
#   whatever `coro()` returns.
#
# * asyncio.create_task(coro())
#   Called from a coroutine to schedule another coroutine to execute eventually.
#   This call does not suspend the current coroutine. It returns a `asynchio.Task`
#   instance, an object that wraps the coroutine object and provides methods
#   control and query its state.
#
# * await coro()
#   Called from a coroutine to transfer control to the coroutine object returned by coro().
#   This suspend the current coroutine until the body of `coro()` returns.
#   The value of the `await` is whatever teh body of `coro()` returns.


import asyncio
import itertools
import time


def main() -> None:
    # asyncio.run starts the event loop to drive the coroutine,
    # that will set the other coroutines in motion.
    # main() is blocked until the given coroutine returns.
    result = asyncio.run(supervisor())
    print(f'Answer: {result}')


# Native coroutines are defined with `async def`
async def supervisor() -> int:
    # `asyncio.create_task` schedules execution of another coroutine.
    # It returns an `asyncio.Task`
    spinner = asyncio.create_task(spin('thinking'))
    print(f"Spinner asyncio.Task object: {spinner}")
    result = await slow() # blocks supervisor() until slow() returns
    spinner.cancel() # Raises `CancelledError` exception inside the spin() coro.
    return result


# We don't need the `Event` argument with coroutines - they're cooperative by design.
async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            # We need to use `await asyncio.sleep()` instead of `time.sleep()` to pause
            # without blocking other coroutines.
            await asyncio.sleep(.1)
        # raised after `.cancel()` method is called on the `Task` controlling this coro
        except asyncio.CancelledError:
            break

    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


async def slow() -> int:
    # Also uses `asyncio.sleep()` to avoid blocking other coroutines.
    await asyncio.sleep(3)
    # If we use `time.sleep()` the call to this coroutine would block until `time.sleep()` returns,
    # halting the entire coroutine loop for the time.
    # time.sleep(3)
    return 42

if __name__ == '__main__':
    main()
