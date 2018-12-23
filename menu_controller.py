import pygame

from controller import Controller
from config import settings
from constants import Color, Font, Anchor, Mouse
from label import Label
from button import Button
from layout import Grid

class Menu_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)

    def initialize_components(self):

        self.title_layout = Grid(4, 4)

        self.title_label = Label(self.interface, 'Press enter to play')
        self.title_label.loc = self.title_layout.get_pixel(3, 3)
        self.title_label.anchor = Anchor.center
        self.title_label.font = Font.menu

        self.start_button = Button(self.interface, 'Click to play')
        self.start_button.loc = self.title_layout.get_pixel(3, 4)
        self.start_button.anchor = Anchor.center

    def update_components(self):
        self.title_label.refresh()
        self.start_button.refresh(self.mouse_x, self.mouse_y)

    def open_on_close(self):
        from game_controller import Game_Controller
        return Game_Controller(self.interface)

    # do actions based on what was pressed
    def key_actions(self):
        if self.key_presses[pygame.K_RETURN]:
            self.done = True

    def mouse_actions(self):
        if self.mouse_presses[Mouse.l_click] and self.start_button.focused:
            self.start_button_clicked()

    def start_button_clicked(self):
        self.done = True
