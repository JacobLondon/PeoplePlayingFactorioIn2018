import pygame, time, copy, sys

from pyngine.constants import Color, Dir, Anchor, Font
from pyngine.controller import Controller
from pyngine.label import Label
from pyngine.panel import Panel
from pyngine.layout import Relative, Grid

from thread import Thread
from sprite import Player, Missile
from client import Client
from gamestate import State, json_to_obj
from config import settings

class Game_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, settings.tick_rate)

        # try to connect
        try:
            self.client = Client()
        except ConnectionRefusedError:
            self.done = True
            return

        # load players
        self.p1 = Player.create_playerone()
        self.p2 = Player.create_playertwo()

        # hold the missiles until tick, then empty the buffer
        self.missiles = []
        self.missile_buffer = []

        # object which stores the data for the state
        self.gamestate = State(self.p1, self.p2, self.missiles, self.client.id)

        # the player id changes depending on client
        self.player = self.p1 if self.client.id == 0 else self.p2

        self.fire_ready = True
        self.move_ready = True
        self.paused = False

    def initialize_components(self):

        # defined by where the play takes place
        self.game_panel = Panel(self.background_panel)
        self.game_panel.width = settings.game_size
        self.game_panel.height = settings.game_size

        # center label shows info in the center of the game panel
        self.relative_layout = Relative(self.game_panel)
        self.center_label = Label(self.interface, 'Press esc to pause')
        self.center_label.loc = self.relative_layout.center
        self.center_label.anchor = Anchor.center

        # pause layout displays the pause menu based from the background
        self.pause_layout = Relative(self.background_panel)
        self.pause_label = Label(self.interface, 'Paused')
        self.pause_label.loc = self.pause_layout.northeast
        self.pause_label.anchor = Anchor.northeast
        self.pause_label.font = Font.large
        self.pause_label.background = Color.pause
        self.pause_label.visible = False

    def load_components(self):
        self.center_label.load()
        self.pause_label.load()

    def update_components(self):
        self.center_label.refresh()
        self.pause_label.visible = self.paused
        self.pause_label.refresh()

    def draw_missiles(self):

        # update each missile
        for m in self.missiles:

            # update to next pos
            m.loc = (m.loc[0], m.loc[1] + m.dir / settings.missile_vel)

            # remove if it went off the screen
            if m.loc[1] < 0 or m.loc[1] > settings.grid_size:
                self.missiles.remove(m)
                continue

            self.interface.draw_sprite(m)


    def move_cooldown(self):
        time.sleep(settings.move_cooldown)
        self.move_ready = True

    def shoot_cooldown(self):
        time.sleep(settings.shoot_cooldown)
        self.fire_ready = True

    def move(self, direction, player):

        # only move if cooldown and not paused
        if not self.move_ready or self.paused:
            return

        # move left and bounds check
        if direction == Dir.left:
            if 0 <= player.loc[0] - 1:
                player.loc = (player.loc[0] - 1, player.loc[1])

        # move right and bounds check
        elif direction == Dir.right:
            if player.loc[0] + 1 < settings.grid_size:
                self.player.loc = (player.loc[0] + 1, player.loc[1])

        self.move_ready = False
        Thread(target=self.move_cooldown, args=()).start()

    def shoot(self, dir):

        # onlly shoot if cooldown and not paused
        if not self.fire_ready or self.paused:
            return

        # make a missile player and put it in the missile list
        missile = Missile(dir=dir)
        missile.loc = (self.player.loc[0], self.player.loc[1])
        self.missiles.append(missile)
        self.missile_buffer.append(copy.deepcopy(missile))

        # cannot fire again until the cooldown timer is done
        self.fire_ready = False
        Thread(target=self.shoot_cooldown, args=()).start()

    def send(self):

        # send gamestate as a json
        try:
            self.client.send(self.gamestate.to_json())
        # the host was forcibly closed, end the program
        except:
            self.done = True
            return

        # empty the buffer because it will have been sent
        self.missile_buffer = []

    def receive(self):

        try:
            received_data = self.client.receive()
        # the host was forcibly closed, end the program
        except:
            self.done = True
            return

        # convert json to object if there is data
        received_state = json_to_obj(received_data)
        if received_state is None:
            return

        # player cannot receive their own missiles
        if self.client.id != received_state.id:

            # load the new missiles
            for m in received_state.missile_buffer:
                self.missiles.append(m)

        # set pos of the other player
        if self.client.id == 0:
            self.p2 = received_state.p2
        else:
            self.p1 = received_state.p1

    def tick_actions(self):
        Thread(target=self.send, args=()).start()
        Thread(target=self.receive, args=()).start()

    def update_actions(self):

        # update and draw sprites
        self.draw_missiles()
        self.interface.draw_sprite(self.p1)
        self.interface.draw_sprite(self.p2)

        # set gamestate
        self.gamestate.set_state(self.p1, self.p2, self.missile_buffer)

    def close_actions(self):
        self.client.handshake_close()

    def open_on_close(self):
        from menu_controller import Menu_Controller
        return Menu_Controller(self.interface)

    def escape_keydown(self):
        self.paused = not self.paused
        self.key_presses[pygame.K_ESCAPE] = False

    def left_keydown(self):
        self.move(Dir.left, self.player)

    def right_keydown(self):
        self.move(Dir.right, self.player)

    def up_keydown(self):
        self.shoot(Dir.up)

    def down_keydown(self):
        self.shoot(Dir.down)
