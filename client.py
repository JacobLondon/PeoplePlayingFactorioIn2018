from socket import socket, AF_INET, SOCK_STREAM

# address according to host IP and port
address = ('127.0.0.1', 5678)
buffersize = 4096
encoding = 'utf8'
disconnect = 'QUIT'

class Client(object):

    def __init__(self, number):

        self.number = str(number)

        # create and connect socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(address)

        # give the server the client's name
        self.send(self.number)


    def send(self, message):
        self.socket.send(bytes(message, encoding))

    def receive(self):
        message = self.socket.recv(buffersize).decode(encoding)
        return message

    def close(self):
        self.socket.send(bytes(disconnect, encoding))
        self.socket.close()
