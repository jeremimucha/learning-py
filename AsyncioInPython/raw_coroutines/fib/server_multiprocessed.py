#!/usr/bin/env python

# server.py - simple 'microservice' serving results of the fibonacci sequence
from socket import *
from fib import fib
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

# This is a multiprocess-pooled version of the server - it bypasses the GIL by using multiple instances
# of the service - running in separate processes.
# This makes the request rate and response time of individual requests essentially independent of other requests.
# The downside of this approach is that it introduces rather significant overhead of interprocess communication.


def fib_server(address, pool):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        Thread(target=fib_handler, args=(client, pool), daemon=True).start()


def fib_handler(client, pool):
    while True:
        req = client.recv(100)
        if not req:
            break
        try:
            n = int(req)
        except ValueError:
            result = 'Error: Invalid input'
        else:
            # Submit the job to the process pool
            future = pool.submit(fib, n)
            result = future.result()
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed.")


if __name__ == '__main__':
    try:
        pool = Pool()   # default workers matches the CPU core count
        fib_server(('', 25000), pool)
    except KeyboardInterrupt:
        print("Server shutting down...")
