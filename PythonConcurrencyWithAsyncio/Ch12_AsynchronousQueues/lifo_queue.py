#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Queue, LifoQueue
from dataclasses import dataclass, field


# Here we also employ an order counting strategy - every subsequent item added has an incremental counter.
# This plays role in PriorityQueues - for items that have the same priority but were added subsequently,
# it's one of the approaches that can be used to introduce some secondary ordering.
@dataclass(order=True)
class WorkItem:
    priority: int
    order: int
    data: str = field(compare=False)


async def worker(queue: Queue):
    while not queue.empty():
        # Get an item from the queue, or pop it from the stack
        work_item: WorkItem = await queue.get()
        queue.task_done()


async def main():
    lifo_queue = LifoQueue()

    work_items = [
        WorkItem(3, 1, 'Lowest priority first'),
        WorkItem(3, 2, 'Lowest priority second'),
        WorkItem(3, 3, 'Lowest priority third'),
        WorkItem(2, 4, 'Medium priority'),
        WorkItem(3, 5, 'High priority'),
    ]

    for work in work_items:
        # Push an item onto the stack
        lifo_queue.put_nowait(work)
    
    worker_task = asyncio.create_task(worker(lifo_queue))

    await asyncio.gather(lifo_queue.join(), worker_task)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
