from game.pyngine.constants import Color, Font, Anchor
from game.pyngine.label import Label
from game.pyngine.button import Button
from game.pyngine.layout import Grid
from game.pyngine.controller import Controller

from game.utils.config import settings

class Menu_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)

    def initialize_components(self):

        self.title_layout = Grid(self.background_panel, 8, 8)

        self.title_label = Label(self, 'People Playing Factorio in 2018')
        self.title_label.loc = self.title_layout.get_pixel(5, 5)
        self.title_label.anchor = Anchor.center
        self.title_label.font = Font.menu

        self.start_button = Button(self, 'Multiplayer')
        self.start_button.loc = self.title_layout.get_pixel(5, 6)
        self.start_button.anchor = Anchor.center

        self.quit_button = Button(self, 'Quit')
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
        from .lobby_controller import Lobby_Controller
        lobby = Lobby_Controller(self.interface)
        lobby.run()

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
