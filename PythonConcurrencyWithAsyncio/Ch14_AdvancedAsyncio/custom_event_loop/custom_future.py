#!/usr/bin/env python3

import os
import asyncio


# Awaitables are required to implement the __await__ method, which should return an iterator.
# By the example of the Future - a wrapper around a value that may be there at some point.
# Assuming it's used in an infinite event loop, and we want to check if a future is done
# with an iterator. If the operation is finished, we caj just return the result,
# and the iterator is done. Otherwise, to indicate that "we're not done, check again later",
# we can just yield the iterator itself.


class CustomFuture:

    def __init__(self):
        self._result = None
        self._is_finished = False
        self._done_callback = None

    def result(self):
        return self._result
    
    def is_finished(self):
        return self._is_finished

    def set_result(self, result):
        self._result = result
        self._is_finished = True
        if self._done_callback:
            self._done_callback(result)
    
    def add_done_callback(self, fn):
        self._done_callback = fn
    
    def __await__(self):
        if not self._is_finished:
            yield self
        return self.result()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    future = CustomFuture()

    i = 0
    while True:
        try:
            print('Checking future...')
            gen = future.__await__()
            gen.send(None)
            print('Future is not done...')
            if i == 1:
                print('Setting future value...')
                future.set_result('Finished!')
            i = i + 1
        except StopIteration as si:
            print(f'Value is {si.value}')
            break
