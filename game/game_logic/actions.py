import numpy as np, time, copy
from threading import Thread

from game.pyngine.constants import Color, Dir

from game.game_logic.game_objects import Player, Missile
from game.game_logic.client import Client
from game.game_logic.gamestate import State, json_to_obj

from game.utils.config import settings

class Actions(object):

    def __init__(self, controller):

        self.controller = controller
        self.interface = controller.interface
        self.game_panel = controller.game_panel

        # load players
        self.p1 = Player.create_playerone()
        self.p2 = Player.create_playertwo()

        # hold the missiles until tick, then empty the buffer
        self.missiles = []
        self.missile_buffer = []

        # unit vector from player to mouse
        self.pmouse_uvector = np.array([0., 0.])

        # object which stores the data for the state
        self.gamestate = State(self.p1, self.p2, self.missiles, self.controller.client.id)

        # the player id changes depending on client
        self.player = self.p1 if self.controller.client.id == 0 else self.p2

        self.fire_ready = True
        self.move_ready = True
        self.paused = False
        self.receiving = False

    def setup(self):

        # set the players' positions based on game_panel
        center_x = self.game_panel.anchored_loc[0] + self.game_panel.width / 2
        top_y = self.game_panel.anchored_loc[1]
        bot_y = self.game_panel.anchored_loc[1] + self.game_panel.height - self.interface.tile_height
        self.p1.loc = (center_x, bot_y)
        self.p2.loc = (center_x, top_y)

    def draw_missiles(self):
    
        # update each missile
        for m in self.missiles:

            # update to next pos
            delta_x = m.dir[0] * settings.missile_vel
            delta_y = m.dir[1] * settings.missile_vel
            m.loc = (m.loc[0] + delta_x, m.loc[1] + delta_y)

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

    def move(self):
        x = self.player.loc[0]
        dx = self.player.vel[0]
        y = self.player.loc[1]
        dy = self.player.vel[1]

        if not self.game_panel.within(x + dx, y):
            dx = 0
            self.player.vel[0] = 0
        if not self.game_panel.within(x, y + dy):
            dy = 0
            self.player.vel[1] = 0

        self.player.loc = (x + dx, y + dy)

    def add_velocity(self, direction):

        # only move if cooldown and not paused
        if not self.move_ready or self.paused:
            return

        # LRUD movement
        if direction == Dir.left:
            self.player.vel[0] = self.player.vel[0] - settings.player_vel
        elif direction == Dir.right:
            self.player.vel[0] = self.player.vel[0] + settings.player_vel
        elif direction == Dir.up:
            self.player.vel[1] = self.player.vel[1] - settings.player_vel
        elif direction == Dir.down:
            self.player.vel[1] = self.player.vel[1] + settings.player_vel

        # diagnal movement
        elif direction == Dir.up_right:
            self.player.vel[0] = self.player.vel[0] + settings.player_vel
            self.player.vel[1] = self.player.vel[1] - settings.player_vel
        elif direction == Dir.down_right:
            self.player.vel[0] = self.player.vel[0] + settings.player_vel
            self.player.vel[1] = self.player.vel[1] + settings.player_vel
        elif direction == Dir.down_left:
            self.player.vel[0] = self.player.vel[0] - settings.player_vel
            self.player.vel[1] = self.player.vel[1] + settings.player_vel
        elif direction == Dir.up_left:
            self.player.vel[0] = self.player.vel[0] - settings.player_vel
            self.player.vel[1] = self.player.vel[1] - settings.player_vel

        self.move_ready = False
        Thread(target=self.move_cooldown).start()

    def shoot(self):

        # only shoot if cooldown and not paused
        if not self.fire_ready or self.paused:
            return

        # make a missile and put it in the missile list
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
        x2 = self.controller.mouse_x
        y1 = self.player.loc[1]
        y2 = self.controller.mouse_y

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
            self.controller.client.send(self.gamestate.to_json())
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
            received_data = self.controller.client.receive()
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
        if self.controller.client.id != received_state.id:

            # load the new missiles
            for m in received_state.missile_buffer:
                self.missiles.append(m)

        # set pos of the other player
        if self.controller.client.id == 0:
            self.p2 = received_state.p2
        else:
            self.p1 = received_state.p1

    def tick(self):
        Thread(target=self.send).start()
        Thread(target=self.receive).start()

    def update(self):
        # update and draw sprites
        self.draw_missiles()
        self.interface.draw_sprite(self.p1)
        self.interface.draw_sprite(self.p2)

        self.move()
        self.player.slow()

        # set gamestate
        self.gamestate.set_state(self.p1, self.p2, self.missile_buffer)
