import random

from game.pyngine.constants import Color, Dir
from game.pyngine.screen_object import ScreenObject
from game.pyngine.image import Image

from game.utils.config import settings

class GameObject(ScreenObject):

    def __init__(self, color=None, loc=(0, 0), angle=(0., 0.)):
        ScreenObject.__init__(self)
        self.color = color
        self.loc = loc

        self.path = None
        self.angle = angle

class Player(GameObject):

    def __init__(self, id=0, color=None, loc=(0, 0), vel=[0., 0.], health=0, angle=(0., 0.)):
        GameObject.__init__(self, color=color, loc=loc, angle=angle)
        self.id = id
        self.vel = vel
        self.health = health
        if self.color is None:
            self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.path = 'game/assets/player.png'

    # reduce the velocity by the friction amount
    def slow(self):
        for i in range(len(self.vel)):
            if abs(self.vel[i]) < settings.cutoff_vel:
                self.vel[i] = 0
            else:
                self.vel[i] *= settings.player_friction

class Missile(GameObject):

    def __init__(self, color=Color.green, loc=(0, 0), angle=(0., 0.)):
        GameObject.__init__(self, color=color, loc=loc, angle=angle)

        self.path = 'game/assets/missile.png'
