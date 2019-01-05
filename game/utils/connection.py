from socket import socket as socket_socket
from socket import AF_INET, SOCK_STREAM
from socket import error as socket_error
from select import select

from .config import settings

class Socket():
    error = socket_error

    def __init__(self, socket=None, client_address=settings.client_address, accepted_addr=None):
        self.closed = False
        self.accepted_addr = accepted_addr
        if not accepted_addr is None:
            print("%s: %s has connected." % accepted_addr)
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
        self.closed = True
        if not self.accepted_addr is None:
            print("%s: %s has disconnected." % self.accepted_addr)
        self.socket.close()

    def has_input(self):
        ret = select((self.socket,), (), (), 0.5)
        return ret[0] == [self.socket]

    def wait_for_input(self):
        has_input = True
        while has_input:
            has_input = not self.has_input()
            print("Waiting %s" % has_input)

    def accept(self):
        self.wait_for_input()
        conn, addr = self.socket.accept()
        return Socket(socket=conn, accepted_addr=addr)

    def check_closed(self):
        if self.has_input():
            if self.receive() == settings.disconnect:
                self.close()
                return True
        return False
