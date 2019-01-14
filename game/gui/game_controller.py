import pygame, time, copy, numpy as np
from threading import Thread

from game.pyngine.constants import Color, Dir, Anchor, Font
from game.pyngine.controller import Controller
from game.pyngine.label import Label
from game.pyngine.panel import Panel
from game.pyngine.layout import Relative, Grid

from game.game_logic.game_objects import Player, Missile
from game.game_logic.client import Client
from game.game_logic.gamestate import State, json_to_obj
from game.game_logic.actions import Actions

from game.utils.config import settings

class Game_Controller(Controller):

    def __init__(self, interface, client):
        Controller.__init__(self, interface, settings.tick_rate)

        self.client = client

        '''# try to connect or timeout
        self.client = Client(client_address)
        if not self.client.success_connect:
            self.done = True
            return'''

    def initialize_components(self):

        # defined by where the play takes place
        self.game_panel = Panel(self)
        self.game_panel.width = settings.resolution[0]
        self.game_panel.height = settings.resolution[1]

        # center label shows info in the center of the game panel
        self.relative_layout = Relative(self.game_panel)
        self.center_label = Label(self, 'Press esc to pause')
        self.center_label.loc = self.relative_layout.center
        self.center_label.anchor = Anchor.center

        # pause layout displays the pause menu based from the background
        self.pause_layout = Relative(self.background_panel)
        self.pause_label = Label(self, 'Paused')
        self.pause_label.loc = self.pause_layout.northeast
        self.pause_label.anchor = Anchor.northeast
        self.pause_label.font = Font.large
        self.pause_label.background = Color.pause
        self.pause_label.visible = False

    def setup(self):
        self.game_actions = Actions(self)
        self.game_actions.setup()

    def tick_actions(self):
        self.game_actions.tick()

    def update_actions(self):
        self.game_actions.update()
        self.pause_label.visible = self.game_actions.paused

    def close_actions(self):
        self.client.handshake_close()

    def open_on_close(self):

        '''# show timeout screen if connection fails
        if not self.client.success_connect:
            from .timeout_controller import Timeout_Controller
            timeout = Timeout_Controller(self.interface)
            timeout.run()
        # go to main menu
        else:'''
        from .menu_controller import Menu_Controller
        menu = Menu_Controller(self.interface)
        menu.run()

    def escape_keydown(self):
        self.game_actions.paused = not self.game_actions.paused
        self.key_presses[pygame.K_ESCAPE] = False

    def w_keydown(self):
        self.game_actions.add_velocity(Dir.up)

    def a_keydown(self):
        self.game_actions.add_velocity(Dir.left)

    def s_keydown(self):
        self.game_actions.add_velocity(Dir.down)

    def d_keydown(self):
        self.game_actions.add_velocity(Dir.right)

    def l_click_down(self):
        self.game_actions.shoot()

    def custom_key_actions(self):
        # custom key actions for moving diagnally
        if self.key_presses[pygame.K_w] and self.key_presses[pygame.K_d]:
            self.wd_keydown()
        if self.key_presses[pygame.K_s] and self.key_presses[pygame.K_d]:
            self.sd_keydown()
        if self.key_presses[pygame.K_s] and self.key_presses[pygame.K_a]:
            self.sa_keydown()
        if self.key_presses[pygame.K_w] and self.key_presses[pygame.K_a]:
            self.wa_keydown()

    # custom actions for moving diagnally
    def wd_keydown(self):
        self.game_actions.add_velocity(Dir.up_right)
    def sd_keydown(self):
        self.game_actions.add_velocity(Dir.down_right)
    def sa_keydown(self):
        self.game_actions.add_velocity(Dir.down_left)
    def wa_keydown(self):
        self.game_actions.add_velocity(Dir.up_left)
