#!/usr/bin/env python3

import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter = counter + 1
    end = time.time()
    print(f'Finished counting to {count_to} in {end - start}')
    return counter


if __name__ == '__main__':
    # Starts number of processes equal to cpu core count.
    with ProcessPoolExecutor() as process_pool:
        numbers = [1, 3, 5, 22, 100000000]
        # Execute a callable with a number of arguments.
        # The order in which the values are returned is deterministic - corresponds to the order passed-in.
        for result in process_pool.map(count, numbers):
            print(result)
