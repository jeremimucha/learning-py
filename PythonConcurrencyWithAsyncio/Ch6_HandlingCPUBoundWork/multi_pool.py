#!/usr/bin/env python3

from multiprocessing import Pool


def say_hello(name: str) -> str:
    return f'Hi there, {name}'


if __name__ == '__main__':
    # By default Pool() will create number of processes equal to the number of cores on the machine.
    with Pool() as process_pool:
        # The .apply() call blocks until a result is returned!
        hi_jeff = process_pool.apply(say_hello, args=('Jeff',))
        hi_john = process_pool.apply(say_hello, args=('John',))
        print(hi_jeff)
        print(hi_john)

        # Instead we can use .apply_async() which returns immediately, and starts the process in the background.
        # We get retrieve the result using .get()

        hi_jeff = process_pool.apply_async(say_hello, args=('Jeff',))
        hi_john = process_pool.apply_async(say_hello, args=('John',))
        print(hi_jeff.get())
        print(hi_john.get())
