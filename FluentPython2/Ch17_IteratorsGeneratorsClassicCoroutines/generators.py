#!/usr/bin/env python3


def gen_123():
    print('start')
    yield 1
    print('continue .')
    yield 2
    print('continue ..')
    yield 3
    print('end.')



if __name__ == '__main__':
    print(gen_123)      # <function gen_123 at 0x...>
    g = gen_123()
    print(g)        # <generator object gen_123 at 0x...>

    for i in g:
        print(i)

    g = gen_123()
    print(next(g))  # 1
    print(next(g))  # 2
    print(next(g))  # 3
    print(next(g))  # StopIteration
