import pygame

from controller import Controller
from config import settings
from constants import Color, Font, Anchor
from label import Label
from layout import Grid

class Menu_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)

    def initialize_components(self):
        
        self.title_layout = Grid(2, 2)

        self.title_label = Label(self.interface, 'Press enter to play')
        self.title_label.loc = self.title_layout.get_pixel(2, 2)
        self.title_label.anchor = Anchor.center
        self.title_label.font = Font.menu

    def update_components(self):
        self.title_label.refresh()

    def open_on_close(self):
        from game_controller import Game_Controller
        game = Game_Controller(self.interface)
        game.run()

    # do actions based on what was pressed
    def key_actions(self):
        if self.key_presses[pygame.K_RETURN]:
            self.done = True
