#!/usr/bin/env python3


from time import sleep, strftime
from concurrent import futures


def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done'
    display(msg.format('\t'*n, n))
    return n * 10


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, range(5))
    display('results:', results)    # `results` is a generator - see output
    display('Waiting for individual results:')
    # enumerate(results) will implicitly call `next(results)`, iterating over the generator,
    # which in turn will invoke `.result()` on the internal future representing each
    # call to `loiter(n)`. The `.result()` method will block until the future is done,
    # therefore each iteration in this loop will have to wait for the next result to be ready.
    for i, result in enumerate(results):
        display(f'result {i}: {result}')


if __name__ == '__main__':
    main()
