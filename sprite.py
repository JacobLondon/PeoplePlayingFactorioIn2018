
from constants import color, dir
from config import settings

class Sprite(object):

    def __init__(self, color=color.black, loc=(0, 0)):
        self.color = color
        self.loc = loc

class Player(Sprite):

    def __init__(self, number=0):
        Sprite.__init__(self, color=color)
        self.number = number

    @staticmethod
    def create_playerone():
        player = Player()
        player.number = 0
        player.color = color.red
        player.loc = (settings.grid_size / 2, settings.grid_size - 1)
        return player

    @staticmethod
    def create_playertwo():
        player = Player()
        player.number = 1
        player.color = color.blue
        player.loc = (settings.grid_size / 2, 0)
        return player

class Missile(Sprite):

    def __init__(self, color=color.green, loc=(0, 0), dir=dir.down):
        Sprite.__init__(self, color=color, loc=loc)
        self.dir = dir
