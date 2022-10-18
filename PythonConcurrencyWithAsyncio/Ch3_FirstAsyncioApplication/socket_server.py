#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))


import socket


def main():
    # Create a socket using the IP:PORT addressing and TCP communication protocol
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the reusable flag, so that we can re-run the application without errors
    # due to the system not releasing the socket.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # We need to assign an address and port to the socket, so that the server
    # can listen on this address and clients can connect to it.
    address = ('127.0.0.1', 8000)
    server_socket.bind(address)
    # Listen for connections from clients who want to connect to our server.
    server_socket.listen()
    # accepting a connection returns a `connection` object and the address of the client
    try:
        connection, client_address = server_socket.accept()
        print(f'I got a connection from {client_address}!')

        buffer = b''
        while buffer[-2:] != b'\r\n':
            # Intentionally use a tiny buffer size here, to demonstrate interaction
            # with short messages received from the telnet client.
            # In a real world application we'd set buffer to something large ~1024 Bytes or greater.
            data = connection.recv(2)
            if not data:
                break
            else:
                print(f'I got data: {data}!')
                buffer = buffer + data

        print(f'All the data is: {buffer}')
        # Echo the data back to the client
        connection.sendall(buffer)
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
