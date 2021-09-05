#!/usr/bin/env python
# Time a long running request - sends a request to the fibonacci server, requesting the fibonacci number for n=30

from socket import *
from time import perf_counter


def perftest(host, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))

    while True:
        start = perf_counter()
        sock.send(b'30')
        resp = sock.recv(100)
        end = perf_counter()
        print('Response time: {} ms'.format((end - start) * 1e3))


if __name__ == '__main__':
    from argparse import ArgumentParser
    argp = ArgumentParser('Request response timer')
    argp.add_argument('--host', default='localhost', help='URL of the service')
    argp.add_argument('--port', default=25000, type=int, help='Port the service is running on')
    args = argp.parse_args()

    try:
        perftest(args.host, args.port)
    except KeyboardInterrupt:
        pass
