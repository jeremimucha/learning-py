#! /usr/bin/env python

import asyncio
from asyncio import StreamReader, StreamWriter


# Mock coroutine - assume that this would contact an external server
# and notify it about specific events.
async def send_event(msg: str):
    await asyncio.sleep(1)


async def echo(reader: StreamReader, writer: StreamWriter):
    print("New connection.")
    try:
        while (data := await reader.readline()):
            writer.write(data.upper())
            await writer.drain()
        print("Leaving Connection.")
    except asyncio.CancelledError:
        msg = "Connection dropped!"
        print(msg)
        # Note that this is bad practice that leads to errors.
        # A task/future should never be created within a CancelledError
        # handler of a coroutine. Due to specifics of how asyncio.run
        # is implemented, this will cause the loop to be closed while
        # the task created here is still pending. This is because
        # asyncio.run gathers unfinished tasks, cancells them
        # and runs until completion once - meaning that tasks
        # created due to cancellation will not be awaited
        # until completion.
        # asyncio.create_task(send_event(msg))



async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bye!")
