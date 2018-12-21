import pygame, time, copy, sys

from thread import Thread
from sprite import Player, Missile
from client import Client
from gamestate import State, json_to_obj
from config import settings
from constants import Color, Dir, Anchor
from controller import Controller
from label import Label
from layout import Relative

class Game_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)
        self.client = Client()

        # load players
        self.p1 = Player.create_playerone()
        self.p2 = Player.create_playertwo()

        # the player id changes depending on client
        self.player = self.p1 if self.client.id == 0 else self.p2

        # hold the missiles until tick, then empty the buffer
        self.missiles = []
        self.missile_buffer = []

        # object which stores the data for the state
        self.gamestate = State(self.p1, self.p2, self.missiles, self.client.id)
        self.fire_ready = True
        self.move_ready = True

    def initialize_components(self):

        self.title_label = Label(self.interface, 'Press esc to stop')
        self.title_label.loc = Relative.center
        self.title_label.anchor = Anchor.center

    def update_components(self):
        self.title_label.refresh()

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

        if not self.move_ready:
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

        # make a missile player and put it in the missile list
        if self.fire_ready:
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
        menu = Menu_Controller(self.interface)
        menu.run()

    # do actions based on what was pressed
    def key_actions(self):
        if self.key_presses[pygame.K_LEFT]:
            self.move(Dir.left, self.player)

        if self.key_presses[pygame.K_RIGHT]:
            self.move(Dir.right, self.player)

        if self.key_presses[pygame.K_UP]:
            self.shoot(Dir.up)

        if self.key_presses[pygame.K_DOWN]:
            self.shoot(Dir.down)

        if self.key_presses[pygame.K_ESCAPE]:
            self.done = True
