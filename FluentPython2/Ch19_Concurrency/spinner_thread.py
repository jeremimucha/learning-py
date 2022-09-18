#!/usr/bin/env python3

import itertools
import time
from threading import Thread, Event


# This function will run in a separate thread.
# The `Event` type is a simple object that can be used
# for thread synchronization.
def spin(msg: str, done: Event) -> None:
    # Infinite loop - .cycle yields one character at a time, cycling forever.
    for char in itertools.cycle(r'\|/-'):
        # `\r` ASCII control character moves the cursor back to the start of the line
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        # Event.wait(timeout=None) -> returns True if the event has been set by another thread.
        # If the timeout elapses it returns False.
        if done.wait(.1):
            break
    # Clear the status line
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


# Will be called by the main thread.
# time.sleep() blocks the main thread, but releases the GIL,
# so the spinner thread can proceed.
def slow() -> int:
    time.sleep(3)
    return 42


def supervisor() -> int:
    done = Event()  # Create an Event instance, to communicate with the Thread,
    spinner = Thread(target=spin, args=('thinking!', done))
    print(f'Spinner Thread object: {spinner}')
    spinner.start()
    # slow() blocks, but GIL is released - most system calls release the GIL.
    # In the meantime the secondary thread will run the spinner animation.
    result = slow()
    done.set()  # Setting the done Event to True will terminate the other thread.
    spinner.join()
    return result


def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')


if __name__ == '__main__':
    main()
