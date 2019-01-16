from game.pyngine.constants import Color, Font, Anchor
from game.pyngine.label import Label
from game.pyngine.button import Button
from game.pyngine.layout import Grid
from game.pyngine.controller import Controller
from game.pyngine.image import Image

from game.utils.config import settings

import pygame

class Menu_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)

    def initialize_surfaces(self):
        self.logo_layout = Grid(self.background_panel, 8, 8)
        self.logo = Image('game/assets/ppfi2018.png')
        self.logo.loc = self.logo_layout.get_pixel(5, 4)
        self.logo.anchor = Anchor.center
        self.logo.set_anchor()

    def initialize_components(self):

        self.title_layout = Grid(self.background_panel, 8, 8)

        self.start_button = Button(self, 'Multiplayer')
        self.start_button.loc = self.title_layout.get_pixel(5, 6)
        self.start_button.anchor = Anchor.center
        self.start_button.action = self.start_button_clicked

        self.quit_button = Button(self, 'Quit')
        self.quit_button.loc = self.title_layout.get_pixel(5, 7)
        self.quit_button.anchor = Anchor.center
        self.quit_button.width = self.start_button.width
        self.quit_button.action = self.quit_button_clicked

    def open_on_close(self):
        from .lobby_controller import Lobby_Controller
        lobby = Lobby_Controller(self.interface)
        lobby.run()

    def start_button_clicked(self):
        self.done = True

    def quit_button_clicked(self):
        self.done = True
        self.quit = True
        
    def draw_foreground(self):
        self.logo.draw(self.interface.display)
