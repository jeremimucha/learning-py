import functools
import time
from typing import Callable, Any


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        # A coroutine that when awaited starts timing the execution of the coroutine it wraps.
        async def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with args{args} {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'finished {func} in {total:.4f} seconds(s)')
        
        return wrapped
    return wrapper
