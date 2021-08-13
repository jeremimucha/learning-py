#! /usr/bin/env python

import asyncio
import inspect

# ------------------------------------------------------------------------------------------------
# Functions defined with `async def` are function, or more precisely "coroutine functions",
# and not coroutines themselves. The `async def` function (i.e. coroutine function) returns
# a coroutine.

async def f():
    return 123


print(f"type(f): {type(f)}")
print(f"inspect.iscoroutinefunction(f): {inspect.iscoroutinefunction(f)}")

coro = f()
print(f"type(f()): {type(coro)}")
print(f"inspect.iscoroutinefunction(f()): {inspect.iscoroutinefunction(coro)}")
print(f"inspect.iscoroutine(f()): {inspect.iscoroutine(coro)}")
# ------------------------------------------------------------------------------------------------


# Manually driving the coroutine
# ------------------------------------------------------------------------------------------------
# coroutines are really just generators - internally `await` is no different than `yield from`.
# A coro is initiated by sending it a None value. This will cause the code to advance until the
# first await / yield from statement or return statement.
# Reaching `return` results in a StopIteration exception being thrown with a `value` attribute
# carrying the return value.
print("\nManually driving the coroutine:")
try:
    coro.send(None)
except StopIteration as e:
    print("The result was:", e.value)

async def foo():
    await asyncio.sleep(1.0)
    return 321

async def main():
    result = await foo()
    return result

result = asyncio.run(main())
print("Main result: ", result)
# ------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------
# It is also possible to feed a coroutine an exception:
# ------------------------------------------------------------------------------------------------
try:
    coro = foo()
    coro.throw(Exception, 'foobar') # sends the exception at the await point.
except Exception as e:
    print(e)

# This is used internally by asyncio for task cancellation.
async def bar():
    try:
        while True: await asyncio.sleep(0)
    except asyncio.CancelledError:
        print("I was cancelled!")
    else:
        return 111

coro = bar()
coro.send(None)
coro.send(None)
coro.throw(asyncio.CancelledError) # This is what the event loop does to cancel the task.

# This results in the coroutine printing the "I was cancelled!" message and ending operation
# with the usual StopIteration!
#
# I was cancelled!
# Traceback (most recent call last):
#   File "...\async_functions.py", line 64, in <module>
#     coro.throw(asyncio.CancelledError)
# StopIteration
