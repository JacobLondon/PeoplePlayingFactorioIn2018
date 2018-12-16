from enum import Enum

class Color(object):

    def __init__(self):
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.blue = (0,0,255)
        self.green = (0,255,0)

class Dir(object):

    def __init__(self):
        self.right = 2
        self.left = 3
        self.down = 1
        self.up = -1

color = Color()
dir = Dir()
