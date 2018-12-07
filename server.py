from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time

# server vars
address = ('', 5678)
clients = {}
addresses = {}
buffersize = 4096
tick_rate = 20
disconnect = 'QUIT'
encoding = 'utf8'

# await clients to join server
def await_clients():
    while True:

        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)

        # add client address to addresses array
        addresses[client] = client_address

        # start thread for client
        Thread(target=handle_client, args=(client,)).start()

# handle data transmission for a given client
def handle_client(client):

    message = b''

    # add new client to array of client sockets
    name = client.recv(buffersize).decode(encoding)
    clients[client] = name

    while True:

        # receive data from clients
        try:
            message = client.recv(buffersize)

        # the client forcibly disconnected
        except:
            message = bytes(disconnect, encoding)

        # check if the client wants to disconnect
        if message.decode(encoding) == disconnect:
            client.close()
            print("%s:%s has disconnected." % addresses[client])
            del clients[client]
            break

        # send data to all clients
        broadcast(message, name)
        #print(message.decode(encoding))
        time.sleep(1 / tick_rate)

# send binary data to all clients
def broadcast(message, sender):

    # send message to all other clients
    for client in clients:
        if clients[client] != sender:
            client.send(message)

# prepare server
server = socket(AF_INET, SOCK_STREAM)
server.bind(address)

# listen for maximum connections made to the socket
server.listen(2)

# handle client connections in another thread
connection_thread = Thread(target=await_clients)
connection_thread.start()
print('Server Started')

# server shutdown
connection_thread.join()
server.close()
