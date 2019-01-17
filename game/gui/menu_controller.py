from game.pyngine.constants import Color, Font, Anchor
from game.pyngine.label import Label
from game.pyngine.button import Button
from game.pyngine.layout import Grid
from game.pyngine.controller import Controller
from game.pyngine.imagebox import Imagebox

from game.utils.config import settings

import pygame

class MenuController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)        

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

        self.logo_imagebox = Imagebox(self, 'game/assets/ppfi2018.png')
        self.logo_imagebox.loc = self.title_layout.get_pixel(5, 4)
        self.logo_imagebox.anchor = Anchor.center

    def open_on_close(self):
        from .lobby_controller import LobbyController
        lobby = LobbyController(self.interface)
        lobby.run()

    def start_button_clicked(self):
        self.done = True

    def quit_button_clicked(self):
        self.done = True
        self.quit = True
    
