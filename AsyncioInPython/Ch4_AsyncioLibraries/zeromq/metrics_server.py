#! /usr/bin/env python

# This is the collection service of the microservice-based application demo.

import asyncio
import aiohttp, aiohttp.web
import zmq, zmq.asyncio
import json
from aiohttp_sse import sse_response    # sse == server-sent events
from contextlib import suppress
from weakref import WeakSet


# zmq.asyncio.install()
ctx = zmq.asyncio.Context()
connections = WeakSet() # keeps track of all the connected web clients


# This coro recieves instrumented data from every service.
async def collector():
    sock = ctx.socket(zmq.SUB)
    # empty topic name -> accept all messages on this port
    sock.setsockopt_string(zmq.SUBSCRIBE, '')
    # Note that the server here is the receiving end of the connection
    # so we bind even though we're exposing a SUB socket.
    sock.bind('tcp://*:5555')
    await sock.recv()   # necessary? discard initial empty message? see poller_aio.py
    with suppress(asyncio.CancelledError):
        while data := await sock.recv_json():
            print(data)
            # send the received data to all clients
            for q in connections:
                await q.put(data)
    sock.close()


async def feed(request):
    queue = asyncio.Queue()
    connections.add(queue)
    with suppress(asyncio.CancelledError):
        async with sse_response(request) as resp:
            while data := await queue.get():
                print('sending data:', data)
                await resp.send(json.dumps(data))
    return resp


async def index(request):
    return aiohttp.web.FileResponse('./charts.html')


async def start_collector(app: aiohttp.web.Application):
    app['collector'] = app.loop.create_task(collector())


async def stop_collector(app: aiohttp.web.Application):
    print("Stopping collector...")
    app["collector"].cancel()
    await app['collector']
    ctx.term()


if __name__ == '__main__':
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/feed', feed)
    app.on_startup.append(start_collector)
    app.on_cleanup.append(stop_collector)
    aiohttp.web.run_app(app, host='127.0.0.1', port=8088)
