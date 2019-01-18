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

class PlayerInfo(object):

    def __init__(self, player, interface):
        self.player = player
        self.id = self.player.id
        self.image = Image(self.player.path)
        self.image.scale_to(interface.tile_width, interface.tile_height)
        self.image.fill(self.player.color)

    def draw(self, display):
        self.image.loc = self.player.loc
        self.image.draw(display)

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
    def slow_down(self):
        for i in range(len(self.vel)):
            if abs(self.vel[i]) < settings.cutoff_vel:
                self.vel[i] = 0
            else:
                self.vel[i] *= settings.player_friction

    def speed_up(self, direction):
        # LRUD movement
        if direction == Dir.left:
            self.vel[0] = self.vel[0] - settings.player_vel
        elif direction == Dir.right:
            self.vel[0] = self.vel[0] + settings.player_vel
        elif direction == Dir.up:
            self.vel[1] = self.vel[1] - settings.player_vel
        elif direction == Dir.down:
            self.vel[1] = self.vel[1] + settings.player_vel

        # diagnal movement
        elif direction == Dir.up_right:
            self.vel[0] = self.vel[0] + settings.player_vel
            self.vel[1] = self.vel[1] - settings.player_vel
        elif direction == Dir.down_right:
            self.vel[0] = self.vel[0] + settings.player_vel
            self.vel[1] = self.vel[1] + settings.player_vel
        elif direction == Dir.down_left:
            self.vel[0] = self.vel[0] - settings.player_vel
            self.vel[1] = self.vel[1] + settings.player_vel
        elif direction == Dir.up_left:
            self.vel[0] = self.vel[0] - settings.player_vel
            self.vel[1] = self.vel[1] - settings.player_vel

    # move player with a bounds check
    def move(self, panel):
        x = self.loc[0]
        dx = self.vel[0]
        y = self.loc[1]
        dy = self.vel[1]

        # bounds check
        if not panel.within(x + dx, y):
            dx = 0
            self.vel[0] = 0
        if not panel.within(x, y + dy):
            dy = 0
            self.vel[1] = 0

        self.loc = (x + dx, y + dy)

class Missile(GameObject):

    def __init__(self, color=Color.green, loc=(0, 0), angle=(0., 0.)):
        GameObject.__init__(self, color=color, loc=loc, angle=angle)

        self.path = 'game/assets/missile.png'

    def move(self, panel, missiles):
        # update to next pos
        delta_x = self.angle[0] * settings.missile_vel
        delta_y = self.angle[1] * settings.missile_vel
        self.loc = (self.loc[0] + delta_x, self.loc[1] + delta_y)

        # remove if it went off the panel
        if not panel.within(self.loc[0], self.loc[1]):
            missiles.remove(self)

class MissileInfo(object):

    def __init__(self, missile, angle):
        self.missile = missile
        self.image = Image(self.missile.path)
        self.image.rotate_by(angle)
        self.image.loc = self.missile.loc
