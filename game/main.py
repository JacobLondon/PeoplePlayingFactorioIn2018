import sys

from game.pyngine.interface import Interface

from game.gui import Menu, Lobby

from game.utils.config import settings

def main():

    args = sys.argv
    nargs = len(args)

    inter_args = ['PPFI18', tuple(settings.resolution), settings.grid_width,
        settings.grid_height, settings.refresh_rate]


    interface = Interface(*inter_args)
    
    if nargs == 1:
        controller = Menu(interface)

    elif nargs == 2:
        if args[1].lower() == 'lobby':
            controller = Lobby(interface)

        else:
            print('Invalid args')
            return

    # run the first controller
    controller.run()

if __name__ == '__main__':
    main()
