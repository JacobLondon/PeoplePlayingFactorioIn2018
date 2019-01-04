import pygame

from pyngine.constants import Color, Font

class Interface(object):

    def __init__(self, window_text, resolution, grid_width, grid_height, refresh_rate):

        # pygame tools
        pygame.init()
        pygame.font.init()
        self.resolution = resolution
        self.tile_width = resolution[0] / grid_width
        self.tile_height = resolution[1] / grid_height
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
        area = [self.tile_width * x, self.tile_height * y,
                self.tile_width, self.tile_height]
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
