import pygame

from controller import Controller
from config import settings
from constants import Font, Color
from layout import Grid
from label import Label

class Pause_Controller(Controller):

    def __init__(self, interface, game_ref):
        Controller.__init__(self, interface, False)
        self.game_ref = game_ref

    def initialize_components(self):

        self.pause_layout = Grid(8, 8)

        self.pause_label = Label(self.interface, 'Paused')
        self.pause_label.loc = self.pause_layout.get_pixel(8, 1)
        self.pause_label.font = Font.large

        self.pause_label.background = Color.pause

    def update_components(self):
        self.pause_label.refresh()

    def clear(self):
        self.interface.draw_area(
            self.pause_label.loc[0],
            self.pause_label.loc[1],
            self.pause_layout.width,
            settings.display_size,
            Color.pause)

    def open_on_close(self):
        #from game_controller import Game_Controller
        #return Game_Controller(self.interface, self.game_ref)
        from menu_controller import Menu_Controller
        return Menu_Controller(self.interface)

    def key_actions(self):
        if self.key_presses[pygame.K_ESCAPE]:
            self.done = True
