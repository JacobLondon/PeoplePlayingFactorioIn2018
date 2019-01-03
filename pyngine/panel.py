import pygame

from pyngine.component import Component

class Panel(Component):

    def __init__(self, interface):
        Component.__init__(self, interface)

    def load(self):
        self.set_anchor()

    def refresh(self):

        if not self.visible:
            return

        x, y = pygame.mouse.get_pos()
        if self.in_component(x, y):
            self.focused = True
        else:
            self.focused = False

        self.draw_component()

    def draw_component(self):

        # draw the area of the panel
        self.interface.draw_area(
            self.anchored_loc[0],
            self.anchored_loc[1],
            self.width,
            self.height,
            self.background)
