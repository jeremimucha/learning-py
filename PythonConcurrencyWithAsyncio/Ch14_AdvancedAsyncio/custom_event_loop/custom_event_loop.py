#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import functools
import selectors
from typing import List

from Ch14_AdvancedAsyncio.custom_event_loop.custom_future import CustomFuture
from Ch14_AdvancedAsyncio.custom_event_loop.custom_task import CustomTask


class EventLoop:
    _tasks_to_run: List[CustomTask] = []

    def __init__(self):
        self.selector = selectors.DefaultSelector()
        self.current_result = None

    # Register a socket with the selector for read events
    def _register_socket_to_read(self, sock, callback):
        future = CustomFuture()
        try:
            self.selector.get_key(sock)
        except KeyError:
            sock.setblocking(False)
            self.selector.register(sock, selectors.EVENT_READ, functools.partial(callback, future))
        else:
            self.selector.modify(sock, selectors.EVENT_READ, functools.partial(callback, future))
        return future

    def _set_current_result(self, result):
        self.current_result = result

    # Register a scoket to receive data from a client.
    async def sock_recv(self, sock):
        print('Registering socket to listen for data...')
        return await self._register_socket_to_read(sock, self.received_data)

    # Register a scoket to accept connections from a client
    async def sock_accept(self, sock):
        print('Registering socket to accept connections...')
        return await self._register_socket_to_read(sock, self.accept_connection)

    def sock_close(self, sock):
        self.selector.unregister(sock)
        sock.close()

    # Register a task with the event loop
    def register_task(self, task):
        self._tasks_to_run.append(task)

    def received_data(self, future, sock):
        data = sock.recv(1024)
        future.set_result(data)

    def accept_connection(self, future, sock):
        result = sock.accept()
        future.set_result(result)

    # Run a main coroutine until it finishes, executing any pending tasks at each iteration.
    def run(self, coro):
        self.current_result = coro.send(None)

        while True:
            try:
                if isinstance(self.current_result, CustomFuture):
                    self.current_result.add_done_callback(self._set_current_result)
                    if self.current_result.result() is not None:
                        self.current_result = coro.send(self.current_result.result())
                else:
                    self.current_result = coro.send(self.current_result)
            except StopIteration as si:
                return si.value

            for task in self._tasks_to_run:
                task.step()

            self._tasks_to_run = [task for task in self._tasks_to_run if not task.is_finished()]

            events = self.selector.select()
            print('Selector has an event, processing...')
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)


if __name__ == '__main__':
    pass