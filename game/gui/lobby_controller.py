import json, time
from threading import Thread

from game.pyngine.controller import Controller
from game.pyngine.label import Label
from game.pyngine.button import Button
from game.pyngine.textbox import Textbox
from game.pyngine.layout import Relative, Grid
from game.pyngine.constants import Color, Anchor, Font

from game.utils.config import settings

class Lobby_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)
        self.connect = False
        self.back = False
        self.client_address = settings.client_address

    def initialize_components(self):

        # info about the lobby label
        self.lobby_layout = Grid(self.background_panel, 32, 32)
        self.lobby_label = Label(self, 'Lobby')
        self.lobby_label.loc = self.lobby_layout.get_pixel(4, 3)
        self.lobby_label.anchor = Anchor.center
        self.lobby_label.font = Font.menu
        self.lobby_label.background = None

        # button to connect/join a lobby
        self.join_button = Button(self, 'Join')
        self.join_button.loc = self.lobby_layout.get_pixel(32, 30)
        self.join_button.anchor = Anchor.northeast
        self.join_button.action = self.join_button_clicked

        # button to go back to the main menu
        self.back_button = Button(self, 'Back')
        self.back_button.loc = self.lobby_layout.get_pixel(2, 30)
        self.back_button.action = self.back_button_clicked

        # textbox to enter the ip address to connect to
        self.ip_textbox = Textbox(self)
        self.ip_textbox.loc = self.lobby_layout.get_pixel(3, 5)
        self.ip_textbox.anchor = Anchor.northwest
        self.ip_textbox.text = settings.client_ip

        # button to connect to a server
        self.connect_button = Button(self, 'Connect')
        self.connect_button.loc = self.lobby_layout.get_pixel(3, 7)
        self.connect_button.width = self.ip_textbox.width

        # get most recent lobby data from server
        self.refresh_button = Button(self, 'Refresh')
        self.refresh_button.loc = self.lobby_layout.get_pixel(3, 10)
        self.refresh_button.width = self.ip_textbox.width

    def open_on_close(self):

        if self.connect:
            from .connect_controller import Connect_Controller
            connection = Connect_Controller(self.interface, self.client_address)
            connection.run()
        elif self.back:
            from .menu_controller import Menu_Controller
            menu = Menu_Controller(self.interface)
            menu.run()

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
