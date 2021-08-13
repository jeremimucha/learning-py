#! /usr/bin/env python

import threading
from enum import Enum
from queue import Queue

from cutlery import Cutlery, ThreadsafeCutlery


# Demonstrates issues with traditional threaded programs - data races.


Task = Enum('Task', 'PrepareTable ClearTable Shutdown')


class ThreadBot(threading.Thread):
    def __init__(self, kitchen):
        super().__init__(target=self.manage_table)
        self.kitchen = kitchen
        self.cutlery = Cutlery(knives=0, forks=0)
        self.tasks = Queue()

    def manage_table(self):
        while True:
            task = self.tasks.get()
            if task == Task.PrepareTable:
                self.kitchen.give(to=self.cutlery, knives=4, forks=4)
            elif task == Task.ClearTable:
                self.cutlery.give(to=self.kitchen, knives=4, forks=4)
            elif task == Task.Shutdown:
                return
            else:
                raise RuntimeError("Invalid task: {!r}".format(task))


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: thread_bot.py <iter-count>")
        print("  where <iter-count> is the number of iterations to use for the test.")
        sys.exit(1)

    def test_bots(bots, kitchen):
        for bot in bots:
            for i in range(int(sys.argv[1])):
                bot.tasks.put(Task.PrepareTable)
                bot.tasks.put(Task.ClearTable)
            bot.tasks.put(Task.Shutdown)

        print('Kitchen inventory before service:', kitchen)

        for bot in bots:
            bot.start()
        
        for bot in bots:
            bot.join()
        
        print('Kitchen inventory after service:', kitchen)

    # The ThreadBot instances accessing the Cutlery instance concurrently leads to data races,
    # since the Cutlery instance is shared and its underlying data is not accessed in a thread-safe manner.
    # The initial and post-test 'knives' and 'forks' values may vary.
    kitchen = Cutlery(knives=100, forks=100)
    bots =[ThreadBot(kitchen) for i in range(10)]

    test_bots(bots, kitchen)

    # The same ThreadBot instances but accessing a threadsafe Cutlery instance will perform correctly,
    # in a threaded environment. Note that this implementation will be slower due to locking.
    print('\nThe same test executed with threadsafe cutlery:')
    safe_kitchen = ThreadsafeCutlery(knives=100, forks=100)
    safe_bots = [ThreadBot(safe_kitchen) for i in range(10)]

    test_bots(safe_bots, safe_kitchen)
