import time

from connection import Socket
from config import settings
from thread import Thread

class Server(object):

    def __init__(self):
        self.clients = {}
        self.addresses = {}
        self.run()

    # await clients to join server
    def await_clients(self):

        while True:
            client, client_address = self.server.accept()
            print("%s:%s has connected." % client_address)
            client.send(1)

            # add client address to addresses array
            self.addresses[client] = client_address

            # start thread for client
            Thread(target=self.handle_client, args=(client,)).start()

    # handle data transmission for a given client
    def handle_client(self, client):

        message = b''

        # add new client to array of client sockets
        name = client.receive()
        self.clients[client] = name
        connected = True

        while connected:

            # receive data from clients
            try:
                message = client.receive()

                # check if the client wants to disconnect
                if message == settings.disconnect:
                    connected = False
                    break

                # send data to all other clients
                self.broadcast(message, name)

            # the client forcibly disconnected
            except Socket.error as e:
                print("Error: " + e)
                connected = False

            time.sleep(1 / settings.tick_rate)

        client.close()
        print("%s:%s has disconnected." % self.addresses[client])
        del self.clients[client]

    # send binary data to all clients
    def broadcast(self, message, sender):

        # send message to all other clients
        for client in self.clients:
            if self.clients[client] != sender:
                client.send(message)

    def run(self):
        # prepare server
        self.server = Socket()
        self.server.listenAsServer()

        # handle client connections in another thread
        connection_thread = Thread(target=self.await_clients)
        connection_thread.start()
        print('Server Started')

        # server shutdown
        connection_thread.join()
        self.server.close()

if __name__ == '__main__':
    server = Server()
