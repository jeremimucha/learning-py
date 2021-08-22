#! /usr/bin/env python

# Program demonstratic how to use the asyncio interface of zeromq
import asyncio
import zmq
from asyncio import Queue
from zmq.asyncio import Context


context = Context()

# Using coroutines for the ZMQ code has the advantage of
# encapsulating code related to each socket in a single coroutine.
# There's also no Poller - it's integrated into the asyncio event loop.


# TODO: It seems like to `do_receiver` and `do_subscriber` both need
# an initial `await .recv()`, which always returns a b'0' msg,
# otherwise the asyncio ends up looping over just one of the coros
# indefinitely. After the poller_aio is killer and restarted
# the communication proceeds as expected (looping over both coros).
# Another symptom is that if the poller_aio is started first, and the
# poller_aio_srv (or just poller_srv) is started later, the poller_aio
# crashes with no errors reported, if these initial .recv()'s are not present.
#
# Figure out why.


async def do_receiver():
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")
    # This initial recv seems to be necessary to initialize communication correctly,
    # check the docs.    
    msg = await receiver.recv()
    if msg:
        print(f"PULL init msg: {msg}")
    while message := await receiver.recv_json():
        print(f"Via PULL: {message}")


async def do_subscriber():
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5556")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
    # This initial recv seems to be necessary to initialize communication correctly,
    # check the docs.
    msg = await subscriber.recv()
    if msg:
        print(f"SUB init msg: {msg}")
    while message := await subscriber.recv_json():
        print(f"Via SUB: {message}")


async def main():
    await asyncio.gather(
        do_receiver(),
        do_subscriber(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
