import json

from game.game_logic.game_objects import Missile, Player
from game.game_logic.vector import Vector2

# turn json string to object
def _json_object_hook(d):

    if all([key in d for key  in ['id', 'players', 'missile_buffer']]):
        return State(**d)

    elif all([key in d for key in ['color', 'loc', 'dir']]):
        return Missile(**d)

    elif all([key in d for key in ['id', 'color', 'loc', 'health']]):
        return Player(**d)

    elif all([key in d for key in ['head', 'tail', 'angle', 'mag', 'unit']]):
        return Vector2(**d)

def json_to_obj(data):
    try:
        obj = json.loads(data, object_hook=_json_object_hook)
    except:
        obj = None
    finally:
        return obj

class State(object):

    def __init__(self, player, players, missile_buffer, id):
        self.id = id
        self.player = player
        self.players = players
        self.missile_buffer = missile_buffer

    def set_state(self, player, players, missile_buffer):
        self.player = player
        self.players = players
        self.missile_buffer = missile_buffer

    # turns the object into a json string
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
