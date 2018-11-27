import json, getpass
from sprite import Player
from collections import namedtuple

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

    # turns the object into a json string
    def get_state(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    # turn json string to object
    def _json_object_hook(self, d):
        return namedtuple('X', d.keys())(*d.values())

    @staticmethod
    def json2obj(data):
        return json.loads(data, object_hook=_self.json_object_hook)

    # turn json string to binary
    @staticmethod
    def dict_to_binary(the_dict):
        str = json.dumps(the_dict)
        binary = bytes(' '.join(format(ord(letter), 'b') for letter in str), 'utf8')
        return binary

    # turn binary to json
    @staticmethod
    def binary_to_dict(the_binary):
        jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
        d = json.loads(jsn)
        return d
