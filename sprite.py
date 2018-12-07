
class Sprite(object):

    def __init__(self, color=(0,0,0)):
        self.color = color
        self.loc = (0, 0)

class Player(Sprite):

    def __init__(self, number=0, gsize=10, color=(0,0,255)):

        Sprite.__init__(self, color=color)

        # player 1
        self.number = number
        if self.number == 0:
            self.loc = (gsize / 2, gsize - 1)

        # player 2
        elif self.number == 1:
            self.loc = (gsize / 2, 0)
            self.color = (255,0,0)

class Missile(Sprite):

    def __init__(self, color=(0,255,0), dir=1):

        Sprite.__init__(self, color=color)
        self.dir = dir
