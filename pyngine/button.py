import pygame

from pyngine.constants import Color, Font, Anchor
from pyngine.component import Component
from pyngine.panel import Panel
from pyngine.label import Label
from pyngine.layout import Relative

class Button(Component):

        def __init__(self, interface, text):
            Component.__init__(self, interface)
            self.text = text
            self.scale = 2
            self.background = Color.button
            self.foreground = Color.black
            self.hover = Color.hover
            self.font = Font.button

            # adjust the button to the given scale size
            self.width, self.height = self.font.size(self.text)
            self.width *= self.scale
            self.height *= self.scale

            # button is made with a label on a panel
            self.panel = Panel(interface)

            self.label = Label(interface, self.text)
            self.label.anchor = Anchor.center

        def load(self):

            self.set_anchor()

            # update the panel with button's members
            self.panel.anchor = self.anchor
            self.panel.loc = self.loc
            self.panel.background = self.background
            self.panel.width = self.width
            self.panel.height = self.height
            self.panel.load()

            # update the label with button's members
            self.center_layout = Relative(self.panel)
            self.label.text = self.text
            self.label.font = self.font
            self.label.loc = self.center_layout.center
            self.label.anchor = Anchor.center
            self.label.foreground = self.foreground
            self.label.background = None
            self.label.load()

        def refresh(self):

            if not self.visible:
                return

            # change color based on mouse hovering
            x, y = pygame.mouse.get_pos()
            if self.in_component(x, y):
                self.panel.background = self.hover
                self.focused = True
            else:
                self.panel.background = self.background
                self.focused = False

            self.draw_component()

        def draw_component(self):
            self.panel.refresh()
            self.label.refresh()
