#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from threading import Lock, RLock
from typing import List


class IntListThreadsafe:

    def __init__(self, wrapped_list: List[int]):
        # We need a recursive lock here, since both methods acquire the lock,
        # and a normal Lock() is not reentrant (trying to acquire while alredy holding is a deadlock).
        self._lock = RLock()
        self._inner_list = wrapped_list

    def indices_of(self, to_find: int) -> List[int]:
        with self._lock:
            enumerator = enumerate(self._inner_list)
            return [index for index, value in enumerator if value == to_find]

    def find_and_replace(self, to_replace: int, replace_with: int) -> None:
        with self._lock:
            indices = self.indices_of(to_replace)
            for index in indices:
                self._inner_list[index] = replace_with


def main():
    threadsafe_list = IntListThreadsafe([1, 2, 1, 2, 1])
    threadsafe_list.find_and_replace(1, 2)
    print(threadsafe_list._inner_list)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
