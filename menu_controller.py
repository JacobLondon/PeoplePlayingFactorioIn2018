import pygame, copy

from pyngine.constants import Color, Font, Anchor
from pyngine.label import Label
from pyngine.button import Button
from pyngine.layout import Grid
from pyngine.controller import Controller

from config import settings

class Menu_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)

    def initialize_components(self):

        self.title_layout = Grid(self.background_panel, 8, 8)

        self.title_label = Label(self.interface, 'Press enter to play')
        self.title_label.loc = self.title_layout.get_pixel(5, 5)
        self.title_label.anchor = Anchor.center
        self.title_label.font = Font.menu

        self.start_button = Button(self.interface, 'Click to play')
        self.start_button.loc = self.title_layout.get_pixel(5, 6)
        self.start_button.anchor = Anchor.center

        self.quit_button = Button(self.interface, 'Quit')
        self.quit_button.loc = self.title_layout.get_pixel(5, 7)
        self.quit_button.anchor = Anchor.center
        self.quit_button.width = self.start_button.width

    def load_components(self):
        self.title_label.load()
        self.start_button.load()
        self.quit_button.load()

    def update_components(self):
        self.title_label.refresh()
        self.start_button.refresh()
        self.quit_button.refresh()

    def open_on_close(self):
        from lobby_controller import Lobby_Controller
        return Lobby_Controller(self.interface)

    def return_keydown(self):
        self.start_button_clicked()

    def l_click_down(self):
        if self.start_button.focused:
            self.start_button_clicked()
        elif self.quit_button.focused:
            self.quit_button_clicked()

    def start_button_clicked(self):
        self.done = True

    def quit_button_clicked(self):
        self.done = True
        self.quit = True
