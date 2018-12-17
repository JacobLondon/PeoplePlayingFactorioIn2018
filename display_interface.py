import pygame

from config import settings
from constants import Color

class Interface(object):

    def __init__(self):

        # pygame tools
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((settings.display_size, settings.display_size))
        pygame.display.set_caption('PPFI18')
        pygame.display.update()
        self.clock = pygame.time.Clock()

    # call to update the screen
    def update(self):
        pygame.display.update()
        self.clock.tick(settings.refresh_rate)

    # draw a tile defined in config
    def draw_tile(self, x, y, color):
        area = [settings.square_size * x, settings.square_size * y,
                settings.square_size, settings.square_size]
        pygame.draw.rect(self.display, color, area)

    # draw a sprite on a tile
    def draw_sprite(self, sprite):
        self.draw_tile(sprite.loc[0], sprite.loc[1], sprite.color)

    # set the screen to background color
    def clear(self):
        area = [0, 0, settings.display_size, settings.display_size]
        pygame.draw.rect(self.display, Color.background, area)
