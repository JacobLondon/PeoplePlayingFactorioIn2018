import json
from player import Player

class State(object):

    def __init__(self, p1, p2, missiles):

        self.p1 = p1#.loc
        self.p2 = p2#.loc
        self.missiles = missiles#[for m in missiles: m.loc]
        self.state = self.create_gamestate()

    def create_gamestate(self):
        return json.dumps(self, default=lambda o: o.__dict__)
