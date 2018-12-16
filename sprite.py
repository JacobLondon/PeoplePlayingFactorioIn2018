
from constants import color, dir
from config import settings

class Sprite(object):

    def __init__(self, color=color.black, loc=(0, 0)):
        self.color = color
        self.loc = loc

class Player(Sprite):

<<<<<<< HEAD
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
=======
    def __init__(self, id=0, gsize=10, color=(0,0,255)):

        Sprite.__init__(self, color=color)

        # player 1
        self.id = id
        if self.id == 0:
            self.loc = (gsize / 2, gsize - 1)

        # player 2
        elif self.id == 1:
            self.loc = (gsize / 2, 0)
            self.color = (255,0,0)
>>>>>>> 350c8818f60d1cf76ed75d82d528dedcd7f06c0e

    @staticmethod
    def create_playerone(gsize):
        player = Player()
        player.id = 0
        player.color = (0,0,255)
        player.loc = (gsize / 2, gsize - 1)
        return player

    @staticmethod
    def create_playertwo(gsize):
        player = Player()
        player.id = 1
        player.color = (255, 0, 0)
        player.loc = (gisze / 2, 0)
        return player

class Missile(Sprite):

    def __init__(self, color=color.green, loc=(0, 0), dir=dir.down):
        Sprite.__init__(self, color=color, loc=loc)
        self.dir = dir
