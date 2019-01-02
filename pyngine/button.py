
from pyngine.constants import Color, Font, Anchor
from pyngine.component import Component

class Button(Component):

        def __init__(self, interface, text):
            Component.__init__(self, interface)
            self.text = text
            self.scale = 2
            self.background = Color.button
            self.foreground = Color.black
            self.font = Font.button

        def refresh(self, x, y):

            if not self.visible:
                return

            # button is wider than the text by the scale amount
            self.width, self.height = self.font.size(self.text)
            self.set_anchor()

            # change color based on mouse hovering
            if self.in_component(x, y):
                self.background = Color.hover
                self.focused = True
            else:
                self.background = Color.button
                self.focused = False

            self.draw_component()

        def draw_component(self):

            self.interface.draw_area(
                self.loc[0] - self.width * self.scale / 2,
                self.loc[1] - self.height * self.scale / 2,
                self.width * self.scale,
                self.height * self.scale,
                self.background)

            # draw the text in the component
            self.text_surface = self.font.render(self.text, True, self.foreground, self.background)
            self.interface.display.blit(self.text_surface, self.anchored_loc)

        def in_component(self, x, y):
            left = self.loc[0] - self.width * self.scale / 2
            right = self.loc[0] + self.width * self.scale / 2
            top = self.loc[1] - self.height * self.scale / 2
            bottom = self.loc[1] + self.height * self.scale / 2

            return left <= x <= right and top <= y <= bottom
