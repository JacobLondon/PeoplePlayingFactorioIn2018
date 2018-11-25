import socket

class Connection():

    @staticmethod
    def create_server(addr=socket.gethostname(), port=5678):
        conn = socket.socket()
        conn.bind((addr, port))
        conn.listen()
        return Connection(conn)

    @staticmethod
    def create_client(addr="127.0.0.1", port=5678):
        conn = socket.socket()
        conn.connect((addr, port))
        return Connection(conn)

    def __init__(self, connection):
        self.conn = connection

    def send_update(self, gamestate):
        self.conn.send(gamestate)

    def get_update(self):
        return self.conn.recv(4096)

    def close(self):
        self.conn.close()
