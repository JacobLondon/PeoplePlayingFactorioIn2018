import pygame, time
from collections import defaultdict

from thread import Thread
from config import settings

class Controller(object):

    def __init__(self, interface, clear=True):

        self.ticking = True
        self.done = False
        self.quit = False
        self.interface = interface
        if clear:
            interface.clear()

        self.key_presses = defaultdict(lambda: False)
        self.mouse_presses = defaultdict(lambda: False)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        self.tick_thread = Thread(target=self.tick, args=())
        self.initialize_components()

    def initialize_components(self):
        pass

    # thread handling ticking
    def tick(self):
        while self.ticking:
            self.tick_actions()
            time.sleep(1 / settings.tick_rate)

    # custom actions during tick
    def tick_actions(self):
        pass

    def clear(self):
        self.interface.clear()

    # do on every frame
    def update(self):

        # clear screen before drawing
        self.clear()
        self.draw_background()

        # custom component updates
        self.update_components()

        # draw and update controller items
        self.update_actions()

        # pygame update
        self.interface.update()

    # draw things behind all items
    def draw_background(self):
        pass

    # refresh/update components
    def update_components(self):
        pass

    # custom actions during update
    def update_actions(self):
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
            return None
        else:
            return self.open_on_close()

    # the controller will be closed
    def close_actions(self):
        pass

    # give the controller to run when the current one closes
    def open_on_close(self):

        # by default, close the program
        self.interface.close()
        return None

    def run(self):

        self.setup()
        self.tick_thread.start()

        # game loop for controller
        while not self.done:
            for event in pygame.event.get():
                self.handle_event(event)

            self.key_actions()
            self.mouse_actions()
            self.component_actions()
            Thread(target=self.update, args=()).start()

        return self.close()

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

        # mouse starts clicking/scrolling
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_presses[event.button] = True

        # mouse stops clicking/scrolling
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_presses[event.button] = False

        # mouse moves
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    # do actions based on what was pressed
    def key_actions(self):
        pass

    def mouse_actions(self):
        pass

    # actions for components
    def component_actions(self):
        pass
