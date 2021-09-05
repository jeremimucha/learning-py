#!/usr/bin/env python

# server.py - simple 'microservice' serving results of the fibonacci sequence
import asyncio
from socket import *
from fib import fib

# This is a trivially threaded version of the service.
# Running this service in combination with the performance tools - perf1 (response time) and perf2 (response/second)
# can be used to show that the side effect of the GIL is that if a long running, computationally heavy
# request is made by a single client, the response time and response/second of all other clients
# will suffer greatly.


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()    # blocking
        print("Connection", addr)


def fib_handler(client):
    while True:
        req = client.recv(100)  # blocking
        if not req:
            break
        try:
            n = int(req)
            result = fib(n)
        except ValueError:
            result = 'Error: Invalid input'
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)   # blocking
    print("Closed.")


if __name__ == '__main__':
    try:
        fib_server(('', 25000))
    except KeyboardInterrupt:
        print("Server shutting down...")
