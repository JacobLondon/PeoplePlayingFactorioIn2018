import json
from sprite import Player

class State(object):

    def __init__(self, p1, p2, missile_buffer):

        self.p1_loc = p1.loc
        self.p2_loc = p2.loc
        self.missile_buffer = missile_buffer
        self.state = None

    def set_state(self, p1, p2, missile_buffer):
        self.p1_loc = p1.loc
        self.p2_loc = p2.loc
        self.missile_buffer = missile_buffer

    def get_state(self):
        return json.dumps(self, default=lambda o: o.__dict__)
