#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))


import socket


# Utilize nonblocking sockets to handle multiple clients.
# This direct implementation ignores the BlockingIOError exceptions
# raised on an attempt to read from a socket that doens't have any data.
# This works, but comes at a cost of busy-looping the entire time,
# while clients are not sending any data.


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen()
    # Configure the socket to be non-blocking. Meaning that it will only
    # return the data it already has available, or in case of this listening socket,
    # any clients attempting to connect.
    # If there isn't any clients attempting to connect when .accept() is called
    # the socket will raise `BlockingIOError` instead.
    # We can catch and ignore this exception repeatedly until a client connects.
    server_socket.setblocking(False)

    # Keep track of connected clients
    connections = []
    
    try:
        while True:
            try:
                connection, client_address = server_socket.accept()
                # Set the client connection as non-blocking as well.
                connection.setblocking(False)
                print(f'I got a connection from {client_address}!')
                connections.append(connection)
            except BlockingIOError:
                pass
            for conn in connections:
                try:
                    buffer = b''
                    while buffer[-2:] != b'\r\n':
                        data = conn.recv(2)
                        if not data:
                            break
                        else:
                            print(f'I got data: {data}!')
                            buffer = buffer + data
                    print(f'All the data is: {buffer}')
                    # conn.sendall(buffer)
                    conn.send(buffer)
                except BlockingIOError:
                    pass
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
