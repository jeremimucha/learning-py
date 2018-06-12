'''
The request.cached_setup method can be used to create function argument
variables that last longer than one test. This is useful when setting up an
expensive operation that can be reused by multiple tests.

Example:
An echo server instance running in a separate process, and then have multiple
tests connect to that instance.
'''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 1028))
s.listen(1)

    while True:
        client, address = s.accept()
        data = client.recv(1024)
        client.send(data)
        client.close()
