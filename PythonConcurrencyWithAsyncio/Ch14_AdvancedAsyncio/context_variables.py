#!/usr/bin/env python3
import os
import asyncio
from asyncio import StreamReader, StreamWriter
from contextvars import ContextVar


# Python's context variables are meant to handle the concept of a thread local variable
# within a single-threaded concurrency model - specifically within coroutines and asyncio's event loop.
#
# If a task creates a context variable, any inner coroutine or task within that initial task will have
# access to that variable. No other tasks outside of that chain will be able to see or modify the variable.


class Server:
    # Create a context variable with the name 'user_address'
    user_address = ContextVar('user_address')

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def start_server(self):
        server = await asyncio.start_server(self._client_connected, self.host, self.port)
        await server.serve_forever()
    
    def _client_connected(self, reader: StreamReader, writer: StreamWriter):
        # Store the client's address in the context variable.
        # This data will be accessible to this coroutine and all coroutines
        # started from within the context of this coroutine - here self.listen_for_messages.
        # This gives us a clean way of passing variables to coroutines/tasks, without doing so
        # explicitly via arguments.
        self.user_address.set(writer.get_extra_info('peername'))
        asyncio.create_task(self.listen_for_messages(reader))

    async def listen_for_messages(self, reader: StreamReader):
        while data := await reader.readline():
            # Display the user's message alogside theire address from the context variable.
            print(f'Got message {data} from {self.user_address.get()}')
    

async def main():
    server = Server('127.0.0.1', 9000)
    await server.start_server()
    

if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
