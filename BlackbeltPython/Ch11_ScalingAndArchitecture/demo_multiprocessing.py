#! /usr/bin/env python

from multiprocessing.spawn import freeze_support
import random
import multiprocessing


def compute(n):
    return sum([random.randint(1, 100) for i in range(1000000)])


if __name__ == '__main__':
    freeze_support()
    pool = multiprocessing.Pool(processes=8)
    print("Results: %s" % pool.map(compute, range(8)))
