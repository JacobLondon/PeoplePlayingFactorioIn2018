import time
from threading import Thread

from game.utils.connection import Socket
from game.utils.config import settings

class Client(object):

    def __init__(self, client_address):

        self.client_address = client_address

        # measuring/controlling timeout
        self.connection_time = 0.
        self.success_connect = False
        self.timed_out = False
        self.attempting = True
        self.finished = False

    def attempt_connection(self):
        # attempt to connect the client to the address
        connect_thread = Thread(target=self.connect, daemon=True)
        connect_thread.start()
        timeout_thread = Thread(target=self.wait_for_timeout, daemon=True)
        timeout_thread.start()

        # attempt to connect until connection or failure
        while not self.timed_out and not self.success_connect:
            pass
        self.attempting = False

        connect_thread.join()
        timeout_thread.join()

        # Get id from server
        if self.success_connect:
            self.id = int(self.receive())

        self.finished = True

    # count until connection
    def wait_for_timeout(self):
        self.connection_time = 0.
        while self.connection_time < settings.timeout:
            time.sleep(settings.timeout_increment)
            self.connection_time += settings.timeout_increment
            if self.success_connect:
                return

        self.timed_out = True

    def connect(self):
        try:
            # create and connect socket
            self.socket = Socket(client_address=self.client_address)
            self.socket.connect_to_server()
            self.send = self.socket.send
            self.receive = self.socket.receive
            self.close = self.socket.close
            self.handshake_close = self.socket.handshake_close
            self.success_connect = True

        except ConnectionRefusedError:
            self.success_connect = False

