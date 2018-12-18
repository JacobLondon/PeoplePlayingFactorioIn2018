
from menu_controller import Menu_Controller
from display_interface import Interface
from config import settings

def main():

    interface = Interface('PPFI18')

    menu = Menu_Controller(interface)
    menu.run()

if __name__ == '__main__':
    main()
