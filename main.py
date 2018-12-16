import sys

from controller import Controller
from sprite import Player

square = 20    # size of each pixel
gsize = 40     # number of grids wide/tall the game is
cooldown = 0.1 # seconds between shots

# server main
def main():

    # make a server/client interface depending on args
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        client_id = 1
    else:
        client_id = 0

    p1 = Player(gsize=gsize)
    p2 = Player(id=1, gsize=gsize)
    #p1 = create_playerone(gsize)
    #p2 = create_playertwo(gsize)

    game = Controller(square, gsize, p1, p2, client_id, cooldown)
    game.run()

if __name__ == '__main__':
    main()
