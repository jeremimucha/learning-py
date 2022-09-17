#!/usr/bin/env python3


from concurrent.futures.process import _chain_from_iterable_of_lists


class DemoException(Exception):
    """An exception type for demonstrating coro exception handling"""


def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print("*** DemoException handled. Continuing...")
        else:
            print(f'-> coroutine received: {x!r}')    
    # The following line is unreachable - the only way to exit the
    # infinite loop is to raise an unhandled exception,
    # and that terminates the coroutine immediately - never reaching this line.
    raise RuntimeError('This line should never run.')


def demo_finally():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print("*** DemoException handled. Continuing...")
            else:
                print(f'-> coroutine received: {x!r}')
    finally:
        print('-> coroutine ending')


def coro_driver(coro):
    coro_obj = coro()
    next(coro_obj)
    coro_obj.send(11)
    coro_obj.send(22)
    coro_obj.throw(DemoException)
    coro_obj.send(33)
    coro_obj.close()
    try:
        coro_obj.send(44)
    except StopIteration as e:
        print(f'Coro: {coro_obj} is stopped: {e}')



if __name__ == '__main__':
    for coro in (demo_exc_handling, demo_finally):
        coro_driver(coro)
        print('')
