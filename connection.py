from socket import socket as socket_socket
from socket import AF_INET, SOCK_STREAM
from socket import error as socket_error
from select import select

from config import settings

class Socket():
    error = socket_error

    def __init__(self, socket=None, client_address=settings.client_address):
        if socket is None:
            self.socket = socket_socket(AF_INET, SOCK_STREAM)
        else:
            self.socket = socket

        self.client_address = client_address

    def connect_to_server(self):
        self.socket.connect(self.client_address)

    def listen_as_server(self):
        self.socket.bind(settings.server_address)
        self.socket.listen(settings.num_clients)

    def send(self, message):
        self.socket.send(bytes(str(message), settings.encoding))

    def receive(self):
        recv = self.socket.recv(settings.buffer_size).decode(settings.encoding)
        return recv

    def handshake_close(self):
        self.send(settings.disconnect)
        self.close()

    def close(self):
        self.socket.close()

    def accept(self):
        self.socket.setblocking(0)
        while not select((self.socket,), (), (), 0.5)[0]:
            pass
        self.socket.setblocking(1)
        conn, addr = self.socket.accept()
        return Socket(conn), addr

'''
port = 8880
import select
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.bind(("", port))
s.listen(1)
while 1:
    ready = select.select((s,), (), (), 0.5)
    #print '(ready %s)' % repr(ready)
    if (ready[0]):
        try:
            endpoint = s.accept()
        except socket.error, details:
            print 'Ignoring socket error:', repr(details)
            continue
        print '(endpoint %s)' % repr(endpoint)
        if endpoint:
            break
'''
