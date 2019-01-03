import pygame

from pyngine.constants import Color, Font, Anchor
from pyngine.component import Component
from pyngine.panel import Panel
from pyngine.label import Label
from pyngine.layout import Relative

class Textbox(Component):

    def __init__(self, interface, num_chars=15):
        Component.__init__(self, interface)
        self.num_chars = num_chars

        self.background = Color.white
        self.foreground = Color.black
        self.font = Font.large

        # textbox made with a label on a panel
        self.panel = Panel(interface)

        self.label = Label(interface, self.text)

    def load(self):

        self.width, self.height = self.font.size(' ' * 3 * self.num_chars)
        self.set_anchor()

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
        self.label.loc = self.center_layout.northwest
        self.label.anchor = Anchor.northwest
        self.label.foreground = self.foreground
        self.label.background = None
        self.label.load()

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
        self.panel.refresh()
        self.label.refresh()
