import pygame

class Color(object):

    black = (0,0,0)
    white = (255,255,255)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)

    background = black
    foreground = white

class Dir(object):

    right = 2
    left = 3
    down = 1
    up = -1

class Font(object):
    pygame.font.init()
    arial = pygame.font.SysFont('Arial', 60)
