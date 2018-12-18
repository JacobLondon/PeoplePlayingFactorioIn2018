
from game_controller import Game_Controller
from sprite import Player
from config import settings
from display_interface import Interface

def main():

    interface = Interface('PPFI18')

    game = Game_Controller(interface)
    game.run()

if __name__ == '__main__':
    main()
