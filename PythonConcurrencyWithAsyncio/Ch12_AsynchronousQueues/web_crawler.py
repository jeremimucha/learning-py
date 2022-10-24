#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Queue
import aiohttp
from aiohttp import ClientSession
import logging
from bs4 import BeautifulSoup


class WorkItem:
    def __init__(self, item_depth: int, url: str):
        self.item_depth = item_depth
        self.url = url


async def worker(worker_id: int, queue: Queue, session: ClientSession, max_depth: int):
    print(f'Worker {worker_id}')
    # Grab a URL from the queue to process and then begin to download it.
    while True:
        work_item: WorkItem = await queue.get()
        print(f'Worker {worker_id}: Processing {work_item.url}')
        await process_page(work_item, queue, session, max_depth)
        print(f'Worker {worker_id}: Finished {work_item.url}')
        queue.task_done()


# Download the URL contents, and parse all links from the page, putting them back on the queue.
async def process_page(work_item: WorkItem, queue: Queue, session: ClientSession, max_depth: int):
    try:
        response = await asyncio.wait_for(session.get(work_item.url), timeout=3)
        if work_item.item_depth == max_depth:
            print(f'Max depth reached, for {work_item.url}')
        else:
            body = await response.text()
            soup = BeautifulSoup(body, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                # Note: If we were working with a bounded queue, we'd need to use `await queue.put()` here.
                url: str = link['href']
                if url.startswith('/'):
                    url = work_item.url + url
                if url.startswith('http'):
                    queue.put_nowait(WorkItem(work_item.item_depth + 1, url))
    except Exception as e:
        logging.exception(f'Error processing url {work_item.url}')


# Create a queue and 100 worker tasks to process URLs.
async def main():
    start_url = 'http://example.com'
    url_queue = Queue()
    url_queue.put_nowait(WorkItem(0, start_url))
    async with aiohttp.ClientSession() as session:
        workers = [asyncio.create_task(worker(i, url_queue, session, 3))
                   for i in range(100)]
        await url_queue.join()
        [w.cancel() for w in workers]


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
