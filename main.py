import sys

from controller import Controller
from sprite import Player
from config import settings

def main():

    # make a server/client interface depending on args
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        client_id = 1
    else:
        client_id = 0

    game = Controller()
    game.run()

if __name__ == '__main__':
    main()
