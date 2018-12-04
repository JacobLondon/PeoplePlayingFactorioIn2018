import json, getpass
from sprite import Player
from collections import namedtuple

# turn json string to object
def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

class State(object):

    def __init__(self, p1, p2, missile_buffer, number):

        self.number = number
        self.p1_loc = p1.loc
        self.p2_loc = p2.loc
        self.missile_buffer = missile_buffer
        #self.state = None

    def set_state(self, p1, p2, missile_buffer):
        self.p1_loc = p1.loc
        self.p2_loc = p2.loc
        self.missile_buffer = missile_buffer

    # turns the object into a json string
    def get_state(self):
        return json.dumps(self, default=lambda o: o.__dict__)
