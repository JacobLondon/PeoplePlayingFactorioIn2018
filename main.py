
from menu_controller import Menu_Controller
from display_interface import Interface
from config import settings

def main():

    interface = Interface('PPFI18')
    controller = Menu_Controller(interface)

    # run controllers until close
    while controller is not None:
        controller = controller.run()

if __name__ == '__main__':
    main()
