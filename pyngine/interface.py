import pygame

from pyngine.constants import Color, Font

class Interface(object):

    def __init__(self, window_text, resolution, tile_size, refresh_rate):

        # pygame tools
        pygame.init()
        pygame.font.init()
        self.resolution = resolution
        self.tile_size = tile_size
        self.refresh_rate = refresh_rate
        self.display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(window_text)
        pygame.display.update()
        self.clock = pygame.time.Clock()

    def close(self):
        pygame.quit()

    # call to update the screen
    def update(self):
        pygame.display.update()
        self.clock.tick(self.refresh_rate)

    # draw a tile defined in config
    def draw_tile(self, x, y, color):
        area = [self.tile_size * x, self.tile_size * y,
                self.tile_size, self.tile_size]
        pygame.draw.rect(self.display, color, area)

    # draw a sprite on a tile
    def draw_sprite(self, sprite):
        self.draw_tile(sprite.loc[0], sprite.loc[1], sprite.color)

    # draw a given area
    def draw_area(self, x, y, width, height, color):
        area = [x, y, width, height]
        pygame.draw.rect(self.display, color, area)

    # set the screen to background color
    def clear(self):
        area = [0, 0, self.resolution[0], self.resolution[1]]
        pygame.draw.rect(self.display, Color.background, area)
