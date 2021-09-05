#!/usr/bin/env python
# Check how many requests per second can be executed by the fibonacci server.
# Sends a request for the fibonacci number for n=1 (simulating a quick task).

from socket import *
from time import perf_counter, sleep
from threading import Thread


n = 0

def monitor():
    global n
    while True:
        sleep(1)
        print(n, 'reqs/sec')

def perftest(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))

    while True:
        global n
        sock.send(b'1')
        resp = sock.recv(100)
        n += 1


if __name__ == '__main__':
    from argparse import ArgumentParser
    argp = ArgumentParser('Request response timer')
    argp.add_argument('--host', default='localhost', help='URL of the service')
    argp.add_argument('--port', default=25000, type=int, help='Port the service is running on')
    args = argp.parse_args()

    try:
        Thread(target=monitor).start()
        perftest(args.host, args.port)
    except KeyboardInterrupt:
        pass
