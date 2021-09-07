#!/usr/bin/env python

# async/await is built on top of coroutines. This demo shows how async/await operates internally
# using coroutines and generators.


from types import coroutine
from collections import deque
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


@coroutine
def read_wait(sock):
    """Returns an 'op code' and the arguments for the operation - sock."""
    yield 'read_wait', sock


@coroutine
def write_wait(sock):
    """Returns an 'op code' and the arguments for the operation - sock."""
    yield 'write_wait', sock


class Loop:
    def __init__(self):
        # queue of ready tasks
        self.ready = deque()
        # interface for the operating system's `select` calls,
        # informing which file handles (sockets) are ready to read/write
        self.selector = DefaultSelector()

    async def sock_recv(self, sock, maxbytes):
        await read_wait(sock)
        return sock.recv(maxbytes)

    async def sock_accept(self, sock):
        await read_wait(sock)
        return sock.accept()

    async def sock_sendall(self, sock, data):
        while data:
            try:
                nsent = sock.send(data)
                data = data[nsent:]
            except BlockingIOError:
                await write_wait(sock)

    def create_task(self, coro):
        self.ready.append(coro)

    def run_forever(self):
        while True:
            while not self.ready:
                events = self.selector.select()
                for key, _ in events:
                    self.ready.append(key.data)
                    self.selector.unregister(key.fileobj)

            while self.ready:
                self.current_task = self.ready.popleft()
                try:
                    op, *args = self.current_task.send(None)  # Run to the yield
                    # call the operation yielded by the pending task
                    getattr(self, op)(*args)
                except StopIteration:
                    pass

    def read_wait(self, sock):
        # The current_tasks expects a signal that the socket `sock` is readable
        self.selector.register(sock, EVENT_READ, self.current_task)

    def write_wait(self, sock):
        self.selector.register(sock, EVENT_WRITE, self.current_task)
