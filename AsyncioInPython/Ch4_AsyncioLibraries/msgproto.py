#! /usr/bin/env python

from asyncio import StreamReader, StreamWriter


async def read_msg(stream: StreamReader) -> bytes:
    size_bytes = await stream.readexactly(4)            # read the msg header
    size = int.from_bytes(size_bytes, byteorder='big')  # convert the header to an int
    data = await stream.readexactly(size)               # read the data
    return data


async def send_msg(stream: StreamWriter, data: bytes):
    # prepare the 'header' - the size of the data
    size_bytes = len(data).to_bytes(4, byteorder='big')
    stream.writelines([size_bytes, data])   # send the data size and the data itself
    await stream.drain()
