from game.utils.connection import Socket
from game.utils.config import settings

class Client(object):

    def __init__(self, client_address):

        # create and connect socket
        self.socket = Socket(client_address=client_address)
        self.socket.connect_to_server()
        self.send = self.socket.send
        self.receive = self.socket.receive
        self.close = self.socket.close
        self.handshake_close = self.socket.handshake_close

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
