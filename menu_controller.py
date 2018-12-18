import pygame

from controller import Controller

class Menu_Controller(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface)

    def open(self):
        from game_controller import Game_Controller
        game = Game_Controller(self.interface)
        game.run()

    # do actions based on what was pressed
    def key_actions(self):
        if self.key_presses[pygame.K_RETURN]:
            self.done = True
