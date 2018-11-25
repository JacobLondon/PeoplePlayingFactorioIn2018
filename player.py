import copy

class Player(object):

    def __init__(self, number=0, size=10, color=(0,0,255), dir=1):

        # player 1
        self.number = number
        if self.number == 0:
            self.loc = (size / 2, size)
            self.color = color

        # player 2
        elif self.number == 1:
            self.loc = (size / 2, 0)
            self.color = (255,0,0)

        # missile
        else:
            self.loc = (0, 0)
            self.color = (0,255,0)

        self.dir = dir
