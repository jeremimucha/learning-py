#! /usr/bin/env python

# Demonstrates a traditional 0MQ approach to polling - no asyncio used.
import zmq


context = zmq.Context()

# ZMQ sockets are typed. Create a PULL socket - a receive-only socket
# that will receive data from a send-only socket of type PUSH
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# SUB is another receive-only socket, it receives data from
# a send-only socket of type PUB.
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")
subscriber.setsockopt_string(zmq.SUBSCRIBE, '')

# Sockets are not thread-safe, so in a threaded application it's necessary
# to use a poller in order to move data between multiple sockets.
# The Poller will unblock when there's data ready to be received on one
# of the registered sockets.
poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)
poller.register(subscriber, zmq.POLLIN)

while True:
    try:
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break

    if receiver in socks:
        message = receiver.recv_json()
        print(f'Via PULL: {message}')

    if subscriber in socks:
        message = subscriber.recv_json()
        print(f"Via SUB: {message}")
