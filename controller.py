import pygame, time
from collections import defaultdict

from thread import Thread
from config import settings

class Controller(object):

    def __init__(self, interface):

        self.ticking = True
        self.done = False
        self.quit = False
        self.interface = interface
        interface.clear()

        self.key_presses = defaultdict(lambda: False)
        self.tick_thread = Thread(target=self.tick, args=())

    # thread handling ticking
    def tick(self):
        while self.ticking:
            self.tick_actions()
            time.sleep(1 / settings.tick_rate)

    # custom actions during tick
    def tick_actions(self):
        pass

    # do on every frame
    def update(self):

        # clear screen before drawing
        self.interface.clear()
        self.draw_background()

        # draw and update controller items
        self.update_actions()

        # pygame update
        self.interface.update()

    # custom actions during update
    def update_actions(self):
        pass

    def draw_background(self):
        pass

    # do before the game loop
    def setup(self):
        pass

    # the program will exit
    def close(self):
        self.ticking = False
        self.tick_thread.join()
        self.close_actions()

        # shutdown the program or open the parent container
        if self.quit:
            self.interface.close()
        else:
            self.open()

    # the controller will be closed
    def close_actions(self):
        pass

    # give the controller to run when the current closes
    def open(self):

        # by default, close the program
        self.interface.close()

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
            self.quit = True

        # player starts doing actions
        elif event.type == pygame.KEYDOWN:
            self.key_presses[event.key] = True

        # player stops doing actions
        elif event.type == pygame.KEYUP:
            self.key_presses[event.key] = False

    # do actions based on what was pressed
    def key_actions(self):
        pass
