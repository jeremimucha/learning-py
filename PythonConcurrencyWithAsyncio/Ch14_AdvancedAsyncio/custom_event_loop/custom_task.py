#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio

from Ch14_AdvancedAsyncio.custom_event_loop.custom_future import CustomFuture

# Tasks are a combination of a future and a coroutine.
# A task's future is complete when the coroutine it wraps finishes.
# We can wrap a coroutine ina future by subclassing our CustomFuture.


class CustomTask(CustomFuture):

    def __init__(self, coro, loop):
        super(CustomTask, self).__init__()
        self._coro = coro
        self._loop = loop
        self._current_result = None
        self._task_state = None
        # Register teh task with the event loop
        loop.register_task(self)

    # Run one step of the coroutines
    def step(self):
        try:
            if self._task_state is None:
                self._task_state = self._coro.send(None)
            # If the coroutine yields a future, add a done callback
            if isinstance(self._task_state, CustomFuture):
                self._task_state.add_done_callback(self._future_done)
        except StopIteration as si:
            self.set_result(si.value)

    def _future_done(self, result):
        try:
            self._task_state = self._coro.send(self._current_result)
        except StopIteration as si:
            self.set_result(si.value)



if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
