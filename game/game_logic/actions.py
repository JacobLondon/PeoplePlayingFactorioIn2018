import numpy as np, time, copy, random, re, pygame
from threading import Thread

from game.pyngine.constants import Color, Dir
from game.pyngine.image import Image

from game.game_logic.game_objects import Player, PlayerInfo, Missile, MissileInfo
from game.game_logic.client import Client
from game.game_logic.gamestate import State, json_to_obj
from game.game_logic.game_connection import GameConnection
from game.game_logic.vector import Vector2

from game.utils.config import settings

class Actions(object):

    def __init__(self, controller):

        self.controller = controller
        self.interface = controller.interface
        self.game_panel = controller.game_panel

        # send/receive game data to/from the server
        self.connection = GameConnection(self, controller)

        self.player_infos = []

        # load players
        self.player = Player(id=self.controller.client.id)
        self.load_player(self.player)

        # hold the missiles until tick, then empty the buffer
        self.missiles = []
        self.missile_buffer = []

        # vector from player to mouse
        self.pm_vector = Vector2()

        # object which stores the data for the state
        self.gamestate = State([], self.missile_buffer, self.controller.client.id)

        self.fire_ready = True
        self.move_ready = True
        self.paused = False

    def setup(self):

        # set the players' positions based on game_panel
        left = self.game_panel.anchored_loc[0]
        right = self.game_panel.anchored_loc[1] + self.game_panel.width - self.interface.tile_width
        top = self.game_panel.anchored_loc[1]
        bot = self.game_panel.anchored_loc[1] + self.game_panel.height - self.interface.tile_height
        
        # randomly place the player in the game
        self.player.loc = (random.randint(left, right), random.randint(top, bot))

    def move_cooldown(self):
        time.sleep(settings.move_cooldown)
        self.move_ready = True

    def shoot_cooldown(self):
        time.sleep(settings.shoot_cooldown)
        self.fire_ready = True

    # give the player directional velocity
    def add_vel(self, direction):

        # only move if cooldown and not paused
        if not self.move_ready or self.paused:
            return

        self.player.speed_up(direction)

        self.move_ready = False
        Thread(target=self.move_cooldown).start()

    def shoot(self):

        # only shoot if cooldown and not paused
        if not self.fire_ready or self.paused:
            return

         # make a missile and put it in the missile list
        angle = (self.pm_vector.unit[0] + self.player.vel[0], self.pm_vector.unit[1] + self.player.vel[1])
        missile = Missile(angle=angle)

        # spawn the missile away from the player
        startx = self.player.loc[0] + self.interface.tile_width*angle[0]
        starty = self.player.loc[1] + self.interface.tile_height*angle[1]
        missile.loc = (startx, starty)
            
        self.missiles.append(missile)
        self.missile_buffer.append(copy.deepcopy(missile))

        # cannot fire again until the cooldown timer is done
        self.fire_ready = False
        Thread(target=self.shoot_cooldown).start()        


    def tick(self):
        Thread(target=self.connection.send).start()
        Thread(target=self.connection.receive).start()

    def update(self):
        # update and draw sprites
        self.player.move(self.game_panel)
        self.player.slow_down()

        # update the player mouse vector
        tail = self.player.loc
        # correct for top left corner
        x = self.controller.mouse_x - self.interface.tile_width / 2
        y = self.controller.mouse_y - self.interface.tile_height / 2
        head = (x, y)
        self.pm_vector.set(head, tail)

        # set gamestate
        players = [p.player for p in self.player_infos]
        self.gamestate.set_state(players, self.missile_buffer)

    def draw(self):

        self.draw_missiles()

        for player_info in self.player_infos:
            #self.interface.draw_sprite(player)
            player_info.draw(self.interface.display)

    # update each missile
    def draw_missiles(self):
        for m in self.missiles:
            m.move(self.game_panel, self.missiles)
            self.interface.draw_sprite(m)
        
    # give a player, and a corresponding PlayerInfo is created and added
    def load_player(self, player):
        self.player_infos.append(PlayerInfo(player, self.interface))