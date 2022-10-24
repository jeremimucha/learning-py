#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))


import socket


def recv_line(connection: socket.socket):
    buffer = b''
    while buffer[-2:] != b'\r\n':
        data = connection.recv(2)
        if not data:
            break
        else:
            print(f'I got data: {data}!')
            buffer = buffer + data
    return buffer


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    address = ('127.0.0.1', 8000)
    server_socket.bind(address)
    server_socket.listen()

    # Keep track of connected clients
    connections = []
    
    try:
        # Attempt to handle multiple clients at the same time.
        # This can't be done reliably by a single-threaded application, since the socket.recv/socket.send
        # are blockign calls. The first client that reaches the `recv_line(...)` call, will block other
        # clients from sending messages until it fully sends and received its message.
        # This also means that new clients are blocked from connecting until the next iteration of the loop.
        while True:
            connection, client_address = server_socket.accept()
            print(f'I got a connection from {client_address}!')
            connections.append(connection)
            for conn in connections:
                data = recv_line(conn)
                print(f'All the data is: {data}')
                # conn.sendall(data)
                conn.send(data)
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
