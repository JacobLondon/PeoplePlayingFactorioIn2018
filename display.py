import pygame, numpy as np, time
from player import Player
from network_interface import Connection
from enum import Enum

class Controller(object):

    """
    @param square: size of each tile in pixels
    @param size: number of squares wide the screen is
    """
    def __init__(self, square, size):

        self.square = square
        self.size = square * size

        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption('PPFI18')
        self.clock = pygame.time.Clock()

        self.refresh_rate = 60

        self.missiles = []
        self.done = False

        self.BLACK = (0,0,0)

        pygame.display.update()

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

    def run(self, p1, p2):

        p1.loc = (p1.loc[0], p1.loc[1] - 1)
        self.draw_player(p1)
        pygame.display.update()

        # program loop
        while not self.done:

            # traverse all events occurring that frame
            for event in pygame.event.get():

                # top right corner X
                if event.type == pygame.QUIT:
                    self.done = True

                #  player moves left + bounds check
                if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
                    if 0 <= p1.loc[0] - 1:
                        self.draw_tile(p1.loc[0], p1.loc[1], self.BLACK)
                        p1.loc = (p1.loc[0] - 1, p1.loc[1])
                        self.draw_player(p1)

                #  player moves right + bounds check
                if pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
                    if p1.loc[0] + 1 < self.size / self.square:
                        self.draw_tile(p1.loc[0], p1.loc[1], self.BLACK)
                        p1.loc = (p1.loc[0] + 1, p1.loc[1])
                        self.draw_player(p1)

                # player shoots
                if pygame.key.get_pressed()[pygame.K_UP] != 0:
                    missile = Player(number=3, size=self.size/self.square, dir=-1)
                    missile.loc = (p1.loc[0], p1.loc[1] + missile.dir)
                    self.missiles.append(missile)

            # end of for loop
            self.draw_missiles()

            # loop controls
            pygame.display.update()
            self.clock.tick(self.refresh_rate)

        pygame.quit()
