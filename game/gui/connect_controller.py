from threading import Thread

from game.pyngine.controller import Controller
from game.pyngine.label import Label
from game.pyngine.button import Button
from game.pyngine.progress_bar import Bar
from game.pyngine.layout import Relative, Grid
from game.pyngine.constants import Color, Anchor, Font

from game.game_logic.client import Client

from game.utils.config import settings

class Connect_Controller(Controller):

    def __init__(self, interface, client_address):
        Controller.__init__(self, interface, settings.tick_rate)

        self.client_address = client_address

        # try to connect or timeout
        Thread(target=self.connect).start()

    def connect(self):
        self.client = Client(self.client_address)

        # connect/timeout in another thread
        Thread(target=self.client.attempt_connection).start()

        # track connection progress in this thread
        while self.client.attempting:
            self.progress_bar.increment(settings.timeout, self.client.connection_time)
        self.progress_bar.complete()

        # wait until the client is finished connecting
        while not self.client.finished:
            pass

        # load game_controller
        if self.client.success_connect:
            self.done = True
        # let user return to main menu with timeout message
        else:
            self.timeout_label.visible = True
            self.return_button.visible = True
            self.connect_label.visible = False
            self.progress_bar.visible = False

    def initialize_components(self):
        self.connect_layout = Grid(self.background_panel, 16, 16)
        self.connect_label = Label(self, 'Attempting to connect to server...')
        self.connect_label.loc = self.connect_layout.get_pixel(9, 8)
        self.connect_label.anchor = Anchor.center
        self.connect_label.font = Font.large
        self.connect_label.background = None

        self.progress_bar = Bar(self)
        self.progress_bar.loc = self.connect_layout.get_pixel(9, 9)
        self.progress_bar.anchor = Anchor.center
        self.progress_bar.font = Font.large
        self.progress_bar.width = settings.resolution[0] / 2

        # display to the user the connection has timed out
        timeout_text = 'Connection timed out.'
        self.timeout_layout = Grid(self.background_panel, 32, 32)
        self.timeout_label = Label(self, timeout_text)
        self.timeout_label.loc = self.timeout_layout.get_pixel(17, 16)
        self.timeout_label.font = Font.menu
        self.timeout_label.background = None
        self.timeout_label.anchor = Anchor.center
        self.timeout_label.visible = False

        return_text = 'Return to menu'
        self.return_button = Button(self, return_text)
        self.return_button.loc = self.timeout_layout.get_pixel(17, 19)
        self.return_button.anchor = Anchor.center
        self.return_button.visible = False
        self.return_button.action = self.return_button_clicked

    def open_on_close(self):
        # show timeout screen if connection fails
        if not self.client.success_connect:
            from .menu_controller import Menu_Controller
            menu = Menu_Controller(self.interface)
            menu.run()
        else:
            from .game_controller import Game_Controller
            game = Game_Controller(self.interface, self.client)
            game.run()

    def return_button_clicked(self):
        self.done = True