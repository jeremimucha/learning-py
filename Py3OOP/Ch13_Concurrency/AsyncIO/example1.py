import asyncio
import random


@asyncio.coroutine
def random_sleep(counter):
    delay = random.random() * 5
    print("{} sleeps for {:.2f} seconds".format(counter, delay))
    yield from asyncio.sleep(delay)
    print("{} awakens".format(counter))


@asyncio.coroutine
def five_sleepers():
    print("Creating five tasks")
    tasks = [asyncio.async(random_sleep(i)) for i in range(5)]
    print("Sleeping after starting five tasks")
    yield from asyncio.sleep(2)
    print("Waking and waiting for five tasks")
    yield from asyncio.wait(tasks)

asyncio.get_event_loop().run_until_complete(five_sleepers())
print("Done five tasks")

'''
The five_sleepers coroutine constructs five instances of random_sleep future.
The resulting futures are wrapped in asyncio.async tasks, which adds them
to the loop's task queue so they can execute concurrently when control is
returned to the event loop.
The control is returned whenever 'yield from' is called.
'yield from asyncio.sleep' pauses execution of the coroutine for 2 secs.
During this pause the event loop executes the tasks that it has queued up
i.e. the five random_sleep futures. They each print starting messages then
send the control back to the event loop for a specific amount of time.
Any random_sleep futures with 'sleep' calls shorter than 2 seconds are executed
 - they print the 'awakens' message and return.
Then the five_sleepers wakes up and prints the "Waking..." message.
'yield from asyncio.wait(tasks)' pauses untill all the 'random_sleep' futures
are complete (these will be the ones with .sleep calls longer than 2 seconds).
At that point the event loop queue will be empty and the program terminates.
'''