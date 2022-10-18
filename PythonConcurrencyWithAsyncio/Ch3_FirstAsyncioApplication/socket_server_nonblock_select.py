#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))


import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple


# This nonblocking multi-client server uses system events - kqueue, epoll, IOCP (depending on OS)
# to implement a server capable of handling multiple clients without blocking, while not
# being CPU intensive.
# The system-specific details are abstracted away by the `selectors` module.
# Each socket (server socket, connecetd client sockets) are registered with the BaseSelector,
# stating that we're interested in events from that socket.
# When `select` is called it will block until an event has happened, and once it does,
# the call will return with a list of sockets that are ready for processing along with
# the vent that triggered it. It also supports timeout, which will return an empty
# set of events after a specified amount of time.


def main():
    # Let the module decide what is the best implementation for this OS.
    selector = selectors.DefaultSelector()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)
    server_address = ('127.0.0.1', 8000)
    server_socket.bind(server_address)
    server_socket.listen()

    # Register the server socket - we're interested in read events - clients trying to connect.
    selector.register(server_socket, selectors.EVENT_READ)

    while True:
        # Wait for events for up to 1 second - new connections or client messages.
        events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

        # If we get no events for 1s just log a mesasge and proceed.
        if len(events) == 0:
            print("No events, waiting a bit more!")

        for event, _ in events:
            # Get the socket for the event, which is stored in the fileobj field.
            event_socket = event.fileobj

            # If the event_socket is the same as the server_socket we know
            # this is a new incomming connection attempt.
            if event_socket == server_socket:
                connection, address = server_socket.accept()
                connection.setblocking(False)
                print(f'I got a connection from {address}')
                # Register the new client socket with our selector
                selector.register(connection, selectors.EVENT_READ)
            else:
                # Otherwise this is client data - recv and echo back.
                data = event_socket.recv(1024)
                print(f"I got some data: {data}")
                event_socket.send(data)

if __name__ == '__main__':
    main()
