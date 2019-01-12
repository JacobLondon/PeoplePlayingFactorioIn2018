from game.pyngine.controller import Controller
from game.pyngine.label import Label
from game.pyngine.button import Button
from game.pyngine.layout import Relative, Grid
from game.pyngine.constants import Color, Anchor, Font

from game.utils.config import settings

class Timeout_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)

    def initialize_components(self):

        # display to the user the connection has timed out
        timeout_text = 'Connection timed out.'
        self.timeout_layout = Grid(self.background_panel, 32, 32)
        self.timeout_label = Label(self, timeout_text)
        self.timeout_label.loc = self.timeout_layout.get_pixel(17, 16)
        self.timeout_label.font = Font.menu
        self.timeout_label.background = None
        self.timeout_label.anchor = Anchor.center

        return_text = 'Return to menu'
        self.return_button = Button(self, return_text)
        self.return_button.loc = self.timeout_layout.get_pixel(17, 19)
        self.return_button.anchor = Anchor.center

    def open_on_close(self):
        from .menu_controller import Menu_Controller
        menu = Menu_Controller(self.interface)
        menu.run()

    def l_click_down(self):
        if self.return_button.focused:
            self.return_button_clicked()

    def return_button_clicked(self):
        self.done = True
