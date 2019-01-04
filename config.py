import json

class Settings(object):

    def __init__(self):
        settings = json.load(open('config.json'))
        self.client_ip = settings['client_ip']
        self.server_ip = settings['server_ip']
        self.port = settings['port']
        self.client_address = (self.client_ip, self.port)
        self.server_address = (self.server_ip, self.port)
        self.buffer_size = settings['buffer_size']
        self.encoding = settings['encoding']
        self.disconnect = settings['disconnect']
        self.timeout = settings['timeout']                  # num of seconds for the client connection to time out
        self.tick_rate = settings['tick_rate']
        self.refresh_rate = settings['refresh_rate']
        self.num_clients = settings['num_clients']          # number of connections per server

        self.num_players = settings['num_players']          # number of players per lobby
        self.missile_vel = 1 / settings['missile_vel']      # the velocity of missiles
        self.shoot_cooldown = settings['shoot_cooldown']    # cooldown in seconds for shooting
        self.move_cooldown = settings['move_cooldown']      # cooldown in seconds for moving

        self.resolution = settings['resolution']
        self.grid_size = settings['grid_size']              # number of grids wide/tall the game is
        self.tile_size = settings['tile_size']              # number of pixels wide/tall each grid is
        self.game_size = settings['grid_size'] * settings['tile_size']

    # simplistic formatting method for json strings
    @staticmethod
    def format_json(json_str):
        json_build = ''
        for char in json_str:

            if char == '}':
                json_build += '\n'

            json_build += char

            if char == '{' or char == ',':
                json_build += '\n\t'

        return json_build

settings = Settings()
