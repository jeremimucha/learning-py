#!/usr/bin/env python3

"""
procs.py: shows that multiprocessing on a multicore machine
can be faster than sequential code for CPU-intensive work.
"""

# tag::PRIMES_PROC_TOP[]
import sys
from time import perf_counter
from typing import NamedTuple
# SimpleQueue is bound to a predefined instance of a lower-level BaseContext class
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues  # Has a SimpleQueue type hint

from primes import is_prime, NUMBERS

# This time we also include the number checked for primality with the result - simplifies the code later
class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int]  # Type alias for the queue used by main() to send numbers to processes.
ResultQueue = queues.SimpleQueue[PrimeResult]  # Type alias for the queu used to collect results in main.

# Basically the same code as in sequential.py, aside for the result type
def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

# Worker routine - gets a JobQueue and runs, calculating the results
# until there are jobs available, putting results on the results queue.
def worker(jobs: JobQueue, results: ResultQueue) -> None:  # <7>
    while n := jobs.get():  # number `0` will terminate the loop (sentinel value)
        results.put(check(n))  # invokes primality check and enqueues the result
    results.put(PrimeResult(0, False, 0.0))  # Sends back result for `0` as indication that this worker is done.

def start_jobs(
    procs: int, jobs: JobQueue, results: ResultQueue  # procs == number of processes computing results
) -> None:
    for n in NUMBERS:
        jobs.put(n)  # enqueue the numbers to check
    for _ in range(procs):
        # Fork a child process for each worker
        proc = Process(target=worker, args=(jobs, results))
        proc.start()  # Start the process
        jobs.put(0)  # enqueue `0` sentinel value that will terminate the process.
# end::PRIMES_PROC_TOP[]

# tag::PRIMES_PROC_MAIN[]
def main() -> None:
    # Get numer of processes from command line or default to number of cores
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)  # start the processes computing results
    checked = report(procs, results)  # continuously report work done by processes
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')  # display totals

def report(procs: int, results: ResultQueue) -> int: # (number_processes, results_queue)
    checked = 0
    procs_done = 0
    while procs_done < procs:  # loop until proceses are done - indicated by the number of returned `0`s
        n, prime, elapsed = results.get()  # .get() blocks until there is a result
        if n == 0:  # If `0` than process exited
            procs_done += 1
        else:
            checked += 1  # otherwise increment count of checked numbers
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')
    return checked

if __name__ == '__main__':
    main()
# end::PRIMES_PROC_MAIN[]
