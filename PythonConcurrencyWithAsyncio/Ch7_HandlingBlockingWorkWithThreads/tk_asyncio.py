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
from asyncio import AbstractEventLoop
from aiohttp import ClientSession
from concurrent.futures import Future
from queue import Queue # threadsafe queue
from tkinter import Tk
from tkinter import ttk
from tkinter import Label
from tkinter import Entry
from typing import Callable, Optional
from threading import Thread

# TkInter and asyncio both run on blocking event loops. To mary the two, we need to launch
# asyncio event loop on a separate thread and schedule the work from the main TkInter event loop thread.
# asyncio exposes some functions that can help with scheduling work from different threads:
# * .call_soon_threadsafe - schedules a function (not coro) to run on the next iteration of the event loop.
# * .run_coroutine_threadsafe - schedules a coroutine to run on the next iteration of the event loop.
#   This returns a concurrent.future, which is threadsafe.


class StressTest:

    def __init__(self,
                 loop: AbstractEventLoop,
                 url: str,
                 total_requests: int,
                 callback: Callable[[int, int], None]):
        self._completed_requests: int = 0
        self._load_test_future: Optional[Future] = None
        self._loop = loop
        self._url = url
        self._total_requests = total_requests
        self._callback = callback
        self._refresh_rate = total_requests // 100

    # Start making the requests, and store the future, so we can later cancel if needed.
    def start(self):
        future = asyncio.run_coroutine_threadsafe(self._make_requests(), self._loop)
        self._load_test_future = future

    # If we want to cancel, we can use the future we received.
    def cancel(self):
        if self._load_test_future:
            # We're also scheduling the cancelation on the asyncio thread.
            self._loop.call_soon_threadsafe(self._load_test_future.cancel)

    async def _get_url(self, session: ClientSession, url: str):
        try:
            await session.get(url)
        except Exception as e:
            print(e)
        # Note that we're not synchronizing anything here, despite the fact that this code can be executed
        # from multiple coroutines. This is because asyncio is inherently single-threaded, and the event loop
        # runs only a single piece of python code at a time, there's no need for synchronization.
        self._completed_requests += 1
        # Every `_refresh_rate`% of requests call the callback with the number of completed requests and total requests
        if self._completed_requests % self._refresh_rate == 0 \
            or self._completed_requests == self._total_requests:
            # Note that the callback we're calling here only communicates witha threadsafe Queue,
            # posting updates on the completion changes. The TK thread polls the queue and actually updates the UI.
            # In theory TkInter is threadsafe and since asyncio only runs one coro at a time we could be updating
            # the UI on the asyncio thread (provided that Tk doesn't touch that particular widget?), but it makes
            # sense to use a generic pattern that's always safe.
            self._callback(self._completed_requests, self._total_requests)

    async def _make_requests(self):
        async with ClientSession() as session:
            reqs = [self._get_url(session, self._url) for _ in range(self._total_requests)]
            await asyncio.gather(*reqs)


class LoadTester(Tk):

    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self._queue = Queue()
        self._refresh_ms = 25

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title('URL Requester')

        self._url_label = Label(self, text='URL:')
        self._url_label.grid(column=0, row=0)
        self._url_field = Entry(self, width=10)
        self._url_field.grid(column=1, row=0)

        self._request_label = Label(self, text="Number of requests:")
        self._request_label.grid(column=0, row=1)
        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        # Run the _start method when clicked
        self._submit = ttk.Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress:")
        self._pb_label.grid(column=0, row=3)
        self._pb = ttk.Progressbar(self, orient='horizontal', length=200, mode="determinate")
        self._pb.grid(column=1, row=3, columnspan=2)

    # The update bar method will set the progress bar to a percentage complete value from 0 to 100.
    # This method should only be called in the main thread.
    def _update_bar(self, pct: int):
        # if self._load_test is not None:
        if pct == 100:
            self._load_test = None
            self._submit['text'] = 'Submit'
        else:
            self._pb['value'] = pct
            self.after(self._refresh_ms, self._poll_queue)
        # else:
        #     self._pb['value'] = 0

    # Callback passed to the StressTest instance. It adds a progress update to the queue.
    def _queue_update(self, completed_requests: int, total_requests: int):
        self._queue.put(int(completed_requests / total_requests * 100))

    # Try to get a progress update from the queue. If we have one - update the progress bar.
    def _poll_queue(self):
        if not self._queue.empty():
            percent_complete = self._queue.get()
            self._update_bar(percent_complete)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._poll_queue)

    # Start the load test and start polling every 25 milliseconds for queue updates
    def _start(self):
        if self._load_test is None:
            self._submit['text'] = 'Cancel'
            test = StressTest(self._loop,
                              self._url_field.get(),
                              int(self._request_field.get()),
                              self._queue_update)
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit['text'] = 'Submit'
            self._pb['value'] = 0
            self._queue = Queue()


# Create a new thread calss to run the asyncio event loop forever.
class ThreadedEventLoop(Thread):
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Get an asyncio event loop without starting it.
    loop = asyncio.new_event_loop()
    # Start the new thread to run the asyncio event loop in the background.
    asyncio_thread = ThreadedEventLoop(loop)
    asyncio_thread.start()

    # Create the load tester Tkinter application, and start its main event loop
    app = LoadTester(loop)
    app.mainloop()
