import pygame

from controller import Controller

class Menu_Controller(Controller):

    def __init__(self, interface):

        Controller.__init__(self, interface)

        # top right corner X
        if event.type == pygame.QUIT:
            self.done = True

        # player starts doing actions
        elif event.type == pygame.KEYDOWN:
            self.key_presses[event.key] = True

        # player stops doing actions
        elif event.type == pygame.KEYUP:
            self.key_presses[event.key] = False

    # do actions based on what was pressed
    def key_actions(self):
        if self.key_presses[pygame.K_LEFT]:
            self.move(Dir.left, self.player)

        if self.key_presses[pygame.K_RIGHT]:
            self.move(Dir.right, self.player)

        if self.key_presses[pygame.K_UP]:
            self.shoot(Dir.up)

        if self.key_presses[pygame.K_DOWN]:
            self.shoot(Dir.down)
