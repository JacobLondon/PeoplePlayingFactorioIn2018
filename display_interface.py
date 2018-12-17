import pygame

from config import settings

class Interface(object):

    def __init__(self):

        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((settings.display_size, settings.display_size))
        pygame.display.set_caption('PPFI18')
        pygame.display.update()
        self.clock = pygame.time.Clock()

    def update(self):
        pygame.display.update()
        self.clock.tick(settings.refresh_rate)
