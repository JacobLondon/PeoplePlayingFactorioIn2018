import json

from sprite import Missile, Player

# turn json string to object
def _json_object_hook(d):

    if all([key in d for key  in ['number', 'p1', 'p2', 'missile_buffer']]):
        #print(d)
        return State(**d)

    elif all([key in d for key in ['color', 'loc', 'dir']]):
        return Missile(**d)

    elif all([key in d for key in ['color', 'loc']]):
        #print("Player", d)
        return Player(**d)

def json_to_obj(data):

    print(data)
    try:
        obj = json.loads(data, object_hook=_json_object_hook)
    except:
        obj = None
    finally:
        return obj

class State(object):

    def __init__(self, p1, p2, missile_buffer, id):
        self.id = id
        self.p1 = p1
        self.p2 = p2
        self.missile_buffer = missile_buffer

    def set_state(self, p1, p2, missile_buffer):
        self.p1 = p1
        self.p2 = p2
        self.missile_buffer = missile_buffer

    # turns the object into a json string
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
