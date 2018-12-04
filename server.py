"""Server for multithreaded encrypted chat script."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import string, time

HOST = '' # localhost
PORT = 5678

def handleNewConnection():
    """Handle a new incoming client."""
    while True:
        client, clientAddress = SERVER.accept()
        print("%s:%s has connected." % clientAddress)
        addresses[client] = clientAddress # add client address to addresses array
        Thread(target=handleClient, args=(client,)).start() # start thread for client


 # Takes client socket as argument.
def handleClient(client):
    """Handles a single client connection."""

    message = ''
    name = client.recv(BUFFERSIZE).decode("utf8")
    clients[client] = name # add new client to array of client sockets

    while True:

        if message == "{quit}":
            client.close()
            del clients[client]
            break

        message = client.recv(BUFFERSIZE) # receive messages from clients
        broadcast(message)
        print(message)
        time.sleep(1/20)


def broadcast(message):
    """Broadcasts a message to all the clients."""

    # loop through all connected sockets and send the message to them
    for sock in clients:
        sock.send(message)

print('Server Started')

clients = {}
addresses = {}

BUFFERSIZE = 4096
ADDRESS = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

SERVER.listen(2) # listen for maximum connections made to the socket
CLIENT_THREAD = Thread(target=handleNewConnection) # New thread for handling client connections
CLIENT_THREAD.start()
CLIENT_THREAD.join()
SERVER.close()
