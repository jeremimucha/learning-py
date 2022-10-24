#!/usr/bin/env python3

from dataclasses import dataclass, field
from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Queue, PriorityQueue
from typing import Tuple

# Example of how PriorityQueues work.
# For simple cases we can just use Tuples, and rely on the ordering they provide.

async def worker_tuples(queue: Queue):
    while not queue.empty():
        work_item: Tuple[int, str] = await queue.get()
        print(f'Processing work item {work_item}')
        queue.task_done()


async def simple_prio_queue_tuple():
    priority_queue = PriorityQueue()

    work_items = [(3, 'Lowest priority'),
                  (2, 'Medium priority'),
                  (1, 'High priority')]

    for work in work_items:
        priority_queue.put_nowait(work)

    worker_task = asyncio.create_task(worker_tuples(priority_queue))
    await asyncio.gather(priority_queue.join(), worker_task)


# A more realistic example would use dataclasses, or some other ordering mechanism for our data

@dataclass(order=True)
class WorkItem:
    priority: int
    data: str = field(compare=False)

async def worker(queue: Queue):
    while not queue.empty():
        work_item: WorkItem = await queue.get()
        print(f'Processing work item {work_item}')
        queue.task_done()

async def prio_queue_dataclasses():
    priority_queue = PriorityQueue()

    work_items = [WorkItem(3, 'Lowest priority'),
                  WorkItem(2, 'Medium priority'),
                  WorkItem(1, 'High priority')]

    for work in work_items:
        priority_queue.put_nowait(work)

    worker_task = asyncio.create_task(worker(priority_queue))
    await asyncio.gather(priority_queue.join(), worker_task)


async def main():
    await simple_prio_queue_tuple()
    await prio_queue_dataclasses()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
