from socket import socket as socket_socket
from socket import AF_INET, SOCK_STREAM
from socket import error as socket_error

from config import settings

class Socket():
    error = socket_error

    def __init__(self, socket=None):
        if socket is None:
            self.socket = socket_socket(AF_INET, SOCK_STREAM)
        else:
            self.socket = socket

    def connect_to_server(self):
        self.socket.connect(settings.client_address)

    def listen_as_server(self):
        self.socket.bind(settings.server_address)
        self.socket.listen(settings.num_clients)

    def send(self, message):
        print("sending %s" % message)
        self.socket.send(bytes(str(message), settings.encoding))

    def receive(self):
        recv = self.socket.recv(settings.buffer_size).decode(settings.encoding)
        print("recving %s" % recv)
        return recv

    def handshake_close(self):
        self.send(settings.disconnect)
        self.close()

    def close(self):
        self.socket.close()

    def accept(self):
        conn, addr = self.socket.accept()
        return Socket(conn), addr
