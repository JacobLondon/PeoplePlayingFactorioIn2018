from game.pyngine.interface import Interface

from game.gui import Menu

from game.utils.config import settings

def main():

    inter_args = ['PPFI18', tuple(settings.resolution), settings.grid_width,
        settings.grid_height, settings.refresh_rate]

    interface = Interface(*inter_args)
    controller = Menu(interface)

    # run the first controller
    controller.run()

if __name__ == '__main__':
    main()
