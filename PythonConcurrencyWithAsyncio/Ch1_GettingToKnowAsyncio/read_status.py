#!/usr/bin/env python3

import time
from typing import Callable
import threading
import requests


def read_example() -> None:
    response = requests.get('https://www.example.com')
    print(response.status_code)


def timed_call(callable: Callable, repeat: int = 1) -> float:
    start = time.time()
    for _ in range(repeat):
        callable()
    end = time.time()
    return end - start


def threaded_call() -> float:
    thread1 = threading.Thread(target=read_example)
    thread2 = threading.Thread(target=read_example)

    start = time.time()
    thread1.start()
    thread2.start()

    print("All threads running!")

    thread1.join()
    thread2.join()
    
    end = time.time()
    return end - start


if __name__ == '__main__':
    sync_time = timed_call(read_example, repeat=2)
    print(f'Running synchronously took {sync_time:.4f} seconds')

    threaded_time = threaded_call()
    print(f'Running with threads took {threaded_time:.4f} seconds')
