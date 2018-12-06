import sys
from game_controller import Controller
from sprite import Player

square = 20    # size of each pixel
gsize = 40     # number of grids wide/tall the game is
cooldown = 0.1 # seconds between shots

# server main
def main():

    # make a server/client interface depending on args
    if len(sys.argv) > 1 and sys.argv[1] == '2':
        client_num = 1
    else:
        client_num = 0

    p1 = Player(gsize=gsize)
    p2 = Player(number=1, gsize=gsize)

    game = Controller(square, gsize, p1, p2, client_num, cooldown)
    game.run()

if __name__ == '__main__':
    main()
