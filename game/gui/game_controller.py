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

from game.utils.config import settings

class Game_Controller(Controller):

    def __init__(self, interface, client_address):
        Controller.__init__(self, interface, settings.tick_rate)

        # attempt to connect the client to the address
        self.success_connect = False
        self.timed_out = False
        connect_thread = Thread(target=self.connect, args=(client_address,))
        connect_thread.start()
        timeout_thread = Thread(target=self.wait_for_timeout)
        timeout_thread.start()
        # check to see if the connection is timing out
        while not self.timed_out and not self.success_connect:
            pass
        # if the client fails to connect
        if not self.success_connect:
            self.done = True
            return

        connect_thread.join()
        timeout_thread.join()

        # load players
        self.p1 = Player.create_playerone()
        self.p2 = Player.create_playertwo()

        # hold the missiles until tick, then empty the buffer
        self.missiles = []
        self.missile_buffer = []

        # unit vector from player to mouse
        self.pmouse_uvector = np.array([0., 0.])

        # object which stores the data for the state
        self.gamestate = State(self.p1, self.p2, self.missiles, self.client.id)

        # the player id changes depending on client
        self.player = self.p1 if self.client.id == 0 else self.p2

        self.fire_ready = True
        self.move_ready = True
        self.paused = False
        self.receiving = False

    def wait_for_timeout(self):
        for _ in range(settings.timeout):
            time.sleep(1)
            if self.success_connect:
                return

        self.timed_out = True

    def connect(self, client_address):
        try:
            self.client = Client(client_address)
            self.success_connect = True
        except ConnectionRefusedError:
            self.success_connect = False

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

    def load_components(self):
        self.game_panel.load()
        self.center_label.load()
        self.pause_label.load()

    def update_components(self):
        self.center_label.refresh()
        self.pause_label.visible = self.paused
        self.pause_label.refresh()

    def setup(self):

        # set the players' positions based on game_panel
        center_x = self.game_panel.anchored_loc[0] + self.game_panel.width / 2
        top_y = self.game_panel.anchored_loc[1]
        bot_y = self.game_panel.anchored_loc[1] + self.game_panel.height - settings.grid_height
        self.p1.loc = (center_x, bot_y)
        self.p2.loc = (center_x, top_y)

    def draw_missiles(self):

        # update each missile
        for m in self.missiles:

            # update to next pos
            delta_x = m.dir[0] * settings.missile_vel
            delta_y = m.dir[1] * settings.missile_vel
            m.loc = (m.loc[0] + delta_x, m.loc[1] + delta_y)

            top = self.game_panel.anchored_loc[1]
            bottom = self.game_panel.anchored_loc[1] + self.game_panel.height

            # remove if it went off the game panel
            if not self.game_panel.within(m.loc[0], m.loc[1]):
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
            if self.game_panel.within(player.loc[0] - settings.player_vel, player.loc[1]):
                self.player.loc = (player.loc[0] - settings.player_vel, player.loc[1])

        # move right and bounds check
        elif direction == Dir.right:
            if self.game_panel.within(player.loc[0] + settings.player_vel, player.loc[1]):
                self.player.loc = (player.loc[0] + settings.player_vel, player.loc[1])

        if direction == Dir.up:
            if self.game_panel.within(player.loc[0], player.loc[1] - settings.player_vel):
                self.player.loc = (player.loc[0], player.loc[1] - settings.player_vel)
        elif direction == Dir.down:
            if self.game_panel.within(player.loc[0], player.loc[1] + settings.player_vel):
                self.player.loc = (player.loc[0], player.loc[1] + settings.player_vel)

        self.move_ready = False
        Thread(target=self.move_cooldown).start()

    def shoot(self):

        # onlly shoot if cooldown and not paused
        if not self.fire_ready or self.paused:
            return

        # make a missile player and put it in the missile list
        self.update_pmouse_uvector()
        dir = (self.pmouse_uvector[0], self.pmouse_uvector[1])
        missile = Missile(dir=dir)
        missile.loc = (self.player.loc[0], self.player.loc[1])
        self.missiles.append(missile)
        self.missile_buffer.append(copy.deepcopy(missile))

        # cannot fire again until the cooldown timer is done
        self.fire_ready = False
        Thread(target=self.shoot_cooldown).start()

    def update_pmouse_uvector(self):
        x1 = self.player.loc[0]
        x2 = self.mouse_x
        y1 = self.player.loc[1]
        y2 = self.mouse_y

        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)

        left = x2 < x1
        up = y2 < y1

        dir = np.arctan2(delta_y, delta_x)
        self.pmouse_uvector[0] = np.cos(dir)
        self.pmouse_uvector[1] = np.sin(dir)
        if left: self.pmouse_uvector[0] *= -1
        if up: self.pmouse_uvector[1] *= -1

    def send(self):

        # send gamestate as a json
        try:
            self.client.send(self.gamestate.to_json())
        # the host was forcibly closed, end the program
        except Exception as e:
            print('failed to send')
            print(e)
            self.done = True
            return

        # empty the buffer because it will have been sent
        self.missile_buffer = []

    def receive(self):

        # do not try to receive more if there is nothing to receive
        if self.receiving:
            return

        self.receiving = True
        try:
            received_data = self.client.receive()
        # the host was forcibly closed, end the program
        except Exception as e:
            print('failed to receive')
            print(e)
            self.done = True
            self.receiving = False
            return
        finally:
            self.receiving = False

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
        Thread(target=self.send).start()
        Thread(target=self.receive).start()

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

        # show timeout screen if connection fails
        if not self.success_connect:
            from .timeout_controller import Timeout_Controller
            timeout = Timeout_Controller(self.interface)
            timeout.run()
        # go to main menu
        else:
            from .menu_controller import Menu_Controller
            menu = Menu_Controller(self.interface)
            menu.run()

    def escape_keydown(self):
        self.paused = not self.paused
        self.key_presses[pygame.K_ESCAPE] = False

    def w_keydown(self):
        self.move(Dir.up, self.player)

    def a_keydown(self):
        self.move(Dir.left, self.player)

    def s_keydown(self):
        self.move(Dir.down, self.player)

    def d_keydown(self):
        self.move(Dir.right, self.player)

    def l_click_down(self):
        self.shoot()
