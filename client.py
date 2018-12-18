from connection import Socket
from config import settings

class Client(object):

    def __init__(self):

        # create and connect socket
        self.socket = Socket()
        self.socket.connect_to_server()
        self.send = self.socket.send
        self.receive = self.socket.receive
        self.close = self.socket.close

        # Get id from server
        self.id = int(self.receive())

    '''
    def send(self, message):
        self.socket.send(message)

    def receive(self):
        return self.socket.receive()

    def close(self):
        self.socket.close()
    '''
