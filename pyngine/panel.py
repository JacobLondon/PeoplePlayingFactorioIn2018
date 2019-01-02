
from pyngine.component import Component

class Panel(Component):

    def __init__(self, interface):
        Component.__init__(self, interface)

    def refresh(self):

        if not self.visible:
            return

        self.set_anchor()
        self.draw_component()

    def draw_component(self):

        self.interface.draw_area(
            self.anchored_loc[0],
            self.anchored_loc[1],
            self.width,
            self.height,
            self.background)
