import json

from sprite import Missile

# turn json string to object
def _json_object_hook(d):

    if all([key in d for key  in ['number', 'p1_loc', 'p2_loc', 'missile_buffer']]):
        return State(**d)

    elif all([key in d for key in ['color', 'loc', 'dir']]):
        return Missile(**d)

def json2obj(data):

    print('data:')
    print(data)

    try:
        obj = json.loads(data, object_hook=_json_object_hook)
    except:
        obj = None
    finally:
        return obj

class State(object):

    def __init__(self, p1_loc, p2_loc, missile_buffer, number):

        self.number = number
        self.p1_loc = p1_loc
        self.p2_loc = p2_loc
        self.missile_buffer = missile_buffer

    def set_state(self, p1_loc, p2_loc, missile_buffer):
        self.p1_loc = p1_loc
        self.p2_loc = p2_loc
        self.missile_buffer = missile_buffer

    # turns the object into a json string
    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
