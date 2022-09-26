#!/usr/bin/env python3

# tag::TCP_MOJIFINDER_TOP[]
import asyncio
import functools
import sys
from asyncio.trsock import TransportSocket
from typing import cast

# `format_results` is used to display the results of InvertedIndex.search
# in a text-based UI such as teh command line or a Telnet session.
from charindex import InvertedIndex, format_results

CRLF = b'\r\n'
PROMPT = b'?> '

# This is later wrapped with a functools.partial, to bind the index argument,
# because `asyncio.start_server` expects a callback that takes only
# the reader and writer.
async def finder(index: InvertedIndex,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
    # Get the remote client addres to which the socket is connected.
    client = writer.get_extra_info('peername')
    # Handle a dialog that last until a control character is received
    # from the client.
    while True:
        # The StreamWriter.write method is not a coroutine - just a plain function.
        writer.write(PROMPT)  # can't await!
        # StreamWriter.drain flushes the writer buffer, it is a coroutine
        # so it must be driven with await.
        await writer.drain()  # must await!
        # StreamReader.readline is a coroutine, returns bytes.
        data = await reader.readline()
        # If no bytes were received - the clinet closed the connection, so exit the loop.
        if not data:
            break
        try:
            # Decode the bytes to string, using the default encoding.
            query = data.decode().strip()
        # UnicodeDecodeError may happen when the user hits Ctrl-C and the Telnet client sends control bytes;
        # if that happens, replace the query with a null character for simplicity.
        except UnicodeDecodeError:
            query = '\x00'
        # Log the query to the server console.
        print(f' From {client}: {query!r}')
        if query:
            # Exit the loop if a control or a null character was received.
            if ord(query[:1]) < 32:
                break
            #  Do the actual search
            results = await search(query, index, writer)
            # Log the response to the server console.
            print(f'   To {client}: {results} results.')

    # Close the stream writer,
    writer.close()
    # Wait for the StreamWriter to close - this is recommended in the .close() method documentation.
    await writer.wait_closed()
    # Log the end of this client's session to the server console.
    print(f'Close {client}.')
# end::TCP_MOJIFINDER_TOP[]


# tag::TCP_MOJIFINDER_SEARCH[]
# search must be a coroutine, because it writes to a StreamWriter and must use it's .drian() coroutine method.
async def search(query: str,
                 index: InvertedIndex,
                 writer: asyncio.StreamWriter) -> int:
    # Query the inverted index
    chars = index.search(query)
    # This generator expression will yield byte strings encoded in UTF-8 with the Unicode codepoint,
    # the actual character, its name, and CRLF sequence.
    lines = (line.encode() + CRLF for line
                in format_results(chars))
    # Send the lines, writer.writelines is not a coroutine, so no await.
    writer.writelines(lines)
    # writer.drain() is a coro - await it.
    await writer.drain()
    # Build a status line, then send it.
    status_line = f'{"─" * 66} {len(chars)} found'
    writer.write(status_line.encode() + CRLF)
    await writer.drain()
    return len(chars)
# end::TCP_MOJIFINDER_SEARCH[]


# tag::TCP_MOJIFINDER_MAIN[]
async def supervisor(index: InvertedIndex, host: str, port: int) -> None:
    # We await the start of the server - asyncio.start_server,
    # returns asyncio.Server - a TCP socket server ready to receive connections.
    server = await asyncio.start_server(
        # The first argument is a `client_connected_cb` - a callback
        # to run when a new client connection starts. The callback can be
        # a function or a coroutine, but it must accept exactly two arguments:
        # - asyncio.StreamReader,
        # - asyncio.StreamWriter.
        # However, the `finder` coroutine defined here also needs to get an
        # `index`, so it is bound here using functools.partial.
        functools.partial(finder, index),
        # host and port arguments are also required.
        host, port)

    # Needed because of outdated `server.sockets` type hints on `typeshed`.
    socket_list = cast(tuple[TransportSocket, ...], server.sockets)
    addr = socket_list[0].getsockname()
    # Display the address and the port of the first socket of the server.
    print(f'Serving on {addr}. Hit CTRL-C to stop.')
    # Suspend the supervisor coroutine here so that the `supervisor` coroutine
    # doesn't exit immediately.
    # The server is already serving connections since the moment it was constructed
    # on line 60, but this use is allowed specifically for the purpose of yielding
    # control to the server, just like is done here.
    await server.serve_forever()

def main(host: str = '127.0.0.1', port_arg: str = '2323'):
    port = int(port_arg)
    print('Building index.')
    # Build the inverted index. This could also be delegated to a thread
    # using `loop.run_with_executor()`, so that the server starts handling
    # requests quicker, while the index is being built.
    index = InvertedIndex()
    try:
        # Start the event loop running supervisor.
        asyncio.run(supervisor(index, host, port))
    # Catch the KeyboardInterrupt to avoid a traceback when stopping the server with Ctrl-C
    except KeyboardInterrupt:
        print('\nServer shut down.')

if __name__ == '__main__':
    main(*sys.argv[1:])
# end::TCP_MOJIFINDER_MAIN[]
