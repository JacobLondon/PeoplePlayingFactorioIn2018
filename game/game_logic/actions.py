import numpy as np, time, copy, random
from threading import Thread

from game.pyngine.constants import Color, Dir

from game.game_logic.game_objects import Player, Missile
from game.game_logic.client import Client
from game.game_logic.gamestate import State, json_to_obj
from game.game_logic.vector import Vector2

from game.utils.config import settings

class Actions(object):

    def __init__(self, controller):

        self.controller = controller
        self.interface = controller.interface
        self.game_panel = controller.game_panel

        self.players = []

        # load players
        self.player = Player(id=self.controller.client.id)
        self.players.append(self.player)

        # hold the missiles until tick, then empty the buffer
        self.missiles = []
        self.missile_buffer = []

        # vector from player to mouse
        self.pm_vector = Vector2()

        # object which stores the data for the state
        self.gamestate = State(self.players, self.missile_buffer, self.controller.client.id)

        self.fire_ready = True
        self.move_ready = True
        self.paused = False
        self.receiving = False

    def setup(self):

        # set the players' positions based on game_panel
        left = self.game_panel.anchored_loc[0]
        right = self.game_panel.anchored_loc[1] + self.game_panel.width - self.interface.tile_width
        top = self.game_panel.anchored_loc[1]
        bot = self.game_panel.anchored_loc[1] + self.game_panel.height - self.interface.tile_height
        
        # randomly place the player in the game
        for player in self.players:
            player.loc = (random.randint(left, right), random.randint(top, bot))

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

    # move the player based on their velocity
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

    # give the player directional velocity
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

        # update the player mouse vector
        tail = self.player.loc
        head = (self.controller.mouse_x, self.controller.mouse_y)
        self.pm_vector.set(head, tail)

         # make a missile and put it in the missile list
        dir = (self.pm_vector.unit[0], self.pm_vector.unit[1])
        missile = Missile(dir=dir)
        missile.loc = (self.player.loc[0], self.player.loc[1])
        self.missiles.append(missile)
        self.missile_buffer.append(copy.deepcopy(missile))

        # cannot fire again until the cooldown timer is done
        self.fire_ready = False
        Thread(target=self.shoot_cooldown).start()        

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

        # update state from other clients
        if not self.gamestate.id == received_state.id:

            # load the new missiles
            for m in received_state.missile_buffer:
                self.missiles.append(m)

            # load the players
            for player in received_state.players:

                # get player from players list which matches the received player
                match = list(filter(lambda p: p.id == player.id, self.players))

                # received player is not in players list, it should be
                if not match:
                    self.players.append(player)

                # update the player to be the received player if not self player
                elif not match[0].id == self.player.id:
                    self.update_player(match[0], player)

            # players list may have a player who left the game, remove it
            # TODO
            '''for player in self.players:
                match = list(filter(lambda p: p.id == player.id, received_state.players))
                if not match:
                    self.players.remove(player)'''

    # update player with the received player
    def update_player(self, current, received):
        current.loc = received.loc
        current.vel = received.vel
        current.health = received.health

    def tick(self):
        Thread(target=self.send).start()
        Thread(target=self.receive).start()

    def update(self):
        # update and draw sprites
        self.draw_missiles()
        for player in self.players:
            self.interface.draw_sprite(player)

        self.move()
        self.player.slow()

        # set gamestate
        self.gamestate.set_state(self.players, self.missile_buffer)
