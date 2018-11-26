import json
from player import Player

class State(object):

    def __init__(self, p1, p2, missiles):

        self.p1 = p1
        self.p2 = p2
        self.missiles = missiles
        self.gamestate = None
        self.create_gamestate()
    
    def create_gamestate(self):
        self.gamestate = json.dumps(self, default=lambda o: o.__dict__)