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
        self.tick_rate = settings['tick_rate']
        self.num_clients = settings['num_clients']

settings = Settings()
