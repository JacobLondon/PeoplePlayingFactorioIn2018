import sys
from display import Controller
from player import Player
from network_interface import Connection

square = 20    # size of each pixel
gsize = 40     # number of grids wide/tall the game is
cooldown = 0.1 # wait time between shots

# server main
def s_main():

        #server = Connection.create_server()

        p1 = Player(gsize=gsize)
        p2 = Player(number=1, gsize=gsize)

        game = Controller(square=square, size=gsize, p1=p1, p2=p2, connection=None, cooldown=cooldown)
        game.run()

# client main
def c_main():

        #client = Connection.create_client()

        p1 = Player(gsize=gsize)
        p2 = Player(number=1, gsize=gsize)
        p1.color, p2.color = p2.color, p1.color

        game = Controller(square=square, size=gsize, p1=p1, p2=p2, connection=None, cooldown=cooldown)
        game.run()

if __name__ == '__main__':

        if len(sys.argv) > 1 and sys.argv[1].lower() == 'c':
                c_main()
        else:
                s_main()
