#! /usr/bin/env python

import asyncio

# ------------------------------------------------------------------------------------------------
# Future class represents a state of "something" (callable) that is interacting with an event loop.
# It carries information about completion and result of some computation.
# * .set_result(value), .result() -> result value set/get,
# * .cancel(), .cancelled() -> cancellation set/get,
# * callback functions can be registered to be called when the future completes,
# ------------------------------------------------------------------------------------------------

async def main(f: asyncio.Future):
    await asyncio.sleep(1.0)
    f.set_result("I have finished.")
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
# Since python 3.8 it is no longer valid to set_result on a Task (subclass of Future),
# to guard against it we could do the following:

async def main2(f: asyncio.Future):
    await asyncio.sleep(1.0)
    try:
        f.set_result("I have finished.")
    except RuntimeError as e:
        print("No longer allowed: ", e)
        f.cancel()
# ------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    # ------------------------------------------------------------------------------------------------
    # Demonstrate how to use a Future
    # ------------------------------------------------------------------------------------------------
    loop = asyncio.get_event_loop()
    ftr = asyncio.Future()
    print(ftr.done())   # False. By default a future is not done
    loop.create_task(main(ftr))
    loop.run_until_complete(ftr)
    print(ftr.done())
    print(ftr.result())
    # ------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------
    # Demonstate that Tasks can not have their result value set directly
    # ------------------------------------------------------------------------------------------------
    from contextlib import suppress
    print("\nTask demonstration:")
    task = asyncio.Task(asyncio.sleep(1_000_000))
    print(task.done())
    loop.create_task(main2(task))
    with suppress(asyncio.CancelledError):
        loop.run_until_complete(task)
    print("task.done()", task.done())
    print("task.cancelled()", task.cancelled())
    # ------------------------------------------------------------------------------------------------


    # ------------------------------------------------------------------------------------------------
    # Official docs also describe the asyncio.ensure_future() function, which
    # - if given a coroutine wraps the coroutine in a task, registers the task with the event loop
    #   and returns the task (same as asyncio.create_task())
    # - if given a Future object (i.e. also a Task - subclass of Future) does nothing and just
    #   returns the given instance.
    # It is meant for use in framework development, however, some older code may use it
    # where asyncio.create_task would be more suitable.
    # ------------------------------------------------------------------------------------------------
    async def f():
        pass

    coro = f()
    loop = asyncio.get_event_loop()

    # create_task - no surprises
    task = loop.create_task(coro)
    assert isinstance(task, asyncio.Task)

    # ensure_future - given a coro does the same work as create_task
    new_task = asyncio.ensure_future(coro)
    assert isinstance(new_task, asyncio.Task)

    # ensure_future - given a Future/Task just returns it
    passthrough = asyncio.ensure_future(task)
    assert passthrough is task
    # ------------------------------------------------------------------------------------------------
