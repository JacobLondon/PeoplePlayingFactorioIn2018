
from pyngine.constants import Color, Font, Anchor
from pyngine.component import Component

class Label(Component):

    def __init__(self, interface, text):
        Component.__init__(self, interface)
        self.text = text

    def load(self):
        self.width, self.height = self.font.size(self.text)
        self.set_anchor()

    def refresh(self):

        if not self.visible:
            return

        # draw the text to the display
        self.draw_component()

    def draw_component(self):

        # draw the text in the component
        self.text_surface = self.font.render(self.text, True, self.foreground, self.background)
        self.interface.display.blit(self.text_surface, self.anchored_loc)
