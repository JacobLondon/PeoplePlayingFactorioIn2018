import pygame

class Color(object):

    black = (0,0,0)
    dark_gray = (80,80,80)
    light_gray = (160,160,160)
    white = (255,255,255)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)

    background = black
    foreground = white

    pause = (67, 85, 123)

    button = (130,130,130)
    hover = (200,200,255)

class Dir(object):

    right = 2
    left = 3
    down = 1
    up = -1

class Font(object):
    pygame.font.init()
    standard = pygame.font.SysFont('Sans MS', 20)
    large = pygame.font.SysFont('Sans MS', 40)
    menu = pygame.font.SysFont('Sans MS', 60)
    button = pygame.font.SysFont('Sans MS', 40)

class Anchor(object):
    northwest = 0
    northeast = 1
    southeast = 2
    southwest = 3
    center = 4

class Mouse(object):
    l_click = 1
    m_click = 2
    r_click = 3
    scroll_up = 4
    scroll_down = 5
