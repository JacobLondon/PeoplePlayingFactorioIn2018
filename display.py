import pygame, numpy as np, time, threading
from player import Player
from network_interface import Connection
from gamestate import State
from enum import Enum

class Dir(Enum):
    RIGHT = 0
    LEFT = 1

class Controller(object):

    """
    @param square: size of each tile in pixels
    @param size: number of squares wide the screen is
    """
    def __init__(self, square, size, p1, p2, connection, cooldown):

        self.square = square
        self.size = square * size
        self.BLACK = (0,0,0)

        # pygame tools
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption('PPFI18')
        pygame.display.update()

        self.clock = pygame.time.Clock()
        self.refresh_rate = 60
        self.tick_rate = 20
        self.ticking = True
        self.done = False

        # load players and fix p1 offset
        self.p1 = p1
        self.p1.loc = (self.p1.loc[0], self.p1.loc[1] - 1)
        self.p2 = p2
        self.missiles = []
        self.gamestate = State(self.p1, self.p2, self.missiles)
        self.cooldown = cooldown
        self.fire_ready = True

    def draw_tile(self, x, y, color):

        # [left, top, width, height]
        pygame.draw.rect(self.display, color, \
            [self.square * x, self.square * y, self.square, self.square])

    def draw_player(self, player):

        self.draw_tile(player.loc[0], player.loc[1], player.color)

    def draw_missiles(self):

        # update each missile
        for m in self.missiles:

            # remove the previous missile square
            self.draw_tile(m.loc[0], m.loc[1], self.BLACK)

            # update to next pos
            m.loc = (m.loc[0], m.loc[1] + m.dir)

            # remove if it went off the screen
            if m.loc[1] < 0 or m.loc[1] > self.size:
                self.missiles.remove(m)
                continue

            self.draw_player(m)

    def move(self, direction, player):
        if direction == Dir.LEFT:
            if 0 <= player.loc[0] - 1:
                self.draw_tile(player.loc[0], player.loc[1], self.BLACK)
                player.loc = (player.loc[0] - 1, player.loc[1])
        elif direction == Dir.RIGHT:
            if player.loc[0] + 1 < self.size / self.square:
                self.draw_tile(player.loc[0], player.loc[1], self.BLACK)
                self.p1.loc = (player.loc[0] + 1, player.loc[1])

    def reload(self):
        time.sleep(self.cooldown)
        self.fire_ready = True

    def shoot(self):

        # make a missile player and put it in the missile list
        if self.fire_ready:
            missile = Player(number=3, gsize=self.size/self.square, dir=-1)
            missile.loc = (self.p1.loc[0], self.p1.loc[1] + missile.dir)
            self.missiles.append(missile)

            # cannot fire again until the cooldown timer is done
            self.fire_ready = False
            t = threading.Thread(target=self.reload, args=())
            t.start()

    def create_gamestate(self):
        self.gamestate.state = self.gamestate.create_gamestate()

    def tick(self):
        while self.ticking:
            c = threading.Thread(target=self.create_gamestate, args=())
            c.start()
            time.sleep(1 / self.tick_rate)
            c.join()

    def update(self):

        # update players
        t = threading.Thread(target=self.draw_missiles, args=())
        t.start()
        self.draw_player(self.p1)
        self.draw_player(self.p2)

        # set gamestate
        self.gamestate.p1 = self.p1
        self.gamestate.p2 = self.p2
        self.gamestate.missiles = self.missiles

        #print(threading.active_count())

        pygame.display.update()
        self.clock.tick(self.refresh_rate)

    def run(self):

        tick_thread = threading.Thread(target=self.tick, args=())
        tick_thread.start()

        # program loop
        while not self.done:

            # traverse all events occurring that frame
            for event in pygame.event.get():

                # top right corner X
                if event.type == pygame.QUIT:
                    self.done = True

                #  player moves left
                if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
                    t = threading.Thread(target=self.move, args=(Dir.LEFT, self.p1))
                    t.start()
                    break

                #  player moves right
                elif pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
                    t = threading.Thread(target=self.move, args=(Dir.RIGHT, self.p1))
                    t.start()
                    break

                # player shoots
                elif pygame.key.get_pressed()[pygame.K_UP] != 0:
                    t = threading.Thread(target=self.shoot, args=())
                    t.start()
                    break

            # update screen/tick clock
            self.update()

        self.ticking = False
        tick_thread.join()
        pygame.quit()
