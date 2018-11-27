import socket
from enum import Enum

class Type(Enum):
    SERVER = 0
    CLIENT = 1

class Connection():

    @staticmethod
    def create_server(addr=socket.gethostname(), port=5678):
        conn = socket.socket()
        conn.bind((addr, port))
        conn.listen()
        return Connection(conn, Type.SERVER)

    @staticmethod
    def create_client(addr="127.0.0.1", port=5678):
        conn = socket.socket()
        conn.connect((addr, port))
        return Connection(conn, Type.CLIENT)

    def __init__(self, connection, type):
        self.conn = connection
        self.type = type

    def send_update(self, gamestate):
        self.conn.send(gamestate)

    def get_update(self):
        return self.conn.recv(4096)

    def close(self):
        self.conn.close()
