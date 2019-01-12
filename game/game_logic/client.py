import time
from threading import Thread

from game.utils.connection import Socket
from game.utils.config import settings

class Client(object):

    def __init__(self, client_address):

        # attempt to connect the client to the address
        self.success_connect = False
        self.timed_out = False
        connect_thread = Thread(target=self.connect, args=(client_address,))
        connect_thread.start()
        timeout_thread = Thread(target=self.wait_for_timeout)
        timeout_thread.start()

        # check to see if the connection is timing out
        while not self.timed_out and not self.success_connect:
            pass

        connect_thread.join()
        timeout_thread.join()

        # Get id from server
        if self.success_connect:
            self.id = int(self.receive())

    def wait_for_timeout(self):
        for _ in range(settings.timeout):
            time.sleep(1)
            if self.success_connect:
                return

        self.timed_out = True

    def connect(self, client_address):
        try:
            # create and connect socket
            self.socket = Socket(client_address=client_address)
            self.socket.connect_to_server()
            self.send = self.socket.send
            self.receive = self.socket.receive
            self.close = self.socket.close
            self.handshake_close = self.socket.handshake_close
            self.success_connect = True

        except ConnectionRefusedError:
            self.success_connect = False

