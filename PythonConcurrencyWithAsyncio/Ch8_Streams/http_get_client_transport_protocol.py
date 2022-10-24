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
from asyncio import Transport, Future, AbstractEventLoop
from typing import Optional


# Transports and Protocols
# - Transport is an abstraction for communication with an arbitrary stream of data,
#   such as standard input. It provides definitions for sending and receiving data
#   to and from a source.
# - Protocol is an abstraction defining the lifecycle of a connection between the ends
#   of the communication channel (e.g. socket).
#   It defines how a connection is established, how the received data is processed
#   and how to handle the end of transmission.
#
# asyncio exposes a coroutine named `create_connection`, which creates a socket connection
# to a given host an wraps it in an appropriate Transport.
# It requires a `protocol factory` as one of its arguments

# This is a rather low-level API, that wouldn't normally be used in application-level code.
# It's generally used in designing and implementation networking libraries or web frameworks.
# For application level code asyncio provides Streams - StreamReader and StreamWriter.


class HTTPGetClientProtocol(asyncio.Protocol):

    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host: str = host
        self._future: Future = loop.create_future()
        self._transport: Optional[Transport] = None
        self._response_buffer: bytes = b''

    # Await the internal future until we get a reponse from the server
    async def get_response(self):
        return await self._future
    
    # Create the HTTP request.
    def _get_request_bytes(self) -> bytes:
        request = f'GET / HTTP/1.1\r\n' \
                  f'CONNECTION: close\r\n' \
                  f'Host: {self._host}\r\n\r\n'
        return request.encode()

    # The `connection_made` method is a callback called when the client
    # (instance of this class) connects to the server.
    def connection_made(self, transport: Transport):
        print(f'Connection made to {self._host}')
        self._transport = transport
        # Once the connection is established, use the transport to send the request.
        self._transport.write(self._get_request_bytes())

    # The `data_received` callback is called when the client receives data from the server.
    def data_received(self, data: bytes) -> None:
        print(f'Data received!')
        # Once we have data, save it to our internal buffer
        self._response_buffer += data

    # The `eof_received` callback is called when the connection is closed.
    # Returning `False` from this callback means that the Transport instance should handle shutdown.
    # Returning `True` would indicate that we're going to handle shutdown ourselves
    def eof_received(self) -> Optional[bool]:
        # Once the connection closes, complete the future with the buffer
        self._future.set_result(self._response_buffer.decode())
        return False
    
    # If the connection closes without error, do nothing. Otherwise complete the future with an exception.
    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc is None:
            print('Connection closed without error.')
        else:
            self._future.set_exception(exc)


# Define a coroutine that makes the request.
# It defined a factory function that returns the HTTPGetClientProtocol.
# The `create_connection` returns both `transport` and the `protocol` instance (constructed by our factory).
# Here, we use just the protocol instance to get the response.
async def make_request(host: str, port: int, loop: AbstractEventLoop) -> str:
    def protocol_factory():
        return HTTPGetClientProtocol(host, loop)

    transport, protocol = await loop.create_connection(protocol_factory, host=host, port=port)
    # transport unused here

    return await protocol.get_response()


async def main():
    loop = asyncio.get_running_loop()
    result = await make_request('www.example.com', 80, loop)
    print(result)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
