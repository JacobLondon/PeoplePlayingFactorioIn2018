from socket import socket, AF_INET, SOCK_STREAM

from config import settings

class Client(object):

    def __init__(self, id):

        self.id = id

        # create and connect socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(settings.client_address)

        # give the server the client's name
        self.send(str(self.id))

    def send(self, message):
        self.socket.send(bytes(message, settings.encoding))

    def receive(self):
        message = self.socket.recv(settings.buffer_size).decode(settings.encoding)
        return message

    def close(self):
        self.socket.send(bytes(settings.disconnect, settings.encoding))
        self.socket.close()
