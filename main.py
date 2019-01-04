
from pyngine.interface import Interface

from menu_controller import Menu_Controller
from config import settings

def main():

    args = ['PPFI18', tuple(settings.resolution), settings.grid_width,
        settings.grid_height, settings.refresh_rate]

    interface = Interface(*args)
    controller = Menu_Controller(interface)

    # run the first controller
    controller = controller.run()

if __name__ == '__main__':
    main()
