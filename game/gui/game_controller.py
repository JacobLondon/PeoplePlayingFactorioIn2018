import pygame, time, copy, numpy as np
from threading import Thread

from game.pyngine.constants import Color, Dir, Anchor, Font
from game.pyngine.controller import Controller
from game.pyngine.label import Label
from game.pyngine.button import Button
from game.pyngine.panel import Panel
from game.pyngine.listbox import Listbox
from game.pyngine.layout import Relative, Grid

from game.game_logic.game_objects import Player, Missile
from game.game_logic.client import Client
from game.game_logic.gamestate import State, json_to_obj
from game.game_logic.actions import Actions

from game.utils.config import settings

class GameController(Controller):

    def __init__(self, interface, client):
        Controller.__init__(self, interface, settings.tick_rate)

        self.client = client

    def initialize_components(self):

        # defined by where the play takes place
        self.game_panel = Panel(self, in_foreground=False)
        self.game_panel.width = settings.resolution[0]
        self.game_panel.height = settings.resolution[1]

        # center label shows info in the center of the game panel
        self.relative_layout = Relative(self.game_panel)
        self.center_label = Label(self, 'Press esc to pause', in_foreground=False)
        self.center_label.loc = self.relative_layout.center
        self.center_label.anchor = Anchor.center

        # pause layout displays the pause menu based from the background
        self.pause_layout = Relative(self.game_panel)
        self.pause_listbox = Listbox(self)
        self.pause_listbox.loc = self.pause_layout.northeast
        self.pause_listbox.anchor = Anchor.northeast
        self.pause_listbox.font = Font.large
        self.pause_listbox.background = Color.pause
        self.pause_listbox.visible = False
        self.pause_listbox.width = self.game_panel.width / 5
        self.pause_listbox.height = self.game_panel.height

        # put buttons w/ their actions in the listbox
        self.menu_button = Button(self, 'Menu')
        self.menu_button.action = self.stop
        self.unpause_button = Button(self, 'Close')
        self.unpause_button.action = self.escape_keydown
        self.pause_listbox.add(self.menu_button)
        self.pause_listbox.add(self.unpause_button)

    def setup(self):
        self.game_actions = Actions(self)
        self.game_actions.setup()

    def tick_actions(self):
        self.game_actions.tick()

    def update_actions(self):
        self.game_actions.update()
        self.pause_listbox.visible = self.game_actions.paused

    def draw_midground(self):
        self.game_actions.draw()

    def close_actions(self):
        self.client.handshake_close()

    def open_on_close(self):
        from .menu_controller import MenuController
        menu = MenuController(self.interface)
        menu.run()

    def escape_keydown(self):
        self.game_actions.paused = not self.game_actions.paused
        self.key_presses[pygame.K_ESCAPE] = False

    def w_keydown(self):
        self.game_actions.add_vel(Dir.up)

    def a_keydown(self):
        self.game_actions.add_vel(Dir.left)

    def s_keydown(self):
        self.game_actions.add_vel(Dir.down)

    def d_keydown(self):
        self.game_actions.add_vel(Dir.right)

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
        self.game_actions.add_vel(Dir.up_right)
    def sd_keydown(self):
        self.game_actions.add_vel(Dir.down_right)
    def sa_keydown(self):
        self.game_actions.add_vel(Dir.down_left)
    def wa_keydown(self):
        self.game_actions.add_vel(Dir.up_left)
