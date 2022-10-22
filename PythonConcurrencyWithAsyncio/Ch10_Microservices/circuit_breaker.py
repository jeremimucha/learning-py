#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from datetime import datetime, timedelta


# The CircuitBreaker pattern can be used to improve response time of the service overall,
# in presence of some slow underlying microservices.
# The Circuit Breaker will allow connections as long as the service operates as expected,
# however, if the service fails repeatedly, or is repeatedly slow to respond, (or whatever
# other criteria we embed in our breaker), the breaker will "open", meaning that it will
# quick-fail all requests. After a set time interval it will reset, attempting to start
# serving requests again.


class CircuitOpenException(Exception):
    pass


class CircuitBreaker:

    def __init__(self,
                 callback,
                 timeout: float,
                 time_window: float,
                 max_failures: int,
                 reset_interval: float):
        self.callback = callback
        self.timeout = timeout
        self.time_window = time_window
        self.max_failures = max_failures
        self.reset_interval = reset_interval
        self.last_request_time = None
        self.last_failure_time = None
        self.current_failures = 0

    # make the request failing fast if we've exceeded the failure count
    async def request(self, *args, **kwargs):
        if self.current_failures >= self.max_failures:
            if datetime.now() > self.last_request_time + timedelta(seconds=self.reset_interval):
                self._reset('Circuit is going from open to closed, resetting!')
                return await self._do_request(*args, **kwargs)
            else:
                print('Circuit is open, failing fast!')
                raise CircuitOpenException()
        else:
            if self.last_failure_time and datetime.now() > \
               self.last_failure_time + timedelta(seconds=self.time_window):
                self._reset('Interval since first failure elapsed, resetting!')
            print('Circuit is closed, requesting!')
            return await self._do_request(*args, **kwargs)

    # Reset out counters and last failure time.
    def _reset(self, msg: str):
        print(msg)
        self.last_failure_time = None
        self.current_failures = 0

    # Make the request, keeping track of how many failures we've had and when they last happened
    async def _do_request(self, *args, **kwargs):
        try:
            print('Making request!')
            self.last_request_time = datetime.now()
            return await asyncio.wait_for(self.callback(*args, **kwargs), timeout=self.timeout)
        except Exception as e:
            self.current_failures += 1
            if self.last_failure_time is None:
                self.last_failure_time = datetime.now()
            raise


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
