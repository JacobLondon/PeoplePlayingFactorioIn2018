import random

from game.pyngine.constants import Color, Dir

from game.utils.config import settings

class GameObject(object):

    def __init__(self, color=Color.black, loc=(0, 0)):
        self.color = color
        self.loc = loc

class Player(GameObject):

    def __init__(self, id=0, color=Color.blue, loc=(0, 0), vel=[0., 0.], health=0):
        GameObject.__init__(self, color=color, loc=loc)
        self.id = id
        self.vel = vel
        self.health = health
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    # reduce the velocity by the friction amount
    def slow(self):
        for i in range(len(self.vel)):
            if abs(self.vel[i]) < settings.cutoff_vel:
                self.vel[i] = 0
            else:
                self.vel[i] *= settings.player_friction

class Missile(GameObject):

    def __init__(self, color=Color.green, loc=(0, 0), dir=(0., 0.)):
        GameObject.__init__(self, color=color, loc=loc)
        self.dir = dir
