
class Sprite(object):

    def __init__(self, color=(0,0,0), loc=(0, 0)):
        self.color = color
        self.loc = loc

class Player(Sprite):

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

    def __init__(self, color=(0,255,0), loc=(0, 0), dir=1):

        Sprite.__init__(self, color=color, loc=loc)
        self.dir = dir
