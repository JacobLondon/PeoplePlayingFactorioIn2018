import json, time

from pyngine.controller import Controller
from pyngine.label import Label
from pyngine.button import Button
from pyngine.textbox import Textbox
from pyngine.layout import Relative, Grid
from pyngine.constants import Color, Anchor, Font

from ..config import settings
from ..thread import Thread

class Lobby_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)
        self.connect = False
        self.back = False
        self.client_address = settings.client_address

    def initialize_components(self):

        # info about the lobby label
        self.lobby_layout = Grid(self.background_panel, 32, 32)
        self.lobby_label = Label(self.interface, 'Lobby')
        self.lobby_label.loc = self.lobby_layout.get_pixel(4, 3)
        self.lobby_label.anchor = Anchor.center
        self.lobby_label.font = Font.menu
        self.lobby_label.background = None

        # button to connect/join a lobby
        self.join_button = Button(self.interface, 'Connect')
        self.join_button.loc = self.lobby_layout.get_pixel(25, 30)

        # button to go back to the main menu
        self.back_button = Button(self.interface, 'Back')
        self.back_button.loc = self.lobby_layout.get_pixel(2, 30)

        # textbox to enter the ip address to connect to
        self.ip_textbox = Textbox(self.interface)
        self.ip_textbox.loc = self.lobby_layout.get_pixel(17, 15)
        self.ip_textbox.anchor = Anchor.center
        self.ip_textbox.text = settings.client_ip

    def load_components(self):
        self.background_panel.load()
        self.lobby_label.load()
        self.join_button.load()
        self.back_button.load()
        self.ip_textbox.load()

    def update_components(self):
        self.background_panel.refresh()
        self.lobby_label.refresh()
        self.join_button.refresh()
        self.back_button.refresh()
        self.ip_textbox.refresh()

    def open_on_close(self):

        if self.connect:
            from .game_controller import Game_Controller
            game = Game_Controller(self.interface, self.client_address)
            game.run()
        elif self.back:
            from .menu_controller import Menu_Controller
            menu = Menu_Controller(self.interface)
            menu.run()

    def l_click_down(self):
        if self.join_button.focused:
            self.join_button_clicked()
        elif self.back_button.focused:
            self.back_button_clicked()
        elif self.ip_textbox.focused and not self.typing:
            Thread(target=self.ip_textbox_input, args=()).start()
        elif self.background_panel.focused:
            self.background_panel_clicked()

    def background_panel_clicked(self):
        self.typing = False

    def join_button_clicked(self):
        self.done = True
        self.connect = True

        # change the client ip to what is given
        config = json.load(open('config.json', 'r'))
        config['client_ip'] = self.ip_textbox.text
        self.client_address = (self.ip_textbox.text, self.client_address[1])
        json.dump(config, open('config.json', 'w'), indent=4, separators=(',', ': '))

    def back_button_clicked(self):
        self.done = True
        self.back = True

    def ip_textbox_input(self):
        self.typing = True
        self.typed_text = self.ip_textbox.text
        while self.typing:
            self.ip_textbox.text = self.typed_text
            self.ip_textbox.load()
            time.sleep(1 / settings.refresh_rate)

    def close_actions(self):

        # make sure no input is still being read while in another controller
        self.typing = False
