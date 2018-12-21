
from constants import Color, Font, Anchor
from component import Component

class Label(Component):

    def __init__(self, interface, text):
        Component.__init__(self, interface)
        self.text = text

    def refresh(self):
        self.set_anchor()
        self.text_surface = self.font.render(self.text, True, self.foreground, self.background)
        self.interface.display.blit(self.text_surface, self.anchored_loc)
