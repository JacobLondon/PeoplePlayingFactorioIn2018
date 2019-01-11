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
        self.missile_vel = settings['missile_vel']      # the velocity of missiles
        self.player_vel = settings['player_vel']
        self.shoot_cooldown = settings['shoot_cooldown']    # cooldown in seconds for shooting
        self.move_cooldown = settings['move_cooldown']      # cooldown in seconds for moving

        self.resolution = settings['resolution']
        self.grid_width = settings['grid_width']            # number of grids wide the game is
        self.grid_height = settings['grid_height']          # number of grid tall the game is

settings = Settings()
