#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import socket
from threading import Thread


def echo(client: socket.socket):
    while True:
        data = client.recv(2048)
        print(f'Received {data}, sending!')
        client.sendall(data)


def run_threaded_server_bad():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen()
        while True:
            # Block waiting for a client to connect
            connection, _ = server.accept()
            # Once a client connects, create a thread to run our echo function.
            thread = Thread(target=echo, args=(connection,))
            thread.start()
            # Note we're not managing the thread's lifetime.
            # This creates some problems - killing the process will not actualy stop the Threads!
            # They will keep the process alive and all connected clients will be able to communicate.
            #
            # "Solutions":
            # - Make the threads `daemon threads` - these would be killed after KeyboardInterrupt
            #   The downside is that we can't run any cleanup code on shutdown.
            # - Instead we should manage the threads ourselves.


# To handle shutdown cleanly we can subclass the Thread class.
# It has a `run` method that we can override, making it run the startup and shutdown code we need.
class ClientEchoThread(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                # If there's no data, raise an exception.
                # This happens when the connection was closed by the client
                # or the connection was shut down.
                if not data:
                    raise BrokenPipeError('Connection closed!')
                print(f'Received {data}, sending!')
                self.client.sendall(data)
        # When we get an exception, exit the run method.
        # This terminates the thread.
        except OSError as e:
            print(f'Thread interrupted by {e} exception. Shutting down!')

    def close(self):
        # Shut down the connection if the thread is alive; the thread may not be alive
        # if the client closed the connection.
        if self.is_alive():
            self.client.sendall(bytes('Shutting down!', encoding='utf-8'))
            # Shutdown the client connection for reads and writes.
            self.client.shutdown(socket.SHUT_RDWR)


def run_threaded_server_better():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen()
        connection_threads = []
        try:
            while True:
                # We're still blocking listening for connections
                connection, addr = server.accept()
                thread = ClientEchoThread(connection)
                connection_threads.append(thread)
                thread.start()
        except KeyboardInterrupt:
            print('Shutting down!')
            # Call the `close` method on our threads to shut down each client connection on KeyboardInterrupt
            [thread.close() for thread in connection_threads]

def main():
    # run_threaded_server_bad()
    run_threaded_server_better()


if __name__ == '__main__':

    main()
