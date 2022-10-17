#!/usr/bin/env python3

import threading
import time


def print_fib(number: int) -> None:
    def fib(n: int) -> int:
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    
    print(f'fib({number}) is {fib(number)}')


def fibs_no_threading():
    print_fib(36)
    print_fib(37)


def fibs_with_threads():
    thread1 = threading.Thread(target=print_fib, args=(36,))
    thread2 = threading.Thread(target=print_fib, args=(37,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == '__main__':
    start = time.time()
    fibs_no_threading()
    end = time.time()
    print(f'Complete in {end - start:.4f} seconds.')

    start_threads = time.time()
    fibs_with_threads()
    end_threads = time.time()
    print(f'Threads took {end_threads - start_threads:.4f} seconds.')

    # The above shows that threading is not the solution to CPU-bound work in python due to the GIL.
