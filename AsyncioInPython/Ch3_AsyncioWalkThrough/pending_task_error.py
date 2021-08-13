#! /usr/bin/env python

import asyncio


async def foo(delay):
    await asyncio.sleep(delay)


# Given two tasks, if we fail to take care of proper shutdown,
# the remaining task will result in an error

loop = asyncio.get_event_loop()
# Create two tasks
t1 = loop.create_task(foo(1))
t2 = loop.create_task(foo(2))
# run the loop only until the first task is done
loop.run_until_complete(t1)
# close the loop immediately after the first task completes
loop.close()
# This will result in `t2` error:
# ```
# Task was destroyed but it is pending!
# task: <Task pending name='Task-2' coro=<foo() running at pending_task_error.py:7> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x00000254AED51C40>()]>>
# ```
