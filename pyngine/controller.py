import pygame, time, threading
from collections import defaultdict

from thread import Thread

from pyngine.constants import Mouse
from pyngine.panel import Panel

class Controller(object):

    def __init__(self, interface, tick_rate=1, clear=True):

        self.tick_rate = tick_rate
        self.ticking = True     # ticking separate from framerate
        self.done = False       # controller looping
        self.quit = False       # close and return controller
        self.typing = False     # user is typing text
        self.typed_text = ''    # the text the user is typing

        self.interface = interface
        if clear:
            interface.clear()

        self.key_presses = defaultdict(lambda: False)
        self.mouse_presses = defaultdict(lambda: False)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        self.tick_thread = Thread(target=self.tick, args=())

        # create an empty panel for components to be on
        self.background_panel = Panel(self.interface)
        self.background_panel.width = interface.resolution[0]
        self.background_panel.height = interface.resolution[1]

    def initialize_components(self):
        pass

    def load_components(self):
        pass

    # thread handling ticking
    def tick(self):
        while self.ticking:
            print(threading.active_count())
            self.tick_actions()
            time.sleep(1 / self.tick_rate)

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
        else:
            self.open_on_close()

    # the controller will be closed
    def close_actions(self):
        pass

    # give the controller to run when the current one closes
    def open_on_close(self):

        # by default, close the program
        self.interface.close()

    def run(self):

        # the connection failed before running
        if self.done:
            self.open_on_close()

        self.initialize_components()
        self.load_components()
        self.load_components()
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

        # control user text input
        if self.typing and event.type == pygame.KEYDOWN:
            if self.key_presses[pygame.K_BACKSPACE]:
                self.typed_text = self.typed_text[:-1]
            elif self.key_presses[pygame.K_SPACE]:
                self.typed_text += ' '
            else:
                self.typed_text += pygame.key.name(event.key)

        # mouse starts clicking/scrolling
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_presses[event.button] = True

        # mouse stops clicking/scrolling
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_presses[event.button] = False

        # mouse moves
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    # actions for components
    def component_actions(self):
        pass

    def mouse_actions(self):
        if self.mouse_presses[Mouse.l_click]:
            self.l_click_down()
        if self.mouse_presses[Mouse.m_click]:
            self.m_click_down()
        if self.mouse_presses[Mouse.r_click]:
            self.r_click_down()
        if self.mouse_presses[Mouse.scroll_up]:
            self.scroll_up()
        if self.mouse_presses[Mouse.scroll_down]:
            self.scroll_down()

    def l_click_down(self):
        pass
    def m_click_down(self):
        pass
    def r_click_down(self):
        pass
    def scroll_up(self):
        pass
    def scroll_down(self):
        pass

    # do actions based on what was pressed
    def key_actions(self):
        if self.key_presses[pygame.K_RETURN]:
            self.return_keydown()
        if self.key_presses[pygame.K_ESCAPE]:
            self.escape_keydown()
        if self.key_presses[pygame.K_LEFT]:
            self.left_keydown()
        if self.key_presses[pygame.K_RIGHT]:
            self.right_keydown()
        if self.key_presses[pygame.K_UP]:
            self.up_keydown()
        if self.key_presses[pygame.K_DOWN]:
            self.down_keydown()

    def return_keydown(self):
        pass
    def escape_keydown(self):
        pass
    def left_keydown(self):
        pass
    def right_keydown(self):
        pass
    def up_keydown(self):
        pass
    def down_keydown(self):
        pass

    def background_panel_clicked(self):
        self.typing = False
