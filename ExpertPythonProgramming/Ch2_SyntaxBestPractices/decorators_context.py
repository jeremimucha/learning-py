#! usr/bin/env python3

'''
decorators can be used to provide a `context` for function execution - essentially to emulate
RAII and run some code before the function execution and after - e.g. to ensure that a mutex
is locked at scope entry and unlocked at exit
'''

from threading import RLock
lock = RLock()

def synchronized(function):
    def _synchronized(*args, **kw):
        lock.acquire()
        try:
            return function(*args, **kw)
        finally:
            lock.release()
    return _synchronized

@synchronized
def thread_safe():      # make sure the function acquires the resource
    pass

# Context decorators are more often replaced by using context managers - the `with` statement
