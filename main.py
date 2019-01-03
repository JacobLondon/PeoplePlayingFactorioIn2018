
from pyngine.interface import Interface

from menu_controller import Menu_Controller
from config import settings

def main():

    interface = Interface('PPFI18', tuple(settings.resolution), settings.tile_size, settings.refresh_rate)
    controller = Menu_Controller(interface)

    # run controllers until close
    while controller is not None:
        controller = controller.run()

if __name__ == '__main__':
    main()
