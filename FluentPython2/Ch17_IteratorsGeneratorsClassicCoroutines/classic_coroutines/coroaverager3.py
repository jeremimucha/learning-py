#!/usr/bin/env python3



# Behavior of `yield from` and subgenerators:
# * Any values that the subgenerator yields are passed directly to the caller of the delegating generator
#   (i.e., the client code).
# * Any values sent to the delegating generator using send() are passed directly to the subgenerator.
#   If the sent value is None, the subgenerator’s next() method is called. If the sent value is not None,
#   the subgenerator’s send() method is called. If the call raises StopIteration, the delegating generator is resumed.
#   Any other exception is propagated to the delegating generator.
# * `return expr` in a generator (or subgenerator) causes `StopIteration(expr)` to be raised upon exit from the
#    generator.
# * The value of the yield from expression is the first argument to the StopIteration exception raised
#   by the subgenerator when it terminates.


from collections import namedtuple


Result = namedtuple('Result', 'count average')


# the subgenerator
def averager() -> Result[int, float]: #1
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield        # this generator only accepts values
        if term is None:    # None is the cancel-generator sentinel
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)   # This will raise StopIteration(value=Result(count, average))


def grouper(results, key):
    while True:
        # `yield from` yields the control to the `averager()` coroutine,
        # it also handles priming the generator with next() or .send(None),
        # and handles the StopIteration(value=...), by extracting the `.value`
        # and simply returning it - here assigning to `result[key]`.
        # Thanks to this behavior the caller can send values directly
        # to the averager() coroutine, with all of the details of driving
        # the coroutine being handled by `yield from`.
        results[key] = yield from averager()


# the client code, a.k.a the caller
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group) # prime the grouper generator
        for value in values:
            group.send(value)   # send values to the subgenerator
        group.send(None)        # Important - terminate the subgenerator

    report(results)


# output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print(f'{result.count:2} {group:5}', f'averaging {result.average:.2f}{unit}')


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


if __name__ == '__main__':
    main(data)
