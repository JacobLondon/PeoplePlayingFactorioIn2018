from socket import socket, AF_INET, SOCK_STREAM

from config import settings

# local connect
#addr = '127.0.0.1'
#addr = '70.95.45.63'
#port = 5678
#address = (addr, port)
#buffersize = 4096

#encoding = 'utf8'
#disconnect = 'QUIT'

class Client(object):

    def __init__(self, number):

        self.number = str(number)

        # create and connect socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(settings.client_address)

        # give the server the client's name
        self.send(self.number)

    def send(self, message):
        self.socket.send(bytes(message, settings.encoding))

    def receive(self):
        message = self.socket.recv(settings.buffer_size).decode(settings.encoding)
        return message

    def close(self):
        self.socket.send(bytes(settings.disconnect, settings.encoding))
        self.socket.close()
