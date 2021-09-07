#!/usr/bin/env python

# The same echo server, but using the "fake_asyncio" module, that emulates asyncio using coroutines

from socket import *
import fake_asyncio

loop = fake_asyncio.Loop()

async def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)

    # loop = asyncio.get_running_loop()
    while True:
        client, addr = await loop.sock_accept(sock)
        print('Connection from', addr)
        loop.create_task(echo_handler(client))


async def echo_handler(client: socket):
    # loop = asyncio.get_running_loop()
    with client:
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                break
            await loop.sock_sendall(client, b'Got: ' + data)
    print('Connection closed')


if __name__ == '__main__':
    try:
        # asyncio.run(echo_server(('', 25000)))
        loop.create_task(echo_server(('', 25000)))
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
