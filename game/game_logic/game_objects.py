
from game.pyngine.constants import Color, Dir

from game.utils.config import settings

class GameObject(object):

    def __init__(self, color=Color.black, loc=(0, 0)):
        self.color = color
        self.loc = loc

class Player(GameObject):

    def __init__(self, color=Color.blue, loc=(0,0)):
        super().__init__(self, color=color, loc=loc)

    @staticmethod
    def create_playerone():
        player = Player()
        player.color = Color.red
        player.loc = (settings.grid_size / 2, settings.grid_size - 1)
        return player

    @staticmethod
    def create_playertwo():
        player = Player()
        player.color = Color.blue
        player.loc = (settings.grid_size / 2, 0)
        return player

class Missile(GameObject):

    def __init__(self, color=Color.green, loc=(0, 0), dir=Dir.down):
        super().__init__(self, color=color, loc=loc)
        self.dir = dir
