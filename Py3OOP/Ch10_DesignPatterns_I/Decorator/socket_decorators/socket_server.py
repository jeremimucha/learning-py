import socket
from socket_decorators import LogSocket, GzipSocket

log_send = True
compress_hosts = ('localhost', '127.0.0.1')

def respond(client):
    response = input("Enter a value: ")
    client.send(bytes(response, 'utf8'))
    client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost',2401))
server.listen(1)
try:
    while True:
        client, addr = server.accept()
        # using decorators allows us to dynamicly wrap objects based on
        # some conditions (here state of global variables)
        if log_send:
            client = LogSocket(client)
        if client.getpeername()[0] in compress_hosts:
            client = GzipSocket(client)
        respond(client)
finally:
    server.close()
