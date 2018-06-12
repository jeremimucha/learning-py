import gzip
from io import BytesIO


# A decorator that logs data sent over the socket to stdout
class LogSocket:

    def __init__(self, socket):
        self.socket = socket

    def send(self, data):
        print("Sending {0} to {1}".format(data, self.socket.getpeername()[0]))
        self.socket.send(data)

    def close(self):
        print("Closing socket {0}".format(self.socket.getsockname()))
        self.socket.close()

    def getpeername(self):
        return self.socket.getpeername()


# A decorator that compresses data using gzip compression whenever send is called
class GzipSocket:

    def __init__(self, socket):
        self.socket = socket

    def send(self, data):
        buf = BytesIO()
        zipfile = gzip.GzipFile(fileobj=buf, mode='w')
        zipfile.write(data)
        zipfile.close()
        self.socket.send(buf.getvalue())

    def close(self):
        self.socket.close()
