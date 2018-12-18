import pygame, time
from collections import defaultdict

from thread import Thread
from config import settings

class Controller(object):

    def __init__(self, interface):

        self.ticking = True
        self.done = False
        self.interface = interface
        interface.clear()

        self.key_presses = defaultdict(lambda: False)
        self.tick_thread = Thread(target=self.tick, args=())

    def tick(self):
        while self.ticking:
            self.tick_actions()
            time.sleep(1 / settings.tick_rate)

    def tick_actions(self):
        pass

    def update(self):

        # clear screen before drawing
        self.interface.clear()

        # draw and update controller items
        self.update_actions()

        # pygame update
        self.interface.update()

    def update_actions(self):
        pass

    def setup(self):
        pass

    # the program will exit
    def close(self):
        self.ticking = False
        self.tick_thread.join()
        self.close_actions()
        self.interface.close()

    # the controller will be closed
    def close_actions(self):
        pass

    def run(self):

        self.setup()
        self.tick_thread.start()

        while not self.done:
            for event in pygame.event.get():
                self.handle_event(event)

            self.key_actions()
            self.update()

        self.close()

    def handle_event(self, event):

        # top right corner X
        if event.type == pygame.QUIT:
            self.done = True

        # player starts doing actions
        elif event.type == pygame.KEYDOWN:
            self.key_presses[event.key] = True

        # player stops doing actions
        elif event.type == pygame.KEYUP:
            self.key_presses[event.key] = False

    # do actions based on what was pressed
    def key_actions(self):
        pass
