import time
from threading import Thread

from game.utils.connection import Socket
from game.utils.config import settings

class Server(object):

    def __init__(self, run_as_thread=False):
        self.clients = {}
        self.addresses = {}
        if run_as_thread:
            Thread(target=self.run, daemon=True).start()
        else:
            self.run()

    # await clients to join server
    def await_clients(self):

        while True:
            for id in range(settings.num_players):
                client = self.server.accept()
                client_address = client.accepted_addr
                client.send(id)

                # add client address to addresses array
                self.addresses[client] = client_address

                # start thread for client
                Thread(target=self.handle_client, args=(client, id), daemon=True).start()

    # handle data transmission for a given client
    def handle_client(self, client, id):

        message = b''

        # add new client to array of client sockets
        name = client.receive()
        self.clients[client] = name
        connected = True

        try:
            while connected:
                # receive data from clients
                message = client.receive()

                # check if the client wants to disconnect
                if message == settings.disconnect:
                    connected = False
                    break

                # send data to all other clients
                self.broadcast(message, name)
                time.sleep(1 / settings.tick_rate)

        # the client forcibly disconnected
        except Socket.error as e:
            pass

        finally:
            # inform other clients who disconnected
            try:
                self.broadcast(settings.disconnect + str(id))
            except Socket.error as e:
                pass

            # stop sending data to the client
            client.close()
            del self.clients[client]

    # send binary data to all clients
    def broadcast(self, message, sender=None):
        
        # send message to all other clients
        for client in self.clients:
            if sender is None or self.clients[client] != sender:
                client.send(message)

    # prepare server
    def run(self):
        self.server = Socket()
        self.server.listen_as_server()

        # await for clients to connect
        print('Server Started')
        self.await_clients()

        # server shutdown
        self.server.close()

if __name__ == '__main__':
    server = Server()
