from socket import socket, AF_INET, SOCK_STREAM
from socket import error as socket_error
from thread import Thread
import time

from config import settings

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

            # add client address to addresses array
            self.addresses[client] = client_address

            # start thread for client
            Thread(target=self.handle_client, args=(client,)).start()

    # handle data transmission for a given client
    def handle_client(self, client):

        message = b''

        # add new client to array of client sockets
        name = client.recv(settings.buffer_size).decode(settings.encoding)
        self.clients[client] = name
        connected = True

        while connected:

            # receive data from clients
            try:
                message = client.recv(settings.buffer_size)

                # check if the client wants to disconnect
                if message.decode(settings.encoding) == settings.disconnect:
                    connected = False
                    break

                # send data to all other clients
                self.broadcast(message, name)

            # the client forcibly disconnected
            except socket_error as e:
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
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(settings.server_address)

        # listen for maximum connections made to the socket
        self.server.listen(settings.num_clients)

        # handle client connections in another thread
        connection_thread = Thread(target=self.await_clients)
        connection_thread.start()
        print('Server Started')

        # server shutdown
        connection_thread.join()
        self.server.close()

if __name__ == '__main__':
    server = Server()
